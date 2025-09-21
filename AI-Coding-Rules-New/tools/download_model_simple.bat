@echo off
REM Qwen Coder 简单下载脚本
echo 🚀 Qwen Coder 模型下载器
echo ====================================
echo.

echo 📦 安装依赖...
python -m pip install huggingface_hub transformers torch accelerate --quiet
if %errorlevel% neq 0 (
    echo ❌ 依赖安装失败
    pause
    exit /b 1
)
echo ✅ 依赖安装完成
echo.

echo 🎯 开始下载 Qwen/Qwen2.5-Coder-7B-Instruct
echo 📍 保存到: D:\Gitstars\models\QwenCoder
echo ⚠️  这将下载约15GB的文件
echo 💡 提示: 下载需要30-60分钟，请耐心等待
echo.

python -c "
import time
from huggingface_hub import snapshot_download

print('🚀 开始下载...')
start_time = time.time()

try:
    path = snapshot_download(
        repo_id='Qwen/Qwen2.5-Coder-7B-Instruct',
        local_dir=r'D:\Gitstars\models\QwenCoder',
        local_dir_use_symlinks=False,
        resume_download=True,
        max_workers=4
    )
    
    elapsed = time.time() - start_time
    print(f'\n✅ 下载完成! 耗时: {elapsed:.1f}秒')
    print(f'📁 保存位置: {path}')
    
except Exception as e:
    print(f'❌ 下载失败: {e}')
    import sys
    sys.exit(1)
"

if %errorlevel% equ 0 (
    echo.
    echo 🎉 Qwen Coder 模型下载成功！
    echo.
    echo 📋 下一步:
    echo 1. 进入 QwenCoder-Project 目录
    echo 2. 运行: python qwen_coder.py --model "D:\Gitstars\models\QwenCoder"
    echo 3. 开始使用AI编程助手！
) else (
    echo.
    echo ❌ 下载失败，请检查网络连接和磁盘空间
)

echo.
pause
