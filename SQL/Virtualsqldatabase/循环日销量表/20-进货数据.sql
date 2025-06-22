/*
 * 文件名: 20-进货数据.sql
 * 功能: 进货数据分析
 * 描述: 本脚本用于分析进货数据，支持按商品、大类等多维度分析，提供同比分析功能
 */

-- 1. 获取本月进货数据
DROP TABLE IF EXISTS #tm_data1;
SELECT 
    gid AS 商品GID,
    code AS 商品编码,
    SUM(outtotal - outbcktotal) AS 出货数量,
    SUM(lackqty) AS 缺货数量,
    SUM(lacktotal) AS 缺货金额,
    SUM(ordqty) AS 订货数量,
    SUM(ordtotal) AS 订货金额,
    SUM(arvqty) AS 到货数量,
    SUM(arvtotal) AS 到货金额,
    GETDATE() AS 统计时间
INTO #tm_data1
FROM odsdbfq_result.dbo.sort_out_mout_r WITH (NOLOCK)
WHERE companycode = 'HN' 
    AND date_id >= '20240101' 
    AND date_id <= '20240131'
GROUP BY gid, code;

-- 2. 获取去年同期进货数据
DROP TABLE IF EXISTS #LY_data1;
SELECT 
    gid AS 商品GID,
    code AS 商品编码,
    SUM(outtotal - outbcktotal) AS 出货数量,
    SUM(lackqty) AS 缺货数量,
    SUM(lacktotal) AS 缺货金额,
    SUM(ordqty) AS 订货数量,
    SUM(ordtotal) AS 订货金额,
    SUM(arvqty) AS 到货数量,
    SUM(arvtotal) AS 到货金额
INTO #LY_data1
FROM odsdbfq_result.dbo.sort_out_mout_r WITH (NOLOCK)
WHERE companycode = 'HN' 
    AND date_id >= '20230101' 
    AND date_id <= '20230131'
GROUP BY gid, code;

-- 3. 合并本月和去年同期数据
DROP TABLE IF EXISTS #tt;
SELECT 
    ISNULL(a.商品编码, b.商品编码) AS 商品编码,
    a.出货数量,
    a.缺货数量,
    a.缺货金额,
    a.订货数量,
    a.订货金额,
    a.到货数量,
    a.到货金额,
    b.出货数量 AS 去年同期出货数量,
    b.缺货数量 AS 去年同期缺货数量,
    b.缺货金额 AS 去年同期缺货金额,
    b.订货数量 AS 去年同期订货数量,
    b.订货金额 AS 去年同期订货金额,
    b.到货数量 AS 去年同期到货数量,
    b.到货金额 AS 去年同期到货金额
INTO #tt
FROM #tm_data1 a
FULL JOIN #LY_data1 b ON a.商品编码 = b.商品编码;

-- 4. 输出分析结果
SELECT 
    c.大类,
    -- 商品分类
    CASE 
        WHEN c.大类 = '水' THEN '农夫水系列' 
        WHEN c.大类 = '饮料茶叶' THEN c.大类 
        ELSE '农夫其他' 
    END AS 商品分类,
    b.scode1 AS 大类编码,
    b.sname1 AS 大类名称,
    b.scode2 AS 中类编码,
    b.sname2 AS 中类名称,
    b.scode3 AS 小类编码,
    b.sname3 AS 小类名称,
    b.code AS 商品编码,
    b.[name] AS 商品名称,
    -- 本月数据
    a.出货数量,
    a.缺货数量,
    a.缺货金额,
    a.订货数量,
    a.订货金额,
    a.到货数量,
    a.到货金额,
    -- 去年同期数据
    a.去年同期到货数量,
    a.去年同期到货金额,
    -- 同比分析
    CASE 
        WHEN a.去年同期到货数量 = 0 THEN NULL
        ELSE ROUND((a.到货数量 - a.去年同期到货数量) * 100.0 / a.去年同期到货数量, 2)
    END AS 到货数量同比,
    CASE 
        WHEN a.去年同期到货金额 = 0 THEN NULL
        ELSE ROUND((a.到货金额 - a.去年同期到货金额) * 100.0 / a.去年同期到货金额, 2)
    END AS 到货金额同比,
    -- 缺货率分析
    CASE 
        WHEN a.订货数量 = 0 THEN NULL
        ELSE ROUND(a.缺货数量 * 100.0 / a.订货数量, 2)
    END AS 缺货率,
    -- 到货率分析
    CASE 
        WHEN a.订货数量 = 0 THEN NULL
        ELSE ROUND(a.到货数量 * 100.0 / a.订货数量, 2)
    END AS 到货率
FROM #tt a
LEFT JOIN odsdbfqbi.dbo.nongfu c ON a.商品编码 = c.商品编码
LEFT JOIN odsdbfq_basic.dbo.goodsz b ON a.商品编码 = b.code 
    AND b.companycode = 'hn'
WHERE c.商品编码 IS NOT NULL
ORDER BY a.到货金额 DESC;

-- 5. 清理临时表
DROP TABLE IF EXISTS #tm_data1;
DROP TABLE IF EXISTS #LY_data1;
DROP TABLE IF EXISTS #tt;

/*
 * 代码优化说明：
 * 1. 添加了详细的文件头注释，说明脚本功能和目的
 * 2. 优化了字段命名，使用中文别名提高可读性
 * 3. 添加了更多分析维度：
 *    - 商品分类分析
 *    - 同比分析
 *    - 缺货率分析
 *    - 到货率分析
 * 4. 完善了数据统计时间记录
 * 5. 添加了临时表清理代码
 * 6. 优化了代码结构和注释
 */
