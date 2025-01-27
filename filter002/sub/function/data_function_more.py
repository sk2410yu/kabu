def get_more_info(df):
    if df.empty:
        return "データが取得できませんでした。"
    
    # 終値の変化を計算
    df['Price_Change'] = df['Close'].diff()
    df['Price_Change_Percent'] = df ["Price_Change"] / df["Close"]

    # 続伸日数を計算
    df['Up'] = df['Price_Change'] > 0
    df['Down'] = df['Price_Change'] < 0
    
    #幅の計算する
    df["High_percent"] = df["High"]-df["Close"].shift(1)
    df["Low_percent"] = df["Low"]-df["Close"].shift(1)
    
    #幅差を計算する
    df["Price_width"] = df["High"]- df["Low"]
    df["Price_width_Percent"] = df["High"]- df["Low"] / df["Close"]
    
    return df