#!/usr/bin/env python3
"""Master pipeline: analyze → plot → report → export → html → validate."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
PYTHON = sys.executable


def run(cmd: list[str], cwd: Path | None = None) -> None:
    print(f"\n>>> {' '.join(str(c) for c in cmd)}")
    subprocess.run(cmd, cwd=cwd or ROOT, check=True)


def main():
    parser = argparse.ArgumentParser(description="数据分析一键流水线")
    parser.add_argument("target", type=Path, nargs="?", default=Path("."), help="项目目录")
    parser.add_argument("--long-table", type=Path, default=None, help="直接指定长表路径")
    parser.add_argument("--weight-method", choices=["entropy", "critic", "equal"], default="entropy")
    parser.add_argument("--skip-html", action="store_true")
    parser.add_argument("--skip-validate", action="store_true")
    args = parser.parse_args()

    project = args.target.resolve()
    output = project / "output"
    long_csv = args.long_table or output / "02_清洗后长表.csv"

    if not long_csv.exists():
        print(f"长表不存在: {long_csv}", file=sys.stderr)
        sys.exit(1)

    run([PYTHON, str(SCRIPTS / "check_long_table.py"), str(long_csv)])
    run([PYTHON, str(SCRIPTS / "quality_report.py"), str(long_csv), "-o", str(output / "03_数据质量检查表.csv")])
    run([
        PYTHON, str(SCRIPTS / "analyze_long_table.py"), str(long_csv),
        "-o", str(output), "--weight-method", args.weight_method,
    ])
    run([PYTHON, str(SCRIPTS / "plot_delivery.py"), str(output)])
    run([PYTHON, str(SCRIPTS / "generate_report.py"), str(project)])
    run([PYTHON, str(SCRIPTS / "export_workbook.py"), str(output)])

    if not args.skip_html:
        run([PYTHON, str(SCRIPTS / "build_html_report.py"), str(project)])

    if not args.skip_validate:
        run([PYTHON, str(SCRIPTS / "validate_delivery.py"), str(output), "--strict", "--project", str(project)])

    print("\n✅ 流水线完成")


if __name__ == "__main__":
    main()
