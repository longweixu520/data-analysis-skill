#!/usr/bin/env python3
"""Parse Excel workbook from analysis.config.yaml."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

try:
    import yaml
except ImportError:
    yaml = None

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.parse_matrix import parse_excel_matrix  # noqa: E402


def load_config(path: Path) -> dict:
    if yaml is None:
        raise SystemExit("需要 PyYAML: pip install pyyaml")
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def parse_entry(raw_dir: Path, entry: dict) -> pd.DataFrame:
    path = raw_dir / entry["file"]
    sheet = entry.get("sheet", 0)
    if str(sheet).isdigit():
        sheet = int(sheet)
    in_comp = entry.get("in_composite", True)
    return parse_excel_matrix(
        path,
        sheet_name=sheet,
        subject_col=entry.get("subject_col", 0),
        indicator_name=entry["indicator"],
        indicator_category=entry.get("category", ""),
        unit=entry.get("unit", ""),
        direction=entry.get("direction", "正向"),
        in_composite="是" if in_comp else "否",
        header_row=entry.get("header_row"),
    )


def main():
    parser = argparse.ArgumentParser(description="按 analysis.config.yaml 批量解析 Excel")
    parser.add_argument("config", type=Path, help="analysis.config.yaml")
    parser.add_argument("-o", "--output", type=Path, default=None)
    args = parser.parse_args()

    cfg = load_config(args.config)
    project_root = args.config.parent
    raw_dir = project_root / cfg.get("data", {}).get("raw_dir", "原始数据")
    out = args.output or project_root / "output" / "01_原始标准长表.csv"

    parts = []
    for entry in cfg.get("parse", []):
        if entry.get("pattern", "matrix_a") != "matrix_a":
            print(f"跳过未支持模式: {entry}", file=sys.stderr)
            continue
        parts.append(parse_entry(raw_dir, entry))

    if not parts:
        print("无解析条目", file=sys.stderr)
        sys.exit(1)

    long = pd.concat(parts, ignore_index=True)
    out.parent.mkdir(parents=True, exist_ok=True)
    long.to_csv(out, index=False, encoding="utf-8-sig")
    print(f"已写入 {out} ({len(long)} 行)")


if __name__ == "__main__":
    main()
