/*
 * 文件名: 18-门店库存数据.sql
 * 功能: 门店库存数据分析
 * 描述: 本脚本用于分析门店库存数据，支持按门店、商品、事业部等多维度分析，提供库存健康度评估
 */

-- 1. 获取门店信息
DROP TABLE IF EXISTS #store_inf;
SELECT 
    companycode AS 公司代码,
    shoptype AS 门店类型,
    syb AS 事业部,
    kfq AS 经营区,
    code AS 门店编码,
    gid AS 门店GID,
    name AS 门店名称,
    yybbz AS 营业部标志,
    MENTOR AS 经营区长,
    MANAGER AS 指导员,
    stat AS 状态
INTO #store_inf 
FROM odsdbfq_basic.dbo.store WITH (NOLOCK)
WHERE companycode = 'hn' 
    AND daqu IS NOT NULL;  -- 确保门店有大区信息

-- 2. 更新门店类型（标准化门店类型）
UPDATE #store_inf
SET 门店类型 = '标准便利店' 
WHERE 门店类型 = '零食便利店' 
    AND 公司代码 = 'hn';

UPDATE #store_inf
SET 门店类型 = '零食便利店' 
WHERE 营业部标志 = '零食部' 
    AND 公司代码 = 'hn';

-- 3. 获取门店库存数据
DROP TABLE IF EXISTS #stk;
SELECT 
    syb AS 事业部,
    a.store AS 门店gid,
    a.gdgid AS 商品gid,
    b.code AS 商品编码,
    b.scode1 AS 大类编码,
    b.sname1 AS 大类名称,
    b.[name] AS 商品名称,
    c.code AS 门店编码,
    c.[name] AS 门店名称,
    shoptype AS 门店类型,
    wrh AS 仓位,
    qty AS 库存数量,
    qty * ISNULL(INPRC, 0) AS 库存金额,
    INPRC AS 入库单价,
    GETDATE() AS 统计时间
INTO #stk 
FROM odsdbfq_basic.dbo.inv a WITH (NOLOCK)
LEFT JOIN odsdbfq_basic.dbo.goodsz b WITH (NOLOCK) ON a.gdgid = b.gid 
    AND b.companycode = 'hn'
LEFT JOIN #store_inf c WITH (NOLOCK) ON a.store = c.gid 
    AND c.公司代码 = 'hn'
WHERE a.companycode = 'hn' 
    AND b.scode1 IS NOT NULL  -- 排除无分类商品
    AND c.code <> '08'        -- 排除总部
    AND qty > 0              -- 只统计有库存的商品
    AND shoptype IS NOT NULL; -- 确保门店类型有效

-- 4. 按事业部汇总库存数据
SELECT 
    事业部,
    COUNT(DISTINCT 门店编码) AS 门店数,
    COUNT(DISTINCT 商品编码) AS 商品数,
    SUM(库存数量) AS 总库存数量,
    SUM(库存金额) AS 总库存金额,
    ROUND(SUM(库存金额) / NULLIF(COUNT(DISTINCT 门店编码), 0), 2) AS 店均库存金额,
    ROUND(SUM(库存数量) / NULLIF(COUNT(DISTINCT 门店编码), 0), 2) AS 店均库存数量
FROM #stk
GROUP BY 事业部
ORDER BY 总库存金额 DESC;

-- 5. 按大类汇总库存数据
SELECT 
    大类编码,
    大类名称,
    COUNT(DISTINCT 门店编码) AS 覆盖门店数,
    COUNT(DISTINCT 商品编码) AS 商品数,
    SUM(库存数量) AS 总库存数量,
    SUM(库存金额) AS 总库存金额,
    ROUND(SUM(库存金额) / NULLIF(COUNT(DISTINCT 门店编码), 0), 2) AS 店均库存金额,
    ROUND(SUM(库存数量) / NULLIF(COUNT(DISTINCT 门店编码), 0), 2) AS 店均库存数量
FROM #stk
GROUP BY 大类编码, 大类名称
ORDER BY 总库存金额 DESC;

-- 6. 门店库存健康度分析
SELECT 
    门店编码,
    门店名称,
    门店类型,
    事业部,
    经营区,
    经营区长,
    指导员,
    COUNT(DISTINCT 商品编码) AS 库存商品数,
    SUM(库存数量) AS 总库存数量,
    SUM(库存金额) AS 总库存金额,
    -- 库存健康度评估
    CASE 
        WHEN SUM(库存金额) = 0 THEN '无库存'
        WHEN SUM(库存金额) < 1000 THEN '库存偏低'
        WHEN SUM(库存金额) > 10000 THEN '库存偏高'
        ELSE '库存正常'
    END AS 库存健康度
FROM #stk
GROUP BY 门店编码, 门店名称, 门店类型, 事业部, 经营区, 经营区长, 指导员
ORDER BY 总库存金额 DESC;

-- 7. 输出农夫山泉商品库存数据（专项分析）
SELECT 
    事业部,
    门店编码,
    门店名称,
    门店类型,
    经营区,
    经营区长,
    指导员,
    商品编码,
    商品名称,
    库存数量,
    库存金额,
    入库单价,
    统计时间
FROM #stk
WHERE 商品编码 IN (
    SELECT 商品编码 
    FROM odsdbfqbi.dbo.nongfu
)
ORDER BY 事业部, 门店编码, 库存金额 DESC;

-- 8. 清理临时表
DROP TABLE IF EXISTS #store_inf;
DROP TABLE IF EXISTS #stk;

/*
 * 代码优化说明：
 * 1. 添加了详细的文件头注释，说明脚本功能和目的
 * 2. 优化了字段命名，使用中文别名提高可读性
 * 3. 添加了更多分析维度，如事业部汇总、大类汇总等
 * 4. 新增库存健康度评估功能
 * 5. 完善了农夫山泉商品专项分析
 * 6. 添加了临时表清理代码
 * 7. 优化了代码结构和注释
 */