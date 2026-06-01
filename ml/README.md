# ml — 機械学習による株価予測

第1フィルターで計算している既存のテクニカル指標（MACD / DMI / パラボリックSAR /
RSI / ストキャス / サイコロジカル / RCI / 移動平均乖離）を**そのまま特徴量**として再利用し、
**翌 N 営業日のリターンが上昇するか**を予測するモデルを学習・評価・推論する。

## 構成

| ファイル | 役割 |
|----------|------|
| `features.py` | 既存指標を再利用し、価格スケールに依存しない特徴量に整形（`FEATURE_COLUMNS`） |
| `dataset.py` | 銘柄×日付の特徴量に、`shift(-horizon)` でフォワードリターンのラベルを付与 |
| `model.py` | 時系列split（境界に embargo）で学習・評価、AUC/正答率＋上位K銘柄の簡易バックテスト |
| `run_ml.py` | CLI（`train` / `score`） |

## 使い方

```bash
# 学習・評価（既定の銘柄リスト）。モデルは ml/model.joblib に保存される
python -m ml.run_ml train --horizon 5

# 既存の銘柄CSV（filter001/prepare/stocknumber_1month.csv）の先頭100銘柄で学習
python -m ml.run_ml train --from-stocklist 100 --horizon 5

# 学習済みモデルで当日の上昇確率を高い順にランキング表示
python -m ml.run_ml score --top 20
```

## 設計上のポイント（金融時系列のリーク対策）

- **シャッフルしない**：日付で前半=学習 / 後半=検証に分割（ウォークフォワード）。
- **embargo**：ラベルが未来 `horizon` 日を参照するため、検証開始日の直前 `horizon`
  取引日を学習から除外し、境界での情報リークを防ぐ。
- **特徴量は定常寄り**：MACD/SAR など価格スケール依存の指標は終値で正規化。

## 注意

- AUC は 0.5 付近になりやすい（株価の短期予測は本質的に困難）。本モジュールは
  「既存特徴量を使った予測の土台」であり、特徴量追加・銘柄数拡大・ハイパラ調整・
  別ターゲット（相対リターン等）で改善していく前提。
- 依存：`pip install -r ml/requirements.txt`
