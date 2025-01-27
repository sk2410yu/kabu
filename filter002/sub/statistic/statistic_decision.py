def all_decision_df(ticker,add_df, result_df):
    # result_dfの初期設定
    if 'ticker' not in result_df.columns:
        result_df['ticker'] = ticker
    if 'purasu' not in result_df.columns:
        result_df['purasu'] = 0
    if 'mainsu' not in result_df.columns:
        result_df['mainsu'] = 0
    
    #単純シグナル判定
    # Closeが現在値より高く、MACDが正のとき
    if add_df['Close'] > add_df['Close']and add_df['MACD'] > 0:
        result_df.at[0, 'purasu'] += 1
    # MACDが負のとき
    elif add_df['MACD'] < 0:
        result_df.at[0, 'mainsu'] += 1
        
    
    return result_df

