import sys
sys.path.append(r'C:\Users\MT626\Desktop\独学\株\filter001\sub')

import yfinance as yf
import pandas as pd
import datetime
from datetime import datetime
import os
from concurrent.futures import ThreadPoolExecutor

from onedaymarket import *
from function import *
from statistic import *
from my_csv.csv_default import *
from my_csv.csv_function import *
from my_csv.csv_market import *
from my_csv.csv_stock import *


"""個別銘柄のDF作成
    
"""

"""ADDDFにデータ書き込み
    
"""

"""データ抽出
    
"""

def marketinfo():
    market_ticker=["^N225", "^TOPX", "^N300", "^VIX", "JPY=X"]
    all_data =fetch_and_process_data(market_ticker)
    all_data = calculate_nt_ratio(all_data)
    all_data = save_to_excel(all_data)
    return None

#決算　テクニカル
def stockfinancedataget(ticker,max_price,min_price,min_volume, dividend_status, target_yield, financedatage=0):
    df_finance=pd.DataFrame()
    if financedatage ==0:
    # ファンダメンタル情報を取得
        df_finance = get_finance_info(ticker,max_price,min_price,min_volume, dividend_status, target_yield)
    return df_finance
           

# 並列実行のワーカー数（I/Oバウンドのため大きめでも可。APIレート制限に注意）
DEFAULT_MAX_WORKERS = 10


def _flatten_columns(df):
    """yfinanceのMultiIndex列（フィールド, ティッカー）を単層列に正規化する。"""
    if isinstance(df.columns, pd.MultiIndex):
        df = df.copy()
        df.columns = df.columns.get_level_values(0)
    return df


def download_prices_batch(tickers, end_date, max_workers=DEFAULT_MAX_WORKERS):
    """複数銘柄の価格履歴を一括取得し、{ticker: DataFrame(単層列)} を返す。

    銘柄ごとに yf.download を呼ぶ代わりに1回のリクエストでまとめて取得するため、
    通信回数を大幅に削減できる。
    """
    result = {}
    if not tickers:
        return result

    data = yf.download(
        tickers,
        start="1980-1-1",
        end=end_date,
        interval="5d",
        group_by="ticker",
        threads=max_workers,
        progress=False,
    )

    # 単一銘柄のときは group_by が効かず単層列で返るため個別に扱う
    if len(tickers) == 1:
        result[tickers[0]] = _flatten_columns(data)
        return result

    for ticker in tickers:
        try:
            sub = data[ticker].dropna(how="all")
        except (KeyError, TypeError):
            sub = None
        result[ticker] = sub
    return result


def stockdataget(ticker,end_date,dataget=0,):
    df = yf.download(ticker, start="1980-1-1", end=end_date, interval="5d")
    # MultiIndex列を単層に正規化（新しいyfinance互換）
    df = _flatten_columns(df)
    # ダウンロードしたデータフレームが空でないことを確認
    #df = get_more_info(df)
    if dataget == 0:
        df = get_calculate_trend(df)
        df = get_calculate_oscillator(df)
    return df 
        
#上２つを動かす
def stockanalysis(ticker,end_date,add_df,price_outlist, price_inlist,max_price,min_price, min_volume,dividend_status, target_yield,analysis=0):
    #取得
    df_finance = stockfinancedataget(ticker,max_price,min_price,min_volume, dividend_status, target_yield)
    if df_finance is None:
        price_outlist.append(ticker)
        return None
    price_inlist.append(ticker)
    df = stockdataget(ticker,end_date)
    #基本的情報追加
    # df の最終行を取得
    last_row_df = df.tail(1).round(3)
    # df_finance と last_row_df を列方向で結合
    add_df = pd.concat([df_finance.reset_index(drop=True), last_row_df.reset_index(drop=True)], axis=1)
    
    #%+四分位+個数、合計、偏差、現在偏差
    df_vix = all_statistics_df(df).round(3)
    add_df =  pd.concat([add_df.reset_index(drop=True), df_vix.reset_index(drop=True)], axis=1)
    #クロス+クロス統計(移動平均線、MACD)
    df_cross = all_cross_df(df)
    add_df =  pd.concat([add_df.reset_index(drop=True), df_cross.reset_index(drop=True)], axis=1)    
    
    return add_df,price_outlist,price_inlist
    
# データフレームをCSVとして保存する関数
def save_dataframe_to_csv(df, filename=None):
    # 実行日と時間を基にファイル名を生成
    if filename is None:
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"result/{current_time}.csv"
    else:
        filename = f"{filename}.csv"
    # ディレクトリが存在しない場合は作成
    os.makedirs("result", exist_ok=True)
    
    # データフレームをCSVファイルとして保存
    df.to_csv(filename, index=False, encoding="shift-jis")
    
    print(f"CSVファイルが保存されました: {filename}")


    """このあと基本的情報設定
    """

# 個別銘柄の指標DFを組み立てる（CPU処理。価格DFはダウンロード済みのものを使う）
def build_stock_row(ticker, price_df, df_finance):
    if price_df is None or price_df.empty:
        return None
    df = _flatten_columns(price_df)
    df = get_calculate_trend(df)
    df = get_calculate_oscillator(df)
    # df の最終行を取得
    last_row_df = df.tail(1).round(3)
    # df_finance と last_row_df を列方向で結合
    add_df = pd.concat([df_finance.reset_index(drop=True), last_row_df.reset_index(drop=True)], axis=1)
    #%+四分位+個数、合計、偏差、現在偏差
    df_vix = all_statistics_df(df).round(3)
    add_df = pd.concat([add_df.reset_index(drop=True), df_vix.reset_index(drop=True)], axis=1)
    #クロス+クロス統計(移動平均線、MACD)
    df_cross = all_cross_df(df)
    add_df = pd.concat([add_df.reset_index(drop=True), df_cross.reset_index(drop=True)], axis=1)
    return add_df


# sub_main においてのメイン関数はこれとなる
def First_filter_stocks(stocklist,max_price,min_price,min_volume, dividend_status, target_yield, max_workers=DEFAULT_MAX_WORKERS):
    end_date = datetime.today()
    stock_unlist = []
    price_inlist = []
    price_outlist = []
    finance_map = {}

    # フェーズ1: ファンダ情報の取得・条件判定を並列実行
    # （銘柄ごとに .info / .history を直列で叩いていた最重量のネットワーク処理を並列化）
    def _screen(ticker):
        try:
            return ticker, stockfinancedataget(
                ticker, max_price, min_price, min_volume, dividend_status, target_yield
            ), None
        except Exception as e:  # noqa: BLE001 個別銘柄のAPIエラーは握りつぶしつつ記録
            return ticker, None, e

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # map は入力順を保つため、結果の並び順は元のループと同じになる
        for ticker, df_finance, err in executor.map(_screen, stocklist):
            if err is not None:
                stock_unlist.append(ticker)
                continue
            if df_finance is None or df_finance.empty:
                price_outlist.append(ticker)
            else:
                price_inlist.append(ticker)
                finance_map[ticker] = df_finance

    print(f"ファンダ条件通過: {len(price_inlist)}銘柄 / 価格履歴を一括取得します")

    # フェーズ2: 条件通過した銘柄の価格履歴を一括ダウンロード（通信回数を激減）
    price_map = download_prices_batch(price_inlist, end_date, max_workers=max_workers)

    # フェーズ3: 指標を計算して行を組み立て、最後に一度だけ concat（ループ内concatのO(n^2)を解消）
    rows = []
    for ticker in price_inlist:
        try:
            add_df = build_stock_row(ticker, price_map.get(ticker), finance_map[ticker])
        except Exception:  # noqa: BLE001 指標計算で落ちた銘柄は除外
            stock_unlist.append(ticker)
            continue
        if add_df is not None and not add_df.empty:
            rows.append(add_df)

    serch_df = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()

    save_dataframe_to_csv(serch_df)
    save_to_excel_stock(serch_df)

    # 結果を表示
    print(f"{len(stock_unlist)}がAPIによるエラーが発生した。")
    print(f"{len(price_inlist)}が条件に該当しました")
    print(f"{len(price_outlist)}を条件により排除しました")

    return serch_df

def add_ml_score(serch_df, model_path=None, start="2015-01-01", interval="1d"):
    """serch_df の各銘柄に、学習済みモデルの上昇確率を 'MLスコア' 列として付与する。

    ml/ の依存（scikit-learn 等）や学習済みモデルが無い場合は、警告を出して
    serch_df をそのまま返す（第1フィルター本体は ML 無しでも動作する）。
    `python -m ml.run_ml train` でモデルを作成しておくこと。
    """
    if serch_df is None or serch_df.empty or "銘柄番号" not in serch_df.columns:
        return serch_df

    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    try:
        from ml.model import load_model, score_latest
    except Exception as e:  # noqa: BLE001 ml依存が無くても本体は動かす
        print(f"MLスコアをスキップ（ml/ の読み込みに失敗）: {e}")
        return serch_df

    path = model_path or os.path.join(repo_root, "ml", "model.joblib")
    if not os.path.exists(path):
        print(f"MLスコアをスキップ（モデル未学習: {path}）。"
              f"`python -m ml.run_ml train` で作成してください。")
        return serch_df

    try:
        model = load_model(path)
        tickers = serch_df["銘柄番号"].astype(str).tolist()
        ranked = score_latest(tickers, model, start=start, interval=interval)
        score_map = dict(zip(ranked["ticker"].astype(str), ranked["ml_score"]))
        serch_df = serch_df.copy()
        serch_df["MLスコア"] = serch_df["銘柄番号"].astype(str).map(score_map)
        print(f"MLスコアを付与しました（{serch_df['MLスコア'].notna().sum()}/{len(serch_df)}銘柄）")
    except Exception as e:  # noqa: BLE001 スコア計算失敗時も本体は継続
        print(f"MLスコア計算でエラー: {e}")
    return serch_df


def First_select_stocks(df):
    """
    データフレーム内の指定された要素でランキングを作成し、
    上昇・下降用のランキング辞書を作成する。

    Args:
        df (pd.DataFrame): データフレーム（'ticker'を含む必要がある）

    Returns:
        dict: 上昇と下降用のランキング辞書
    """
    # ランキング対象のカラムを定義
    ascending_elements = ['MACD_Percentile','MACD_Current Deviation','MACD_Signal_difference_Percentile',
        'MACD_Signal_difference_Current Deviation','DI+_Percentile','DI+_Current Deviation',
        'DI-_Percentile','DI-_Current Deviation','DI+DI-_difference_Percentile',
        'DI+DI-_difference_Current Deviation','Parabolic_SAR_Percentile','Parabolic_SAR_Current Deviation',
        'RSI_14_Percentile','RSI_14_Current Deviation','%K_Percentile','%K_Current Deviation',
        'Psychological_Line_Percentile','Psychological_Line_Current Deviation','RCI_26_Percentile',
        'RCI_26_Current Deviation','MA_Deviation_Percentile','MA_Deviation_Current Deviation'] # 小さい値が上位
    
    descending_elements = ["MACD_Signal_difference",'MACD_Signal_Line_Next_Cross_Day',
                           'DI+_DI-_Next_Cross_Day']  # 大きい値が上位

    # MLスコア（上昇確率）が付与されていればランキング基準に加える（大きいほど上位）
    if 'MLスコア' in df.columns:
        descending_elements = descending_elements + ['MLスコア']

    result={}

    # 上昇用ランキング作成
    for element in ascending_elements:
        sorted_df = df.sort_values(by=element, ascending=True)
        sorted_df = sorted_df.head(20)
        ranked_list = sorted_df['銘柄番号'].tolist()
        result[element] = ranked_list

    # 下降用ランキング作成
    for element in descending_elements:
        sorted_df = df.sort_values(by=element, ascending=False)
        sorted_df = sorted_df.head(20)
        ranked_list = sorted_df['銘柄番号'].tolist()
        result[element] = ranked_list
        
    return result

def First_count_duplicates(data):
    # 全ての値をリストにまとめる
    all_values = []
    for values in data.values():
        all_values.extend(values)
    
    # 値のカウントを行う
    from collections import Counter
    counts = Counter(all_values)
    
    # 結果をリスト形式に変換
    result = [(key, count) for key, count in counts.items()]
    result = sorted(result, key=lambda x: x[1], reverse=True)
    return result