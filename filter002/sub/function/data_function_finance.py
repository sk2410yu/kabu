import yfinance as yf 
import pandas as pd
from datetime import datetime, date,timedelta
"現在株価,bps,eps,roe,自己資本比率,per,pbr,配当利回り"


today=date.today()

def day_get_finance_info(ticker):
    # Ticker オブジェクトを作成
    
    stock = yf.Ticker(ticker)
    
    # 株価の履歴を取得
    # 決算日を取得(辞書型)
    price  = stock.history(period="1d")["Close"].iloc[-1]
    calender =stock.calendar
    
    near_earning =calender['Earnings Date']
    #デフォルトでリストに入っているので型変更
    near_earning = near_earning[0]
    near_earnig_difference,near_earning_obj=change_date2(near_earning,today)
    
    info = stock.info
    volume_day10= info.get("averageVolume10days", None)
    
    dividend_last = info.get("trailingAnnualDividendRate", None)
  
    this_year_yield =info.get("dividendYield", None)

    

    # 配当落ち日と株分割日を取得し、日付形式に変換
    # 配当落ち日は約一か月立つまで過去のになる(計算結果としてはマイナス)
    ex_dividend_date = info.get("exDividendDate", None)
    last_split_date = info.get("lastSplitDate", None)
    if ex_dividend_date is not None:
        ex_dividend_date = datetime.strftime(datetime.fromtimestamp(ex_dividend_date), '%Y-%m-%d')
        ex_dividend_date_obj = change_date(ex_dividend_date)
        # 日付の差を計算
        ex_dividend_date_difference,ex_dividend_date_obj =change_date2(ex_dividend_date_obj,today)
    else:
        ex_dividend_date_difference,ex_dividend_date_obj= None, None
        
    if last_split_date is not None:
        last_split_date = datetime.strftime(datetime.fromtimestamp(last_split_date), '%Y-%m-%d')
        last_split_date_obj = change_date(last_split_date)
        # 日付の差を計算
        last_split_date_difference,last_split_date_obj=change_date2(last_split_date_obj,today)
    else:
        last_split_date_difference,last_split_date_obj = None, None
        
    #ここまで金額、配当の有無、希望配当利回りでの該当銘柄判定と
    #日にちデータの整理と当日との差を計算
    #そして日にちによる該当銘柄判定を行った

    # 各種情報の取得（日本語でのキー名）
    new_row = {
        "銘柄番号": ticker,
        "現在価格": price,
        "決算日":near_earning_obj,
        "決算日まで":near_earnig_difference,
        "配当落ち日": ex_dividend_date_obj,
        "権利落ちまで":ex_dividend_date_difference,
        "株分割日": last_split_date_obj,
        "分割日まで": last_split_date_difference,
        #この3つは個別調査でいい
        #"業界": info.get("industry", None),
        #"セクター": info.get("sector", None),
        #"銘柄名": info.get("longName", None),
        "時価総額": info.get("marketCap", None),
        #"次回決算日":earnings_date,
        "予想PER": info.get("forwardPE", None),
        "過去PER": info.get("trailingPE", None),
        "PBR": info.get("priceToBook", None),
        "過去EPS": info.get("trailingEps", None),
        "予想EPS": info.get("forwardEps", None),
        "BPS": info.get("bookValue", None),
        "配当性向": info.get("payoutRatio", None),
        "ベータ値": info.get("beta", None),
        #昨年決算だが数値ずれあり(0以上が好ましい)
        "過去配当額": info.get("trailingAnnualDividendRate", None),
        "過去配当利回り": info.get("trailingAnnualDividendYield", None),
        "平均配当利回り": info.get("fiveYearAvgDividendYield", None),
        #たぶん今期?
        "現在配当額": info.get("dividendRate", None),
        "現在配当利回り": info.get("dividendYield", None),
        "株分割比率": info.get("lastSplitFactor", None),
        "52週安値": info.get("fiftyTwoWeekLow", None),
        "52週高値": info.get("fiftyTwoWeekHigh", None),
        "200日平均": info.get("twoHundredDayAverage", None),
        "50日平均": info.get("fiftyDayAverage", None),
        "取引量": info.get("volume", None),
        "10日平均取引量": info.get("averageVolume10days", None),
        "一株売上高": info.get("revenuePerShare", None),
        "自己資本比率": info.get("debtToEquity", None),
        #この辺も個別が好ましい
        #意見数と推奨のみでいいかも
        #"目標株価高値": info.get("targetHighPrice", None),
        #"目標株価安値": info.get("targetLowPrice", None),
        #"目標平均株価": info.get("targetMeanPrice", None),
        #"目標中央値": info.get("targetMedianPrice", None),
        #"推奨評価平均": info.get("recommendationMean", None),
        "推奨": info.get("recommendationKey", None),
        "アナリスト意見数": info.get("numberOfAnalystOpinions", None),
    }
    #取引量
    
    
        # 新しい行に最新値と統計的情報を追加
    for key, value in new_row.items():
            new_row[key] = value
    df_finance =pd.DataFrame([new_row])
    return df_finance


#str型の日にちデータをdateで計算するように加工する関数
def change_date(unstring):
    parts = unstring.split('-')

    # 分割した要素を整数に変換
    year = int(parts[0])
    month = int(parts[1])
    day = int(parts[2])
    # datetime.date() で日付オブジェクトを作成
    date_obj = date(year, month, day)

    return date_obj

def change_date2(obj,timedata):
    difference = obj - timedata
    obj = int(obj.strftime('%Y%m%d'))
    difference = int(difference.days)
    return difference, obj

