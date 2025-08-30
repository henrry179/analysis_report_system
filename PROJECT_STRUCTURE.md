# 📁 项目结构说明

## 🏗️ 优化后的项目架构 (2025-08-30)

```
analysis_report_system/
├── 📄 README.md                     # 主项目文档
├── 📄 PROJECT_STRUCTURE.md          # 项目结构说明 (本文档)
├── 📄 .gitignore                    # Git忽略文件配置
├── 📄 .dockerignore                 # Docker忽略文件配置
│
├── 📁 src/                          # 🎯 核心源代码
│   ├── 📄 main.py                   # FastAPI主应用入口
│   ├── 📄 __init__.py               # Python包初始化
│   │
│   ├── 📁 core/                     # 核心功能模块
│   │   ├── 📄 auth.py               # 用户认证与权限管理
│   │   ├── 📄 models.py             # 数据模型定义
│   │   └── 📄 websocket.py          # WebSocket连接管理
│   │
│   ├── 📁 api/                      # API接口模块
│   │   └── 📄 reports.py            # 报告相关API路由
│   │
│   ├── 📁 analysis/                 # 数据分析引擎
│   │   ├── 📄 professional_analytics.py   # 专业分析引擎
│   │   ├── 📄 advanced_analytics_engine.py # 高级分析引擎
│   │   └── 📄 metrics_analyzer.py          # 指标分析器
│   │
│   ├── 📁 data/                     # 数据处理模块
│   │   ├── 📄 sample_data_generator.py     # 样本数据生成器
│   │   └── 📄 data_quality_checker.py      # 数据质量检查
│   │
│   ├── 📁 visualization/            # 可视化模块
│   │   ├── 📄 chart_generator.py            # 图表生成器
│   │   ├── 📄 enhanced_chart_generator.py  # 增强图表生成器
│   │   └── 📄 dashboard_generator.py       # 仪表板生成器
│   │
│   ├── 📁 utils/                    # 工具函数模块
│   │   ├── 📄 logger.py             # 日志管理
│   │   ├── 📄 exceptions.py         # 自定义异常
│   │   ├── 📄 metrics.py            # 监控指标
│   │   └── 📄 file_utils.py         # 文件操作工具
│   │
│   ├── 📁 templates/                # 前端模板
│   │   ├── 📄 index.html            # 主页模板
│   │   ├── 📄 dashboard.html        # 仪表盘模板
│   │   ├── 📄 reports.html          # 报告管理模板
│   │   ├── 📄 analysis.html         # 分析中心模板
│   │   ├── 📄 settings.html         # 设置页面模板
│   │   └── 📄 api_docs.html         # API文档模板
│   │
│   ├── 📁 static/                   # 静态资源 (CSS, JS, 图片)
│   └── 📁 demo/                     # 演示脚本
│
├── 📁 config/                       # ⚙️ 配置文件
│   ├── 📄 settings.py               # 系统设置配置
│   ├── 📄 requirements.txt          # Python依赖列表
│   ├── 📄 requirements_*.txt        # 不同级别的依赖配置
│   └── 📁 scripts/                  # 配置相关脚本
│
├── 📁 tests/                        # 🧪 测试文件 (整合后)
│   ├── 📄 comprehensive_test.py     # 综合功能测试
│   ├── 📄 test_web_system.py        # Web系统测试
│   ├── 📄 test_websocket.py         # WebSocket测试
│   ├── 📄 test_*.py                 # 各模块单元测试
│   └── 📁 database/                 # 数据库相关测试
│       └── 📄 test_db.py            # 数据库连接测试
│
├── 📁 tools/                        # 🔧 工具脚本 (新增)
│   ├── 📁 database/                 # 数据库工具
│   │   ├── 📄 check_db_url.py       # 数据库连接检查
│   │   ├── 📄 create_db.py          # 数据库创建脚本
│   │   └── 📄 init_db.bat           # 数据库初始化批处理
│   └── 📁 setup/                    # 设置工具
│       ├── 📄 performance_monitor.py  # 性能监控
│       └── 📄 setup.py                # 项目设置脚本
│
├── 📁 scripts/                      # 🚀 启动脚本
│   ├── 📄 start_server.py           # Web服务启动脚本
│   ├── 📄 run_system.py             # 系统运行脚本
│   └── 📄 run_tests.py              # 测试运行脚本
│
├── 📁 output/                       # 📊 输出文件
│   ├── 📁 reports/                  # 生成的报告文件
│   ├── 📁 charts/                   # 生成的图表文件
│   └── 📁 data/                     # 输出数据文件
│
├── 📁 docs/                         # 📚 文档集合
│   ├── 📁 api-docs/                 # API文档 (新增)
│   └── 📁 deployment/               # 部署文档 (新增)
│
├── 📁 data/                         # 💾 数据目录
│   ├── 📁 uploads/                  # 上传文件
│   ├── 📁 imports/                  # 导入数据
│   └── 📁 exports/                  # 导出数据
│
├── 📁 database/                     # 🗄️ 数据库相关
│   └── 📁 migrations/               # 数据库迁移脚本
│
├── 📁 deploy/                       # 🐳 部署配置
│   ├── 📁 nginx/                    # Nginx配置
│   └── 📁 monitoring/               # 监控配置
│
├── 📁 examples/                     # 📖 示例数据
│   └── 📁 data/                     # 示例数据文件
│
├── 📁 logs/                         # 📝 日志文件
├── 📁 pdf_reports/                  # 📋 PDF报告
├── 📁 backup/                       # 💾 备份目录 (新增)
│   └── 📁 legacy/                   # 遗留文件备份
│
├── 📁 archived/                     # 🗃️ 归档文件 (新增)
│   ├── 📁 cli-tools/                # CLI工具归档
│   └── 📁 cli-tools-expert/         # 独立CLI工具项目
│
└── 📁 .github/                      # 🔧 GitHub配置
    ├── 📁 workflows/                # GitHub Actions工作流
    └── 📁 ISSUE_TEMPLATE/           # Issue模板
```

## 📋 目录功能说明

### 🎯 **核心开发目录**
- **`src/`**: 所有源代码，按功能模块清晰分类
- **`config/`**: 统一的配置文件管理
- **`tests/`**: 整合后的测试文件，便于测试管理

### 🔧 **工具与脚本目录**
- **`tools/`**: 数据库工具、设置工具等开发工具
- **`scripts/`**: 系统启动和运行脚本
- **`docs/`**: 项目文档和API文档

### 📊 **数据与输出目录**
- **`output/`**: 系统生成的报告、图表等输出文件
- **`data/`**: 用户数据、上传文件、导入导出数据
- **`logs/`**: 系统运行日志

### 🗃️ **归档与备份目录**
- **`archived/`**: 归档的旧版本文件和独立项目
- **`backup/`**: 备份文件和遗留代码

### 🚀 **部署与示例目录**
- **`deploy/`**: Docker、Nginx等部署配置
- **`examples/`**: 示例数据和演示文件

## ✅ **结构优化亮点**

1. **📁 文件归类**: 零散文件按功能分类到对应目录
2. **🧪 测试整合**: 所有测试文件统一到`tests/`目录
3. **🔧 工具集中**: 数据库工具、设置脚本集中到`tools/`
4. **🗃️ 历史归档**: CLI工具和压缩包移至`archived/`
5. **📚 文档分类**: API文档、部署文档分类管理
6. **💾 备份预留**: 新增`backup/`目录用于未来备份需求

## 🎯 **开发建议**

- **新功能开发**: 在`src/`对应模块中添加代码
- **测试编写**: 在`tests/`目录下编写对应测试文件
- **工具脚本**: 新工具放在`tools/`对应子目录
- **文档更新**: 在`docs/`目录下维护相关文档
- **配置修改**: 在`config/`目录下统一管理配置

---

*📅 结构优化时间: 2025-08-30 10:48*  
*🏷️ 版本: v3.4.1 Restructured Optimized*  
*👥 维护者: Analysis Report System Team*