import os
import pandas as pd
from datetime import datetime

def save_to_excel(all_data, base_dir='market'):
    # 現在の日時を取得してファイル名に追加
    current_time = datetime.now().date().strftime("%Y%m%d")
    file_name = f"market_{current_time}.xlsx"

    # market フォルダに保存する
    output_dir = os.path.join(base_dir)  # daily_reports フォルダは削除

    # market フォルダがなければ作成
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    file_path = os.path.join(output_dir, file_name)

    # Excel ファイルを保存
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        for ticker, data in all_data.items():
            data.to_excel(writer, sheet_name=ticker, index=False)

    print(f"Excelファイルを保存しました: {file_path}")