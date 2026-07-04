---
name: xlsx-data-analysis
description: 数据分析场景下的 Excel 处理。读取 .xlsx/.xls、探测多工作表结构、抽样表头、导出标准长表。在分析 Excel 统计表、多工作表年鉴、复杂表头时使用。
---

# Excel 数据分析子 Skill

## 读取策略

**先探测，后解析** — 不要假设表头在第一行。

```python
import pandas as pd

# 探测：无表头读前 15 行
df = pd.read_excel("data.xlsx", sheet_name="Sheet1", header=None, nrows=15)
print(df.to_string())
```

## 多工作表遍历

```python
xl = pd.ExcelFile("data.xlsx")
for sheet in xl.sheet_names:
  sample = pd.read_excel(xl, sheet_name=sheet, header=None, nrows=15)
  print(f"=== {sheet} ===")
  print(sample)
```

## 合并单元格

```python
df = pd.read_excel("data.xlsx", sheet_name=0, header=2)
subject_col = df.columns[0]
df[subject_col] = df[subject_col].ffill()
```

## 导出

```python
df.to_excel("output/汇总.xlsx", index=False, engine="openpyxl")
# 标准长表优先 CSV（utf-8-sig）便于 diff 与版本管理
df.to_csv("output/02_清洗后长表.csv", index=False, encoding="utf-8-sig")
```

## 脚本

```bash
python tools/xlsx/scripts/probe_excel.py 原始数据/xxx.xlsx
```

## 依赖

```
pandas>=2.0
openpyxl>=3.1
xlrd>=2.0  # 仅 .xls
```

## 注意

- 公式单元格：用 `data_only=True`（openpyxl load_workbook）读计算值
- 大文件：考虑 `read_excel(..., usecols=)` 限定列
- 结构识别模式见 `assets/01-数据解析与结构识别.md`
