import numpy as np
import pandas as pd

def all_statistics_df(df):
    # 属性名取得
    column_names = list(df.columns)
    
    # 削除したい要素を指定
    elements_to_remove = ['Open','High','Close','Low','Adj Close', 'Volume','Signal_Line']

    # リストから削除
    column_names = [item for item in column_names if item not in elements_to_remove]
    
    # 結果を格納する辞書を初期化
    stats_dict = {}
    
    # 各列の統計データを計算して辞書に追加
    for column in column_names:
        percentile = calculate_column_percentile(df[column])
        current_deviation = calculate_column_stats(df[column])
        # 統計データを辞書に追加
        stats_dict[f"{column}_Percentile"] = percentile
        stats_dict[f"{column}_Current Deviation"] = current_deviation
    
    # 結果を一行のデータフレームに変換
    df_stats = pd.DataFrame([stats_dict])
    
    return df_stats

def calculate_column_percentile(data_series):
    """指定したカラムのパーセンタイルを計算"""
    last_value = data_series.dropna().iloc[-1]  # 最新の値
    percentile = (np.sum(data_series < last_value) / len(data_series.dropna())) * 100 if len(data_series.dropna()) > 0 else 0
    return percentile

def calculate_column_stats(data_series):
    """指定したカラムの合計、平均、偏差、現在の偏差を計算"""
    clean_series = data_series.dropna()  # 欠損値を除去
    #長さにかえる

    mean = clean_series.mean()
    std_dev = clean_series.std()
    
    # 現在の偏差 (最新の値 - 平均)
    last_value = clean_series.iloc[-1]
    current_deviation = (last_value - mean)/std_dev
    
    return current_deviation