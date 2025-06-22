/*
 * 文件名: 01-农历出货.sql
 * 功能: 农历出货对比分析（按农历同期对比本期与去年出货净额）
 * 描述: 本脚本根据农历日期对齐，比较当前年度与去年同期的出货净额数据
 */

-- 1. 定义日期参数
DECLARE @sdate DATE = '2024-01-01';      -- 本期开始日期
DECLARE @edate DATE = '2024-12-31';      -- 本期结束日期
DECLARE @lysdate DATE = '2022-01-01';    -- 去年同期开始日期
DECLARE @lyedate DATE = '2024-12-31';    -- 去年同期结束日期

-- 2. 输出日期参数（便于调试和确认）
SELECT 
    @sdate AS 开始日期,
    @edate AS 结束日期, 
    @lysdate AS 去年开始日期, 
    @lyedate AS 去年结束日期;

-- 3. 计算本期每日净出货额（出货金额减退货金额）
IF OBJECT_ID('tempdb..#cy') IS NOT NULL DROP TABLE #cy; -- 如果临时表已存在则先删除

SELECT 
    CONVERT(VARCHAR(20), adate, 112) AS 出货日期, -- 转换为YYYYMMDD格式
    SUM(goods_out_money - goods_back_money) AS 净出货额 -- 计算净出货额（出货金额-退货金额）
INTO #cy -- 存入临时表#cy
FROM odsdbfq_result.dbo.m_store_out_sort WITH (NOLOCK) -- 使用NOLOCK提高查询性能
WHERE adate BETWEEN @sdate AND @edate -- 使用BETWEEN简化日期范围条件
  AND LEFT(sort, 1) NOT IN ('6', '7', '8', '9') -- 排除特定分类编码
  AND companycode = 'hn' -- 仅统计hn公司数据
  AND outmemo = '总仓'   -- 仅统计总仓数据
GROUP BY CONVERT(VARCHAR(20), adate, 112);

-- 4. 计算去年同期每日净出货额，并将日期平移384天（农历对齐）
IF OBJECT_ID('tempdb..#ly') IS NOT NULL DROP TABLE #ly; -- 如果临时表已存在则先删除

SELECT 
    CONVERT(VARCHAR(20), adate, 112) AS 出货日期, -- 去年原始日期
    CONVERT(VARCHAR(20), DATEADD(DAY, 384, CONVERT(DATETIME, adate)), 112) AS 对比日期, -- 平移后的日期（农历对齐）
    SUM(goods_out_money - goods_back_money) AS 净出货额 -- 计算去年同期净出货额
INTO #ly -- 存入临时表#ly
FROM odsdbfq_result.dbo.m_store_out_sort WITH (NOLOCK)
WHERE adate BETWEEN @lysdate AND @lyedate -- 使用BETWEEN简化日期范围条件
  AND LEFT(sort, 1) NOT IN ('6', '7', '8', '9') -- 排除特定分类编码
  AND companycode = 'hn' -- 仅统计hn公司数据
  AND outmemo = '总仓'   -- 仅统计总仓数据
GROUP BY 
    CONVERT(VARCHAR(20), adate, 112),
    CONVERT(VARCHAR(20), DATEADD(DAY, 384, CONVERT(DATETIME, adate)), 112);

-- 5. 合并本期与去年同期数据进行对比分析
SELECT 
    ISNULL(a.出货日期, b.对比日期) AS 出货日期, -- 以本期日期为主，若不存在则使用去年平移日期
    a.净出货额 AS 本期出货,                    -- 本期净出货额
    b.净出货额 AS 同期出货,                    -- 去年同期净出货额
    CASE 
        WHEN b.净出货额 = 0 OR b.净出货额 IS NULL THEN NULL
        ELSE ROUND((a.净出货额 - b.净出货额) / b.净出货额 * 100, 2) 
    END AS 同比增长率                         -- 新增：计算同比增长率，避免除零错误
FROM #cy a 
FULL JOIN #ly b ON a.出货日期 = b.对比日期
ORDER BY ISNULL(a.出货日期, b.对比日期);

-- 6. 清理临时表（提高性能）
DROP TABLE IF EXISTS #cy;
DROP TABLE IF EXISTS #ly;

/*
 * 代码优化说明：
 * 1. 添加了详细的文件头注释，说明脚本功能和目的
 * 2. 使用BETWEEN替代>=和<=来简化日期范围条件
 * 3. 添加了更详细的中文注释，解释每个步骤的目的和逻辑
 * 4. 新增同比增长率计算，并避免除零错误
 * 5. 启用临时表清理，优化资源使用
 * 6. 保持了WITH (NOLOCK)提示以提高查询性能
 */
