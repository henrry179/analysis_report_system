#!/bin/bash

# 分析报告系统启动脚本
echo "🚀 启动业务分析报告系统 v4.0 Optimized"
echo "=============================================="

# 检查虚拟环境
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  建议激活虚拟环境："
    echo "   source .venv/bin/activate"
    echo ""
fi

# 检查依赖
echo "📦 检查Python依赖..."
python -c "import fastapi, uvicorn, pydantic" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ 缺少必要依赖，正在安装..."
    pip install -r requirements.txt
fi

# 检查端口占用
echo "🔍 检查端口状态..."
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  端口8000被占用，系统将自动切换到其他端口"
fi

# 启动系统
echo "🌟 启动系统..."
echo "=============================================="
cd "$(dirname "$0")/.." && python scripts/start_server.py

echo ""
echo "👋 系统已关闭" 