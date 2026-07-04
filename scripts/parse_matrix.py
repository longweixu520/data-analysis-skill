#!/usr/bin/env python3
"""CLI: Excel/CSV matrix → standard long table (pattern A)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.parse_matrix import matrix_to_long, parse_excel_matrix  # noqa: E402
import pandas as pd  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description="主体×年份矩阵 → 标准长表")
    parser.add_argument("input", type=Path)
    parser.add_argument("-o", "--output", type=Path, default=Path("output/01_原始标准长表.csv"))
    parser.add_argument("--sheet", default=0)
    parser.add_argument("--subject-col", default="0", help="主体列名或列索引")
    parser.add_argument("--indicator", required=True, help="指标名称")
    parser.add_argument("--category", default="", help="指标分类")
    parser.add_argument("--unit", default="")
    parser.add_argument("--header-row", type=int, default=None, help="表头所在行（0-based）")
    args = parser.parse_args()

    subject_col: str | int = int(args.subject_col) if str(args.subject_col).isdigit() else args.subject_col

    suffix = args.input.suffix.lower()
    if suffix in (".xlsx", ".xls", ".xlsm"):
        sheet = int(args.sheet) if str(args.sheet).isdigit() else args.sheet
        long = parse_excel_matrix(
            args.input,
            sheet_name=sheet,
            subject_col=subject_col,
            indicator_name=args.indicator,
            indicator_category=args.category,
            unit=args.unit,
            header_row=args.header_row,
        )
    elif suffix == ".csv":
        df = pd.read_csv(args.input, encoding="utf-8-sig", header=None if args.header_row is not None else 0)
        long = matrix_to_long(
            df,
            subject_col=subject_col,
            indicator_name=args.indicator,
            indicator_category=args.category,
            source_file=args.input.name,
            unit=args.unit,
            header_row=args.header_row,
        )
    else:
        print(f"不支持: {suffix}", file=sys.stderr)
        sys.exit(1)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    long.to_csv(args.output, index=False, encoding="utf-8-sig")
    print(f"已写入 {args.output} ({len(long)} 行, {long['主体'].nunique()} 主体)")


if __name__ == "__main__":
    main()
