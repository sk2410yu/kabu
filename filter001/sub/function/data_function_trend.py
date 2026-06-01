import numpy as np
import pandas as pd

#トレンド分析指数
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

# DMI 30%が目安　持ち合いは難しい
# DMIを計算する関数
def calculate_dmi(df, period=14):
    """
    DataFrame内の価格データを基にDMI関連指標を計算し、元のdfにDI+, DI-, ADX, ADX-R列を追加。

    Args:
        df (pd.DataFrame): High, Low, Close列を含むデータフレーム
        period (int): 計算に用いる期間

    Returns:
        pd.DataFrame: 元のdfにDI+, DI-, ADX, ADX-R列を追加したDataFrame
    """
    # 中間計算結果を別のDataFrameに保存
    df_dmi = pd.DataFrame(index=df.index)

    # 中間計算
    df_dmi['TR'] = np.maximum(
        df['High'] - df['Low'],
        np.maximum(abs(df['High'] - df['Close'].shift(1)), abs(df['Low'] - df['Close'].shift(1)))
    )
    df_dmi['DM+'] = np.where(
        (df['High'] - df['High'].shift(1)) > (df['Low'].shift(1) - df['Low']),
        np.maximum(df['High'] - df['High'].shift(1), 0),
        0
    )
    df_dmi['DM-'] = np.where(
        (df['Low'].shift(1) - df['Low']) > (df['High'] - df['High'].shift(1)),
        np.maximum(df['Low'].shift(1) - df['Low'], 0),
        0
    )

    # 期間での集計
    df_dmi['TR14'] = df_dmi['TR'].rolling(window=period).sum()
    df_dmi['DM+14'] = df_dmi['DM+'].rolling(window=period).sum()
    df_dmi['DM-14'] = df_dmi['DM-'].rolling(window=period).sum()

    # DI+, DI-計算
    df['DI+'] = 100 * (df_dmi['DM+14'] / df_dmi['TR14'])
    df['DI-'] = 100 * (df_dmi['DM-14'] / df_dmi['TR14'])
    
    df['DI+DI-_difference']= df['DI+']-df['DI-']

    # DXとADX計算
    
    #df_dmi['DX'] = 100 * abs(df_dmi['DM+14'] - df_dmi['DM-14']) / (df_dmi['DM+14'] + df_dmi['DM-14'])
    #df['ADX'] = df_dmi['DX'].rolling(window=period).mean()

    # ADX-R計算
    #df['ADX-R'] = (df['ADX'] + df['ADX'].shift(period)) / 2

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
    
    # numpy配列で位置参照（ラベルindexに依存せず高速）
    high = df['High'].to_numpy(dtype=float)
    low = df['Low'].to_numpy(dtype=float)
    n = len(df)

    if n == 0:
        df['Parabolic_SAR'] = []
        df['Parabolic_SAR_difference'] = df["Close"] - df['Parabolic_SAR']
        return df

    # 初期設定
    sar = low[0]   # SARの初期値として、最初のLowを使用
    ep = high[0]   # エクストリームポイント (最初は最初のHigh)
    af = initial_af     # 初期アクセラレーションファクター
    uptrend = True      # 最初は上昇トレンドからスタート

    # 結果を保存するリスト
    sar_list = []

    for i in range(1, n):
        prev_sar = sar  # 前回のSAR

        if uptrend:
            sar = prev_sar + af * (ep - prev_sar)  # SARの更新
            if low[i] < sar:  # トレンド転換の判定
                uptrend = False
                sar = ep  # 転換後のSAR初期値はエクストリームポイント
                ep = low[i]  # エクストリームポイントをリセット
                af = initial_af  # アクセラレーションファクターをリセット
        else:
            sar = prev_sar + af * (ep - prev_sar)
            if high[i] > sar:
                uptrend = True
                sar = ep
                ep = high[i]
                af = initial_af

        # SARの上昇・下降トレンドに応じてエクストリームポイントを更新
        if uptrend:
            if high[i] > ep:
                ep = high[i]
                af = min(af + step_af, max_af)  # アクセラレーションファクターを増加
        else:
            if low[i] < ep:
                ep = low[i]
                af = min(af + step_af, max_af)

        sar_list.append(sar)

    # sar_list の長さを df の長さに合わせる例
    if len(sar_list) < n:
        sar_list.append(None)  # None で埋める例

    df['Parabolic_SAR'] = [None] + sar_list[:-1]
    df['Parabolic_SAR_difference'] = df["Close"]- df['Parabolic_SAR']

    return df


def get_calculate_trend(df):
    #　トレンド指数
    df = calculate_macd(df)
    df = calculate_dmi(df)
    df = calculate_parabolic_sar(df)
    
    return df