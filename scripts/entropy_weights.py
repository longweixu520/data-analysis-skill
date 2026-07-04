#!/usr/bin/env python3
"""Entropy weight method — thin CLI over da_core."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.da_core import entropy_weights, min_max_norm  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description="熵值法计算指标权重")
    parser.add_argument("csv", type=str, help="宽表 CSV：行=主体，列=指标")
    parser.add_argument("-o", "--output", type=str, default="权重表.csv")
    parser.add_argument("--index-col", type=str, default=None, help="主体列名")
    args = parser.parse_args()

    df = pd.read_csv(args.csv, encoding="utf-8-sig")
    if args.index_col:
        df = df.set_index(args.index_col)
    else:
        df = df.set_index(df.columns[0])

    numeric = df.select_dtypes(include="number")
    if numeric.empty:
        print("无数值列", file=sys.stderr)
        sys.exit(1)

    norm = pd.DataFrame({c: min_max_norm(numeric[c], True) for c in numeric.columns})
    weights = entropy_weights(norm)

    result = pd.DataFrame({"指标名称": weights.index, "权重": weights.values.round(6)})
    result.to_csv(args.output, index=False, encoding="utf-8-sig")
    print(json.dumps(weights.round(6).to_dict(), ensure_ascii=False, indent=2))
    print(f"已写入 {args.output}")


if __name__ == "__main__":
    main()
