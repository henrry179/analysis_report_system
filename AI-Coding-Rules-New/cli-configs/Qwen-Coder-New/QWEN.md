# 📄 Qwen-Coder.md（全局配置规则）

# QWEN.md - 全局规则配置（个人独立开发者版）

## 📌 全局说明
本文件为个人独立开发者的 **全局开发规范**，Qwen Coder 必须严格遵循以下规则，覆盖国内与出海项目，支持开源与私有项目。  
主要目标：**高可维护性、自动化、可扩展性**。

---

## 1️⃣ 项目范围
- 适用对象：个人独立开发者  
- 项目类型：GitHub 开源项目 / 秒哒项目 / 私人项目  
- 项目形态：网站类项目（前端 / 后端 / API）  

---

## 2️⃣ GitHub 与自动化规则
1. GitHub 仓库：  
   - 自动生成 `.gitignore`  
   - 提交规范：`feat: xxx`、`fix: yyy`、`chore: zzz`  

2. GitHub Actions 自动化：  
   - 自动化测试  
   - 自动化构建  
   - 自动化部署（云服务器 / DockerHub）  

---

## 3️⃣ 云服务配置
Qwen Coder 必须能提供以下配置建议文档：  
- 阿里云（ECS, OSS, RDS, SLB, FC）  
- AWS（EC2, S3, RDS, CloudFront）  
- Google Cloud（GCE, GKE, Cloud SQL）  
- 监控与分析：阿里云ARMS / Google Analytics / Umami  
- 日志与性能：Prometheus + Grafana  

生成文档：`docs/cloud_deployment.md`  

---

## 4️⃣ 测试与虚拟数据
Qwen Coder 必须生成：  
- 单元测试  
- 集成测试  
- 端到端测试（E2E）  
- Mock 数据集  

测试框架：Jest / Vitest / Pytest / Mocha / JUnit  

---

## 5️⃣ 文件结构与代码分析
Qwen Coder 必须在新建项目时，生成 `docs/project_structure.md`，内容包括：  
- 文件树结构  
- 核心模块说明  
- 技术栈总结  
- 每个模块的代码数量统计（行数 / 文件大小 / 文件类型分布）  

---

## 6️⃣ TODO 管理与进度追踪
Qwen Coder 必须维护以下文件：  
- `docs/todos.md`：待完成任务  
- `docs/completed_todos.md`：已完成任务  
- `docs/progress.md`：实时开发进度  

进度必须包括：  
1. 总体完成度（百分比 + 文本进度条）  
2. 各模块进度（前端 / 后端 / 测试 / 部署 / 文档）  
3. 开发时间表（里程碑日志）  

---

## 7️⃣ 文档与校验规则
- 每次更新项目时：Qwen Coder 必须自动更新  
  - `README.md`  
  - `QWEN.md`  
  - `docs/` 下所有衍生文档  
- 必须对比真实开发需求，校验功能是否符合要求  
- Qwen Coder 必须提供 GitHub 推送建议（commit 信息、分支管理）  

---

## 8️⃣ Qwen Coder 上下文 & Token 管理
1. 上下文记忆：Qwen Coder 必须只加载相关模块，避免全量文件读取  
2. Token 消耗提示：  
   - 每次输出必须显示 Token 使用量  
   - 每月费用估算（元）  
   - 超过 10K Token 时必须自动拆分任务  
3. Token 消耗统计与预算管理：
   - 维护 `docs/token_consumption_stats.md` 文件，记录每次API调用的模型、token消耗和成本
   - 提供不同模型的定价信息和token计费标准
   - 实现token消耗进度条，可视化展示预算使用情况
   - 提供Python和Node.js版本的进度条脚本配置

---

## 9️⃣ 高可用与扩展性
Qwen Coder 必须生成 `docs/high_availability.md`：  
1. 数据库主从复制 / 读写分离  
2. 定时备份策略  
3. 跨区部署（多可用区 / 多 Region）  
4. Redis / CDN 缓存  
5. 消息队列（RocketMQ / Kafka / RabbitMQ / SQS）  

---

## 🔟 推荐目录结构
```
my-project/
│── QWEN.md
│── README.md
│── .gitignore
│── package.json / requirements.txt
│── docker-compose.yml
│── .github/
│   └── workflows/
│       └── ci.yml
│── src/
│   ├── api/
│   ├── services/
│   ├── models/
│   ├── utils/
│   └── config/
│── tests/
│── docs/
│   ├── todos.md
│   ├── completed_todos.md
│   ├── project_structure.md
│   ├── progress.md
│   ├── cloud_deployment.md
│   ├── high_availability.md
│   ├── tech_stack.md
│   └── token_consumption_stats.md
```

---

# 📌 使用流程（数字化步骤）

1️⃣ 在本地新建一个项目文件夹，例如：

```bash
mkdir my-project && cd my-project
```

2️⃣ 在项目根目录新建文件：

```bash
nano QWEN.md
```

3️⃣ 复制上面的 **QWEN.md 配置内容**，粘贴到文件中并保存。

4️⃣ 新建 `docs/` 文件夹：

```bash
mkdir docs
```

5️⃣ 新建占位文件：

```bash
touch docs/todos.md docs/completed_todos.md docs/project_structure.md docs/progress.md docs/cloud_deployment.md docs/high_availability.md docs/tech_stack.md docs/token_consumption_stats.md
```

6️⃣ （可选）初始化 GitHub 仓库：

```bash
git init
git add .
git commit -m "chore: init project with QWEN.md rules"
git branch -M main
git remote add origin <your_repo_url>
git push -u origin main
```

7️⃣ 打开 Qwen Coder / 阿里云开发工具 / 秒哒，Qwen Coder 会自动读取 `QWEN.md` 并执行其中的规则。

8️⃣ 每次开发时：

* Qwen Coder 会扫描 `src/` 和 `tests/`
* 自动更新 `docs/` 里的文件
* 提供 **TODO 清单、进度条、架构文档、云部署配置**

---

# 📦 项目模板结构 (最小可运行示例)

```
my-project/
│── QWEN.md                      # 全局配置规则（核心文件）
│── README.md                    # 项目说明文档
│── .gitignore                   # Git 忽略文件
│── package.json                 # 前端 Node 项目示例（可替换为 requirements.txt）
│── docker-compose.yml           # Docker 容器配置
│── .editorconfig                # 编辑器统一规范
│── .github/
│   └── workflows/
│       └── ci.yml               # GitHub Actions 自动化 CI 配置
│── src/
│   └── index.js                 # 示例代码
│── tests/
│   └── test_sample.js           # 示例测试
│── docs/
│   ├── todos.md                 # 待办任务
│   ├── completed_todos.md       # 已完成任务
│   ├── project_structure.md     # 文件结构与技术栈
│   ├── progress.md              # 实时开发进度
│   ├── cloud_deployment.md      # 云部署配置
│   ├── high_availability.md     # 高可用架构文档
│   ├── tech_stack.md            # 技术栈说明
│   └── token_consumption_stats.md # Token消耗统计
```