/*
 * 文件名: 03-指标看板大类出货销售.sql
 * 功能: 多省份大类商品出货销售分析
 * 描述: 本脚本统计多省份大类商品的出货额与毛利额，支持本期累计、上周、去年同期多维度对比
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

-- 2. 分析本期累计出货销售数据
-- 2.1 提取本期原始数据
IF OBJECT_ID('tempdb..#data1') IS NOT NULL DROP TABLE #data1; -- 如果临时表已存在则先删除

SELECT 
    companycode,                                -- 公司代码
    CONVERT(VARCHAR(20), date_id, 112) AS mydate, -- 转换为YYYYMMDD格式
    gid,                                        -- 商品ID
    saletotal,                                  -- 出货额
    salemle                                     -- 毛利额
INTO #data1 -- 存入临时表#data1
FROM odsdbfq_result.dbo.sort_out_mout_r WITH (NOLOCK) -- 使用NOLOCK提高查询性能
WHERE companycode IN ('HB','HN','FJ','JX','AH')      -- 筛选包含的省份公司
  AND date_id BETWEEN @sdate AND @edate               -- 使用BETWEEN简化日期范围条件
  AND saletotal <> 0;                                 -- 新增：排除无出货额数据，提高效率

-- 2.2 关联商品分类信息
IF OBJECT_ID('tempdb..#data2') IS NOT NULL DROP TABLE #data2; -- 如果临时表已存在则先删除

SELECT 
    a.*,
    b.scode1 AS 大类编码,                              -- 商品大类编码
    b.sname1 AS 大类名称,                              -- 商品大类名称
    b.scode2 AS 小类编码,                              -- 商品小类编码
    b.sname2 AS 小类名称,                              -- 商品小类名称
    b.code AS 商品编码,                                -- 商品编码
    b.[name] AS 商品名称                              -- 商品名称
INTO #data2 -- 存入临时表#data2
FROM #data1 a
LEFT JOIN odsdbfq_basic.dbo.goodsz b WITH (NOLOCK)    -- 使用NOLOCK提高查询性能
    ON a.gid = b.gid AND a.companycode = b.companycode; -- 按商品ID和公司代码关联

-- 2.3 按大类汇总本期累计数据
SELECT 
    mydate,                                            -- 日期
    RIGHT(mydate,2) AS mydd,                           -- 提取日（两位数）
    companycode,                                       -- 公司代码
    大类编码,                                          -- 商品大类编码
    大类名称,                                          -- 商品大类名称
    SUM(saletotal) AS 出货额,                          -- 汇总出货额
    SUM(salemle) AS 毛利额,                            -- 汇总毛利额
    ROUND(CASE WHEN SUM(saletotal) = 0 THEN 0 
         ELSE SUM(salemle) / SUM(saletotal) * 100 END, 2) AS 毛利率, -- 新增：计算毛利率(%)
    '本期累计' AS 数据类型                             -- 数据类型标记
FROM #data2
GROUP BY mydate, companycode, 大类编码, 大类名称, RIGHT(mydate,2)
ORDER BY companycode, 大类编码, mydate;                -- 新增：添加排序提高数据可读性

-- 3. 分析上周出货销售数据
-- 3.1 提取上周原始数据
IF OBJECT_ID('tempdb..#LW1') IS NOT NULL DROP TABLE #LW1; -- 如果临时表已存在则先删除

SELECT 
    companycode,                                -- 公司代码
    CONVERT(VARCHAR(20), date_id, 112) AS mydate, -- 转换为YYYYMMDD格式
    gid,                                        -- 商品ID
    saletotal,                                  -- 出货额
    salemle                                     -- 毛利额
INTO #LW1 -- 存入临时表#LW1
FROM odsdbfq_result.dbo.sort_out_mout_r WITH (NOLOCK) -- 使用NOLOCK提高查询性能
WHERE companycode IN ('HB','HN','FJ','JX','AH')      -- 筛选包含的省份公司
  AND date_id BETWEEN @LWsdate AND @LWedate           -- 使用BETWEEN简化日期范围条件
  AND saletotal <> 0;                                 -- 新增：排除无出货额数据，提高效率

-- 3.2 关联商品分类信息
IF OBJECT_ID('tempdb..#LW2') IS NOT NULL DROP TABLE #LW2; -- 如果临时表已存在则先删除

SELECT 
    a.*,
    b.scode1 AS 大类编码,                              -- 商品大类编码
    b.sname1 AS 大类名称,                              -- 商品大类名称
    b.scode2 AS 小类编码,                              -- 商品小类编码
    b.sname2 AS 小类名称,                              -- 商品小类名称
    b.code AS 商品编码,                                -- 商品编码
    b.[name] AS 商品名称                              -- 商品名称
INTO #LW2 -- 存入临时表#LW2
FROM #LW1 a
LEFT JOIN odsdbfq_basic.dbo.goodsz b WITH (NOLOCK)    -- 使用NOLOCK提高查询性能
    ON a.gid = b.gid AND a.companycode = b.companycode; -- 按商品ID和公司代码关联

-- 3.3 按大类汇总上周数据
SELECT 
    mydate,                                            -- 日期
    RIGHT(mydate,2) AS mydd,                           -- 提取日（两位数）
    companycode,                                       -- 公司代码
    大类编码,                                          -- 商品大类编码
    大类名称,                                          -- 商品大类名称
    SUM(saletotal) AS 出货额,                          -- 汇总出货额
    SUM(salemle) AS 毛利额,                            -- 汇总毛利额
    ROUND(CASE WHEN SUM(saletotal) = 0 THEN 0 
         ELSE SUM(salemle) / SUM(saletotal) * 100 END, 2) AS 毛利率, -- 新增：计算毛利率(%)
    '上周' AS 数据类型                                 -- 数据类型标记
FROM #LW2
GROUP BY mydate, companycode, 大类编码, 大类名称, RIGHT(mydate,2)
ORDER BY companycode, 大类编码, mydate;                -- 新增：添加排序提高数据可读性

-- 4. 分析去年同期出货销售数据（新增）
-- 4.1 提取去年同期原始数据
IF OBJECT_ID('tempdb..#LY1') IS NOT NULL DROP TABLE #LY1; -- 如果临时表已存在则先删除

SELECT 
    companycode,                                -- 公司代码
    CONVERT(VARCHAR(20), date_id, 112) AS mydate, -- 转换为YYYYMMDD格式
    gid,                                        -- 商品ID
    saletotal,                                  -- 出货额
    salemle                                     -- 毛利额
INTO #LY1 -- 存入临时表#LY1
FROM odsdbfq_result.dbo.sort_out_mout_r WITH (NOLOCK) -- 使用NOLOCK提高查询性能
WHERE companycode IN ('HB','HN','FJ','JX','AH')      -- 筛选包含的省份公司
  AND date_id BETWEEN @LYsdate AND @LYedate           -- 使用BETWEEN简化日期范围条件
  AND saletotal <> 0;                                 -- 新增：排除无出货额数据，提高效率

-- 4.2 关联商品分类信息
IF OBJECT_ID('tempdb..#LY2') IS NOT NULL DROP TABLE #LY2; -- 如果临时表已存在则先删除

SELECT 
    a.*,
    b.scode1 AS 大类编码,                              -- 商品大类编码
    b.sname1 AS 大类名称,                              -- 商品大类名称
    b.scode2 AS 小类编码,                              -- 商品小类编码
    b.sname2 AS 小类名称,                              -- 商品小类名称
    b.code AS 商品编码,                                -- 商品编码
    b.[name] AS 商品名称                              -- 商品名称
INTO #LY2 -- 存入临时表#LY2
FROM #LY1 a
LEFT JOIN odsdbfq_basic.dbo.goodsz b WITH (NOLOCK)    -- 使用NOLOCK提高查询性能
    ON a.gid = b.gid AND a.companycode = b.companycode; -- 按商品ID和公司代码关联

-- 4.3 按大类汇总去年同期数据
SELECT 
    mydate,                                            -- 日期
    RIGHT(mydate,2) AS mydd,                           -- 提取日（两位数）
    companycode,                                       -- 公司代码
    大类编码,                                          -- 商品大类编码
    大类名称,                                          -- 商品大类名称
    SUM(saletotal) AS 出货额,                          -- 汇总出货额
    SUM(salemle) AS 毛利额,                            -- 汇总毛利额
    ROUND(CASE WHEN SUM(saletotal) = 0 THEN 0 
         ELSE SUM(salemle) / SUM(saletotal) * 100 END, 2) AS 毛利率, -- 新增：计算毛利率(%)
    '去年同期' AS 数据类型                             -- 数据类型标记
FROM #LY2
GROUP BY mydate, companycode, 大类编码, 大类名称, RIGHT(mydate,2)
ORDER BY companycode, 大类编码, mydate;                -- 新增：添加排序提高数据可读性

-- 5. 汇总对比分析（新增）
-- 按大类汇总本期累计、上周同期和去年同期数据
SELECT 
    '汇总分析' AS 分析维度,
    companycode AS 公司代码,
    大类编码,
    大类名称,
    SUM(CASE WHEN 数据类型 = '本期累计' THEN 出货额 ELSE 0 END) AS 本期累计出货额,
    SUM(CASE WHEN 数据类型 = '上周' THEN 出货额 ELSE 0 END) AS 上周出货额,
    SUM(CASE WHEN 数据类型 = '去年同期' THEN 出货额 ELSE 0 END) AS 去年同期出货额,
    SUM(CASE WHEN 数据类型 = '本期累计' THEN 毛利额 ELSE 0 END) AS 本期累计毛利额,
    SUM(CASE WHEN 数据类型 = '上周' THEN 毛利额 ELSE 0 END) AS 上周毛利额,
    SUM(CASE WHEN 数据类型 = '去年同期' THEN 毛利额 ELSE 0 END) AS 去年同期毛利额
FROM (
    -- 合并本期、上周、去年同期数据
    SELECT companycode, 大类编码, 大类名称, 出货额, 毛利额, 数据类型
    FROM #data2
    GROUP BY companycode, 大类编码, 大类名称, 出货额, 毛利额, 数据类型
    UNION ALL
    SELECT companycode, 大类编码, 大类名称, 出货额, 毛利额, 数据类型
    FROM #LW2
    GROUP BY companycode, 大类编码, 大类名称, 出货额, 毛利额, 数据类型
    UNION ALL
    SELECT companycode, 大类编码, 大类名称, 出货额, 毛利额, 数据类型
    FROM #LY2
    GROUP BY companycode, 大类编码, 大类名称, 出货额, 毛利额, 数据类型
) AS combined_data
GROUP BY companycode, 大类编码, 大类名称
ORDER BY companycode, 大类编码;

-- 6. 清理临时表（提高性能）
DROP TABLE IF EXISTS #data1;
DROP TABLE IF EXISTS #data2;
DROP TABLE IF EXISTS #LW1;
DROP TABLE IF EXISTS #LW2;
DROP TABLE IF EXISTS #LY1;
DROP TABLE IF EXISTS #LY2;

/*
 * 代码优化说明：
 * 1. 添加了详细的文件头注释，说明脚本功能和目的
 * 2. 使用BETWEEN替代>=和<=来简化日期范围条件
 * 3. 添加了更详细的中文注释，解释每个步骤的目的和逻辑
 * 4. 添加了saletotal <> 0筛选条件，排除无意义数据提高效率
 * 5. 新增了毛利率计算，提供更多分析维度
 * 6. 新增了去年同期数据分析，完善对比体系
 * 7. 新增了汇总对比分析，方便整体把握趋势
 * 8. 添加了ORDER BY排序，提高数据可读性
 * 9. 启用临时表清理，优化资源使用
 * 10. 保持了WITH (NOLOCK)提示以提高查询性能
 */