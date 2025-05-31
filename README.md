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
- [x] 数据预览组件
- [x] 图表展示组件
- [x] 错误处理优化
- [x] 加载状态优化
- [x] UI/UX 优化

## 安装和运行
### 环境要求
- Python 3.8+ (推荐使用 Python 3.11)
- Node.js 16+ (推荐使用 Node.js 18 LTS)
- npm 8+ 或 yarn 1.22+

### 后端设置
1. 克隆项目：
```bash
git clone https://github.com/henrry179/analysis_report_system.git
cd analysis_report_system
```

2. 创建并激活 Python 虚拟环境：
```bash
# 使用 conda（推荐）
conda create -n analysis-py311 python=3.11
conda activate analysis-py311

# 或使用 venv
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. 安装后端依赖：
```bash
pip install -r requirements.txt
```

4. 启动后端服务：
```bash
python start_server.py
```
服务将在 http://localhost:8000 启动

### 前端设置
1. 进入前端目录：
```bash
cd frontend
```

2. 安装前端依赖：
```bash
npm install
# 或使用 yarn
yarn install
```

3. 启动开发服务器：
```bash
npm run dev
# 或使用 yarn
yarn dev
```
前端将在 http://localhost:5173 启动

### 访问系统
1. 打开浏览器访问 http://localhost:5173
2. 使用以下默认账号登录：
   - 管理员：admin / adminpass
   - 分析师：analyst / analyst123
   - 查看者：viewer / viewer123

## 常见问题
### 1. 端口占用
如果遇到端口占用问题，可以：
```bash
# 查找占用端口的进程
lsof -i:8000  # Mac/Linux
netstat -ano | findstr :8000  # Windows

# 终止进程
kill -9 <PID>  # Mac/Linux
taskkill /PID <PID> /F  # Windows
```

### 2. 依赖安装失败
如果安装依赖时遇到问题：
```bash
# 更新 pip
pip install --upgrade pip

# 清除 npm 缓存
npm cache clean --force

# 删除 node_modules 并重新安装
rm -rf node_modules
npm install
```

### 3. 启动失败
如果服务启动失败：
1. 检查 Python 版本：`python --version`
2. 确认虚拟环境已激活
3. 检查依赖是否完整安装
4. 查看日志文件：`logs/app.log`

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

## 最新进展
- [x] 后端用户认证与配置修复已完成，系统可正常启动并支持多用户登录。
