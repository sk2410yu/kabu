import numpy as np

#トレンド分析指数
# 移動平均線の計算
def calculate_ma(df):
    df.loc[:, 'ma5'] = df['Close'].rolling(window=5).mean()
    df.loc[:, 'ma20'] = df['Close'].rolling(window=20).mean()
    df.loc[:, 'ma50'] = df['Close'].rolling(window=50).mean()
    df.loc[:, 'ma75'] = df['Close'].rolling(window=75).mean()
    df.loc[:, 'ma100'] = df['Close'].rolling(window=100).mean()
    df.loc[:, 'ma200'] = df['Close'].rolling(window=200).mean()

    return df

# MACDを計算し、DataFrameに追加する関数
def calculate_macd(df, short_span=12, long_span=26, signal_span=9):
    # 短期EMA (12期間)
    short_ema = df['Close'].ewm(span=short_span, adjust=False).mean()  
    # 長期EMA (26期間)
    long_ema = df['Close'].ewm(span=long_span, adjust=False).mean()    
    # MACD
    df['MACD'] = short_ema - long_ema                                 
    # シグナルライン
    df['Signal_Line'] = df['MACD'].ewm(span=signal_span, adjust=False).mean()  
    # シグナルとの差
    df['MACD_Signal_difference']= df["MACD"]-df["Signal_Line"]
    # MACDとシグナルラインを追加したデータフレームを返す
    return df

# ボリンジャーバンドの計算
def calculate_bands(df):
    df.loc[:, 'MA20'] = df['Close'].rolling(window=20).mean()
    df.loc[:, 'STD20'] = df['Close'].rolling(window=20).std()
    df.loc[:, 'Top2'] = df['MA20'] + (df['STD20'] * 2)
    df.loc[:, 'Bot2'] = df['MA20'] - (df['STD20'] * 2)
    df.loc[:, 'Top1'] = df['MA20'] + (df['STD20'] * 1)
    df.loc[:, 'Bot1'] = df['MA20'] - (df['STD20'] * 1)
    
    # Top2とBot2の差を追加
    df.loc[:, 'bands_Range2'] = df['Top2'] - df['Bot2']
    # Top1とBot1の差を追加
    df.loc[:, 'bands_Range1'] = df['Top1'] - df['Bot1']
    
    # MA20とCloseの差をSTD20で割った値を追加
    df.loc[:, 'MA_band'] = (df['Close'] - df['MA20']) / df['STD20']
    
    return df


# 一目均衡表 雲の上か下か
def calculate_ichimoku(df):
    # 転換線 (Tenkan-sen): (9日間の最高値 + 9日間の最安値) / 2
    high_9 = df['High'].rolling(window=9).max()
    low_9 = df['Low'].rolling(window=9).min()
    df['Tenkan_sen'] = (high_9 + low_9) / 2

    # 基準線 (Kijun-sen): (26日間の最高値 + 26日間の最安値) / 2
    high_26 = df['High'].rolling(window=26).max()
    low_26 = df['Low'].rolling(window=26).min()
    df['Kijun_sen'] = (high_26 + low_26) / 2

    # 先行スパン1 (Senkou Span A): (転換線 + 基準線) / 2 -> 26日先行
    df['Senkou_Span_A'] = ((df['Tenkan_sen'] + df['Kijun_sen']) / 2).shift(26)

    # 先行スパン2 (Senkou Span B): (52日間の最高値 + 52日間の最安値) / 2 -> 26日先行
    high_52 = df['High'].rolling(window=52).max()
    low_52 = df['Low'].rolling(window=52).min()
    df['Senkou_Span_B'] = ((high_52 + low_52) / 2).shift(26)

    # 遅行スパン (Chikou Span): 終値 -> 26日遅行
    df['Chikou_Span'] = df['Close'].shift(-26)

    return df

# DMI 30%が目安　持ち合いは難しい
# DMIを計算する関数
def calculate_dmi(df, period=14):
    df['TR'] = np.maximum(df['High'] - df['Low'], 
                          np.maximum(abs(df['High'] - df['Close'].shift(1)), 
                                     abs(df['Low'] - df['Close'].shift(1))))
    df['DM+'] = np.where((df['High'] - df['High'].shift(1)) > (df['Low'].shift(1) - df['Low']), 
                         np.maximum(df['High'] - df['High'].shift(1), 0), 0)
    df['DM-'] = np.where((df['Low'].shift(1) - df['Low']) > (df['High'] - df['High'].shift(1)), 
                         np.maximum(df['Low'].shift(1) - df['Low'], 0), 0)

    df['TR14'] = df['TR'].rolling(window=period).sum()
    df['DM+14'] = df['DM+'].rolling(window=period).sum()
    df['DM-14'] = df['DM-'].rolling(window=period).sum()

    df['DI+'] = 100 * (df['DM+14'] / df['TR14'])
    df['DI-'] = 100 * (df['DM-14'] / df['TR14'])
    df['DX'] = 100 * abs(df['DI+'] - df['DI-']) / (df['DI+'] + df['DI-'])
    df['ADX'] = df['DX'].rolling(window=14).mean()
    # ADX-Rを計算する部分の追加
    df['ADX-R'] = (df['ADX'] + df['ADX'].shift(14)) / 2

    return df

# パラボリック,一目均衡表と相性がいい
def calculate_parabolic_sar(df, initial_af=0.02, max_af=0.2, step_af=0.02):
    """
    パラボリックSARを計算し、DataFrameに追加する関数。
    
    :param df: pandas DataFrame, 'High', 'Low' 列を含む必要がある
    :param initial_af: 初期のアクセラレーションファクター (デフォルトは0.02)
    :param max_af: 最大のアクセラレーションファクター (デフォルトは0.2)
    :param step_af: アクセラレーションファクターのステップ (デフォルトは0.02)
    :return: パラボリックSARを追加したDataFrame
    """
    
    # 初期設定
    sar = df['Low'][0]  # SARの初期値として、最初のLowを使用
    ep = df['High'][0]  # エクストリームポイント (最初は最初のHigh)
    af = initial_af     # 初期アクセラレーションファクター
    uptrend = True      # 最初は上昇トレンドからスタート
    
    # 結果を保存するリスト
    sar_list = []
    
    for i in range(1, len(df)):
        prev_sar = sar  # 前回のSAR
        
        if uptrend:
            sar = prev_sar + af * (ep - prev_sar)  # SARの更新
            if df['Low'][i] < sar:  # トレンド転換の判定
                uptrend = False
                sar = ep  # 転換後のSAR初期値はエクストリームポイント
                ep = df['Low'][i]  # エクストリームポイントをリセット
                af = initial_af  # アクセラレーションファクターをリセット
        else:
            sar = prev_sar + af * (ep - prev_sar)
            if df['High'][i] > sar:
                uptrend = True
                sar = ep
                ep = df['High'][i]
                af = initial_af
        
        # SARの上昇・下降トレンドに応じてエクストリームポイントを更新
        if uptrend:
            if df['High'][i] > ep:
                ep = df['High'][i]
                af = min(af + step_af, max_af)  # アクセラレーションファクターを増加
        else:
            if df['Low'][i] < ep:
                ep = df['Low'][i]
                af = min(af + step_af, max_af)
        
        sar_list.append(sar)
    
    # sar_list の長さを df の長さに合わせる例
    if len(sar_list) < len(df):
        sar_list.append(None)  # None で埋める例
        
    df['Parabolic_SAR'] = sar_list
    
    return df

# エンベロープ　乖離率　小型不向き　乖離率売られすぎ買われすぎ
#順張り2.5 5で利確、　逆張り0で利確
# エンベロープを計算する関数
def calculate_envelope(df, period=25, envelope_percentage=0.05):
    df['MA'] = df['Close'].rolling(window=period).mean()
    df['Envelope Upper'] = df['MA'] * (1 + envelope_percentage)
    df['Envelope Lower'] = df['MA'] * (1 - envelope_percentage)

    return df

def get_calculate_trend(df):
    #　トレンド指数
    df = calculate_ma(df)
    df = calculate_macd(df)
    df = calculate_bands(df)
    df = calculate_ichimoku(df)
    df = calculate_dmi(df)
    df = calculate_parabolic_sar(df)
    df = calculate_envelope(df)
    
    return df