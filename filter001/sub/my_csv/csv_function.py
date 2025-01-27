import pandas as pd

class CSVFunction:
    def __init__(self, csv_name):
        self.csv_path = csv_name
        self.loading = self.load_csv()

    def load_csv(self):
        """Load CSV file or create a new one if it doesn't exist."""
        try:
            df = pd.read_csv(self.csv_path)
            print(f"CSV file '{self.csv_path}' exists and has been loaded.")
        except FileNotFoundError:
            print(f"CSV file '{self.csv_path}' not found. Creating a new one.")
            data = {
                "銘柄番号": [],
                "基準配当利回り": [],
                "メモ": [],
                "優待メモ": []
            }
            df = pd.DataFrame(data)
            df.to_csv(self.csv_path, index=False, encoding="UTF-8")
        return df

    def print_alert_threshold(self, ticker):
        """Print the alert threshold, memo, and yuutai for a specific ticker."""
        ticker = str(ticker)
        if ticker in self.loading['銘柄番号'].values:
            row = self.loading[self.loading['銘柄番号'] == ticker].iloc[0]
            print(f"銘柄番号: {ticker} - 現在の配当利回りは {row['基準配当利回り']}%")
            memo = row['メモ'] if pd.notna(row['メモ']) else "No memo"
            yuutai = row['優待メモ'] if pd.notna(row['優待メモ']) else "No yuutai"
            print(f"メモ: {memo}")
            print(f"優待: {yuutai}")
        else:
            print(f"銘柄番号: {ticker} はデータとして保存されていません.")

    def add_ticker(self):
        """Add a new ticker, memo, and yuutai to the CSV."""
        ticker = input("追加したい銘柄番号（例: 7203）: ")
        ticker = f"{ticker}.T"  # Format for Japanese tickers
        if ticker not in self.loading['銘柄番号'].values:
            try:
                new_threshold = float(input("配当利回り基準値を入力: "))
            except ValueError:
                print("無効な数値です。再度入力してください。")
                return

            new_memo = input("メモを追加: ")
            new_yuutaimemo = input("優待情報を追加: ")

            new_row = {
                '銘柄番号': ticker,
                '基準配当利回り': new_threshold,
                'メモ': new_memo,
                '優待メモ': new_yuutaimemo
            }
            self.loading = pd.concat([self.loading, pd.DataFrame([new_row])], ignore_index=True)
            self.save_to_csv()
            print(f"Ticker {ticker} has been added with memo '{new_memo}' and yuutai '{new_yuutaimemo}'.")
        else:
            print(f"Ticker {ticker} already exists. Use an edit function to modify existing entries.")

    def delete_ticker(self):
        """Delete a ticker from the CSV."""
        ticker = input("削除したい銘柄番号（例: 7203）: ")
        ticker = f"{ticker}.T"  # Format for Japanese tickers
        if ticker in self.loading['銘柄番号'].values:
            self.loading = self.loading[self.loading['銘柄番号'] != ticker]
            self.save_to_csv()
            print(f"Ticker {ticker} has been deleted.")
        else:
            print(f"Ticker {ticker} does not exist in the current data.")

    def display_all_info(self):
        """Display all ticker information including memo, and print ticker length."""
        if self.loading.empty:
            print("No data available.")
        else:
            print("全銘柄情報:")
            print(self.loading.to_string(index=False))  # Print entire DataFrame without index
            print("\n銘柄番号とその長さ:")
            for ticker in self.loading['銘柄番号']:
                print(f"銘柄番号: {ticker}, 長さ: {len(ticker)}")
                
    def save_to_csv(self):
        """Save the DataFrame to CSV."""
        try:
            self.loading.to_csv(self.csv_path, index=False, encoding="UTF-8")
            print(f"Data successfully saved to '{self.csv_path}'.")
        except Exception as e:
            print(f"Error saving to CSV: {e}")

# Instantiate and test the CSVFunction class if necessary.
# csv_func = CSVFunction("sample.csv")

"""
csd = CSVFunction("file_1555.xlsx")

class CSV_edit:
    def __init__(self,csv_name):
        self.csv_path = csv_name
        self.loadding = self.load_csv(csv_name)
    
    def load_csv(self, csv_name):
    #CSVファイルからアラート基準、メモ、優待を読み込む。
    #存在しない場合は新しいCSVファイルを作成する。
    
        try:
            # CSVファイルをロード
            df = pd.read_csv(csv_name)
            print(f"CSVfileは存在しておりロードしまいました: {csv_name}")
            return df
        except FileNotFoundError:
            # CSVファイルが存在しない場合は作成
            print(f"{csv_name}は存在しません")
            return None
     
#csd.print_alert_threshold("9105.T")
#csd.add_ticker()
#csd.delete_ticker()
#csd.display_all_info()
"""