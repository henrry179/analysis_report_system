# 业务分析报告自动化系统 v4.0 Optimized

<div align="center">

![版本](https://img.shields.io/badge/版本-v4.0%20Optimized-blue.svg)
![状态](https://img.shields.io/badge/状态-正常运行-green.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-latest-green.svg)
![Vue](https://img.shields.io/badge/Vue-3.x-green.svg)

🏪 **专业业务分析报告系统 - 智能分析 · 数据驱动 · 洞察未来**

</div>

## 🎉 最新更新 (2025-06-01)

### ✅ 系统修复完成
经过全面诊断和修复，系统现已完全正常运行：

- **端口占用问题** ✅ - 实现智能端口检测和自动切换功能
- **报告生成器缺失** ✅ - 创建完整的多行业报告生成模块
- **模板系统错误** ✅ - 重新配置Jinja2模板系统
- **路由冲突问题** ✅ - 调整API路由优先级，确保正确访问

### 🚀 新增功能模块 (Phase 2)
继系统修复后，新增了以下核心功能模块：

- **👥 用户管理系统** ✅ - 完整的用户CRUD、权限管理、统计分析
- **📊 数据分析API** ✅ - 基础/高级分析、指标计算、趋势分析
- **📱 前端用户管理页面** ✅ - 现代化Vue组件，支持搜索、分页、实时统计
- **📈 数据上传分析** ✅ - 支持CSV/Excel/JSON文件上传和智能分析

### 🚀 新增功能
- **智能端口管理**: 自动检测端口占用并切换到可用端口
- **多行业报告生成**: 支持5种行业类型的智能分析报告
- **便捷启动脚本**: 一键启动系统并自动检查依赖
- **系统状态监控**: 实时显示系统运行状态和端口信息
- **用户权限体系**: 完整的用户管理，支持管理员、分析师、查看者三种角色
- **数据分析引擎**: 提供基础和高级数据分析功能
- **文件上传分析**: 支持多种格式文件的智能数据分析
- **实时趋势分析**: 基于时间序列的趋势预测和置信区间计算

---

## 📋 项目概述

业务分析报告自动化系统是一个集数据分析、可视化、报告生成于一体的智能化平台。系统支持多种数据格式导入，提供强大的分析功能，并能生成专业的可视化分析报告。

### 🎯 核心特性

- **🔍 智能数据分析**: 支持多维度数据分析和趋势预测
- **📊 自动报告生成**: 一键生成专业的HTML格式分析报告
- **🏭 多行业支持**: 涵盖零售、金融、社区团购、智能体等5大行业
- **⚡ 实时WebSocket通信**: 支持实时进度推送和状态更新
- **👥 用户权限管理**: 完整的角色权限体系
- **📱 现代化UI**: Vue 3 + Element Plus构建的响应式前端

## 🏗️ 技术架构

### 后端技术栈
- **框架**: FastAPI (高性能异步Web框架)
- **数据分析**: Pandas, NumPy, Scikit-learn
- **模板引擎**: Jinja2
- **认证**: OAuth2 + JWT
- **WebSocket**: 实时通信支持
- **日志**: 结构化日志系统

### 前端技术栈
- **框架**: Vue 3 + TypeScript
- **UI组件**: Element Plus
- **路由**: Vue Router 4
- **HTTP客户端**: Axios
- **图表**: Chart.js / ECharts
- **构建工具**: Vite

## 📁 项目结构

```
analysis_report_system/
├── 🎯 start_server.py         # 主启动脚本
├── 🚀 run_system.sh          # 便捷启动脚本
├── 📋 requirements.txt        # Python依赖
├── 📊 SYSTEM_STATUS.md       # 系统状态报告
├── 
├── 📂 src/                   # 后端核心代码
│   ├── 🔧 main.py           # FastAPI应用主文件
│   ├── 🔌 api/              # API接口层
│   │   └── reports.py       # 报告相关API
│   ├── 🎛️ core/             # 核心业务逻辑
│   │   ├── auth.py         # 用户认证
│   │   ├── websocket.py    # WebSocket管理
│   │   └── models.py       # 数据模型
│   ├── 📊 reports/          # 报告生成模块
│   │   └── multi_industry_report_generator.py
│   ├── ⚙️ config/           # 配置管理
│   │   └── settings.py     # 系统配置
│   ├── 🛠️ utils/            # 工具函数
│   │   ├── logger.py       # 日志系统
│   │   └── exceptions.py   # 异常处理
│   └── 🎨 templates/        # HTML模板
│
├── 📂 frontend/             # 前端项目
│   ├── 📁 src/             # Vue源代码
│   ├── 📁 dist/            # 构建输出
│   ├── 📦 package.json     # 前端依赖
│   └── ⚙️ vite.config.js   # Vite配置
│
├── 📂 output/              # 输出目录
│   └── 📊 reports/         # 生成的报告文件
├── 📂 logs/                # 日志文件
├── 📂 docs/                # 项目文档
└── 📂 tests/               # 测试文件
```

## 🚀 快速开始

### 环境准备

**系统要求**:
- Python 3.8+
- Node.js 16+
- Git

### 1️⃣ 克隆项目
```bash
git clone <repository-url>
cd analysis_report_system
```

### 2️⃣ 后端环境配置
```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt
```

### 3️⃣ 前端环境配置
```bash
cd frontend
npm install
npm run build  # 构建前端
cd ..
```

### 4️⃣ 启动系统

**方式1: 使用便捷脚本 (推荐)**
```bash
chmod +x run_system.sh
./run_system.sh
```

**方式2: 直接启动**
```bash
python start_server.py
```

### 5️⃣ 访问系统
- 🌐 **主页**: http://localhost:8000/
- 📊 **状态页面**: http://localhost:8000/status
- 📚 **API文档**: http://localhost:8000/docs
- 🧪 **测试页面**: http://localhost:8000/test

## 👥 默认账户

| 角色 | 用户名 | 密码 | 权限 |
|------|--------|------|------|
| 管理员 | admin | adminpass | 全部权限 |
| 分析师 | analyst | analyst123 | 分析和报告权限 |
| 查看者 | viewer | viewer123 | 只读权限 |

## 📊 核心功能

### 🏭 多行业报告生成
支持以下5种行业类型的智能分析：

| 行业 | 代码 | 分析内容 |
|------|------|----------|
| 🏪 零售行业 | retail | 销售数据、区域分析、品类表现 |
| 🏘️ 社区团购 | community | 订单数据、城市覆盖、团长运营 |
| 💰 金融交易 | financial | 交易量、风险评估、产品表现 |
| 🤖 智能体 | ai_agent | 技术发展、应用场景、市场趋势 |
| 🔄 跨行业对比 | cross_industry | 多维度比较不同行业发展状况 |

### 📈 报告特性
- **智能数据分析**: 自动生成关键指标和洞察
- **可视化图表**: 内置Chart.js图表支持
- **响应式设计**: 支持移动端和桌面端查看
- **实时生成**: 后台异步生成，WebSocket推送进度
- **多格式输出**: HTML格式，未来支持PDF导出

## 🔧 API接口

### 核心端点
- `GET /health` - 健康检查
- `GET /api/info` - 系统信息
- `GET /api/system/status` - 系统状态
- `GET /api/reports/industry-types` - 获取支持的行业类型
- `POST /api/reports/multi-industry/generate` - 生成多行业报告

### 用户管理API
- `GET /api/users/` - 获取用户列表(支持分页、搜索、角色过滤)
- `GET /api/users/stats` - 获取用户统计信息
- `GET /api/users/profile` - 获取当前用户信息
- `PUT /api/users/profile` - 更新当前用户信息
- `POST /api/users/change-password` - 修改密码
- `POST /api/users/create` - 创建新用户(管理员权限)
- `PUT /api/users/{user_id}` - 更新用户信息(管理员权限)
- `DELETE /api/users/{user_id}` - 删除用户(管理员权限)

### 数据分析API
- `GET /api/analytics/overview` - 获取分析概览
- `POST /api/analytics/basic-analysis` - 执行基础数据分析
- `POST /api/analytics/advanced-analysis` - 执行高级数据分析(分析师权限)
- `POST /api/analytics/calculate-metrics` - 计算关键指标
- `GET /api/analytics/trend-analysis` - 趋势分析
- `POST /api/analytics/upload-data` - 上传数据进行分析
- `GET /api/analytics/analysis-history` - 获取分析历史记录

### 示例调用
```bash
# 生成报告
curl -X POST http://localhost:8000/api/reports/multi-industry/generate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer admin" \
  -d '{"industries": ["retail", "financial"]}'
```

## 🛠️ 开发指南

### 本地开发
```bash
# 启动开发模式（自动重载）
python start_server.py  # 后端会自动检测代码变更

# 前端开发模式
cd frontend
npm run dev  # 热重载开发服务器
```

### 日志查看
```bash
# 查看系统日志
tail -f logs/system.log

# 查看性能日志
tail -f logs/performance.log
```

### 测试
```bash
# 运行单元测试
python -m pytest tests/

# API测试
curl http://localhost:8000/health
```

## 🔍 故障排除

### 常见问题

1. **端口占用**
   - ✅ 系统会自动检测并切换到可用端口
   - 查看实际使用端口: 检查启动日志

2. **依赖安装失败**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **前端构建失败**
   ```bash
   cd frontend
   rm -rf node_modules
   npm install
   npm run build
   ```

4. **报告生成失败**
   - 检查 `output/reports/` 目录权限
   - 查看系统日志: `logs/system.log`

## 📈 系统监控

### 性能指标
- **响应时间**: 平均 < 200ms
- **内存使用**: 监控和日志记录
- **WebSocket连接**: 实时统计
- **报告生成**: 进度追踪

### 状态检查
访问 `/status` 页面查看:
- 系统运行状态
- 端口使用情况
- 可用端点列表
- 快速功能测试

## 🔮 未来规划

### v4.1 计划功能
- [ ] PDF报告导出
- [ ] 数据源连接器(数据库/API)
- [ ] 自定义报告模板
- [ ] 批量报告处理优化

### v4.2 规划
- [ ] 机器学习预测模型
- [ ] 实时数据流处理
- [ ] 多租户支持
- [ ] 国际化支持

## 🤝 贡献指南

1. Fork 项目仓库
2. 创建功能分支: `git checkout -b feature/new-feature`
3. 提交代码: `git commit -m 'Add new feature'`
4. 推送分支: `git push origin feature/new-feature`
5. 提交 Pull Request

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 📞 支持与反馈

- 🐛 **Bug报告**: [Issues](./issues)
- 💡 **功能建议**: [Discussions](./discussions)
- 📧 **技术支持**: 提交Issue获得帮助

---

<div align="center">

**⭐ 如果这个项目对您有帮助，请给我们一个Star！**

*最后更新: 2025-06-01 | 版本: v4.0 Optimized*

</div> 