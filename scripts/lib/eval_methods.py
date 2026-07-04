"""TOPSIS, CRITIC, data quality audit."""

from __future__ import annotations

import numpy as np
import pandas as pd

from .da_core import min_max_norm  # noqa: F401



def critic_weights(norm_matrix: pd.DataFrame) -> pd.Series:
    """CRITIC 客观赋权。"""
    X = norm_matrix.values.astype(float)
    n, m = X.shape
    if m == 0:
        return pd.Series(dtype=float)
    std = X.std(axis=0, ddof=0)
    corr = np.corrcoef(X.T)
    if m == 1:
        corr = np.array([[1.0]])
    conflict = (1 - corr).sum(axis=0)
    info = std * conflict
    total = info.sum()
    if total <= 0:
        return pd.Series(1.0 / m, index=norm_matrix.columns)
    return pd.Series(info / total, index=norm_matrix.columns)


def equal_weights(columns) -> pd.Series:
    n = len(columns)
    return pd.Series(1.0 / n, index=columns)


def get_weights(norm_matrix: pd.DataFrame, method: str = "entropy") -> pd.Series:
    method = method.lower()
    if method == "critic":
        return critic_weights(norm_matrix)
    if method == "equal":
        return equal_weights(norm_matrix.columns)
    from .da_core import entropy_weights
    return entropy_weights(norm_matrix)


def topsis_scores(norm_matrix: pd.DataFrame, weights: pd.Series) -> pd.Series:
    """TOPSIS 贴近度，越大越好。"""
    W = norm_matrix.values * weights.values
    ideal_best = W.max(axis=0)
    ideal_worst = W.min(axis=0)
    d_pos = np.sqrt(((W - ideal_best) ** 2).sum(axis=1))
    d_neg = np.sqrt(((W - ideal_worst) ** 2).sum(axis=1))
    denom = d_pos + d_neg
    denom[denom == 0] = 1e-12
    c = d_neg / denom
    return pd.Series(c, index=norm_matrix.index)


def audit_long_table(df: pd.DataFrame, val_col: str = "清洗值") -> pd.DataFrame:
    """生成数据质量检查行。"""
    rows = []
    key_cols = [c for c in ["主体", "年份", "指标名称", "来源工作表"] if c in df.columns]

    if key_cols:
        dup = df.duplicated(subset=key_cols, keep=False)
        for _, r in df[dup].iterrows():
            rows.append({
                "检查项": "重复记录", "主体": r.get("主体"), "指标": r.get("指标名称"),
                "年份": r.get("年份"), "问题类型": "重复记录", "处理建议": "去重或合并",
            })

    for _, r in df[df[val_col].isna()].iterrows():
        rows.append({
            "检查项": "缺失", "主体": r.get("主体"), "指标": r.get("指标名称"),
            "年份": r.get("年份"), "问题类型": "结构性空值", "处理建议": "保留或按规则补值",
        })

    if val_col in df.columns:
        for ind in df["指标名称"].unique():
            sub = df[df["指标名称"] == ind][val_col].dropna()
            if sub.empty:
                continue
            if ind in {"人口", "企业数", "学校数", "常住人口"} or "人数" in str(ind):
                bad = df[(df["指标名称"] == ind) & (df[val_col].notna()) & (df[val_col] % 1 != 0)]
                for _, r in bad.iterrows():
                    rows.append({
                        "检查项": "类型异常", "主体": r.get("主体"), "指标": ind,
                        "年份": r.get("年份"), "问题类型": "计数型出现小数", "处理建议": "置空并核查列",
                    })

    return pd.DataFrame(rows, columns=["检查项", "主体", "指标", "年份", "问题类型", "处理建议"])
