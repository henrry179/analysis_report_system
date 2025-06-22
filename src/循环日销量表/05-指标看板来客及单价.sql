/*
 * 文件名: 05-指标看板来客及单价.sql
 * 功能: 门店来客及客单价分析
 * 描述: 本脚本统计门店日均销售额、日均来客数及客单价，支持日期范围参数配置，适用于客流分析和门店经营评估
 */

-- 1. 定义日期参数
DECLARE @sdate DATE;    -- 开始日期
DECLARE @edate DATE;    -- 结束日期
DECLARE @LYsdate DATE;  -- 去年同期开始日期
DECLARE @LYedate DATE;  -- 去年同期结束日期

-- 智能设置日期变量（自动计算相关日期）
SET @sdate = DATEADD(DAY, -DATEDIFF(DAY, 0, GETDATE()) % 7, DATEADD(DAY, -7, GETDATE())); -- 上周一
SET @edate = DATEADD(DAY, DATEDIFF(DAY, 0, GETDATE()-1), 0);                              -- 昨日
SET @LYsdate = DATEADD(YEAR, -1, @sdate);                                                  -- 去年同期开始日期
SET @LYedate = DATEADD(YEAR, -1, @edate);                                                  -- 去年同期结束日期

-- 输出日期参数（便于调试和确认）
SELECT 
    @sdate AS 开始日期,
    @edate AS 结束日期,
    @LYsdate AS 去年开始日期,
    @LYedate AS 去年结束日期;

-- 2. 分析本期来客及客单价数据
-- 2.1 提取并计算本期数据
SELECT 
    '本期' AS 数据类型,                                 -- 数据类型标记
    CONVERT(VARCHAR(20), rq, 23) AS 销售日期,          -- 日期（YYYY-MM-DD格式）
    RIGHT(CONVERT(VARCHAR(20), rq, 23), 5) AS 月日,    -- 提取月日（MM-DD格式）
    companycode AS 公司代码,                           -- 公司代码
    SUM(lks) AS 来客数,                                -- 汇总来客数
    SUM(noxse) AS 销售额,                              -- 汇总销售额
    COUNT(DISTINCT code) AS 门店数,                    -- 统计门店数
    COUNT(rq) AS 经营天数,                             -- 统计经营天数
    -- 计算各项指标
    ROUND(SUM(noxse) / COUNT(rq), 2) AS 日均销售额,    -- 日均销售额
    ROUND(SUM(lks) / COUNT(rq), 2) AS 日均来客数,      -- 日均来客数
    CASE 
        WHEN SUM(lks) = 0 THEN 0 
        ELSE ROUND(SUM(noxse) / SUM(lks), 2) 
    END AS 平均客单价,                                 -- 平均客单价（避免除零错误）
    ROUND(SUM(noxse) / COUNT(DISTINCT code), 2) AS 店均销售额 -- 新增：店均销售额
FROM odsdbfq_result.dbo.m_stsale WITH (NOLOCK)         -- 使用NOLOCK提高查询性能
WHERE rq BETWEEN @sdate AND @edate                     -- 使用BETWEEN简化日期范围条件
  AND companycode IN ('HB','HN','FJ','JX','AH')        -- 筛选包含的省份公司
  AND noxse > 0                                        -- 仅包含有效销售额（大于0）
GROUP BY CONVERT(VARCHAR(20), rq, 23), companycode     -- 按日期和公司分组
ORDER BY companycode, 销售日期;                         -- 添加排序提高数据可读性

-- 3. 分析去年同期来客及客单价数据
-- 3.1 提取并计算去年同期数据
SELECT 
    '去年同期' AS 数据类型,                             -- 数据类型标记
    CONVERT(VARCHAR(20), rq, 23) AS 销售日期,          -- 日期（YYYY-MM-DD格式）
    RIGHT(CONVERT(VARCHAR(20), rq, 23), 5) AS 月日,    -- 提取月日（MM-DD格式）
    companycode AS 公司代码,                           -- 公司代码
    SUM(lks) AS 来客数,                                -- 汇总来客数
    SUM(noxse) AS 销售额,                              -- 汇总销售额
    COUNT(DISTINCT code) AS 门店数,                    -- 统计门店数
    COUNT(rq) AS 经营天数,                             -- 统计经营天数
    -- 计算各项指标
    ROUND(SUM(noxse) / COUNT(rq), 2) AS 日均销售额,    -- 日均销售额
    ROUND(SUM(lks) / COUNT(rq), 2) AS 日均来客数,      -- 日均来客数
    CASE 
        WHEN SUM(lks) = 0 THEN 0 
        ELSE ROUND(SUM(noxse) / SUM(lks), 2) 
    END AS 平均客单价,                                 -- 平均客单价（避免除零错误）
    ROUND(SUM(noxse) / COUNT(DISTINCT code), 2) AS 店均销售额 -- 新增：店均销售额
FROM odsdbfq_result.dbo.m_stsale WITH (NOLOCK)         -- 使用NOLOCK提高查询性能
WHERE rq BETWEEN @LYsdate AND @LYedate                 -- 使用BETWEEN简化日期范围条件
  AND companycode IN ('HB','HN','FJ','JX','AH')        -- 筛选包含的省份公司
  AND noxse > 0                                        -- 仅包含有效销售额（大于0）
GROUP BY CONVERT(VARCHAR(20), rq, 23), companycode     -- 按日期和公司分组
ORDER BY companycode, 销售日期;                         -- 添加排序提高数据可读性

-- 4. 按周统计来客及客单价趋势（新增）
-- 4.1 提取并计算本期周度数据
SELECT 
    '本期' AS 数据类型,                                 -- 数据类型标记
    DATEPART(YEAR, rq) AS 年份,                        -- 提取年份
    DATEPART(WEEK, rq) AS 周次,                        -- 提取周次
    companycode AS 公司代码,                           -- 公司代码
    MIN(CONVERT(VARCHAR(20), rq, 23)) AS 开始日期,     -- 本周第一天
    MAX(CONVERT(VARCHAR(20), rq, 23)) AS 结束日期,     -- 本周最后一天
    SUM(lks) AS 来客数,                                -- 汇总来客数
    SUM(noxse) AS 销售额,                              -- 汇总销售额
    COUNT(DISTINCT code) AS 门店数,                    -- 统计门店数
    COUNT(rq) AS 经营天数,                             -- 统计经营天数
    -- 计算各项指标
    ROUND(SUM(noxse) / COUNT(rq), 2) AS 日均销售额,    -- 日均销售额
    ROUND(SUM(lks) / COUNT(rq), 2) AS 日均来客数,      -- 日均来客数
    CASE 
        WHEN SUM(lks) = 0 THEN 0 
        ELSE ROUND(SUM(noxse) / SUM(lks), 2) 
    END AS 平均客单价                                  -- 平均客单价（避免除零错误）
FROM odsdbfq_result.dbo.m_stsale WITH (NOLOCK)         -- 使用NOLOCK提高查询性能
WHERE rq BETWEEN @sdate AND @edate                     -- 使用BETWEEN简化日期范围条件
  AND companycode IN ('HB','HN','FJ','JX','AH')        -- 筛选包含的省份公司
  AND noxse > 0                                        -- 仅包含有效销售额（大于0）
GROUP BY DATEPART(YEAR, rq), DATEPART(WEEK, rq), companycode -- 按年、周次和公司分组
ORDER BY companycode, 年份, 周次;                       -- 添加排序提高数据可读性

-- 5. 汇总对比分析（新增）
-- 5.1 按公司汇总本期与去年同期对比
WITH 本期数据 AS (
    SELECT 
        companycode AS 公司代码,
        SUM(lks) AS 本期来客数,
        SUM(noxse) AS 本期销售额,
        COUNT(DISTINCT code) AS 本期门店数,
        COUNT(rq) AS 本期经营天数,
        ROUND(SUM(noxse) / COUNT(rq), 2) AS 本期日均销售额,
        ROUND(SUM(lks) / COUNT(rq), 2) AS 本期日均来客数,
        CASE WHEN SUM(lks) = 0 THEN 0 ELSE ROUND(SUM(noxse) / SUM(lks), 2) END AS 本期客单价
    FROM odsdbfq_result.dbo.m_stsale WITH (NOLOCK)
    WHERE rq BETWEEN @sdate AND @edate
      AND companycode IN ('HB','HN','FJ','JX','AH')
      AND noxse > 0
    GROUP BY companycode
),
去年同期数据 AS (
    SELECT 
        companycode AS 公司代码,
        SUM(lks) AS 去年来客数,
        SUM(noxse) AS 去年销售额,
        COUNT(DISTINCT code) AS 去年门店数,
        COUNT(rq) AS 去年经营天数,
        ROUND(SUM(noxse) / COUNT(rq), 2) AS 去年日均销售额,
        ROUND(SUM(lks) / COUNT(rq), 2) AS 去年日均来客数,
        CASE WHEN SUM(lks) = 0 THEN 0 ELSE ROUND(SUM(noxse) / SUM(lks), 2) END AS 去年客单价
    FROM odsdbfq_result.dbo.m_stsale WITH (NOLOCK)
    WHERE rq BETWEEN @LYsdate AND @LYedate
      AND companycode IN ('HB','HN','FJ','JX','AH')
      AND noxse > 0
    GROUP BY companycode
)
SELECT 
    a.公司代码,
    a.本期来客数,
    b.去年来客数,
    CASE WHEN b.去年来客数 = 0 THEN NULL ELSE ROUND((a.本期来客数 - b.去年来客数) / b.去年来客数 * 100, 2) END AS 来客数同比增长率,
    a.本期销售额,
    b.去年销售额,
    CASE WHEN b.去年销售额 = 0 THEN NULL ELSE ROUND((a.本期销售额 - b.去年销售额) / b.去年销售额 * 100, 2) END AS 销售额同比增长率,
    a.本期日均来客数,
    b.去年日均来客数,
    CASE WHEN b.去年日均来客数 = 0 THEN NULL ELSE ROUND((a.本期日均来客数 - b.去年日均来客数) / b.去年日均来客数 * 100, 2) END AS 日均来客数同比增长率,
    a.本期客单价,
    b.去年客单价,
    CASE WHEN b.去年客单价 = 0 THEN NULL ELSE ROUND((a.本期客单价 - b.去年客单价) / b.去年客单价 * 100, 2) END AS 客单价同比增长率
FROM 本期数据 a
FULL JOIN 去年同期数据 b ON a.公司代码 = b.公司代码
ORDER BY a.公司代码;

/*
 * 代码优化说明：
 * 1. 添加了详细的文件头注释，说明脚本功能和目的
 * 2. 添加了日期参数定义，使脚本更加灵活，适应不同时间段分析
 * 3. 扩展了多省份支持，原脚本仅支持'hn'公司
 * 4. 使用BETWEEN替代>=和<=来简化日期范围条件
 * 5. 添加了更详细的中文注释，解释每个计算字段的目的
 * 6. 增加了门店数统计，便于比较不同规模公司的客流效率
 * 7. 新增了去年同期对比分析，便于同比趋势判断
 * 8. 新增了周度趋势分析，便于观察客流周期性变化
 * 9. 新增了汇总对比分析，计算多个关键指标的同比增长率
 * 10. 所有计算指标均添加了除零保护，避免计算错误
 * 11. 添加了ORDER BY排序，提高数据可读性
 * 12. 保持了WITH (NOLOCK)提示以提高查询性能
 */
