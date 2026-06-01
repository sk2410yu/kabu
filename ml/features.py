"""特徴量生成。

既存のテクニカル指標関数（filter001/sub/function 配下）をそのまま再利用し、
価格スケールに依存する指標は終値で正規化して学習に使いやすい形にする。
"""
import os
import sys

import numpy as np

# 既存の指標計算関数を再利用する（numpy/pandas のみに依存しておりクリーンに import できる）
_FUNC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "..", "filter001", "sub", "function")
_FUNC_DIR = os.path.abspath(_FUNC_DIR)
if _FUNC_DIR not in sys.path:
    sys.path.insert(0, _FUNC_DIR)

from data_function_trend import get_calculate_trend  # noqa: E402
from data_function_oscillator import get_calculate_oscillator  # noqa: E402


# 学習に用いる特徴量（できるだけ価格スケールに依存しない／定常的な量に揃える）
FEATURE_COLUMNS = [
    "macd_norm",              # MACD / 終値
    "macd_signal_diff_norm",  # (MACD - シグナル) / 終値
    "DI+",                    # 0-100
    "DI-",                    # 0-100
    "DI+DI-_difference",      # DI+ - DI-
    "sar_diff_norm",          # (終値 - パラボリックSAR) / 終値
    "RSI_14",                 # 0-100
    "%K",                     # 0-100
    "Psychological_Line",     # 0-100
    "RCI_26",                 # -100..100
    "MA_Deviation",           # 移動平均乖離率(%)
    "ret_5",                  # 直近5本リターン
    "ret_10",                 # 直近10本リターン
    "ret_20",                 # 直近20本リターン
    "vol_z",                  # 出来高の標準化スコア(20本)
]


def add_indicators(df):
    """既存の指標関数で MACD/DMI/SAR/RSI 等を付与する。"""
    df = get_calculate_trend(df)
    df = get_calculate_oscillator(df)
    return df


def add_features(df):
    """OHLCV の DataFrame に指標 + 学習用特徴量を付与して返す。

    df は単層列（'Open','High','Low','Close','Volume'）を想定。
    """
    df = add_indicators(df.copy())

    close = df["Close"].replace(0, np.nan)
    df["macd_norm"] = df["MACD"] / close
    df["macd_signal_diff_norm"] = df["MACD_Signal_difference"] / close
    df["sar_diff_norm"] = df["Parabolic_SAR_difference"] / close

    df["ret_5"] = close.pct_change(5)
    df["ret_10"] = close.pct_change(10)
    df["ret_20"] = close.pct_change(20)

    vol = df["Volume"].astype(float)
    vol_mean = vol.rolling(20).mean()
    vol_std = vol.rolling(20).std()
    df["vol_z"] = (vol - vol_mean) / vol_std

    return df
