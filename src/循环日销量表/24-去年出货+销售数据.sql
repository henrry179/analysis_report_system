-- 创建临时表存储销售数据
DECLARE @StartDate DATETIME,        -- 开始日期
        @EndDate DATETIME,          -- 结束日期
        @CurrentDate DATETIME,      -- 当前日期
        @Year VARCHAR(4),           -- 年份
        @DateStr VARCHAR(8),        -- 日期字符串
        @StartDate2 DATETIME        -- 备用开始日期

-- 设置初始日期参数
SET @StartDate = DATEADD(dd, DATEDIFF(dd, 0, convert(datetime,'2023-02-01')), 0)
SET @CurrentDate = '2023-02-01'
SET @DateStr = CONVERT(VARCHAR(20), @StartDate, 112)
SET @Year = YEAR(@StartDate)

-- 输出参数值用于调试
SELECT @DateStr AS DateString,
       @Year AS Year,
       @StartDate AS StartDate,
       @CurrentDate AS CurrentDate

-- 创建临时表存储销售报表数据
DROP TABLE IF EXISTS #moutdrpt
CREATE TABLE #moutdrpt
(
    astore VARCHAR(10),    -- 门店编号
    adate DATETIME,        -- 日期
    bgdgid VARCHAR(10),    -- 商品编号
    dq1 MONEY,            -- 数量1
    dq5 MONEY,            -- 数量5
    dt1 MONEY,            -- 金额1
    dt5 MONEY,            -- 金额5
    whsprc MONEY          -- 批发价格
)

-- 循环插入销售数据
DECLARE @SQL1 VARCHAR(MAX)

-- 注意：hn表示双引号
WHILE @StartDate < @CurrentDate
BEGIN
    SET @sql1 = '
    INSERT INTO #moutdrpt
    SELECT astore, adate, bgdgid, dq1, dq5, dt1, dt5, whsprc 
    FROM odsdbfq_' + @Year + '.dbo.moutdrpt_' + @DateStr + ' with (NOLOCK)
    WHERE companycode = ''hn''
    '
    
    SET @StartDate = DATEADD(day, +1, @StartDate)
    SET @Year = YEAR(@StartDate)
    SET @DateStr = CONVERT(VARCHAR(20), @StartDate, 112)
    EXEC (@SQL1)
END

-- 计算销售汇总数据
DROP TABLE IF EXISTS #sales
SELECT 
    astore,
    bgdgid,
    SUM(DQ1 - DQ5) as SalesQuantity,        -- 销售数量
    SUM(DT1 - DT5) as SalesAmount,          -- 销售金额
    SUM((DT1 - DT5) - (whsprc*(DQ1-DQ5))) as SalesProfit  -- 销售毛利额
INTO #sales
FROM #moutdrpt
GROUP BY astore, bgdgid

-- 获取出货日报
DROP TABLE IF EXISTS #chuhuo
SELECT 
    bcstgid as StoreGID,                    -- 门店GID
    bgdgid as ProductGID,                   -- 商品GID
    SUM(dq4 - dq7) as ShipQuantity,         -- 出货数量
    SUM(dt4 - dt7) as ShipAmount,           -- 出货金额
    SUM((dt4-dt7)-(di4-di7)) as ShipProfit  -- 出货毛利额
INTO #chuhuo
FROM odsdbfq_basic.dbo.outdrpt (NOLOCK)
WHERE adate >= '2023-02-01' 
    AND adate <= '2023-02-28' 
    AND companycode = 'HN' 
GROUP BY bgdgid, bcstgid

-- 最终结果查询
SELECT 
    a.*,
    Category,
    CASE 
        WHEN Category = '水' THEN '农夫水系列'
        WHEN Category = '饮料茶叶' THEN Category
        ELSE '农夫其他'
    END as Category2
FROM (
    SELECT 
        b.syb as BusinessUnit,              -- 事业部
        kfq as OperationArea,               -- 经营区
        b.code as StoreCode,                -- 门店代码
        b.name as StoreName,                -- 门店名称
        c.code as ProductCode,              -- 商品代码
        c.name as ProductName,              -- 商品名称
        SalesQuantity,                      -- 销售数量
        SalesAmount,                        -- 销售金额
        SalesProfit,                        -- 销售毛利额
        ShipQuantity,                       -- 出货数量
        ShipAmount,                         -- 出货金额
        ShipProfit                          -- 出货毛利额
    FROM (
        SELECT 
            ISNULL(astore, StoreGID) as astore,
            ISNULL(bgdgid, ProductGID) as bgdgid,
            SalesQuantity,
            SalesAmount,
            SalesProfit,
            ShipQuantity,
            ShipAmount,
            ShipProfit
        FROM #sales a
        FULL JOIN #chuhuo b ON a.astore = b.StoreGID AND a.bgdgid = b.ProductGID
    ) a
    LEFT JOIN odsdbfq_basic.dbo.store b(NOLOCK) 
        ON a.astore = b.gid AND b.companycode = 'hn'
    LEFT JOIN odsdbFQ_basic.dbo.goodsz c(NOLOCK) 
        ON a.bgdgid = c.gid AND c.companycode = 'hn'
) a
LEFT JOIN odsdbfqbi.dbo.nongfu x 
    ON a.ProductCode = x.ProductCode
WHERE x.ProductCode IS NOT NULL 
    AND BusinessUnit IS NOT NULL