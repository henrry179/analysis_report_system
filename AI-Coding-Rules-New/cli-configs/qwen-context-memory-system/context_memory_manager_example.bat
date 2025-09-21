@echo off
chcp 65001 >nul
REM Qwen Coder Context Memory Manager 使用示例脚本
REM 演示如何在实际场景中使用上下文记忆系统

echo ================================
echo Qwen Coder Context Memory Manager 使用示例
echo ================================

REM 1. 创建新会话
echo.
echo 1. 创建新会话...
call context_memory_manager.bat --create-session --description "今日编程任务"

REM 获取会话ID (实际使用中需要从输出中提取)
REM 为演示目的，我们使用一个固定ID
set SESSION_ID=20250903_230000

REM 2. 添加上下文到会话
echo.
echo 2. 添加上下文到会话...
call context_memory_manager.bat --add-context --session-id %SESSION_ID% --prompt "帮我写一个Python函数来计算斐波那契数列" --response "好的，这是一个计算斐波那契数列的Python函数: def fibonacci(n): if n ^^^<= 1: return n else: return fibonacci(n-1) + fibonacci(n-2)"

echo.
call context_memory_manager.bat --add-context --session-id %SESSION_ID% --prompt "优化一下这个函数，使用记忆化技术" --response "好的，这是优化后的版本: def fibonacci(n, memo={}): if n in memo: return memo[n] if n ^^^<= 1: return n memo[n] = fibonacci(n-1, memo) + fibonacci(n-2, memo) return memo[n]"

REM 3. 查看会话上下文
echo.
echo 3. 查看会话上下文...
call context_memory_manager.bat --view-context --session-id %SESSION_ID%

REM 4. 生成会话摘要
echo.
echo 4. 生成会话摘要...
call context_memory_manager.bat --generate-summary --session-id %SESSION_ID%

REM 5. 查看今日会话
echo.
echo 5. 查看今日会话...
call context_memory_manager.bat --today

REM 6. 查看内存摘要
echo.
echo 6. 查看内存摘要...
call context_memory_manager.bat --summary

echo.
echo ================================
echo 完成示例演示
echo ================================
echo.
echo 您可以执行以下操作来进一步使用该工具:
echo.
echo 查看所有会话:
echo   context_memory_manager.bat --list-sessions
echo.
echo 清理旧会话:
echo   context_memory_manager.bat --cleanup --days-to-keep 7
echo.
pause