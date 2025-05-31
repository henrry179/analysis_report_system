# 综合分析报告-{{ report_date }}

## 核心结论

### GMV负向贡献最大的两个指标

本期GMV环比增长{{ gmv_change_rate }}%，但存在两个主要负向贡献因素：

1. **笔单价**：环比下降{{ order_price_change_rate }}%，贡献度为{{ order_price_contribution }}%，是最大的负向贡献因素
2. **转化率**：环比下降{{ conversion_rate_change }}%，贡献度为{{ conversion_rate_contribution }}%，是第二大负向贡献因素

### 笔单价下滑归因

笔单价下降{{ order_price_change_rate }}%的主要原因：

- 根据基尼系数分析，品类维度的基尼系数({{ category_gini }})显著高于区域维度({{ region_gini }})，说明笔单价的变化主要由品类因素引起
- 进一步分析表明，笔单价下降主要由品类自身笔单价变化导致，贡献度为{{ category_price_contribution }}%
- 笔单价下降最显著的品类包括：
  {% for category in top_declining_categories %}
  - {{ category.name }}：笔单价下降{{ category.decline_rate }}%
  {% endfor %}

### 转化率下滑归因

转化率下降{{ conversion_rate_change }}%的主要原因：

- 区域维度的基尼系数（{{ region_conversion_gini }})高于品类维度（{{ category_conversion_gini }}），说明转化率的变化主要由区域因素引起
- 转化率下降最显著的区域包括：
  {% for region in top_declining_regions %}
  - {{ region.name }}：转化率下降{{ region.decline_rate }}%
  {% endfor %}

## 改进建议

{% for suggestion in improvement_suggestions %}
{{ loop.index }}. {{ suggestion }}
{% endfor %}

## GMV贡献度分析概览

| 项目 | 当前GMV | 上周GMV | 环比变化 |
|------|----------|---------|----------|
| GMV  | {{ current_gmv }}元 | {{ previous_gmv }}元 | {{ gmv_change_rate }}%    |

### GMV贡献度分析

| 指标 | 当前值   | 上周值  | 变化率(%) | 贡献度(%) |
|------|----------|---------|-----------|-----------|
| DAU  | {{ current_dau }}  | {{ previous_dau }} | {{ dau_change_rate }}     | {{ dau_contribution }}   |
| 频次 | {{ current_frequency }}     | {{ previous_frequency }}    | {{ frequency_change_rate }}     | {{ frequency_contribution }}    |
| 笔单价 | {{ current_order_price }}元 | {{ previous_order_price }}元 | {{ order_price_change_rate }}     | {{ order_price_contribution }}    |
| 转化率 | {{ current_conversion_rate }}%    | {{ previous_conversion_rate }}%  | {{ conversion_rate_change }}     | {{ conversion_rate_contribution }}    |

## 笔单价维度分析

### 总体笔单价变化分析

笔单价环比变化{{ order_price_change_rate }}%，主要受以下因素影响：

- 品类自身笔单价变化：贡献度{{ category_price_contribution }}%
- 品类结构变化：贡献度{{ category_structure_contribution }}%

结论：笔单价变化主要由品类自身笔单价变化导致。

### 品类维度分析

| 品类   | 当前笔单价(元) | 上周笔单价(元) | 变化率(%) | 当前销售占比 | 上周销售占比 | 结构变化率(%) | 笔单价变化贡献度 |
|--------|----------------|----------------|-----------|--------------|--------------|---------------|------------------|
{% for category in category_analysis %}
| {{ category.name }}   | {{ category.current_price }}          | {{ category.previous_price }}          | {{ category.change_rate }}     | {{ category.current_share }}%       | {{ category.previous_share }}%       | {{ category.structure_change }}        | {{ category.contribution }}            |
{% endfor %}

## 件单价和件单数分析

### 件单价变化分析

| 品类   | 当前件单价(元) | 上周件单价(元) | 变化率(%) | 贡献度 |
|--------|----------------|----------------|-----------|--------|
{% for category in unit_price_analysis %}
| {{ category.name }}   | {{ category.current_price }}          | {{ category.previous_price }}          | {{ category.change_rate }}     | {{ category.contribution }}  |
{% endfor %}

### 件单数变化分析

| 品类   | 当前件单数 | 上周件单数 | 变化率(%) | 贡献度 |
|--------|------------|------------|-----------|--------|
{% for category in unit_count_analysis %}
| {{ category.name }}   | {{ category.current_count }}       | {{ category.previous_count }}       | {{ category.change_rate }}     | {{ category.contribution }}  |
{% endfor %}

## 区域维度分析

### 笔单价区域分析

| 区域     | 当前笔单价（元） | 上周笔单价（元） | 变化值（元） | 变化率(%) |
|----------|------------------|------------------|--------------|-----------|
{% for region in region_price_analysis %}
| {{ region.name }}     | {{ region.current_price }}            | {{ region.previous_price }}            | {{ region.change_value }}        | {{ region.change_rate }}     |
{% endfor %}

### 转化率区域分析

| 区域     | 当前转化率 | 上周转化率 | 变化值 | 变化率(%) |
|----------|------------|------------|--------|-----------|
{% for region in region_conversion_analysis %}
| {{ region.name }}     | {{ region.current_rate }}%      | {{ region.previous_rate }}%      | {{ region.change_value }}  | {{ region.change_rate }}    |
{% endfor %}

## 可视化分析

### GMV贡献度分析
![GMV贡献度分析]({{ chart_paths.gmv_contribution }})

### 品类分析
![品类分析]({{ chart_paths.category_analysis }})

### 区域分析
![区域分析]({{ chart_paths.region_analysis }}) 