/*
 * 文件名: 16-循环日销表V2.sql
 * 功能: 循环门店销售分析（增强版）
 * 描述: 本脚本通过循环处理每日销售数据，统计门店销售与库存情况，支持按门店、商品、备注等多维度分析，是循环日销量表的优化版本
 */

-- 1. 定义日期参数
DECLARE @SDD DATETIME;        -- 开始日期
DECLARE @EDD DATETIME;        -- 结束日期（当前日期的前一天）
DECLARE @CURDD DATETIME;      -- 当前日期
DECLARE @CY_YYYY VARCHAR(4);  -- 当前年份
DECLARE @CY_DATE VARCHAR(8);  -- 当前日期(YYYYMMDD格式)
DECLARE @DDP_PERIOD VARCHAR(6) = '202401';  -- 大单品期间代码（可根据需要修改）

-- 智能设置日期变量（可根据需要修改）
SET @SDD = DATEADD(dd, DATEDIFF(dd, 0, CONVERT(DATETIME, '2024-1-1')), 0);  -- 开始日期(2024年1月1日)
SET @EDD = DATEADD(dd, DATEDIFF(dd, 0, GETDATE()-1), 0);                    -- 结束日期(昨日)
SET @CURDD = DATEADD(dd, DATEDIFF(dd, 0, GETDATE()), 0);                    -- 当前日期
SET @CY_DATE = CONVERT(VARCHAR(20), @SDD, 112);                             -- 转为YYYYMMDD格式
SET @CY_YYYY = YEAR(@SDD);                                                  -- 获取年份

-- 输出日期参数（便于调试和确认）
SELECT 
    @CY_DATE AS 日期代码,
    @CY_YYYY AS 年份,
    @SDD AS 开始日期,
    @EDD AS 结束日期,
    @CURDD AS 当前日期,
    DATEDIFF(day, @SDD, @EDD) + 1 AS 总天数,
    @DDP_PERIOD AS 大单品期间代码;

-- 2. 创建销售数据临时表
DROP TABLE IF EXISTS #moutdrpt;
CREATE TABLE #moutdrpt (
    astore VARCHAR(10),     -- 门店GID
    adate DATETIME,         -- 销售日期
    bgdgid VARCHAR(10),     -- 商品GID
    dq1 MONEY,              -- 销售数量
    dq5 MONEY,              -- 退货数量
    dt1 MONEY,              -- 销售金额
    dt5 MONEY               -- 退货金额
);

-- 3. 循环获取每日销售数据
DECLARE @SQL1 VARCHAR(MAX);
PRINT '开始循环获取销售数据，日期范围: ' + CONVERT(VARCHAR(10), @SDD, 23) + ' 至 ' + CONVERT(VARCHAR(10), @EDD, 23);

WHILE @SDD < @CURDD
BEGIN
    -- 构建动态SQL语句
    SET @SQL1 = '
    INSERT INTO #moutdrpt
    SELECT 
        astore,             -- 门店GID
        adate,              -- 销售日期
        bgdgid,             -- 商品GID
        dq1,                -- 销售数量
        dq5,                -- 退货数量
        dt1,                -- 销售金额
        dt5                 -- 退货金额
    FROM odsdbfq_' + @CY_YYYY + '.dbo.moutdrpt_' + @CY_DATE + ' WITH (NOLOCK)
    WHERE companycode = ''hn''
    ';
    
    -- 输出正在处理的日期（调试用）
    PRINT '正在处理: ' + @CY_DATE;
    
    -- 执行动态SQL，添加错误处理
    BEGIN TRY
        EXEC (@SQL1);
    END TRY
    BEGIN CATCH
        PRINT '处理日期 ' + @CY_DATE + ' 出错: ' + ERROR_MESSAGE();
    END CATCH

    -- 日期前进一天
    SET @SDD = DATEADD(day, 1, @SDD);
    SET @CY_YYYY = YEAR(@SDD);
    SET @CY_DATE = CONVERT(VARCHAR(20), @SDD, 112);
END

-- 4. 获取大单品清单
DROP TABLE IF EXISTS #ddplist;
SELECT 
    a.*,                      -- 大单品基础信息
    b.gid,                    -- 商品GID
    scode1 AS 大类,            -- 商品大类编码
    sname1 AS 大类名           -- 商品大类名称
INTO #ddplist 
FROM odsdbfqbi.dbo.ddp_hn a
LEFT JOIN odsdbfq_basic.dbo.goodsz b WITH (NOLOCK) ON a.itemcode = b.code 
    AND b.companycode = 'hn'
WHERE mydate = @DDP_PERIOD    -- 使用参数化的期间代码
    AND DQ = '全月';          -- 仅包含全月数据

-- 5. 统计大单品销售数据
DROP TABLE IF EXISTS #sale_data1;
SELECT 
    astore AS storegid,        -- 门店GID
    bgdgid AS 商品gid,         -- 商品GID
    SUM(DQ1 - DQ5) AS 销售数量, -- 计算净销售数量（销售-退货）
    SUM(DT1 - DT5) AS 销售金额  -- 计算净销售金额（销售-退货）
INTO #sale_data1
FROM #moutdrpt
WHERE bgdgid IN (SELECT gid FROM #ddplist)  -- 仅包含大单品清单中的商品
GROUP BY astore, bgdgid;

-- 6. 统计所有门店销售数据（不限于大单品）
DROP TABLE IF EXISTS #sale_data11;
SELECT 
    astore AS storegid,        -- 门店GID
    bgdgid AS 商品gid,         -- 商品GID
    SUM(DQ1 - DQ5) AS 销售数量, -- 计算净销售数量（销售-退货）
    SUM(DT1 - DT5) AS 销售金额  -- 计算净销售金额（销售-退货）
INTO #sale_data11
FROM #moutdrpt
GROUP BY astore, bgdgid;

-- 7. 获取0705类商品销售数据（用于判断门店是否开展特定活动）
DROP TABLE IF EXISTS #sales0705;
SELECT 
    a.*,                      -- 销售基础数据
    c.code AS 门店编码,         -- 门店编码
    b.scode2,                 -- 商品小类编码
    c.syb AS 事业部            -- 所属事业部
INTO #sales0705 
FROM #sale_data11 a
LEFT JOIN odsdbfq_basic.dbo.goodsz b WITH (NOLOCK) ON a.商品gid = b.gid 
    AND b.companycode = 'hn'
LEFT JOIN odsdbfq_basic.dbo.store c WITH (NOLOCK) ON a.storegid = c.gid 
    AND c.companycode = 'hn'
WHERE b.scode2 = '0705';      -- 筛选0705类商品（通常为特定活动商品）

-- 8. 统计有效门店数量（按事业部分组）
SELECT 
    ISNULL(d.事业部, a.事业部) AS 事业部,    -- 优先使用storeinf表中的事业部
    COUNT(门店编码) AS 有效门店数,           -- 统计门店数量
    '销售0705类商品的门店' AS 说明           -- 数据说明
FROM (
    -- 获取有销售的门店
    SELECT DISTINCT 门店编码, 事业部 
    FROM #sales0705 
    WHERE 销售金额 > 0                     -- 仅包含有销售的门店
) a
LEFT JOIN odsdbfqbi.dbo.storeinf d ON a.门店编码 = d.编码
GROUP BY ISNULL(d.事业部, a.事业部)
ORDER BY 事业部;                           -- 按事业部排序

-- 9. 匹配销售数据与门店、商品信息
DROP TABLE IF EXISTS #sale_data2;
SELECT 
    c.shoptype AS 门店类型,     -- 门店类型
    c.syb AS 事业部,            -- 所属事业部
    c.kfq AS 经营区,            -- 所属经营区
    c.mentor AS 区长,           -- 区长信息
    c.manager AS 指导员,        -- 指导员信息
    c.code AS 门店编码,          -- 门店编码
    b.大类,                     -- 商品大类编码
    b.大类名,                   -- 商品大类名称
    b.remark AS 备注,           -- 备注（商品分类标识）
    b.DQ AS 区域,               -- 区域信息
    b.itemcode AS 商品编码,      -- 商品编码
    b.itemcn AS 商品名称,        -- 商品名称
    a.销售数量,                 -- 销售数量
    a.销售金额                  -- 销售金额
INTO #sale_data2 
FROM #sale_data1 a
LEFT JOIN #ddplist b ON a.商品gid = b.gid
LEFT JOIN odsdbfq_basic.dbo.store c WITH (NOLOCK) ON a.storegid = c.gid 
    AND c.companycode = 'hn';

-- 10. 获取库存数据
DROP TABLE IF EXISTS #stk;
SELECT 
    a.store AS 门店gid,         -- 门店GID
    a.gdgid AS 商品gid,         -- 商品GID
    b.code AS 商品编码,          -- 商品编码
    b.scode1 AS 大类,           -- 商品大类编码
    b.sname1 AS 大类名,          -- 商品大类名称
    b.[name] AS 商品名称,        -- 商品名称
    c.code AS 门店编码,          -- 门店编码
    c.[name] AS 门店名称,        -- 门店名称
    c.shoptype AS 门店类型,      -- 门店类型
    c.syb AS 事业部,             -- 所属事业部
    c.kfq AS 经营区,             -- 所属经营区
    c.mentor AS 区长,            -- 区长信息
    c.manager AS 指导员,         -- 指导员信息
    a.wrh,                      -- 仓位
    a.qty AS 库存数量,           -- 库存数量
    a.qty * ISNULL(a.whsprc, 0) AS 库存金额  -- 计算库存金额（数量*单价）
INTO #stk 
FROM odsdbfq_basic.dbo.inv a WITH (NOLOCK)
LEFT JOIN odsdbfq_basic.dbo.goodsz b WITH (NOLOCK) ON a.gdgid = b.gid 
    AND b.companycode = 'hn'
LEFT JOIN odsdbfq_basic.dbo.store c WITH (NOLOCK) ON a.store = c.gid 
    AND c.CompanyCode = 'hn'
WHERE a.companycode = 'hn'      -- 筛选公司
    AND b.scode1 IS NOT NULL    -- 排除无分类商品
    AND c.code <> '08'          -- 排除特定门店（08总部）
    AND a.gdgid IN (SELECT gid FROM #ddplist);  -- 仅包含大单品清单中的商品

-- 11. 匹配库存数据与商品信息
DROP TABLE IF EXISTS #stk2;
SELECT 
    a.*,                       -- 库存基础数据
    b.remark AS 备注,           -- 备注（商品分类标识）
    b.DQ AS 区域                -- 区域信息
INTO #stk2 
FROM #stk a
LEFT JOIN #ddplist b ON a.商品编码 = b.itemcode;

-- 12. 按门店和备注分组统计销售汇总
DROP TABLE IF EXISTS #sale01;
SELECT 
    备注,                      -- 备注（商品分类标识）
    门店编码,                   -- 门店编码
    SUM(销售数量) AS 销售数量,    -- 汇总销售数量
    SUM(销售金额) AS 销售金额     -- 汇总销售金额
INTO #sale01 
FROM #sale_data2
GROUP BY 门店编码, 备注;

-- 13. 按门店和备注分组统计库存汇总
DROP TABLE IF EXISTS #stk01;
SELECT 
    备注,                      -- 备注（商品分类标识）
    门店编码,                   -- 门店编码
    SUM(库存数量) AS 库存数量,    -- 汇总库存数量
    SUM(库存金额) AS 库存金额     -- 汇总库存金额
INTO #stk01 
FROM #stk2
GROUP BY 门店编码, 备注;

-- 14. 获取有效门店清单
DROP TABLE IF EXISTS #stores;
SELECT 
    syb AS 事业部,               -- 所属事业部
    kfq AS 经营区,               -- 所属经营区
    mentor AS 区长,              -- 区长信息
    manager AS 指导员,           -- 指导员信息
    code AS 门店编码,             -- 门店编码
    [name] AS 门店名称,           -- 门店名称
    shoptype AS 门店类型          -- 门店类型
INTO #stores 
FROM odsdbfq_basic.dbo.store WITH (NOLOCK)
WHERE stat = '有效'             -- 仅包含有效门店
    AND companycode = 'hn';     -- 筛选公司

-- 15. 匹配门店数据与备注信息（笛卡尔积，为每个门店生成所有备注类型的记录）
DROP TABLE IF EXISTS #store2;
SELECT 
    b.remark AS 备注,            -- 备注（商品分类标识）
    a.*                         -- 门店基础数据
INTO #store2 
FROM #stores a
CROSS JOIN (SELECT DISTINCT remark FROM #ddplist WHERE remark IS NOT NULL) b;  -- 获取所有唯一的备注值

-- 16. 更新门店事业部（根据特定规则）
UPDATE #store2
SET 事业部 = '零食事业部'           -- 设置为零食事业部
WHERE 门店编码 IN (
    SELECT DISTINCT 编码            -- 获取零食事业部的门店编码
    FROM odsdbfqbi.dbo.storeinf
    WHERE 事业部 = '零食事业部'
);

-- 17. 输出最终分析结果
SELECT 
    a.事业部,                       -- 所属事业部
    a.经营区,                       -- 所属经营区
    a.区长,                         -- 区长信息
    a.指导员,                       -- 指导员信息
    a.门店编码,                     -- 门店编码
    a.门店名称,                     -- 门店名称
    a.门店类型,                     -- 门店类型
    a.备注 AS 商品,                 -- 商品分类标识
    ISNULL(b.销售数量, 0) AS 销售数量, -- 销售数量（空值处理为0）
    ISNULL(b.销售金额, 0) AS 销售金额, -- 销售金额（空值处理为0）
    ISNULL(c.库存数量, 0) AS 库存数量, -- 库存数量（空值处理为0）
    ISNULL(c.库存金额, 0) AS 库存金额, -- 库存金额（空值处理为0）
    -- 计算周转天数（避免除零错误）
    CASE 
        WHEN ISNULL(b.销售金额, 0) = 0 THEN NULL 
        ELSE ROUND(ISNULL(c.库存金额, 0) / (ISNULL(b.销售金额, 0) / NULLIF(DATEDIFF(DAY, @SDD, @EDD) + 1, 0)), 1) 
    END AS 周转天数,
    -- 判断是否开展农夫活动
    CASE 
        WHEN e.门店编码 IS NOT NULL AND a.备注 = '农夫' THEN 'Y' 
        ELSE 'N' 
    END AS 是否开活,
    -- 判断是否为零动销（无销售）
    CASE 
        WHEN ISNULL(b.销售金额, 0) <= 0 THEN 1 
        ELSE 0 
    END AS 零动销,
    -- 判断是否为有库存零动销（有库存但无销售）
    CASE 
        WHEN ISNULL(b.销售金额, 0) <= 0 AND ISNULL(c.库存金额, 0) > 0 THEN 1 
        ELSE 0 
    END AS 有库存零动销,
    -- 判断是否为无库存
    CASE 
        WHEN ISNULL(c.库存金额, 0) <= 0 THEN 1 
        ELSE 0 
    END AS 无库存,
    -- 新增：库销比（库存金额/销售金额）
    CASE 
        WHEN ISNULL(b.销售金额, 0) = 0 THEN NULL 
        ELSE ROUND(ISNULL(c.库存金额, 0) / ISNULL(b.销售金额, 0), 2) 
    END AS 库销比,
    -- 新增：判断库存健康度
    CASE 
        WHEN ISNULL(b.销售金额, 0) = 0 AND ISNULL(c.库存金额, 0) > 0 THEN '不健康'
        WHEN ISNULL(c.库存金额, 0) = 0 AND ISNULL(b.销售金额, 0) > 0 THEN '需备货'
        WHEN ISNULL(c.库存金额, 0) > 0 AND ISNULL(b.销售金额, 0) > 0 THEN '健康'
        ELSE '待评估'
    END AS 库存健康度
FROM #store2 a
LEFT JOIN #sale01 b ON a.门店编码 = b.门店编码 AND a.备注 = b.备注
LEFT JOIN #stk01 c ON a.门店编码 = c.门店编码 AND a.备注 = c.备注
LEFT JOIN (
    SELECT DISTINCT 门店编码, 事业部 
    FROM #sales0705 
    WHERE 销售金额 > 0
) e ON a.门店编码 = e.门店编码
ORDER BY a.事业部, a.经营区, 商品;

-- 18. 增强版报表：按事业部和商品统计汇总（新增）
SELECT 
    a.事业部,                              -- 所属事业部
    a.备注 AS 商品,                        -- 商品分类标识
    COUNT(DISTINCT a.门店编码) AS 总门店数,  -- 门店总数
    COUNT(DISTINCT CASE WHEN ISNULL(b.销售金额, 0) > 0 THEN a.门店编码 END) AS 有销售门店数,
    COUNT(DISTINCT CASE WHEN ISNULL(c.库存金额, 0) > 0 THEN a.门店编码 END) AS 有库存门店数,
    COUNT(DISTINCT CASE WHEN ISNULL(b.销售金额, 0) <= 0 AND ISNULL(c.库存金额, 0) > 0 THEN a.门店编码 END) AS 有库存零动销门店数,
    -- 计算门店覆盖率
    CAST(COUNT(DISTINCT CASE WHEN ISNULL(b.销售金额, 0) > 0 THEN a.门店编码 END) * 100.0 / 
         NULLIF(COUNT(DISTINCT a.门店编码), 0) AS DECIMAL(10,2)) AS 动销覆盖率,
    -- 计算销售汇总信息
    SUM(ISNULL(b.销售数量, 0)) AS 总销售数量,
    SUM(ISNULL(b.销售金额, 0)) AS 总销售金额,
    -- 计算库存汇总信息
    SUM(ISNULL(c.库存数量, 0)) AS 总库存数量,
    SUM(ISNULL(c.库存金额, 0)) AS 总库存金额,
    -- 计算平均周转天数
    CASE 
        WHEN SUM(ISNULL(b.销售金额, 0)) = 0 THEN NULL 
        ELSE ROUND(SUM(ISNULL(c.库存金额, 0)) / (SUM(ISNULL(b.销售金额, 0)) / NULLIF(DATEDIFF(DAY, @SDD, @EDD) + 1, 0)), 1) 
    END AS 平均周转天数,
    -- 计算有销售门店的店均销售额
    CASE 
        WHEN COUNT(DISTINCT CASE WHEN ISNULL(b.销售金额, 0) > 0 THEN a.门店编码 END) = 0 THEN NULL
        ELSE ROUND(SUM(ISNULL(b.销售金额, 0)) / COUNT(DISTINCT CASE WHEN ISNULL(b.销售金额, 0) > 0 THEN a.门店编码 END), 2)
    END AS 店均销售额
FROM #store2 a
LEFT JOIN #sale01 b ON a.门店编码 = b.门店编码 AND a.备注 = b.备注
LEFT JOIN #stk01 c ON a.门店编码 = c.门店编码 AND a.备注 = c.备注
GROUP BY a.事业部, a.备注
ORDER BY a.事业部, 总销售金额 DESC;

-- 19. 清理临时表（提高性能）
DROP TABLE IF EXISTS #moutdrpt;
DROP TABLE IF EXISTS #ddplist;
DROP TABLE IF EXISTS #sale_data1;
DROP TABLE IF EXISTS #sale_data11;
DROP TABLE IF EXISTS #sales0705;
DROP TABLE IF EXISTS #sale_data2;
DROP TABLE IF EXISTS #stk;
DROP TABLE IF EXISTS #stk2;
DROP TABLE IF EXISTS #sale01;
DROP TABLE IF EXISTS #stk01;
DROP TABLE IF EXISTS #stores;
DROP TABLE IF EXISTS #store2;

/*
 * 代码优化说明：
 * 1. 添加了详细的文件头注释，说明脚本功能和目的
 * 2. 使用参数化设计，使日期范围和大单品期间代码可配置
 * 3. 添加了错误处理机制，优化循环逻辑的稳定性
 * 4. 修复了goodsz表和store表的WITH (NOLOCK)语法错误
 * 5. 添加了更详细的中文注释，解释每个字段的含义和计算逻辑
 * 6. 新增周转天数计算，提供更有价值的业务指标
 * 7. 新增库销比和库存健康度指标，便于评估库存合理性
 * 8. 新增按事业部和商品的汇总分析报表，提供更高层面的数据视角
 * 9. 优化了CROSS JOIN查询，确保只包含有效的备注值
 * 10. 添加了临时表清理代码，优化资源使用
 * 11. 优化了数据排序逻辑，提高结果可读性
 */
