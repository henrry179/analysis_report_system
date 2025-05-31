# 分析报告系统 (Analysis Report System)

一个基于Python和Vue.js的数据分析和报告生成系统，提供数据处理、分析、可视化和报告生成功能。

## 功能特性

### 1. 数据处理
- 支持CSV、Excel、JSON格式数据导入
- 数据预处理（缺失值处理、异常值处理、数据类型转换）
- 数据验证和清洗
- 数据导出功能

### 2. 数据分析
- 描述性统计分析
- 相关性分析
- 趋势分析
- 预测分析
- 客户分群分析

### 3. 报告生成
- 可视化报告生成
- 分析报告生成
- 执行摘要生成
- 支持多种输出格式（HTML、PDF、Markdown、JSON）

### 4. 系统管理
- 用户认证和授权
- 权限管理
- 系统日志记录
- 系统备份和恢复

## 技术栈

### 后端
- Python 3.8+
- FastAPI
- Pandas
- NumPy
- JWT认证
- WeasyPrint (PDF生成)

### 前端
- Vue.js 3
- Element Plus
- Axios
- ECharts

## 安装说明

1. 克隆项目
```bash
git clone https://github.com/yourusername/analysis_report_system.git
cd analysis_report_system
```

2. 安装后端依赖
```bash
pip install -r requirements.txt
```

3. 安装前端依赖
```bash
cd frontend
npm install
```

## 使用方法

1. 启动后端服务
```bash
python src/api/main.py
```

2. 启动前端服务
```bash
cd frontend
npm run serve
```

3. 访问系统
打开浏览器访问 http://localhost:8080

## 项目结构

```
analysis_report_system/
├── src/
│   ├── api/            # API接口
│   ├── core/           # 核心功能模块
│   ├── static/         # 静态资源
│   └── templates/      # 模板文件
├── tests/              # 测试文件
├── frontend/           # 前端代码
└── docs/              # 文档
```

## 开发进度

### 已完成
- [x] 数据处理模块
- [x] 分析引擎模块
- [x] 报告生成模块
- [x] 系统管理模块
- [x] API接口实现
- [x] 前端界面实现
- [x] 单元测试

### 进行中
- [ ] 系统集成测试
- [ ] 性能优化
- [ ] 文档完善

### 待完成
- [ ] 部署文档
- [ ] 用户手册
- [ ] API文档

## 贡献指南

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License
