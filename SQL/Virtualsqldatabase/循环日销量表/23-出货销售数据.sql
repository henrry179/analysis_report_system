/*
 * 文件名: 23-出货销售数据.sql
 * 功能: 出货销售数据分析
 * 描述: 本脚本用于分析出货和销售数据，支持按门店、商品等多维度分析，提供销售和毛利分析
 */

-- 1. 设置日期参数
DECLARE @SDD DATETIME,        -- 开始日期
        @EDD DATETIME,        -- 结束日期
        @CURDD DATETIME,      -- 当前日期
        @CY_YYYY VARCHAR(4),  -- 年份
        @CY_DATE VARCHAR(8),  -- 日期
        @SDD2 DATETIME;       -- 备用日期

SET @SDD = DATEADD(dd, DATEDIFF(dd, 0, CONVERT(datetime, '2024-02-01')), 0);
SET @CURDD = '2024-02-01';
SET @CY_DATE = CONVERT(VARCHAR(20), @SDD, 112);
SET @CY_YYYY = YEAR(@SDD);

-- 2. 创建出货数据临时表
DROP TABLE IF EXISTS #moutdrpt;
CREATE TABLE #moutdrpt (
    astore VARCHAR(10),    -- 门店编码
    adate DATETIME,        -- 日期
    bgdgid VARCHAR(10),    -- 商品编码
    dq1 MONEY,            -- 数量1
    dq5 MONEY,            -- 数量5
    dt1 MONEY,            -- 金额1
    dt5 MONEY,            -- 金额5
    whsprc MONEY          -- 仓库价格
);

-- 3. 循环获取每日出货数据
DECLARE @SQL1 VARCHAR(MAX);
WHILE @SDD < @CURDD
BEGIN
    SET @sql1 = '
    INSERT INTO #moutdrpt
    SELECT 
        astore,
        adate,
        bgdgid,
        dq1,
        dq5,
        dt1,
        dt5,
        whsprc 
    FROM odsdbfq_' + @CY_YYYY + '.dbo.moutdrpt_' + @CY_DATE + ' WITH (NOLOCK)
    WHERE companycode = ''hn''
    ';

    SET @SDD = DATEADD(day, +1, @SDD);
    SET @CY_YYYY = YEAR(@SDD);
    SET @CY_DATE = CONVERT(VARCHAR(20), @SDD, 112);
    EXEC (@SQL1);
END;

-- 4. 汇总销售数据
DROP TABLE IF EXISTS #sales;
SELECT 
    astore AS 门店编码,
    bgdgid AS 商品编码,
    SUM(DQ1 - DQ5) AS 销售数量,
    SUM(DT1 - DT5) AS 销售金额,
    SUM((DT1 - DT5) - (whsprc * (DQ1 - DQ5))) AS 销售毛利额,
    -- 计算毛利率
    CASE 
        WHEN SUM(DT1 - DT5) = 0 THEN NULL
        ELSE ROUND(SUM((DT1 - DT5) - (whsprc * (DQ1 - DQ5))) * 100.0 / SUM(DT1 - DT5), 2)
    END AS 毛利率
INTO #sales
FROM #moutdrpt
GROUP BY astore, bgdgid;

-- 5. 获取出货日报数据
DROP TABLE IF EXISTS #chuhuo;
SELECT 
    bcstgid AS 门店GID,
    bgdgid AS 商品GID,
    SUM(dq4 - dq7) AS 出货数量,
    SUM(dt4 - dt7) AS 出货金额,
    SUM((dt4 - dt7) - (di4 - di7)) AS 出货毛利额,
    -- 计算出货毛利率
    CASE 
        WHEN SUM(dt4 - dt7) = 0 THEN NULL
        ELSE ROUND(SUM((dt4 - dt7) - (di4 - di7)) * 100.0 / SUM(dt4 - dt7), 2)
    END AS 出货毛利率
INTO #chuhuo
FROM odsdbfq_basic.dbo.outdrpt WITH (NOLOCK)
WHERE adate >= '2024-02-01' 
    AND adate <= '2024-02-20' 
    AND companycode = 'HN' 
GROUP BY bgdgid, bcstgid;

-- 6. 输出分析结果
SELECT 
    a.事业部,
    a.经营区,
    a.门店编码,
    a.门店名称,
    a.商品编码,
    a.商品名称,
    -- 销售数据
    a.销售数量,
    a.销售金额,
    a.销售毛利额,
    a.毛利率,
    -- 出货数据
    a.出货数量,
    a.出货金额,
    a.出货毛利额,
    a.出货毛利率,
    -- 商品分类
    x.大类,
    CASE 
        WHEN x.大类 = '水' THEN '农夫水系列' 
        WHEN x.大类 = '饮料茶叶' THEN x.大类 
        ELSE '农夫其他' 
    END AS 商品分类,
    -- 销售状态评估
    CASE 
        WHEN a.销售金额 = 0 THEN '无销售'
        WHEN a.销售金额 < 1000 THEN '销售偏低'
        WHEN a.销售金额 > 10000 THEN '销售良好'
        ELSE '销售一般'
    END AS 销售状态,
    -- 毛利状态评估
    CASE 
        WHEN a.毛利率 IS NULL THEN '无毛利'
        WHEN a.毛利率 < 10 THEN '毛利偏低'
        WHEN a.毛利率 > 30 THEN '毛利良好'
        ELSE '毛利一般'
    END AS 毛利状态,
    -- 出货达成率
    CASE 
        WHEN a.出货数量 = 0 THEN NULL
        ELSE ROUND(a.销售数量 * 100.0 / a.出货数量, 2)
    END AS 出货达成率,
    GETDATE() AS 统计时间
FROM (
    SELECT 
        b.syb AS 事业部,
        b.kfq AS 经营区,
        b.code AS 门店编码,
        b.name AS 门店名称,
        c.code AS 商品编码,
        c.name AS 商品名称,
        s.销售数量,
        s.销售金额,
        s.销售毛利额,
        s.毛利率,
        ch.出货数量,
        ch.出货金额,
        ch.出货毛利额,
        ch.出货毛利率
    FROM (
        SELECT 
            ISNULL(s.门店编码, ch.门店GID) AS 门店编码,
            ISNULL(s.商品编码, ch.商品GID) AS 商品编码,
            s.销售数量,
            s.销售金额,
            s.销售毛利额,
            s.毛利率,
            ch.出货数量,
            ch.出货金额,
            ch.出货毛利额,
            ch.出货毛利率
        FROM #sales s
        FULL JOIN #chuhuo ch 
            ON s.门店编码 = ch.门店GID 
            AND s.商品编码 = ch.商品GID
    ) a
    LEFT JOIN odsdbfq_basic.dbo.store b WITH (NOLOCK) 
        ON a.门店编码 = b.gid 
        AND b.companycode = 'hn'
    LEFT JOIN odsdbfq_basic.dbo.goodsz c WITH (NOLOCK) 
        ON a.商品编码 = c.gid 
        AND c.companycode = 'hn'
) a
LEFT JOIN odsdbfqbi.dbo.nongfu x 
    ON a.商品编码 = x.商品编码
WHERE x.商品编码 IS NOT NULL 
    AND a.事业部 IS NOT NULL
ORDER BY a.销售金额 DESC;

-- 7. 清理临时表
DROP TABLE IF EXISTS #moutdrpt;
DROP TABLE IF EXISTS #sales;
DROP TABLE IF EXISTS #chuhuo;

/*
 * 代码优化说明：
 * 1. 添加了详细的文件头注释，说明脚本功能和目的
 * 2. 优化了字段命名，使用中文别名提高可读性
 * 3. 添加了更多分析维度：
 *    - 商品分类分析
 *    - 销售状态评估
 *    - 毛利状态评估
 *    - 毛利率计算
 *    - 出货达成率分析
 * 4. 完善了数据统计时间记录
 * 5. 添加了临时表清理代码
 * 6. 优化了代码结构和注释
 */