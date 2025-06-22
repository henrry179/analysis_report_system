-- =============================================
-- 农夫山泉出货数据分析
-- 说明: 统计和分析农夫山泉相关商品的出货数据，包括出货数量、金额和毛利
-- =============================================

-- 创建门店信息临时表
DROP TABLE IF EXISTS #StoreInfo
SELECT 
    companycode,
    shoptype,
    syb,
    kfq,
    gid,
    code,
    name,
    yybbz AS BusinessUnit,  -- 业务单元
    MENTOR AS Mentor,       -- 经营区长
    MANAGER AS Manager,     -- 指导员
    stat
INTO #StoreInfo 
FROM odsdbfq_basic.dbo.store(NOLOCK)
WHERE companycode = 'hn'

-- 更新门店类型
UPDATE #StoreInfo
SET shoptype = '标准门店' 
WHERE shoptype = '食品事业部' 
    AND companycode = 'hn'

-- 更新业务单元为农夫山泉的门店类型
UPDATE #StoreInfo
SET shoptype = '食品事业部' 
WHERE BusinessUnit = '农夫山泉' 
    AND companycode = 'hn'

-- 更新业务单元为农夫山泉的事业部
UPDATE #StoreInfo
SET syb = '食品事业部' 
WHERE BusinessUnit = '农夫山泉' 
    AND companycode = 'hn'

-- 创建出货数据临时表
DROP TABLE IF EXISTS #ShipmentData
SELECT 
    bcstgid AS StoreGID,    -- 门店GID
    bgdgid AS ProductGID,   -- 商品GID
    SUM(dq4 - dq7) AS ShipmentQuantity,  -- 出货数量
    SUM(dt4 - dt7) AS ShipmentAmount,    -- 出货金额
    SUM((dt4-dt7)-(di4-di7)) AS ShipmentProfit  -- 出货毛利
INTO #ShipmentData
FROM odsdbfq_basic.dbo.outdrpt (NOLOCK)
WHERE adate >= '2023-03-01' 
    AND adate <= '2023-03-31' 
    AND companycode = 'HN' 
GROUP BY bgdgid, bcstgid

-- 输出最终结果
SELECT 
    a.*,
    b.code AS ProductCode,      -- 商品编码
    b.name AS ProductName,      -- 商品名称
    c.code AS StoreCode,        -- 门店编码
    c.name AS StoreName,        -- 门店名称
    c.syb AS BusinessUnit,      -- 事业部
    c.kfq AS OperationArea,     -- 经营区
    d.ProductType               -- 商品类型
FROM #ShipmentData a
LEFT JOIN odsdbFQ_basic.dbo.goodsz b(NOLOCK) 
    ON a.ProductGID = b.gid 
    AND b.companycode = 'hn' 
LEFT JOIN #StoreInfo c(NOLOCK) 
    ON a.StoreGID = c.gid 
    AND c.companycode = 'hn'
LEFT JOIN odsdbfqbi.dbo.nongfu d 
    ON a.ProductCode = d.ProductCode
WHERE d.ProductCode IS NOT NULL
ORDER BY a.ShipmentAmount DESC