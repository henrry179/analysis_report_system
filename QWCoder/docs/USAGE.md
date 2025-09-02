# QWCoder 使用指南

本指南将帮助你充分利用 QWCoder 的所有功能。

## 🎯 快速开始

### 基本命令

```bash
# 显示帮助信息
qwcoder help

# 更新 QWCoder
qwupdate

# 进入 QWCoder 目录
qwc
```

### 验证安装

```bash
# 检查系统信息
sysinfo

# 显示公网 IP
myip

# 检查天气
weather
```

## 🧭 导航和文件管理

### 智能导航

```bash
# 快速导航
..          # 上一级目录
...         # 上二级目录
....        # 上三级目录
qwc         # QWCoder 主目录
dl          # 下载目录
dt          # 桌面目录
doc         # 文档目录

# 创建并进入目录
mkcd new-project
```

### 文件操作

```bash
# 解压各种格式文件
extract archive.tar.gz
extract file.zip
extract archive.7z

# 查找文件
ff "*.js"              # 按文件名查找
fc "console.log"       # 按内容查找
ff "*.py" -type f      # 查找 Python 文件

# 显示磁盘使用情况
duh                    # 按人类可读格式显示
duh | head -10         # 显示前 10 个
```

## 🐙 Git 工作流程

### 基本 Git 操作

```bash
# 状态和历史
gs                    # git status
gl                    # git log (图形化)
gll                   # git log (详细)

# 添加和提交
ga                    # git add
gaa                   # git add --all
gcm "commit message"  # git commit -m
gca "amend message"   # git commit --amend

# 分支管理
gb                    # git branch
gco branch-name       # git checkout
gcb new-branch        # git checkout -b
gm master             # git merge

# 远程操作
gf                    # git fetch
gpl                   # git pull
gp                    # git push
gpf                   # git push --force-with-lease

# 其他
gd                    # git diff
gds                   # git diff --staged
gst                   # git stash
gstl                  # git stash list
gstp                  # git stash pop
```

### 高级 Git 功能

```bash
# 组合操作
gac "initial commit"     # git add . && git commit -m
gacp "feature done"      # git add . && git commit -m && git push

# 分支操作
gcb feature/login        # 创建并切换到新分支
gco -                    # 切换到上一个分支

# 清理
git-clean() {            # 自定义清理函数
  git branch --merged | grep -v master | xargs git branch -d
}
```

## 🐳 Docker 集成

### 容器管理

```bash
# Docker 基本操作
d ps                    # 查看运行中的容器
d ps -a                 # 查看所有容器
d images                # 查看镜像
d rm container_id       # 删除容器
d rmi image_id          # 删除镜像

# 快捷操作
dps                     # docker ps
dpsa                    # docker ps -a
di                      # docker images
drm                     # docker rm
drmi                    # docker rmi
```

### Docker Compose

```bash
# 服务管理
dc up                   # 启动服务
dc up -d                # 后台启动
dc down                 # 停止服务
dc restart              # 重启服务

# 日志和监控
dcl                     # docker-compose logs
dclf                    # docker-compose logs -f (跟随)
dc ps                   # 查看服务状态

# 开发工作流
dcb                     # docker-compose build
dcr                     # docker-compose run
dce                     # docker-compose exec
```

### Docker 清理

```bash
# 清理未使用资源
docker-clean            # 清理容器、镜像、卷、网络

# 或分别清理
d rm $(d ps -aq)        # 删除所有容器
d image prune -f        # 删除悬空镜像
d volume prune -f       # 删除未使用卷
d network prune -f      # 删除未使用网络
```

## 💻 开发环境

### Node.js 开发

```bash
# NPM 操作
n i                     # npm install
n i -D package          # npm install --save-dev
n r dev                 # npm run dev
n r build               # npm run build
n r test                # npm run test

# 版本管理 (需要 NVM)
nvm use 18              # 切换到 Node.js 18
nvm install --lts       # 安装最新 LTS
nvm list                # 列出已安装版本
```

### Python 开发

```bash
# 虚拟环境
venv                    # 创建虚拟环境
va                      # 激活虚拟环境 (source venv/bin/activate)
vd                      # 退出虚拟环境 (deactivate)

# 包管理
pi package              # pip install
pir                     # pip install -r requirements.txt
pf                      # pip freeze
pfr                     # pip freeze > requirements.txt

# 快捷操作
py file.py              # python3 file.py
python file.py          # 与上面相同
```

### Go 开发

```bash
# 基本操作
go run main.go          # 运行程序
go build                # 编译程序
go test                 # 运行测试
go mod tidy             # 整理依赖

# 代码质量
go fmt                  # 格式化代码
go vet                  # 检查代码
go mod verify           # 验证依赖
```

## 🛠️ 实用工具

### 系统监控

```bash
# 系统信息
sysinfo                 # 完整系统信息
htop                    # 进程监控 (需要安装 htop)
top                     # 系统监控

# 网络工具
ping g                  # ping Google
myip                    # 显示公网 IP
speedtest               # 网速测试
ports                   # 显示开放端口
```

### 开发工具

```bash
# HTTP 服务器
serve                   # 在端口 8000 启动服务器
serve 3000              # 在指定端口启动

# JSON 处理
jsonpp                  # 美化 JSON (从管道输入)
curl api.example.com | jsonpp

# 编码转换
urlencode "hello world" # URL 编码
urldecode "hello%20world" # URL 解码

# 计算器
calc "2 * 3 + 4"        # 基本计算
calc "sqrt(16)"         # 高级数学函数
```

### 文件处理

```bash
# 批量操作
ff "*.tmp" -delete      # 删除所有 .tmp 文件
ff "*.log" -exec wc -l {} \;  # 统计日志文件行数

# 归档
tar czf archive.tar.gz directory/
extract archive.tar.gz

# 权限管理
chmod +x scripts/*.sh   # 使所有脚本可执行
find . -type f -name "*.sh" -exec chmod +x {} \;
```

## 📝 项目管理

### 创建新项目

```bash
# 使用项目模板
./tools/project-templates.sh nodejs my-api
./tools/project-templates.sh python data-app
./tools/project-templates.sh react my-frontend
./tools/project-templates.sh go web-server

# 快速创建项目 (需要自定义函数)
create-project nodejs my-project
create-project python analyzer
```

### 项目模板特性

每个项目模板包含：

- **完整的目录结构**
- **配置文件** (.gitignore, README.md 等)
- **依赖文件** (package.json, requirements.txt 等)
- **基本代码模板**
- **开发工具配置** (ESLint, Black, Prettier 等)

### 示例：创建 Node.js API

```bash
./tools/project-templates.sh nodejs my-api
cd my-api

# 项目结构
my-api/
├── package.json      # 依赖配置
├── index.js          # 主应用文件
├── .gitignore        # Git 忽略文件
├── .eslintrc.js      # ESLint 配置
├── .prettierrc       # Prettier 配置
└── README.md         # 项目文档

# 安装依赖并运行
npm install
npm run dev
```

## ⚙️ 自定义配置

### 编辑配置文件

```bash
# 主配置文件
qwconfig               # 编辑 qwcoder.json
vim $QWCODER_HOME/config/qwcoder.json

# 别名配置
vim $QWCODER_HOME/config/aliases.sh

# 环境变量
vim $QWCODER_HOME/config/environment.env

# Shell 特定配置
vim $QWCODER_HOME/config/bashrc  # Bash
vim $QWCODER_HOME/config/zshrc   # Zsh
```

### 添加自定义别名

编辑 `config/aliases.sh`：

```bash
# 添加你的自定义别名
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias ..='cd ..'
alias ...='cd ../..'
```

### 添加自定义函数

编辑 `scripts/functions.sh`：

```bash
# 添加你的自定义函数
my-function() {
    echo "Hello from my custom function!"
    # 你的代码逻辑
}
```

### 环境变量配置

编辑 `config/environment.env`：

```bash
# 添加你的环境变量
export MY_PROJECT_PATH="/path/to/projects"
export DATABASE_URL="postgresql://localhost/mydb"
export API_KEY="your-api-key"
```

## 🔄 工作流程示例

### Web 开发工作流程

```bash
# 1. 创建新项目
./tools/project-templates.sh react my-app
cd my-app

# 2. 安装依赖
npm install

# 3. 初始化 Git 仓库
git init
gaa
gcm "Initial commit"

# 4. 启动开发服务器
npm start

# 5. 在新终端中监控文件变化
# (在新终端中)
cd my-app
npm run build
```

### 数据分析工作流程

```bash
# 1. 创建 Python 项目
./tools/project-templates.sh python data-analysis
cd data-analysis

# 2. 激活虚拟环境
va

# 3. 安装数据科学包
pi pandas numpy matplotlib scikit-learn jupyter

# 4. 创建分析脚本
# 编辑 main.py 添加你的分析代码

# 5. 运行分析
python main.py

# 6. 启动 Jupyter
jupyter notebook
```

### API 开发工作流程

```bash
# 1. 创建 Node.js 项目
create-project nodejs my-api
cd my-api

# 2. 安装必要包
ni express mongoose dotenv

# 3. 设置环境变量
cp .env.example .env
# 编辑 .env 文件

# 4. 开发 API
# 编辑 index.js 添加路由和逻辑

# 5. 测试 API
npm run dev

# 6. 使用工具测试
curl localhost:3000/api/test | jsonpp
```

## 🎨 高级用法

### 组合命令

```bash
# Git 工作流程
gac "update README" && gp

# Docker 开发
dc down && dcb && dc up -d

# 文件处理
ff "*.log" -exec gzip {} \;

# 系统维护
sudo apt update && sudo apt upgrade -y
```

### 脚本编写

创建自定义脚本：

```bash
# 在 scripts/ 目录下创建脚本
vim $QWCODER_HOME/scripts/my-script.sh

# 使脚本可执行
chmod +x $QWCODER_HOME/scripts/my-script.sh

# 在别名中引用
echo "alias myscript='$QWCODER_HOME/scripts/my-script.sh'" >> $QWCODER_HOME/config/aliases.sh
```

### 自动化任务

使用函数创建自动化任务：

```bash
# 添加到 functions.sh
deploy() {
    echo "🚀 Starting deployment..."
    npm run build
    dc down
    dcb
    dc up -d
    echo "✅ Deployment completed!"
}

# 使用
deploy
```

## 📊 监控和调试

### 性能监控

```bash
# 系统资源
htop                    # 实时进程监控
df -h                   # 磁盘使用情况
free -h                 # 内存使用情况

# 网络监控
ss -tlnp                # 查看监听端口
netstat -i              # 网络接口统计
```

### 日志分析

```bash
# 查找错误日志
fc "ERROR" *.log
fc "Exception" *.log

# 监控日志变化
tail -f app.log

# 分析日志
grep "ERROR" app.log | wc -l  # 错误数量
grep "WARN" app.log | tail -10  # 最近警告
```

### 调试技巧

```bash
# 调试脚本
bash -x scripts/setup.sh

# 检查变量
echo $QWCODER_HOME
echo $PATH

# 验证配置
source ~/.bashrc && echo "Configuration loaded"

# 测试网络连接
ping -c 3 google.com
curl -I https://github.com
```

## 🔧 维护和更新

### 定期维护

```bash
# 更新系统
./tools/package-manager.sh update

# 更新 QWCoder
qwupdate

# 清理系统
docker-clean
ff "*.tmp" -delete
```

### 备份配置

```bash
# 备份 QWCoder 配置
cp -r $QWCODER_HOME $QWCODER_HOME.backup.$(date +%Y%m%d)

# 备份个人配置
cp ~/.bashrc ~/.bashrc.backup
cp ~/.zshrc ~/.zshrc.backup
```

## 🎯 最佳实践

### 1. 保持更新

```bash
# 定期更新
qwupdate

# 更新依赖
./tools/package-manager.sh update
```

### 2. 使用版本控制

```bash
# 为你的配置创建 Git 仓库
cd $QWCODER_HOME
git init
git add .
git commit -m "Initial QWCoder setup"
```

### 3. 自定义和扩展

```bash
# 添加你的偏好设置
vim $QWCODER_HOME/config/aliases.sh

# 创建个人脚本
vim $QWCODER_HOME/scripts/personal.sh
```

### 4. 备份重要数据

```bash
# 定期备份
backup ~/projects ~/projects.backup
backup ~/.ssh ~/.ssh.backup
```

### 5. 学习和探索

```bash
# 探索可用函数
grep "^function" $QWCODER_HOME/scripts/functions.sh

# 查看所有别名
grep "^alias" $QWCODER_HOME/config/aliases.sh

# 学习新命令
man <command>
tldr <command>
```

通过遵循这些指南和最佳实践，你可以充分利用 QWCoder 的强大功能，提升你的开发效率和工作流程。享受高效的终端开发体验！ 🚀
