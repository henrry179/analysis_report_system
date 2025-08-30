#!/bin/bash

# GitHub仓库设置脚本
# 使用前请确保已经安装并配置了GitHub CLI (gh)

echo "=========================================="
echo "CLI Tools Expert - GitHub仓库设置脚本"
echo "=========================================="
echo ""

# 检查是否安装了GitHub CLI
if ! command -v gh &> /dev/null; then
    echo "❌ 未检测到GitHub CLI (gh)"
    echo "请先安装GitHub CLI："
    echo "  - macOS: brew install gh"
    echo "  - Linux: https://github.com/cli/cli/blob/trunk/docs/install_linux.md"
    echo "  - Windows: winget install --id GitHub.cli"
    echo ""
    echo "或者手动创建仓库："
    echo "1. 访问 https://github.com/new"
    echo "2. 仓库名称: cli-tools-expert"
    echo "3. 描述: Terminal Command Line Tools & CLI Tools Expert - 终端命令行工具与CLI工具专家"
    echo "4. 设置为公开仓库"
    echo "5. 不要初始化README、.gitignore或LICENSE（我们已经有了）"
    echo ""
    echo "创建后运行以下命令："
    echo "git remote add origin https://github.com/YOUR_USERNAME/cli-tools-expert.git"
    echo "git push -u origin main"
    exit 1
fi

# 检查是否已登录GitHub
echo "检查GitHub登录状态..."
if ! gh auth status &> /dev/null; then
    echo "请先登录GitHub："
    gh auth login
fi

# 获取当前用户名
USERNAME=$(gh api user --jq .login)
echo "当前GitHub用户: $USERNAME"
echo ""

# 询问是否创建仓库
read -p "是否在GitHub上创建新仓库 'cli-tools-expert'? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "创建GitHub仓库..."
    
    # 创建仓库
    gh repo create cli-tools-expert \
        --public \
        --description "Terminal Command Line Tools & CLI Tools Expert - 终端命令行工具与CLI工具专家项目" \
        --source=. \
        --remote=origin \
        --push
    
    if [ $? -eq 0 ]; then
        echo "✅ 仓库创建成功！"
        echo ""
        echo "仓库地址: https://github.com/$USERNAME/cli-tools-expert"
        echo ""
        echo "您可以访问以下链接查看您的仓库："
        echo "https://github.com/$USERNAME/cli-tools-expert"
        echo ""
        echo "后续更新代码使用："
        echo "git add ."
        echo "git commit -m 'your commit message'"
        echo "git push"
    else
        echo "❌ 仓库创建失败"
        echo "可能该仓库已存在，或者您没有创建权限"
        echo ""
        echo "您可以手动添加远程仓库："
        echo "git remote add origin https://github.com/$USERNAME/cli-tools-expert.git"
        echo "git push -u origin main"
    fi
else
    echo "跳过仓库创建"
    echo ""
    echo "如果您已经创建了仓库，请运行："
    echo "git remote add origin https://github.com/$USERNAME/cli-tools-expert.git"
    echo "git push -u origin main"
fi

echo ""
echo "=========================================="
echo "设置完成！"
echo "=========================================="