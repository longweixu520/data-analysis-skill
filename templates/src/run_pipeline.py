"""项目流水线入口 — 解析 → 清洗 → 输出标准长表。"""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "原始数据"
OUTPUT = ROOT / "output"
OUTPUT.mkdir(parents=True, exist_ok=True)


def load_raw() -> pd.DataFrame:
    """TODO: 调用 src/parse/ 下各解析器，合并为长表。"""
    # 示例：若已有手工长表
    sample = OUTPUT / "01_原始标准长表.csv"
    if sample.exists():
        return pd.read_csv(sample, encoding="utf-8-sig")
    raise FileNotFoundError("请实现 load_raw() 或将原始 xlsx 放入 原始数据/")


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """清洗：类型转换、主体统一、补值（须写说明列）。"""
    out = df.copy()
    out["清洗值"] = pd.to_numeric(out.get("清洗值", out["原始值"]), errors="coerce")
    out["主体"] = out["主体"].astype(str).str.strip()
    return out


def main():
    raw = load_raw()
    raw.to_csv(OUTPUT / "01_原始标准长表.csv", index=False, encoding="utf-8-sig")

    cleaned = clean(raw)
    cleaned.to_csv(OUTPUT / "02_清洗后长表.csv", index=False, encoding="utf-8-sig")

    # 质量检查表：至少输出表头
    qc = OUTPUT / "03_数据质量检查表.csv"
    if not qc.exists():
        pd.DataFrame(columns=["检查项", "主体", "指标", "年份", "问题类型", "处理建议"]).to_csv(
            qc, index=False, encoding="utf-8-sig"
        )
    print(f"完成 → {OUTPUT}")


if __name__ == "__main__":
    main()
