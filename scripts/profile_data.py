#!/usr/bin/env python3
"""Quick data profile for reconnaissance phase."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def profile_csv(path: Path, nrows: int) -> dict:
    import pandas as pd

    detect_script = ROOT / "tools/csv/scripts/detect_csv.py"
    proc = subprocess.run(
        [sys.executable, str(detect_script), str(path), "--recommend"],
        capture_output=True,
        text=True,
    )
    meta_lines = proc.stdout.strip().splitlines()

    encoding = "utf-8-sig"
    delim = ","
    recommend = "pandas"
    for line in meta_lines:
        if line.startswith("编码:"):
            encoding = line.split(":", 1)[1].strip().split()[0]
        if line.startswith("分隔符:"):
            delim = line.split(":", 1)[1].strip().strip("'\"")
        if line.startswith("推荐工具:"):
            recommend = line.split(":", 1)[1].strip()

    df = pd.read_csv(path, encoding=encoding, sep=delim, nrows=1000)
    return {
        "encoding": encoding,
        "delimiter": delim,
        "recommend": recommend,
        "columns": list(df.columns),
        "dtypes": {c: str(t) for c, t in df.dtypes.items()},
        "nrows_sampled": len(df),
        "missing_pct": {c: round(float(df[c].isna().mean()) * 100, 1) for c in df.columns},
        "head": df.head(nrows).fillna("").astype(str).to_dict(orient="records"),
    }


def profile_excel(path: Path, nrows: int) -> dict:
    probe_script = ROOT / "tools/xlsx/scripts/probe_excel.py"
    proc = subprocess.run(
        [sys.executable, str(probe_script), str(path), "-n", str(nrows), "--json"],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr or proc.stdout)
    return json.loads(proc.stdout)


def profile_file(path: Path, nrows: int = 5) -> dict:
    suffix = path.suffix.lower()
    result = {
        "path": str(path),
        "type": suffix,
        "size_mb": round(path.stat().st_size / 1024 / 1024, 2),
    }

    if suffix in (".xlsx", ".xls", ".xlsm"):
        result["excel"] = profile_excel(path, nrows)
    elif suffix == ".csv":
        result["csv"] = profile_csv(path, nrows)
    else:
        result["error"] = f"不支持的格式: {suffix}"

    return result


def main():
    parser = argparse.ArgumentParser(description="数据文件快速画像")
    parser.add_argument("path", type=Path)
    parser.add_argument("-n", "--nrows", type=int, default=5)
    args = parser.parse_args()

    if not args.path.exists():
        print(f"文件不存在: {args.path}", file=sys.stderr)
        sys.exit(1)

    try:
        result = profile_file(args.path, args.nrows)
    except Exception as e:
        print(f"画像失败: {e}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
