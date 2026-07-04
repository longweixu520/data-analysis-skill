#!/usr/bin/env python3
"""Probe Excel workbook structure for data analysis reconnaissance."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def probe_excel(path: Path, nrows: int = 15) -> dict:
    try:
        import pandas as pd
    except ImportError:
        print("需要安装 pandas 和 openpyxl: pip install pandas openpyxl", file=sys.stderr)
        sys.exit(1)

    if not path.exists():
        raise FileNotFoundError(path)

    xl = pd.ExcelFile(path)
    result = {
        "path": str(path),
        "size_mb": round(path.stat().st_size / 1024 / 1024, 2),
        "sheets": [],
    }

    for name in xl.sheet_names:
        df = pd.read_excel(xl, sheet_name=name, header=None, nrows=nrows)
        sample = df.fillna("").astype(str).values.tolist()
        result["sheets"].append({
            "name": name,
            "nrows_sampled": len(df),
            "ncols": len(df.columns),
            "sample": sample,
        })

    return result


def main():
    parser = argparse.ArgumentParser(description="探测 Excel 工作表结构")
    parser.add_argument("path", type=Path, help="Excel 文件路径")
    parser.add_argument("-n", "--nrows", type=int, default=15, help="抽样行数")
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    args = parser.parse_args()

    result = probe_excel(args.path, args.nrows)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"文件: {result['path']} ({result['size_mb']} MB)")
        for sheet in result["sheets"]:
            print(f"\n=== Sheet: {sheet['name']} ({sheet['ncols']} 列) ===")
            for i, row in enumerate(sheet["sample"]):
                print(f"  {i:2d} | " + " | ".join(str(c)[:20] for c in row[:8]))
                if len(row) > 8:
                    print(f"      ... +{len(row)-8} 列")


if __name__ == "__main__":
    main()
