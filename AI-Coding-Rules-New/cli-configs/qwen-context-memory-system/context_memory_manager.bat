@echo off
chcp 65001 >nul
REM Qwen Coder Context Memory Manager 启动脚本
REM 用于简化 context_memory_manager.py 脚本的执行

REM 检查Python是否可用
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Python解释器
    echo 请确保已安装Python 3.6或更高版本，并已将其添加到系统PATH中
    pause
    exit /b 1
)

REM 获取脚本所在目录
set SCRIPT_DIR=%~dp0

REM 执行Python脚本
python "%SCRIPT_DIR%context_memory_manager.py" %*

REM 检查执行结果
if %errorlevel% neq 0 (
    echo.
    echo 脚本执行出错，请检查参数是否正确
    pause
)