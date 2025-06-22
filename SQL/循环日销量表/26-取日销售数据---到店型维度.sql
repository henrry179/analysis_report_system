-- =============================================
-- 日销售数据统计 - 店型维度
-- 说明: 按店型维度统计销售数据，包括同比分析
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

-- 创建当前销售数据临时表
DROP TABLE IF EXISTS #CurrentSales
SELECT 
    astore AS StoreGID,
    bgdgid AS ProductGID,
    CONVERT(VARCHAR(20), adate, 23) AS SaleDate,
    DQ1 - DQ5 AS SalesQuantity,
    DT1 - DT5 AS SalesAmount
INTO #CurrentSales
FROM odsdbfq_2024.dbo.moutdrpt_202402(NOLOCK)
WHERE adate >= @StartDate 
    AND adate <= @EndDate 
    AND companycode = 'hn'

-- 关联商品和门店信息
DROP TABLE IF EXISTS #CurrentSalesWithInfo
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
INTO #CurrentSalesWithInfo
FROM #CurrentSales a
LEFT JOIN odsdbfq_basic.dbo.goodsz b(NOLOCK) 
    ON a.ProductGID = b.gid 
    AND b.companycode = 'hn'
LEFT JOIN #StoreInfo c(NOLOCK) 
    ON a.StoreGID = c.gid 
    AND c.CompanyCode = 'hn'
WHERE b.[name] IS NOT NULL

-- 按品类汇总销售数据
DROP TABLE IF EXISTS #CategorySales
SELECT 
    SaleDate,
    CategoryCode,
    CategoryName,
    SubCategoryCode,
    SubCategoryName,
    SUM(SalesAmount) AS TotalSalesAmount
INTO #CategorySales
FROM #CurrentSalesWithInfo
GROUP BY 
    SaleDate,
    CategoryCode,
    CategoryName,
    SubCategoryCode,
    SubCategoryName

-- 创建去年同期销售数据临时表
DROP TABLE IF EXISTS #LastYearSales
SELECT 
    astore AS StoreGID,
    bgdgid AS ProductGID,
    CONVERT(VARCHAR(20), adate, 23) AS SaleDate,
    DQ1 - DQ5 AS SalesQuantity,
    DT1 - DT5 AS SalesAmount
INTO #LastYearSales
FROM odsdbfq_2023.dbo.moutdrpt_202302(NOLOCK)
WHERE adate >= @LastYearStartDate 
    AND adate <= @LastYearEndDate 
    AND companycode = 'hn'

-- 关联商品和门店信息
DROP TABLE IF EXISTS #LastYearSalesWithInfo
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
INTO #LastYearSalesWithInfo
FROM #LastYearSales a
LEFT JOIN odsdbfq_basic.dbo.goodsz b(NOLOCK) 
    ON a.ProductGID = b.gid 
    AND b.companycode = 'hn'
LEFT JOIN #StoreInfo c(NOLOCK) 
    ON a.StoreGID = c.gid 
    AND c.CompanyCode = 'hn'
WHERE b.[name] IS NOT NULL

-- 按品类汇总去年同期销售数据
DROP TABLE IF EXISTS #LastYearCategorySales
SELECT 
    SaleDate,
    CategoryCode,
    CategoryName,
    SubCategoryCode,
    SubCategoryName,
    SUM(SalesAmount) AS TotalSalesAmount
INTO #LastYearCategorySales
FROM #LastYearSalesWithInfo
GROUP BY 
    SaleDate,
    CategoryCode,
    CategoryName,
    SubCategoryCode,
    SubCategoryName

-- 创建完整品类清单
DROP TABLE IF EXISTS #CategoryList
SELECT 
    SaleDate,
    CategoryCode,
    CategoryName,
    SubCategoryCode,
    SubCategoryName
INTO #CategoryList
FROM #CategorySales
UNION
SELECT 
    SaleDate,
    CategoryCode,
    CategoryName,
    SubCategoryCode,
    SubCategoryName
FROM #LastYearCategorySales

-- 合并当前和去年同期数据
SELECT 
    a.*,
    a.CategoryCode + ' ' + a.CategoryName AS CategoryFullName,
    a.SubCategoryCode + ' ' + a.SubCategoryName AS SubCategoryFullName,
    ISNULL(b.TotalSalesAmount, 0) AS CurrentSalesAmount,
    ISNULL(c.TotalSalesAmount, 0) AS LastYearSalesAmount
FROM #CategoryList a
LEFT JOIN #CategorySales b 
    ON a.SaleDate = b.SaleDate 
    AND a.CategoryCode = b.CategoryCode
LEFT JOIN #LastYearCategorySales c 
    ON a.SaleDate = c.SaleDate 
    AND a.CategoryCode = c.CategoryCode
