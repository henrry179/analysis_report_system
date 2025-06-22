# SQL工作空间管理器使用指南

## 🎯 概述

SQL工作空间管理器是一个专为本地SQL开发和个性化数据集管理设计的综合工具。它帮助您在本地环境中编写SQL代码文件，创建个性化数据集，并通过MySQL数据库完善系统数据。

## ✨ 主要功能

### 📝 SQL代码管理
- **本地SQL文件编写和管理** - 支持queries、schema、procedures、functions等不同类型
- **SQL文件执行** - 直接执行SQL文件并查看结果
- **SQL模板生成** - 提供常用的SQL查询模板
- **查询结果导出** - 支持CSV、JSON、Excel格式导出

### 📊 个性化数据集生成
- **预设数据集类型** - 商业数据、用户数据、产品数据、财务数据
- **自定义数据集** - 根据模板或手动定义结构生成数据
- **数据模板管理** - 保存和重用数据结构模板
- **多格式导出** - 支持CSV、JSON、Excel格式

### 🗄️ 数据库集成
- **MySQL连接管理** - 便捷的数据库连接配置和测试
- **数据导入导出** - 将生成的数据集导入到MySQL数据库
- **数据库操作** - 执行SQL语句，管理数据库表结构

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install pandas numpy faker sqlalchemy pymysql openpyxl
```

### 2. 启动工作空间管理器

```bash
python sql_workspace_manager.py
```

### 3. 快速开始向导

首次使用建议选择"快速开始向导"（选项7），它将引导您：
1. 配置MySQL数据库连接
2. 初始化管理器
3. 创建示例数据集和SQL文件
4. 导入数据到数据库

## 📁 目录结构

运行后会自动创建以下目录结构：

```
├── sql_scripts/           # SQL脚本文件
│   ├── queries/          # 查询语句
│   ├── schema/           # 表结构定义
│   ├── procedures/       # 存储过程
│   └── functions/        # 函数定义
├── custom_datasets/       # 自定义数据集
│   ├── csv/             # CSV格式数据
│   ├── json/            # JSON格式数据
│   └── excel/           # Excel格式数据
├── sql_templates/         # SQL模板
├── dataset_templates/     # 数据集模板
├── exports/              # 导出文件
└── backups/              # 备份文件
```

## 🔧 详细功能说明

### SQL代码管理

#### 创建SQL文件
1. 选择"SQL代码管理"
2. 选择"创建SQL文件"
3. 输入文件名和类型
4. 编写SQL内容

#### 执行SQL文件
1. 选择要执行的SQL文件
2. 系统自动解析并执行SQL语句
3. 查看执行结果和影响行数

#### SQL模板
系统提供以下预设模板：
- `basic_select.sql` - 基础查询模板
- `data_analysis.sql` - 数据分析模板
- `join_query.sql` - 关联查询模板
- `create_index.sql` - 创建索引模板
- `data_validation.sql` - 数据验证模板

### 个性化数据集生成

#### 预设数据集类型

**1. 商业数据集**
```
字段包括：日期、类别、地区、GMV、DAU、订单均价、转化率、
页面浏览量、跳出率、会话时长、广告支出、自然流量占比等
```

**2. 用户数据集**
```
字段包括：用户ID、用户名、邮箱、电话、姓名、性别、年龄、
生日、省份、城市、地址、职业、公司、注册日期、最后登录、
登录次数、总订单数、总金额、平均订单价值、用户等级、
VIP状态、信用评分等
```

**3. 产品数据集**
```
字段包括：产品ID、产品名称、类别、品牌、成本价、售价、
折扣价、库存数量、销售数量、评分、评论数、重量、尺寸、
颜色、上市日期、是否激活、是否推荐、供应商、供应商联系方式等
```

**4. 财务数据集**
```
字段包括：交易ID、交易日期、交易类型、金额、货币、账户ID、
账户类型、账户余额、交易对方、对方账户、描述、分类、
子分类、地点、商户、风险评分、是否可疑、状态等
```

#### 自定义数据集

支持的字段类型：
- `id` - 自动生成的ID
- `string` - 字符串（可指定选项）
- `name` - 姓名
- `email` - 邮箱地址
- `phone` - 电话号码
- `address` - 地址
- `company` - 公司名称
- `integer` - 整数（可指定范围）
- `float` - 浮点数（可指定范围和精度）
- `boolean` - 布尔值
- `date` - 日期
- `datetime` - 日期时间

### 数据库连接配置

#### 快速配置
- 主机：localhost
- 端口：3306
- 用户：root
- 数据库：analysis_system

#### 自定义配置
可以自定义所有连接参数

## 📋 示例用法

### 1. 创建商业分析数据集

```python
# 通过数据集生成器创建
generator = CustomDatasetGenerator()
business_df = generator.create_business_dataset(
    name="my_business_data",
    size=1000,
    date_range=365,
    categories=['电商', '零售', '餐饮'],
    regions=['北京', '上海', '广州']
)
```

### 2. 编写数据分析SQL

```sql
-- 文件：sales_analysis.sql
SELECT 
    DATE(date) as analysis_date,
    category,
    region,
    SUM(gmv) as total_gmv,
    AVG(order_price) as avg_order_price,
    SUM(dau) as total_dau
FROM business_data
WHERE date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
GROUP BY DATE(date), category, region
ORDER BY analysis_date DESC, total_gmv DESC;
```

### 3. 创建自定义数据模板

```json
{
  "customer_id": {
    "type": "id",
    "options": {"prefix": "CUST"}
  },
  "customer_name": {
    "type": "name"
  },
  "age": {
    "type": "integer",
    "options": {"min": 18, "max": 80}
  },
  "city": {
    "type": "string",
    "options": {"choices": ["北京", "上海", "广州", "深圳"]}
  },
  "purchase_amount": {
    "type": "float",
    "options": {"min": 10.0, "max": 5000.0, "decimals": 2}
  }
}
```

## 🎵 30秒轻音乐提醒系统

根据用户规则，系统在完成重要任务后会播放30秒轻音乐提醒：

### 提醒类型
- **重大成就** - 古典轻音乐（工作空间设置完成）
- **代码优化** - 钢琴轻音乐（SQL优化完成）
- **日常任务** - 自然轻音乐（数据导入完成）

### 智能提醒策略
- **工作时间** - 正常音量播放
- **深夜模式** - 仅轻柔语音提醒
- **连续任务** - 延迟播放避免重叠

## 📊 工作空间状态监控

系统提供实时的工作空间状态监控：
- 数据库连接状态
- SQL文件统计（按类型分类）
- 数据集文件统计（按格式分类）
- 数据模板数量

## 🔄 开发进度记录

根据用户规则，每次优化都会记录到README.md：

### 记录格式
```
## 开发进度更新

### 2024-12-19 15:30:45 - SQL工作空间管理器优化
- 模块：SQL代码管理和数据集生成
- 改进点：
  1. 创建了完整的SQL文件管理系统
  2. 实现了个性化数据集生成功能
  3. 集成了MySQL数据库连接和操作
  4. 添加了30秒轻音乐提醒系统
- 技术难点：
  1. SQL语句解析和执行
  2. 多种数据格式的生成和导出
  3. 数据库连接管理和错误处理
- 性能指标：
  1. 支持生成万级数据集
  2. SQL执行响应时间<1秒
  3. 数据导入速度>1000条/秒
```

## 🛠️ 故障排除

### 常见问题

**1. 数据库连接失败**
- 检查MySQL服务是否启动
- 验证用户名和密码
- 确认数据库是否存在

**2. SQL执行错误**
- 检查SQL语法
- 确认表是否存在
- 验证字段名称

**3. 数据生成失败**
- 检查磁盘空间
- 验证文件权限
- 确认依赖包是否安装

## 📈 扩展功能

### 自定义数据生成器
可以扩展CustomDatasetGenerator类添加新的数据类型：

```python
def create_custom_industry_dataset(self, industry_type: str):
    # 根据行业类型生成特定的数据结构
    pass
```

### SQL模板扩展
在sql_templates目录下添加新的SQL模板文件。

### 数据库支持扩展
目前支持MySQL，可以扩展支持PostgreSQL、SQLite等。

## 📞 技术支持

如有问题，请检查：
1. 系统日志输出
2. 数据库连接状态
3. 文件权限设置
4. 依赖包版本

## 🎉 开始使用

现在您可以开始使用SQL工作空间管理器来：
1. 编写和管理本地SQL代码文件
2. 生成个性化的数据集
3. 通过MySQL数据库完善系统数据
4. 享受30秒轻音乐提醒带来的愉悦开发体验

祝您使用愉快！🚀 