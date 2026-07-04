#!/usr/bin/env python3
"""Initialize a data analysis project directory scaffold."""

from __future__ import annotations

import argparse
import textwrap
from pathlib import Path

SAMPLE_LONG_CSV = """\
来源文件,来源工作表,主体,年份,指标名称,指标分类,原始值,清洗值,单位,说明,指标方向,是否纳入综合指数
sample.xlsx,Sheet1,北京,2022,GDP,经济,41610,41610,亿元,,正向,是
sample.xlsx,Sheet1,北京,2023,GDP,经济,43760,43760,亿元,,正向,是
sample.xlsx,Sheet1,北京,2024,GDP,经济,45300,45300,亿元,,正向,是
sample.xlsx,Sheet1,上海,2022,GDP,经济,44653,44653,亿元,,正向,是
sample.xlsx,Sheet1,上海,2023,GDP,经济,47218,47218,亿元,,正向,是
sample.xlsx,Sheet1,上海,2024,GDP,经济,49100,49100,亿元,,正向,是
sample.xlsx,Sheet1,深圳,2022,GDP,经济,32388,32388,亿元,,正向,是
sample.xlsx,Sheet1,深圳,2023,GDP,经济,34606,34606,亿元,,正向,是
sample.xlsx,Sheet1,深圳,2024,GDP,经济,36200,36200,亿元,,正向,是
sample.xlsx,Sheet1,广州,2022,GDP,经济,28839,28839,亿元,,正向,是
sample.xlsx,Sheet1,广州,2023,GDP,经济,30356,30356,亿元,,正向,是
sample.xlsx,Sheet1,广州,2024,GDP,经济,31800,31800,亿元,,正向,是
sample.xlsx,Sheet1,北京,2022,研发投入强度,创新,6.2,6.2,%,,正向,是
sample.xlsx,Sheet1,北京,2023,研发投入强度,创新,6.4,6.4,%,,正向,是
sample.xlsx,Sheet1,北京,2024,研发投入强度,创新,6.5,6.5,%,,正向,是
sample.xlsx,Sheet1,上海,2022,研发投入强度,创新,4.2,4.2,%,,正向,是
sample.xlsx,Sheet1,上海,2023,研发投入强度,创新,4.4,4.4,%,,正向,是
sample.xlsx,Sheet1,上海,2024,研发投入强度,创新,4.5,4.5,%,,正向,是
sample.xlsx,Sheet1,深圳,2022,研发投入强度,创新,5.8,5.8,%,,正向,是
sample.xlsx,Sheet1,深圳,2023,研发投入强度,创新,6.0,6.0,%,,正向,是
sample.xlsx,Sheet1,深圳,2024,研发投入强度,创新,6.1,6.1,%,,正向,是
sample.xlsx,Sheet1,广州,2022,研发投入强度,创新,3.1,3.1,%,,正向,是
sample.xlsx,Sheet1,广州,2023,研发投入强度,创新,3.2,3.2,%,,正向,是
sample.xlsx,Sheet1,广州,2024,研发投入强度,创新,3.3,3.3,%,,正向,是
sample.xlsx,Sheet1,北京,2022,城镇化率,社会,87.6,87.6,%,,正向,是
sample.xlsx,Sheet1,北京,2023,城镇化率,社会,87.8,87.8,%,,正向,是
sample.xlsx,Sheet1,北京,2024,城镇化率,社会,88.0,88.0,%,,正向,是
sample.xlsx,Sheet1,上海,2022,城镇化率,社会,89.3,89.3,%,,正向,是
sample.xlsx,Sheet1,上海,2023,城镇化率,社会,89.5,89.5,%,,正向,是
sample.xlsx,Sheet1,上海,2024,城镇化率,社会,89.6,89.6,%,,正向,是
sample.xlsx,Sheet1,深圳,2022,城镇化率,社会,100.0,100.0,%,,正向,是
sample.xlsx,Sheet1,深圳,2023,城镇化率,社会,100.0,100.0,%,,正向,是
sample.xlsx,Sheet1,深圳,2024,城镇化率,社会,100.0,100.0,%,,正向,是
sample.xlsx,Sheet1,广州,2022,城镇化率,社会,86.5,86.5,%,,正向,是
sample.xlsx,Sheet1,广州,2023,城镇化率,社会,86.7,86.7,%,,正向,是
sample.xlsx,Sheet1,广州,2024,城镇化率,社会,86.9,86.9,%,,正向,是
"""

DATA_CONTRACT = """\
# Data Contract

## 核心问题
[用一句话描述本次分析要回答的问题]

## 可信数据源
| 文件 | 说明 |
|------|------|
| 原始数据/ | 用户指定，只读 |

## 子问题-方法映射
| 子问题 | 方法 | 产出 |
|--------|------|------|
| 1. | | |

## 交付清单
- [ ] 01_原始标准长表.csv
- [ ] 02_清洗后长表.csv
- [ ] 03_数据质量检查表.csv
- [ ] 数据分析报告.md
"""

RUN_PIPELINE = '''\
"""一键运行：解析 → 清洗 → 输出标准长表。"""
from pathlib import Path
import pandas as pd

OUTPUT = Path(__file__).resolve().parent.parent / "output"
OUTPUT.mkdir(parents=True, exist_ok=True)

def main():
    # TODO: 替换为实际解析逻辑
    sample = OUTPUT.parent / "output" / "02_清洗后长表.csv"
    if sample.exists():
        print(f"已存在 {sample}，跳过")
        return
    print("请实现 src/run_pipeline.py 中的解析逻辑")

if __name__ == "__main__":
    main()
'''


def create_project(root: Path, with_sample: bool) -> None:
    dirs = [
        root / "原始数据",
        root / "output" / "图表",
        root / "src" / "parse",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

    (root / "Data_Contract.md").write_text(DATA_CONTRACT, encoding="utf-8")
    (root / "数据侦查报告.md").write_text("# 数据侦查报告\n\n待填写。\n", encoding="utf-8")
    (root / "术语与口径表.md").write_text(
        "| 指标名称 | 单位 | 方向 | 说明 |\n|----------|------|------|------|\n",
        encoding="utf-8",
    )
    (root / "交付清单.md").write_text("# 交付清单\n\n- [ ] output/\n", encoding="utf-8")
    (root / "src" / "run_pipeline.py").write_text(RUN_PIPELINE, encoding="utf-8")
    (root / "src" / "parse" / "__init__.py").write_text("", encoding="utf-8")
    (root / "requirements.txt").write_text("pandas>=2.0\nopenpyxl>=3.1\nmatplotlib>=3.8\n", encoding="utf-8")

    gitkeep = root / "原始数据" / ".gitkeep"
    gitkeep.write_text("", encoding="utf-8")

    if with_sample:
        (root / "output" / "02_清洗后长表.csv").write_text(SAMPLE_LONG_CSV, encoding="utf-8-sig")
        (root / "output" / "01_原始标准长表.csv").write_text(SAMPLE_LONG_CSV, encoding="utf-8-sig")
        (root / "output" / "03_数据质量检查表.csv").write_text(
            "检查项,主体,指标,年份,问题类型,处理建议\n", encoding="utf-8-sig"
        )


def main():
    parser = argparse.ArgumentParser(description="初始化数据分析项目目录")
    parser.add_argument("name", type=str, help="项目目录名")
    parser.add_argument("--with-sample", action="store_true", help="生成示例长表")
    parser.add_argument("--parent", type=Path, default=Path.cwd(), help="父目录")
    args = parser.parse_args()

    root = args.parent / args.name
    if root.exists() and any(root.iterdir()):
        raise SystemExit(f"目录非空: {root}")

    create_project(root, args.with_sample)
    print(f"已创建项目: {root}")
    print(textwrap.dedent("""
        下一步:
          1. 将原始文件放入 原始数据/
          2. 填写 Data_Contract.md
          3. python src/run_pipeline.py
          4. python ../scripts/validate_delivery.py output/
    """).strip())


if __name__ == "__main__":
    main()
