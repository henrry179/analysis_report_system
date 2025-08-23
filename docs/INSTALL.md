# 业务分析报告自动化系统 - 安装指南

## 🚀 快速开始

业务分析报告自动化系统支持**渐进式安装**，您可以根据需求选择不同的功能级别：

## 📦 安装级别

### **Level 0: 零依赖模式** (推荐新手尝试)
```bash
# 无需安装任何依赖，直接运行
git clone <repository-url>
cd analysis_report_system
python src/main.py
```

**可用功能:**
- ✅ 基础数据分析（简化模式）
- ✅ 文本图表生成
- ✅ 简化报告输出
- ✅ 系统测试和演示

### **Level 1: 最小依赖** (轻量级使用)
```bash
pip install -r requirements_minimal.txt
```

**新增功能:**
- ✅ Pandas数据处理
- ✅ Jinja2模板引擎
- ✅ 完整测试支持

### **Level 2: 标准功能** (推荐大多数用户)
```bash
pip install -r requirements_standard.txt
```

**新增功能:**
- ✅ 图表可视化 (matplotlib/seaborn)
- ✅ Web管理界面 (FastAPI)
- ✅ 用户认证系统
- ✅ HTML报告生成

### **Level 3: 完整功能** (生产环境)
```bash
pip install -r requirements.txt
```

**新增功能:**
- ✅ 机器学习预测分析
- ✅ 交互式仪表盘 (Streamlit)
- ✅ PDF报告生成
- ✅ 数据库支持
- ✅ 完整测试覆盖

## 🎯 使用场景选择

| 场景 | 推荐级别 | 安装命令 |
|------|----------|----------|
| **快速体验/学习** | Level 0 | 无需安装 |
| **个人项目/原型** | Level 1 | `pip install -r requirements_minimal.txt` |
| **小团队使用** | Level 2 | `pip install -r requirements_standard.txt` |
| **生产部署** | Level 3 | `pip install -r requirements.txt` |

## 🔧 安装验证

### 验证安装
```bash
# 运行系统测试
python test_runner.py

# 运行功能演示
python enhanced_demo.py

# 检查项目完整性
python project_check.py
```

### 启动服务
```bash
# 基础分析服务
python src/main.py

# Web管理界面 (Level 2+)
python src/web_interface.py

# 交互式仪表盘 (Level 3)
streamlit run src/visualization/chart_generator.py
```

## 🐛 常见问题

### 依赖安装失败
```bash
# 更新pip
python -m pip install --upgrade pip

# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

### 网络连接问题
```bash
# 离线安装模式
pip install --no-deps -r requirements_minimal.txt

# 或直接使用零依赖模式
python src/main.py  # 无需任何依赖
```

### 权限问题
```bash
# 使用用户安装
pip install --user -r requirements.txt

# 或创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

## 📊 性能建议

### 系统要求
- **Python**: 3.8+ (必需)
- **内存**: 
  - Level 0-1: 256MB+
  - Level 2: 512MB+
  - Level 3: 1GB+
- **存储**: 100MB+ (包含依赖)

### 优化建议
1. **数据量大**时建议使用Level 3的完整功能
2. **网络受限**时可使用Level 0零依赖模式
3. **内存受限**时推荐Level 1最小依赖

## 🆘 技术支持

### 问题诊断
```bash
# 系统诊断
python project_check.py

# 依赖检查
python -c "import sys; print(sys.version)"
python -c "import pkg_resources; print([str(d) for d in pkg_resources.working_set])"
```

### 获取帮助
1. 查看 [README.md](README.md) 详细文档
2. 运行 `python quick_start.py` 查看快速指南
3. 检查 [PROJECT_STATUS.md](PROJECT_STATUS.md) 了解项目状态

---

**安装建议**: 首次使用建议从Level 0开始体验，然后根据需求逐步升级到更高级别。 