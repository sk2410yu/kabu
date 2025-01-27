import pandas as pd
# Excelファイルを読み込む
file_path = 'data_j.xls'
df = pd.read_excel(file_path)

# 商品区分がETF・ETN PRO Marketでないものをフィルタリング 
filtered_df = df[~df['市場・商品区分'].isin(['ETF・ETN'])]
filtered_df = filtered_df[~filtered_df['市場・商品区分'].isin(['PRO Market'])]
# コードリストと業種区分リストを作成
code_list = filtered_df['コード'].tolist()
industry_list = filtered_df['17業種区分'].tolist()

# コードリストと業種区分リストをDataFrameに変換
code_list_df = pd.DataFrame(code_list, columns=['コード'])
industry_list_df = pd.DataFrame(industry_list, columns=['業種区分'])

# コードリストと業種区分リストを結合
combined_df = pd.concat([code_list_df, industry_list_df], axis=1)

# 業種別にコードをまとめる
industry_code_map = filtered_df.groupby('17業種区分')['コード'].apply(list).reset_index()
industry_code_map.columns = ['業種区分', '業種別コードリスト']

# 結合したDataFrameに業種別コードを追加
combined_df = pd.concat([combined_df, industry_code_map], axis=1)
filename = f"stocknumber_1month.csv"
# データフレームをCSVファイルとして保存
combined_df.to_csv(filename, index=False, encoding="shift-jis")
    
print(f"CSVファイルが保存されました: {filename}")


