#!/usr/bin/env bash
# 安装 data-analysis-skill 到本机 Agent skills 目录
set -euo pipefail
SRC="$(cd "$(dirname "$0")/.." && pwd)"
NAME="data-analysis-skill"

install_one() {
  local dest="$1"
  mkdir -p "$(dirname "$dest")"
  if [ -e "$dest" ]; then
    echo "已存在，跳过: $dest"
  else
    ln -sf "$SRC" "$dest" 2>/dev/null || cp -R "$SRC" "$dest"
    echo "已安装 → $dest"
  fi
}

install_one "$HOME/.cursor/skills/$NAME"
install_one "$HOME/.codex/skills/$NAME"
install_one "$HOME/.claude/skills/$NAME"

echo ""
echo "验证: 在 Agent 中输入 /data-analysis 或打开 xlsx/csv 文件触发 skill"
