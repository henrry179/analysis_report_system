# Qwen3 Coder Windows 启动脚本
# 用于快速启动Qwen3 Coder环境

param(
    [string]$Mode = "web",
    [int]$Port = 7860,
    [string]$Model = "Qwen/Qwen3-Coder-30B-A3B-Instruct"
)

Write-Host "🚀 Qwen3 Coder Windows 启动器" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Yellow
Write-Host ""

# 检查Python环境
Write-Host "🔍 检查Python环境..." -ForegroundColor Cyan
try {
    $pythonVersion = python --version 2>$null
    Write-Host "✓ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python未找到，请先安装Python 3.8+" -ForegroundColor Red
    Write-Host "下载地址: https://python.org" -ForegroundColor Yellow
    exit 1
}

# 检查必要的包
Write-Host "📦 检查依赖包..." -ForegroundColor Cyan
$requiredPackages = @("torch", "transformers", "gradio", "accelerate")
$missingPackages = @()

foreach ($package in $requiredPackages) {
    try {
        python -c "import $package" 2>$null
        Write-Host "✓ $package" -ForegroundColor Green
    } catch {
        $missingPackages += $package
        Write-Host "✗ $package" -ForegroundColor Red
    }
}

if ($missingPackages.Count -gt 0) {
    Write-Host "" -ForegroundColor Yellow
    Write-Host "❌ 缺少必要的包: $($missingPackages -join ', ')" -ForegroundColor Red
    Write-Host "请运行以下命令安装:" -ForegroundColor Yellow
    Write-Host "pip install -r requirements_v3.txt" -ForegroundColor Cyan
    Write-Host ""
    $installNow = Read-Host "是否现在安装依赖? (y/n)"
    if ($installNow -eq "y" -or $installNow -eq "Y") {
        Write-Host "📥 正在安装依赖..." -ForegroundColor Cyan
        pip install -r requirements_v3.txt
        Write-Host "✅ 依赖安装完成" -ForegroundColor Green
    } else {
        exit 1
    }
}

Write-Host "" -ForegroundColor Yellow
Write-Host "🎯 启动配置:" -ForegroundColor Cyan
Write-Host "  模式: $Mode" -ForegroundColor White
Write-Host "  端口: $Port" -ForegroundColor White
Write-Host "  模型: $Model" -ForegroundColor White
Write-Host "" -ForegroundColor Yellow

# 根据模式启动
switch ($Mode) {
    "web" {
        Write-Host "🌐 启动Web界面模式..." -ForegroundColor Green
        Write-Host "浏览器将自动打开: http://localhost:$Port" -ForegroundColor Cyan
        Write-Host "" -ForegroundColor Yellow

        python qwen_coder_v3.py --mode web --port $Port --model $Model
    }

    "streamlit" {
        Write-Host "📱 创建Streamlit应用..." -ForegroundColor Green
        python qwen_coder_v3.py --mode streamlit

        Write-Host "" -ForegroundColor Yellow
        Write-Host "🚀 启动Streamlit应用:" -ForegroundColor Cyan
        Write-Host "streamlit run qwen_coder_app_v3.py" -ForegroundColor White
        Write-Host "" -ForegroundColor Yellow

        streamlit run qwen_coder_app_v3.py
    }

    "cli" {
        Write-Host "💬 启动命令行交互模式..." -ForegroundColor Green
        Write-Host "输入 'help' 查看帮助，输入 'exit' 退出" -ForegroundColor Cyan
        Write-Host "" -ForegroundColor Yellow

        python qwen_coder_v3.py --mode cli
    }

    default {
        Write-Host "❌ 无效的模式: $Mode" -ForegroundColor Red
        Write-Host "可用模式: web, streamlit, cli" -ForegroundColor Yellow
        exit 1
    }
}

Write-Host "" -ForegroundColor Yellow
Write-Host "👋 Qwen3 Coder 已停止运行" -ForegroundColor Cyan