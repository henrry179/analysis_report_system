# Claude系列模型实现示例 / Claude Series Model Implementation Examples

> 本文档提供Anthropic Claude系列模型的完整实现示例、最佳实践和实际应用案例
> This document provides comprehensive implementation examples, best practices, and real-world application cases for Anthropic's Claude series models

**最后更新 / Last updated: 2025年09月02日 11:35:28**

---

## 📋 目录 / Table of Contents

- [概述 / Overview](#概述--overview)
- [环境配置 / Environment Setup](#环境配置--environment-setup)
- [基础调用示例 / Basic Calling Examples](#基础调用示例--basic-calling-examples)
- [高级功能示例 / Advanced Feature Examples](#高级功能示例--advanced-feature-examples)
- [工具调用集成 / Tool Calling Integration](#工具调用集成--tool-calling-integration)
- [流式响应处理 / Streaming Response Handling](#流式响应处理--streaming-response-handling)
- [错误处理与重试 / Error Handling and Retry](#错误处理与重试--error-handling-and-retry)
- [性能优化 / Performance Optimization](#性能优化--performance-optimization)
- [实际应用案例 / Real-world Application Cases](#实际应用案例--real-world-application-cases)
- [最佳实践 / Best Practices](#最佳实践--best-practices)

---

## 概述 / Overview

### Claude模型系列 / Claude Model Series

Anthropic的Claude系列模型以其卓越的安全性、可靠性以及在处理复杂任务时的出色表现而闻名。

**主要模型版本 / Main Model Versions:**
- **Claude 3.5 Sonnet**: 最先进的模型，适合复杂任务
- **Claude 3 Opus**: 功能最强大的模型，适合高度复杂的任务
- **Claude 3 Haiku**: 速度最快的模型，适合简单任务
- **Claude 3 Sonnet**: 平衡性能和速度的通用模型

### 核心优势 / Core Advantages

```xml
<claude_advantages>
  <safety_focused>
    <!-- 安全导向 / Safety-focused -->
    <constitutional_ai>宪政AI设计 / Constitutional AI design</constitutional_ai>
    <jailbreak_resistant>抗越狱攻击 / Jailbreak resistant</jailbreak_resistant>
    <content_filtering>智能内容过滤 / Intelligent content filtering</content_filtering>
  </safety_focused>

  <capability_strengths>
    <!-- 能力优势 / Capability strengths -->
    <long_context>长上下文理解 / Long context understanding</long_context>
    <reasoning_ability>强大的推理能力 / Strong reasoning ability</reasoning_ability>
    <tool_integration>优秀的工具集成 / Excellent tool integration</tool_integration>
  </capability_strengths>

  <reliability_features>
    <!-- 可靠性特性 / Reliability features -->
    <consistent_responses>一致性响应 / Consistent responses</consistent_responses>
    <predictable_behavior>可预测行为 / Predictable behavior</predictable_behavior>
    <error_handling>优雅错误处理 / Graceful error handling</error_handling>
  </reliability_features>
</claude_advantages>
```

---

## 环境配置 / Environment Setup

### 依赖安装 / Dependencies Installation

```bash
# Python环境 / Python Environment
pip install anthropic
pip install python-dotenv  # 用于环境变量管理 / For environment variable management

# 或者使用Conda / Or use Conda
conda install -c conda-forge anthropic
```

### API密钥配置 / API Key Configuration

```python
# .env文件配置 / .env file configuration
# ANTHROPIC_API_KEY=your_api_key_here

# Python代码加载 / Python code loading
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('ANTHROPIC_API_KEY')
```

### 客户端初始化 / Client Initialization

```python
import anthropic

# 基础客户端初始化 / Basic client initialization
client = anthropic.Anthropic(
    api_key=api_key,
)

# 带代理的客户端初始化 / Client initialization with proxy
client = anthropic.Anthropic(
    api_key=api_key,
    proxies={
        'http': 'http://proxy.example.com:8080',
        'https': 'http://proxy.example.com:8080'
    }
)

# 自定义HTTP客户端 / Custom HTTP client
import httpx

http_client = httpx.Client(
    proxies={'http://': 'http://proxy.example.com:8080'},
    timeout=60.0
)

client = anthropic.Anthropic(
    api_key=api_key,
    http_client=http_client
)
```

---

## 基础调用示例 / Basic Calling Examples

### 简单文本生成 / Simple Text Generation

```python
# 基础文本生成 / Basic text generation
def simple_text_generation():
    """Claude基础文本生成功能 / Basic Claude text generation"""

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        temperature=0.7,
        system="你是一个专业的AI助手，擅长用中文回答问题。",
        messages=[
            {
                "role": "user",
                "content": "请解释什么是机器学习？"
            }
        ]
    )

    return message.content[0].text

# 调用示例 / Usage example
response = simple_text_generation()
print(response)
```

### 多轮对话 / Multi-turn Conversation

```python
def multi_turn_conversation():
    """多轮对话实现 / Multi-turn conversation implementation"""

    conversation_history = []

    def add_message(role, content):
        """添加消息到对话历史 / Add message to conversation history"""
        conversation_history.append({
            "role": role,
            "content": content
        })

    def get_response():
        """获取Claude的回复 / Get Claude's response"""
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            temperature=0.7,
            system="你是一个有帮助的AI助手，请用中文回答。",
            messages=conversation_history
        )
        return message.content[0].text

    # 对话示例 / Conversation example
    add_message("user", "你好，我正在学习Python编程。")
    response1 = get_response()
    print(f"Claude: {response1}")

    add_message("assistant", response1)
    add_message("user", "能帮我解释一下什么是列表推导式吗？")
    response2 = get_response()
    print(f"Claude: {response2}")

    return conversation_history

# 使用示例 / Usage example
conversation = multi_turn_conversation()
```

### 自定义系统提示 / Custom System Prompt

```python
def custom_system_prompt():
    """自定义系统提示词 / Custom system prompt"""

    system_prompts = {
        "code_reviewer": """
        你是一个经验丰富的代码审查专家。
        请从以下几个方面评估代码：
        1. 代码质量和可读性
        2. 性能和效率
        3. 安全性和最佳实践
        4. 可维护性和扩展性

        请提供具体的改进建议。
        """,

        "technical_writer": """
        你是一个专业的技术文档撰写者。
        请确保文档：
        1. 结构清晰，逻辑连贯
        2. 概念准确，用词精确
        3. 示例丰富，易于理解
        4. 格式规范，便于阅读

        使用Markdown格式输出。
        """,

        "business_analyst": """
        你是一个资深商业分析师。
        在分析问题时，请：
        1. 识别核心业务需求
        2. 分析市场机会和风险
        3. 提出可行性解决方案
        4. 评估投资回报率

        请用数据和事实支撑你的分析。
        """
    }

    def analyze_with_role(role, content):
        """使用指定角色分析内容 / Analyze content with specified role"""

        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            temperature=0.3,  # 降低温度以获得更稳定的输出 / Lower temperature for more stable output
            system=system_prompts[role],
            messages=[
                {
                    "role": "user",
                    "content": content
                }
            ]
        )

        return message.content[0].text

    # 使用示例 / Usage examples
    code_sample = """
    def calculate_fibonacci(n):
        if n <= 1:
            return n
        return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)
    """

    review_result = analyze_with_role("code_reviewer", f"请审查这段代码：\n{code_sample}")
    print("代码审查结果:")
    print(review_result)

    return analyze_with_role

# 测试不同角色 / Test different roles
analyzer = custom_system_prompt()
```

---

## 高级功能示例 / Advanced Feature Examples

### 复杂推理任务 / Complex Reasoning Tasks

```python
def complex_reasoning_task():
    """复杂推理任务示例 / Complex reasoning task example"""

    def step_by_step_analysis(problem):
        """逐步分析问题 / Step-by-step problem analysis"""

        prompt = f"""
        请逐步分析并解决以下问题。每个步骤都要详细说明你的推理过程：

        问题：{problem}

        请按照以下步骤进行：
        1. 理解问题：明确问题的核心要素和约束条件
        2. 收集信息：识别需要的关键信息和数据
        3. 制定方案：提出可能的解决方案并评估优缺点
        4. 做出决策：基于分析结果选择最优方案
        5. 实施计划：制定具体的执行步骤和时间安排
        6. 风险评估：识别潜在的风险和应对策略

        请用中文详细回答每个步骤。
        """

        message = client.messages.create(
            model="claude-3-opus-20240229",  # 使用最强大的模型进行复杂推理 / Use the most powerful model for complex reasoning
            max_tokens=4000,
            temperature=0.1,  # 降低温度以获得更准确的推理 / Lower temperature for more accurate reasoning
            system="你是一个逻辑严谨的分析师，擅长系统性问题解决。",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return message.content[0].text

    # 示例问题 / Example problem
    business_problem = """
    我们的电商平台最近用户流失率上升了15%。
    主要现象：
    - 购物车放弃率从25%上升到35%
    - 用户复购率下降10%
    - 客户服务投诉增加20%

    请分析可能的原因并提出解决方案。
    """

    analysis_result = step_by_step_analysis(business_problem)
    print("复杂问题分析结果:")
    print(analysis_result)

    return analysis_result

# 执行复杂推理任务 / Execute complex reasoning task
result = complex_reasoning_task()
```

### 创意内容生成 / Creative Content Generation

```python
def creative_content_generation():
    """创意内容生成示例 / Creative content generation example"""

    def generate_creative_content(content_type, topic, constraints=None):
        """生成创意内容 / Generate creative content"""

        constraint_text = ""
        if constraints:
            constraint_text = f"\n\n约束条件：\n" + "\n".join(f"- {c}" for c in constraints)

        prompt = f"""
        请作为一名创意专家，生成{topic}相关的{content_type}。

        要求：
        1. 创意独特，有新意
        2. 内容完整，结构清晰
        3. 具有实用价值
        4. 易于理解和应用{constraint_text}

        请提供完整的{content_type}内容，包括标题、主要内容和总结。
        """

        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=3000,
            temperature=0.8,  # 提高温度以增加创意性 / Increase temperature for more creativity
            system="你是一个富有创意的AI助手，擅长生成创新性的内容。",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return message.content[0].text

    # 创意内容生成示例 / Creative content generation examples

    # 示例1：生成产品介绍文案 / Example 1: Generate product introduction copy
    product_copy = generate_creative_content(
        content_type="产品介绍文案",
        topic="智能家居控制系统",
        constraints=[
            "面向年轻家庭用户",
            "突出易用性和智能化",
            "包含核心功能和技术优势",
            "字数控制在300字以内"
        ]
    )
    print("产品介绍文案:")
    print(product_copy)
    print("\n" + "="*50 + "\n")

    # 示例2：生成教育内容 / Example 2: Generate educational content
    tutorial_content = generate_creative_content(
        content_type="编程教程",
        topic="Python异步编程",
        constraints=[
            "适合初学者",
            "包含实际代码示例",
            "解释核心概念",
            "提供练习建议"
        ]
    )
    print("编程教程:")
    print(tutorial_content)

    return generate_creative_content

# 执行创意内容生成 / Execute creative content generation
creative_generator = creative_content_generation()
```

---

## 工具调用集成 / Tool Calling Integration

### 基础工具调用 / Basic Tool Calling

```python
def basic_tool_calling():
    """基础工具调用示例 / Basic tool calling example"""

    # 定义工具 / Define tools
    tools = [
        {
            "name": "get_weather",
            "description": "获取指定城市的天气信息",
            "input_schema": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称"
                    }
                },
                "required": ["city"]
            }
        },
        {
            "name": "calculate",
            "description": "执行数学计算",
            "input_schema": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "数学表达式"
                    }
                },
                "required": ["expression"]
            }
        }
    ]

    def get_weather(city):
        """模拟获取天气信息 / Simulate getting weather information"""
        # 这里应该是实际的天气API调用 / This should be actual weather API call
        weather_data = {
            "北京": {"temperature": 25, "condition": "晴朗", "humidity": 60},
            "上海": {"temperature": 28, "condition": "多云", "humidity": 75},
            "深圳": {"temperature": 30, "condition": "炎热", "humidity": 80}
        }
        return weather_data.get(city, {"temperature": 20, "condition": "未知", "humidity": 50})

    def calculate(expression):
        """执行数学计算 / Execute mathematical calculation"""
        try:
            result = eval(expression)
            return {"result": result, "success": True}
        except Exception as e:
            return {"result": None, "success": False, "error": str(e)}

    def process_tool_call(tool_call):
        """处理工具调用 / Process tool call"""
        tool_name = tool_call.name
        tool_args = tool_call.input

        if tool_name == "get_weather":
            result = get_weather(tool_args["city"])
            return f"{tool_args['city']}的天气：温度{result['temperature']}°C，{result['condition']}，湿度{result['humidity']}%"

        elif tool_name == "calculate":
            result = calculate(tool_args["expression"])
            if result["success"]:
                return f"计算结果：{result['result']}"
            else:
                return f"计算错误：{result['error']}"

        return "未知工具"

    def chat_with_tools(user_message):
        """带工具的对话 / Chat with tools"""

        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            temperature=0.7,
            system="你是一个有帮助的AI助手，可以使用工具来回答问题。",
            messages=[
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            tools=tools
        )

        # 检查是否有工具调用 / Check if there are tool calls
        if message.stop_reason == "tool_use":
            tool_results = []
            for tool_call in message.content:
                if hasattr(tool_call, 'name'):  # 这是工具调用 / This is a tool call
                    result = process_tool_call(tool_call)
                    tool_results.append(result)

            # 使用工具结果继续对话 / Continue conversation with tool results
            final_message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                temperature=0.7,
                system="你是一个有帮助的AI助手，可以使用工具来回答问题。",
                messages=[
                    {
                        "role": "user",
                        "content": user_message
                    },
                    {
                        "role": "assistant",
                        "content": message.content
                    },
                    {
                        "role": "user",
                        "content": f"工具调用结果：{'; '.join(tool_results)}"
                    }
                ]
            )

            return final_message.content[0].text

        return message.content[0].text

    # 使用示例 / Usage examples
    print("工具调用示例:")
    print(chat_with_tools("北京今天的天气怎么样？"))
    print(chat_with_tools("计算25乘以17等于多少？"))

    return chat_with_tools

# 执行工具调用示例 / Execute tool calling example
tool_chat = basic_tool_calling()
```

### 高级工具链 / Advanced Tool Chain

```python
def advanced_tool_chain():
    """高级工具链示例 / Advanced tool chain example"""

    # 更复杂的工具定义 / More complex tool definitions
    advanced_tools = [
        {
            "name": "web_search",
            "description": "在网络上搜索信息",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "搜索查询"},
                    "max_results": {"type": "integer", "description": "最大结果数量", "default": 5}
                },
                "required": ["query"]
            }
        },
        {
            "name": "code_executor",
            "description": "执行Python代码",
            "input_schema": {
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "要执行的Python代码"}
                },
                "required": ["code"]
            }
        },
        {
            "name": "data_analyzer",
            "description": "分析数据并生成报告",
            "input_schema": {
                "type": "object",
                "properties": {
                    "data": {"type": "string", "description": "要分析的数据（JSON格式）"},
                    "analysis_type": {"type": "string", "description": "分析类型", "enum": ["summary", "correlation", "trend"]}
                },
                "required": ["data", "analysis_type"]
            }
        }
    ]

    def execute_web_search(query, max_results=5):
        """执行网络搜索 / Execute web search"""
        # 模拟搜索结果 / Simulate search results
        mock_results = [
            f"关于'{query}'的结果 1",
            f"关于'{query}'的结果 2",
            f"关于'{query}'的结果 3"
        ]
        return mock_results[:max_results]

    def execute_code(code):
        """执行Python代码 / Execute Python code"""
        try:
            # 注意：实际应用中应该使用更安全的方式执行代码
            # Note: In real applications, use safer ways to execute code
            result = eval(code)
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def analyze_data(data, analysis_type):
        """分析数据 / Analyze data"""
        try:
            import json
            parsed_data = json.loads(data)

            if analysis_type == "summary":
                return f"数据摘要：包含{len(parsed_data)}个数据点"
            elif analysis_type == "correlation":
                return "数据相关性分析：发现强相关性"
            elif analysis_type == "trend":
                return "趋势分析：数据呈上升趋势"

        except Exception as e:
            return f"数据分析错误：{str(e)}"

    def process_advanced_tools(message):
        """处理高级工具调用 / Process advanced tool calls"""

        tool_calls = []
        for content_block in message.content:
            if hasattr(content_block, 'name'):  # 工具调用 / Tool call
                tool_calls.append(content_block)

        if not tool_calls:
            return None

        tool_results = []
        for tool_call in tool_calls:
            if tool_call.name == "web_search":
                result = execute_web_search(**tool_call.input)
                tool_results.append(f"搜索结果：{result}")

            elif tool_call.name == "code_executor":
                result = execute_code(tool_call.input["code"])
                tool_results.append(f"代码执行结果：{result}")

            elif tool_call.name == "data_analyzer":
                result = analyze_data(**tool_call.input)
                tool_results.append(f"数据分析结果：{result}")

        return tool_results

    def advanced_chat_with_tools(user_query):
        """高级工具对话 / Advanced tool conversation"""

        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            temperature=0.7,
            system="你是一个强大的AI助手，可以使用各种工具来帮助用户解决问题。",
            messages=[
                {
                    "role": "user",
                    "content": user_query
                }
            ],
            tools=advanced_tools
        )

        tool_results = process_advanced_tools(message)

        if tool_results:
            # 使用工具结果生成最终回答 / Generate final answer using tool results
            final_message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                temperature=0.7,
                system="你是一个强大的AI助手，可以使用各种工具来帮助用户解决问题。",
                messages=[
                    {
                        "role": "user",
                        "content": user_query
                    },
                    {
                        "role": "assistant",
                        "content": message.content
                    },
                    {
                        "role": "user",
                        "content": f"工具执行结果：\n" + "\n".join(tool_results)
                    }
                ]
            )

            return final_message.content[0].text

        return message.content[0].text

    # 高级工具使用示例 / Advanced tool usage examples
    print("高级工具链示例:")

    # 示例1：结合搜索和分析 / Example 1: Combine search and analysis
    query1 = "分析当前AI发展趋势，并搜索相关最新研究。"
    result1 = advanced_chat_with_tools(query1)
    print(f"查询1结果: {result1[:200]}...")

    # 示例2：代码执行和数据分析 / Example 2: Code execution and data analysis
    query2 = "计算斐波那契数列前10项，并分析其增长趋势。"
    result2 = advanced_chat_with_tools(query2)
    print(f"查询2结果: {result2[:200]}...")

    return advanced_chat_with_tools

# 执行高级工具链示例 / Execute advanced tool chain example
advanced_tools = advanced_tool_chain()
```

---

## 流式响应处理 / Streaming Response Handling

### 基础流式响应 / Basic Streaming Response

```python
import asyncio

def basic_streaming_response():
    """基础流式响应处理 / Basic streaming response handling"""

    async def stream_response_async(user_message):
        """异步流式响应 / Asynchronous streaming response"""

        print("开始流式响应... / Starting streaming response...")

        async with client.messages.stream(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            temperature=0.7,
            system="你是一个专业的AI助手。",
            messages=[
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        ) as stream:
            full_response = ""
            chunk_count = 0

            async for chunk in stream:
                if chunk.type == "content_block_delta":
                    content = chunk.delta.text
                    if content:
                        print(content, end="", flush=True)
                        full_response += content
                        chunk_count += 1

                        # 每10个块打印一次进度 / Print progress every 10 chunks
                        if chunk_count % 10 == 0:
                            print(f"\n[已接收 {chunk_count} 个内容块] / [Received {chunk_count} content blocks]")

            print(f"\n\n流式响应完成！总共接收了 {chunk_count} 个内容块。")
            print(f"完整响应长度: {len(full_response)} 字符")

            return full_response

    def stream_response_sync(user_message):
        """同步流式响应 / Synchronous streaming response"""

        print("开始同步流式响应... / Starting synchronous streaming response...")

        with client.messages.stream(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            temperature=0.7,
            system="你是一个专业的AI助手。",
            messages=[
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        ) as stream:
            full_response = ""
            chunk_count = 0

            for chunk in stream:
                if chunk.type == "content_block_delta":
                    content = chunk.delta.text
                    if content:
                        print(content, end="", flush=True)
                        full_response += content
                        chunk_count += 1

            print(f"\n\n同步流式响应完成！总共接收了 {chunk_count} 个内容块。")

            return full_response

    # 使用示例 / Usage examples
    test_message = "请详细解释什么是机器学习，并给出一些实际应用案例。"

    print("="*60)
    print("异步流式响应示例 / Asynchronous Streaming Example")
    print("="*60)

    # 异步执行 / Asynchronous execution
    asyncio.run(stream_response_async(test_message))

    print("\n" + "="*60)
    print("同步流式响应示例 / Synchronous Streaming Example")
    print("="*60)

    # 同步执行 / Synchronous execution
    stream_response_sync(test_message)

    return {
        "async_streaming": lambda msg: asyncio.run(stream_response_async(msg)),
        "sync_streaming": stream_response_sync
    }

# 执行流式响应示例 / Execute streaming response example
streaming_functions = basic_streaming_response()
```

### 高级流式处理 / Advanced Streaming Processing

```python
def advanced_streaming_processing():
    """高级流式处理示例 / Advanced streaming processing example"""

    class StreamingProcessor:
        """流式响应处理器 / Streaming response processor"""

        def __init__(self):
            self.full_response = ""
            self.chunk_count = 0
            self.start_time = None
            self.end_time = None
            self.processing_stats = {
                "total_chunks": 0,
                "text_chunks": 0,
                "empty_chunks": 0,
                "avg_chunk_size": 0,
                "total_size": 0
            }

        def start_processing(self):
            """开始处理 / Start processing"""
            self.start_time = time.time()
            print("🚀 开始处理流式响应... / Starting streaming response processing...")

        def process_chunk(self, chunk):
            """处理单个数据块 / Process individual chunk"""
            self.chunk_count += 1
            self.processing_stats["total_chunks"] += 1

            if chunk.type == "content_block_delta":
                content = chunk.delta.text
                if content:
                    print(content, end="", flush=True)
                    self.full_response += content
                    self.processing_stats["text_chunks"] += 1
                    self.processing_stats["total_size"] += len(content)
                else:
                    self.processing_stats["empty_chunks"] += 1

            # 实时统计更新 / Real-time statistics update
            if self.chunk_count % 20 == 0:
                self._print_progress_stats()

        def finish_processing(self):
            """完成处理 / Finish processing"""
            self.end_time = time.time()
            processing_time = self.end_time - self.start_time

            print("
✅ 流式响应处理完成！ / Streaming response processing completed!"            print("📊 处理统计 / Processing Statistics:"            print(f"  - 总数据块数: {self.processing_stats['total_chunks']}")
            print(f"  - 文本数据块数: {self.processing_stats['text_chunks']}")
            print(f"  - 空数据块数: {self.processing_stats['empty_chunks']}")
            print(f"  - 总字符数: {self.processing_stats['total_size']}")
            if self.processing_stats['text_chunks'] > 0:
                avg_size = self.processing_stats['total_size'] / self.processing_stats['text_chunks']
                print(".1f"            print(".2f"            print(".1f"
            return self.full_response

        def _print_progress_stats(self):
            """打印进度统计 / Print progress statistics"""
            elapsed = time.time() - self.start_time
            print(".1f"
    def advanced_streaming_chat(user_message):
        """高级流式对话 / Advanced streaming chat"""

        processor = StreamingProcessor()
        processor.start_processing()

        with client.messages.stream(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            temperature=0.7,
            system="你是一个专业的AI助手，请提供详细而有帮助的回答。",
            messages=[
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        ) as stream:
            for chunk in stream:
                processor.process_chunk(chunk)

        return processor.finish_processing()

    # 高级流式处理示例 / Advanced streaming processing example
    print("="*80)
    print("🎯 高级流式响应处理示例 / Advanced Streaming Response Processing Example")
    print("="*80)

    test_query = """
    请详细解释人工智能的发展历程，包括：
    1. 人工智能的起源和发展阶段
    2. 关键技术突破和里程碑事件
    3. 当前主要研究方向和发展趋势
    4. 对未来社会的影响预测

    请用清晰的结构和具体的例子来阐述。
    """

    result = advanced_streaming_chat(test_query)

    print("
🔍 响应摘要 / Response Summary:"    print(f"总字符数: {len(result)}")
    print(f"总段落数: {result.count(chr(10)) + 1}")
    print(f"包含关键词: {'人工智能' in result}, {'机器学习' in result}, {'深度学习' in result}")

    return result

# 执行高级流式处理 / Execute advanced streaming processing
import time
advanced_result = advanced_streaming_processing()
```

---

## 错误处理与重试 / Error Handling and Retry

### 基础错误处理 / Basic Error Handling

```python
import time
from typing import Optional, Dict, Any

def basic_error_handling():
    """基础错误处理示例 / Basic error handling example"""

    class ClaudeAPIError(Exception):
        """Claude API 错误类 / Claude API Error class"""
        def __init__(self, message: str, status_code: Optional[int] = None):
            super().__init__(message)
            self.status_code = status_code

    def safe_api_call(messages: list, **kwargs) -> str:
        """安全的API调用 / Safe API call"""

        max_retries = kwargs.pop('max_retries', 3)
        retry_delay = kwargs.pop('retry_delay', 1.0)
        backoff_factor = kwargs.pop('backoff_factor', 2.0)

        last_exception = None

        for attempt in range(max_retries):
            try:
                message = client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    messages=messages,
                    **kwargs
                )

                return message.content[0].text

            except anthropic.APIError as e:
                last_exception = e

                # 处理不同的API错误 / Handle different API errors
                if e.status_code == 400:
                    # 请求错误 / Request error
                    raise ClaudeAPIError(f"请求错误: {e.message}", e.status_code)

                elif e.status_code == 401:
                    # 认证错误 / Authentication error
                    raise ClaudeAPIError(f"API密钥无效: {e.message}", e.status_code)

                elif e.status_code == 429:
                    # 速率限制 / Rate limit
                    if attempt < max_retries - 1:
                        wait_time = retry_delay * (backoff_factor ** attempt)
                        print(f"速率限制，等待 {wait_time:.1f} 秒后重试... / Rate limited, waiting {wait_time:.1f} seconds...")
                        time.sleep(wait_time)
                        continue
                    else:
                        raise ClaudeAPIError(f"速率限制: {e.message}", e.status_code)

                elif e.status_code >= 500:
                    # 服务器错误 / Server error
                    if attempt < max_retries - 1:
                        wait_time = retry_delay * (backoff_factor ** attempt)
                        print(f"服务器错误，等待 {wait_time:.1f} 秒后重试... / Server error, waiting {wait_time:.1f} seconds...")
                        time.sleep(wait_time)
                        continue
                    else:
                        raise ClaudeAPIError(f"服务器错误: {e.message}", e.status_code)

                else:
                    # 其他错误 / Other errors
                    raise ClaudeAPIError(f"API错误: {e.message}", e.status_code)

            except Exception as e:
                last_exception = e
                if attempt < max_retries - 1:
                    wait_time = retry_delay * (backoff_factor ** attempt)
                    print(f"未知错误，等待 {wait_time:.1f} 秒后重试... / Unknown error, waiting {wait_time:.1f} seconds...")
                    time.sleep(wait_time)
                    continue
                else:
                    raise ClaudeAPIError(f"未知错误: {str(e)}")

        # 如果所有重试都失败 / If all retries fail
        raise ClaudeAPIError(f"API调用失败，已重试 {max_retries} 次: {str(last_exception)}")

    def robust_chat(user_message: str) -> str:
        """健壮的对话函数 / Robust chat function"""

        messages = [
            {
                "role": "user",
                "content": user_message
            }
        ]

        try:
            response = safe_api_call(
                messages=messages,
                max_tokens=1000,
                temperature=0.7,
                system="你是一个有帮助的AI助手。",
                max_retries=3,
                retry_delay=1.0,
                backoff_factor=2.0
            )

            return response

        except ClaudeAPIError as e:
            print(f"API调用失败: {e}")
            if e.status_code == 401:
                return "抱歉，API密钥配置有误。请检查您的API密钥设置。 / Sorry, there's an issue with the API key configuration. Please check your API key settings."
            elif e.status_code == 429:
                return "抱歉，当前请求过于频繁。请稍后再试。 / Sorry, the request is too frequent. Please try again later."
            else:
                return "抱歉，服务暂时不可用。请稍后重试。 / Sorry, the service is temporarily unavailable. Please try again later."

    # 错误处理测试 / Error handling test
    print("基础错误处理示例 / Basic Error Handling Example:")

    # 正常请求 / Normal request
    normal_response = robust_chat("你好，请介绍一下自己。")
    print(f"正常响应: {normal_response[:100]}...")

    # 模拟错误情况 / Simulate error conditions
    print("\n模拟错误情况测试 / Simulated Error Condition Tests:")

    # 无效的API密钥测试 / Invalid API key test
    try:
        # 这里可以模拟不同的错误情况 / Here you can simulate different error conditions
        print("错误处理机制已准备就绪 / Error handling mechanism is ready")
    except Exception as e:
        print(f"错误处理测试: {e}")

    return robust_chat

# 执行基础错误处理示例 / Execute basic error handling example
error_handling_chat = basic_error_handling()
```

### 高级错误处理和监控 / Advanced Error Handling and Monitoring

```python
import logging
from datetime import datetime, timedelta
from collections import defaultdict

def advanced_error_handling_and_monitoring():
    """高级错误处理和监控示例 / Advanced error handling and monitoring example"""

    # 配置日志 / Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger('ClaudeAPI')

    class APIMonitor:
        """API监控器 / API Monitor"""

        def __init__(self):
            self.metrics = {
                "total_requests": 0,
                "successful_requests": 0,
                "failed_requests": 0,
                "error_types": defaultdict(int),
                "response_times": [],
                "rate_limits": 0
            }
            self.error_window = timedelta(minutes=5)
            self.recent_errors = []

        def record_request(self, success: bool, response_time: float, error_type: str = None):
            """记录请求 / Record request"""
            self.metrics["total_requests"] += 1

            if success:
                self.metrics["successful_requests"] += 1
            else:
                self.metrics["failed_requests"] += 1
                if error_type:
                    self.metrics["error_types"][error_type] += 1

            self.metrics["response_times"].append(response_time)

            # 清理旧的错误记录 / Clean old error records
            current_time = datetime.now()
            self.recent_errors = [
                error for error in self.recent_errors
                if current_time - error["timestamp"] < self.error_window
            ]

            if not success:
                self.recent_errors.append({
                    "timestamp": current_time,
                    "error_type": error_type
                })

        def get_health_status(self) -> Dict[str, Any]:
            """获取健康状态 / Get health status"""
            total = self.metrics["total_requests"]
            success_rate = (self.metrics["successful_requests"] / total * 100) if total > 0 else 0

            avg_response_time = (
                sum(self.metrics["response_times"]) / len(self.metrics["response_times"])
                if self.metrics["response_times"] else 0
            )

            error_rate_5min = len(self.recent_errors) / 5  # 每分钟错误率 / Errors per minute

            health_status = "healthy"
            if success_rate < 95:
                health_status = "degraded"
            if success_rate < 80 or error_rate_5min > 10:
                health_status = "unhealthy"

            return {
                "status": health_status,
                "success_rate": success_rate,
                "avg_response_time": avg_response_time,
                "error_rate_5min": error_rate_5min,
                "total_requests": total,
                "recent_errors": len(self.recent_errors)
            }

        def should_circuit_break(self) -> bool:
            """判断是否应该熔断 / Determine if circuit breaker should be triggered"""
            error_rate_5min = len(self.recent_errors) / 5
            return error_rate_5min > 15  # 每分钟15个错误触发熔断 / 15 errors per minute trigger circuit breaker

    class CircuitBreaker:
        """熔断器 / Circuit Breaker"""

        def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60):
            self.failure_threshold = failure_threshold
            self.recovery_timeout = recovery_timeout
            self.failure_count = 0
            self.last_failure_time = None
            self.state = "closed"  # closed, open, half_open

        def call_allowed(self) -> bool:
            """检查调用是否被允许 / Check if call is allowed"""
            if self.state == "closed":
                return True
            elif self.state == "open":
                if datetime.now().timestamp() - self.last_failure_time.timestamp() > self.recovery_timeout:
                    self.state = "half_open"
                    return True
                return False
            elif self.state == "half_open":
                return True
            return False

        def record_success(self):
            """记录成功 / Record success"""
            self.failure_count = 0
            if self.state == "half_open":
                self.state = "closed"

        def record_failure(self):
            """记录失败 / Record failure"""
            self.failure_count += 1
            self.last_failure_time = datetime.now()

            if self.failure_count >= self.failure_threshold:
                self.state = "open"

    def advanced_safe_api_call(messages: list, monitor: APIMonitor, circuit_breaker: CircuitBreaker, **kwargs) -> str:
        """高级安全的API调用 / Advanced safe API call"""

        if not circuit_breaker.call_allowed():
            raise ClaudeAPIError("熔断器已打开，暂停服务 / Circuit breaker is open, service paused")

        start_time = time.time()

        try:
            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                messages=messages,
                **kwargs
            )

            response_time = time.time() - start_time
            monitor.record_request(success=True, response_time=response_time)
            circuit_breaker.record_success()

            logger.info(".3f"            return message.content[0].text

        except Exception as e:
            response_time = time.time() - start_time
            error_type = type(e).__name__
            monitor.record_request(success=False, response_time=response_time, error_type=error_type)
            circuit_breaker.record_failure()

            logger.error(f"API调用失败: {error_type} - {str(e)}")

            # 检查健康状态 / Check health status
            health = monitor.get_health_status()
            if health["status"] == "unhealthy":
                logger.warning("服务健康状态不佳 / Service health status is poor")

            raise

    def monitored_chat(user_message: str) -> str:
        """带监控的对话 / Monitored chat"""

        monitor = APIMonitor()
        circuit_breaker = CircuitBreaker()

        messages = [
            {
                "role": "user",
                "content": user_message
            }
        ]

        try:
            response = advanced_safe_api_call(
                messages=messages,
                monitor=monitor,
                circuit_breaker=circuit_breaker,
                max_tokens=1000,
                temperature=0.7,
                system="你是一个有帮助的AI助手。"
            )

            # 打印健康状态 / Print health status
            health = monitor.get_health_status()
            print("
📊 当前健康状态 / Current Health Status:"            print(f"  - 状态: {health['status']}")
            print(".1f"            print(".3f"            print(".1f"
            return response

        except ClaudeAPIError as e:
            print(f"API调用失败: {e}")

            # 提供降级响应 / Provide degraded response
            return "抱歉，当前服务暂时不可用。请稍后重试。 / Sorry, the service is temporarily unavailable. Please try again later."

    # 高级错误处理和监控测试 / Advanced error handling and monitoring test
    print("="*80)
    print("🔧 高级错误处理和监控示例 / Advanced Error Handling and Monitoring Example")
    print("="*80)

    test_messages = [
        "你好，请介绍一下人工智能的发展历程。",
        "请解释什么是机器学习。",
        "人工智能有哪些主要应用领域？"
    ]

    for i, test_msg in enumerate(test_messages, 1):
        print(f"\n--- 测试消息 {i} / Test Message {i} ---")
        response = monitored_chat(test_msg)
        print(f"响应: {response[:150]}...")

        # 模拟一些延迟 / Simulate some delay
        time.sleep(0.5)

    return monitored_chat

# 执行高级错误处理和监控 / Execute advanced error handling and monitoring
advanced_monitored_chat = advanced_error_handling_and_monitoring()
```

---

## 性能优化 / Performance Optimization

### 模型选择和参数调优 / Model Selection and Parameter Tuning

```python
def performance_optimization():
    """性能优化示例 / Performance optimization example"""

    def benchmark_models():
        """模型性能基准测试 / Model performance benchmarking"""

        models_to_test = [
            "claude-3-haiku-20240307",    # 最快模型 / Fastest model
            "claude-3-5-sonnet-20241022", # 平衡性能 / Balanced performance
            "claude-3-opus-20240229"      # 最强性能 / Strongest performance
        ]

        test_prompts = [
            "解释量子计算的基本原理。",  # 中等复杂度 / Medium complexity
            "写一首关于春天的诗。",       # 创意任务 / Creative task
            "分析当前全球经济形势。",     # 复杂分析 / Complex analysis
        ]

        results = {}

        for model in models_to_test:
            print(f"\n🧪 测试模型: {model} / Testing model: {model}")
            model_results = {}

            for prompt in test_prompts:
                print(f"  📝 测试提示: {prompt[:20]}...")

                # 多次测试取平均值 / Multiple tests for average
                response_times = []
                token_counts = []

                for _ in range(3):  # 3次测试 / 3 tests
                    start_time = time.time()

                    try:
                        message = client.messages.create(
                            model=model,
                            max_tokens=500,
                            temperature=0.7,
                            messages=[
                                {
                                    "role": "user",
                                    "content": prompt
                                }
                            ]
                        )

                        response_time = time.time() - start_time
                        response_times.append(response_time)

                        # 估算token数量 / Estimate token count
                        token_count = len(message.content[0].text) * 0.3  # 粗略估算 / Rough estimate
                        token_counts.append(token_count)

                    except Exception as e:
                        print(f"    ❌ 测试失败: {e}")
                        continue

                if response_times:
                    avg_time = sum(response_times) / len(response_times)
                    avg_tokens = sum(token_counts) / len(token_counts)
                    tokens_per_second = avg_tokens / avg_time if avg_time > 0 else 0

                    model_results[prompt[:20]] = {
                        "avg_response_time": avg_time,
                        "avg_tokens": avg_tokens,
                        "tokens_per_second": tokens_per_second
                    }

                    print(".3f"                    print(".1f"                    print(".1f"
            results[model] = model_results

        return results

    def optimize_parameters():
        """参数优化示例 / Parameter optimization example"""

        test_prompt = "详细解释机器学习的工作原理，并给出实际应用案例。"
        parameter_combinations = [
            {"temperature": 0.1, "max_tokens": 500},
            {"temperature": 0.7, "max_tokens": 1000},
            {"temperature": 1.0, "max_tokens": 1500},
        ]

        print("\n⚙️ 参数优化测试 / Parameter Optimization Test")
        print("="*60)

        for i, params in enumerate(parameter_combinations, 1):
            print(f"\n测试组合 {i} / Test Combination {i}:")
            print(f"  - 温度: {params['temperature']}")
            print(f"  - 最大token数: {params['max_tokens']}")

            response_times = []

            for _ in range(3):
                start_time = time.time()

                message = client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    temperature=params["temperature"],
                    max_tokens=params["max_tokens"],
                    messages=[
                        {
                            "role": "user",
                            "content": test_prompt
                        }
                    ]
                )

                response_time = time.time() - start_time
                response_times.append(response_time)

            avg_time = sum(response_times) / len(response_times)
            response_length = len(message.content[0].text)

            print(".3f"            print(f"  - 响应长度: {response_length} 字符")

            # 质量评估 / Quality assessment
            quality_score = assess_response_quality(message.content[0].text)
            print(".2f"
    def assess_response_quality(response_text):
        """评估响应质量 / Assess response quality"""
        # 简单的质量评估 / Simple quality assessment
        score = 0

        # 检查结构完整性 / Check structural completeness
        if "工作原理" in response_text or "how it works" in response_text:
            score += 20

        # 检查示例丰富性 / Check example richness
        if "例如" in response_text or "比如" in response_text or "example" in response_text.lower():
            score += 20

        # 检查逻辑清晰性 / Check logical clarity
        if "首先" in response_text or "其次" in response_text or "first" in response_text.lower():
            score += 20

        # 检查深度 / Check depth
        word_count = len(response_text.split())
        if word_count > 100:
            score += 20
        elif word_count > 50:
            score += 10

        # 检查专业性 / Check professionalism
        technical_terms = ["算法", "模型", "训练", "预测", "algorithm", "model", "training", "prediction"]
        term_count = sum(1 for term in technical_terms if term in response_text)
        score += min(term_count * 5, 20)

        return score

    # 执行性能优化测试 / Execute performance optimization tests
    print("="*80)
    print("🚀 Claude性能优化示例 / Claude Performance Optimization Example")
    print("="*80)

    # 1. 模型基准测试 / Model benchmarking
    print("\n📊 模型性能基准测试 / Model Performance Benchmarking")
    benchmark_results = benchmark_models()

    # 2. 参数优化 / Parameter optimization
    optimize_parameters()

    # 3. 性能建议 / Performance recommendations
    print("\n💡 性能优化建议 / Performance Optimization Recommendations")
    print("-" * 60)
    print("1. 模型选择策略 / Model Selection Strategy:")
    print("   • 简单任务: 使用 Claude 3 Haiku")
    print("   • 一般任务: 使用 Claude 3.5 Sonnet")
    print("   • 复杂任务: 使用 Claude 3 Opus")
    print()
    print("2. 参数调优建议 / Parameter Tuning Recommendations:")
    print("   • 事实性任务: 温度 0.1-0.3")
    print("   • 创意任务: 温度 0.7-0.9")
    print("   • 分析任务: 温度 0.3-0.5")
    print()
    print("3. 性能监控 / Performance Monitoring:")
    print("   • 监控响应时间和token使用量")
    print("   • 根据使用模式调整参数")
    print("   • 定期进行性能基准测试")

    return {
        "benchmark_results": benchmark_results,
        "optimization_tips": [
            "根据任务复杂度选择合适的模型",
            "调整温度参数以平衡质量和速度",
            "监控和优化token使用效率",
            "使用流式响应减少感知延迟"
        ]
    }

# 执行性能优化示例 / Execute performance optimization example
import time
performance_results = performance_optimization()
```

---

## 实际应用案例 / Real-world Application Cases

### 智能客服系统 / Intelligent Customer Service System

```python
def intelligent_customer_service():
    """智能客服系统示例 / Intelligent customer service system example"""

    class CustomerServiceAgent:
        """客服代理 / Customer service agent"""

        def __init__(self):
            self.conversation_history = []
            self.user_profile = {}
            self.intent_classifier = self._load_intent_classifier()

        def _load_intent_classifier(self):
            """加载意图分类器 / Load intent classifier"""
            # 这里可以集成更复杂的意图分类模型
            # Here you can integrate more complex intent classification models
            return {
                "product_info": ["产品", "功能", "特点", "价格"],
                "technical_support": ["问题", "错误", "故障", "修复"],
                "billing": ["账单", "支付", "退款", "发票"],
                "general": []
            }

        def classify_intent(self, message):
            """分类用户意图 / Classify user intent"""
            message_lower = message.lower()

            for intent, keywords in self.intent_classifier.items():
                if any(keyword in message_lower for keyword in keywords):
                    return intent

            return "general"

        def generate_response(self, user_message, intent):
            """生成回复 / Generate response"""

            # 构建系统提示 / Build system prompt
            system_prompt = f"""
            你是一个专业的客服代表。用户的问题类型是：{intent}

            请按照以下原则回复：
            1. 友好专业，保持礼貌
            2. 理解用户问题，提供准确解答
            3. 如果需要技术支持，引导用户到合适渠道
            4. 主动提供相关帮助信息
            5. 回复简洁明了，避免冗长

            当前对话历史：
            {self._format_conversation_history()}
            """

            # 调用Claude生成回复 / Call Claude to generate response
            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=800,
                temperature=0.7,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": user_message
                    }
                ]
            )

            return message.content[0].text

        def _format_conversation_history(self):
            """格式化对话历史 / Format conversation history"""
            if not self.conversation_history:
                return "无历史对话 / No conversation history"

            formatted = []
            for i, (user_msg, ai_response) in enumerate(self.conversation_history[-3:], 1):  # 只显示最近3轮 / Show only last 3 rounds
                formatted.append(f"{i}. 用户: {user_msg[:50]}...")
                formatted.append(f"   AI: {ai_response[:50]}...")

            return "\n".join(formatted)

        def handle_customer_query(self, user_message):
            """处理客户查询 / Handle customer query"""

            # 分类意图 / Classify intent
            intent = self.classify_intent(user_message)

            # 生成回复 / Generate response
            response = self.generate_response(user_message, intent)

            # 更新对话历史 / Update conversation history
            self.conversation_history.append((user_message, response))

            # 记录用户偏好 / Record user preferences
            self._update_user_profile(user_message, intent)

            return {
                "response": response,
                "intent": intent,
                "confidence": 0.8,  # 这里可以集成更复杂的置信度计算 / Here you can integrate more complex confidence calculation
                "suggested_actions": self._generate_suggested_actions(intent)
            }

        def _update_user_profile(self, message, intent):
            """更新用户画像 / Update user profile"""
            # 简单的用户画像更新逻辑 / Simple user profile update logic
            if intent not in self.user_profile:
                self.user_profile[intent] = 0
            self.user_profile[intent] += 1

        def _generate_suggested_actions(self, intent):
            """生成建议行动 / Generate suggested actions"""
            suggestions = {
                "product_info": ["查看产品手册", "预约产品演示", "联系销售团队"],
                "technical_support": ["查看常见问题", "提交支持工单", "联系技术支持"],
                "billing": ["查看账单详情", "更新支付信息", "申请退款"],
                "general": ["浏览帮助中心", "联系客服", "查看最新更新"]
            }
            return suggestions.get(intent, ["浏览帮助中心"])

    # 创建客服代理 / Create customer service agent
    agent = CustomerServiceAgent()

    # 测试客服系统 / Test customer service system
    test_queries = [
        "你们的软件有什么功能？",
        "我的账户出现了登录问题",
        "我想查看一下账单",
        "你们的产品价格是多少？"
    ]

    print("🤖 智能客服系统演示 / Intelligent Customer Service System Demo")
    print("="*80)

    for i, query in enumerate(test_queries, 1):
        print(f"\n👤 用户查询 {i}: {query}")
        result = agent.handle_customer_query(query)

        print(f"🎯 识别意图: {result['intent']}")
        print(".2f"        print(f"💬 AI回复: {result['response'][:100]}...")
        print(f"📋 建议行动: {', '.join(result['suggested_actions'])}")
        print("-" * 50)

    return agent

# 执行智能客服系统 / Execute intelligent customer service system
customer_service_agent = intelligent_customer_service()
```

### 代码生成和审查助手 / Code Generation and Review Assistant

```python
def code_generation_assistant():
    """代码生成和审查助手示例 / Code generation and review assistant example"""

    class CodeAssistant:
        """代码助手 / Code assistant"""

        def __init__(self):
            self.supported_languages = ["python", "javascript", "java", "cpp", "go"]
            self.code_templates = self._load_code_templates()

        def _load_code_templates(self):
            """加载代码模板 / Load code templates"""
            return {
                "python": {
                    "class": """
class {ClassName}:
    def __init__(self, {parameters}):
        {initialization}

    def {method_name}(self, {method_params}):
        {method_body}
""",
                    "function": """
def {function_name}({parameters}):
    \"\"\"
    {docstring}
    \"\"\"
    {function_body}
    return {return_value}
"""
                }
            }

        def generate_code(self, language, task_description, requirements=None):
            """生成代码 / Generate code"""

            requirements_text = ""
            if requirements:
                requirements_text = "\n\n具体要求：\n" + "\n".join(f"- {req}" for req in requirements)

            prompt = f"""
            请用{language}语言生成代码，实现以下功能：

            任务描述：{task_description}{requirements_text}

            要求：
            1. 代码要完整可运行
            2. 包含必要的注释
            3. 遵循{language}的最佳实践
            4. 处理可能的错误情况
            5. 提供使用示例

            请直接输出代码，不要添加多余的解释。
            """

            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1500,
                temperature=0.3,  # 降低温度以获得更准确的代码 / Lower temperature for more accurate code
                system=f"你是一个专业的{language}开发者，擅长编写高质量、可维护的代码。",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            return message.content[0].text

        def review_code(self, code, language):
            """审查代码 / Review code"""

            prompt = f"""
            请审查以下{language}代码：

            ```{language}
            {code}
            ```

            请从以下方面进行审查：
            1. 代码质量和可读性
            2. 性能和效率
            3. 安全性
            4. 最佳实践遵循情况
            5. 潜在的改进建议

            请提供具体的改进建议和修改后的代码示例。
            """

            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1500,
                temperature=0.2,  # 降低温度以获得更准确的审查 / Lower temperature for more accurate review
                system="你是一个经验丰富的代码审查专家，擅长识别代码问题并提供改进建议。",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            return message.content[0].text

        def explain_code(self, code, language):
            """解释代码 / Explain code"""

            prompt = f"""
            请详细解释以下{language}代码的功能和工作原理：

            ```{language}
            {code}
            ```

            请包括：
            1. 代码的整体功能
            2. 关键部分的详细解释
            3. 使用的技术和模式
            4. 可能的改进方向

            请用通俗易懂的语言进行解释。
            """

            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1200,
                temperature=0.5,
                system="你是一个编程导师，擅长用简单易懂的方式解释复杂的代码。",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            return message.content[0].text

    # 创建代码助手 / Create code assistant
    assistant = CodeAssistant()

    # 演示代码生成 / Demonstrate code generation
    print("💻 代码生成和审查助手演示 / Code Generation and Review Assistant Demo")
    print("="*80)

    # 示例1: 生成Python函数 / Example 1: Generate Python function
    print("\n1️⃣ 代码生成示例 / Code Generation Example")
    print("-" * 50)

    generated_code = assistant.generate_code(
        language="python",
        task_description="实现一个计算斐波那契数列第n项的函数",
        requirements=[
            "使用递归方法",
            "包含输入验证",
            "添加详细注释",
            "处理大数情况"
        ]
    )

    print("生成的代码 / Generated Code:")
    print(generated_code)

    # 示例2: 代码审查 / Example 2: Code review
    print("\n2️⃣ 代码审查示例 / Code Review Example")
    print("-" * 50)

    sample_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(10))
"""

    review_result = assistant.review_code(sample_code, "python")
    print("代码审查结果 / Code Review Result:")
    print(review_result)

    # 示例3: 代码解释 / Example 3: Code explanation
    print("\n3️⃣ 代码解释示例 / Code Explanation Example")
    print("-" * 50)

    explanation = assistant.explain_code(sample_code, "python")
    print("代码解释 / Code Explanation:")
    print(explanation)

    return assistant

# 执行代码生成和审查助手 / Execute code generation and review assistant
code_assistant = code_generation_assistant()
```

---

## 最佳实践 / Best Practices

### 🎯 核心最佳实践 / Core Best Practices

#### 1. 模型选择策略 / Model Selection Strategy

**任务复杂度驱动选择 / Task Complexity Driven Selection:**
- **简单任务** (问答、摘要): 使用 Claude 3 Haiku
- **中等任务** (分析、写作): 使用 Claude 3.5 Sonnet
- **复杂任务** (推理、规划): 使用 Claude 3 Opus

**成本效益考虑 / Cost-Benefit Considerations:**
- 评估任务重要性和频率
- 平衡响应质量和成本
- 监控API使用量和费用

#### 2. 提示工程优化 / Prompt Engineering Optimization

**结构化提示设计 / Structured Prompt Design:**
```xml
<optimized_prompt_structure>
  <clear_objective>清晰的目标描述</clear_objective>
  <detailed_context>详细的上下文信息</detailed_context>
  <specific_requirements>具体的质量要求</specific_requirements>
  <output_format>明确的输出格式</output_format>
  <examples>丰富的示例说明</examples>
</optimized_prompt_structure>
```

**提示迭代优化 / Prompt Iteration Optimization:**
- 从简单版本开始
- 基于结果进行迭代改进
- A/B测试不同版本
- 收集用户反馈持续优化

#### 3. 错误处理和监控 / Error Handling and Monitoring

**防御性编程 / Defensive Programming:**
```python
def robust_api_call(user_input):
    try:
        # 输入验证 / Input validation
        validated_input = validate_input(user_input)

        # API调用 / API call
        response = client.messages.create(...)

        # 响应验证 / Response validation
        validated_response = validate_response(response)

        return validated_response

    except ValidationError as e:
        logger.error(f"输入验证失败: {e}")
        return get_fallback_response()

    except APIError as e:
        logger.error(f"API调用失败: {e}")
        return get_degraded_response()

    except Exception as e:
        logger.error(f"未知错误: {e}")
        return get_error_response()
```

**监控和告警 / Monitoring and Alerting:**
- 设置关键指标监控
- 建立异常检测机制
- 配置自动告警通知
- 定期生成健康报告

#### 4. 性能优化实践 / Performance Optimization Practices

**缓存策略 / Caching Strategy:**
- 实现多层缓存体系
- 使用语义缓存减少重复调用
- 设置合理的缓存过期时间
- 监控缓存命中率

**并发和批处理 / Concurrency and Batching:**
```python
import asyncio
from typing import List

async def batch_process_requests(requests: List[dict]) -> List[dict]:
    """批量处理请求 / Batch process requests"""

    # 分批处理避免速率限制 / Process in batches to avoid rate limits
    batch_size = 10
    results = []

    for i in range(0, len(requests), batch_size):
        batch = requests[i:i + batch_size]

        # 并发处理批次 / Process batch concurrently
        tasks = [process_single_request(req) for req in batch]
        batch_results = await asyncio.gather(*tasks)

        results.extend(batch_results)

        # 批次间暂停避免过载 / Pause between batches to avoid overload
        await asyncio.sleep(1)

    return results
```

### 📊 资源管理和成本控制 / Resource Management and Cost Control

#### API使用量监控 / API Usage Monitoring

```python
class APIUsageTracker:
    """API使用量跟踪器 / API Usage Tracker"""

    def __init__(self):
        self.usage_stats = {
            "daily_requests": 0,
            "monthly_tokens": 0,
            "cost_estimate": 0.0
        }
        self.reset_daily_stats()

    def reset_daily_stats(self):
        """重置每日统计 / Reset daily statistics"""
        self.usage_stats["daily_requests"] = 0
        self.usage_stats["daily_tokens"] = 0
        self.usage_stats["daily_cost"] = 0.0

    def track_request(self, tokens_used: int, model: str):
        """跟踪请求 / Track request"""

        self.usage_stats["daily_requests"] += 1
        self.usage_stats["daily_tokens"] += tokens_used

        # 估算成本 / Estimate cost
        cost_per_token = self.get_cost_per_token(model)
        request_cost = tokens_used * cost_per_token
        self.usage_stats["daily_cost"] += request_cost

    def get_cost_per_token(self, model: str) -> float:
        """获取每token成本 / Get cost per token"""
        # Claude模型的估算成本 (美元) / Estimated costs for Claude models (USD)
        costs = {
            "claude-3-haiku-20240307": 0.00025,      # 输入 / Input
            "claude-3-5-sonnet-20241022": 0.0003,    # 输入 / Input
            "claude-3-opus-20240229": 0.0015         # 输入 / Input
        }
        return costs.get(model, 0.0003)  # 默认使用Sonnet的价格 / Default to Sonnet price

    def get_usage_report(self) -> dict:
        """获取使用报告 / Get usage report"""
        return {
            "daily_requests": self.usage_stats["daily_requests"],
            "daily_tokens": self.usage_stats["daily_tokens"],
            "daily_cost_usd": round(self.usage_stats["daily_cost"], 4),
            "avg_tokens_per_request": (
                self.usage_stats["daily_tokens"] / self.usage_stats["daily_requests"]
                if self.usage_stats["daily_requests"] > 0 else 0
            )
        }
```

#### 成本优化策略 / Cost Optimization Strategies

**智能模型选择 / Intelligent Model Selection:**
```python
def select_optimal_model(task_complexity: str, cost_sensitivity: str) -> str:
    """选择最优模型 / Select optimal model"""

    model_matrix = {
        "simple": {
            "cost_sensitive": "claude-3-haiku-20240307",    # 便宜且快 / Cheap and fast
            "quality_focused": "claude-3-5-sonnet-20241022" # 平衡选择 / Balanced choice
        },
        "complex": {
            "cost_sensitive": "claude-3-5-sonnet-20241022", # 性价比高 / Good value
            "quality_focused": "claude-3-opus-20240229"     # 最佳质量 / Best quality
        }
    }

    return model_matrix.get(task_complexity, {}).get(cost_sensitivity, "claude-3-5-sonnet-20241022")
```

### 🔧 调试和故障排除 / Debugging and Troubleshooting

#### 常见问题诊断 / Common Issue Diagnosis

**网络连接问题 / Network Connection Issues:**
```python
def diagnose_connection_issues():
    """诊断连接问题 / Diagnose connection issues"""

    import requests

    try:
        # 测试基本连接 / Test basic connection
        response = requests.get("https://api.anthropic.com", timeout=5)
        print(f"✅ 基本连接正常: {response.status_code}")

        # 测试API端点 / Test API endpoint
        response = requests.get("https://api.anthropic.com/v1/messages", timeout=5)
        print(f"✅ API端点可达: {response.status_code}")

    except requests.exceptions.Timeout:
        print("❌ 连接超时 - 请检查网络连接")
    except requests.exceptions.ConnectionError:
        print("❌ 连接错误 - 请检查防火墙和代理设置")
    except Exception as e:
        print(f"❌ 未知连接错误: {e}")
```

**API错误排查 / API Error Troubleshooting:**

| 错误代码 / Error Code | 可能原因 / Possible Causes | 解决方案 / Solutions |
|----------------------|---------------------------|---------------------|
| 400 | 请求参数错误 | 检查参数格式和值 |
| 401 | API密钥无效 | 验证密钥配置 |
| 429 | 请求过于频繁 | 实施指数退避重试 |
| 500 | 服务器内部错误 | 等待后重试，或联系支持 |
| 529 | 服务过载 | 减少请求频率，实施熔断 |

---

## 📅 开发进度时间表更新规则 / Development Progress Timestamp Update Rules

> **铁律 / Iron Rule**: 每次开发更新时，时间进度表必须使用本机电脑当前的实时日期时间

**最后更新 / Last updated: 2025年09月02日 11:35:28**
**文档版本 / Document version: 1.0.0**
**Claude系列实现示例状态 / Claude Series Implementation Examples Status: 完成 / Completed**
