import pandas as pd

def all_up_down_df(df):
    """
    DataFrameの各カラムについて、隣り合う値が上昇または下降している回数の統計を一行で取得する関数。
    
    Parameters:
    df (pd.DataFrame): 各カラムにデータが含まれたデータフレーム
    
    Returns:
    pd.DataFrame: 各カラムの上昇・下降回数の統計を一行で格納したデータフレーム
    """
    # 属性名取得
    column_names = list(df.columns)
    
    # 削除したい要素を指定
    elements_to_remove = ['Open','High','Low','Adj Close', 'Volume','Signal_Line']

    # リストから削除
    column_names = [item for item in column_names if item not in elements_to_remove]
    
    # 結果を格納する辞書を初期化
    up_down_counts = {}

    # 各列の上昇・下降回数を計算して辞書に追加
    for column in column_names:
        differences = df[column].diff().iloc[1:]  # 隣り合う値の差分を取得
        up_count = (differences > 0).sum()  # 上昇回数
        down_count = (differences < 0).sum()  # 下降回数
        
        # 辞書に結果を格納
        up_down_counts[f"{column}_up"] = up_count
        up_down_counts[f"{column}_down"] = down_count
    
    # 結果を一行のデータフレームに変換
    df_up_down_stats = pd.DataFrame([up_down_counts])
    
    return df_up_down_stats