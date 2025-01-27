import pandas as pd
import numpy as np

def show_data(df, std_df, cross_df,periods):
    df = df.round(2)
    df = df.dropna()
    std_df = std_df.round(2)
    std_df = std_df.dropna()
    cross_df = cross_df.round(2)
    cross_df = cross_df.dropna()
    if periods =="1wk":
        resent_df =df.tail(52)
        print("1週間足の分析")
        print(f"1年の幅{min(resent_df['Close'])}~{max(resent_df['Close'])}")
        print(f"MACD,現在値:({df['MACD'].iloc[-1]},{df['Signal_Line'].iloc[-1]}),統計:({std_df['MACD_Percentile'].iloc[0]}%, 0%:{min(df['MACD'])}, 25%:{std_df['MACD_Q1'].iloc[0]}, 50%:{std_df['MACD_Median'].iloc[0]}, 75%:{std_df['MACD_Q3'].iloc[0]}, 100%:{max(df['MACD'])})")
        print(f"DMI,現在値:({df['DI+'].iloc[-1]},{df['DI-'].iloc[-1]},{df['ADX'].iloc[-1]},{df['ADX-R'].iloc[-1]}),統計:({std_df['DI+_Percentile'].iloc[0]}%, 0%:{min(df['DI+'])}, 25%:{std_df['DI+_Q1'].iloc[0]}, 50%:{std_df['DI+_Median'].iloc[0]}, 75%:{std_df['DI+_Q3'].iloc[0]}, 100%:{max(df['DI+'])})")
        print(f"RSI現在値:({df['RSI_9'].iloc[-1]},{df['RSI_14'].iloc[-1]}),統計:({std_df['RSI_14_Percentile'].iloc[0]}%, 0%:{min(df['RSI_14'])}, 25%:{std_df['RSI_14_Q1'].iloc[0]}, 50%:{std_df['RSI_14_Median'].iloc[0]}, 75%:{std_df['RSI_14_Q3'].iloc[0]}, 100%:{max(df['RSI_14'])})")
        print(f"ストキャスティクス:(K%: {df['%K'].iloc[-1]},D%: {df['%D'].iloc[-1]}),サイコロジカル:({df['Psychological_Line'][-1]})")
    
    if periods == "1d":
        resent_df =df.tail(200)
        print("1日足の分析")
        print(f"6か月の幅{min(resent_df['Close'])}~{max(resent_df['Close'])}")
        print(f"MACD,現在値:({df['MACD'].iloc[-1]},{df['Signal_Line'].iloc[-1]}),統計:({std_df['MACD_Percentile'].iloc[0]}%, 0%:{min(df['MACD'])}, 25%:{std_df['MACD_Q1'].iloc[0]}, 50%:{std_df['MACD_Median'].iloc[0]}, 75%:{std_df['MACD_Q3'].iloc[0]}, 100%:{max(df['MACD'])})")
        print(f"DMI,現在値:({df['DI+'].iloc[-1]},{df['DI-'].iloc[-1]},{df['ADX'].iloc[-1]},{df['ADX-R'].iloc[-1]}),統計:({std_df['DI+_Percentile'].iloc[0]}%, 0%:{min(df['DI+'])}, 25%:{std_df['DI+_Q1'].iloc[0]}, 50%:{std_df['DI+_Median'].iloc[0]}, 75%:{std_df['DI+_Q3'].iloc[0]}, 100%:{max(df['DI+'])})")
        print(f"RSI現在値:({df['RSI_9'].iloc[-1]},{df['RSI_14'].iloc[-1]}),統計:({std_df['RSI_14_Percentile'].iloc[0]}%, 0%:{min(df['RSI_14'])}, 25%:{std_df['RSI_14_Q1'].iloc[0]}, 50%:{std_df['RSI_14_Median'].iloc[0]}, 75%:{std_df['RSI_14_Q3'].iloc[0]}, 100%:{max(df['RSI_14'])})")
        print(f"ストキャスティクス:(K%: {df['%K'].iloc[-1]},D%: {df['%D'].iloc[-1]}),サイコロジカル:({df['Psychological_Line'][-1]})")
    
    if periods == "60m":
        resent_df =df.tail(480)
        print("1時間の分析")
        print(f"4か月の幅{min(resent_df['Close'])}~{max(resent_df['Close'])}")
        print(f"MACD,現在値:({df['MACD'].iloc[-1]},{df['Signal_Line'].iloc[-1]}),統計:({std_df['MACD_Percentile'].iloc[0]}%, 0%:{min(df['MACD'])}, 25%:{std_df['MACD_Q1'].iloc[0]}, 50%:{std_df['MACD_Median'].iloc[0]}, 75%:{std_df['MACD_Q3'].iloc[0]}, 100%:{max(df['MACD'])})")
        print(f"DMI,現在値:({df['DI+'].iloc[-1]},{df['DI-'].iloc[-1]},{df['ADX'].iloc[-1]},{df['ADX-R'].iloc[-1]}),統計:({std_df['DI+_Percentile'].iloc[0]}%, 0%:{min(df['DI+'])}, 25%:{std_df['DI+_Q1'].iloc[0]}, 50%:{std_df['DI+_Median'].iloc[0]}, 75%:{std_df['DI+_Q3'].iloc[0]}, 100%:{max(df['DI+'])})")
        print(f"RSI現在値:({df['RSI_9'].iloc[-1]},{df['RSI_14'].iloc[-1]}),統計:({std_df['RSI_14_Percentile'].iloc[0]}%, 0%:{min(df['RSI_14'])}, 25%:{std_df['RSI_14_Q1'].iloc[0]}, 50%:{std_df['RSI_14_Median'].iloc[0]}, 75%:{std_df['RSI_14_Q3'].iloc[0]}, 100%:{max(df['RSI_14'])})")
        print(f"ストキャスティクス:(K%: {df['%K'].iloc[-1]},D%: {df['%D'].iloc[-1]}),サイコロジカル:({df['Psychological_Line'][-1]})")
    
    if periods == "5m":
        print("5分足の分析")
        print(f"2か月の幅{min(df['Close'])}~{max(df['Close'])}")
        print(f"MACD,現在値:({df['MACD'].iloc[-1]},{df['Signal_Line'].iloc[-1]}),統計:({std_df['MACD_Percentile'].iloc[0]}%, 0%:{min(df['MACD'])}, 25%:{std_df['MACD_Q1'].iloc[0]}, 50%:{std_df['MACD_Median'].iloc[0]}, 75%:{std_df['MACD_Q3'].iloc[0]}, 100%:{max(df['MACD'])})")
        print(f"DMI,現在値:({df['DI+'].iloc[-1]},{df['DI-'].iloc[-1]},{df['ADX'].iloc[-1]},{df['ADX-R'].iloc[-1]}),統計:({std_df['DI+_Percentile'].iloc[0]}%, 0%:{min(df['DI+'])}, 25%:{std_df['DI+_Q1'].iloc[0]}, 50%:{std_df['DI+_Median'].iloc[0]}, 75%:{std_df['DI+_Q3'].iloc[0]}, 100%:{max(df['DI+'])})")
        print(f"RSI現在値:({df['RSI_9'].iloc[-1]},{df['RSI_14'].iloc[-1]}),統計:({std_df['RSI_14_Percentile'].iloc[0]}%, 0%:{min(df['RSI_14'])}, 25%:{std_df['RSI_14_Q1'].iloc[0]}, 50%:{std_df['RSI_14_Median'].iloc[0]}, 75%:{std_df['RSI_14_Q3'].iloc[0]}, 100%:{max(df['RSI_14'])})")
        print(f"ストキャスティクス:(K%: {df['%K'].iloc[-1]},D%: {df['%D'].iloc[-1]}),サイコロジカル:({df['Psychological_Line'][-1]})")
    
    return None