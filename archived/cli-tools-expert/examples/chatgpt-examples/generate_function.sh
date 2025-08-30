#!/bin/bash
# ChatGPT Code 示例：生成函数

# 生成斐波那契数列函数
chatgpt-code generate --prompt "Write a Python function to calculate fibonacci sequence up to n terms" \
  --language python \
  --output fibonacci.py

# 生成带缓存的递归函数
chatgpt-code generate --prompt "Create a memoized recursive function for calculating factorials" \
  --language python \
  --style functional

# 生成异步函数
chatgpt-code generate --prompt "Write an async function to fetch data from multiple APIs concurrently" \
  --language javascript \
  --framework node

echo "函数生成完成！"