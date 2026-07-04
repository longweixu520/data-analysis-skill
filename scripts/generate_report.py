#!/usr/bin/env python3
"""从分析产出自动生成报告骨架。"""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

import pandas as pd


def load_summary(output_dir: Path) -> dict:
    summary = {}
    rank_path = output_dir / "最新年份综合排名.csv"
    comp_path = output_dir / "综合指数.csv"

    if rank_path.exists():
        rank = pd.read_csv(rank_path, encoding="utf-8-sig")
        score_col = "得分" if "得分" in rank.columns else rank.columns[-2]
        top3 = rank.nsmallest(3, "排名")
        summary["top3"] = [
            f"{r['主体']}（排名第{int(r['排名'])}，{score_col}={r[score_col]:.4f}）"
            for _, r in top3.iterrows()
        ]
        summary["latest_year"] = int(rank["年份"].max()) if "年份" in rank.columns else ""

    if comp_path.exists():
        comp = pd.read_csv(comp_path, encoding="utf-8-sig")
        if len(comp) >= 2:
            years = sorted(comp["年份"].unique())
            if len(years) >= 2:
                y0, y1 = years[-2], years[-1]
                avg0 = comp[comp["年份"] == y0]["综合指数"].mean()
                avg1 = comp[comp["年份"] == y1]["综合指数"].mean()
                if avg0:
                    summary["avg_yoy"] = (avg1 - avg0) / avg0

    return summary


def build_report(project_name: str, summary: dict, contract_path: Path | None) -> str:
    today = date.today().isoformat()
    core_q = "［待填写核心问题］"
    if contract_path and contract_path.exists():
        for line in contract_path.read_text(encoding="utf-8").splitlines():
            if "核心问题" in line or line.startswith("## 核心"):
                continue
            if line.strip() and not line.startswith("#") and "［" not in line:
                core_q = line.strip()
                break

    lines = [
        f"# {project_name} 数据分析报告",
        "",
        f"> 报告日期：{today}",
        "",
        "## 摘要",
        "",
    ]

    if summary.get("top3"):
        lines.append(f"- **{summary.get('latest_year', '')}年排名前 3**：" + "；".join(summary["top3"]))
    if summary.get("avg_yoy") is not None:
        pct = summary["avg_yoy"] * 100
        lines.append(f"- **综合指数均值同比**：{pct:+.2f}%（仅供参考）")

    lines.extend([
        "",
        "## 1. 项目说明",
        f"核心问题：{core_q}",
        "",
        "## 2. 数据来源",
        "| 文件 | 说明 |",
        "|------|------|",
        "| 原始数据/ | 用户指定原始文件 |",
        "",
        "## 3. 处理流程",
        "1. 数据侦查 → 2. 数据工程 → 3. 分析计算 → 4. 交付汇报",
        "",
        "## 4. 核心结果",
        "［根据 output/ 下 CSV 补充具体数字与解读］",
        "",
        "## 5. 图表解读",
        "- 图1 排名：见 `output/图表/fig01_排名.png`",
        "- 图2 趋势：见 `output/图表/fig02_趋势.png`",
        "",
        "## 6. 风险与限制",
        "- 补值与口径假设见数据质量检查表",
        "",
        "## 7. 交付清单",
        "| 文件 | 说明 |",
        "|------|------|",
        "| output/02_清洗后长表.csv | 清洗后标准长表 |",
        "| output/最新年份综合排名.csv | 排名结果 |",
        "| output/综合指数.csv | 综合指数（若适用） |",
        "",
    ])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="生成数据分析报告骨架")
    parser.add_argument("project_dir", type=Path, help="项目根目录")
    parser.add_argument("-n", "--name", type=str, default=None, help="报告标题")
    args = parser.parse_args()

    output = args.project_dir / "output"
    name = args.name or args.project_dir.name
    contract = args.project_dir / "Data_Contract.md"
    summary = load_summary(output)
    report = build_report(name, summary, contract)
    out_path = args.project_dir / "数据分析报告.md"
    out_path.write_text(report, encoding="utf-8")
    print(f"已写入 {out_path}")


if __name__ == "__main__":
    main()
