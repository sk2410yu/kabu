import sys
sys.path.append(r'C:\Users\MT626\Desktop\独学\株\filter001\sub')

import yfinance as yf
import pandas as pd
import datetime
from datetime import datetime
import os

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
           

def stockdataget(ticker,end_date,dataget=0,):
    df = yf.download(ticker, start="1980-1-1", end=end_date, interval="5d",period='1d')
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

# sub_main においてのメイン関数はこれとなる
def First_filter_stocks(stocklist,max_price,min_price,min_volume, dividend_status, target_yield):
    end_date = datetime.today()
    stock_unlist =[]
    price_inlist =[]
    price_outlist=[]
    stock_unlist = []
    serch_df = pd.DataFrame()
    total_tickers = len(stocklist)

    for index, ticker in enumerate(stocklist):
        print(index)
        add_df = pd.DataFrame()
        try:
            add_df,price_outlist,price_inlist = stockanalysis(ticker, end_date, add_df,price_outlist,price_inlist,max_price,min_price,min_volume, dividend_status, target_yield)  # `stockanalysis` は事前定義された関数を仮定
        except Exception as e:
            stock_unlist.append(ticker)
            continue

        if add_df is not None and not add_df.empty:
            serch_df = pd.concat([serch_df, add_df], ignore_index=True)

        # 進捗を10%ごとに表示
        percentage = (index + 1) * 100 // total_tickers
        if percentage % 10 == 0 and percentage != 0:
            print(f"{percentage}% 完了")
        
        #ここまで個別調査のＡＰＩが繰り返しされこれ以降一回の実行
    save_dataframe_to_csv(serch_df)
    save_to_excel_stock(serch_df)

    # 結果を表示
    print(f"{len(stock_unlist)}がAPIによるエラーが発生した。")
    print(f"{len(price_inlist)}が条件に該当しました")
    print(f"{len(price_outlist)}を条件により排除しました")
    
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