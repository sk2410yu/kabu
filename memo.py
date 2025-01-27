import pandas as pd

def next_close_for_zero_macd(df, short_span=12, long_span=26):
    # 最新の短期EMAと長期EMAを取得
    short_ema = df['Close'].ewm(span=short_span, adjust=False).mean().iloc[-1]
    long_ema = df['Close'].ewm(span=long_span, adjust=False).mean().iloc[-1]

    # 次の「Close」価格でMACDが0になる条件を求める
    # 式: 新しいMACD = (new_short_ema - new_long_ema) = 0
    # 新しい短期EMAと長期EMAの関係を考慮して計算
    multiplier_short = 2 / (short_span + 1)
    multiplier_long = 2 / (long_span + 1)

    # 次のCloseを X として
    # short_ema_next = short_ema + multiplier_short * (X - short_ema)
    # long_ema_next = long_ema + multiplier_long * (X - long_ema)
    # short_ema_next - long_ema_next = 0 の解を求める

    numerator = short_ema - long_ema
    denominator = multiplier_long - multiplier_short

    next_close = numerator / denominator + short_ema

    return next_close

# 使用例
data = {'Close': [100, 102, 101, 103, 105]}  # サンプルデータ
df = pd.DataFrame(data)
next_close_value = next_close_for_zero_macd(df)
print(f"次のMACDが0になるためのClose値: {next_close_value}")
