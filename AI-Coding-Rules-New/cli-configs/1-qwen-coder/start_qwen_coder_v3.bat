@echo off
REM Qwen3 Coder Windows 快速启动脚本
REM 用于一键启动Qwen3 Coder Web界面

echo 🚀 Qwen3 Coder Windows 快速启动器
echo ===================================
echo.

echo 🔍 检查Python环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python未找到，请先安装Python 3.8+
    echo 下载地址: https://python.org
    pause
    exit /b 1
)
echo ✓ Python环境正常
echo.

echo 📦 检查依赖包...
python -c "import torch" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 缺少必要的依赖包
    echo 请运行: pip install -r requirements_v3.txt
    echo.
    set /p choice="是否现在安装依赖? (y/n): "
    if /i "%choice%"=="y" (
        echo 📥 正在安装依赖...
        pip install -r requirements_v3.txt
        if %errorlevel% neq 0 (
            echo ❌ 依赖安装失败
            pause
            exit /b 1
        )
        echo ✅ 依赖安装完成
    ) else (
        echo 取消安装，退出程序
        pause
        exit /b 1
    )
) else (
    echo ✓ 依赖包正常
)
echo.

echo 🎯 启动Qwen3 Coder Web界面...
echo 浏览器将自动打开: http://localhost:7860
echo 按 Ctrl+C 停止服务
echo.

python qwen_coder_v3.py --mode web --port 7860 --model Qwen/Qwen3-Coder-30B-A3B-Instruct

echo.
echo 👋 Qwen3 Coder已停止运行
pause