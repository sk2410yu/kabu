import numpy as np
import pandas as pd


def all_statistics_df(df):
    # 属性名取得
    column_names = ['Price_Change_Percent','High_percent','Low_percent','Price_width_Percent','Volume', 'MACD', 'Signal_Line', 'MACD_Signal_difference', "MA_band", 
                    'DI+','DI-','ADX','ADX-R','Parabolic_SAR', 'RSI_9', 'RSI_14', '%K', '%K_smooth', 
                    '%D', 'Psychological_Line', 'RCI_9', 'RCI_14', 'RCI_26', 'MA_Deviation']
    
    # 結果を格納する辞書を初期化
    stats_dict = {}
    
    # 各列の統計データを計算して辞書に追加
    for column in column_names:
        percentile = calculate_column_percentile(df[column])
        q1, median, q3 = calculate_quartiles(df[column])
        total, mean, std_dev, current_deviation = calculate_column_stats(df[column])
        
        # 統計データを辞書に追加
        stats_dict[f"{column}_Percentile"] = percentile
        stats_dict[f"{column}_Q1"] = q1
        stats_dict[f"{column}_Median"] = median
        stats_dict[f"{column}_Q3"] = q3
        stats_dict[f"{column}_Total"] = total
        stats_dict[f"{column}_Mean"] = mean
        stats_dict[f"{column}_Standard Deviation"] = std_dev
        stats_dict[f"{column}_Current Deviation"] = current_deviation
    
    # 結果を一行のデータフレームに変換
    df_stats = pd.DataFrame([stats_dict])
    
    return df_stats

def calculate_column_percentile(data_series):
    """指定したカラムのパーセンタイルを計算"""
    last_value = data_series.dropna().iloc[-1]  # 最新の値
    percentile = (np.sum(data_series < last_value) / len(data_series.dropna())) * 100 if len(data_series.dropna()) > 0 else 0
    return percentile

def calculate_quartiles(data_series):
    """指定したカラムの四分位数を計算"""
    q1 = data_series.dropna().quantile(0.25)
    median = data_series.dropna().quantile(0.5)
    q3 = data_series.dropna().quantile(0.75)
    return q1, median, q3

def calculate_column_stats(data_series):
    """指定したカラムの合計、平均、偏差、現在の偏差を計算"""
    clean_series = data_series.dropna()  # 欠損値を除去
    #長さにかえる
    total = len(clean_series)
    mean = clean_series.mean()
    std_dev = clean_series.std()
    
    # 現在の偏差 (最新の値 - 平均)
    last_value = clean_series.iloc[-1]
    current_deviation = (last_value - mean)/std_dev
    
    return total, mean, std_dev, current_deviation