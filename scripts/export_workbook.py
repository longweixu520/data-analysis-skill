#!/usr/bin/env python3
"""Export analysis CSVs to a single Excel workbook."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


SHEETS = [
    ("01_原始标准长表", "01_原始标准长表.csv"),
    ("02_清洗后长表", "02_清洗后长表.csv"),
    ("03_质量检查", "03_数据质量检查表.csv"),
    ("04_指标权重", "04_指标权重表.csv"),
    ("综合指数", "综合指数.csv"),
    ("最新排名", "最新年份综合排名.csv"),
    ("同比分析", "同比分析.csv"),
]


def main():
    parser = argparse.ArgumentParser(description="汇总 output/ CSV 为 Excel 工作簿")
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("-o", "--out", type=Path, default=None)
    args = parser.parse_args()

    out_xlsx = args.out or (args.output_dir / "数据分析汇总.xlsx")
    written = 0
    with pd.ExcelWriter(out_xlsx, engine="openpyxl") as writer:
        for sheet_name, filename in SHEETS:
            path = args.output_dir / filename
            if path.exists():
                df = pd.read_csv(path, encoding="utf-8-sig")
                # Excel sheet name max 31 chars
                df.to_excel(writer, sheet_name=sheet_name[:31], index=False)
                written += 1

    if written == 0:
        print("未找到可导出的 CSV", file=__import__("sys").stderr)
        raise SystemExit(1)
    print(f"已写入 {out_xlsx}（{written} 个工作表）")


if __name__ == "__main__":
    main()
