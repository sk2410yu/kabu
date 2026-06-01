"""機械学習パイプラインのCLIエントリポイント。

使い方の例:
    # 既定の銘柄リストで学習・評価し、モデルを保存
    python -m ml.run_ml train

    # 既存の銘柄CSVから先頭100銘柄を使って学習
    python -m ml.run_ml train --from-stocklist 100 --horizon 5

    # 学習済みモデルで当日の上位銘柄をランキング表示
    python -m ml.run_ml score --top 20
"""
import argparse
import os

import pandas as pd

from .dataset import build_dataset
from .model import (
    load_model,
    save_model,
    score_latest,
    train_and_evaluate,
)

# 動作確認用の既定銘柄（配当のある主要銘柄を中心に）
DEFAULT_TICKERS = [
    "8306.T", "9432.T", "8411.T", "9101.T", "9104.T",
    "8058.T", "5401.T", "8001.T", "8316.T", "8053.T",
    "7201.T", "2914.T", "9433.T", "8031.T", "8002.T",
    "8604.T", "8766.T", "8725.T", "5108.T", "6178.T",
    "9020.T", "9022.T", "5020.T", "5019.T", "1605.T",
    "8267.T", "3382.T", "2502.T", "2503.T", "4502.T",
]

_STOCKLIST_CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "..", "filter001", "prepare", "stocknumber_1month.csv")


def load_tickers_from_csv(limit, csv_path=_STOCKLIST_CSV):
    """既存の銘柄CSV（'コード'列、shift_jis）から先頭 limit 銘柄を読む。"""
    df = pd.read_csv(csv_path, encoding="shift_jis")
    if "コード" not in df.columns:
        raise ValueError(f"'コード' 列が見つかりません: {csv_path}")
    codes = df["コード"].dropna().astype(str).str.extract(r"(\d+)")[0].dropna()
    return [f"{c}.T" for c in codes.tolist()[:limit]]


def _print_metrics(metrics):
    bt = metrics["backtest"]
    print("=== 検証結果（時系列split: 後半=検証） ===")
    print(f"学習サンプル数: {metrics['n_train']}  検証サンプル数: {metrics['n_test']}")
    print(f"上昇ラベル比率  学習: {metrics['train_pos_rate']:.3f}  検証: {metrics['test_pos_rate']:.3f}")
    print(f"AUC: {metrics['auc']:.4f}   正答率: {metrics['accuracy']:.4f}")
    print("--- 簡易バックテスト（各検証日でスコア上位を購入） ---")
    print(f"上位平均リターン: {bt['top_mean_return']:.4%}  "
          f"全銘柄平均: {bt['all_mean_return']:.4%}  "
          f"エッジ: {bt['edge']:.4%}  (対象日数={bt['n_dates']})")


def cmd_train(args):
    tickers = (load_tickers_from_csv(args.from_stocklist)
               if args.from_stocklist else DEFAULT_TICKERS)
    print(f"銘柄数: {len(tickers)}  horizon={args.horizon}営業日  期間開始={args.start}")
    data = build_dataset(tickers, horizon=args.horizon, start=args.start,
                         interval=args.interval)
    print(f"データセット: {len(data)} 行 / 特徴量 {data.shape[1]} 列")
    model, metrics = train_and_evaluate(data, test_frac=args.test_frac,
                                        k_frac=args.k_frac, horizon=args.horizon)
    _print_metrics(metrics)
    path = save_model(model, args.model_path) if args.model_path else save_model(model)
    print(f"モデルを保存しました: {path}")


def cmd_score(args):
    tickers = (load_tickers_from_csv(args.from_stocklist)
               if args.from_stocklist else DEFAULT_TICKERS)
    model = load_model(args.model_path) if args.model_path else load_model()
    ranked = score_latest(tickers, model, start=args.start, interval=args.interval)
    cols = ["ticker", "date", "ml_score"]
    print("=== 当日 MLスコア ランキング（上昇確率の高い順） ===")
    with pd.option_context("display.max_rows", None, "display.width", 120):
        print(ranked[cols].head(args.top).to_string(index=False))


def build_parser():
    p = argparse.ArgumentParser(description="株価予測の機械学習パイプライン")
    sub = p.add_subparsers(dest="command", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--from-stocklist", type=int, default=0,
                        help="既存の銘柄CSVから先頭N銘柄を使う（0なら既定リスト）")
    common.add_argument("--start", default="2015-01-01", help="取得開始日")
    common.add_argument("--interval", default="1d", help="足種（既定: 1d）")
    common.add_argument("--model-path", default=None, help="モデルの保存/読込パス")

    pt = sub.add_parser("train", parents=[common], help="学習と評価")
    pt.add_argument("--horizon", type=int, default=5, help="予測する先のリターン日数")
    pt.add_argument("--test-frac", type=float, default=0.2, help="検証に回す後半割合")
    pt.add_argument("--k-frac", type=float, default=0.2, help="バックテストの上位割合")
    pt.set_defaults(func=cmd_train)

    ps = sub.add_parser("score", parents=[common], help="当日スコアのランキング")
    ps.add_argument("--top", type=int, default=20, help="表示する上位件数")
    ps.set_defaults(func=cmd_score)
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
