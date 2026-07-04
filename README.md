# 📊 Data Analysis Skill

<div align="center">

**从原始表格到可交付结论 — 结构化四阶段数据分析流水线**

[![Agent Skill](https://img.shields.io/badge/Agent-Skill-blue)](https://cursor.com/docs/skills)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

</div>

---

## 简介

本技能为 **Excel/CSV 统计表、面板数据、区域对标、综合评价** 等真实业务数据分析场景，提供 **数据侦查 → 数据工程 → 分析计算 → 交付汇报** 四阶段协作工作流。

与 [math-modeling-skill](https://github.com/XiaoMaColtAI/math-modeling-skill) 互补：本 skill 聚焦**表格型业务数据的可复现交付**；数模 skill 聚焦**竞赛建模与论文**。

### 核心差异（原创设计）

| 机制 | 说明 |
|------|------|
| **Data Contract** | 类比 Model Contract，分析前锁定核心问题、子问题-方法映射、交付规格 |
| **标准长表中枢** | 所有分析从长表出发，拒绝宽表临时计算 |
| **证据链原则** | 每个结论可追溯到 原始值→清洗规则→公式→输出表 |
| **四角色渐进加载** | 降低上下文负担，每阶段独立子 Skill |
| **工具选型矩阵** | 按文件大小自动选择 pandas / polars / DuckDB |

---

## 特性

- 🔄 **四阶段流水线**：侦查、工程、计算、交付，阶段门禁质检
- 📋 **11 种表结构模式**：覆盖统计年鉴、多工作表、多层表头
- ⚖️ **综合评价方法库**：熵值法、AHP、TOPSIS、CRITIC
- 📈 **Figure Contract**：图表即论证，中文 SVG+PNG 双格式
- 🛠️ **三子 Skill**：xlsx / csv / docx
- ✅ **交付质检脚本**：`validate_delivery.py` 一键检查

---

## 工作流程

| 阶段 | 角色 | 产出 |
|:----:|------|------|
| ① 侦查 | 数据侦查手 | 侦查报告 + Data Contract + 术语表 |
| ② 工程 | 数据工程手 | 标准长表 + 质量检查表 + 可复现脚本 |
| ③ 计算 | 分析计算手 | 排名/同比/综合指数/权重表 |
| ④ 交付 | 交付汇报手 | 中文图表 + 分析报告 + 交付清单 |

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
├── SKILL.md                 # 技能主入口
├── README.md
├── assets/                  # 7 类方法资源库
├── references/
│   └── roles/               # 四角色子 Skill
│       ├── 数据侦查手/
│       ├── 数据工程手/
│       ├── 分析计算手/
│       └── 交付汇报手/
├── tools/
│   ├── xlsx/                # Excel 探测与处理
│   ├── csv/                 # 编码检测与工具选型
│   └── docx/                # Word 报告
├── scripts/
│   ├── profile_data.py      # 快速数据画像
│   └── validate_delivery.py # 交付质检
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
| 时间序列 | 05 | 趋势、断点、CAGR |
| 统计推断 | 06 | 相关、回归、效应量 |
| 可视化 | 07 | Figure Contract、中文图表 |

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
```

---

## 致谢

- [math-modeling-skill](https://github.com/XiaoMaColtAI/math-modeling-skill) — 三阶段角色协作与渐进加载架构参考
- [Anthropic xlsx skill](https://github.com/anthropics/skills/tree/main/skills/xlsx) — 表格处理模式参考
- CSV 工具选型思路参考社区 csv-data-wrangler 实践

---

## 许可证

MIT License — 详见 [LICENSE](LICENSE)
