/*
 * 文件名: 06-指标看板去年出货.sql
 * 功能: 去年同期出货分析
 * 描述: 本脚本统计去年同期每日各品类出货额与毛利额，支持灵活的日期参数配置，便于与本期数据进行对比分析
 */

-- 1. 定义日期参数
DECLARE @sdate DATE;    -- 去年开始日期
DECLARE @edate DATE;    -- 去年结束日期
DECLARE @TYsdate DATE;  -- 本年同期开始日期（新增）
DECLARE @TYedate DATE;  -- 本年同期结束日期（新增）

-- 可根据需要设置日期范围
-- 方法1：固定日期范围
SET @sdate = '2023-01-01';                -- 去年开始日期
SET @edate = '2023-01-31';                -- 去年结束日期
SET @TYsdate = DATEADD(YEAR, 1, @sdate);  -- 本年同期开始日期
SET @TYedate = DATEADD(YEAR, 1, @edate);  -- 本年同期结束日期

-- 方法2：动态计算日期范围（注释状态，需要时可以启用）
/*
-- 获取上个月的第一天和最后一天
-- SET @TYsdate = CONVERT(DATE, DATEADD(MONTH, DATEDIFF(MONTH, 0, GETDATE()) - 1, 0));
-- SET @TYedate = DATEADD(DAY, -1, DATEADD(MONTH, DATEDIFF(MONTH, 0, GETDATE()), 0));
-- SET @sdate = DATEADD(YEAR, -1, @TYsdate);
-- SET @edate = DATEADD(YEAR, -1, @TYedate);
*/

-- 输出日期参数（便于调试和确认）
SELECT 
    @sdate AS 去年开始日期,
    @edate AS 去年结束日期,
    @TYsdate AS 本年同期开始日期,
    @TYedate AS 本年同期结束日期,
    DATEDIFF(DAY, @sdate, @edate) + 1 AS 天数;

-- 2. 统计去年同期每日出货额与毛利额
SELECT 
    CONVERT(VARCHAR(20), adate, 23) AS 日期,           -- 日期（YYYY-MM-DD格式）
    RIGHT(CONVERT(VARCHAR(20), adate, 112), 2) AS 日份, -- 日（两位数）
    sort AS 品类编码,                                   -- 品类编码
    -- 查询商品分类名称（如果有需要，取消注释即可）
    -- (SELECT sname FROM odsdbfq_basic.dbo.sort WHERE scode = sort AND companycode = 'hn') AS 品类名称,
    COUNT(DISTINCT gid) AS 商品数,                      -- 统计商品数量
    SUM(goods_out_money - goods_back_money) AS 出货额,  -- 计算净出货额（出货金额-退货金额）
    SUM(goods_out_maoli - goods_back_maoli) AS 毛利额,  -- 计算净毛利额（出货毛利-退货毛利）
    CASE 
        WHEN SUM(goods_out_money - goods_back_money) = 0 THEN 0
        ELSE ROUND(SUM(goods_out_maoli - goods_back_maoli) / SUM(goods_out_money - goods_back_money) * 100, 2)
    END AS 毛利率                                       -- 计算毛利率，避免除零错误
FROM odsdbfq_result.dbo.m_store_out_sort WITH (NOLOCK)  -- 使用NOLOCK提高查询性能
WHERE adate BETWEEN @sdate AND @edate                   -- 使用BETWEEN简化日期范围条件
  AND LEFT(sort, 1) NOT IN ('6','7','8','9')            -- 排除特定品类编码
  AND companycode = 'hn'                                -- 仅统计hn公司数据
  AND outmemo = '总仓'                                  -- 仅统计总仓数据
GROUP BY CONVERT(VARCHAR(20), adate, 23), RIGHT(CONVERT(VARCHAR(20), adate, 112), 2), sort
ORDER BY 日期, 品类编码;                                -- 添加排序提高数据可读性

-- 3. 按品类汇总去年同期出货数据（新增）
SELECT 
    sort AS 品类编码,                                   -- 品类编码
    -- 查询商品分类名称（如果有需要，取消注释即可）
    -- (SELECT sname FROM odsdbfq_basic.dbo.sort WHERE scode = sort AND companycode = 'hn') AS 品类名称,
    COUNT(DISTINCT gid) AS 商品数,                      -- 统计商品数量
    SUM(goods_out_money) AS 出货金额,                   -- 统计出货金额
    SUM(goods_back_money) AS 退货金额,                  -- 统计退货金额
    SUM(goods_out_money - goods_back_money) AS 净出货额, -- 计算净出货额
    SUM(goods_out_maoli - goods_back_maoli) AS 净毛利额, -- 计算净毛利额
    CASE 
        WHEN SUM(goods_out_money - goods_back_money) = 0 THEN 0
        ELSE ROUND(SUM(goods_out_maoli - goods_back_maoli) / SUM(goods_out_money - goods_back_money) * 100, 2)
    END AS 毛利率,                                       -- 计算毛利率，避免除零错误
    COUNT(DISTINCT CONVERT(VARCHAR(10), adate, 112)) AS 出货天数 -- 统计出货天数
FROM odsdbfq_result.dbo.m_store_out_sort WITH (NOLOCK)  -- 使用NOLOCK提高查询性能  
WHERE adate BETWEEN @sdate AND @edate                   -- 使用BETWEEN简化日期范围条件
  AND LEFT(sort, 1) NOT IN ('6','7','8','9')            -- 排除特定品类编码
  AND companycode = 'hn'                                -- 仅统计hn公司数据
  AND outmemo = '总仓'                                  -- 仅统计总仓数据
GROUP BY sort
ORDER BY 净出货额 DESC;                                 -- 按净出货额降序排列，突出重点品类

-- 4. 统计本年同期数据以便对比（新增）
SELECT 
    '本年同期' AS 数据类型,
    sort AS 品类编码,                                   -- 品类编码
    -- 查询商品分类名称（如果有需要，取消注释即可）
    -- (SELECT sname FROM odsdbfq_basic.dbo.sort WHERE scode = sort AND companycode = 'hn') AS 品类名称,
    SUM(goods_out_money - goods_back_money) AS 净出货额, -- 计算净出货额
    SUM(goods_out_maoli - goods_back_maoli) AS 净毛利额, -- 计算净毛利额
    CASE 
        WHEN SUM(goods_out_money - goods_back_money) = 0 THEN 0
        ELSE ROUND(SUM(goods_out_maoli - goods_back_maoli) / SUM(goods_out_money - goods_back_money) * 100, 2)
    END AS 毛利率                                       -- 计算毛利率，避免除零错误
FROM odsdbfq_result.dbo.m_store_out_sort WITH (NOLOCK)  -- 使用NOLOCK提高查询性能
WHERE adate BETWEEN @TYsdate AND @TYedate               -- 使用BETWEEN简化日期范围条件
  AND LEFT(sort, 1) NOT IN ('6','7','8','9')            -- 排除特定品类编码
  AND companycode = 'hn'                                -- 仅统计hn公司数据
  AND outmemo = '总仓'                                  -- 仅统计总仓数据
GROUP BY sort

UNION ALL

SELECT 
    '去年同期' AS 数据类型,
    sort AS 品类编码,                                   -- 品类编码
    -- 查询商品分类名称（如果有需要，取消注释即可）
    -- (SELECT sname FROM odsdbfq_basic.dbo.sort WHERE scode = sort AND companycode = 'hn') AS 品类名称,
    SUM(goods_out_money - goods_back_money) AS 净出货额, -- 计算净出货额
    SUM(goods_out_maoli - goods_back_maoli) AS 净毛利额, -- 计算净毛利额
    CASE 
        WHEN SUM(goods_out_money - goods_back_money) = 0 THEN 0
        ELSE ROUND(SUM(goods_out_maoli - goods_back_maoli) / SUM(goods_out_money - goods_back_money) * 100, 2)
    END AS 毛利率                                       -- 计算毛利率，避免除零错误
FROM odsdbfq_result.dbo.m_store_out_sort WITH (NOLOCK)  -- 使用NOLOCK提高查询性能
WHERE adate BETWEEN @sdate AND @edate                   -- 使用BETWEEN简化日期范围条件
  AND LEFT(sort, 1) NOT IN ('6','7','8','9')            -- 排除特定品类编码
  AND companycode = 'hn'                                -- 仅统计hn公司数据
  AND outmemo = '总仓'                                  -- 仅统计总仓数据
GROUP BY sort

ORDER BY 品类编码, 数据类型 DESC;                       -- 按品类编码和数据类型排序，便于对比

-- 5. 同比增长率分析（新增）
WITH 本年数据 AS (
    SELECT 
        sort AS 品类编码,
        SUM(goods_out_money - goods_back_money) AS 本年净出货额,
        SUM(goods_out_maoli - goods_back_maoli) AS 本年净毛利额
    FROM odsdbfq_result.dbo.m_store_out_sort WITH (NOLOCK)
    WHERE adate BETWEEN @TYsdate AND @TYedate
      AND LEFT(sort, 1) NOT IN ('6','7','8','9')
      AND companycode = 'hn'
      AND outmemo = '总仓'
    GROUP BY sort
),
去年数据 AS (
    SELECT 
        sort AS 品类编码,
        SUM(goods_out_money - goods_back_money) AS 去年净出货额,
        SUM(goods_out_maoli - goods_back_maoli) AS 去年净毛利额
    FROM odsdbfq_result.dbo.m_store_out_sort WITH (NOLOCK)
    WHERE adate BETWEEN @sdate AND @edate
      AND LEFT(sort, 1) NOT IN ('6','7','8','9')
      AND companycode = 'hn'
      AND outmemo = '总仓'
    GROUP BY sort
)
SELECT 
    ISNULL(a.品类编码, b.品类编码) AS 品类编码,
    -- 查询商品分类名称（如果有需要，取消注释即可）
    -- (SELECT sname FROM odsdbfq_basic.dbo.sort WHERE scode = ISNULL(a.品类编码, b.品类编码) AND companycode = 'hn') AS 品类名称,
    a.本年净出货额,
    b.去年净出货额,
    CASE 
        WHEN b.去年净出货额 IS NULL OR b.去年净出货额 = 0 THEN NULL
        ELSE ROUND((a.本年净出货额 - b.去年净出货额) / b.去年净出货额 * 100, 2)
    END AS 出货额同比增长率,
    a.本年净毛利额,
    b.去年净毛利额,
    CASE 
        WHEN b.去年净毛利额 IS NULL OR b.去年净毛利额 = 0 THEN NULL
        ELSE ROUND((a.本年净毛利额 - b.去年净毛利额) / b.去年净毛利额 * 100, 2)
    END AS 毛利额同比增长率
FROM 本年数据 a
FULL JOIN 去年数据 b ON a.品类编码 = b.品类编码
ORDER BY 
    CASE WHEN 出货额同比增长率 IS NOT NULL THEN 0 ELSE 1 END,
    出货额同比增长率 DESC;  -- 按同比增长率降序排列，突出增长最快的品类

/*
 * 代码优化说明：
 * 1. 添加了详细的文件头注释，说明脚本功能和目的
 * 2. 增加了本年同期日期参数，便于对比分析
 * 3. 提供了两种日期设置方法：固定日期和动态计算
 * 4. 使用BETWEEN替代>=和<=来简化日期范围条件
 * 5. 添加了更详细的中文注释，解释每个字段的计算逻辑
 * 6. 新增商品数和出货天数统计，提供更多分析维度
 * 7. 新增按品类汇总分析，便于掌握整体出货情况
 * 8. 新增本年同期数据分析，支持同比对比
 * 9. 新增同比增长率分析，突出变化最明显的品类
 * 10. 所有计算字段均添加了除零保护，避免计算错误
 * 11. 添加了ORDER BY排序，提高数据可读性
 * 12. 保持了WITH (NOLOCK)提示以提高查询性能
 */
