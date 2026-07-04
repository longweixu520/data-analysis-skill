"""Pattern A: subject x year matrix → long table."""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

YEAR_RE = re.compile(r"^(20\d{2})(年)?$")


def detect_year_columns(columns) -> list:
    years = []
    for c in columns:
        s = str(c).strip()
        if YEAR_RE.match(s):
            years.append(c)
    return years


def matrix_to_long(
    df: pd.DataFrame,
    subject_col: str | int,
    indicator_name: str,
    indicator_category: str = "",
    source_file: str = "",
    source_sheet: str = "",
    unit: str = "",
    direction: str = "正向",
    in_composite: str = "是",
    header_row: int | None = None,
) -> pd.DataFrame:
    """将「主体×年份」矩阵转为标准长表。"""
    work = df.copy()
    if header_row is not None:
        work.columns = work.iloc[header_row]
        work = work.iloc[header_row + 1 :].reset_index(drop=True)

    if subject_col not in work.columns:
        subject_col = work.columns[0]

    year_cols = detect_year_columns(work.columns)
    if not year_cols:
        raise ValueError("未识别到年份列（格式 2019 或 2019年）")

    work = work[[subject_col] + year_cols].copy()
    work = work.rename(columns={subject_col: "主体"})
    work["主体"] = work["主体"].astype(str).str.strip()

    long = work.melt(id_vars=["主体"], value_vars=year_cols, var_name="年份", value_name="原始值")
    long["年份"] = long["年份"].astype(str).str.extract(r"(20\d{2})")[0].astype(int)
    long["原始值"] = pd.to_numeric(long["原始值"], errors="coerce")
    long["清洗值"] = long["原始值"]
    long["指标名称"] = indicator_name
    long["指标分类"] = indicator_category
    long["来源文件"] = source_file
    long["来源工作表"] = source_sheet
    long["单位"] = unit
    long["说明"] = ""
    long["指标方向"] = direction
    long["是否纳入综合指数"] = in_composite
    return long


def parse_excel_matrix(
    path: str | Path,
    sheet_name: str | int = 0,
    subject_col: str | int = 0,
    indicator_name: str = "指标",
    header_row: int | None = None,
    **kwargs,
) -> pd.DataFrame:
    path = Path(path)
    df = pd.read_excel(path, sheet_name=sheet_name, header=None if header_row is not None else 0)
    return matrix_to_long(
        df,
        subject_col=subject_col,
        indicator_name=indicator_name,
        source_file=path.name,
        source_sheet=str(sheet_name),
        header_row=header_row,
        **kwargs,
    )
