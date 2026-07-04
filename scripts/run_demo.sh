#!/usr/bin/env bash
# 一键演示：样本长表 → 分析 → 图表 → 报告 → 质检
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEMO="$ROOT/examples/demo"
PYTHON="${PYTHON:-python3}"

echo "==> 环境检查"
$PYTHON "$ROOT/scripts/doctor.py"

echo "==> 初始化演示项目"
rm -rf "$DEMO"
$PYTHON "$ROOT/scripts/init_project.py" "$DEMO" --with-sample --parent "$ROOT/examples"

echo "==> 长表校验"
$PYTHON "$ROOT/scripts/check_long_table.py" "$DEMO/output/02_清洗后长表.csv"

echo "==> 分析计算"
$PYTHON "$ROOT/scripts/analyze_long_table.py" "$DEMO/output/02_清洗后长表.csv" -o "$DEMO/output/"

echo "==> 生成图表"
$PYTHON "$ROOT/scripts/plot_delivery.py" "$DEMO/output/"

echo "==> 报告骨架"
$PYTHON "$ROOT/scripts/generate_report.py" "$DEMO" -n "演示项目"

echo "==> 交付质检"
$PYTHON "$ROOT/scripts/validate_delivery.py" "$DEMO/output/" --strict --project "$DEMO"

echo ""
echo "✅ 演示完成，产出目录: $DEMO/output/"
