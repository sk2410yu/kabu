import pandas as pd

# オシレータ分析　逆張り傾向あり
# 短期RSI計算関数
# 短期RSIを計算し、DataFrameに追加する関数
# RSI (Relative Strength Index) を計算し、DataFrameに追加する汎用関数
def calculate_rsi(df, column='Close', window=9):
    """
    RSI (Relative Strength Index) を計算し、DataFrameに追加する汎用関数。
    
    :param df: pandas DataFrame, 'Close' 列を含む
    :param column: str, RSIを計算する対象の列 (デフォルトは 'Close')
    :param window: int, RSIを計算する期間
    :return: RSIを追加したDataFrame
    """
    # 終値の変化量を計算
    delta = df[column].diff(1)
    
    # 上昇分と下降分を分離して計算
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    
    # RSIの計算
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    # RSIをDataFrameに追加
    df[f'RSI_{window}'] = rsi
    
    return df

# 長期RSIを計算する関数
def calculate_rsiLong(df, column='Close', window=14):
    return calculate_rsi(df, column, window)

# ストキャスティクス　売買の勢いを表す
def calculate_stochastic(df, period=14, smooth_k=3, smooth_d=3):
    """
    ストキャスティクス (Stochastic Oscillator) を計算し、DataFrameに追加する関数。
    
    :param df: pandas DataFrame, 'High', 'Low', 'Close' 列を含む必要がある
    :param period: int, 過去何期間を使ってストキャスティクスを計算するか (デフォルトは14)
    :param smooth_k: int, %Kラインをスムージングする期間 (デフォルトは3)
    :param smooth_d: int, %Dラインの期間 (デフォルトは3)
    :return: ストキャスティクスを追加したDataFrame
    """
    
    # 過去の最高値と最安値を計算
    high_roll = df['High'].rolling(window=period).max()
    low_roll = df['Low'].rolling(window=period).min()
    
    # %K の計算: ((現在の終値 - 最安値) / (最高値 - 最安値)) * 100
    df['%K'] = 100 * ((df['Close'] - low_roll) / (high_roll - low_roll))
    
    # %K_smoothと%Dを含むデータフレームを返す
    return df

# サイコロジカル　75で売　25で買い
def calculate_psychological_line(df, column='Close', window=12):
    """
    サイコロジカルライン (Psychological Line, PL) を計算し、DataFrameに追加する関数。
    
    :param df: pandas DataFrame, 'Close' 列を含む
    :param column: str, PLを計算する対象の列 (デフォルトは 'Close')
    :param window: int, PLを計算する期間 (デフォルトは12)
    :return: サイコロジカルラインを追加したDataFrame
    """
    # 前日との差分を計算
    delta = df[column].diff(1)
    
    # 差分が正（上昇）の日を1、それ以外の日を0として計算
    up_days = delta.apply(lambda x: 1 if x > 0 else 0)  # 差分が正のとき1、その他は0
    
    # 指定期間内の上昇日数をカウントして、その割合を計算
    pl = up_days.rolling(window=window).sum() / window * 100
    
    # PLの列をDataFrameに追加
    df['Psychological_Line'] = pl
    
    # サイコロジカルラインを含むDataFrameを返す
    return df

def calculate_rci(df, column='Close', window=9):
    """
    RCI (Rank Correlation Index) を計算し、DataFrameに追加する関数。
    
    :param df: pandas DataFrame, 'Close' 列を含む
    :param column: str, RCIを計算する対象の列 (デフォルトは 'Close')
    :param window: int, RCIを計算する期間
    :return: RCIを追加したDataFrame
    """
    def compute_rci(prices):
        length = len(prices)
        
        # 日付の順位 (1からlengthまでの整数)
        date_ranks = pd.Series(range(1, length + 1), index=prices.index)
        
        # 価格の順位
        price_ranks = prices.rank(method='first')
        
        # 順位の差を計算
        rank_diff = date_ranks - price_ranks
        
        # RCIの計算
        rci_value = (1 - (6 * (rank_diff ** 2).sum()) / (length * (length ** 2 - 1))) * 100
        return rci_value
    
    # 各ウィンドウでRCIを計算
    df[f'RCI_{window}'] = df[column].rolling(window=window).apply(compute_rci, raw=False)
    
    return df

# 長期RCIを計算する関数
def calculate_rciLong(df, column='Close', window=26):
    return calculate_rci(df, column, window)

#　移動平均線乖離率
def calculate_ma_deviation(df, column='Close', window=25):
    """
    移動平均乖離率を計算し、DataFrameに追加する関数。
    
    :param df: pandas DataFrame, 'Close' 列を含む
    :param column: str, 移動平均乖離率を計算する対象の列 (デフォルトは 'Close')
    :param window: int, 移動平均を計算する期間 (デフォルトは25)
    :return: 移動平均乖離率を追加したDataFrame
    """
    # 移動平均の計算
    moving_average = df[column].rolling(window=window).mean()
    
    # 移動平均乖離率の計算: ((株価 - 移動平均) / 株価) * 100
    df['MA_Deviation'] = ((df[column] - moving_average) / df[column]) * 100
    
    return df

def get_calculate_oscillator(df):
    # オシレータ
    df = calculate_rsiLong(df)
    df = calculate_stochastic(df)
    df = calculate_psychological_line(df)
    df = calculate_rciLong(df)
    df = calculate_ma_deviation(df)

    return df