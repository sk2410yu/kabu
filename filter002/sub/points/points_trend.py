
def point_trend(serch_df,point_df):
    
    #1%設定
    price = serch_df ["Close"]/100
    
    if serch_df["MACD_Signal_difference"] > 0:
        point_df["MACD"]=1
    else:
        point_df["MACD"]=-1
    
    if serch_df["bands_Range1"]<price:
        point_df["bands"]=1
    else:
        point_df["bands"]=0
        
    if serch_df["DI+"]>20 and ["DI-"]<10:
        point_df["DMI"]=1
    elif serch_df["DI+"] > 25:
        point_df["DMI"]=1
    elif serch_df["DI-"] < 5:
        point_df["DMI"]=1
    elif serch_df["DI-"] > 25:
        point_df["DMI"]=-1
    elif serch_df["DI+"] > 5:
        point_df["DMI"]=-1
    else:
        point_df["DMI"]=0    
           
        
    if serch_df["Close"]>serch_df["Senkou_Span_A"] and serch_df["Close"]>serch_df["Senkou_Span_B"]:
        point_df["itimoku_kumo"]=1
    elif serch_df["Close"]>serch_df["Senkou_Span_A"] and serch_df["Close"]< serch_df["Senkou_Span_B"]:
        point_df["itimoku_kumo"]=0
    elif serch_df["Close"]<serch_df["Senkou_Span_A"] and serch_df["Close"]> serch_df["Senkou_Span_B"]:
        point_df["itimoku_kumo"]=0
    else: 
        point_df["itimoku_kumo"]=-1
    
    return point_df
        
        
    