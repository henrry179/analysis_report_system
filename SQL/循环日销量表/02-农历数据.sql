/*
 * 文件名: 02-农历数据.sql
 * 功能: 农历销售数据对比分析
 * 描述: 本脚本根据农历日期对齐，比较当前年度与去年同期的销售数据和经营天数
 */

-- 1. 定义日期参数
DECLARE @sdate DATE;    -- 本期开始日期
DECLARE @edate DATE;    -- 本期结束日期
DECLARE @LYsdate DATE;  -- 去年同期开始日期
DECLARE @LYedate DATE;  -- 去年同期结束日期

-- 智能设置日期变量（自动获取本月初至昨日）
SET @sdate = CONVERT(DATE, DATEADD(MONTH, DATEDIFF(MONTH, 0, GETDATE()-1), 0)); -- 本月初
SET @edate = DATEADD(DAY, DATEDIFF(DAY, 0, GETDATE()-1), 0);                    -- 昨日
SET @LYsdate = '2022-12-13';  -- 去年同期开始日期（根据农历对应关系）
SET @LYedate = '2023-01-12';  -- 去年同期结束日期（根据农历对应关系）

-- 2. 输出日期参数（便于调试和确认）
SELECT 
    @sdate AS 开始日期,
    @edate AS 结束日期,
    @LYsdate AS 去年开始日期,
    @LYedate AS 去年结束日期;

-- 3. 计算本期每日销售数据（销售额和经营天数）
IF OBJECT_ID('tempdb..#data') IS NOT NULL DROP TABLE #data; -- 如果临时表已存在则先删除

SELECT 
    CONVERT(VARCHAR(20), rq, 112) AS 销售日期, -- 转换为YYYYMMDD格式
    companycode,                              -- 公司代码
    COUNT(rq) AS 天数,                        -- 统计经营天数
    SUM(noxse) AS 销售额                      -- 统计销售额
INTO #data -- 存入临时表#data
FROM odsdbfq_result.dbo.m_stsale WITH (NOLOCK) -- 使用NOLOCK提高查询性能
WHERE rq BETWEEN @sdate AND @edate -- 使用BETWEEN简化日期范围条件
  AND companycode = 'hn'          -- 仅统计hn公司数据
  AND noxse > 0                   -- 仅包含有效销售额（大于0）
GROUP BY companycode, CONVERT(VARCHAR(20), rq, 112);

-- 4. 计算去年同期每日销售数据，并将日期平移384天（农历对齐）
IF OBJECT_ID('tempdb..#lydata') IS NOT NULL DROP TABLE #lydata; -- 如果临时表已存在则先删除

SELECT 
    CONVERT(VARCHAR(20), rq, 112) AS 销售日期,  -- 去年原始日期
    CONVERT(VARCHAR(20), DATEADD(DAY, 384, CONVERT(DATETIME, rq)), 112) AS 对比日期, -- 平移后的日期（农历对齐）
    companycode,                               -- 公司代码
    COUNT(rq) AS 天数,                         -- 统计经营天数
    SUM(noxse) AS 销售额                       -- 统计销售额
INTO #lydata -- 存入临时表#lydata
FROM odsdbfq_result.dbo.m_stsale WITH (NOLOCK) -- 使用NOLOCK提高查询性能
WHERE rq BETWEEN @LYsdate AND @LYedate -- 使用BETWEEN简化日期范围条件
  AND companycode = 'hn'              -- 仅统计hn公司数据
  AND noxse > 0                       -- 仅包含有效销售额（大于0）
GROUP BY companycode, 
         CONVERT(VARCHAR(20), rq, 112), 
         CONVERT(VARCHAR(20), DATEADD(DAY, 384, CONVERT(DATETIME, rq)), 112)
ORDER BY CONVERT(VARCHAR(20), rq, 112);

-- 5. 合并本期与去年同期数据进行对比分析
SELECT 
    ISNULL(a.销售日期, b.对比日期) AS 销售日期, -- 以本期日期为主，若不存在则使用去年平移日期
    ISNULL(a.companycode, b.companycode) AS companycode, -- 公司代码
    a.天数 AS 本期天数,                      -- 本期经营天数
    b.天数 AS 去年天数,                      -- 去年同期经营天数
    a.销售额 AS 本期销售额,                  -- 本期销售额
    b.销售额 AS 去年销售额,                  -- 去年同期销售额
    CASE 
        WHEN b.销售额 = 0 OR b.销售额 IS NULL THEN NULL
        ELSE ROUND((a.销售额 - b.销售额) / b.销售额 * 100, 2) 
    END AS 销售额同比增长率,                 -- 新增：计算销售额同比增长率，避免除零错误
    CASE 
        WHEN a.天数 > 0 AND b.天数 > 0 THEN 
            ROUND((a.销售额/a.天数) - (b.销售额/b.天数), 2)
        ELSE NULL
    END AS 日均销售额差异                    -- 新增：计算日均销售额差异
FROM #data a
FULL JOIN #lydata b ON a.销售日期 = b.对比日期 
                   AND a.companycode = b.companycode
ORDER BY 销售日期;

-- 6. 清理临时表（提高性能）
DROP TABLE IF EXISTS #data;
DROP TABLE IF EXISTS #lydata;

/*
 * 代码优化说明：
 * 1. 添加了详细的文件头注释，说明脚本功能和目的
 * 2. 使用BETWEEN替代>=和<=来简化日期范围条件
 * 3. 添加了更详细的中文注释，解释每个变量和步骤的目的
 * 4. 新增销售额同比增长率计算，并避免除零错误
 * 5. 新增日均销售额差异计算，提供更多分析维度
 * 6. 启用临时表清理，优化资源使用
 * 7. 保持了WITH (NOLOCK)提示以提高查询性能
 */