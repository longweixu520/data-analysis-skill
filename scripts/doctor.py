#!/usr/bin/env python3
"""Check skill runtime dependencies."""

from __future__ import annotations

import importlib
import sys

REQUIRED = ["pandas", "numpy", "matplotlib", "openpyxl"]
OPTIONAL = ["seaborn", "polars", "duckdb", "chardet", "docx", "scipy", "statsmodels"]


def check():
    print("=== 数据分析 Skill 环境检查 ===\n")
    ok = True
    for pkg in REQUIRED:
        try:
            m = importlib.import_module(pkg if pkg != "docx" else "docx")
            ver = getattr(m, "__version__", "ok")
            print(f"✅ {pkg}: {ver}")
        except ImportError:
            print(f"❌ {pkg}: 未安装")
            ok = False

    print("\n可选依赖:")
    for pkg in OPTIONAL:
        try:
            name = "docx" if pkg == "docx" else pkg
            m = importlib.import_module(name)
            ver = getattr(m, "__version__", "ok")
            print(f"  ✅ {pkg}: {ver}")
        except ImportError:
            print(f"  ○ {pkg}: 未安装")

    if not ok:
        print("\n请运行: pip install -r requirements.txt")
        sys.exit(1)
    print("\n✅ 核心依赖就绪")


if __name__ == "__main__":
    check()
