#!/usr/bin/env python3
"""Entropy weight method for composite index."""

from __future__ import annotations

import argparse
import json
import sys

import numpy as np
import pandas as pd


def entropy_weights(norm_matrix: pd.DataFrame) -> pd.Series:
    """Rows=entities, cols=indicators, values in [0,1]."""
    X = norm_matrix.values.astype(float)
    m, n = X.shape
    if m < 2 or n == 0:
        return pd.Series(1.0 / max(n, 1), index=norm_matrix.columns)
    X = X + 1e-12
    P = X / X.sum(axis=0)
    k = 1.0 / np.log(m)
    E = -k * (P * np.log(P)).sum(axis=0)
    D = 1 - E
    total = D.sum()
    if total <= 0:
        return pd.Series(1.0 / n, index=norm_matrix.columns)
    return pd.Series(D / total, index=norm_matrix.columns)


def min_max_by_columns(df: pd.DataFrame, positive: dict[str, bool]) -> pd.DataFrame:
    out = pd.DataFrame(index=df.index)
    for col in df.columns:
        s = df[col]
        lo, hi = s.min(), s.max()
        if hi == lo:
            out[col] = 1.0
        elif positive.get(col, True):
            out[col] = (s - lo) / (hi - lo)
        else:
            out[col] = (hi - s) / (hi - lo)
    return out


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

    norm = min_max_by_columns(numeric, {c: True for c in numeric.columns})
    weights = entropy_weights(norm)

    result = pd.DataFrame({
        "指标名称": weights.index,
        "权重": weights.values.round(6),
    })
    result.to_csv(args.output, index=False, encoding="utf-8-sig")
    print(json.dumps(weights.round(6).to_dict(), ensure_ascii=False, indent=2))
    print(f"已写入 {args.output}")


if __name__ == "__main__":
    main()
