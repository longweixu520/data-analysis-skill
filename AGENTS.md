# Agent 使用指南

本仓库是 **data-analysis** Agent Skill，供 Cursor / Claude Code / Codex 等加载。

## 触发

用户提到：Excel/CSV 分析、排名、综合指数、同比、数据清洗、中文报告 等。

## 执行顺序

1. 读 `SKILL.md` + `references/场景路由表.md`（裁剪阶段）
2. 当前阶段角色 `references/roles/*/SKILL.md`
3. 按需读 `assets/` 与 `references/速查手册.md`

## 可执行命令（优先使用，少写一次性代码）

```bash
python scripts/doctor.py
python scripts/init_project.py <name> --with-sample
python scripts/parse_matrix.py <file> --indicator <名> -o output/01_*.csv
python scripts/check_long_table.py output/02_清洗后长表.csv
python scripts/analyze_long_table.py output/02_清洗后长表.csv -o output/
python scripts/plot_delivery.py output/
python scripts/generate_report.py .
python scripts/export_workbook.py output/
python scripts/validate_delivery.py output/ --strict
bash scripts/run_demo.sh
make demo   # 同上
```

## 硬性约束

- 只信用户指定的原始文件
- 补值必须写入 `说明` 列
- 结论必须对应 output/ 中的表或图
- 中文交付时图表与报告全部中文

## 目录

| 路径 | 用途 |
|------|------|
| `assets/` | 方法库 |
| `references/roles/` | 四角色细则 |
| `scripts/lib/` | 可复用 Python 库 |
| `templates/` | 复制到用户项目的脚手架 |
