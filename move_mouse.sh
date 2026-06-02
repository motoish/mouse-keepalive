#!/usr/bin/env bash
# 本地开发入口：在仓库根目录直接运行，无需 pip/npm 全局安装
# Local dev entry: run from repo root without global pip/npm install
#
#   ./move_mouse.sh
#   ./move_mouse.sh -i 30 -q
#   /path/to/mouse-keepalive/move_mouse.sh -i 60

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

# 优先使用仓库内虚拟环境 / Prefer repo .venv
if [[ -x "$ROOT/.venv/bin/python" ]]; then
  PYTHON="$ROOT/.venv/bin/python"
elif command -v python3 &>/dev/null; then
  PYTHON=python3
elif command -v python &>/dev/null; then
  PYTHON=python
else
  echo "错误: 未找到 Python / Error: Python not found" >&2
  echo "请安装 Python 3.11+ / Please install Python 3.11+" >&2
  exit 1
fi

# src 布局：从 src/ 加载包 / Load package from src layout
export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"

if ! "$PYTHON" -c "import pyautogui" &>/dev/null; then
  echo "错误: 未安装 pyautogui / Error: pyautogui not installed" >&2
  echo "请在本目录执行 / Run in this directory:" >&2
  echo "  pip install -e ." >&2
  exit 1
fi

exec "$PYTHON" -m mouse_keepalive "$@"
