-- =============================================
-- 经营天数统计
-- 说明: 统计各门店的经营天数及相关指标
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

-- 创建当前经营天数临时表
DROP TABLE IF EXISTS #CurrentOperatingDays
SELECT 
    companycode,
    code AS StoreCode,
    COUNT(DISTINCT rq) AS OperatingDays,
    SUM(noxse) AS TotalSales,
    SUM(nomle) AS TotalProfit
INTO #CurrentOperatingDays
FROM odsdbfq_result.dbo.m_stsale (NOLOCK)
WHERE rq >= @StartDate 
    AND rq <= @EndDate 
    AND companycode IN ('HB','HN','FJ','JX','AH') 
    AND noxse > 0
GROUP BY companycode, code

-- 创建去年同期经营天数临时表
DROP TABLE IF EXISTS #LastYearOperatingDays
SELECT 
    companycode,
    code AS StoreCode,
    COUNT(DISTINCT rq) AS OperatingDays,
    SUM(noxse) AS TotalSales,
    SUM(nomle) AS TotalProfit
INTO #LastYearOperatingDays
FROM odsdbfq_result.dbo.m_stsale (NOLOCK)
WHERE rq >= @LastYearStartDate 
    AND rq <= @LastYearEndDate 
    AND companycode IN ('HB','HN','FJ','JX','AH') 
    AND noxse > 0
GROUP BY companycode, code

-- 关联门店信息
DROP TABLE IF EXISTS #CurrentOperatingDaysWithInfo
SELECT 
    a.*,
    b.shoptype,
    b.syb
INTO #CurrentOperatingDaysWithInfo
FROM #CurrentOperatingDays a
LEFT JOIN #StoreInfo b(NOLOCK) 
    ON a.StoreCode = b.code 
    AND b.CompanyCode = 'hn' 
    AND b.stat = '有效'

-- 更新事业部信息
UPDATE #CurrentOperatingDaysWithInfo
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
    OperatingDays,
    TotalSales AS DailySales,
    TotalProfit AS DailyProfit
FROM (
    SELECT 
        '本月累计' AS TimePeriod,
        b.shoptype AS StoreType,
        a.companycode,
        COUNT(StoreCode) AS StoreCount,
        SUM(OperatingDays) AS OperatingDays,
        SUM(TotalSales) AS TotalSales,
        SUM(TotalProfit) AS TotalProfit
    FROM #CurrentOperatingDaysWithInfo a
    WHERE shoptype IS NOT NULL
    GROUP BY b.shoptype, a.companycode
    
    UNION ALL
    
    SELECT 
        '去年同期' AS TimePeriod,
        b.shoptype AS StoreType,
        a.companycode,
        COUNT(StoreCode) AS StoreCount,
        SUM(OperatingDays) AS OperatingDays,
        SUM(TotalSales) AS TotalSales,
        SUM(TotalProfit) AS TotalProfit
    FROM #LastYearOperatingDays a
    LEFT JOIN #StoreInfo b(NOLOCK) 
        ON a.StoreCode = b.code 
        AND b.CompanyCode = 'hn'
    WHERE shoptype IS NOT NULL
    GROUP BY b.shoptype, a.companycode
) b
