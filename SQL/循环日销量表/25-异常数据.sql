-- =============================================
-- 异常数据分析
-- 说明: 检测和分析销售数据中的异常情况
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
WHERE companycode = 'hn'

-- 更新门店类型
UPDATE #StoreInfo
SET shoptype = '标准门店' 
WHERE code IN (SELECT StoreCode FROM odsdbfqbi.dbo.xsb)

-- 创建异常数据临时表
DROP TABLE IF EXISTS #ExceptionData
SELECT 
    astore AS StoreGID,
    bgdgid AS ProductGID,
    SUM(saleqty) AS SalesQuantity,
    SUM(saletotal) AS SalesAmount,
    SUM(salemle) AS SalesProfit
INTO #ExceptionData
FROM odsdbfqtemp.dbo.moutdrpt_yccl (NOLOCK)
WHERE companycode = 'hn' 
    AND adate >= @StartDate 
    AND adate <= @EndDate 
    AND saletotal > 0
GROUP BY astore, bgdgid

-- 创建去年同期异常数据临时表
DROP TABLE IF EXISTS #LastYearExceptionData
SELECT 
    astore AS StoreGID,
    bgdgid AS ProductGID,
    SUM(saleqty) AS SalesQuantity,
    SUM(saletotal) AS SalesAmount,
    SUM(salemle) AS SalesProfit
INTO #LastYearExceptionData
FROM odsdbfqtemp.dbo.moutdrpt_yccl (NOLOCK)
WHERE companycode = 'hn' 
    AND adate >= @LastYearStartDate 
    AND adate <= @LastYearEndDate 
    AND saletotal > 0
GROUP BY astore, bgdgid

-- 创建完整数据清单
DROP TABLE IF EXISTS #CompleteList
SELECT StoreGID, ProductGID 
INTO #CompleteList 
FROM #ExceptionData
UNION
SELECT StoreGID, ProductGID 
FROM #LastYearExceptionData

-- 合并当前和去年同期数据
DROP TABLE IF EXISTS #MergedData
SELECT 
    a.*,
    ISNULL(b.SalesQuantity, 0) AS CurrentSalesQuantity,
    ISNULL(b.SalesAmount, 0) AS CurrentSalesAmount,
    ISNULL(b.SalesProfit, 0) AS CurrentSalesProfit,
    ISNULL(c.SalesQuantity, 0) AS LastYearSalesQuantity,
    ISNULL(c.SalesAmount, 0) AS LastYearSalesAmount,
    ISNULL(c.SalesProfit, 0) AS LastYearSalesProfit
INTO #MergedData 
FROM #CompleteList a
LEFT JOIN #ExceptionData b 
    ON a.StoreGID = b.StoreGID 
    AND a.ProductGID = b.ProductGID
LEFT JOIN #LastYearExceptionData c 
    ON a.StoreGID = c.StoreGID 
    AND a.ProductGID = c.ProductGID

-- 输出最终结果
SELECT 
    a.*,
    b.scode1 AS CategoryCode,
    b.sname1 AS CategoryName,
    b.scode2 AS SubCategoryCode,
    b.sname2 AS SubCategoryName,
    b.code AS ProductCode,
    b.[name] AS ProductName,
    c.code AS StoreCode,
    c.[name] AS StoreName,
    c.syb AS BusinessUnit,
    shoptype AS StoreType
FROM #MergedData a
LEFT JOIN odsdbfq_basic.dbo.goodsz b(NOLOCK) 
    ON a.ProductGID = b.gid 
    AND b.companycode = 'hn'
LEFT JOIN #StoreInfo c(NOLOCK) 
    ON a.StoreGID = c.gid 
    AND c.CompanyCode = 'hn'
WHERE b.[name] IS NOT NULL
