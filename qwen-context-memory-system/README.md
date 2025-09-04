# Qwen Coder Context Memory Manager 使用说明

## 简介

Qwen Coder Context Memory Manager 是一个用于管理 Qwen Coder 提示词上下文记忆的系统。它可以帮助您保存、组织和检索与 Qwen Coder 的对话上下文，支持每日维护更新。

## 功能特性

- 创建和管理会话
- 保存对话上下文（提示词和响应）
- 按日期维护上下文记忆
- 生成会话摘要
- 查看和检索历史上下文
- 清理旧会话数据

## 安装和配置

### 环境要求

- Python 3.6 或更高版本

### 安装步骤

1. 将整个 `qwen-context-memory-system` 目录保存到您的计算机上
2. 确保您的系统已安装 Python 3

## 目录结构

```
qwen-context-memory-system/
├── context_memory_manager.py     # 主程序文件
├── context_memory_manager.bat    # Windows批处理启动脚本
├── context_memory.json           # 主内存文件
├── sessions/                     # 会话数据目录
│   └── [session_id]/            # 单个会话目录
│       └── session_data.json    # 会话数据文件
└── README.md                    # 本说明文件
```

## 使用方法

### 1. 创建新会话

```bash
python context_memory_manager.py --create-session --description "代码生成任务"
```

### 2. 添加上下文到会话

```bash
python context_memory_manager.py --add-context --session-id 20250903_143022 --prompt "帮我写一个Python函数" --response "好的，这是一个Python函数..."
```

### 3. 查看会话上下文

```bash
python context_memory_manager.py --view-context --session-id 20250903_143022
```

### 4. 生成会话摘要

```bash
python context_memory_manager.py --generate-summary --session-id 20250903_143022
```

### 5. 查看今日会话

```bash
python context_memory_manager.py --today
```

### 6. 查看内存摘要

```bash
python context_memory_manager.py --summary
```

### 7. 清理会话 (保留最近30天)

```bash
python context_memory_manager.py --cleanup
```

## 集成到 Qwen Coder 工作流

要将此系统集成到您的 Qwen Coder 工作流中，您可以：

1. 在每次开始新的编码任务时创建一个新会话
2. 在每次与 Qwen Coder 交互后，将提示词和响应添加到相应的会话中
3. 定期查看和管理会话数据

### 自动化集成示例

您可以创建一个包装脚本，在调用 Qwen Coder 后自动记录上下文：

```python
import subprocess
import json
from context_memory_manager import ContextMemoryManager

# 创建会话
manager = ContextMemoryManager()
session_id = manager.create_session(description="自动化编码任务")

# 调用Qwen Coder
prompt = "帮我写一个快速排序算法"
result = subprocess.run(["qwen-coder", "--prompt", prompt], capture_output=True, text=True)

# 记录上下文
manager.add_context(
    session_id=session_id,
    prompt=prompt,
    response=result.stdout,
    metadata={"exit_code": result.returncode}
)
```

## 数据结构说明

### 主内存文件 (context_memory.json)

```json
{
  "version": "1.0",
  "created_at": "2025-09-03T23:00:00.000000",
  "last_updated": "2025-09-03T23:00:00.000000",
  "total_sessions": 0,
  "sessions": {
    "2025-09-03": [
      {
        "session_id": "20250903_143022",
        "created_at": "2025-09-03T14:30:22.123456",
        "description": "代码生成任务"
      }
    ]
  }
}
```

### 会话数据文件 (sessions/[session_id]/session_data.json)

```json
{
  "session_id": "20250903_143022",
  "created_at": "2025-09-03T14:30:22.123456",
  "last_updated": "2025-09-03T14:35:10.654321",
  "description": "代码生成任务",
  "contexts": [
    {
      "timestamp": "2025-09-03T14:32:45.789012",
      "prompt": "帮我写一个Python函数",
      "response": "好的，这是一个Python函数...",
      "metadata": {}
    }
  ],
  "summary": "会话包含1个交互..."
}
```

## 注意事项

1. 系统会自动创建和管理目录结构
2. 会话ID默认使用时间戳格式 (YYYYMMDD_HHMMSS)
3. 数据文件使用JSON格式存储，便于查看和处理
4. 清理功能默认保留最近30天的数据
5. 系统支持添加元数据，可用于存储额外信息

## 故障排除

### 无法找到Python解释器

- 确保已安装Python 3.6或更高版本
- 确认Python已添加到系统PATH中

### 数据文件损坏

- 系统会在检测到文件损坏时自动创建新的数据文件
- 建议定期备份重要数据

### 其他问题

如遇到其他问题，请检查错误信息或联系开发者。