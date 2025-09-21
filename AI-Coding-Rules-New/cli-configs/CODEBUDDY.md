# AI-Coding-rules 项目指南 / AI-Coding-rules Project Guide

## 项目概览 / Project Overview
本仓库是一个全面的AI编码规则和最佳实践文档集合。它提供了与各种AI模型（包括GPT-5、Claude、Gemini和开源模型）协作的标准化指南。

This repository is a comprehensive collection of AI coding rules and best practices documentation. It provides standardized guidelines for working with various AI models including GPT-5, Claude, Gemini, and open-source models.

## 关键开发命令 / Key Development Commands

### Git 操作 / Git Operations
```bash
git status                    # 检查仓库状态 / Check repository status
git add .                     # 暂存所有更改 / Stage all changes
git commit -m "message"       # 提交更改 / Commit changes
git push                      # 推送到远程 / Push to remote
```

### 时间管理（关键规则）/ Time Management (Critical Rule)
所有文档必须使用当前本地系统时间格式：`YYYY年MM月DD日 HH:MM:SS`
All documentation must use the current local system time format: `YYYY年MM月DD日 HH:MM:SS`
- **铁律 / Iron Rule**: 使用本地计算机系统的实时时间 / Use real-time from local computer system
- **更新频率 / Update Frequency**: 每次实质性更改后 / After every substantive change
- **格式要求 / Format**: 严格遵守 `YYYY年MM月DD日 HH:MM:SS` / Strict adherence to `YYYY年MM月DD日 HH:MM:SS`

## 项目架构 / Project Architecture

### 核心文档结构 / Core Documentation Structure
- **模型特定规则 / Model-specific rules**: GPT-5、Claude、Gemini、DeepSeek、Llama等
- **技术实践 / Technical practices**: 设计原则、API标准、评估框架
- **工程工作流 / Engineering workflows**: 复杂的TODO管理系统
- **学习资源 / Learning resources**: 从新手到专家的渐进式学习路径

### 关键文档文件 / Key Documentation Files
- `README.md`: 主要项目概览，包含集成的TODO管理系统
- `gpt-5-coding.md`: GPT-5特定的提示技术和XML语法
- `design-principles.md`: 核心AI编程设计原则
- `todoschecklist.md`: 详细的TODO管理标准
- `evaluation-framework.md`: 质量评估标准
- `prompt-engineering.md`: 专业提示工程技术
- `api-calling-rules.md`: 标准API调用规范

### 复杂的TODO管理系统 / Sophisticated TODO Management System
项目使用高级的TODO系统，包含：
- **原子性原则 / Atomicity Principle**: 每个TODO都是不可分割的独立任务
- **状态唯一性 / Status Uniqueness**: 任何时候只有一个任务处于`in_progress`状态
- **优先级层次 / Priority Hierarchy**: P0（紧急）到P3（低优先级）系统
- **自动时间戳 / Automated Time Stamping**: 实时本地系统时间更新
- **进度分析 / Progress Analytics**: 完成百分比跟踪和指标

## 开发工作流 / Development Workflow

1. **时间合规性 / Time Compliance**: 始终使用当前本地系统时间进行更新
2. **文档标准 / Documentation Standards**: 遵循XML-like语法处理结构化内容
3. **双语内容 / Bilingual Content**: 维护中英文并行的章节
4. **TODO集成 / TODO Integration**: 系统性地更新README.md的TODO部分
5. **质量保证 / Quality Assurance**: 遵守评估框架标准

### XML语法结构（GPT-5关键）/ XML Syntax Structure (Critical for GPT-5)
使用XML-like语法进行结构化指令：
Use XML-like syntax for structured instructions:
```xml
<component_rules>
  <guiding_principles>
    - Every component should be modular and reusable
    - 每个组件都应当模块化且可复用
  </guiding_principles>
</component_rules>
```

## 本仓库的最佳实践 / Best Practices for This Repository

### 设计原则（来自design-principles.md）/ Design Principles (from design-principles.md)
- **以用户为中心的设计 / User-Centric Design**: AI服务于用户目标，而非技术本身
- **可靠性优先 / Reliability First**: 稳定性优于功能丰富性
- **可扩展性设计 / Scalability Design**: 平稳处理增长和扩展
- **分层架构 / Layered Architecture**: 分离AI逻辑、业务逻辑和用户界面
- **AI服务抽象 / AI Service Abstraction**: 隔离模型实现
- **渐进式AI采用 / Progressive AI Adoption**: 逐步的用户适应

### 提示工程标准 / Prompt Engineering Standards
- **精确性 / Precision**: 避免模糊或冲突的指令
- **推理强度 / Reasoning Effort**: 选择合适的级别（高/中/低）
- **自我反思 / Self-Reflection**: 在实施前允许规划
- **持久化策略 / Persistence Strategy**: 做出合理假设并记录

### TODO管理原则 / TODO Management Principles
- **任务分解 / Task Decomposition**: 将复杂任务分解为原子单元
- **状态纪律 / Status Discipline**: 维持单个进行中任务
- **优先级遵守 / Priority Adherence**: 严格遵循P0-P3优先级系统
- **完成标准 / Completion Standards**: 根据质量检查清单进行验证

## 重要约定 / Important Conventions

### 格式化标准 / Formatting Standards
- **时间格式 / Time Format**: YYYY年MM月DD日 HH:MM:SS（本地系统时间）
- **文件命名 / File Naming**: 文档文件使用kebab-case
- **内容结构 / Content Structure**: 清晰的双语章节和分隔符
- **XML语法 / XML Syntax**: 使用XML-like标签的结构化指令

### 优先级系统 / Priority System
- **🔥 P0**: 紧急且重要 - 立即处理 / Urgent & Important - Handle immediately
- **⚡ P1**: 重要但不紧急 - 本周内完成 / Important but not urgent - Complete within week
- **📅 P2**: 中等优先级 - 本月内完成 / Medium priority - Complete within month
- **🌱 P3**: 低优先级 - 视情况处理 / Low priority - Handle as appropriate

### 状态定义 / Status Definitions
- **🔄 in_progress**:  actively working (only one at a time)
- **✅ completed**: 成功完成 / Successfully finished
- **⏳ pending**: 等待开始 / Waiting to start
- **🚫 cancelled**: 任务已放弃 / Task abandoned
- **🔄 blocked**: 被依赖关系阻塞 / Blocked by dependencies

## 质量标准和评估 / Quality Standards & Evaluation

仓库遵循严格的质量标准：
The repository follows rigorous quality standards:
- **功能完整性 / Functional Completeness**: 核心功能已实现
- **代码质量 / Code Quality**: 遵守编码标准
- **文档完整性 / Documentation**: 完整且最新
- **测试覆盖 / Testing**: 足够的测试覆盖率
- **用户接受度 / User Acceptance**: 满足用户需求

## 风险管理 / Risk Management

常见风险和缓解策略：
Common risks and mitigation strategies:
- **技术风险 / Technical Risk**: 新技术不熟悉
- **进度风险 / Schedule Risk**: 任务估计不准确
- **质量风险 / Quality Risk**: 测试不充分
- **沟通风险 / Communication Risk**: 需求不明确

## 项目状态跟踪 / Project Status Tracking

仓库维护全面的进度跟踪：
The repository maintains comprehensive progress tracking:
- **完成指标 / Completion Metrics**: 基于百分比的进度跟踪
- **任务分析 / Task Analytics**: 按状态和优先级的细分
- **历史记录 / Historical Records**: 变更日志和版本历史
- **风险评估 / Risk Assessment**: 已识别的风险和缓解计划
- **下一步行动 / Next Actions**: 清晰的周度和月度计划

注意：这主要是一个文档仓库，专注于在多个AI平台上建立AI编码最佳实践、标准和实施指南。
Note: This is primarily a documentation repository focused on establishing AI coding best practices, standards, and implementation guidelines across multiple AI platforms.

## CodeBuddy Added Memories
- 此项目包含全面的AI编码规则文档，包括：
1. 严格的时间管理规则：必须使用本地系统时间格式 YYYY年MM月DD日 HH:MM:SS
2. 双语内容标准：所有文档保持中英文并行结构
3. 高级TODO管理系统：原子性原则、状态唯一性、P0-P3优先级系统
4. XML-like语法结构：用于GPT-5等AI模型的提示工程
5. 设计原则：用户中心设计、可靠性优先、可扩展性设计等
6. 质量评估框架：功能完整性、代码质量、文档完整性等维度

关键文件：README.md, gpt-5-coding.md, design-principles.md, todoschecklist.md, evaluation-framework.md
开发命令：标准git操作，强调时间戳合规性