#!/usr/bin/env python3
"""Detect CSV encoding, delimiter, and recommend processing tool."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


def detect_encoding(path: Path, sample_size: int = 200_000) -> dict:
    try:
        import chardet
    except ImportError:
        chardet = None

    raw = path.read_bytes()[:sample_size]
    if chardet:
        det = chardet.detect(raw)
        return {"encoding": det.get("encoding"), "confidence": det.get("confidence")}
    for enc in ("utf-8-sig", "utf-8", "gbk", "gb18030", "latin-1"):
        try:
            raw.decode(enc)
            return {"encoding": enc, "confidence": None}
        except UnicodeDecodeError:
            continue
    return {"encoding": "utf-8", "confidence": None}


def detect_delimiter(path: Path, encoding: str) -> str:
    with path.open("r", encoding=encoding, errors="replace") as f:
        sample = f.read(8192)
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",\t;|")
        return dialect.delimiter
    except csv.Error:
        return ","


def recommend_tool(size_mb: float) -> str:
    if size_mb < 50:
        return "pandas"
    if size_mb < 500:
        return "polars"
    return "duckdb"


def main():
    parser = argparse.ArgumentParser(description="检测 CSV 编码与工具建议")
    parser.add_argument("path", type=Path)
    parser.add_argument("--recommend", action="store_true", help="输出工具建议")
    args = parser.parse_args()

    if not args.path.exists():
        print(f"文件不存在: {args.path}", file=sys.stderr)
        sys.exit(1)

    size_mb = args.path.stat().st_size / 1024 / 1024
    enc = detect_encoding(args.path)
    encoding = enc["encoding"] or "utf-8"
    delim = detect_delimiter(args.path, encoding)

    print(f"文件: {args.path}")
    print(f"大小: {size_mb:.2f} MB")
    print(f"编码: {encoding} (confidence={enc.get('confidence')})")
    print(f"分隔符: {repr(delim)}")

    if args.recommend:
        tool = recommend_tool(size_mb)
        print(f"推荐工具: {tool}")
        if tool == "pandas":
            print(f'  pd.read_csv("{args.path}", encoding="{encoding}", sep="{delim}")')
        elif tool == "polars":
            print(f'  pl.read_csv("{args.path}")')
        else:
            print(f"  duckdb.sql(\"SELECT * FROM read_csv_auto('{args.path}') LIMIT 10\")")


if __name__ == "__main__":
    main()
