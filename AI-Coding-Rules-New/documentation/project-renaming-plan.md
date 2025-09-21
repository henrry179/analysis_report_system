# Gitstars 项目重命名方案

根据项目类型和状态，我建议采用以下编号系统：

## 编号规则
- **01-XX**: 核心AI项目 (AI Hedge Fund, Qwen Coder)
- **02-XX**: 数据分析与BI项目 (Analysis Report System, RST Systems)
- **03-XX**: 开发工具与配置 (CLI Tools, QWCoder, Claude配置)
- **04-XX**: 财务管理项目
- **05-XX**: 数据生成与处理工具
- **06-XX**: 其他进行中的项目
- **07-XX**: 已完成但仍在维护的项目
- **08-XX**: 存档或备用项目
- **09-XX**: 配置和环境相关项目

## 建议的重命名方案

| 原文件夹名 | 新文件夹名 | 说明 |
| :--- | :--- | :--- |
| 1-ai-hedge-fund | 01-ai-hedge-fund | 核心AI项目 |
| 2-analysis_report_system | 02-analysis-report-system | 数据分析项目 |
| 4-clitools-algodata-mldl | 03-cli-tools-expert | 开发工具集 |
| 8-financial-management-systems | 04-financial-management-systems | 财务管理系统 |
| 12-RST-Systems | 02-rst-bi-systems | BI系统 (与数据分析相关) |
| 15-VirtualDataSetsCreatePython | 05-virtual-data-sets-generator | 数据生成工具 |
| 17-QWCoder | 03-qwcoder-terminal | 终端配置工具 |
| 18-QwenCoder-Project | 01-qwen-coder | 核心AI代码模型 |
| claude-memory-config | 03-claude-memory-config | Claude配置 |
| Claudeconfig | 03-claude-api-config | Claude API配置 |
| 7-Financereport | 04-financial-reports | 财务报告相关 |
| 13-SQLBusinessAlgorithm | 06-sql-business-algorithm | 进行中的项目 |
| 14-venv | 08-python-venv | 存档的虚拟环境 |
| 16-.claude | 08-claude-backup | 存档的Claude配置 |
| .claude | 09-claude-local | 本地Claude配置 |
| 6-data | 05-project-data | 项目数据 |
| 9-logs | 08-project-logs | 项目日志 |
| 10-output | 05-generated-output | 生成的输出 |
| 11-pdf_reports | 05-pdf-reports | PDF报告 |
| models | 01-ai-models | AI模型 |
| Openaiconfig | 03-openai-config | OpenAI配置 |

注意：部分文件夹如 `api-calling-rules.md` 等文档文件，以及 `download_model_simple.bat` 等工具脚本，将保留在根目录中。