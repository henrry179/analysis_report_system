# 大模型调用编程规则 / Large Language Model API Calling Rules

> 本文档提供各类大模型API调用的标准规范和最佳实践
> This document provides standard specifications and best practices for calling various large language model APIs

**最后更新 / Last updated: 2025年09月02日 11:09:34**

---

## 📋 目录 / Table of Contents

- [概述 / Overview](#概述--overview)
- [通用调用规则 / General Calling Rules](#通用调用规则--general-calling-rules)
- [OpenAI GPT系列调用规则 / OpenAI GPT Series Calling Rules](#openai-gpt系列调用规则--openai-gpt-series-calling-rules)
- [Anthropic Claude调用规则 / Anthropic Claude Calling Rules](#anthropic-claude调用规则--anthropic-claude-calling-rules)
- [Google Gemini调用规则 / Google Gemini Calling Rules](#google-gemini调用规则--google-gemini-calling-rules)
- [国产模型调用规则 / Domestic Model Calling Rules](#国产模型调用规则--domestic-model-calling-rules)
- [错误处理策略 / Error Handling Strategies](#错误处理策略--error-handling-strategies)
- [性能优化技巧 / Performance Optimization Techniques](#性能优化技巧--performance-optimization-techniques)
- [安全和合规要求 / Security and Compliance Requirements](#安全和合规要求--security-and-compliance-requirements)

---

## 概述 / Overview

### 设计目标 / Design Goals

大模型调用编程规则旨在提供统一的API调用标准，确保：
- **可靠性**: 稳定的服务调用和错误恢复
- **效率**: 优化的性能和资源使用
- **安全性**: 保护数据和API密钥安全
- **可维护性**: 清晰的代码结构和文档

The large language model calling programming rules aim to provide unified API calling standards to ensure:
- **Reliability**: Stable service calls and error recovery
- **Efficiency**: Optimized performance and resource usage
- **Security**: Protection of data and API key security
- **Maintainability**: Clear code structure and documentation

---

## 通用调用规则 / General Calling Rules

### 🔧 1. API客户端架构 / API Client Architecture

#### 标准化客户端设计 / Standardized Client Design

```xml
<api_client_architecture>
  <client_structure>
    <!-- 客户端结构 / Client structure -->
    <configuration_layer>配置层 / Configuration layer</configuration_layer>
    <authentication_layer>认证层 / Authentication layer</authentication_layer>
    <request_layer>请求层 / Request layer</request_layer>
    <response_layer>响应层 / Response layer</response_layer>
    <error_handling_layer>错误处理层 / Error handling layer</error_handling_layer>
  </client_structure>

  <abstraction_requirements>
    <!-- 抽象化要求 / Abstraction requirements -->
    <model_abstraction>模型抽象 / Model abstraction</model_abstraction>
    <provider_abstraction>提供商抽象 / Provider abstraction</provider_abstraction>
    <interface_unification>接口统一 / Interface unification</interface_unification>
  </abstraction_requirements>
</api_client_architecture>
```

#### 客户端实现示例 / Client Implementation Example

```python
# 统一的API客户端接口 / Unified API client interface
class LLMClient(ABC):
    @abstractmethod
    async def chat_completion(self, messages: List[Dict], **kwargs) -> Dict:
        """统一的聊天完成接口 / Unified chat completion interface"""
        pass

    @abstractmethod
    async def stream_completion(self, messages: List[Dict], **kwargs) -> AsyncGenerator:
        """统一的流式响应接口 / Unified streaming response interface"""
        pass
```

### 🔐 2. 认证和授权 / Authentication and Authorization

#### API密钥管理 / API Key Management

```xml
<authentication_management>
  <key_storage>
    <!-- 密钥存储策略 / Key storage strategy -->
    <environment_variables>环境变量存储 / Environment variables</environment_variables>
    <secure_vaults>安全保管库 / Secure vaults</secure_vaults>
    <key_rotation>密钥轮换机制 / Key rotation mechanism</key_rotation>
  </key_storage>

  <access_control>
    <!-- 访问控制 / Access control -->
    <rate_limiting>速率限制 / Rate limiting</rate_limiting>
    <quota_management>配额管理 / Quota management</quota_management>
    <usage_monitoring>使用监控 / Usage monitoring</usage_monitoring>
  </access_control>
</authentication_management>
```

#### 安全最佳实践 / Security Best Practices

```python
# 安全的API密钥管理 / Secure API key management
class SecureAPIKeyManager:
    def __init__(self):
        self._keys = {}
        self._load_keys_from_secure_storage()

    def get_key(self, provider: str) -> str:
        """安全获取API密钥 / Securely get API key"""
        if provider not in self._keys:
            raise ValueError(f"API key for {provider} not found")
        return self._decrypt_key(self._keys[provider])

    def rotate_key(self, provider: str, new_key: str):
        """轮换API密钥 / Rotate API key"""
        self._validate_key_format(provider, new_key)
        encrypted_key = self._encrypt_key(new_key)
        self._keys[provider] = encrypted_key
        self._save_keys_to_secure_storage()
```

### 📊 3. 请求构建规范 / Request Construction Standards

#### 消息格式标准化 / Message Format Standardization

```xml
<message_formatting>
  <standard_structure>
    <!-- 标准消息结构 / Standard message structure -->
    <role_field>角色字段 / Role field</role_field>
    <content_field>内容字段 / Content field</content_field>
    <metadata_field>元数据字段 / Metadata field</metadata_field>
  </standard_structure>

  <content_types>
    <!-- 内容类型 / Content types -->
    <text_content>文本内容 / Text content</text_content>
    <multimodal_content>多模态内容 / Multimodal content</multimodal_content>
    <structured_content>结构化内容 / Structured content</structured_content>
  </content_types>
</message_formatting>
```

#### 请求参数验证 / Request Parameter Validation

```python
# 请求参数验证器 / Request parameter validator
class RequestValidator:
    @staticmethod
    def validate_messages(messages: List[Dict]) -> bool:
        """验证消息格式 / Validate message format"""
        if not isinstance(messages, list) or not messages:
            return False

        for msg in messages:
            if not isinstance(msg, dict):
                return False
            if 'role' not in msg or 'content' not in msg:
                return False
            if msg['role'] not in ['system', 'user', 'assistant']:
                return False
            if not isinstance(msg['content'], str) or not msg['content'].strip():
                return False
        return True

    @staticmethod
    def validate_parameters(**kwargs) -> Dict:
        """验证并规范化参数 / Validate and normalize parameters"""
        validated = {}

        # 温度参数验证 / Temperature parameter validation
        if 'temperature' in kwargs:
            temp = kwargs['temperature']
            if not isinstance(temp, (int, float)) or not 0 <= temp <= 2:
                raise ValueError("Temperature must be between 0 and 2")
            validated['temperature'] = float(temp)

        # 最大token验证 / Max tokens validation
        if 'max_tokens' in kwargs:
            max_t = kwargs['max_tokens']
            if not isinstance(max_t, int) or max_t <= 0:
                raise ValueError("Max tokens must be a positive integer")
            validated['max_tokens'] = max_t

        return validated
```

---

## OpenAI GPT系列调用规则 / OpenAI GPT Series Calling Rules

### 🎯 4. GPT模型调用规范 / GPT Model Calling Standards

#### 模型选择策略 / Model Selection Strategy

```xml
<gpt_model_selection>
  <model_mapping>
    <!-- 模型映射 / Model mapping -->
    <gpt-4-turbo>GPT-4 Turbo - 复杂任务 / Complex tasks</gpt-4-turbo>
    <gpt-4>GPT-4 - 高质量输出 / High-quality output</gpt-4>
    <gpt-3.5-turbo>GPT-3.5 Turbo - 快速响应 / Fast response</gpt-3.5-turbo>
  </model_mapping>

  <task_model_matching>
    <!-- 任务模型匹配 / Task-model matching -->
    <creative_tasks>创意任务 - GPT-4 / Creative tasks - GPT-4</creative_tasks>
    <analytical_tasks>分析任务 - GPT-4 / Analytical tasks - GPT-4</analytical_tasks>
    <simple_tasks>简单任务 - GPT-3.5 / Simple tasks - GPT-3.5</simple_tasks>
  </task_model_matching>
</gpt_model_selection>
```

#### GPT-4最佳实践 / GPT-4 Best Practices

```python
# GPT-4调用最佳实践 / GPT-4 calling best practices
class GPT4Client:
    async def optimized_completion(self, messages: List[Dict], task_type: str) -> Dict:
        """优化的GPT-4调用 / Optimized GPT-4 call"""
        # 根据任务类型调整参数 / Adjust parameters based on task type
        params = self._get_task_specific_params(task_type)

        # 使用JSON模式进行结构化输出 / Use JSON mode for structured output
        if task_type in ['analysis', 'classification']:
            params['response_format'] = {'type': 'json_object'}

        # 启用并行函数调用 / Enable parallel function calling
        if task_type == 'multi_step':
            params['parallel_tool_calls'] = True

        response = await self._call_openai_api(messages, **params)
        return self._process_response(response)

    def _get_task_specific_params(self, task_type: str) -> Dict:
        """获取任务特定参数 / Get task-specific parameters"""
        base_params = {
            'model': 'gpt-4-turbo-preview',
            'temperature': 0.7,
            'max_tokens': 2000
        }

        task_configs = {
            'creative': {'temperature': 0.9, 'max_tokens': 3000},
            'analytical': {'temperature': 0.1, 'max_tokens': 1500},
            'conversational': {'temperature': 0.7, 'max_tokens': 1000},
            'coding': {'temperature': 0.2, 'max_tokens': 4000}
        }

        return {**base_params, **task_configs.get(task_type, {})}
```

### 🔄 5. 流式响应处理 / Streaming Response Handling

#### 流式调用实现 / Streaming Implementation

```python
# 流式响应处理器 / Streaming response handler
class StreamingHandler:
    async def handle_streaming_response(self, response_stream):
        """处理流式响应 / Handle streaming response"""
        accumulated_content = ""
        last_chunk_time = time.time()

        async for chunk in response_stream:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                accumulated_content += content

                # 实时处理内容 / Process content in real-time
                await self._process_chunk(content)

                # 检查响应超时 / Check for response timeout
                if time.time() - last_chunk_time > self.timeout_threshold:
                    await self._handle_timeout()
                    break

                last_chunk_time = time.time()

            # 处理函数调用 / Handle function calls
            if chunk.choices[0].delta.tool_calls:
                await self._handle_tool_calls(chunk.choices[0].delta.tool_calls)

        return accumulated_content

    async def _process_chunk(self, content: str):
        """处理内容块 / Process content chunk"""
        # 实时语法检查 / Real-time syntax checking
        # 内容过滤 / Content filtering
        # 用户界面更新 / UI updates
        pass
```

---

## Anthropic Claude调用规则 / Anthropic Claude Calling Rules

### 🧠 6. Claude模型特性 / Claude Model Characteristics

#### Claude优势和应用场景 / Claude Advantages and Use Cases

```xml
<claude_model_characteristics>
  <strengths>
    <!-- Claude优势 / Claude strengths -->
    <long_context>长上下文理解 / Long context understanding</long_context>
    <ethical_reasoning>伦理推理能力 / Ethical reasoning ability</ethical_reasoning>
    <instruction_following>指令遵循性 / Instruction following</instruction_following>
  </strengths>

  <optimal_use_cases>
    <!-- 最优应用场景 / Optimal use cases -->
    <complex_analysis>复杂分析任务 / Complex analysis tasks</complex_analysis>
    <creative_writing>创意写作 / Creative writing</creative_writing>
    <code_review>代码审查 / Code review</code_review>
  </optimal_use_cases>
</claude_model_characteristics>
```

#### Claude调用最佳实践 / Claude Calling Best Practices

```python
# Claude调用优化 / Claude calling optimization
class ClaudeClient:
    async def optimized_call(self, messages: List[Dict], task_type: str) -> Dict:
        """优化的Claude调用 / Optimized Claude call"""
        # Claude特定的提示格式 / Claude-specific prompt formatting
        formatted_messages = self._format_claude_messages(messages)

        params = {
            'model': 'claude-3-opus-20240229',
            'max_tokens': 4096,
            'system': self._get_system_prompt(task_type)
        }

        # 根据任务调整参数 / Adjust parameters based on task
        if task_type == 'creative':
            params['temperature'] = 0.8
        elif task_type == 'analytical':
            params['temperature'] = 0.1

        response = await self._call_anthropic_api(formatted_messages, **params)
        return self._parse_claude_response(response)

    def _format_claude_messages(self, messages: List[Dict]) -> str:
        """格式化Claude消息 / Format Claude messages"""
        formatted = []

        for msg in messages:
            if msg['role'] == 'system':
                # Claude使用system参数 / Claude uses system parameter
                continue
            elif msg['role'] == 'user':
                formatted.append(f"Human: {msg['content']}")
            elif msg['role'] == 'assistant':
                formatted.append(f"Assistant: {msg['content']}")

        return "\n\n".join(formatted) + "\n\nAssistant:"
```

---

## Google Gemini调用规则 / Google Gemini Calling Rules

### 🌟 7. Gemini多模态特性 / Gemini Multimodal Features

#### 多模态集成 / Multimodal Integration

```xml
<gemini_multimodal>
  <supported_modalities>
    <!-- 支持的模态 / Supported modalities -->
    <text_modality>文本模态 / Text modality</text_modality>
    <image_modality>图像模态 / Image modality</image_modality>
    <audio_modality>音频模态 / Audio modality</audio_modality>
    <video_modality>视频模态 / Video modality</video_modality>
  </supported_modalities>

  <integration_patterns>
    <!-- 集成模式 / Integration patterns -->
    <text_only>纯文本模式 / Text-only mode</text_only>
    <image_text>图文混合 / Image-text hybrid</image_text>
    <multimodal_chain>多模态链式调用 / Multimodal chain calling</multimodal_chain>
  </integration_patterns>
</gemini_multimodal>
```

#### Gemini调用实现 / Gemini Calling Implementation

```python
# Gemini多模态调用 / Gemini multimodal calling
class GeminiClient:
    async def multimodal_completion(self, content: List[Dict]) -> Dict:
        """多模态内容完成 / Multimodal content completion"""
        # 构建多模态内容 / Build multimodal content
        multimodal_content = []

        for item in content:
            if item['type'] == 'text':
                multimodal_content.append({
                    'text': item['content']
                })
            elif item['type'] == 'image':
                # 处理图像输入 / Process image input
                image_data = await self._process_image(item['content'])
                multimodal_content.append({
                    'inline_data': {
                        'mime_type': image_data['mime_type'],
                        'data': image_data['base64_data']
                    }
                })

        # 调用Gemini API / Call Gemini API
        response = await self._call_gemini_api(multimodal_content)
        return self._parse_gemini_response(response)
```

---

## 国产模型调用规则 / Domestic Model Calling Rules

### 🇨🇳 8. 国内模型集成 / Domestic Model Integration

#### 支持的国产模型 / Supported Domestic Models

```xml
<domestic_models>
  <supported_providers>
    <!-- 支持的提供商 / Supported providers -->
    <baidu_ernie>百度文心一言 / Baidu Ernie</baidu_ernie>
    <alibaba_qwen>阿里通义千问 / Alibaba Qwen</alibaba_qwen>
    <tencent_hunyuan>腾讯混元 / Tencent Hunyuan</tencent_hunyuan>
    <iflytek_spark>科大讯飞星火 / iFlyTek Spark</iflytek_spark>
  </supported_providers>

  <integration_requirements>
    <!-- 集成要求 / Integration requirements -->
    <api_compatibility>API兼容性 / API compatibility</api_compatibility>
    <data_compliance>数据合规性 / Data compliance</data_compliance>
    <performance_optimization>性能优化 / Performance optimization</performance_optimization>
  </integration_requirements>
</domestic_models>
```

#### 统一接口适配器 / Unified Interface Adapter

```python
# 国产模型统一适配器 / Domestic model unified adapter
class DomesticModelAdapter:
    def __init__(self, provider: str, config: Dict):
        self.provider = provider
        self.config = config
        self._initialize_client()

    async def unified_call(self, messages: List[Dict], **kwargs) -> Dict:
        """统一的国产模型调用接口 / Unified domestic model calling interface"""
        # 标准化消息格式 / Standardize message format
        standardized_messages = self._standardize_messages(messages)

        # 适配提供商特定参数 / Adapt provider-specific parameters
        adapted_params = self._adapt_parameters(kwargs)

        # 调用具体实现 / Call specific implementation
        if self.provider == 'baidu':
            return await self._call_ernie(standardized_messages, adapted_params)
        elif self.provider == 'alibaba':
            return await self._call_qwen(standardized_messages, adapted_params)
        elif self.provider == 'tencent':
            return await self._call_hunyuan(standardized_messages, adapted_params)

        raise ValueError(f"Unsupported provider: {self.provider}")

    def _standardize_messages(self, messages: List[Dict]) -> List[Dict]:
        """标准化消息格式 / Standardize message format"""
        # 转换不同提供商的消息格式 / Convert message formats for different providers
        pass
```

---

## 错误处理策略 / Error Handling Strategies

### 🚨 9. 异常分类和处理 / Exception Classification and Handling

#### 错误类型定义 / Error Type Definitions

```xml
<error_classification>
  <network_errors>
    <!-- 网络错误 / Network errors -->
    <connection_timeout>连接超时 / Connection timeout</connection_timeout>
    <dns_resolution>DNS解析失败 / DNS resolution failure</dns_resolution>
    <ssl_errors>SSL证书错误 / SSL certificate errors</ssl_errors>
  </network_errors>

  <api_errors>
    <!-- API错误 / API errors -->
    <rate_limit_exceeded>速率限制超限 / Rate limit exceeded</rate_limit_exceeded>
    <quota_exceeded>配额用尽 / Quota exceeded</quota_exceeded>
    <invalid_request>无效请求 / Invalid request</invalid_request>
  </api_errors>

  <content_errors>
    <!-- 内容错误 / Content errors -->
    <content_filter>内容过滤 / Content filtering</content_filter>
    <safety_violation>安全违规 / Safety violation</safety_violation>
    <model_limitations>模型限制 / Model limitations</model_limitations>
  </content_errors>
</error_classification>
```

#### 错误处理框架 / Error Handling Framework

```python
# 统一的错误处理框架 / Unified error handling framework
class APIErrorHandler:
    async def handle_api_call(self, api_call_func, *args, **kwargs):
        """处理API调用的错误 / Handle API call errors"""
        retry_count = 0
        max_retries = self.config.get('max_retries', 3)

        while retry_count < max_retries:
            try:
                return await api_call_func(*args, **kwargs)
            except NetworkError as e:
                await self._handle_network_error(e, retry_count)
            except RateLimitError as e:
                await self._handle_rate_limit_error(e, retry_count)
            except APIError as e:
                await self._handle_api_error(e, retry_count)
            except Exception as e:
                await self._handle_unexpected_error(e, retry_count)

            retry_count += 1
            if retry_count < max_retries:
                await asyncio.sleep(self._calculate_backoff_delay(retry_count))

        # 所有重试都失败 / All retries failed
        return await self._execute_fallback_strategy()

    async def _handle_rate_limit_error(self, error, retry_count):
        """处理速率限制错误 / Handle rate limit error"""
        # 解析重试时间 / Parse retry time
        retry_after = self._parse_retry_after(error)

        # 记录日志 / Log the event
        logger.warning(f"Rate limit exceeded, retrying after {retry_after}s")

        # 等待重试 / Wait for retry
        await asyncio.sleep(retry_after)
```

### 🔄 10. 重试和回退策略 / Retry and Fallback Strategies

#### 智能重试机制 / Intelligent Retry Mechanism

```python
# 智能重试策略 / Intelligent retry strategy
class IntelligentRetryStrategy:
    def __init__(self):
        self.retry_delays = [1, 2, 4, 8, 16]  # 指数退避 / Exponential backoff
        self.jitter_factor = 0.1  # 抖动因子 / Jitter factor

    def should_retry(self, error: Exception, attempt: int) -> bool:
        """判断是否应该重试 / Determine if should retry"""
        if attempt >= len(self.retry_delays):
            return False

        # 根据错误类型判断 / Judge based on error type
        if isinstance(error, (ConnectionError, TimeoutError)):
            return True
        elif isinstance(error, RateLimitError):
            return True
        elif isinstance(error, ServerError) and error.status_code >= 500:
            return True

        return False

    def get_retry_delay(self, attempt: int) -> float:
        """获取重试延迟 / Get retry delay"""
        if attempt >= len(self.retry_delays):
            return self.retry_delays[-1]

        delay = self.retry_delays[attempt]
        # 添加抖动避免惊群效应 / Add jitter to avoid thundering herd
        jitter = delay * self.jitter_factor * random.random()
        return delay + jitter
```

---

## 性能优化技巧 / Performance Optimization Techniques

### ⚡ 11. 缓存策略 / Caching Strategies

#### 多层缓存架构 / Multi-Level Caching Architecture

```xml
<caching_architecture>
  <cache_layers>
    <!-- 缓存层级 / Cache layers -->
    <memory_cache>内存缓存 / Memory cache</memory_cache>
    <distributed_cache>分布式缓存 / Distributed cache</distributed_cache>
    <persistent_cache>持久化缓存 / Persistent cache</persistent_cache>
  </cache_layers>

  <cache_strategies>
    <!-- 缓存策略 / Cache strategies -->
    <semantic_cache>语义缓存 / Semantic caching</semantic_cache>
    <response_cache>响应缓存 / Response caching</response_cache>
    <embedding_cache>嵌入缓存 / Embedding caching</embedding_cache>
  </cache_strategies>
</caching_architecture>
```

#### 语义缓存实现 / Semantic Caching Implementation

```python
# 语义缓存系统 / Semantic caching system
class SemanticCache:
    def __init__(self, embedding_model, similarity_threshold=0.85):
        self.embedding_model = embedding_model
        self.similarity_threshold = similarity_threshold
        self.cache = {}

    async def get_cached_response(self, query: str) -> Optional[str]:
        """获取缓存的响应 / Get cached response"""
        # 生成查询嵌入 / Generate query embedding
        query_embedding = await self._get_embedding(query)

        # 查找相似查询 / Find similar queries
        best_match = None
        best_similarity = 0

        for cached_query, (embedding, response) in self.cache.items():
            similarity = self._calculate_similarity(query_embedding, embedding)
            if similarity > best_similarity and similarity >= self.similarity_threshold:
                best_similarity = similarity
                best_match = response

        return best_match

    async def cache_response(self, query: str, response: str):
        """缓存响应 / Cache response"""
        query_embedding = await self._get_embedding(query)
        self.cache[query] = (query_embedding, response)

        # 清理过期缓存 / Clean up expired cache
        if len(self.cache) > self.max_cache_size:
            await self._cleanup_cache()
```

### 📊 12. 请求批处理和并发控制 / Request Batching and Concurrency Control

#### 批量请求优化 / Batch Request Optimization

```python
# 请求批处理器 / Request batch processor
class BatchRequestProcessor:
    def __init__(self, batch_size=10, max_wait_time=1.0):
        self.batch_size = batch_size
        self.max_wait_time = max_wait_time
        self.request_queue = asyncio.Queue()
        self.processing_task = None

    async def add_request(self, request: Dict) -> asyncio.Future:
        """添加请求到批处理队列 / Add request to batch processing queue"""
        future = asyncio.Future()
        await self.request_queue.put((request, future))

        # 启动批处理任务 / Start batch processing task
        if self.processing_task is None or self.processing_task.done():
            self.processing_task = asyncio.create_task(self._process_batch())

        return future

    async def _process_batch(self):
        """处理请求批次 / Process request batch"""
        while True:
            batch = []
            start_time = time.time()

            # 收集批次请求 / Collect batch requests
            while len(batch) < self.batch_size:
                try:
                    # 设置超时 / Set timeout
                    request, future = await asyncio.wait_for(
                        self.request_queue.get(),
                        timeout=self.max_wait_time
                    )
                    batch.append((request, future))
                except asyncio.TimeoutError:
                    break

                # 检查等待时间 / Check wait time
                if time.time() - start_time >= self.max_wait_time:
                    break

            if not batch:
                break

            # 批量处理请求 / Process batch requests
            try:
                responses = await self._execute_batch([req for req, _ in batch])
                for (request, future), response in zip(batch, responses):
                    future.set_result(response)
            except Exception as e:
                # 处理批处理错误 / Handle batch processing error
                for request, future in batch:
                    future.set_exception(e)
```

---

## 安全和合规要求 / Security and Compliance Requirements

### 🔒 13. 数据保护和隐私 / Data Protection and Privacy

#### 数据处理安全 / Data Processing Security

```xml
<data_security>
  <encryption_standards>
    <!-- 加密标准 / Encryption standards -->
    <data_in_transit>传输中数据加密 / Data in transit encryption</data_in_transit>
    <data_at_rest>静态数据加密 / Data at rest encryption</data_at_rest>
    <key_management>密钥管理 / Key management</key_management>
  </encryption_standards>

  <privacy_protection>
    <!-- 隐私保护 / Privacy protection -->
    <data_minimization>数据最小化 / Data minimization</data_minimization>
    <consent_management>同意管理 / Consent management</consent_management>
    <right_to_be_forgotten>被遗忘权 / Right to be forgotten</right_to_be_forgotten>
  </privacy_protection>
</data_security>
```

#### 合规检查清单 / Compliance Checklist

```python
# 合规检查器 / Compliance checker
class ComplianceChecker:
    def __init__(self):
        self.compliance_rules = self._load_compliance_rules()

    def check_request_compliance(self, request: Dict) -> ComplianceResult:
        """检查请求合规性 / Check request compliance"""
        result = ComplianceResult()

        # 检查数据内容 / Check data content
        if self._contains_sensitive_data(request):
            result.add_violation("Sensitive data detected")

        # 检查地理位置限制 / Check geographic restrictions
        if self._violates_geo_restrictions(request):
            result.add_violation("Geographic restriction violation")

        # 检查内容安全 / Check content safety
        if self._contains_harmful_content(request):
            result.add_violation("Harmful content detected")

        return result

    def check_response_compliance(self, response: Dict) -> ComplianceResult:
        """检查响应合规性 / Check response compliance"""
        result = ComplianceResult()

        # 检查输出内容 / Check output content
        if self._contains_disallowed_content(response):
            result.add_violation("Disallowed content in response")

        # 检查数据泄露 / Check data leakage
        if self._contains_data_leakage(response):
            result.add_violation("Potential data leakage")

        return result
```

---

## 📅 开发进度时间表更新规则 / Development Progress Timestamp Update Rules

> **铁律 / Iron Rule**: 每次开发更新时，时间进度表必须使用本机电脑当前的实时日期时间

**最后更新 / Last updated: 2025年09月02日 11:09:34**
**文档版本 / Document version: 1.0.0**
