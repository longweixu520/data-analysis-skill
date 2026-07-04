#!/usr/bin/env python3
"""Validate long table schema and basic quality."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.da_core import read_long_table, validate_long_table  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description="校验标准长表")
    parser.add_argument("csv", type=Path)
    args = parser.parse_args()

    df = read_long_table(args.csv)
    issues = validate_long_table(df)

    print(f"文件: {args.csv}")
    print(f"行数: {len(df)}")
    print(f"主体数: {df['主体'].nunique() if '主体' in df.columns else 'N/A'}")
    print(f"年份范围: {df['年份'].min()}–{df['年份'].max()}" if "年份" in df.columns else "")
    print(f"指标数: {df['指标名称'].nunique() if '指标名称' in df.columns else 'N/A'}")

    if issues:
        for i in issues:
            print(f"❌ {i}")
        sys.exit(1)
    print("✅ 长表校验通过")


if __name__ == "__main__":
    main()
