-- =============================================
-- 华中五省数据整合与追加
-- 说明: 整合华中五省(湖南、湖北、安徽、福建、江西)的销售数据并进行追加分析
-- =============================================

-- 设置日期参数
DECLARE @StartDate DATE,
        @EndDate DATE,
        @LastYearStartDate DATE,
        @LastYearEndDate DATE,
        @LastMonthStartDate DATE,
        @LastMonthEndDate DATE

-- 设置日期范围
SET @StartDate = CONVERT(NVARCHAR(50), DATEADD(MM, DATEDIFF(MM, 0, GETDATE()-1), 0), 23)  -- 本月第一天
SET @EndDate = DATEADD(DD, DATEDIFF(DD, 0, GETDATE()-1), 0)  -- 昨天
SET @LastYearStartDate = DATEADD("YY", -1, @StartDate)  -- 去年开始日期
SET @LastYearEndDate = DATEADD("YY", -1, @EndDate)  -- 去年结束日期

-- 输出日期参数用于验证
SELECT @StartDate AS StartDate,
       @EndDate AS EndDate,
       @LastYearStartDate AS LastYearStartDate,
       @LastYearEndDate AS LastYearEndDate

-- 创建门店信息临时表
DROP TABLE IF EXISTS #StoreInfo
SELECT * 
INTO #StoreInfo 
FROM odsdbfq_basic.dbo.store 
WHERE companycode IN ('HB','HN','FJ','JX','AH')

-- 更新门店类型
UPDATE #StoreInfo
SET shoptype = '标准门店' 
WHERE code IN (SELECT StoreCode FROM odsdbfqbi.dbo.xsb) 
    AND companycode IN ('HB','HN','FJ','JX','AH')

-- 创建当前销售数据临时表
DROP TABLE IF EXISTS #CurrentSales
SELECT 
    companycode,
    code AS StoreCode,
    SUM(saleqty) AS SalesQuantity,
    SUM(saletotal) AS SalesAmount,
    SUM(salemle) AS SalesProfit
INTO #CurrentSales
FROM odsdbfq_result.dbo.m_stsale (NOLOCK)
WHERE rq >= @StartDate 
    AND rq <= @EndDate 
    AND companycode IN ('HB','HN','FJ','JX','AH')
GROUP BY companycode, code

-- 创建去年同期销售数据临时表
DROP TABLE IF EXISTS #LastYearSales
SELECT 
    companycode,
    code AS StoreCode,
    SUM(saleqty) AS SalesQuantity,
    SUM(saletotal) AS SalesAmount,
    SUM(salemle) AS SalesProfit
INTO #LastYearSales
FROM odsdbfq_result.dbo.m_stsale (NOLOCK)
WHERE rq >= @LastYearStartDate 
    AND rq <= @LastYearEndDate 
    AND companycode IN ('HB','HN','FJ','JX','AH')
GROUP BY companycode, code

-- 关联门店信息
DROP TABLE IF EXISTS #CurrentSalesWithInfo
SELECT 
    a.*,
    b.shoptype,
    b.syb
INTO #CurrentSalesWithInfo
FROM #CurrentSales a
LEFT JOIN #StoreInfo b(NOLOCK) 
    ON a.StoreCode = b.code 
    AND b.CompanyCode = 'hn' 
    AND b.stat = '有效'

-- 更新事业部信息
UPDATE #CurrentSalesWithInfo
SET syb = '食品事业部' 
WHERE StoreCode IN (
    SELECT DISTINCT StoreCode 
    FROM odsdbfqbi.dbo.storeinf
    WHERE BusinessUnit = '食品事业部'
)

-- 输出最终结果
SELECT 
    CASE 
        WHEN companycode = 'hn' THEN '湖南'
        WHEN companycode = 'hb' THEN '湖北'
        WHEN companycode = 'ah' THEN '安徽'
        WHEN companycode = 'fj' THEN '福建'
        WHEN companycode = 'jx' THEN '江西'
        ELSE '其他'
    END AS Province,
    TimePeriod,
    CASE 
        WHEN StoreType = '标准门店' THEN '标准门店'
        ELSE StoreType 
    END AS StoreType,
    StoreCount,
    SalesQuantity,
    SalesAmount,
    SalesProfit,
    CASE 
        WHEN SalesAmount = 0 THEN '无销售'
        WHEN SalesAmount < 1000 THEN '销售偏低'
        WHEN SalesAmount > 10000 THEN '销售良好'
        ELSE '销售一般'
    END AS SalesStatus
FROM (
    SELECT 
        '本月累计' AS TimePeriod,
        b.shoptype AS StoreType,
        a.companycode,
        COUNT(StoreCode) AS StoreCount,
        SUM(SalesQuantity) AS SalesQuantity,
        SUM(SalesAmount) AS SalesAmount,
        SUM(SalesProfit) AS SalesProfit
    FROM #CurrentSalesWithInfo a
    WHERE shoptype IS NOT NULL
    GROUP BY b.shoptype, a.companycode
    
    UNION ALL
    
    SELECT 
        '去年同期' AS TimePeriod,
        b.shoptype AS StoreType,
        a.companycode,
        COUNT(StoreCode) AS StoreCount,
        SUM(SalesQuantity) AS SalesQuantity,
        SUM(SalesAmount) AS SalesAmount,
        SUM(SalesProfit) AS SalesProfit
    FROM #LastYearSales a
    LEFT JOIN #StoreInfo b(NOLOCK) 
        ON a.StoreCode = b.code 
        AND b.CompanyCode = 'hn'
    WHERE shoptype IS NOT NULL
    GROUP BY b.shoptype, a.companycode
) b

-- 追加总体汇总数据
UNION ALL
SELECT 
    '华中五省' AS Province,
    TimePeriod,
    '全部' AS StoreType,
    SUM(StoreCount) AS StoreCount,
    SUM(SalesQuantity) AS SalesQuantity,
    SUM(SalesAmount) AS SalesAmount,
    SUM(SalesProfit) AS SalesProfit,
    CASE 
        WHEN SUM(SalesAmount) = 0 THEN '无销售'
        WHEN SUM(SalesAmount) < 5000 THEN '销售偏低'
        WHEN SUM(SalesAmount) > 50000 THEN '销售良好'
        ELSE '销售一般'
    END AS SalesStatus
FROM (
    SELECT 
        TimePeriod,
        StoreCount,
        SalesQuantity,
        SalesAmount,
        SalesProfit
    FROM (
        SELECT 
            '本月累计' AS TimePeriod,
            b.shoptype AS StoreType,
            a.companycode,
            COUNT(StoreCode) AS StoreCount,
            SUM(SalesQuantity) AS SalesQuantity,
            SUM(SalesAmount) AS SalesAmount,
            SUM(SalesProfit) AS SalesProfit
        FROM #CurrentSalesWithInfo a
        WHERE shoptype IS NOT NULL
        GROUP BY b.shoptype, a.companycode
        
        UNION ALL
        
        SELECT 
            '去年同期' AS TimePeriod,
            b.shoptype AS StoreType,
            a.companycode,
            COUNT(StoreCode) AS StoreCount,
            SUM(SalesQuantity) AS SalesQuantity,
            SUM(SalesAmount) AS SalesAmount,
            SUM(SalesProfit) AS SalesProfit
        FROM #LastYearSales a
        LEFT JOIN #StoreInfo b(NOLOCK) 
            ON a.StoreCode = b.code 
            AND b.CompanyCode = 'hn'
        WHERE shoptype IS NOT NULL
        GROUP BY b.shoptype, a.companycode
    ) b
) c
GROUP BY TimePeriod
