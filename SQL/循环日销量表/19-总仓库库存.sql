/*
 * 文件名: 19-总仓库库存.sql
 * 功能: 总仓库库存数据分析
 * 描述: 本脚本用于分析总仓库库存数据，支持按商品、仓库、大类等多维度分析，提供库存健康度评估
 */

-- 1. 获取总仓库库存数据
DROP TABLE IF EXISTS #stk;
SELECT 
    a.gdgid AS 商品gid,
    b.code AS 商品编码,
    b.scode1 AS 大类编码,
    b.sname1 AS 大类名称,
    b.[name] AS 商品名称,
    wrh AS 仓位,
    qty AS 库存数量,
    qty * ISNULL(INPRC, 0) AS 库存金额,
    INPRC AS 入库单价,
    GETDATE() AS 统计时间
INTO #stk 
FROM odsdbfq_basic.dbo.inv a WITH (NOLOCK)
LEFT JOIN odsdbfq_basic.dbo.goodsz b WITH (NOLOCK) ON a.gdgid = b.gid 
    AND b.companycode = 'hn'
WHERE a.companycode = 'hn' 
    AND b.scode1 IS NOT NULL  -- 排除无分类商品
    AND a.store = '1800000'   -- 总仓库gid
    AND qty > 0;              -- 只统计有库存的商品

-- 2. 获取仓库信息
DROP TABLE IF EXISTS #wrh;
SELECT 
    code AS 仓库编码,
    name AS 仓库名称,
    wareHouseType AS 仓库类型,
    LogisticName AS 物流名称,
    address AS 仓库地址,
    contact AS 联系人,
    phone AS 联系电话
INTO #wrh
FROM odsdbfq_basic.dbo.warehouse WITH (NOLOCK)
WHERE companycode = 'hn'
    AND LogisticName IS NOT NULL
    AND wareHouseType = '总仓库'
    AND CHARINDEX('停用', name) = 0
    AND wareHouseType NOT LIKE '设备%';

-- 3. 按大类汇总库存数据
SELECT 
    大类编码,
    大类名称,
    COUNT(DISTINCT 商品编码) AS 商品数,
    SUM(库存数量) AS 总库存数量,
    SUM(库存金额) AS 总库存金额,
    ROUND(SUM(库存金额) / NULLIF(COUNT(DISTINCT 商品编码), 0), 2) AS 商品平均库存金额,
    ROUND(SUM(库存数量) / NULLIF(COUNT(DISTINCT 商品编码), 0), 2) AS 商品平均库存数量
FROM #stk
GROUP BY 大类编码, 大类名称
ORDER BY 总库存金额 DESC;

-- 4. 按仓库汇总库存数据
SELECT 
    a.仓库编码,
    a.仓库名称,
    a.仓库类型,
    a.物流名称,
    COUNT(DISTINCT b.商品编码) AS 商品数,
    SUM(b.库存数量) AS 总库存数量,
    SUM(b.库存金额) AS 总库存金额,
    ROUND(SUM(b.库存金额) / NULLIF(COUNT(DISTINCT b.商品编码), 0), 2) AS 商品平均库存金额,
    ROUND(SUM(b.库存数量) / NULLIF(COUNT(DISTINCT b.商品编码), 0), 2) AS 商品平均库存数量
FROM #wrh a
LEFT JOIN #stk b ON a.仓库编码 = b.仓位
GROUP BY a.仓库编码, a.仓库名称, a.仓库类型, a.物流名称
ORDER BY 总库存金额 DESC;

-- 5. 库存健康度分析
SELECT 
    商品编码,
    商品名称,
    大类编码,
    大类名称,
    仓位,
    (SELECT 仓库名称 FROM #wrh WHERE 仓库编码 = #stk.仓位) AS 仓库名称,
    库存数量,
    库存金额,
    入库单价,
    -- 库存健康度评估
    CASE 
        WHEN 库存金额 = 0 THEN '无库存'
        WHEN 库存金额 < 1000 THEN '库存偏低'
        WHEN 库存金额 > 10000 THEN '库存偏高'
        ELSE '库存正常'
    END AS 库存健康度,
    统计时间
FROM #stk
ORDER BY 库存金额 DESC;

-- 6. 农夫山泉商品专项分析
SELECT 
    a.*,
    b.大类编码,
    b.大类名称,
    c.仓库名称,
    -- 商品分类
    CASE 
        WHEN b.大类编码 = '水' THEN '农夫水系列' 
        WHEN b.大类编码 = '饮料茶叶' THEN b.大类名称
        ELSE '农夫其他' 
    END AS 商品分类,
    -- 库存状态
    CASE 
        WHEN a.库存金额 = 0 THEN '无库存'
        WHEN a.库存金额 < 1000 THEN '库存偏低'
        WHEN a.库存金额 > 10000 THEN '库存偏高'
        ELSE '库存正常'
    END AS 库存状态
FROM #stk a
LEFT JOIN odsdbfqbi.dbo.nongfu b ON a.商品编码 = b.商品编码
LEFT JOIN #wrh c ON a.仓位 = c.仓库编码
WHERE b.商品编码 IS NOT NULL 
    AND c.仓库名称 IS NOT NULL
ORDER BY a.库存金额 DESC;

-- 7. 清理临时表
DROP TABLE IF EXISTS #stk;
DROP TABLE IF EXISTS #wrh;

/*
 * 代码优化说明：
 * 1. 添加了详细的文件头注释，说明脚本功能和目的
 * 2. 优化了字段命名，使用中文别名提高可读性
 * 3. 添加了更多分析维度，如大类汇总、仓库汇总等
 * 4. 新增库存健康度评估功能
 * 5. 完善了农夫山泉商品专项分析
 * 6. 添加了临时表清理代码
 * 7. 优化了代码结构和注释
 */
