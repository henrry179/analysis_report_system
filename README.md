# 数据分析报告系统

## 项目概述
数据分析报告系统是一个用于数据导入、分析、可视化和报告生成的综合平台。系统支持多种数据格式，提供丰富的分析功能，并能生成多种格式的分析报告。

## 功能特性
- 数据管理：支持 CSV、Excel、JSON 格式的数据导入和管理
- 数据分析：提供描述性分析、相关性分析、趋势分析和预测分析
- 报告生成：支持生成可视化报告和分析报告，输出格式包括 HTML、PDF、Markdown 和 JSON
- 系统管理：用户管理、日志查看和系统备份恢复

## 技术栈
### 后端
- Python 3.8+
- FastAPI
- Pandas
- NumPy
- Scikit-learn
- Jinja2
- WeasyPrint

### 前端
- Vue 3
- Vue Router
- Element Plus
- Axios
- ECharts

## 项目结构
```
analysis_report_system/
├── src/
│   ├── api/            # API 接口
│   ├── core/           # 核心功能模块
│   ├── static/         # 静态资源
│   ├── templates/      # 模板文件
│   └── utils/          # 工具函数
├── tests/              # 单元测试
├── frontend/           # 前端项目
│   ├── src/
│   │   ├── views/      # 页面组件
│   │   ├── router/     # 路由配置
│   │   └── assets/     # 静态资源
│   └── public/         # 公共资源
└── docs/              # 项目文档
```

## 实现进度
### 后端实现
- [x] 数据处理器 (DataProcessor)
- [x] 分析引擎 (AnalysisEngine)
- [x] 报告生成器 (ReportGenerator)
- [x] 系统管理器 (SystemManager)
- [x] API 接口实现
- [x] 单元测试

### 前端实现
- [x] 项目初始化
- [x] 路由配置
- [x] 登录页面
- [x] 仪表盘页面
  - [x] 数据管理模块
  - [x] 数据分析模块
  - [x] 报告管理模块
  - [x] 系统管理模块
- [ ] 数据预览组件
- [ ] 图表展示组件
- [ ] 错误处理优化
- [ ] 加载状态优化
- [ ] UI/UX 优化

## 安装和运行
### 后端
1. 创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 运行服务：
```bash
uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```

### 前端
1. 进入前端目录：
```bash
cd frontend
```

2. 安装依赖：
```bash
npm install
```

3. 运行开发服务器：
```bash
npm run dev
```

## API 文档
启动后端服务后，访问 http://localhost:8000/docs 查看完整的 API 文档。

## 测试
运行单元测试：
```bash
python -m pytest tests/
```

## 贡献指南
1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证
MIT License
