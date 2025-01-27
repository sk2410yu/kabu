import pandas as pd
import os

def read_csv_to_list(file_name):
    # 親ディレクトリを取得し、一つ下のフォルダに移動
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, file_name)
    
    # CSVファイルを読み込む
    df = pd.read_csv(file_path, encoding='shift_jis')

     # 特定のコラムをリストに変換し、その数値に .T を付加する
    if 'コード' in df.columns:  # 'target_column' は目的の列名に置き換えてください
        # リストに変換
        stocknumber_list = df['コード'].apply(lambda x: f"{x}.T").tolist()
        #stocknumber_list = stocknumber_list[:300]
    return stocknumber_list

def read_csv_to_default(file_name):
    # 親ディレクトリを取得し、一つ下のフォルダに移動
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, file_name)
    
    # CSVファイルを読み込む
    df_default = pd.read_csv(file_path, encoding='UTF-8')

    max_price = df_default['最大価格'][0]
    min_price = df_default['最小価格'][0]
    min_volume = df_default["最小出来高"][0]
    dividend_status = df_default['配当の有無'][0]
    target_yield = df_default['希望配当利回り'][0]
    return max_price,min_price,min_volume, dividend_status, target_yield