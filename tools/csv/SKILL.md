---
name: csv-data-wrangler
description: CSV 编码检测、分隔符识别、按文件大小选择 pandas/polars/DuckDB。在分析大型 CSV、编码乱码、高性能数据处理时使用。
---

# CSV 数据处理子 Skill

## 工具选型

| 文件大小 | 工具 | 理由 |
|----------|------|------|
| < 50 MB | pandas | 生态成熟 |
| 50–500 MB | polars | 内存效率高 |
| > 500 MB | DuckDB | SQL 查询、懒加载 |

## 编码检测

```bash
python tools/csv/scripts/detect_csv.py data.csv
```

或：

```python
import chardet
with open(path, "rb") as f:
    raw = f.read(100000)
print(chardet.detect(raw))
```

常见：`utf-8-sig`, `gbk`, `gb18030`

## pandas 读取

```python
import pandas as pd
df = pd.read_csv("data.csv", encoding="utf-8-sig", low_memory=False)
```

## polars 读取

```python
import polars as pl
df = pl.read_csv("data.csv", encoding="utf8-lossy", infer_schema_length=10000)
```

## DuckDB 查询

```python
import duckdb
duckdb.sql("SELECT * FROM read_csv_auto('data.csv') LIMIT 10").show()
duckdb.sql("COPY (SELECT ...) TO 'output/result.parquet' (FORMAT PARQUET)")
```

## 脚本

```bash
python tools/csv/scripts/detect_csv.py data.csv
python tools/csv/scripts/detect_csv.py data.csv --recommend
```

## 依赖

```
pandas>=2.0
polars>=0.20  # 可选
duckdb>=0.10  # 可选
chardet>=5.0
```
