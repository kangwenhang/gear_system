#!/bin/bash
set -e

echo "===================================="
echo "  Gear System - 打包脚本"
echo "===================================="
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/backend"
FRONTEND_DIR="$SCRIPT_DIR/frontend"

echo "[1/4] 检查 Python 环境..."
python3 --version
if [ $? -ne 0 ]; then
    echo "错误: 未找到 Python3，请先安装 Python 3.9+"
    exit 1
fi

echo ""
echo "[2/4] 安装依赖..."
cd "$BACKEND_DIR"
pip3 install -r requirements.txt
pip3 install pywebview pyinstaller

echo ""
echo "[3/4] 构建前端..."
cd "$FRONTEND_DIR"
if [ ! -d "node_modules" ]; then
    echo "安装前端依赖..."
    npm install
fi
npm run build

echo "复制前端构建产物到后端目录..."
rm -rf "$BACKEND_DIR/frontend_dist"
cp -r "$FRONTEND_DIR/dist" "$BACKEND_DIR/frontend_dist"

echo ""
echo "[4/4] 打包..."
cd "$BACKEND_DIR"
pyinstaller --clean GearSystem.spec

echo ""
echo "===================================="
echo "  打包完成!"
echo "  输出目录: backend/dist/"
echo "===================================="
