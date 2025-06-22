/*
 * 文件名: 04-指标看板日销数据.sql
 * 功能: 多省份门店日销售数据分析
 * 描述: 本脚本统计多省份门店的日销售数据，按门店类型分组，支持本期、上周、去年同期多维度对比
 */

-- 1. 定义日期参数
DECLARE @sdate DATE;    -- 本期开始日期
DECLARE @edate DATE;    -- 本期结束日期
DECLARE @LYsdate DATE;  -- 去年同期开始日期
DECLARE @LYedate DATE;  -- 去年同期结束日期
DECLARE @LWsdate DATE;  -- 上周开始日期
DECLARE @LWedate DATE;  -- 上周结束日期

-- 智能设置日期变量（自动计算相关日期）
SET @sdate = CONVERT(DATE, DATEADD(MONTH, DATEDIFF(MONTH, 0, GETDATE()-1), 0)); -- 本月初
SET @edate = DATEADD(DAY, DATEDIFF(DAY, 0, GETDATE()-1), 0);                    -- 昨日
SET @LWedate = DATEADD(DAY, -6, GETDATE()-1);                                   -- 上周结束日期（前7天的结束）
SET @LWsdate = DATEADD(DAY, -6, @LWedate);                                      -- 上周开始日期（再往前7天的开始）
SET @LYsdate = DATEADD(YEAR, -1, @sdate);                                       -- 去年同期开始日期
SET @LYedate = DATEADD(YEAR, -1, @edate);                                       -- 去年同期结束日期

-- 输出日期参数（便于调试和确认）
SELECT 
    @sdate AS 开始日期,
    @edate AS 结束日期,
    @LWsdate AS 上周开始日期,
    @LWedate AS 上周结束日期,
    @LYsdate AS 去年开始日期,
    @LYedate AS 去年结束日期;

-- 2. 准备门店基础信息
-- 2.1 提取门店基础信息
IF OBJECT_ID('tempdb..#stinf') IS NOT NULL DROP TABLE #stinf; -- 如果临时表已存在则先删除

SELECT * 
INTO #stinf -- 存入临时表#stinf
FROM odsdbfq_basic.dbo.store WITH (NOLOCK) -- 使用NOLOCK提高查询性能
WHERE companycode IN ('HB','HN','FJ','JX','AH'); -- 筛选包含的省份公司

-- 2.2 标准化门店类型（使门店类型数据更统一规范）
UPDATE #stinf
SET shoptype = '标准门店' -- 将符合条件的门店类型统一设置为"标准门店"
WHERE code IN (
    SELECT code FROM odsdbfqbi.dbo.xsb WITH (NOLOCK) -- 从销售表中获取标准门店编码
) AND companycode IN ('HB','HN','FJ','JX','AH');

UPDATE #stinf
SET shoptype = '标准门店' -- 将直营门店类型统一设置为"标准门店"
WHERE shoptype = '直营';

-- 2.3 创建门店类型索引（优化后续查询性能）
IF NOT EXISTS (SELECT * FROM tempdb.sys.indexes WHERE name = 'idx_stinf_code' AND object_id = OBJECT_ID('tempdb..#stinf'))
BEGIN
    CREATE INDEX idx_stinf_code ON #stinf(companycode, code); -- 创建复合索引提高关联查询性能
END

-- 3. 分析本期日销售数据
-- 3.1 提取本期原始数据
IF OBJECT_ID('tempdb..#data') IS NOT NULL DROP TABLE #data; -- 如果临时表已存在则先删除

SELECT 
    CONVERT(VARCHAR(20), rq, 112) AS 销售日期,           -- 转换为YYYYMMDD格式
    companycode,                                       -- 公司代码
    code AS storecode,                                 -- 门店编码
    COUNT(DISTINCT rq) AS 天数,                         -- 统计经营天数
    SUM(noxse) AS 销售额,                               -- 统计销售额
    SUM(laike) AS 来客数,                               -- 新增：统计来客数
    CASE WHEN SUM(laike) > 0 THEN SUM(noxse) / SUM(laike) ELSE 0 END AS 客单价 -- 新增：计算客单价
INTO #data -- 存入临时表#data
FROM odsdbfq_result.dbo.m_stsale WITH (NOLOCK) -- 使用NOLOCK提高查询性能
WHERE rq BETWEEN @sdate AND @edate -- 使用BETWEEN简化日期范围条件
  AND companycode IN ('HB','HN','FJ','JX','AH') -- 筛选包含的省份公司
  AND noxse > 0 -- 仅包含有效销售额（大于0）
GROUP BY companycode, code, CONVERT(VARCHAR(20), rq, 112);

-- 3.2 按门店类型汇总本期数据
SELECT 
    销售日期,                                           -- 销售日期
    RIGHT(销售日期,2) AS mydd,                          -- 提取日（两位数）
    b.shoptype AS 门店类型,                             -- 门店类型
    a.companycode,                                     -- 公司代码
    COUNT(DISTINCT storecode) AS 门店数,                -- 统计门店数量
    SUM(天数) AS 经营天数,                              -- 统计经营天数
    SUM(销售额) AS 销售额,                              -- 统计销售额
    SUM(来客数) AS 来客数,                              -- 新增：统计来客数
    CASE WHEN SUM(来客数) > 0 THEN ROUND(SUM(销售额) / SUM(来客数), 2) ELSE 0 END AS 客单价, -- 新增：计算客单价
    ROUND(SUM(销售额) / COUNT(DISTINCT storecode), 2) AS 店均销售额, -- 新增：计算店均销售额
    '本期' AS 数据类型                                   -- 数据类型标记
FROM #data a
LEFT JOIN #stinf b WITH (NOLOCK) ON a.companycode = b.companycode AND a.storecode = b.code
WHERE b.shoptype IS NOT NULL -- 排除未知门店类型数据
GROUP BY b.shoptype, a.companycode, 销售日期, RIGHT(销售日期,2)
ORDER BY a.companycode, 门店类型, 销售日期; -- 添加排序提高数据可读性

-- 4. 分析上周日销售数据
-- 4.1 提取上周原始数据
IF OBJECT_ID('tempdb..#lwdata') IS NOT NULL DROP TABLE #lwdata; -- 如果临时表已存在则先删除

SELECT 
    CONVERT(VARCHAR(20), rq, 112) AS 销售日期,           -- 转换为YYYYMMDD格式
    companycode,                                       -- 公司代码
    code AS storecode,                                 -- 门店编码
    COUNT(DISTINCT rq) AS 天数,                         -- 统计经营天数
    SUM(noxse) AS 销售额,                               -- 统计销售额
    SUM(laike) AS 来客数,                               -- 新增：统计来客数
    CASE WHEN SUM(laike) > 0 THEN SUM(noxse) / SUM(laike) ELSE 0 END AS 客单价 -- 新增：计算客单价
INTO #lwdata -- 存入临时表#lwdata
FROM odsdbfq_result.dbo.m_stsale WITH (NOLOCK) -- 使用NOLOCK提高查询性能
WHERE rq BETWEEN @LWsdate AND @LWedate -- 使用BETWEEN简化日期范围条件
  AND companycode IN ('HB','HN','FJ','JX','AH') -- 筛选包含的省份公司
  AND noxse > 0 -- 仅包含有效销售额（大于0）
GROUP BY companycode, code, CONVERT(VARCHAR(20), rq, 112);

-- 4.2 按门店类型汇总上周数据
SELECT 
    销售日期,                                           -- 销售日期
    RIGHT(销售日期,2) AS mydd,                          -- 提取日（两位数）
    b.shoptype AS 门店类型,                             -- 门店类型
    a.companycode,                                     -- 公司代码
    COUNT(DISTINCT storecode) AS 门店数,                -- 统计门店数量
    SUM(天数) AS 经营天数,                              -- 统计经营天数
    SUM(销售额) AS 销售额,                              -- 统计销售额
    SUM(来客数) AS 来客数,                              -- 新增：统计来客数
    CASE WHEN SUM(来客数) > 0 THEN ROUND(SUM(销售额) / SUM(来客数), 2) ELSE 0 END AS 客单价, -- 新增：计算客单价
    ROUND(SUM(销售额) / COUNT(DISTINCT storecode), 2) AS 店均销售额, -- 新增：计算店均销售额
    '上周' AS 数据类型                                   -- 数据类型标记
FROM #lwdata a
LEFT JOIN #stinf b WITH (NOLOCK) ON a.companycode = b.companycode AND a.storecode = b.code
WHERE b.shoptype IS NOT NULL -- 排除未知门店类型数据
GROUP BY b.shoptype, a.companycode, 销售日期, RIGHT(销售日期,2)
ORDER BY a.companycode, 门店类型, 销售日期; -- 添加排序提高数据可读性

-- 5. 分析去年同期日销售数据（新增）
-- 5.1 提取去年同期原始数据
IF OBJECT_ID('tempdb..#lydata') IS NOT NULL DROP TABLE #lydata; -- 如果临时表已存在则先删除

SELECT 
    CONVERT(VARCHAR(20), rq, 112) AS 销售日期,           -- 转换为YYYYMMDD格式
    companycode,                                       -- 公司代码
    code AS storecode,                                 -- 门店编码
    COUNT(DISTINCT rq) AS 天数,                         -- 统计经营天数
    SUM(noxse) AS 销售额,                               -- 统计销售额
    SUM(laike) AS 来客数,                               -- 新增：统计来客数
    CASE WHEN SUM(laike) > 0 THEN SUM(noxse) / SUM(laike) ELSE 0 END AS 客单价 -- 新增：计算客单价
INTO #lydata -- 存入临时表#lydata
FROM odsdbfq_result.dbo.m_stsale WITH (NOLOCK) -- 使用NOLOCK提高查询性能
WHERE rq BETWEEN @LYsdate AND @LYedate -- 使用BETWEEN简化日期范围条件
  AND companycode IN ('HB','HN','FJ','JX','AH') -- 筛选包含的省份公司
  AND noxse > 0 -- 仅包含有效销售额（大于0）
GROUP BY companycode, code, CONVERT(VARCHAR(20), rq, 112);

-- 5.2 按门店类型汇总去年同期数据
SELECT 
    销售日期,                                           -- 销售日期
    RIGHT(销售日期,2) AS mydd,                          -- 提取日（两位数）
    b.shoptype AS 门店类型,                             -- 门店类型
    a.companycode,                                     -- 公司代码
    COUNT(DISTINCT storecode) AS 门店数,                -- 统计门店数量
    SUM(天数) AS 经营天数,                              -- 统计经营天数
    SUM(销售额) AS 销售额,                              -- 统计销售额
    SUM(来客数) AS 来客数,                              -- 新增：统计来客数
    CASE WHEN SUM(来客数) > 0 THEN ROUND(SUM(销售额) / SUM(来客数), 2) ELSE 0 END AS 客单价, -- 新增：计算客单价
    ROUND(SUM(销售额) / COUNT(DISTINCT storecode), 2) AS 店均销售额, -- 新增：计算店均销售额
    '去年同期' AS 数据类型                               -- 数据类型标记
FROM #lydata a
LEFT JOIN #stinf b WITH (NOLOCK) ON a.companycode = b.companycode AND a.storecode = b.code
WHERE b.shoptype IS NOT NULL -- 排除未知门店类型数据
GROUP BY b.shoptype, a.companycode, 销售日期, RIGHT(销售日期,2)
ORDER BY a.companycode, 门店类型, 销售日期; -- 添加排序提高数据可读性

-- 6. 综合销售数据分析（新增）
-- 6.1 汇总三个时间维度的数据进行交叉对比
SELECT 
    '销售分析' AS 分析维度,
    门店类型,
    companycode,
    SUM(CASE WHEN 数据类型 = '本期' THEN 销售额 ELSE 0 END) AS 本期销售额,
    SUM(CASE WHEN 数据类型 = '上周' THEN 销售额 ELSE 0 END) AS 上周销售额,
    SUM(CASE WHEN 数据类型 = '去年同期' THEN 销售额 ELSE 0 END) AS 去年销售额,
    CASE 
        WHEN SUM(CASE WHEN 数据类型 = '上周' THEN 销售额 ELSE 0 END) > 0 
        THEN ROUND((SUM(CASE WHEN 数据类型 = '本期' THEN 销售额 ELSE 0 END) - 
                  SUM(CASE WHEN 数据类型 = '上周' THEN 销售额 ELSE 0 END)) / 
                  SUM(CASE WHEN 数据类型 = '上周' THEN 销售额 ELSE 0 END) * 100, 2)
        ELSE 0
    END AS 环比增长率,
    CASE 
        WHEN SUM(CASE WHEN 数据类型 = '去年同期' THEN 销售额 ELSE 0 END) > 0 
        THEN ROUND((SUM(CASE WHEN 数据类型 = '本期' THEN 销售额 ELSE 0 END) - 
                  SUM(CASE WHEN 数据类型 = '去年同期' THEN 销售额 ELSE 0 END)) / 
                  SUM(CASE WHEN 数据类型 = '去年同期' THEN 销售额 ELSE 0 END) * 100, 2)
        ELSE 0
    END AS 同比增长率,
    SUM(CASE WHEN 数据类型 = '本期' THEN 门店数 ELSE 0 END) AS 本期门店数,
    SUM(CASE WHEN 数据类型 = '去年同期' THEN 门店数 ELSE 0 END) AS 去年门店数,
    SUM(CASE WHEN 数据类型 = '本期' THEN 来客数 ELSE 0 END) AS 本期来客数,
    SUM(CASE WHEN 数据类型 = '去年同期' THEN 来客数 ELSE 0 END) AS 去年来客数,
    SUM(CASE WHEN 数据类型 = '本期' THEN 客单价 ELSE 0 END) AS 本期客单价,
    SUM(CASE WHEN 数据类型 = '去年同期' THEN 客单价 ELSE 0 END) AS 去年客单价
FROM (
    -- 合并本期、上周、去年同期数据
    SELECT 门店类型, companycode, 销售额, 门店数, 来客数, 客单价, 数据类型
    FROM (
        SELECT 门店类型, companycode, SUM(销售额) AS 销售额, COUNT(DISTINCT storecode) AS 门店数, 
               SUM(来客数) AS 来客数, AVG(客单价) AS 客单价, 数据类型
        FROM #data a
        LEFT JOIN #stinf b WITH (NOLOCK) ON a.companycode = b.companycode AND a.storecode = b.code
        WHERE b.shoptype IS NOT NULL
        GROUP BY 门店类型, companycode, 数据类型
    ) t1
    UNION ALL
    SELECT 门店类型, companycode, 销售额, 门店数, 来客数, 客单价, 数据类型
    FROM (
        SELECT 门店类型, companycode, SUM(销售额) AS 销售额, COUNT(DISTINCT storecode) AS 门店数, 
               SUM(来客数) AS 来客数, AVG(客单价) AS 客单价, 数据类型
        FROM #lwdata a
        LEFT JOIN #stinf b WITH (NOLOCK) ON a.companycode = b.companycode AND a.storecode = b.code
        WHERE b.shoptype IS NOT NULL
        GROUP BY 门店类型, companycode, 数据类型
    ) t2
    UNION ALL
    SELECT 门店类型, companycode, 销售额, 门店数, 来客数, 客单价, 数据类型
    FROM (
        SELECT 门店类型, companycode, SUM(销售额) AS 销售额, COUNT(DISTINCT storecode) AS 门店数, 
               SUM(来客数) AS 来客数, AVG(客单价) AS 客单价, 数据类型
        FROM #lydata a
        LEFT JOIN #stinf b WITH (NOLOCK) ON a.companycode = b.companycode AND a.storecode = b.code
        WHERE b.shoptype IS NOT NULL
        GROUP BY 门店类型, companycode, 数据类型
    ) t3
) AS combined_data
GROUP BY 门店类型, companycode
ORDER BY companycode, 门店类型;

-- 7. 清理临时表（提高性能）
DROP TABLE IF EXISTS #stinf;
DROP TABLE IF EXISTS #data;
DROP TABLE IF EXISTS #lwdata;
DROP TABLE IF EXISTS #lydata;

/*
 * 代码优化说明：
 * 1. 添加了详细的文件头注释，说明脚本功能和目的
 * 2. 使用BETWEEN替代>=和<=来简化日期范围条件
 * 3. 添加了更详细的中文注释，解释每个步骤的目的和逻辑
 * 4. 在门店基础信息表上创建索引，提高关联查询性能
 * 5. 新增了来客数和客单价统计，提供更多分析维度
 * 6. 新增了店均销售额计算，便于门店绩效分析
 * 7. 新增了去年同期数据分析，完善对比体系
 * 8. 新增了综合销售数据分析，计算环比和同比增长率
 * 9. 添加了ORDER BY排序，提高数据可读性
 * 10. 启用临时表清理，优化资源使用
 * 11. 保持了WITH (NOLOCK)提示以提高查询性能
 */