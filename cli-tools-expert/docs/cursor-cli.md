# Cursor CLI 使用教程

## 📋 工具概述

Cursor CLI 是 Cursor 编辑器的命令行接口工具，提供了强大的AI辅助编程功能，支持代码生成、重构、调试等操作，可以无缝集成到开发工作流中。

## 🔧 安装指南

### 系统要求
- macOS, Windows, 或 Linux
- Node.js 16.0+
- Cursor 编辑器（可选）
- 4GB+ RAM

### 安装步骤

```bash
# 使用 npm 安装
npm install -g cursor-cli

# 或使用 yarn
yarn global add cursor-cli

# 或使用 Cursor 编辑器内置安装
cursor --install-cli

# 配置 API Key
cursor-cli config set api_key "your-api-key-here"

# 验证安装
cursor-cli --version
cursor-cli status
```

## 📖 基础使用

### 查看帮助信息
```bash
cursor-cli --help
cursor-cli [command] --help
cursor-cli tips  # 显示使用技巧
```

### 基本命令结构
```bash
cursor-cli [command] [options] [files...]
```

## 💡 核心功能

### 1. 智能代码编辑

#### 代码生成
```bash
# 在文件中生成代码
cursor-cli edit --file main.py --instruction "Add error handling"

# 创建新文件
cursor-cli create --file utils.js --description "Utility functions for date manipulation"

# 批量编辑
cursor-cli edit --glob "*.py" --instruction "Add type hints"
```

#### 代码补全
```bash
# 补全函数实现
cursor-cli complete --file incomplete.py --line 42

# 智能导入
cursor-cli imports --file app.js --auto-fix

# 补全文档字符串
cursor-cli document --file api.py --style google
```

### 2. 代码重构

```bash
# 重命名变量
cursor-cli refactor --file code.js --rename "oldName:newName"

# 提取函数
cursor-cli refactor --file long_function.py --extract-function --lines 10-30

# 简化代码
cursor-cli simplify --file complex.ts

# 应用设计模式
cursor-cli refactor --file service.java --pattern factory
```

### 3. AI对话编程

```bash
# 启动交互式会话
cursor-cli chat

# 单次问答
cursor-cli ask "How to implement binary search in Python?"

# 上下文感知对话
cursor-cli chat --context ./src --question "What does this function do?"

# 代码解释
cursor-cli explain --file algorithm.cpp --verbose
```

### 4. 项目级操作

```bash
# 项目分析
cursor-cli analyze --project .

# 生成项目文档
cursor-cli docs --project . --output docs/

# 代码审查
cursor-cli review --branch feature/new-feature

# 依赖更新建议
cursor-cli dependencies --check --update-suggestions
```

### 5. 调试辅助

```bash
# 添加调试语句
cursor-cli debug --file app.py --add-logging

# 生成测试用例
cursor-cli test --file calculator.py --coverage 90

# 错误修复
cursor-cli fix --file broken.js --error "undefined is not a function"

# 性能分析
cursor-cli profile --file slow.py --suggest-optimizations
```

## 🎯 实际应用案例

### 案例 1：快速原型开发

```bash
# 从描述生成完整应用
cursor-cli prototype --description "
TODO app with:
- Add/remove tasks
- Mark as complete
- Filter by status
- Local storage
" --tech "react,typescript" --output todo-app/
```

### 案例 2：代码现代化

```bash
# 升级旧代码
cursor-cli modernize --project legacy-app/ \
  --from "jquery" \
  --to "react" \
  --output modern-app/
```

### 案例 3：自动化重构

```bash
# 批量重构脚本
cat refactor-tasks.txt | cursor-cli batch-refactor --project .

# 代码风格统一
cursor-cli format --project . --style airbnb --fix
```

### 案例 4：智能代码审查

```bash
# PR 审查
cursor-cli review --pr 123 \
  --checks "security,performance,best-practices" \
  --comment  # 自动添加审查评论
```

## ⚙️ 配置文件

创建 `.cursorrc`：

```json
{
  "api": {
    "key": "${CURSOR_API_KEY}",
    "endpoint": "https://api.cursor.sh",
    "timeout": 30000
  },
  "editor": {
    "tabSize": 2,
    "useTabs": false,
    "lineNumbers": true,
    "wordWrap": "on"
  },
  "ai": {
    "model": "gpt-4",
    "temperature": 0.7,
    "maxTokens": 2000,
    "contextWindow": 8000
  },
  "features": {
    "autoComplete": true,
    "autoImports": true,
    "inlineChat": true,
    "codeActions": true
  },
  "shortcuts": {
    "generate": "ctrl+g",
    "chat": "ctrl+k",
    "fix": "ctrl+shift+f"
  }
}
```

## 🔍 高级功能

### 1. 自定义命令

```bash
# 创建自定义命令
cursor-cli command create --name "clean-imports" \
  --script "remove-unused-imports.js"

# 运行自定义命令
cursor-cli run clean-imports --file app.py
```

### 2. 工作流自动化

```bash
# 创建工作流
cursor-cli workflow create --name "pre-commit" \
  --steps "format,lint,test"

# 执行工作流
cursor-cli workflow run pre-commit
```

### 3. 团队协作

```bash
# 共享配置
cursor-cli share-config --team dev-team

# 同步团队设置
cursor-cli sync --team dev-team

# 代码规范检查
cursor-cli standards --check --team-rules
```

### 4. 集成开发环境

```bash
# VS Code 集成
cursor-cli integrate vscode

# Vim 集成
cursor-cli integrate vim --config ~/.vimrc

# Emacs 集成
cursor-cli integrate emacs
```

## 📊 性能优化

### 缓存管理
```bash
# 清理缓存
cursor-cli cache clear

# 预热缓存
cursor-cli cache warm --project .

# 查看缓存状态
cursor-cli cache status
```

### 并行处理
```bash
# 并行编辑多个文件
cursor-cli edit --parallel 4 --glob "*.js" --instruction "Add JSDoc"
```

## 🚨 常见问题

### Q1: 连接问题
```bash
# 测试连接
cursor-cli test-connection

# 使用代理
cursor-cli config set proxy "http://proxy:8080"
```

### Q2: 性能问题
```bash
# 限制并发
cursor-cli config set max_concurrent 2

# 增加超时
cursor-cli config set timeout 60000
```

### Q3: 上下文丢失
```bash
# 重建索引
cursor-cli index --rebuild

# 手动设置上下文
cursor-cli context --add ./src --add ./tests
```

## 📚 相关资源

- **官方网站**: [Cursor.sh](https://cursor.sh/)
- **文档中心**: [Cursor Docs](https://docs.cursor.sh/)
- **GitHub**: [cursor/cursor](https://github.com/getcursor/cursor)
- **社区论坛**: [Cursor Community](https://community.cursor.sh/)
- **视频教程**: [Cursor YouTube](https://youtube.com/@cursor)

## 🎓 学习资源

- [Cursor 快速入门指南](https://docs.cursor.sh/getting-started)
- [AI 编程最佳实践](https://docs.cursor.sh/best-practices)
- [Cursor 插件开发](https://docs.cursor.sh/plugin-development)

## 💰 费用说明

- **免费版**: 基础功能，每月100次请求
- **Pro版**: $20/月，无限请求，高级功能
- **Team版**: $40/用户/月，团队协作功能
- **企业版**: 自定义定价，私有部署

## 🔐 安全特性

1. **本地处理**: 代码可选择本地处理
2. **端到端加密**: 传输数据加密
3. **隐私模式**: 不存储用户代码
4. **SOC 2合规**: 企业级安全标准
5. **自托管选项**: 支持私有部署

## 🤝 快捷键参考

| 操作 | 快捷键 | 描述 |
|------|--------|------|
| 生成代码 | `Ctrl+G` | 在光标位置生成代码 |
| 开启对话 | `Ctrl+K` | 打开AI对话窗口 |
| 快速修复 | `Ctrl+.` | 显示快速修复选项 |
| 重构 | `Ctrl+Shift+R` | 重构菜单 |
| 解释代码 | `Ctrl+E` | 解释选中代码 |

## 🔧 故障排除

```bash
# 诊断工具
cursor-cli doctor

# 查看日志
cursor-cli logs --tail 100

# 重置配置
cursor-cli reset --confirm

# 更新到最新版本
cursor-cli update
```

---

最后更新：2025年1月
返回 [主页](../README.md)