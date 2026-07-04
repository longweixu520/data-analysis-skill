# 示例

## 一键演示

```bash
bash scripts/run_demo.sh
```

自动完成：环境检查 → 样本长表 → 分析 → 图表 → 报告 → 质检。  
产出在 `examples/demo/`（运行后生成，不纳入 git）。

## 新建真实项目

```bash
python scripts/init_project.py my_city_analysis --with-sample
cd my_city_analysis
# 1. 原始 Excel 放入 原始数据/
# 2. 编写 src/parse/ 与 src/run_pipeline.py
# 3. 流水线见 references/速查手册.md
```

## Agent 示例对话

```
用户：这份统计年鉴 Excel，帮我做 2024 年城市排名和综合指数，要中文报告。

Agent 路径：
  侦查 → Data Contract
  工程 → 02_清洗后长表.csv
  计算 → analyze_long_table.py
  交付 → plot_delivery.py + generate_report.py + validate --strict
```
