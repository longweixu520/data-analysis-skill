---
name: docx-analysis-report
description: 将数据分析 Markdown 报告转为格式规范的 Word 文档。在需要 .docx 正式交付、政府/企业公文风格报告时使用。
---

# Word 报告子 Skill

## 推荐流程

1. 先完成 `数据分析报告.md`（见 `references/roles/交付汇报手/references/报告模板.md`）
2. 用 python-docx 生成 Word，或 pandoc 转换

## python-docx 骨架

```python
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()
style = doc.styles["Normal"]
style.font.name = "宋体"
style.font.size = Pt(12)

title = doc.add_heading("数据分析报告", level=0)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.add_heading("1. 项目说明", level=1)
doc.add_paragraph("正文内容...")

# 插入表格
table = doc.add_table(rows=1, cols=3)
hdr = table.rows[0].cells
hdr[0].text = "主体"
hdr[1].text = "排名"
hdr[2].text = "综合指数"

doc.save("数据分析报告.docx")
```

## 插入图片

```python
from docx.shared import Inches
doc.add_picture("output/图表/fig01_排名.png", width=Inches(6))
```

## pandoc 转换（可选）

```bash
pandoc 数据分析报告.md -o 数据分析报告.docx --reference-doc=template.docx
```

## 样式要求

- 标题：黑体
- 正文：宋体 12pt，1.5 倍行距
- 表格：三线表风格
- 图表：居中，下方图题

## 依赖

```
python-docx>=1.1
```

## 注意

- 图表先用 PNG（Word 对 SVG 支持有限）
- 大表放附录，正文只保留核心行
