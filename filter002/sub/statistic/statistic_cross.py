import pandas as pd
import numpy as np


def all_cross_df(df):
    cross_list = [
        ("ma5", "ma20"), ("ma5", "ma50"), ("ma5", "ma75"), ("ma5", "ma100"), ("ma5", "ma200"),
        ("ma20", "ma50"), ("ma20", "ma75"), ("ma20", "ma100"), ("ma20", "ma200"), ("ma50", "ma75"),
        ("ma50", "ma100"), ("ma50", "ma200"), ("ma75", "ma100"), ("ma75", "ma200"), ("ma100", "ma200"), ("MACD", "Signal_Line")
    ]
    
    # 結果を格納する辞書を初期化
    cross_stats_dict = {}

    for columns1, columns2 in cross_list:
        # クロス判定
        golden_cross_col = f'Golden_Cross_{columns1}_{columns2}'
        dead_cross_col = f'Dead_Cross_{columns1}_{columns2}'

        df[golden_cross_col] = (df[columns1] > df[columns2]) & (df[columns1].shift(1) <= df[columns2].shift(1))
        df[dead_cross_col] = (df[columns1] < df[columns2]) & (df[columns1].shift(1) >= df[columns2].shift(1))

        # 発生回数をカウント
        golden_cross_count = df[golden_cross_col].sum()
        dead_cross_count = df[dead_cross_col].sum()

        # 発生日のリストを作成
        golden_cross_dates = df.index[df[golden_cross_col]].tolist()
        dead_cross_dates = df.index[df[dead_cross_col]].tolist()

        golden_day_list = calculate_true_intervals(golden_cross_dates)
        dead_day_list = calculate_true_intervals(dead_cross_dates)

        # 各クロスの平均日数
        golden_day_avg = np.mean(golden_day_list) if golden_day_list else float('inf')
        dead_day_avg = np.mean(dead_day_list) if dead_day_list else float('inf')

        # 最後のクロスを判定
        if golden_cross_dates and (not dead_cross_dates or golden_cross_dates[-1] > dead_cross_dates[-1]):
            last_cross_type = 'Golden'
            last_cross_date = golden_cross_dates[-1]
        elif dead_cross_dates:
            last_cross_type = 'Dead'
            last_cross_date = dead_cross_dates[-1]
        else:
            last_cross_type = 'None'
            last_cross_date = None

        # 最後のクロスからの経過日数を計算
        last_cross_days_ago = (df.index[-1] - last_cross_date).days if last_cross_date else None

        # 平均日数との比較
        if last_cross_days_ago is not None:
            if last_cross_type == 'Golden' and last_cross_days_ago < golden_day_avg:
                closest_cross = 'Golden'
            elif last_cross_type == 'Dead' and last_cross_days_ago < dead_day_avg:
                closest_cross = 'Dead'
            else:
                closest_cross = 'Neither (average exceeded)'
        else:
            closest_cross = 'No recent cross'

        # 結果を辞書に追加
        cross_stats_dict[f"{columns1}_{columns2}_Last_Cross"] = last_cross_type
        cross_stats_dict[f"{columns1}_{columns2}_Last_Cross_Day"] = last_cross_days_ago
        cross_stats_dict[f"{columns1}_{columns2}_Next_Cross_Day"] = closest_cross
        cross_stats_dict[f"{columns1}_{columns2}_Golden_Count"] = golden_cross_count
        cross_stats_dict[f"{columns1}_{columns2}_Golden_Count_Avg"] = golden_day_avg
        cross_stats_dict[f"{columns1}_{columns2}_Dead_Count"] = dead_cross_count
        cross_stats_dict[f"{columns1}_{columns2}_Dead_Count_Avg"] = dead_day_avg

    # 結果を一行のデータフレームに変換
    df_cross = pd.DataFrame([cross_stats_dict])

    return df_cross
        


def calculate_true_intervals(true_indices):
    """
    Trueの出現間隔を計算し、日数を抽出してリストとして返す関数。

    Parameters:
    true_indices (list): Trueのインデックスのリスト

    Returns:
    list: Trueの出現間隔（日数）のリスト
    """
    if len(true_indices) > 1:
        intervals = np.diff(true_indices)
    else:
        intervals = np.array([])  # Trueが1つ以下の場合は空配列

    # days部分を抽出してリストに変換
    days_list = [td.days for td in intervals]

    return days_list
