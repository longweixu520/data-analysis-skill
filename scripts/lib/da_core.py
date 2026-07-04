"""数据分析 skill 核心工具函数 — 供 scripts/ 与项目 src/ 复用。"""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd

LONG_TABLE_SCHEMA = [
    "来源文件", "来源工作表", "主体", "年份", "指标名称", "指标分类",
    "原始值", "清洗值", "单位", "说明", "指标方向", "是否纳入综合指数",
]

REQUIRED_COLUMNS = {"主体", "年份", "指标名称", "原始值", "清洗值"}


def read_long_table(path: str | Path) -> pd.DataFrame:
    return pd.read_csv(path, encoding="utf-8-sig")


def validate_long_table(df: pd.DataFrame) -> list[str]:
    issues: list[str] = []
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        issues.append(f"缺少必需列: {missing}")
    if len(df) == 0:
        issues.append("表为空")
        return issues
    if "年份" in df.columns and not pd.api.types.is_numeric_dtype(df["年份"]):
        issues.append("年份列应为数值类型")
    dup = df.duplicated(subset=[c for c in ["主体", "年份", "指标名称", "来源工作表"] if c in df.columns])
    if dup.any():
        issues.append(f"存在 {dup.sum()} 行重复记录")
    return issues


def value_column(df: pd.DataFrame, prefer: str = "清洗值") -> str:
    if prefer in df.columns and df[prefer].notna().any():
        return prefer
    return "原始值"


def entropy_weights(norm_matrix: pd.DataFrame) -> pd.Series:
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


def min_max_norm(series: pd.Series, positive: bool = True) -> pd.Series:
    lo, hi = series.min(), series.max()
    if hi == lo:
        return pd.Series(1.0, index=series.index)
    if positive:
        return (series - lo) / (hi - lo)
    return (hi - series) / (hi - lo)


def is_positive_direction(direction) -> bool:
    if pd.isna(direction):
        return True
    return str(direction).strip() in {"正向", "正", "+", "1", "True", "true"}


def filter_composite_indicators(df: pd.DataFrame) -> pd.DataFrame:
    if "是否纳入综合指数" not in df.columns:
        return df
    mask = df["是否纳入综合指数"].astype(str).str.strip().isin({"是", "Y", "yes", "true", "1"})
    return df[mask]


def normalize_year_panel(
    df: pd.DataFrame,
    year: int,
    val_col: str,
) -> tuple[pd.DataFrame, pd.Series]:
    """返回 (标准化矩阵, 权重)。"""
    sub = df[df["年份"] == year].copy()
    indicators = sub["指标名称"].unique()
    directions = {
        ind: is_positive_direction(sub.loc[sub["指标名称"] == ind, "指标方向"].iloc[0])
        for ind in indicators
    }
    pivot = sub.pivot_table(index="主体", columns="指标名称", values=val_col, aggfunc="first")
    norm = pd.DataFrame(index=pivot.index)
    for ind in pivot.columns:
        norm[ind] = min_max_norm(pivot[ind], positive=directions.get(ind, True))
    weights = entropy_weights(norm)
    return norm, weights


def composite_index_by_year(df: pd.DataFrame, val_col: str) -> pd.DataFrame:
    df = filter_composite_indicators(df)
    years = sorted(df["年份"].dropna().unique())
    rows = []
    weight_rows = []

    for year in years:
        year = int(year)
        sub = df[df["年份"] == year]
        coverage = sub.groupby("主体")["指标名称"].nunique()
        min_indicators = sub["指标名称"].nunique()
        valid_subjects = coverage[coverage >= min_indicators].index
        sub = sub[sub["主体"].isin(valid_subjects)]
        if sub.empty or sub["指标名称"].nunique() < 2:
            continue

        norm, weights = normalize_year_panel(sub, year, val_col)
        scores = (norm * weights).sum(axis=1)
        for subject, score in scores.items():
            rows.append({"主体": subject, "年份": year, "综合指数": round(float(score), 6)})
        for ind, w in weights.items():
            weight_rows.append({"年份": year, "指标名称": ind, "权重": round(float(w), 6)})

    index_df = pd.DataFrame(rows)
    if not index_df.empty:
        index_df["排名"] = index_df.groupby("年份")["综合指数"].rank(ascending=False, method="min").astype(int)
    weight_df = pd.DataFrame(weight_rows)
    return index_df, weight_df


def latest_ranking(df: pd.DataFrame, val_col: str, by_indicator: str | None = None) -> pd.DataFrame:
    if by_indicator:
        sub = df[df["指标名称"] == by_indicator].copy()
        score_name = by_indicator
    else:
        comp, _ = composite_index_by_year(df, val_col)
        if not comp.empty:
            latest = comp["年份"].max()
            sub = comp[comp["年份"] == latest][["主体", "年份", "综合指数"]].copy()
            sub = sub.rename(columns={"综合指数": "得分"})
            sub["排名"] = sub["得分"].rank(ascending=False, method="min").astype(int)
            return sub.sort_values("排名")
        sub = df.copy()
        score_name = "得分"

    latest = sub["年份"].max()
    sub = sub[sub["年份"] == latest].copy()
    sub["得分"] = sub[val_col]
    sub["排名"] = sub["得分"].rank(ascending=False, method="min").astype(int)
    return sub[["主体", "年份", "得分", "排名"]].sort_values("排名")


def yoy_analysis(df: pd.DataFrame, val_col: str) -> pd.DataFrame:
    parts = []
    for (subject, indicator), g in df.groupby(["主体", "指标名称"]):
        g = g.sort_values("年份").copy()
        g["上期"] = g[val_col].shift(1)
        g["同比"] = (g[val_col] - g["上期"]) / g["上期"]
        g.loc[g["上期"].isin([0]) | g["上期"].isna(), "同比"] = pd.NA
        parts.append(g[["主体", "年份", "指标名称", val_col, "同比"]])
    return pd.concat(parts, ignore_index=True)


def setup_chinese_matplotlib():
    import os
    import matplotlib.pyplot as plt
    # 避免无写权限环境下 matplotlib 崩溃
    cache = Path(os.environ.get("MPLCONFIGDIR", "/tmp/mpl-cache-data-analysis"))
    cache.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("MPLCONFIGDIR", str(cache))
    plt.rcParams.update({
        "font.sans-serif": ["PingFang SC", "STHeiti", "SimHei", "Microsoft YaHei", "Arial Unicode MS"],
        "axes.unicode_minus": False,
        "figure.dpi": 120,
        "savefig.dpi": 300,
        "svg.fonttype": "none",
    })
