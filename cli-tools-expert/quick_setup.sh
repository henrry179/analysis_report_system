#!/bin/bash

# CLI Tools Expert - 快速设置脚本
# 创建时间: 2025年8月19日

echo "================================================"
echo "   CLI Tools Expert - GitHub 快速设置向导"
echo "================================================"
echo ""
echo "📌 当前项目状态："
echo "   ✅ 项目文件已完整创建 (3,293行代码)"
echo "   ✅ Git本地仓库已初始化"
echo "   ✅ 4次提交记录已完成"
echo "   ✅ 版本: v1.0.0"
echo "   ✅ 更新时间: 2025年8月19日"
echo ""
echo "================================================"
echo ""

# 检查git状态
echo "📊 Git状态检查..."
git status --short
echo ""

# 显示当前remote配置
echo "🔗 当前远程仓库配置:"
git remote -v
echo ""

echo "================================================"
echo "  请按照以下步骤完成GitHub仓库创建和推送："
echo "================================================"
echo ""
echo "📝 步骤 1: 创建GitHub仓库"
echo "----------------------------"
echo "1. 打开浏览器访问: https://github.com/new"
echo ""
echo "2. 填写以下信息:"
echo "   Repository name: cli-tools-expert"
echo "   Description: Terminal Command Line Tools & CLI Tools Expert - 终端命令行工具与CLI工具专家"
echo "   选择: Public (公开)"
echo "   ⚠️ 重要: 不要勾选任何初始化选项(README, .gitignore, license)"
echo ""
echo "3. 点击 'Create repository' 按钮"
echo ""
echo "================================================"
echo ""
echo "📝 步骤 2: 推送代码到GitHub"
echo "----------------------------"
echo "仓库创建成功后，复制并运行以下命令:"
echo ""
echo "# 如果还没有添加远程仓库，运行:"
echo "git remote add origin https://github.com/YOUR_USERNAME/cli-tools-expert.git"
echo ""
echo "# 推送代码:"
echo "git push -u origin main"
echo ""
echo "================================================"
echo ""
echo "🚀 一键推送命令 (创建仓库后使用):"
echo "----------------------------"

# 提供交互式选项
read -p "您是否已在GitHub上创建了仓库? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    read -p "请输入您的GitHub用户名: " username
    
    if [ -z "$username" ]; then
        echo "❌ 用户名不能为空"
        exit 1
    fi
    
    echo ""
    echo "设置远程仓库..."
    
    # 删除现有的origin（如果存在）
    git remote remove origin 2>/dev/null
    
    # 添加新的origin
    git remote add origin https://github.com/${username}/cli-tools-expert.git
    
    echo "远程仓库已设置为: https://github.com/${username}/cli-tools-expert.git"
    echo ""
    echo "正在推送代码..."
    
    # 尝试推送
    if git push -u origin main; then
        echo ""
        echo "================================================"
        echo "🎉 恭喜！代码推送成功！"
        echo "================================================"
        echo ""
        echo "您可以访问以下链接查看您的仓库:"
        echo "https://github.com/${username}/cli-tools-expert"
        echo ""
        echo "项目包含:"
        echo "  • 6个CLI工具的完整教程"
        echo "  • 3,293行代码"
        echo "  • 18个文档和示例文件"
        echo "  • 版本: v1.0.0"
        echo "  • 更新时间: 2025年8月19日"
        echo ""
        echo "下一步建议:"
        echo "  1. 添加GitHub Stars支持项目"
        echo "  2. 创建Issues分享使用体验"
        echo "  3. Fork项目并贡献改进"
        echo ""
    else
        echo ""
        echo "⚠️ 推送失败，可能的原因:"
        echo "  1. 仓库还未创建"
        echo "  2. 需要GitHub认证 (用户名和Personal Access Token)"
        echo "  3. 网络连接问题"
        echo ""
        echo "请检查后重试，或手动运行:"
        echo "git push -u origin main"
    fi
else
    echo ""
    echo "请先在GitHub上创建仓库，然后重新运行此脚本。"
    echo ""
    echo "快速链接: https://github.com/new"
fi

echo ""
echo "================================================"
echo "脚本执行完成 - $(date '+%Y年%m月%d日 %H:%M:%S')"
echo "================================================"