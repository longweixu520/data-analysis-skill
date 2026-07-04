"""Long table analysis CLI."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# 允许从 skill 根目录运行
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.da_core import (  # noqa: E402
    composite_index_by_year,
    latest_ranking,
    read_long_table,
    validate_long_table,
    value_column,
    yoy_analysis,
)


def main():
    parser = argparse.ArgumentParser(description="从标准长表生成分析结果表")
    parser.add_argument("long_csv", type=Path, help="02_清洗后长表.csv")
    parser.add_argument("-o", "--output", type=Path, default=Path("output"))
    parser.add_argument("--indicator", type=str, default=None, help="单指标排名时指定指标名")
    parser.add_argument("--no-composite", action="store_true", help="不算综合指数")
    args = parser.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)
    df = read_long_table(args.long_csv)
    issues = validate_long_table(df)
    if issues:
        for i in issues:
            print(f"错误: {i}", file=sys.stderr)
        sys.exit(1)

    val_col = value_column(df)
    print(f"使用数值列: {val_col}")

    yoy = yoy_analysis(df, val_col)
    yoy_path = args.output / "同比分析.csv"
    yoy.to_csv(yoy_path, index=False, encoding="utf-8-sig")
    print(f"已写入 {yoy_path} ({len(yoy)} 行)")

    rank = latest_ranking(df, val_col, by_indicator=args.indicator)
    rank_path = args.output / "最新年份综合排名.csv"
    rank.to_csv(rank_path, index=False, encoding="utf-8-sig")
    print(f"已写入 {rank_path} ({len(rank)} 行)")

    if not args.no_composite:
        comp, weights = composite_index_by_year(df, val_col)
        if not comp.empty:
            comp_path = args.output / "综合指数.csv"
            w_path = args.output / "04_指标权重表.csv"
            comp.to_csv(comp_path, index=False, encoding="utf-8-sig")
            weights.to_csv(w_path, index=False, encoding="utf-8-sig")
            print(f"已写入 {comp_path} ({len(comp)} 行)")
            print(f"已写入 {w_path} ({len(weights)} 行)")
        else:
            print("跳过综合指数：纳入指标不足或覆盖不够", file=sys.stderr)


if __name__ == "__main__":
    main()
