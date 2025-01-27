def save_to_excel_stock(df, base_dir='stock'):
    """
    MACD_Signal_difference, DI+DI-_difference, Parabolic_SAR_difference
    による条件分割で8通りのデータをExcelシートに保存する関数。

    Args:
        df (pd.DataFrame): 保存対象のデータフレーム。以下の列を含む必要あり:
            - 'MACD_Signal_difference'
            - 'DI+DI-_difference'
            - 'Parabolic_SAR_difference'
        base_dir (str): 保存先ディレクトリのベース名。
    """
    from datetime import datetime
    import os
    import pandas as pd

    # 現在の日時を取得してファイル名を作成
    current_time = datetime.now().date().strftime("%Y%m%d")
    file_name = f"market_{current_time}.xlsx"

    # 保存ディレクトリを確認し、なければ作成
    if not os.path.exists(base_dir):
        os.mkdir(base_dir)

    file_path = os.path.join(base_dir, file_name)

    # 条件分けの組み合わせに基づきデータを分割
    conditions = [
        ('001_MAP_DMIP_PaP',
         (df['MACD_Signal_difference'] > 0) & (df['DI+DI-_difference'] > 0) & (df['Parabolic_SAR_difference'] > 0)),
        ('002_MAP_DMIP_PaN',
         (df['MACD_Signal_difference'] > 0) & (df['DI+DI-_difference'] > 0) & (df['Parabolic_SAR_difference'] <= 0)),
        ('003_MAP_DMIN_PaP',
         (df['MACD_Signal_difference'] > 0) & (df['DI+DI-_difference'] <= 0) & (df['Parabolic_SAR_difference'] > 0)),
        ('004_MACP_DMIN_PaN',
         (df['MACD_Signal_difference'] > 0) & (df['DI+DI-_difference'] <= 0) & (df['Parabolic_SAR_difference'] <= 0)),
        ('005_MACD_Signal_Negative_DI_Positive_SAR_Positive',
         (df['MACD_Signal_difference'] <= 0) & (df['DI+DI-_difference'] > 0) & (df['Parabolic_SAR_difference'] > 0)),
        ('006_MAN_DMIP_PaN',
         (df['MACD_Signal_difference'] <= 0) & (df['DI+DI-_difference'] > 0) & (df['Parabolic_SAR_difference'] <= 0)),
        ('007_MAN_DMI_PaP',
         (df['MACD_Signal_difference'] <= 0) & (df['DI+DI-_difference'] <= 0) & (df['Parabolic_SAR_difference'] > 0)),
        ('008_MAN_DMIN_PaN',
         (df['MACD_Signal_difference'] <= 0) & (df['DI+DI-_difference'] <= 0) & (df['Parabolic_SAR_difference'] <= 0)),
    ]

    # Excelファイルを保存
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        # 元のデータ全体を保存
        df.to_excel(writer, sheet_name='All_Data', index=False)

        # 条件に基づいてデータを保存
        for sheet_name, condition in conditions:
            subset = df[condition]
            if subset.empty:
                # 空の場合は空のデータフレームを作成して保存
                pd.DataFrame().to_excel(writer, sheet_name=sheet_name, index=False)
            else:
                # 条件に合うデータを保存
                subset.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f"Excelファイルを保存しました: {file_path}")
