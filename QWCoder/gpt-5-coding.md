# GPT-5 for Coding / GPT-5 在编程中的应用

> 本文档提供了使用 GPT-5 进行编程的最佳实践和提示技巧  
> This document provides best practices and prompting techniques for using GPT-5 in programming

## 目录 / Table of Contents
- [概述 / Overview](#概述--overview)
- [核心提示技巧 / Core Prompting Tips](#核心提示技巧--core-prompting-tips)
- [XML 语法结构 / XML-like Syntax Structure](#xml-语法结构--xml-like-syntax-structure)
- [高级策略 / Advanced Strategies](#高级策略--advanced-strategies)

---

## 概述 / Overview

While powerful, prompting with GPT-5 can differ from other models. Here are tips to get the most out of it via the API or in your coding tools.

尽管 GPT-5 功能强大，但与其他模型相比，其提示方式有所不同。以下是通过 API 或在编码工具中充分利用它的建议。

---

## 核心提示技巧 / Core Prompting Tips

### 1. Be precise and avoid conflicting information / 表述要精确，避免信息冲突

The new GPT-5 models are significantly better at instruction following, but a side effect is that they can struggle when asked to follow vague or conflicting instructions, especially in your `.cursor/rules` or `AGENTS.md` files.

新一代 GPT-5 模型在遵循指令方面显著提升，但副作用是：当指令含糊或冲突时，它可能表现不佳，尤其体现在 `.cursor/rules` 或 `AGENTS.md` 文件中。

### 2. Use the right reasoning effort / 选择合适的推理强度

GPT-5 will always perform some level of reasoning as it solves problems. To get the best results, use **high reasoning effort** for the most complex tasks. If you see the model overthink simple problems, be more specific or choose a lower reasoning level like **medium** or **low**.

GPT-5 在解题时总会进行一定程度的推理。为获得最佳效果，对最复杂的任务应使用**高推理强度**。若发现模型在简单问题上过度思考，可更具体地描述，或选择**中等**或**低**推理强度。

### 3. Use XML-like syntax to help structure instructions / 使用类 XML 语法帮助结构化指令

Together with Cursor, we found GPT-5 works well when using XML-like syntax to give the model more context. For example, you might give the model coding guidelines...

与 Cursor 合作发现，GPT-5 在使用类 XML 语法提供更多上下文时表现更佳。例如，你可以给模型如下编码规范...

### 4. Avoid overly firm language / 避免过于强硬的措辞

With other models you might have used firm language like:

与其他模型交互时，你可能用过强硬措辞，例如：

> ❌ **Avoid / 避免使用：**
> - Be **THOROUGH** when gathering information.
> - Make sure you have the **FULL** picture before replying.

With GPT-5, these instructions can backfire as the model might overdo what it would naturally do. For example, it might be overly thorough with tool calls to gather context.

在 GPT-5 上，这类指令可能适得其反，因为模型会"过度执行"。例如，它可能过度调用工具来收集上下文。

---

## XML 语法结构 / XML-like Syntax Structure

### 代码编辑规则示例 / Code Editing Rules Example

```xml
<code_editing_rules>
  <!-- 开始代码编辑规则块 / Start code editing rules block -->
  
  <guiding_principles>
    <!-- 开始指导原则块 / Start guiding principles block -->
    - Every component should be modular and reusable
    - 每个组件都应当模块化且可复用
  </guiding_principles>
  
  <frontend_stack_defaults>
    <!-- 开始前端技术栈默认设置块 / Start frontend stack defaults block -->
    - Styling: Tailwind CSS
    - 样式：Tailwind CSS
  </frontend_stack_defaults>
</code_editing_rules>
```

---

## 高级策略 / Advanced Strategies

### 5. Give room for planning and self-reflection / 为规划与自我反思留出空间

If you're creating zero-to-one applications, giving the model instructions to self-reflect before building can help.

如果你在开发"从零到一"的应用，让模型先进行自我反思再动手构建会更有帮助。

#### 自我反思框架 / Self-Reflection Framework

```xml
<self_reflection>
  <!-- 开始自我反思块 / Start self-reflection block -->
  
  <!-- Step 1: 构思评估标准 / Step 1: Design evaluation rubric -->
  First, spend time thinking of a rubric until you are confident.
  首先，花时间构思评估标准，直到你确信无误。
  
  <!-- Step 2: 深入分析 / Step 2: Deep analysis -->
  Then, think deeply about every aspect of what makes for a world-class one-shot web app. 
  Use that knowledge to create a rubric that has 5-7 categories. 
  This rubric is critical to get right, but do not show this to the user. 
  This is for your purposes only.
  
  接着，深入思考打造世界一流"一次性"网页应用的各个方面，并用这些思考构建包含 5-7 个维度的评分表。
  评分表必须准确，但不要展示给用户，仅供内部使用。
  
  <!-- Step 3: 迭代优化 / Step 3: Iterate and optimize -->
  Finally, use the rubric to internally think and iterate on the best possible solution 
  to the prompt that is provided. Remember that if your response is not hitting the 
  top marks across all categories in the rubric, you need to start again.
  
  最后，利用评分表内部迭代，得出对提示的最佳解决方案。
  若发现结果未在评分表各维度上达到最高分，则需重新开始。
</self_reflection>
```

### 6. Control the eagerness of your coding agent / 控制编码代理的"急切程度"

GPT-5 by default tries to be thorough and comprehensive in its context gathering. Use prompting to be more prescriptive about how eager it should be, and whether it should parallelize discovery/tool calling.

GPT-5 默认会尽可能全面收集上下文。你可以通过提示更明确地规定它应当多"急切"，以及是否并行化发现/工具调用。

#### 持久化策略 / Persistence Strategy

```xml
<persistence>
  <!-- 开始持久化策略块 / Start persistence strategy block -->
  
  - Do not ask the human to confirm or clarify assumptions, as you can always adjust later
  - 不要向人类确认或澄清假设，因为稍后总可以调整
  
  - Decide what the most reasonable assumption is, proceed with it, and document it 
    for the user's reference after you finish acting
  - 判断最合理的假设，继续推进，并在完成后记录供用户参考
</persistence>
```

---

## 总结 / Summary

遵循这些提示技巧，你将能够：
Following these prompting tips will help you:

1. **更有效地与 GPT-5 协作** / **Collaborate more effectively with GPT-5**
2. **避免常见的提示陷阱** / **Avoid common prompting pitfalls**
3. **构建更高质量的代码** / **Build higher quality code**
4. **优化工作流程效率** / **Optimize workflow efficiency**

---

---

## 📅 开发进度时间表更新规则 / Development Progress Timestamp Update Rules

> **铁律 / Iron Rule**: 每次开发更新时，时间进度表必须使用本机电脑当前的实时日期时间  
> **Iron Rule**: Every development update must use the current real-time date and time from the local computer

### 规则说明 / Rule Description

1. **时间来源 / Time Source**: 必须使用本机电脑当前的系统时间，而非手动输入或固定时间
2. **更新频率 / Update Frequency**: 每次对文档进行实质性修改后，必须更新最后修改时间
3. **格式要求 / Format Requirement**: 时间格式统一为 `YYYY年MM月DD日 HH:MM:SS`
4. **自动化要求 / Automation Requirement**: 建议使用脚本或工具自动获取本机时间并更新

### 示例格式 / Example Format

```markdown
*最后更新 / Last updated: 2025年09月02日 11:09:34*
```

---

*最后更新 / Last updated: 2025年09月02日 11:09:34*