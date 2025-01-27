def get_more_info(df):
    if df.empty:
        return "データが取得できませんでした。"
    
    # 終値の変化を計算
    df['Price_Change'] = df['Close'].diff()
    df['Price_Change_Percent'] = df ["Price_Change"] / df["Close"]

    # 続伸日数を計算
    df =calculate_streaks(df)
    df =calculate_high_open_streaks(df)
    df =calculate_low_close_streaks(df)

    #幅を計算する
    df["Price_width"] = df["High"]- df["Low"]
    df["Price_width_relative"] = (df["High"]- df["Low"])/df["Close"]
    
    return df

# 続落・続伸日数を記録する関数
def calculate_streaks(df):
    """
    DataFrame内のClose列を基に続伸・続落日数を計算し、元のDataFrameに保存。

    Args:
        df (pd.DataFrame): Close列を含むデータフレーム

    Returns:
        pd.DataFrame: up_streak列とdown_streak列を含む更新済みのDataFrame
    """
    # 初期化
    up_streak_list = [0]  # 最初は0
    down_streak_list = [0]  # 最初は0
    up_streak, down_streak = 0, 0

    # Close列を取得
    close_prices = df['Close'].values

    for i in range(1, len(close_prices)):
        if close_prices[i] > close_prices[i - 1]:  # 続伸
            up_streak += 1
            down_streak = 0
        elif close_prices[i] < close_prices[i - 1]:  # 続落
            down_streak += 1
            up_streak = 0
        else:
            up_streak, down_streak = 0, 0  # 同値ならリセット

        up_streak_list.append(up_streak)
        down_streak_list.append(down_streak)

    # 新しい列を追加
    df['up_streak'] = up_streak_list
    df['down_streak'] = down_streak_list

    return df

def calculate_high_open_streaks(df):
    """
    DataFrame内のHigh - Open列を基に続伸・続落日数を計算し、元のDataFrameに保存。

    Args:
        df (pd.DataFrame): High, Open列を含むデータフレーム

    Returns:
        pd.DataFrame: high_open_up_streak列とhigh_open_down_streak列を含む更新済みのDataFrame
    """
    # 初期化
    up_streak_list = [0]  # 最初は0
    down_streak_list = [0]  # 最初は0
    up_streak, down_streak = 0, 0

    # 差分を計算
    high_open_diff = df['High'] - df['Open']

    for i in range(1, len(high_open_diff)):
        if high_open_diff[i] > high_open_diff[i - 1]:  # 続伸
            up_streak += 1
            down_streak = 0
        elif high_open_diff[i] < high_open_diff[i - 1]:  # 続落
            down_streak += 1
            up_streak = 0
        else:
            up_streak, down_streak = 0, 0  # 同値ならリセット

        up_streak_list.append(up_streak)
        down_streak_list.append(down_streak)

    # 新しい列を追加
    df['high_open_up_streak'] = up_streak_list
    df['high_open_down_streak'] = down_streak_list

    return df


def calculate_low_close_streaks(df):
    """
    DataFrame内のLow - Close列を基に続伸・続落日数を計算し、元のDataFrameに保存。

    Args:
        df (pd.DataFrame): Low, Close列を含むデータフレーム

    Returns:
        pd.DataFrame: low_close_up_streak列とlow_close_down_streak列を含む更新済みのDataFrame
    """
    # 初期化
    up_streak_list = [0]  # 最初は0
    down_streak_list = [0]  # 最初は0
    up_streak, down_streak = 0, 0

    # 差分を計算
    low_close_diff = df['Low'] - df['Close']

    for i in range(1, len(low_close_diff)):
        if low_close_diff[i] > low_close_diff[i - 1]:  # 続伸
            up_streak += 1
            down_streak = 0
        elif low_close_diff[i] < low_close_diff[i - 1]:  # 続落
            down_streak += 1
            up_streak = 0
        else:
            up_streak, down_streak = 0, 0  # 同値ならリセット

        up_streak_list.append(up_streak)
        down_streak_list.append(down_streak)

    # 新しい列を追加
    df['low_close_up_streak'] = up_streak_list
    df['low_close_down_streak'] = down_streak_list

    return df
