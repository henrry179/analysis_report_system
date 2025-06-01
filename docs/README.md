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
├── data/              # 数据目录
│   ├── logs/         # 日志文件
│   ├── output/       # 输出文件
│   └── reports/      # 报告文件
├── docs/             # 项目文档
├── frontend/         # 前端项目
│   ├── src/         # 源代码
│   ├── dist/        # 构建输出
│   └── public/      # 静态资源
├── src/             # 后端源代码
│   ├── api/         # API 接口
│   ├── core/        # 核心功能
│   ├── utils/       # 工具函数
│   └── templates/   # 模板文件
├── tests/           # 测试文件
├── .gitignore      # Git 忽略配置
├── requirements.txt # Python 依赖
└── start_server.py  # 启动脚本
```

## 配置说明
### 环境配置
1. Python 虚拟环境：
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   .venv\Scripts\activate     # Windows
   ```

2. 依赖安装：
   ```bash
   # 使用 pip
   pip install -r requirements.txt
   
   # 或使用 conda
   conda install numpy pandas fastapi uvicorn pydantic jinja2 passlib python-multipart
   ```

3. 前端依赖：
   ```bash
   cd frontend
   npm install
   ```

### 系统配置
1. 日志配置：
   - 日志文件位置：`data/logs/`
   - 日志级别：INFO
   - 日志轮转：每天

2. 数据存储：
   - 临时文件：`data/output/`
   - 报告文件：`data/reports/`
   - 上传文件：`data/uploads/`

3. 安全配置：
   - 默认管理员：admin / adminpass
   - 默认分析师：analyst / analyst123
   - 默认查看者：viewer / viewer123

## 启动系统

### 后端服务启动
1. 确保已安装依赖并激活虚拟环境：
   ```bash
   pip install -r requirements.txt
   # 或使用 conda 安装依赖
   conda install numpy pandas fastapi uvicorn pydantic jinja2 passlib python-multipart
   ```

2. 启动后端服务：
   ```bash
   python start_server.py
   ```
   服务默认运行在 http://localhost:8000

### 前端服务启动
1. 进入前端目录并安装依赖：
   ```bash
   cd frontend
   npm install
   ```

2. 启动前端开发服务器：
   ```bash
   npm run dev
   ```
   前端默认运行在 http://localhost:5173

### 访问系统
- 浏览器访问 http://localhost:5173
- 默认账号：
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
4. 查看日志文件：`data/logs/app.log`

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
- [x] 项目结构优化完成，统一了数据、文档和测试目录
- [x] 更新了依赖管理，支持 pip 和 conda 安装
- [x] 完善了系统配置说明
- [x] 优化了文档结构，增加了配置说明章节
