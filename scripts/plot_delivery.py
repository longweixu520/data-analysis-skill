"""Generate standard delivery charts from analysis outputs."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.da_core import read_long_table, setup_chinese_matplotlib  # noqa: E402

PALETTE_PRIMARY = "#0F4D92"


def plot_ranking_bar(csv_path: Path, out_dir: Path, top_n: int = 15):
    import pandas as pd
    df = pd.read_csv(csv_path, encoding="utf-8-sig")
    score_col = "得分" if "得分" in df.columns else "综合指数"
    df = df.nlargest(top_n, score_col).sort_values(score_col)
    fig, ax = plt.subplots(figsize=(10, max(4, top_n * 0.35)))
    ax.barh(df["主体"], df[score_col], color=PALETTE_PRIMARY)
    ax.set_xlabel(score_col)
    ax.set_title(f"最新年份排名（Top {len(df)}）")
    for i, v in enumerate(df[score_col]):
        ax.text(v, i, f" {v:.3f}", va="center", fontsize=9)
    fig.tight_layout()
    for ext in ("png", "svg"):
        fig.savefig(out_dir / f"fig01_排名.{ext}", bbox_inches="tight")
    plt.close(fig)


def plot_trend_line(csv_path: Path, out_dir: Path, top_n: int = 5):
    import pandas as pd
    df = pd.read_csv(csv_path, encoding="utf-8-sig")
    if "综合指数" not in df.columns:
        return
    latest_year = df["年份"].max()
    top_subjects = (
        df[df["年份"] == latest_year]
        .nlargest(top_n, "综合指数")["主体"]
        .tolist()
    )
    sub = df[df["主体"].isin(top_subjects)]
    fig, ax = plt.subplots(figsize=(10, 5))
    for subject, g in sub.groupby("主体"):
        g = g.sort_values("年份")
        ax.plot(g["年份"], g["综合指数"], marker="o", label=subject)
    ax.set_xlabel("年份")
    ax.set_ylabel("综合指数")
    ax.set_title("综合指数年度趋势")
    ax.legend(loc="best", fontsize=8)
    fig.tight_layout()
    for ext in ("png", "svg"):
        fig.savefig(out_dir / f"fig02_趋势.{ext}", bbox_inches="tight")
    plt.close(fig)


def plot_weights_bar(csv_path: Path, out_dir: Path):
    import pandas as pd
    if not csv_path.exists():
        return
    df = pd.read_csv(csv_path, encoding="utf-8-sig")
    if df.empty:
        return
    latest = df["年份"].max()
    sub = df[df["年份"] == latest].sort_values("权重", ascending=True)
    fig, ax = plt.subplots(figsize=(8, max(4, len(sub) * 0.3)))
    ax.barh(sub["指标名称"], sub["权重"], color=PALETTE_PRIMARY)
    ax.set_xlabel("权重")
    ax.set_title(f"{latest} 年指标权重（熵值法）")
    fig.tight_layout()
    for ext in ("png", "svg"):
        fig.savefig(out_dir / f"fig03_权重.{ext}", bbox_inches="tight")
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description="从分析结果 CSV 生成标准图表")
    parser.add_argument("output_dir", type=Path, help="output/ 目录")
    parser.add_argument("--top-n", type=int, default=15)
    args = parser.parse_args()

    out = args.output_dir
    charts = out / "图表"
    charts.mkdir(parents=True, exist_ok=True)
    setup_chinese_matplotlib()

    rank_csv = out / "最新年份综合排名.csv"
    comp_csv = out / "综合指数.csv"
    weight_csv = out / "04_指标权重表.csv"

    if rank_csv.exists():
        plot_ranking_bar(rank_csv, charts, args.top_n)
        print(f"已生成 {charts}/fig01_排名.*")
    if comp_csv.exists():
        plot_trend_line(comp_csv, charts, min(5, args.top_n))
        print(f"已生成 {charts}/fig02_趋势.*")
    if weight_csv.exists():
        plot_weights_bar(weight_csv, charts)
        print(f"已生成 {charts}/fig03_权重.*")

    if not any(charts.glob("fig*")):
        print("未找到可绘图的结果文件", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
