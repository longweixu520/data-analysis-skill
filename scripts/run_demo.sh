#!/usr/bin/env bash
# 一键演示：样本长表 → 完整流水线
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEMO="$ROOT/examples/demo"
PYTHON="${PYTHON:-python3}"

echo "==> 环境检查"
$PYTHON "$ROOT/scripts/doctor.py"

echo "==> 初始化演示项目"
rm -rf "$DEMO"
$PYTHON "$ROOT/scripts/init_project.py" demo --with-sample --parent "$ROOT/examples"

echo "==> 一键流水线"
$PYTHON "$ROOT/scripts/run_pipeline.py" "$DEMO"

echo ""
echo "✅ 演示完成"
echo "   数据: $DEMO/output/"
echo "   报告: $DEMO/数据分析报告.md"
echo "   HTML: $DEMO/数据分析报告.html"
