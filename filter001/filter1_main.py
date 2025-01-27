import sys
sys.path.append(r'C:\Users\MT626\Desktop\独学\株\filter001')

"日経情報全般の読み込みを終わらせる"

"その後デフォルト設定の変更確認"

"お気に入りの実行の有無"
"配当の実行の有無"
"サーチの実行の有無"

from prepare import *
from sub import *
import time
"""
ここでマーケっととばす
検索銘柄してい
subに飛ばしサーチ

別に飛んで分析かける"""
def filter1():
    start_time = time.time()

    if check_market_info() is not True:
        marketinfo()
    
    file_name = 'stocknumber_1month.csv'  # CSVファイル名（親ディレクトリからの相対パス）
    result = read_csv_to_list(file_name)
    defaul_name ="Default.csv"
    max_price,min_price, min_volume ,dividend_status, target_yield = read_csv_to_default(defaul_name)

    aaalist=["9101.T","9104.T"]
    serch_df = First_filter_stocks(aaalist,max_price,min_price,min_volume, dividend_status, target_yield)
    
    
    tick_dict = First_select_stocks(serch_df)
    tick_list = First_count_duplicates(tick_dict)
    end_time = time.time()
    print(f"フィルター1実行時間: {end_time - start_time:.4f} 秒")

    return tick_list

