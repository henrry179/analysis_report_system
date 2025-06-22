/*
 * 文件名: 21-周转天数.sql
 * 功能: 商品周转天数分析
 * 描述: 本脚本用于分析商品周转天数，支持按商品、大类等多维度分析，提供周转效率评估
 */

-- 1. 获取商品周转数据
WITH 商品周转数据 AS (
    SELECT 
        a.adate AS 统计月份,
        a.goodscode AS 商品编码,
        a.invqty AS 库存数量,
        a.invtotal AS 库存金额,
        a.outqty AS 出货数量,
        a.outtotal AS 出货金额,
        a.bwrh AS 仓库编码,
        a.wrhmemo AS 仓库名称,
        b.name AS 商品名称,
        b.scode1 AS 大类编码,
        b.sname1 AS 大类名称,
        b.scode2 AS 中类编码,
        b.sname2 AS 中类名称,
        b.scode3 AS 小类编码,
        b.sname3 AS 小类名称,
        c.大类,
        -- 商品分类
        CASE 
            WHEN c.大类 = '水' THEN '农夫水系列' 
            WHEN c.大类 = '饮料茶叶' THEN c.大类 
            ELSE '农夫其他' 
        END AS 商品分类,
        -- 周转天数计算
        CASE 
            WHEN a.outqty = 0 THEN NULL
            ELSE ROUND(a.invqty * 30.0 / a.outqty, 2)
        END AS 周转天数,
        -- 周转率计算
        CASE 
            WHEN a.invqty = 0 THEN NULL
            ELSE ROUND(a.outqty * 100.0 / a.invqty, 2)
        END AS 周转率,
        -- 周转效率评估
        CASE 
            WHEN a.outqty = 0 THEN '无销售'
            WHEN a.invqty = 0 THEN '无库存'
            WHEN a.invqty * 30.0 / a.outqty <= 7 THEN '周转良好'
            WHEN a.invqty * 30.0 / a.outqty <= 15 THEN '周转一般'
            ELSE '周转较差'
        END AS 周转效率,
        GETDATE() AS 统计时间
    FROM odsdbfq_result.dbo.zhh_mon_goods_zzts a WITH (NOLOCK)
    LEFT JOIN odsdbfq_basic.dbo.goodsz b WITH (NOLOCK) 
        ON a.goodscode = b.code 
        AND b.companycode = 'hn'
    LEFT JOIN odsdbfqbi.dbo.nongfu c 
        ON a.goodscode = c.商品编码
    WHERE a.companycode = 'hn' 
        AND a.wrhmemo = '总仓库' 
        AND a.adate = '202401'
)

-- 2. 输出分析结果
SELECT 
    统计月份,
    商品编码,
    商品名称,
    大类编码,
    大类名称,
    中类编码,
    中类名称,
    小类编码,
    小类名称,
    大类,
    商品分类,
    库存数量,
    库存金额,
    出货数量,
    出货金额,
    仓库编码,
    仓库名称,
    周转天数,
    周转率,
    周转效率,
    统计时间
FROM 商品周转数据
WHERE 大类 IS NOT NULL
ORDER BY 周转天数;

/*
 * 代码优化说明：
 * 1. 添加了详细的文件头注释，说明脚本功能和目的
 * 2. 优化了字段命名，使用中文别名提高可读性
 * 3. 添加了更多分析维度：
 *    - 商品分类分析
 *    - 周转天数计算
 *    - 周转率计算
 *    - 周转效率评估
 * 4. 使用CTE优化代码结构
 * 5. 完善了数据统计时间记录
 * 6. 优化了代码结构和注释
 */