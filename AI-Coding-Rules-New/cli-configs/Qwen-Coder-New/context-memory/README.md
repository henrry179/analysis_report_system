# Qwen Coder 上下文记忆系统 (Context Memory System)

## 📌 概述

本目录用于存储 Qwen Coder 的上下文记忆信息，以便在不同项目和会话之间共享和复用上下文。

## 📁 目录结构

```
context-memory/
├── sessions/                   # 会话历史记录
│   ├── session_20231027_143045/  # 示例会话目录
│   │   ├── context.json          # 会话上下文数据
│   │   ├── conversation_history.txt # 对话历史记录
│   │   └── project_files/        # 会话中涉及的项目文件快照
│   └── ...                       # 其他会话目录
├── project_knowledge/          # 项目知识库
│   ├── my-web-app/             # 示例项目知识库
│   │   ├── tech_stack.json       # 技术栈信息
│   │   ├── code_patterns.json    # 代码模式和最佳实践
│   │   ├── api_endpoints.json    # API 端点信息
│   │   └── documentation/        # 项目相关文档摘要
│   └── ...                       # 其他项目知识库
├── user_preferences/           # 用户偏好设置
│   ├── coding_style.json         # 编码风格偏好
│   ├── framework_choices.json    # 框架选择偏好
│   └── tool_configurations.json  # 工具配置偏好
├── global_cache/               # 全局缓存
│   ├── code_snippets/            # 代码片段缓存
│   ├── documentation_cache/      # 文档缓存
│   └── research_findings/        # 研究发现缓存
└── memory_config.json          # 记忆系统配置文件
```

## 🧠 核心功能

### 1. 会话管理 (Sessions)
- 自动保存每个开发会话的上下文
- 记录对话历史以便回顾
- 快照项目文件状态用于参考

### 2. 项目知识库 (Project Knowledge)
- 为每个项目维护一个知识库
- 存储技术栈、代码模式、API信息
- 便于新成员快速了解项目或跨项目复用知识

### 3. 用户偏好 (User Preferences)
- 记录用户的编码风格和工具偏好
- 个性化 Qwen Coder 的响应和建议

### 4. 全局缓存 (Global Cache)
- 缓存常用的代码片段和文档
- 存储通用的研究发现和最佳实践

## ⚙️ 配置说明

`memory_config.json` 文件用于配置记忆系统的行为，例如：
- 会话保存策略
- 缓存过期时间
- 知识库更新频率

## 🔒 注意事项

- 此目录应定期备份以防止数据丢失
- 敏感信息（如API密钥）不应存储在此系统中
- 可以根据需要扩展目录结构以满足特定需求