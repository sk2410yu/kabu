"""学習用データセットの構築。

各銘柄・各日付について特徴量を計算し、翌 horizon 営業日の
フォワードリターン（と上昇/下落ラベル）を付与する。
未来情報リーク防止のため、ラベルは shift(-horizon) で作る。
"""
import numpy as np
import pandas as pd
import yfinance as yf

from .features import FEATURE_COLUMNS, add_features


def _flatten(df):
    if isinstance(df.columns, pd.MultiIndex):
        df = df.copy()
        df.columns = df.columns.get_level_values(0)
    return df


def download_prices(tickers, start="2015-01-01", end=None, interval="1d",
                    max_workers=10):
    """複数銘柄の価格履歴を一括取得し {ticker: DataFrame(単層列)} を返す。"""
    result = {}
    tickers = list(tickers)
    if not tickers:
        return result

    data = yf.download(
        tickers,
        start=start,
        end=end,
        interval=interval,
        group_by="ticker",
        threads=max_workers,
        auto_adjust=True,
        progress=False,
    )

    if len(tickers) == 1:
        result[tickers[0]] = _flatten(data)
        return result

    for ticker in tickers:
        try:
            sub = data[ticker].dropna(how="all")
        except (KeyError, TypeError):
            sub = None
        result[ticker] = sub
    return result


def build_dataset(tickers, horizon=5, start="2015-01-01", end=None,
                  interval="1d", min_rows=120):
    """特徴量 + フォワードリターンラベルの長表（long-format）を返す。

    返り値の列: ['date','ticker', *FEATURE_COLUMNS, 'fwd_return','target']
    """
    price_map = download_prices(tickers, start=start, end=end, interval=interval)

    frames = []
    for ticker, df in price_map.items():
        if df is None or df.empty or len(df) < min_rows:
            continue
        df = add_features(df)
        # 翌 horizon 営業日のリターン（リーク防止のため未来側を参照）
        df["fwd_return"] = df["Close"].shift(-horizon) / df["Close"] - 1
        df["target"] = (df["fwd_return"] > 0).astype(int)
        df["ticker"] = ticker
        df["date"] = pd.to_datetime(df.index)
        frames.append(df[["date", "ticker"] + FEATURE_COLUMNS + ["fwd_return", "target"]])

    if not frames:
        return pd.DataFrame(columns=["date", "ticker"] + FEATURE_COLUMNS + ["fwd_return", "target"])

    data = pd.concat(frames, ignore_index=True)
    # 欠損・無限大を除去（指標のウォームアップ期間や末尾のラベル欠損を落とす）
    data = data.replace([np.inf, -np.inf], np.nan)
    data = data.dropna(subset=FEATURE_COLUMNS + ["fwd_return"]).reset_index(drop=True)
    return data
