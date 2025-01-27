
import sys
sys.path.append(r'C:\Users\MT626\Desktop\独学\株\filter002\sub')

from sub import *
"""
このコードはお気に入りコードと
個別銘柄コードについてリストにいれ
瞬間時にその日トレンドしていかをまとめるDay_serch関数と
1時間と5分テクニカルで分析するDay_sort関数となる
"""









def filter2(ticker):
    start_time = time.time()


    aaalist=["9101.T","9104.T"]
    serch_df = Second_filter_stocks(ticker)
    
    tick_dict = Second_select_stocks(serch_df)
    tick_list = Second_count_duplicates(tick_dict)
    end_time = time.time()
    print(f"フィルター1実行時間: {end_time - start_time:.4f} 秒")

    return tick_list


start_time = time.time()

aaalist=["9101.T"]
serch_df =Day_serch_stocks(aaalist)
#Final_df = Second_serch_stocks(serch_df)
#順張り時需給悪(信用悪が一番クソ)
#決算ボリンジャーバンドは需給がいい銘柄だけ
#
#
end_time = time.time()
print(f"Execution time: {end_time - start_time:.4f} seconds")