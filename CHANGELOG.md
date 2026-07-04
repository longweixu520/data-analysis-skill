# 更新日志

## v1.4.0 (2026-07)

### 一键交付
- `run_pipeline.py`：分析→图→报告→Excel→HTML→质检 一条命令
- `build_html_report.py`：单文件 HTML 交付（可浏览器直接打开分享）
- `quality_report.py`：自动质量审计表

### 评价方法
- CRITIC / 等权 / 熵值法（`--weight-method`）
- `eval_methods.py`：TOPSIS、CRITIC、audit

### 配置驱动
- `templates/analysis.config.yaml` + `parse_from_config.py`
- `install_skill.sh` 一键安装到 Cursor/Codex/Claude

### 图表与标准
- 雷达图 fig05；`assets/10-交付标准与质量标杆.md`
- `references/任务决策树.md`

## v1.3.0 (2026-07)

- `parse_matrix.py`：模式 A 矩阵一键转长表
- `export_workbook.py`：多 sheet Excel 汇总交付
- `plot_delivery` 增加热力图（fig04）
- `Makefile`、`AGENTS.md`、`templates/src/run_pipeline.py`
- `assets/09-解析代码模板.md`
- SKILL.md 增加 `paths` 自动触发

## v1.2.0 (2026-07)

### 可运行工具链
- `scripts/lib/da_core.py`：熵权、综合指数、同比、中文 matplotlib
- `analyze_long_table.py`：长表 → 排名/同比/综合指数
- `plot_delivery.py`：标准排名/趋势/权重图（PNG+SVG）
- `generate_report.py`：自动报告骨架
- `check_long_table.py` / `doctor.py`：校验与环境检查
- `run_demo.sh`：一键演示全流程

### 文档
- `references/速查手册.md`、`references/常见问题.md`
- 样本数据扩展为 4 城 × 3 年 × 3 指标

## v1.1.0 (2026-07)

- 新增 `references/场景路由表.md`：按任务裁剪四阶段
- 新增 `assets/08-业务场景手册.md`：6 类典型场景默认路径
- 新增 `scripts/init_project.py`：项目脚手架
- 新增 `scripts/entropy_weights.py`：熵值法权重 CLI
- 增强 `validate_delivery.py`：行数检查、strict 模式扩展
- 文档去外部项目引用，定位为独立 skill
- csv 子 Skill 更名为 `csv-analysis`

## v1.0.0 (2026-07)

- 初始发布：四阶段流水线、四角色子 Skill
- 7 类方法资源库、xlsx/csv/docx 子 Skill
- profile_data / validate_delivery 脚本
