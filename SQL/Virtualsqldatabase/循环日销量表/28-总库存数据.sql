-- =============================================
-- 总库存数据分析
-- 说明: 统计和分析各门店的总库存数据，包括库存金额、数量等指标
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

-- 创建当前库存数据临时表
DROP TABLE IF EXISTS #CurrentInventory
SELECT 
    companycode,
    code AS StoreCode,
    SUM(invqty) AS TotalQuantity,
    SUM(invamt) AS TotalAmount,
    COUNT(DISTINCT gid) AS ProductCount
INTO #CurrentInventory
FROM odsdbfq_result.dbo.m_stinv (NOLOCK)
WHERE rq = @EndDate 
    AND companycode IN ('HB','HN','FJ','JX','AH')
GROUP BY companycode, code

-- 创建去年同期库存数据临时表
DROP TABLE IF EXISTS #LastYearInventory
SELECT 
    companycode,
    code AS StoreCode,
    SUM(invqty) AS TotalQuantity,
    SUM(invamt) AS TotalAmount,
    COUNT(DISTINCT gid) AS ProductCount
INTO #LastYearInventory
FROM odsdbfq_result.dbo.m_stinv (NOLOCK)
WHERE rq = @LastYearEndDate 
    AND companycode IN ('HB','HN','FJ','JX','AH')
GROUP BY companycode, code

-- 关联门店信息
DROP TABLE IF EXISTS #CurrentInventoryWithInfo
SELECT 
    a.*,
    b.shoptype,
    b.syb
INTO #CurrentInventoryWithInfo
FROM #CurrentInventory a
LEFT JOIN #StoreInfo b(NOLOCK) 
    ON a.StoreCode = b.code 
    AND b.CompanyCode = 'hn' 
    AND b.stat = '有效'

-- 更新事业部信息
UPDATE #CurrentInventoryWithInfo
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
    TotalQuantity,
    TotalAmount,
    ProductCount,
    CASE 
        WHEN TotalAmount = 0 THEN '无库存'
        WHEN TotalAmount < 1000 THEN '库存偏低'
        WHEN TotalAmount > 10000 THEN '库存偏高'
        ELSE '库存正常'
    END AS InventoryStatus
FROM (
    SELECT 
        '当前库存' AS TimePeriod,
        b.shoptype AS StoreType,
        a.companycode,
        COUNT(StoreCode) AS StoreCount,
        SUM(TotalQuantity) AS TotalQuantity,
        SUM(TotalAmount) AS TotalAmount,
        SUM(ProductCount) AS ProductCount
    FROM #CurrentInventoryWithInfo a
    WHERE shoptype IS NOT NULL
    GROUP BY b.shoptype, a.companycode
    
    UNION ALL
    
    SELECT 
        '去年同期' AS TimePeriod,
        b.shoptype AS StoreType,
        a.companycode,
        COUNT(StoreCode) AS StoreCount,
        SUM(TotalQuantity) AS TotalQuantity,
        SUM(TotalAmount) AS TotalAmount,
        SUM(ProductCount) AS ProductCount
    FROM #LastYearInventory a
    LEFT JOIN #StoreInfo b(NOLOCK) 
        ON a.StoreCode = b.code 
        AND b.CompanyCode = 'hn'
    WHERE shoptype IS NOT NULL
    GROUP BY b.shoptype, a.companycode
) b
