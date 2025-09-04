# QWCoder 安装指南

本指南将帮助你完成 QWCoder 终端环境的安装和配置。

## 📋 系统要求

### 支持的操作系统
- **Linux** (Ubuntu, CentOS, Fedora, Arch Linux 等)
- **macOS** (10.15+)
- **Windows** (通过 WSL 或 Git Bash)

### 必要的依赖
- Bash 或 Zsh shell
- curl 或 wget
- git

## 🚀 快速安装

### 方法 1: 自动安装 (推荐)

1. **克隆或下载 QWCoder**
   ```bash
   git clone https://github.com/yourusername/qwcoder.git
   cd qwcoder
   ```

2. **运行安装脚本**
   ```bash
   chmod +x scripts/setup.sh
   ./scripts/setup.sh
   ```

3. **重启终端**
   ```bash
   # 关闭当前终端窗口，打开新的终端窗口
   # 或者手动重新加载配置
   source ~/.bashrc  # Bash 用户
   source ~/.zshrc   # Zsh 用户
   ```

4. **验证安装**
   ```bash
   qwcoder help
   ```

### 方法 2: 手动安装

如果你偏好手动控制安装过程，可以按以下步骤操作：

1. **下载文件**
   ```bash
   wget https://github.com/yourusername/qwcoder/archive/main.zip
   unzip main.zip
   cd qwcoder-main
   ```

2. **设置环境变量**
   ```bash
   export QWCODER_HOME="$(pwd)"
   ```

3. **手动配置 Shell**
   ```bash
   # 对于 Bash
   echo "export QWCODER_HOME=\"$QWCODER_HOME\"" >> ~/.bashrc
   echo "source \"$QWCODER_HOME/config/bashrc\"" >> ~/.bashrc

   # 对于 Zsh
   echo "export QWCODER_HOME=\"$QWCODER_HOME\"" >> ~/.zshrc
   echo "source \"$QWCODER_HOME/config/zshrc\"" >> ~/.zshrc
   ```

4. **使脚本可执行**
   ```bash
   chmod +x scripts/*.sh tools/*.sh
   ```

## ⚙️ 配置选项

### Shell 配置

QWCoder 支持多种 Shell：

- **Bash** (默认)
- **Zsh** (推荐)

安装脚本会自动检测你的默认 Shell 并应用相应配置。

### 自定义安装

你可以通过编辑配置文件来自定义安装：

```bash
# 编辑主配置文件
vim config/qwcoder.json

# 编辑环境变量
vim config/environment.env

# 编辑别名配置
vim config/aliases.sh
```

## 🔧 依赖安装

### 自动依赖安装

安装脚本会尝试自动安装必要的依赖：

```bash
./tools/package-manager.sh dev-tools
```

### 手动依赖安装

如果你需要手动安装依赖：

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install curl wget git vim tree htop jq
```

#### CentOS/RHEL
```bash
sudo yum install curl wget git vim tree htop jq
```

#### Fedora
```bash
sudo dnf install curl wget git vim tree htop jq
```

#### Arch Linux
```bash
sudo pacman -S curl wget git vim tree htop jq
```

#### macOS
```bash
# 使用 Homebrew
brew install curl wget git vim tree htop jq
```

## 🐳 可选组件安装

### Node.js 开发环境

```bash
./tools/package-manager.sh nodejs
```

这将安装：
- NVM (Node Version Manager)
- 最新 LTS 版本的 Node.js
- npm 和 yarn

### Python 开发环境

```bash
./tools/package-manager.sh python
```

这将安装：
- pip 包管理器
- 虚拟环境工具
- 常用 Python 开发包

### Go 开发环境

```bash
./tools/package-manager.sh go
```

这将安装：
- Go 编译器和工具链
- 配置 GOPATH 和 GOROOT

### Docker 环境

```bash
./tools/package-manager.sh docker
```

这将安装：
- Docker 引擎
- Docker Compose
- 配置用户权限

## 🧪 测试安装

### 基本功能测试

```bash
# 测试别名
gs  # 应该显示 git status (如果在 git 仓库中)

# 测试函数
sysinfo  # 应该显示系统信息

# 测试工具
myip  # 应该显示你的公网 IP
```

### 高级功能测试

```bash
# 测试包管理器
./tools/package-manager.sh update

# 测试项目模板
./tools/project-templates.sh nodejs test-project
cd test-project && npm install
```

## 🔍 故障排除

### 常见安装问题

#### 1. 权限被拒绝

**问题**: `chmod: cannot access 'scripts/setup.sh': Permission denied`

**解决**:
```bash
# 确保你有执行权限
ls -la scripts/setup.sh
sudo chown $USER:$USER scripts/setup.sh
chmod +x scripts/setup.sh
```

#### 2. 命令未找到

**问题**: `qwcoder: command not found`

**解决**:
```bash
# 检查 PATH
echo $PATH | grep -q "$QWCODER_HOME/bin" || echo "需要添加 QWCoder 到 PATH"

# 手动添加路径
export PATH="$QWCODER_HOME/bin:$PATH"
```

#### 3. 配置不生效

**问题**: QWCoder 命令可用，但别名和函数不工作

**解决**:
```bash
# 重新加载配置
source ~/.bashrc

# 检查 QWCODER_HOME
echo $QWCODER_HOME

# 验证配置文件存在
ls -la $QWCODER_HOME/config/
```

#### 4. Git 集成不工作

**问题**: Git 别名不可用

**解决**:
```bash
# 检查是否在 Git 仓库中
git rev-parse --git-dir 2>/dev/null || echo "不在 Git 仓库中"

# 手动加载 Git 集成
source $QWCODER_HOME/config/git-integration.sh
```

### 日志和调试

启用详细日志：

```bash
# 运行安装脚本时启用调试
bash -x scripts/setup.sh
```

检查安装日志：

```bash
# 查看最近的修改
ls -la ~/.bashrc ~/.zshrc

# 检查 QWCoder 配置是否正确加载
grep -n "QWCoder" ~/.bashrc ~/.zshrc
```

## 📞 获取帮助

如果遇到问题：

1. **查看帮助文档**
   ```bash
   qwcoder help
   ```

2. **检查系统信息**
   ```bash
   sysinfo
   ```

3. **验证安装**
   ```bash
   # 检查所有组件
   ls -la $QWCODER_HOME/
   ```

4. **重新安装**
   ```bash
   # 备份当前配置
   cp ~/.bashrc ~/.bashrc.backup
   cp ~/.zshrc ~/.zshrc.backup

   # 重新运行安装
   ./scripts/setup.sh
   ```

## 🎉 安装完成

恭喜！QWCoder 已经成功安装。

### 下一步

1. **探索功能**
   ```bash
   qwcoder help
   ```

2. **自定义配置**
   ```bash
   qwconfig
   ```

3. **安装可选组件**
   ```bash
   ./tools/package-manager.sh all
   ```

4. **开始使用**
   ```bash
   # 创建你的第一个项目
   ./tools/project-templates.sh nodejs my-first-project
   ```

享受高效的终端开发体验！ 🚀
