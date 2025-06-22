-- =============================================
-- 农夫山泉和东方树叶销售数据分析
-- 说明: 统计和分析农夫山泉和东方树叶商品的销售数据，包括出货、缺货、订货和到货情况
-- =============================================

-- 创建当前月份数据临时表
DROP TABLE IF EXISTS #CurrentMonthData
SELECT 
    gid,
    code,
    SUM(outtotal - outbcktotal) AS OutTotal,        -- 出货总量
    SUM(lackqty) AS LackQuantity,                    -- 缺货数量
    SUM(lacktotal) AS LackAmount,                    -- 缺货金额
    SUM(ordqty) AS OrderQuantity,                    -- 订货数量
    SUM(ordtotal) AS OrderAmount,                    -- 订货金额
    SUM(arvqty) AS ArrivalQuantity,                  -- 到货数量
    SUM(arvtotal) AS ArrivalAmount                   -- 到货金额
INTO #CurrentMonthData
FROM odsdbfq_result.dbo.sort_out_mout_r(NOLOCK)
WHERE companycode = 'HN' 
    AND date_id >= '20240101' 
    AND date_id <= '20240131'
GROUP BY gid, code

-- 创建去年同期数据临时表
DROP TABLE IF EXISTS #LastYearData
SELECT 
    gid,
    code,
    SUM(outtotal - outbcktotal) AS OutTotal,        -- 出货总量
    SUM(lackqty) AS LackQuantity,                    -- 缺货数量
    SUM(lacktotal) AS LackAmount,                    -- 缺货金额
    SUM(ordqty) AS OrderQuantity,                    -- 订货数量
    SUM(ordtotal) AS OrderAmount,                    -- 订货金额
    SUM(arvqty) AS ArrivalQuantity,                  -- 到货数量
    SUM(arvtotal) AS ArrivalAmount                   -- 到货金额
INTO #LastYearData
FROM odsdbfq_result.dbo.sort_out_mout_r(NOLOCK)
WHERE companycode = 'HN' 
    AND date_id >= '20230201' 
    AND date_id <= '20230220'
GROUP BY gid, code

-- 合并当前月份和去年同期数据
DROP TABLE IF EXISTS #CombinedData
SELECT 
    ISNULL(a.code, b.code) AS code,
    a.OutTotal,
    a.LackQuantity,
    a.LackAmount,
    a.OrderQuantity,
    a.OrderAmount,
    a.ArrivalQuantity,
    a.ArrivalAmount,
    b.OutTotal AS OutTotal_LastYear,
    b.LackQuantity AS LackQuantity_LastYear,
    b.LackAmount AS LackAmount_LastYear,
    b.OrderQuantity AS OrderQuantity_LastYear,
    b.OrderAmount AS OrderAmount_LastYear,
    b.ArrivalQuantity AS ArrivalQuantity_LastYear,
    b.ArrivalAmount AS ArrivalAmount_LastYear
INTO #CombinedData
FROM #CurrentMonthData a
FULL JOIN #LastYearData b 
    ON a.code = b.code

-- 输出最终结果
SELECT 
    c.ProductType,  -- 商品类型
    CASE 
        WHEN c.ProductType = '水' THEN '农夫水系列' 
        WHEN c.ProductType = '东方树叶' THEN c.ProductType 
        ELSE '农夫其他' 
    END AS ProductCategory,  -- 商品分类
    b.scode1 AS CategoryCode,    -- 大类编码
    b.sname1 AS CategoryName,    -- 大类名称
    b.scode2 AS SubCategoryCode, -- 中类编码
    b.sname2 AS SubCategoryName, -- 中类名称
    b.scode3 AS SmallCategoryCode, -- 小类编码
    b.sname3 AS SmallCategoryName, -- 小类名称
    b.code AS ProductCode,       -- 商品编码
    b.[name] AS ProductName,     -- 商品名称
    a.OutTotal AS ShipmentQuantity,           -- 出货数量
    a.LackQuantity AS ShortageQuantity,       -- 缺货数量
    a.LackAmount AS ShortageAmount,           -- 缺货金额
    a.OrderQuantity AS OrderQuantity,         -- 订货数量
    a.OrderAmount AS OrderAmount,             -- 订货金额
    a.ArrivalQuantity AS ArrivalQuantity,     -- 到货数量
    a.ArrivalAmount AS ArrivalAmount,         -- 到货金额
    a.ArrivalQuantity_LastYear AS LastYearArrivalQuantity,  -- 去年到货数量
    a.ArrivalAmount_LastYear AS LastYearArrivalAmount      -- 去年到货金额
FROM #CombinedData a
LEFT JOIN odsdbfqbi.dbo.nongfu c 
    ON a.code = c.ProductCode
LEFT JOIN odsdbfq_basic.dbo.goodsz b 
    ON a.code = b.code 
    AND b.companycode = 'hn'
WHERE c.ProductCode IS NOT NULL
ORDER BY a.OutTotal DESC