#!/usr/bin/env python3
"""Auto-generate data quality check table and summary."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.da_core import read_long_table, value_column, validate_long_table  # noqa: E402
from lib.eval_methods import audit_long_table  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description="生成数据质量检查表")
    parser.add_argument("long_csv", type=Path)
    parser.add_argument("-o", "--output", type=Path, default=None)
    args = parser.parse_args()

    df = read_long_table(args.long_csv)
    issues = validate_long_table(df)
    if issues:
        for i in issues:
            print(f"错误: {i}", file=sys.stderr)
        sys.exit(1)

    val_col = value_column(df)
    qc = audit_long_table(df, val_col)
    out = args.output or args.long_csv.parent / "03_数据质量检查表.csv"
    qc.to_csv(out, index=False, encoding="utf-8-sig")

    print(f"文件: {args.long_csv}")
    print(f"行数: {len(df)} | 主体: {df['主体'].nunique()} | 指标: {df['指标名称'].nunique()}")
    print(f"缺失率: {df[val_col].isna().mean():.1%}")
    print(f"质量问题条目: {len(qc)}")
    print(f"已写入 {out}")
    if len(qc) == 0:
        print("✅ 未发现结构化质量问题")


if __name__ == "__main__":
    main()
