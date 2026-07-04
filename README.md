# 📊 Data Analysis Skill

<div align="center">

**从原始表格到可交付结论 — 结构化四阶段数据分析流水线**

[![Agent Skill](https://img.shields.io/badge/Agent-Skill-blue)](https://cursor.com/docs/skills)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

</div>

---

## 简介

本技能面向 **Excel/CSV 统计表、面板数据、区域对标、综合评价** 等真实业务场景，提供 **数据侦查 → 数据工程 → 分析计算 → 交付汇报** 四阶段协作工作流，产出可复现、可审计、可交付的分析成果。

### 核心机制

| 机制 | 说明 |
|------|------|
| **Data Contract** | 分析前锁定核心问题、子问题-方法映射、交付规格 |
| **标准长表中枢** | 所有分析从长表出发，拒绝宽表临时计算 |
| **证据链原则** | 每个结论可追溯到 原始值→清洗规则→公式→输出表 |
| **四角色渐进加载** | 降低上下文负担，每阶段独立子 Skill |
| **工具选型矩阵** | 按文件大小自动选择 pandas / polars / DuckDB |
| **场景路由** | 按任务类型裁剪阶段，避免过度流程 |

---

## 特性

- 🔄 **四阶段流水线**：侦查、工程、计算、交付，阶段门禁质检
- 📋 **11 种表结构模式**：覆盖统计年鉴、多工作表、多层表头
- ⚖️ **综合评价方法库**：熵值法、AHP、TOPSIS、CRITIC
- 📈 **Figure Contract**：图表即论证，中文 SVG+PNG 双格式
- 🛠️ **三子 Skill**：xlsx / csv / docx
- ✅ **交付质检脚本**：`validate_delivery.py` 一键检查
- 🚀 **项目脚手架**：`init_project.py` 一键初始化目录

---

## 工作流程

| 阶段 | 角色 | 产出 |
|:----:|------|------|
| ① 侦查 | 数据侦查手 | 侦查报告 + Data Contract + 术语表 |
| ② 工程 | 数据工程手 | 标准长表 + 质量检查表 + 可复现脚本 |
| ③ 计算 | 分析计算手 | 排名/同比/综合指数/权重表 |
| ④ 交付 | 交付汇报手 | 中文图表 + 分析报告 + 交付清单 |

轻量任务可跳过阶段，见 [场景路由表](references/场景路由表.md)。

---

## 快速开始

### 安装

```bash
git clone https://github.com/longweixu520/data-analysis-skill.git
```

| Agent | 路径 |
|-------|------|
| Cursor | `~/.cursor/skills/data-analysis-skill` 或项目 `.cursor/skills/` |
| Claude Code | `~/.claude/skills/data-analysis-skill` |
| Codex | `~/.codex/skills/data-analysis-skill` |

### 初始化项目

```bash
python scripts/init_project.py my_analysis --with-sample
cd my_analysis
```

### 使用

```
/data-analysis 分析这份 Excel，做城市排名和综合指数，输出中文报告
```

分阶段：

```
/data-analysis 进行数据侦查
/data-analysis 进行数据工程
/data-analysis 进行分析计算
/data-analysis 进行交付汇报
```

### 依赖

```bash
pip install -r requirements.txt
```

---

## 目录结构

```
data-analysis-skill/
├── SKILL.md
├── README.md
├── CHANGELOG.md
├── assets/                  # 8 类方法资源库
├── references/
│   ├── 场景路由表.md
│   └── roles/               # 四角色子 Skill
├── tools/                   # xlsx / csv / docx
├── scripts/
│   ├── init_project.py
│   ├── profile_data.py
│   ├── entropy_weights.py
│   └── validate_delivery.py
└── examples/
```

---

## 方法覆盖

| 类别 | 文档 | 代表方法 |
|------|------|----------|
| 解析识别 | 01 | 11 种表结构、melt、多层表头 |
| 清洗治理 | 02 | 缺失值优先级、异常审计 |
| 描述对比 | 03 | 排名、同比环比、CAGR |
| 综合评价 | 04 | 熵值法、AHP、TOPSIS |
| 时间序列 | 05 | 趋势、断点、轻量预测 |
| 统计推断 | 06 | 相关、回归、效应量 |
| 可视化 | 07 | Figure Contract、中文图表 |
| 业务场景 | 08 | 城市对标、企业年报、问卷 |

---

## 默认交付物

```
output/
├── 01_原始标准长表.csv
├── 02_清洗后长表.csv
├── 03_数据质量检查表.csv
├── 04_指标权重表.csv
├── 综合指数.csv
├── 最新年份综合排名.csv
├── 同比分析.csv
└── 图表/
数据分析报告.md
交付清单.md
```

质检：

```bash
python scripts/validate_delivery.py output/
python scripts/validate_delivery.py output/ --strict
```

---

## 许可证

MIT License — 详见 [LICENSE](LICENSE)
