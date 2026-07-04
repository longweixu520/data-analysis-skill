#!/usr/bin/env python3
"""Validate data analysis delivery artifacts."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REQUIRED_CORE = [
    "01_原始标准长表.csv",
    "02_清洗后长表.csv",
    "03_数据质量检查表.csv",
]

OPTIONAL_ANALYSIS = [
    "04_指标权重表.csv",
    "综合指数.csv",
    "最新年份综合排名.csv",
    "同比分析.csv",
]

LONG_TABLE_COLUMNS = {
    "主体", "年份", "指标名称", "原始值", "清洗值",
}


def check_dir(output_dir: Path, strict: bool = False) -> list[str]:
    errors: list[str] = []
    warnings: list[str] = []

    if not output_dir.is_dir():
        return [f"输出目录不存在: {output_dir}"]

    for name in REQUIRED_CORE:
        p = output_dir / name
        if not p.exists():
            errors.append(f"缺少必需文件: {name}")

    cleaned = output_dir / "02_清洗后长表.csv"
    if cleaned.exists():
        try:
            import pandas as pd
            df = pd.read_csv(cleaned, encoding="utf-8-sig", nrows=5)
            missing_cols = LONG_TABLE_COLUMNS - set(df.columns)
            if missing_cols:
                errors.append(f"02_清洗后长表 缺少列: {missing_cols}")
        except Exception as e:
            errors.append(f"无法读取 02_清洗后长表.csv: {e}")

    has_analysis = any((output_dir / f).exists() for f in OPTIONAL_ANALYSIS)
    if not has_analysis:
        warnings.append("未发现分析结果表（若仅需清洗可忽略）")

    charts = output_dir / "图表"
    if charts.is_dir():
        pngs = list(charts.glob("*.png"))
        svgs = list(charts.glob("*.svg"))
        if pngs and not svgs:
            warnings.append("图表目录有 PNG 但无 SVG（建议双格式）")
    elif strict:
        warnings.append("缺少 图表/ 目录")

    report_md = output_dir.parent / "数据分析报告.md"
    if strict and not report_md.exists():
        warnings.append("缺少 数据分析报告.md")

    return errors + [f"[警告] {w}" for w in warnings]


def main():
    parser = argparse.ArgumentParser(description="交付物质检")
    parser.add_argument("output_dir", type=Path, help="output/ 目录路径")
    parser.add_argument("--strict", action="store_true", help="严格模式（要求报告和图表）")
    args = parser.parse_args()

    issues = check_dir(args.output_dir, strict=args.strict)
    errors = [i for i in issues if not i.startswith("[警告]")]

    for issue in issues:
        print(issue)

    if errors:
        print(f"\n❌ 质检未通过 ({len(errors)} 个错误)")
        sys.exit(1)
    print("\n✅ 质检通过")
    if any(i.startswith("[警告]") for i in issues):
        print("（存在警告，请确认）")


if __name__ == "__main__":
    main()
