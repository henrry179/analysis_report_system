# 🤖 Qwen3 Coder - 通义千问代码生成模型

Windows本地部署版本，支持代码生成、解释、优化等多种功能。

## 📋 功能特性

- ✅ **代码生成** - 根据自然语言描述生成代码
- ✅ **代码解释** - 详细解释代码功能和逻辑
- ✅ **代码优化** - 改进代码性能和可读性
- ✅ **多语言支持** - 支持358种编程语言
- ✅ **长上下文支持** - 原生支持256K tokens
- ✅ **Web界面** - 现代化的Gradio界面
- ✅ **命令行交互** - 直接在终端中使用
- ✅ **本地运行** - 无需网络，保护隐私

## 🚀 快速开始

### 1. 环境准备

确保已安装：
- Python 3.8+
- pip (Python包管理器)
- Git (可选，用于克隆项目)

### 2. 安装依赖

```bash
# 进入项目目录
cd D:\Gitstars\QwenCoder-Project

# 安装Python依赖
pip install -r requirements_v3.txt
```

### 3. 启动Qwen3 Coder

#### 方式一：Web界面 (推荐)

```powershell
# 使用PowerShell脚本启动
.\start_qwen_coder_v3.ps1 -Mode web -Port 7860
```

或直接使用Python：

```bash
python qwen_coder_v3.py --mode web --port 7860
```

启动后访问：http://localhost:7860

#### 方式二：命令行交互

```powershell
# 启动命令行模式
.\start_qwen_coder_v3.ps1 -Mode cli
```

#### 方式三：Streamlit应用

```powershell
# 创建并启动Streamlit应用
.\start_qwen_coder_v3.ps1 -Mode streamlit

# 然后运行
streamlit run qwen_coder_app_v3.py
```

## 📖 使用指南

### Web界面使用

1. **代码生成**：
   - 在"代码生成"标签页输入需求描述
   - 例如："写一个Python函数来读取JSON文件并处理数据"
   - 调整参数：最大长度、创造性
   - 点击"生成代码"按钮

2. **代码解释**：
   - 在"代码解释"标签页粘贴代码
   - 点击"解释代码"获取详细解释

3. **代码优化**：
   - 在"代码优化"标签页输入代码
   - 选择编程语言
   - 点击"优化代码"获取优化建议

### 命令行交互

```bash
# 启动交互模式
python qwen_coder_v3.py --mode cli

# 可用命令
help          # 显示帮助
exit/quit     # 退出程序

# 示例对话
请输入你的问题: 写一个Python函数来计算斐波那契数列
请输入你的问题: 解释这个JavaScript闭包的用法
请输入你的问题: 优化这个SQL查询的性能
```

## ⚙️ 配置选项

### 启动参数

```bash
python qwen_coder_v3.py [选项]

选项:
  --mode {web,streamlit,cli}  运行模式 (默认: web)
  --model MODEL              模型名称 (默认: Qwen/Qwen3-Coder-30B-A3B-Instruct)
  --port PORT                Web界面端口 (默认: 7860)
  --help                     显示帮助信息
```

### PowerShell脚本参数

```powershell
.\start_qwen_coder_v3.ps1 [参数]

参数:
  -Mode <web|streamlit|cli>  运行模式 (默认: web)
  -Port <端口号>            Web界面端口 (默认: 7860)
  -Model <模型名称>         Hugging Face模型名称
```

## 🧠 支持的模型

### 推荐模型

1. **Qwen3-Coder-30B-A3B-Instruct** (默认)
   - 30B参数，3B活跃参数
   - 内存占用约60GB
   - 强大的代码生成能力

2. **Qwen3-Coder-480B-A35B-Instruct** (顶级性能)
   - 480B参数，35B活跃参数
   - 内存占用约500GB
   - 顶级代码生成能力

### 切换模型

```bash
# 使用不同的模型
python qwen_coder_v3.py --model Qwen/Qwen3-Coder-480B-A35B-Instruct

# 或使用PowerShell脚本
.\start_qwen_coder_v3.ps1 -Model "Qwen/Qwen3-Coder-480B-A35B-Instruct"
```

## 💾 系统要求

### 最低配置
- **CPU**: Intel i7 或 AMD Ryzen 7
- **内存**: 16GB RAM
- **存储**: 70GB 可用空间
- **Python**: 3.8+

### 推荐配置
- **CPU**: Intel i9 或 AMD Ryzen 9
- **内存**: 32GB RAM
- **GPU**: NVIDIA RTX 4090 或更高
- **存储**: 100GB SSD空间

### GPU支持

如果您的电脑有NVIDIA GPU：

```bash
# 安装CUDA版本的PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

## 🔧 故障排除

### 常见问题

#### 1. 内存不足
```
错误: CUDA out of memory
```
**解决**：
- 使用更小的模型：`--model Qwen/Qwen3-Coder-30B-A3B-Instruct`
- 启用8-bit量化（已在代码中配置）
- 关闭其他程序释放内存

#### 2. 模型下载失败
```
错误: Connection timeout
```
**解决**：
- 检查网络连接
- 使用代理或VPN
- 手动下载模型文件

#### 3. 依赖安装失败
```
错误: No module named 'torch'
```
**解决**：
```bash
# 重新安装依赖
pip uninstall torch torchvision torchaudio
pip install -r requirements_v3.txt
```

#### 4. Web界面无法访问
```
错误: Connection refused
```
**解决**：
- 检查端口是否被占用：`netstat -ano | findstr :7860`
- 更换端口：`--port 7861`
- 检查防火墙设置

### 性能优化

1. **使用GPU**：
   - 安装CUDA版本的PyTorch
   - 确保GPU驱动程序最新

2. **内存优化**：
   - 使用量化模型（已默认启用）
   - 减少最大生成长度
   - 使用较小的模型

3. **网络优化**：
   - 使用稳定的网络连接
   - 配置代理（如需要）

## 📚 开发项目示例

### 1. 创建Python Web应用

**需求**：创建一个简单的Flask Web应用

**输入**：
```
写一个Flask Web应用，包含用户注册、登录功能，使用SQLite数据库
```

**输出**：完整的Flask应用代码，包含路由、模板、数据库操作

### 2. 优化现有代码

**输入现有代码**：
```python
def fib(n):
    if n <= 1:
        return n
    else:
        return fib(n-1) + fib(n-2)
```

**优化结果**：使用记忆化或迭代的方式优化性能

### 3. 解释复杂代码

**输入**：复杂的算法或框架代码

**输出**：详细的功能解释、设计模式分析、优化建议

## 🤝 集成到开发环境

### VS Code集成

1. 安装Python扩展
2. 配置Python解释器
3. 创建任务运行Qwen3 Coder

### 其他编辑器

- **PyCharm**: 配置外部工具
- **Vim**: 添加快捷键
- **Emacs**: 创建插件

## 📄 许可证

本项目基于通义千问Qwen模型，遵循相应开源协议。

## 🙋‍♂️ 支持

如果遇到问题：

1. 查看本文档的故障排除部分
2. 检查GitHub Issues
3. 提交新的Issue

## 🔄 更新

```bash
# 更新代码
git pull

# 更新依赖
pip install -r requirements_v3.txt --upgrade
```

---

**🎉 享受使用Qwen3 Coder进行高效编程的乐趣！**

如有问题或建议，欢迎反馈。