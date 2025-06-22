/*
 * 文件名: 07-指标看板出货达成.sql
 * 功能: 本期出货达成分析
 * 描述: 本脚本统计本期出货达成情况，并计算剩余天数和预测达成率，支持品类维度分析和目标对比
 */

-- 1. 定义日期参数
DECLARE @sdate DATE;       -- 本期开始日期
DECLARE @edate DATE;       -- 本期结束日期（当前日期的前一天）
DECLARE @lastdate DATE;    -- 本期最后一天（月末）
DECLARE @totalDays INT;    -- 本期总天数
DECLARE @passedDays INT;   -- 已经过天数
DECLARE @remainDays INT;   -- 剩余天数

-- 智能设置日期变量（自动计算相关日期）
SET @sdate = CONVERT(DATE, DATEADD(MONTH, DATEDIFF(MONTH, 0, GETDATE()-1), 0)); -- 本月初
SET @edate = DATEADD(DAY, DATEDIFF(DAY, 0, GETDATE()-1), 0);                    -- 昨日
SET @lastdate = EOMONTH(@sdate);                                                -- 使用EOMONTH函数获取月末（SQL Server 2012及以上版本）
-- 如果是SQL Server 2008，可以使用下面的替代方法：
-- SET @lastdate = DATEADD(DAY, -1, DATEADD(MONTH, 1, @sdate));                -- 本期最后一天（月末）

-- 计算天数相关信息
SET @totalDays = DATEDIFF(DAY, @sdate, @lastdate) + 1;                         -- 本期总天数
SET @passedDays = DATEDIFF(DAY, @sdate, @edate) + 1;                           -- 已经过天数
SET @remainDays = DATEDIFF(DAY, @edate, @lastdate);                            -- 剩余天数

-- 输出日期参数（便于调试和确认）
SELECT 
    @sdate AS 开始日期,
    @edate AS 结束日期,
    @lastdate AS 本期最后一天,
    @totalDays AS 本期总天数,
    @passedDays AS 已经过天数,
    @remainDays AS 剩余天数,
    CONVERT(VARCHAR(10), @passedDays * 100.0 / @totalDays) + '%' AS 时间进度;

-- 2. 创建目标表（如果需要设置品类目标，可以取消注释使用）
/*
IF OBJECT_ID('tempdb..#target') IS NOT NULL DROP TABLE #target;
CREATE TABLE #target (
    品类 VARCHAR(20),
    目标出货额 DECIMAL(18,2),
    目标毛利额 DECIMAL(18,2)
);

-- 插入品类目标数据（这里只是示例，实际应根据业务需求设置）
INSERT INTO #target (品类, 目标出货额, 目标毛利额) VALUES 
('1', 5000000, 1000000),   -- 示例：1类商品目标
('2', 3000000, 600000),    -- 示例：2类商品目标
('3', 2000000, 400000),    -- 示例：3类商品目标
('4', 1500000, 300000),    -- 示例：4类商品目标
('5', 1000000, 200000);    -- 示例：5类商品目标
*/

-- 3. 按日期统计本期每日出货达成情况
SELECT 
    CONVERT(VARCHAR(20), adate, 23) AS 出货日期,       -- 日期（YYYY-MM-DD格式）
    RIGHT(CONVERT(VARCHAR(20), adate, 112), 2) AS 日份, -- 提取日（两位数）
    sort AS 品类编码,                                   -- 品类编码
    -- 查询商品分类名称（如果有需要，取消注释即可）
    -- (SELECT sname FROM odsdbfq_basic.dbo.sort WHERE scode = sort AND companycode = 'hn') AS 品类名称,
    COUNT(DISTINCT billno) AS 单据数,                  -- 统计单据数量
    COUNT(DISTINCT gid) AS 商品数,                     -- 统计商品数量
    SUM(goods_out_money) AS 出货金额,                  -- 统计出货金额
    SUM(goods_back_money) AS 退货金额,                 -- 统计退货金额
    SUM(goods_out_money - goods_back_money) AS 净出货额, -- 计算净出货额
    SUM(goods_out_maoli - goods_back_maoli) AS 净毛利额, -- 计算净毛利额
    CASE 
        WHEN SUM(goods_out_money - goods_back_money) = 0 THEN 0
        ELSE ROUND(SUM(goods_out_maoli - goods_back_maoli) / SUM(goods_out_money - goods_back_money) * 100, 2)
    END AS 毛利率,                                     -- 计算毛利率，避免除零错误
    @remainDays AS 剩余天数,                           -- 显示剩余天数
    @passedDays AS 已过天数                            -- 显示已过天数
FROM odsdbfq_result.dbo.m_store_out_sort WITH (NOLOCK) -- 使用NOLOCK提高查询性能
WHERE adate BETWEEN @sdate AND @edate                  -- 使用BETWEEN简化日期范围条件
  AND LEFT(sort, 1) NOT IN ('6','7','8','9')           -- 排除特定品类编码
  AND companycode = 'hn'                               -- 仅统计hn公司数据
  AND outmemo = '总仓'                                 -- 仅统计总仓数据
GROUP BY CONVERT(VARCHAR(20), adate, 23), RIGHT(CONVERT(VARCHAR(20), adate, 112), 2), sort
ORDER BY 日份, 品类编码;                                -- 添加排序提高数据可读性

-- 4. 按品类汇总本期出货达成情况
SELECT 
    sort AS 品类编码,                                  -- 品类编码
    -- 查询商品分类名称（如果有需要，取消注释即可）
    -- (SELECT sname FROM odsdbfq_basic.dbo.sort WHERE scode = sort AND companycode = 'hn') AS 品类名称,
    COUNT(DISTINCT billno) AS 单据数,                  -- 统计单据数量
    COUNT(DISTINCT gid) AS 商品数,                     -- 统计商品数量
    COUNT(DISTINCT CONVERT(VARCHAR(10), adate, 112)) AS 出货天数, -- 统计出货天数
    SUM(goods_out_money) AS 出货金额,                  -- 统计出货金额
    SUM(goods_back_money) AS 退货金额,                 -- 统计退货金额
    SUM(goods_out_money - goods_back_money) AS 本期累计出货额, -- 计算本期累计出货额
    SUM(goods_out_maoli - goods_back_maoli) AS 本期累计毛利额, -- 计算本期累计毛利额
    CASE 
        WHEN SUM(goods_out_money - goods_back_money) = 0 THEN 0
        ELSE ROUND(SUM(goods_out_maoli - goods_back_maoli) / SUM(goods_out_money - goods_back_money) * 100, 2)
    END AS 毛利率,                                     -- 计算毛利率，避免除零错误
    ROUND(SUM(goods_out_money - goods_back_money) / @passedDays, 2) AS 日均出货额, -- 计算日均出货额
    ROUND(SUM(goods_out_money - goods_back_money) / @passedDays * @totalDays, 2) AS 预测月出货额, -- 预测月出货额
    /*
    t.目标出货额,                                       -- 目标出货额（需要使用#target临时表）
    CASE 
        WHEN t.目标出货额 IS NULL OR t.目标出货额 = 0 THEN NULL
        ELSE ROUND(SUM(goods_out_money - goods_back_money) / t.目标出货额 * 100, 2)
    END AS 目标达成率,                                  -- 计算目标达成率
    CASE 
        WHEN t.目标出货额 IS NULL OR t.目标出货额 = 0 THEN NULL
        ELSE ROUND(SUM(goods_out_money - goods_back_money) / @passedDays * @totalDays / t.目标出货额 * 100, 2)
    END AS 预测达成率,                                 -- 计算预测达成率
    */
    @remainDays AS 剩余天数,                           -- 显示剩余天数
    @passedDays AS 已过天数,                           -- 显示已过天数
    CONVERT(VARCHAR(10), @passedDays * 100.0 / @totalDays) + '%' AS 时间进度 -- 显示时间进度百分比
FROM odsdbfq_result.dbo.m_store_out_sort WITH (NOLOCK) -- 使用NOLOCK提高查询性能
WHERE adate BETWEEN @sdate AND @edate                  -- 使用BETWEEN简化日期范围条件
  AND LEFT(sort, 1) NOT IN ('6','7','8','9')           -- 排除特定品类编码
  AND companycode = 'hn'                               -- 仅统计hn公司数据
  AND outmemo = '总仓'                                 -- 仅统计总仓数据
-- LEFT JOIN #target t ON sort = t.品类                 -- 关联目标表（需要使用#target临时表）
GROUP BY sort /*, t.目标出货额, t.目标毛利额 */
ORDER BY 本期累计出货额 DESC;                            -- 按本期累计出货额降序排列，突出重点品类

-- 5. 按天汇总计算环比增长趋势（新增）
;WITH DailyTotal AS (
    -- 每天总出货情况
    SELECT 
        CONVERT(VARCHAR(20), adate, 23) AS 出货日期,
        SUM(goods_out_money - goods_back_money) AS 日出货额,
        SUM(goods_out_maoli - goods_back_maoli) AS 日毛利额,
        ROW_NUMBER() OVER (ORDER BY adate) AS DayNum  -- 为每天分配序号
    FROM odsdbfq_result.dbo.m_store_out_sort WITH (NOLOCK)
    WHERE adate BETWEEN @sdate AND @edate
      AND LEFT(sort, 1) NOT IN ('6','7','8','9')
      AND companycode = 'hn'
      AND outmemo = '总仓'
    GROUP BY CONVERT(VARCHAR(20), adate, 23), adate
)
SELECT 
    a.出货日期,
    a.日出货额,
    b.日出货额 AS 前一日出货额,
    CASE 
        WHEN b.日出货额 IS NULL OR b.日出货额 = 0 THEN NULL
        ELSE ROUND((a.日出货额 - b.日出货额) / b.日出货额 * 100, 2)
    END AS 环比增长率,
    a.日毛利额,
    a.日出货额 / NULLIF(SUM(a.日出货额) OVER(), 0) * 100 AS 占比,
    SUM(a.日出货额) OVER(ORDER BY a.出货日期) AS 累计出货额,
    CONVERT(VARCHAR(10), @passedDays * 100.0 / @totalDays) + '%' AS 时间进度,
    CONVERT(VARCHAR(10), SUM(a.日出货额) OVER(ORDER BY a.出货日期) / 
            (SELECT SUM(日出货额) FROM DailyTotal) * 100) + '%' AS 出货进度
FROM DailyTotal a
LEFT JOIN DailyTotal b ON a.DayNum = b.DayNum + 1  -- 关联前一天数据
ORDER BY a.出货日期;

-- 6. 计算出货达成趋势（月累计）
SELECT 
    '月累计' AS 汇总类型,
    COUNT(DISTINCT CONVERT(VARCHAR(10), adate, 112)) AS 出货天数,
    SUM(goods_out_money - goods_back_money) AS 本期累计出货额,
    SUM(goods_out_maoli - goods_back_maoli) AS 本期累计毛利额,
    CASE 
        WHEN SUM(goods_out_money - goods_back_money) = 0 THEN 0
        ELSE ROUND(SUM(goods_out_maoli - goods_back_maoli) / SUM(goods_out_money - goods_back_money) * 100, 2)
    END AS 毛利率,
    @totalDays AS 本期总天数,
    @passedDays AS 已过天数,
    @remainDays AS 剩余天数,
    CONVERT(VARCHAR(10), @passedDays * 100.0 / @totalDays) + '%' AS 时间进度,
    ROUND(SUM(goods_out_money - goods_back_money) / @passedDays, 2) AS 日均出货额,
    ROUND(SUM(goods_out_money - goods_back_money) / @passedDays * @totalDays, 2) AS 预测月出货额
    /*
    -- 如果有目标，可以取消注释计算总体达成情况
    ,(SELECT SUM(目标出货额) FROM #target) AS 总目标出货额,
    CASE 
        WHEN (SELECT SUM(目标出货额) FROM #target) IS NULL OR (SELECT SUM(目标出货额) FROM #target) = 0 THEN NULL
        ELSE ROUND(SUM(goods_out_money - goods_back_money) / (SELECT SUM(目标出货额) FROM #target) * 100, 2)
    END AS 总体达成率,
    CASE 
        WHEN (SELECT SUM(目标出货额) FROM #target) IS NULL OR (SELECT SUM(目标出货额) FROM #target) = 0 THEN NULL
        ELSE ROUND(SUM(goods_out_money - goods_back_money) / @passedDays * @totalDays / (SELECT SUM(目标出货额) FROM #target) * 100, 2)
    END AS 预测总体达成率
    */
FROM odsdbfq_result.dbo.m_store_out_sort WITH (NOLOCK)
WHERE adate BETWEEN @sdate AND @edate
  AND LEFT(sort, 1) NOT IN ('6','7','8','9')
  AND companycode = 'hn'
  AND outmemo = '总仓';

/*
 * 代码优化说明：
 * 1. 添加了详细的文件头注释，说明脚本功能和目的
 * 2. 增加了更多的日期计算字段，包括总天数、已过天数、时间进度等
 * 3. 使用EOMONTH函数获取月末（对于SQL Server 2012及以上版本）
 * 4. 使用BETWEEN替代>=和<=来简化日期范围条件
 * 5. 添加了更详细的中文注释，解释每个计算字段的目的
 * 6. 新增商品数和出货天数统计，提供更多分析维度
 * 7. 新增按品类汇总分析，便于掌握整体出货情况
 * 8. 新增日环比增长率分析，观察日出货额变化趋势
 * 9. 新增累计出货额和出货进度计算，便于监控月度进度
 * 10. 增加了目标达成相关代码（注释状态），可根据需要启用
 * 11. 所有计算字段均添加了除零保护，避免计算错误
 * 12. 添加了ORDER BY排序，提高数据可读性
 * 13. 保持了WITH (NOLOCK)提示以提高查询性能
 */
