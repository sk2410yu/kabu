"""モデルの学習・評価・保存・推論。

- 時系列split（日付で前半=学習 / 後半=検証）でリークを避けて評価
- 指標は AUC / 正答率 と「上位K銘柄の平均フォワードリターン」(簡易バックテスト)
- HistGradientBoosting を使用（欠損に強く高速。重い依存を増やさない）
"""
import os

import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import accuracy_score, roc_auc_score

from .features import FEATURE_COLUMNS, add_features
from .dataset import download_prices

_DEFAULT_MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   "model.joblib")


def time_split(data, test_frac=0.2, embargo=0):
    """日付ベースで学習/検証に分割（シャッフルしない＝ウォークフォワード）。

    embargo: 学習/検証の境界で、検証開始日の直前 embargo 取引日を学習から除外する。
    ラベルが shift(-horizon) で未来を参照するため、境界での情報リークを防ぐ。
    """
    data = data.sort_values("date")
    dates = np.sort(data["date"].unique())
    n = len(dates)
    cut_idx = int(n * (1 - test_frac))
    cut_idx = min(max(cut_idx, 1), n - 1)
    test_start_date = dates[cut_idx]

    train_end_idx = cut_idx - max(0, embargo)
    if train_end_idx <= 0:
        train = data.iloc[0:0]
    else:
        train_end_date = dates[train_end_idx - 1]
        train = data[data["date"] <= train_end_date]
    test = data[data["date"] >= test_start_date]
    return train, test


def topk_backtest(test, k_frac=0.2):
    """各検証日でスコア上位 k_frac の銘柄を買った場合の平均フォワードリターン。

    全銘柄平均と比較し、モデルのランキングが有効かを見る。
    """
    top_returns = []
    all_returns = []
    for _, group in test.groupby("date"):
        if len(group) < 2:
            continue
        k = max(1, int(round(len(group) * k_frac)))
        top = group.nlargest(k, "score")
        top_returns.append(top["fwd_return"].mean())
        all_returns.append(group["fwd_return"].mean())
    if not top_returns:
        return {"top_mean_return": float("nan"), "all_mean_return": float("nan"),
                "edge": float("nan"), "n_dates": 0}
    top_mean = float(np.mean(top_returns))
    all_mean = float(np.mean(all_returns))
    return {
        "top_mean_return": top_mean,
        "all_mean_return": all_mean,
        "edge": top_mean - all_mean,
        "n_dates": len(top_returns),
    }


def train_and_evaluate(data, test_frac=0.2, k_frac=0.2, horizon=5,
                       random_state=42, **model_kwargs):
    """データセットを学習し、検証指標とともに (model, metrics) を返す。

    horizon: ラベルのフォワード日数。境界リーク防止の embargo に使う。
    """
    if data.empty:
        raise ValueError("データセットが空です。銘柄リストや取得期間を確認してください。")

    train, test = time_split(data, test_frac=test_frac, embargo=horizon)
    if train.empty or test.empty:
        raise ValueError("時系列splitで学習/検証のどちらかが空になりました。")

    params = dict(max_depth=3, learning_rate=0.05, max_iter=300,
                  l2_regularization=1.0, random_state=random_state)
    params.update(model_kwargs)
    model = HistGradientBoostingClassifier(**params)

    X_train, y_train = train[FEATURE_COLUMNS], train["target"]
    X_test, y_test = test[FEATURE_COLUMNS], test["target"]
    model.fit(X_train, y_train)

    proba = model.predict_proba(X_test)[:, 1]
    metrics = {
        "n_train": int(len(train)),
        "n_test": int(len(test)),
        "train_pos_rate": float(y_train.mean()),
        "test_pos_rate": float(y_test.mean()),
        "auc": float(roc_auc_score(y_test, proba)) if y_test.nunique() > 1 else float("nan"),
        "accuracy": float(accuracy_score(y_test, (proba > 0.5).astype(int))),
    }

    test = test.copy()
    test["score"] = proba
    metrics["backtest"] = topk_backtest(test, k_frac=k_frac)
    return model, metrics


def save_model(model, path=_DEFAULT_MODEL_PATH):
    joblib.dump({"model": model, "features": FEATURE_COLUMNS}, path)
    return path


def load_model(path=_DEFAULT_MODEL_PATH):
    obj = joblib.load(path)
    return obj["model"]


def score_latest(tickers, model, start="2015-01-01", interval="1d"):
    """学習済みモデルで各銘柄の最新時点の上昇確率を算出し、降順で返す。

    返り値: DataFrame[['ticker','date','ml_score', *FEATURE_COLUMNS]]
    """
    price_map = download_prices(tickers, start=start, interval=interval)
    rows = []
    feats = []
    for ticker, df in price_map.items():
        if df is None or df.empty:
            continue
        df = add_features(df)
        last = df.dropna(subset=FEATURE_COLUMNS)
        if last.empty:
            continue
        last = last.iloc[-1]
        rows.append({"ticker": ticker, "date": pd.to_datetime(df.index[-1])})
        feats.append(last[FEATURE_COLUMNS].to_dict())

    if not rows:
        return pd.DataFrame(columns=["ticker", "date", "ml_score"] + FEATURE_COLUMNS)

    feat_df = pd.DataFrame(feats)[FEATURE_COLUMNS]
    proba = model.predict_proba(feat_df)[:, 1]
    out = pd.DataFrame(rows)
    out["ml_score"] = proba
    out = pd.concat([out.reset_index(drop=True), feat_df.reset_index(drop=True)], axis=1)
    return out.sort_values("ml_score", ascending=False).reset_index(drop=True)
