---
name: data-analysis
description: 处理 Excel、CSV、多工作表统计表、面板数据、指标评价、城市/企业/地区横向对比、同比环比、综合指数、权重计算、数据清洗与正式分析报告时使用。适用于从原始数据到可交付结论的完整流水线。在用户只信任原始文件、要求可复现流程、中文交付物、一键生成排名图表HTML报告时使用。
paths: "*.xlsx,*.xls,*.csv,*.xlsm"
---

# 数据分析技能 - Data Analysis

> **黄金路径**（有长表时一条命令交付）：`python scripts/run_pipeline.py <项目目录>`

本技能为**政务统计、企业经营、区域经济、行业对标、科研问卷**等场景提供结构化四阶段流水线 + **可执行工具链**，产出可复现、可审计、可分享的交付物。

## 30 秒开始

```bash
bash scripts/install_skill.sh      # 安装到 ~/.cursor/skills 等
python scripts/doctor.py           # 检查依赖
bash scripts/run_demo.sh           # 看完整产出长什么样
python scripts/init_project.py 我的项目 --with-sample
python scripts/run_pipeline.py 我的项目
```

## 技能概述

数据分析不是「算几个数」，而是**用证据链回答业务问题**：

1. **数据侦查**：理解数据来源、结构、口径与质量风险
2. **数据工程**：解析复杂表头、生成标准长表、治理缺失与异常
3. **分析计算**：描述统计、对比排名、综合评价、趋势推断
4. **交付汇报**：图表论证、正式报告、交付物质检

本技能采用**四角色协作模式**，各阶段按顺序依次执行，支持渐进式加载以降低上下文负担。

**任务路由**：`references/任务决策树.md` → `references/场景路由表.md` → `references/速查手册.md`

### 黄金路径（推荐）

```bash
python scripts/run_pipeline.py <项目目录>
```

等价于：校验 → 质量报告 → 分析 → 图表 → Markdown → Excel → HTML → 质检

### 分步命令链

```bash
python scripts/check_long_table.py output/02_清洗后长表.csv
python scripts/analyze_long_table.py output/02_清洗后长表.csv -o output/
python scripts/plot_delivery.py output/
python scripts/generate_report.py .
python scripts/validate_delivery.py output/ --strict
```

演示全流程：`bash scripts/run_demo.sh`

---

## 核心原则

### 可信源原则

- 默认**只信任用户明确指定的原始文件**
- 不把目录里旧 JSON、旧 CSV、旧结论当作真值
- 所有转换步骤必须可追溯、可复现

### 证据链原则

每个分析结论必须能追溯到：**原始值 → 清洗规则 → 计算公式 → 输出表/图**。不允许「静默补值」或「口径漂移」。

### 够用即可原则

```
1. 能用描述统计回答的，不上复杂模型
2. 能用标准长表 + 透视解决的，不硬写宽表逻辑
3. 能用熵值法/等权的，不堆叠黑盒模型
4. 图表服务于结论，不为好看而堆图
```

---

## 工作流程

### 第一阶段：数据侦查

**执行前提**：必须先读取 `references/roles/数据侦查手/SKILL.md`

**任务**：盘点项目、识别表结构、建立 Data Contract、产出侦查报告。

**产出**：
- `数据侦查报告.md` — 来源、结构模式、口径、风险、分析计划
- `Data_Contract.md` — 核心问题、子问题-方法映射、交付规格
- `术语与口径表.md` — 指标定义、单位、方向、中英文对照

**约束**：本阶段不写分析代码，不产出最终结论。

### 第二阶段：数据工程

**执行前提**：必须先读取 `references/roles/数据工程手/SKILL.md`

**任务**：按 Data Contract 编写解析器、生成标准长表、完成质量治理。

**产出**：
- `01_原始标准长表.csv`
- `02_清洗后长表.csv`
- `03_数据质量检查表.csv`
- `src/` — 可复现的解析与清洗脚本

### 第三阶段：分析计算

**执行前提**：必须先读取 `references/roles/分析计算手/SKILL.md`

**任务**：基于清洗后长表完成统计、对比、综合评价与必要推断。

**产出**：
- `04_指标权重表.csv`（若需综合评价）
- `综合指数.csv`、`最新年份综合排名.csv`、`同比分析.csv`
- `分析脚本/` — 分模块可运行脚本

### 第四阶段：交付汇报

**执行前提**：必须先读取 `references/roles/交付汇报手/SKILL.md`

**任务**：Figure Contract 可视化、撰写正式报告、执行交付质检。

**产出**：
- `图表/` — SVG + PNG 双格式，中文标注
- `数据分析报告.md`（及可选 `.docx`）
- `交付清单.md`

---

## 附加资源

### 方法资源库 (`assets/`)

| 文档 | 内容 |
|------|------|
| `01-数据解析与结构识别.md` | 11 种常见表结构模式、解析决策树 |
| `02-数据清洗与质量治理.md` | 缺失值、异常值、口径统一、审计规则 |
| `03-描述统计与对比分析.md` | 排名、同比环比、分组对比、贡献分解 |
| `04-综合评价与权重方法.md` | 熵值法、AHP、TOPSIS、CRITIC、等权 |
| `05-时间序列与趋势分析.md` | 趋势、季节性、CAGR、断点识别 |
| `06-统计推断与假设检验.md` | 相关、回归、显著性、效应量 |
| `07-可视化与报告规范.md` | Figure Contract、中文图表、报告架构 |
| `08-业务场景手册.md` | 城市对标、企业分析、问卷、面板数据 |
| `10-交付标准与质量标杆.md` | 三级交付标准、表述标杆 |

详见 `assets/README.md`。

### 角色说明 (`references/roles/`)

| 角色 | 阶段 | 入口 |
|------|------|------|
| 数据侦查手 | 侦查 | `references/roles/数据侦查手/SKILL.md` |
| 数据工程手 | 工程 | `references/roles/数据工程手/SKILL.md` |
| 分析计算手 | 计算 | `references/roles/分析计算手/SKILL.md` |
| 交付汇报手 | 交付 | `references/roles/交付汇报手/SKILL.md` |

### 集成子 Skill (`tools/`)

| 子 Skill | 用途 |
|----------|------|
| `tools/xlsx` | Excel 读取、多工作表探测、结构抽样 |
| `tools/csv` | CSV 编码检测、大文件工具选型（pandas/polars/DuckDB） |
| `tools/docx` | 正式 Word 报告生成 |

### 实用脚本 (`scripts/`)

| 脚本 | 用途 |
|------|------|
| `scripts/doctor.py` | 检查 Python 依赖是否就绪 |
| `scripts/check_long_table.py` | 校验长表 schema |
| `scripts/analyze_long_table.py` | 从长表生成排名/同比/综合指数 |
| `scripts/plot_delivery.py` | 从结果 CSV 生成标准中文图表 |
| `scripts/run_pipeline.py` | **一键完整交付**（推荐入口） |
| `scripts/quality_report.py` | 自动数据质量检查表 |
| `scripts/build_html_report.py` | 单文件 HTML 报告 |
| `scripts/parse_matrix.py` | 主体×年份矩阵 → 长表（模式 A） |
| `scripts/parse_from_config.py` | 按 analysis.config.yaml 批量解析 |
| `scripts/export_workbook.py` | 汇总 CSV 为 Excel 工作簿 |
| `scripts/init_project.py` | 初始化项目目录脚手架 |
| `scripts/profile_data.py` | 快速数据画像 |
| `scripts/entropy_weights.py` | 熵值法权重（宽表） |
| `scripts/generate_report.py` | 自动生成报告 Markdown 骨架 |
| `scripts/validate_delivery.py` | 交付物完整性质检 |
| `scripts/parse_from_config.py` | 按 analysis.config.yaml 批量解析 |
| `scripts/run_demo.sh` / `Makefile` | 演示 / `make pipeline` |

共享库：`scripts/lib/da_core.py`、`scripts/lib/parse_matrix.py`

---

## 默认输出目录结构

```
项目名/
├── 原始数据/           # 只读，不修改
├── 数据侦查报告.md
├── Data_Contract.md
├── 术语与口径表.md
├── output/
│   ├── 01_原始标准长表.csv
│   ├── 02_清洗后长表.csv
│   ├── 03_数据质量检查表.csv
│   ├── 04_指标权重表.csv
│   ├── 综合指数.csv
│   ├── 最新年份综合排名.csv
│   ├── 同比分析.csv
│   └── 图表/
├── src/
├── 数据分析报告.md
└── 交付清单.md
```

---

### 参考文档

| 文档 | 用途 |
|------|------|
| `references/速查手册.md` | 命令与文件流一页速查 |
| `references/场景路由表.md` | 按任务裁剪阶段 |
| `references/常见问题.md` | 排错 FAQ |

---

## 使用建议

1. **按顺序执行四阶段**，每阶段开始时加载对应角色 SKILL.md
2. **渐进式加载**：详细引用按需读取，避免一次性加载全部 assets
3. **为每个项目建独立文件夹**，原始数据与产出分离
4. **术语一致性**：侦查阶段建立的术语表贯穿后续阶段
5. **交付前运行** `python scripts/validate_delivery.py output/`

## 典型场景

- 「帮我分析这份 Excel 统计表，做城市排名和综合指数」
- 「多工作表结构混乱，先梳理再出报告」
- 「修复解析规则，生成标准长表」
- 「做同比环比和综合评价，输出中文报告和图表」
- 「面板数据横向对比，要可复现脚本」
