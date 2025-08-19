# ChatGPT Code 使用教程

## 📋 工具概述

ChatGPT Code 是 OpenAI 提供的命令行代码生成工具，可以通过自然语言描述来生成、优化和解释代码。

## 🔧 安装指南

### 系统要求
- Python 3.8+
- OpenAI API Key
- 稳定的网络连接

### 安装步骤

```bash
# 使用 pip 安装
pip install openai-cli

# 或使用 pipx（推荐）
pipx install openai-cli

# 配置 API Key
export OPENAI_API_KEY="your-api-key-here"

# 或将其添加到配置文件
echo 'export OPENAI_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

## 📖 基础使用

### 查看帮助信息
```bash
chatgpt-code --help
```

### 基本命令结构
```bash
chatgpt-code [command] [options]
```

## 💡 核心功能

### 1. 代码生成

#### 基础示例
```bash
# 生成 Python 函数
chatgpt-code generate --prompt "Write a Python function to calculate fibonacci sequence"

# 生成特定语言的代码
chatgpt-code generate --prompt "Create a REST API endpoint" --language javascript

# 生成并保存到文件
chatgpt-code generate --prompt "Binary search algorithm" --output binary_search.py
```

#### 高级示例
```bash
# 生成完整的类
chatgpt-code generate --prompt "Create a User class with authentication methods" \
  --language python \
  --style object-oriented

# 生成单元测试
chatgpt-code generate --prompt "Write unit tests for the fibonacci function" \
  --framework pytest

# 生成文档字符串
chatgpt-code generate --prompt "Add comprehensive docstrings" \
  --input existing_code.py
```

### 2. 代码优化

```bash
# 优化现有代码
chatgpt-code optimize --file slow_algorithm.py

# 重构代码
chatgpt-code refactor --file legacy_code.js --target es6

# 性能优化
chatgpt-code optimize --file data_processor.py --focus performance
```

### 3. 代码解释

```bash
# 解释代码功能
chatgpt-code explain --file complex_algorithm.py

# 逐行解释
chatgpt-code explain --file script.sh --verbose

# 生成代码注释
chatgpt-code comment --file uncommented_code.java
```

### 4. 代码转换

```bash
# 语言转换
chatgpt-code convert --file script.py --to javascript

# 框架迁移
chatgpt-code migrate --file flask_app.py --to fastapi

# 版本升级
chatgpt-code upgrade --file old_python2.py --to python3
```

### 5. 调试辅助

```bash
# 查找 bug
chatgpt-code debug --file buggy_code.py --error "IndexError"

# 生成调试语句
chatgpt-code debug --file app.js --add-logging

# 错误修复建议
chatgpt-code fix --file broken.py --error-message "TypeError: unsupported operand"
```

## 🎯 实际应用案例

### 案例 1：创建 Web API

```bash
# 生成 FastAPI 应用
chatgpt-code generate --prompt "
Create a FastAPI application with:
- User authentication
- CRUD operations for products
- PostgreSQL database integration
- JWT token support
" --language python --output app.py
```

### 案例 2：数据处理脚本

```bash
# 生成数据分析脚本
chatgpt-code generate --prompt "
Create a Python script that:
- Reads CSV files
- Cleans missing data
- Performs statistical analysis
- Generates visualization plots
- Exports results to Excel
" --output data_analyzer.py
```

### 案例 3：自动化脚本

```bash
# 生成自动化部署脚本
chatgpt-code generate --prompt "
Create a bash script for:
- Git repository setup
- Docker container deployment
- Environment variable configuration
- Health check monitoring
" --language bash --output deploy.sh
```

## ⚙️ 配置文件

创建 `~/.chatgpt-code/config.yaml`：

```yaml
# ChatGPT Code 配置
api:
  key: ${OPENAI_API_KEY}
  model: gpt-4
  temperature: 0.7
  max_tokens: 2000

defaults:
  language: python
  output_format: file
  verbose: true

aliases:
  py: python
  js: javascript
  ts: typescript
```

## 🔍 高级技巧

### 1. 使用模板

```bash
# 创建项目模板
chatgpt-code template create --name fastapi-starter

# 使用模板生成项目
chatgpt-code generate --template fastapi-starter --project-name my-api
```

### 2. 批处理

```bash
# 批量优化文件
find . -name "*.py" -exec chatgpt-code optimize --file {} \;

# 批量添加类型注解
chatgpt-code annotate --directory ./src --recursive
```

### 3. 集成到 CI/CD

```yaml
# GitHub Actions 示例
name: Code Review
on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: AI Code Review
        run: |
          pip install openai-cli
          chatgpt-code review --pr ${{ github.event.pull_request.number }}
```

## 📊 性能优化建议

1. **缓存响应**：使用 `--cache` 选项避免重复请求
2. **批量处理**：合并多个小请求为一个大请求
3. **异步执行**：使用 `--async` 进行并行处理
4. **本地模型**：考虑使用本地模型减少延迟

## 🚨 常见问题

### Q1: API Key 无效
```bash
# 验证 API Key
chatgpt-code validate-key

# 重新设置
chatgpt-code config set api.key "new-key-here"
```

### Q2: 超时错误
```bash
# 增加超时时间
chatgpt-code generate --timeout 60 --prompt "complex request"
```

### Q3: 输出格式问题
```bash
# 指定输出格式
chatgpt-code generate --format markdown --prompt "documentation"
```

## 📚 相关资源

- **官方文档**: [OpenAI CLI Documentation](https://platform.openai.com/docs/guides/command-line)
- **API 参考**: [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- **社区论坛**: [OpenAI Community](https://community.openai.com/)
- **GitHub 仓库**: [openai-cli](https://github.com/openai/openai-cli)
- **最佳实践**: [OpenAI Cookbook](https://github.com/openai/openai-cookbook)

## 🎓 学习资源

- [OpenAI 官方教程](https://platform.openai.com/docs/tutorials)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [AI 编程实战课程](https://www.coursera.org/learn/ai-programming)

## 💰 费用说明

- **GPT-3.5**: $0.002 / 1K tokens
- **GPT-4**: $0.03 / 1K tokens (输入), $0.06 / 1K tokens (输出)
- **月度限额**: 可在账户设置中配置

## 🔐 安全建议

1. **不要硬编码 API Key**
2. **使用环境变量或密钥管理服务**
3. **定期轮换 API Key**
4. **审查生成的代码安全性**
5. **不要分享包含敏感信息的提示**

---

最后更新：2025年1月
返回 [主页](../README.md)