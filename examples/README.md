# 示例：最小可运行流水线

本示例演示四阶段产出的**目录结构**，不含真实数据。

## 目录结构

```
my_project/
├── 原始数据/
│   └── sample_stats.xlsx      # 用户提供的原始文件
├── Data_Contract.md
├── 数据侦查报告.md
├── 术语与口径表.md
├── src/
│   ├── parse/city_year.py
│   ├── clean.py
│   └── run_pipeline.py
├── output/
│   ├── 01_原始标准长表.csv
│   ├── 02_清洗后长表.csv
│   ├── 03_数据质量检查表.csv
│   ├── 综合指数.csv
│   ├── 最新年份综合排名.csv
│   └── 图表/
├── 数据分析报告.md
└── 交付清单.md
```

## 启动命令

```bash
# 1. 侦查
/data-analysis 进行数据侦查

# 2. 工程
/data-analysis 进行数据工程

# 3. 计算
/data-analysis 进行分析计算

# 4. 交付
/data-analysis 进行交付汇报

# 质检
python scripts/validate_delivery.py my_project/output/
```

## 一句话启动

```
/data-analysis 分析这份 Excel，做城市排名和综合指数，输出中文报告
```

Agent 将自动按四阶段流水线执行。
