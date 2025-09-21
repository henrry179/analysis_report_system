# Qwen-Coder Token消耗统计表

此表格用于跟踪和统计在项目开发过程中Qwen-Coder的API调用所消耗的token数量及对应的成本。

## Token消耗统计表

| 日期 | 模型名称 | 输入Token数 | 输出Token数 | 总Token数 | 单价（每百万token） | 成本（元） | 累计成本（元） | 备注 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 2025-09-01 | qwen-plus | 800 | 200 | 1000 | 0.0028 | 0.0000028 | 0.0000028 | 代码生成 |
| 2025-09-02 | qwen-max | 1200 | 350 | 1550 | 0.016 | 0.0000248 | 0.0000276 | 复杂逻辑处理 |
| 2025-09-03 | qwen-turbo | 500 | 150 | 650 | 0.0012 | 0.00000078 | 0.00002838 | 简单问答 |

## Token消耗进度条配置

为了直观地展示token消耗情况，可以使用以下ASCII风格的进度条：

```
[====================>.................] 75% (已使用: 750K / 总预算: 1M tokens)
```

### 进度条脚本配置（Python示例）

```python
import math

def display_token_usage_progress(used_tokens, total_budget):
    """
    显示token使用进度条
    
    :param used_tokens: 已使用的token数量
    :param total_budget: 总预算token数量
    """
    progress = used_tokens / total_budget
    bar_length = 40  # 进度条长度
    filled_length = int(bar_length * progress)
    
    bar = '=' * filled_length + '>' + '.' * (bar_length - filled_length - 1)
    percentage = progress * 100
    
    print(f'[ {bar} ] {percentage:.1f}% (已使用: {used_tokens/1000:.0f}K / 总预算: {total_budget/1000000:.0f}M tokens)')

# 使用示例
used_tokens = 750000
total_budget = 1000000
display_token_usage_progress(used_tokens, total_budget)
```

### 进度条脚本配置（Node.js示例）

```javascript
function displayTokenUsageProgress(usedTokens, totalBudget) {
    /**
     * 显示token使用进度条
     * 
     * @param {number} usedTokens - 已使用的token数量
     * @param {number} totalBudget - 总预算token数量
     */
    const progress = usedTokens / totalBudget;
    const barLength = 40; // 进度条长度
    const filledLength = Math.floor(barLength * progress);
    
    const bar = '='.repeat(filledLength) + '>'.concat('.'.repeat(barLength - filledLength - 1));
    const percentage = (progress * 100).toFixed(1);
    
    console.log(`[ ${bar} ] ${percentage}% (已使用: ${Math.floor(usedTokens/1000)}K / 总预算: ${totalBudget/1000000}M tokens)`);
}

// 使用示例
const usedTokens = 750000;
const totalBudget = 1000000;
displayTokenUsageProgress(usedTokens, totalBudget);
```

## 使用说明

1. 每次Qwen-Coder进行API调用后，应记录相关数据到统计表中。
2. 根据项目预算，定期更新进度条以监控token消耗情况。
3. 当token消耗接近预算时，应及时预警并考虑优化策略。