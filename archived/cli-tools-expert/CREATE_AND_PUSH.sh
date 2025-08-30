#!/bin/bash

# CLI Tools Expert - 一键创建和推送脚本
# 这个脚本会在本地重新创建整个项目并推送到GitHub
# 创建时间: 2025年8月19日

echo "================================================"
echo "   CLI Tools Expert - 一键部署脚本"
echo "================================================"

# 创建项目目录
mkdir -p cli-tools-expert/{docs,examples/{chatgpt-examples,claude-examples,gemini-examples,cursor-examples,qwen-examples,amazon-examples},tools}
cd cli-tools-expert

# 初始化Git
git init
git branch -M main

# 创建README.md
cat > README.md << 'EOF'
# CLI Tools Expert - 终端命令行工具与CLI工具专家

## 📚 项目简介

这是一个专门用于学习和掌握多种终端命令行工具和CLI工具的项目仓库。本项目以TODOS清单的方式系统地整理了各种现代AI辅助编程CLI工具的使用教程、示例代码和相关资源。

**版本信息**: v1.0.0  
**创建日期**: 2025年8月19日  
**当前版本更新**: 2025年8月19日 01:59 UTC

## 🎯 项目目标

帮助开发者快速上手并掌握以下终端命令行工具和CLI工具：

1. **ChatGPT Code** - OpenAI的代码生成CLI工具
2. **Claude Code** - Anthropic的Claude AI编程助手
3. **Gemini CLI** - Google的Gemini AI命令行接口
4. **Cursor CLI** - Cursor编辑器的命令行工具
5. **Qwen Code** - 阿里云通义千问的代码生成工具
6. **Amazon Q Code** - Amazon的AI编程助手工具

## 📖 文档结构

- `docs/` - 每个工具的详细使用教程
- `examples/` - 实用的示例代码
- `tools/` - 辅助工具和脚本

## 🚀 快速开始

查看各工具的详细文档：
- [ChatGPT Code 教程](docs/chatgpt-code.md)
- [Claude Code 教程](docs/claude-code.md)
- [Gemini CLI 教程](docs/gemini-cli.md)
- [Cursor CLI 教程](docs/cursor-cli.md)
- [Qwen Code 教程](docs/qwen-code.md)
- [Amazon Q Code 教程](docs/amazon-q-code.md)

最后更新：2025年8月19日
EOF

# 创建VERSION文件
echo "1.0.0" > VERSION

# 创建LICENSE
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2025 CLI Tools Expert

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

# 创建.gitignore
cat > .gitignore << 'EOF'
*.pyc
__pycache__/
.env
.vscode/
.idea/
*.log
node_modules/
.DS_Store
EOF

# 创建示例文档
echo "# ChatGPT Code 使用教程" > docs/chatgpt-code.md
echo "# Claude Code 使用教程" > docs/claude-code.md
echo "# Gemini CLI 使用教程" > docs/gemini-cli.md
echo "# Cursor CLI 使用教程" > docs/cursor-cli.md
echo "# Qwen Code 使用教程" > docs/qwen-code.md
echo "# Amazon Q Code 使用教程" > docs/amazon-q-code.md

# Git提交
git add .
git commit -m "Initial commit: CLI Tools Expert project - 2025年8月19日"

# 添加远程仓库并推送
git remote add origin https://github.com/henrry179/cli-tools-expert.git
git push -u origin main

echo ""
echo "================================================"
echo "✅ 完成！项目已推送到GitHub"
echo "================================================"
echo "访问: https://github.com/henrry179/cli-tools-expert"
EOF