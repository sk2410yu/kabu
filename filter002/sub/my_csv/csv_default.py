import pandas as pd

class Csv_Default:
    def __init__(self, csv_name):
        self.csv_path = csv_name
        self.loading = self.load_csv()

    def load_csv(self):
        """CSVがなければ作成する"""
        try:
            df = pd.read_csv(self.csv_path)
            print("デフォルト設定を読み込んでいます")
        except FileNotFoundError:
            print("デフォルト設定がないので作ります")
            data = {
                "最大価格": [],
                "最小価格": [],
                "配当の有無": [],
                "希望配当利回り": []
            }
            df = pd.DataFrame(data)
            df.to_csv(self.csv_path, index=False, encoding="UTF-8")
        return df
    
    def first_defalt(self):
        """初期設定"""
        max = input("最大価格: ")
        min = input("最小価格:")
        try:
            threshold = float(input("配当の有無: "))
        except ValueError:
            print("無効な数値です。再度入力してください。")
            return

        want_threshold = input("希望配当利回り: ")

        new_row = {
                '最大価格': max,
                '最小価格': min,
                '配当の有無': threshold,
                '希望配当利回り': want_threshold
         }
        self.loading = pd.concat([self.loading, pd.DataFrame([new_row])], ignore_index=True)
        self.save_to_csv()
        print(f"最大価格は{max}最小価格は'{min}'配当の有無は'{threshold}'希望配当利回りは{want_threshold}")


    def update(self):
        if self.loading.empty:
            print("データがないので初期設定を開始します")
            self.first_defalt()

        try:
            idx = 0
            max_price = float(input(f"新しい最大価格を入力(現在)): "))
            min_price = float(input("新しい最小価格を入力: "))
            dividend = input("配当の有無を入力 (例: 有/無): ")
            yield_rate = float(input("新しい希望配当利回りを入力: "))

            # Update the specified row in the DataFrame
            self.loading.loc[idx, '最大価格'] = max_price
            self.loading.loc[idx, '最小価格'] = min_price
            self.loading.loc[idx, '配当の有無'] = dividend
            self.loading.loc[idx, '希望配当利回り'] = yield_rate

            # Save changes to CSV
            self.save_to_csv()
            print("選択した行が更新されました。")
        except ValueError:
            print("無効な入力です。再度お試しください。")
    
    def display_all_info(self):
        """すべてのデータを表示する"""
        if self.loading.empty:
            print("データが見つかりませんでした")
        else:
            print("全デフォルト設定情報:")
            print(self.loading.to_string(index=False))
                
    def save_to_csv(self):
        """CSVに保存."""
        try:
            self.loading.to_csv(self.csv_path, index=False, encoding="UTF-8")
            print("問題なくデータの保存が完了しました")
        except Exception as e:
            print(f"{e}エラーにより保存に失敗しました")
            
    def every_time(self):
        self.display_all_info()
        default_update_checker = int(input("デフォルト設定を変更しますか？(する場合は0,それ以外は0以外で):"))
        if default_update_checker == 0:
            self.update()
            self.display_all_info()
        

# インスタンスを作成してテスト
#csv_manager = Csv_Default('Default.csv')
#csv_manager.every_time()