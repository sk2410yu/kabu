import sys
sys.path.append(r'C:\Users\MT626\Desktop\独学\株\filter002\sub')


import yfinance as yf
import numpy as np
import pandas as pd
import datetime
from datetime import datetime, timedelta
import os
import time

from function import *
from statistic import *
from my_csv.csv_default import *
from my_csv.csv_function import *
from my_csv.csv_market import *
from points import * 
from show import *
#from statistic_decision import all_decision_df


"""個別銘柄のDF作成
    
"""

"""ADDDFにデータ書き込み
    
"""

"""データ抽出
    
"""



#決算　テクニカル
def day_stockfinancedataget(ticker):
    df_finance=pd.DataFrame()
    # ファンダメンタル情報を取得
    df_finance = day_get_finance_info(ticker)
    return df_finance
           

def day_stockdataget(ticker,end_date,strat_date, periods):
    df = yf.download(ticker, start=strat_date, end=end_date, interval=periods)
    # ダウンロードしたデータフレームが空でないことを確認
    df = get_more_info(df)
    df = get_calculate_trend(df)
    df = get_calculate_oscillator(df)
    std_df= all_statistics_df(df)
    cross_df = all_cross_df(df)

    if periods == "1wk":
        show_data(df , std_df, cross_df, periods) 
        
    if periods == "1d":
        show_data(df , std_df, cross_df, periods) 
    
    if periods == "60m":
        show_data(df , std_df, cross_df, periods) 
    
    if periods == "5m":
        show_data(df , std_df, cross_df, periods) 
    
    return None
    
    
#上２つを動かす
def day_stockanalysis(ticker,end_date):
    #取得
    df_finance = day_stockfinancedataget(ticker)
    if df_finance is None:
        print("ファイナンス情報エラー")
        return None

    day_stockdataget(ticker,end_date,strat_date="1980-1-1",periods="1wk")

    day_stockdataget(ticker,end_date,strat_date="1980-1-1",periods="1d")
    
    start_date = end_date - timedelta(days=725)
    df_hour = day_stockdataget(ticker,end_date,strat_date=start_date,periods="60m")
    
    start_date = end_date - timedelta(days=59)
    df_halfhour = day_stockdataget(ticker,end_date,start_date, periods="5m")
    """APIの限界
    start_date = end_date - timedelta(days=59.99)
    df_fiveminitu =day_stockfinancedataget(ticker,end_date,start_date,periods="5m")
    
    start_date = end_date - timedelta(days=7)
    df_fiveminitu =day_stockfinancedataget(ticker,end_date,start_date,periods="1m")
    """
    
    #接近アラート
    #継続アラートこれらチョイ判定ムズイ
    
    #判定
    
    
    #アラート
    #クロス+クロス統計(移動平均線、MACD)
    #df_cross = all_cross_df(df)
    #add_df =  pd.concat([add_df.reset_index(drop=True), df_cross.reset_index(drop=True)], axis=1)
    #add_df =  pd.concat([add_df.reset_index(drop=True), df_cross.reset_index(drop=True)], axis=1)
    #判定ーとりあえず一定値で判断するとする
    #result_df =all_decision_df(ticker,add_df,result_df)
    
    return None
    
    
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

def Second_serch_stocks(stocklist):
    end_date = datetime.today()
    serch_df = pd.DataFrame()

    for index, ticker in enumerate(stocklist):
        try:
            serch_df = day_stockanalysis(ticker, end_date)  # `stockanalysis` は事前定義された関数を仮定
        except Exception as e:
            print("全然分析できてないよ")
            continue

  
    return serch_df


