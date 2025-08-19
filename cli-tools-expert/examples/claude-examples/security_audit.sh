#!/bin/bash
# Claude Code 示例：安全审计

# 扫描Python项目的安全漏洞
claude-code analyze --file app.py --focus security

# SQL注入检测
claude-code security --file database.py --check sql-injection

# XSS漏洞检测
claude-code security --file frontend.js --check xss

# 完整的安全审计报告
claude-code audit --project . \
  --checks "security,vulnerabilities,dependencies" \
  --output security-report.html

echo "安全审计完成！请查看生成的报告。"