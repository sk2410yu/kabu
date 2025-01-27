from datetime import datetime 
import os 

def check_market_info():
    # 今日の日付を使ってファイル名を作成
    today = datetime.now().date().strftime("%Y%m%d")
    market_file = f"market/market_{today}.xlsx"
    
    # ファイルが存在するかをチェック
    if os.path.exists(market_file):
        return True
    else:
        return False