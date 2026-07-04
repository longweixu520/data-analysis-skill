#!/usr/bin/env python3
"""Build single-file HTML delivery report with embedded charts."""

from __future__ import annotations

import argparse
import base64
import html
from datetime import date
from pathlib import Path

import pandas as pd


def img_tag(path: Path) -> str:
    if not path.exists():
        return ""
    data = base64.b64encode(path.read_bytes()).decode()
    ext = path.suffix.lower().lstrip(".")
    mime = "svg+xml" if ext == "svg" else ext
    return f'<img src="data:image/{mime};base64,{data}" alt="{html.escape(path.stem)}" style="max-width:100%;margin:16px 0">'


def table_from_csv(path: Path, max_rows: int = 12) -> str:
    if not path.exists():
        return ""
    df = pd.read_csv(path, encoding="utf-8-sig").head(max_rows)
    return df.to_html(index=False, classes="data-table", border=0)


def build_html(project: Path, title: str) -> str:
    output = project / "output"
    charts = output / "图表"
    today = date.today().isoformat()

    summary_lines = []
    rank_path = output / "最新年份综合排名.csv"
    if rank_path.exists():
        rank = pd.read_csv(rank_path, encoding="utf-8-sig")
        score = "得分" if "得分" in rank.columns else rank.columns[-2]
        for _, r in rank.nsmallest(3, "排名").iterrows():
            summary_lines.append(
                f"<li><strong>{html.escape(str(r['主体']))}</strong> — 第{int(r['排名'])}名（{score}={r[score]:.4f}）</li>"
            )

    figs = []
    for p in sorted(charts.glob("fig*.png")):
        figs.append(f"<section><h3>{html.escape(p.stem)}</h3>{img_tag(p)}</section>")

    md_report = project / "数据分析报告.md"
    report_body = ""
    if md_report.exists():
        report_body = "<pre style='white-space:pre-wrap;font-family:inherit'>"
        report_body += html.escape(md_report.read_text(encoding="utf-8")[:4000])
        report_body += "</pre>"

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<style>
  :root {{ --primary:#0F4D92; --bg:#f7f9fc; --card:#fff; --text:#222; }}
  body {{ font-family: "PingFang SC","Microsoft YaHei",sans-serif; background:var(--bg); color:var(--text); margin:0; line-height:1.6; }}
  header {{ background:var(--primary); color:#fff; padding:28px 24px; }}
  header h1 {{ margin:0 0 8px; font-size:1.6rem; }}
  main {{ max-width:960px; margin:0 auto; padding:24px 16px 48px; }}
  .card {{ background:var(--card); border-radius:10px; padding:20px 24px; margin-bottom:20px; box-shadow:0 2px 8px rgba(0,0,0,.06); }}
  h2 {{ color:var(--primary); border-bottom:2px solid #e8eef5; padding-bottom:8px; }}
  table.data-table {{ width:100%; border-collapse:collapse; font-size:14px; }}
  table.data-table th, table.data-table td {{ border:1px solid #e0e0e0; padding:6px 10px; text-align:left; }}
  table.data-table th {{ background:#eef3fa; }}
  footer {{ text-align:center; color:#888; font-size:12px; padding:24px; }}
</style>
</head>
<body>
<header>
  <h1>{html.escape(title)}</h1>
  <p>数据分析交付报告 · {today}</p>
</header>
<main>
  <div class="card">
    <h2>核心发现</h2>
    <ul>{''.join(summary_lines) or '<li>见下方图表与数据表</li>'}</ul>
  </div>
  <div class="card">
    <h2>最新排名（节选）</h2>
    {table_from_csv(rank_path)}
  </div>
  <div class="card">
    <h2>图表</h2>
    {''.join(figs) or '<p>暂无图表</p>'}
  </div>
  <div class="card">
    <h2>完整报告</h2>
    {report_body or '<p>暂无 Markdown 报告</p>'}
  </div>
</main>
<footer>由 data-analysis-skill 自动生成</footer>
</body>
</html>"""


def main():
    parser = argparse.ArgumentParser(description="生成 HTML 交付报告")
    parser.add_argument("project_dir", type=Path)
    parser.add_argument("-n", "--name", type=str, default=None)
    parser.add_argument("-o", "--output", type=Path, default=None)
    args = parser.parse_args()

    title = args.name or args.project_dir.name
    out = args.output or (args.project_dir / "数据分析报告.html")
    out.write_text(build_html(args.project_dir, title), encoding="utf-8")
    print(f"已写入 {out}")


if __name__ == "__main__":
    main()
