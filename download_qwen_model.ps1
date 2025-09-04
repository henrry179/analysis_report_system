# Qwen Coder 模型下载 PowerShell 脚本
# 下载通义千问Qwen2.5-Coder模型到本地

param(
    [string]$ModelId = "Qwen/Qwen2.5-Coder-7B-Instruct",
    [string]$SavePath = "D:\Gitstars\models\QwenCoder"
)

Write-Host "🤖 Qwen Coder 模型下载器 (PowerShell版本)" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Yellow
Write-Host ""

# 检查Python环境
Write-Host "🔍 检查Python环境..." -ForegroundColor Cyan
try {
    $pythonVersion = python --version 2>$null
    Write-Host "✅ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python未找到，请先安装Python 3.8+" -ForegroundColor Red
    Write-Host "下载地址: https://python.org" -ForegroundColor Yellow
    exit 1
}

# 检查必要的Python包
Write-Host "📦 检查Python依赖..." -ForegroundColor Cyan
$requiredPackages = @("huggingface_hub", "transformers", "torch", "requests")

foreach ($package in $requiredPackages) {
    try {
        python -c "import $package" 2>$null
        Write-Host "✅ $package" -ForegroundColor Green
    } catch {
        Write-Host "❌ 缺少 $package，正在安装..." -ForegroundColor Yellow
        pip install $package
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ 安装 $package 失败" -ForegroundColor Red
            exit 1
        }
        Write-Host "✅ $package 安装完成" -ForegroundColor Green
    }
}

Write-Host "" -ForegroundColor Yellow
Write-Host "📋 下载配置:" -ForegroundColor Cyan
Write-Host "  🎯 模型: $ModelId" -ForegroundColor White
Write-Host "  📍 保存路径: $SavePath" -ForegroundColor White
Write-Host "  💾 预计大小: ~15GB" -ForegroundColor White
Write-Host "  ⏱️ 预计时间: 30-60分钟" -ForegroundColor White
Write-Host "" -ForegroundColor Yellow

# 确认下载
$confirm = Read-Host "是否开始下载? (y/N)"
if ($confirm -notin @('y', 'Y', 'yes', 'Yes')) {
    Write-Host "❌ 用户取消下载" -ForegroundColor Yellow
    exit 0
}

Write-Host "" -ForegroundColor Yellow
Write-Host "🚀 开始下载模型..." -ForegroundColor Green
Write-Host "📝 下载日志会保存到: qwen_model_download.log" -ForegroundColor Cyan
Write-Host "" -ForegroundColor Yellow

# 使用Python脚本下载
try {
    python download_qwen_model.py
    $exitCode = $LASTEXITCODE

    if ($exitCode -eq 0) {
        Write-Host "" -ForegroundColor Yellow
        Write-Host "🎉 模型下载完成！" -ForegroundColor Green
        Write-Host "" -ForegroundColor Cyan
        Write-Host "📋 使用方法:" -ForegroundColor White
        Write-Host "1. 进入QwenCoder-Project目录" -ForegroundColor White
        Write-Host "   cd D:\Gitstars\QwenCoder-Project" -ForegroundColor White
        Write-Host "2. 运行Qwen Coder" -ForegroundColor White
        Write-Host "   python qwen_coder.py --model `"$SavePath`"" -ForegroundColor White
        Write-Host "3. 或使用启动脚本" -ForegroundColor White
        Write-Host "   .\start_qwen_coder.ps1 -Model `"$SavePath`"" -ForegroundColor White
        Write-Host "" -ForegroundColor Green
        Write-Host "🚀 现在可以开始使用Qwen Coder了！" -ForegroundColor Green
    } else {
        Write-Host "❌ 下载失败，请检查日志文件: qwen_model_download.log" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ 下载过程中出现错误: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host "" -ForegroundColor Yellow
Write-Host "📝 日志文件位置: $(Get-Location)\qwen_model_download.log" -ForegroundColor Cyan
Write-Host "📁 模型文件位置: $SavePath" -ForegroundColor Cyan
