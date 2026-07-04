#!/usr/bin/env python3
"""Detect CSV encoding and delimiter."""
import argparse
import sys
from pathlib import Path


def guess_sep(line: str) -> str:
    for sep in [",", "\t", "|", ";"]:
        if line.count(sep) >= 2:
            return sep
    return ","


def main():
    parser = argparse.ArgumentParser(description="Detect CSV encoding and delimiter")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    path = args.path
    if not path.exists():
        print(f"Error: {path} not found", file=sys.stderr)
        sys.exit(1)

    raw = path.read_bytes()[:200_000]
    encoding = "utf-8"
    confidence = 0.0
    try:
        import chardet
        det = chardet.detect(raw)
        encoding = det.get("encoding") or "utf-8"
        confidence = det.get("confidence") or 0.0
    except ImportError:
        for enc in ("utf-8-sig", "utf-8", "gb18030", "gbk"):
            try:
                raw.decode(enc)
                encoding = enc
                confidence = 1.0
                break
            except UnicodeDecodeError:
                continue

    try:
        first_line = raw.decode(encoding, errors="replace").splitlines()[0]
    except Exception:
        first_line = ""

    sep = guess_sep(first_line)
    size_mb = path.stat().st_size / (1024 * 1024)

    print(f"file: {path}")
    print(f"size_mb: {size_mb:.2f}")
    print(f"encoding: {encoding} (confidence: {confidence:.2f})")
    print(f"delimiter: {repr(sep)}")
    if size_mb < 50:
        print("recommend: pandas")
    elif size_mb < 500:
        print("recommend: polars")
    else:
        print("recommend: duckdb")


if __name__ == "__main__":
    main()
