# CLI Tools Expert 项目信息

## 项目概述

本项目是一个综合性的CLI工具学习和参考资源库，专门为开发者提供现代AI辅助编程命令行工具的详细教程和使用指南。

## 项目结构

```
cli-tools-expert/
├── README.md                 # 项目主文档
├── LICENSE                   # MIT许可证
├── CONTRIBUTING.md           # 贡献指南
├── PROJECT_INFO.md          # 项目详细信息（本文件）
├── setup_github.sh          # GitHub仓库设置脚本
├── .gitignore               # Git忽略文件配置
│
├── docs/                    # 详细文档目录
│   ├── chatgpt-code.md     # ChatGPT Code 完整教程
│   ├── claude-code.md      # Claude Code 完整教程
│   ├── gemini-cli.md       # Gemini CLI 完整教程
│   ├── cursor-cli.md       # Cursor CLI 完整教程
│   ├── qwen-code.md        # Qwen Code 完整教程
│   └── amazon-q-code.md    # Amazon Q Code 完整教程
│
├── examples/                # 示例代码目录
│   ├── chatgpt-examples/   # ChatGPT Code 示例
│   ├── claude-examples/    # Claude Code 示例
│   ├── gemini-examples/    # Gemini CLI 示例
│   ├── cursor-examples/    # Cursor CLI 示例
│   ├── qwen-examples/      # Qwen Code 示例
│   └── amazon-examples/    # Amazon Q Code 示例
│
└── tools/                   # 工具脚本目录（待扩展）
    └── setup-scripts/       # 安装配置脚本
```

## 包含的CLI工具

1. **ChatGPT Code** - OpenAI的代码生成工具
2. **Claude Code** - Anthropic的AI编程助手
3. **Gemini CLI** - Google的多模态AI工具
4. **Cursor CLI** - Cursor编辑器命令行接口
5. **Qwen Code** - 阿里云通义千问代码工具
6. **Amazon Q Code** - Amazon的企业级AI编程助手

## 如何使用本项目

### 1. 克隆仓库
```bash
git clone https://github.com/yourusername/cli-tools-expert.git
cd cli-tools-expert
```

### 2. 查看文档
每个工具都有详细的文档，位于 `docs/` 目录下。建议按以下顺序学习：
- 初学者：从 Cursor CLI 开始
- 中级用户：探索 ChatGPT Code 和 Claude Code
- 高级用户：深入 Gemini CLI 和 Amazon Q Code
- 中文用户：重点关注 Qwen Code

### 3. 运行示例
`examples/` 目录包含各种实用示例代码，可以直接运行或修改使用。

### 4. 贡献代码
欢迎提交PR来改进文档、添加新示例或修复错误。请参考 `CONTRIBUTING.md`。

## 推送到GitHub

### 方法1：使用提供的脚本（推荐）
```bash
./setup_github.sh
```

### 方法2：手动创建和推送
1. 在GitHub上创建新仓库（不要初始化任何文件）
2. 添加远程仓库：
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/cli-tools-expert.git
   ```
3. 推送代码：
   ```bash
   git push -u origin main
   ```

### 方法3：使用GitHub CLI
```bash
# 安装GitHub CLI（如果还没有）
# macOS: brew install gh
# Linux: 查看 https://github.com/cli/cli/blob/trunk/docs/install_linux.md

# 登录GitHub
gh auth login

# 创建并推送仓库
gh repo create cli-tools-expert --public --source=. --push
```

## 更新时间

- 项目创建：2025年1月
- 最后更新：2025年1月

## 注意事项

1. **API密钥安全**：不要将API密钥提交到Git仓库
2. **及时更新**：AI工具发展迅速，请定期更新文档
3. **实践为主**：建议边学习边实践，获得最佳学习效果
4. **社区参与**：欢迎在GitHub Issues中提问和讨论

## 联系方式

- GitHub Issues：提交问题和建议
- GitHub Discussions：技术讨论和经验分享
- Pull Requests：贡献代码和文档

## 致谢

感谢所有AI工具的开发团队，以及为本项目贡献的开发者们！

---

**记住**：本项目的目标是帮助开发者快速掌握现代AI辅助编程工具，提高开发效率。持续学习，不断进步！🚀