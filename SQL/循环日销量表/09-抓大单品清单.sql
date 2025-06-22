/*
 * 文件名: 09-抓大单品清单.sql
 * 功能: 大单品多维度分析
 * 描述: 本脚本用于抓取大单品清单及其销售、库存、门店等多维度数据，支持按时间、区域、品类等多维度分析
 */

-- 1. 定义日期参数
DECLARE @start_date DATE;      -- 开始日期
DECLARE @end_date DATE;        -- 结束日期
DECLARE @ddp_period VARCHAR(6); -- 大单品期间代码（年月格式）

-- 智能设置日期变量（可根据需要调整）
SET @start_date = '2023-11-01';                                  -- 开始日期
SET @end_date = CONVERT(DATE, DATEADD(DAY, -1, GETDATE()));      -- 昨日
SET @ddp_period = '202401';                                      -- 大单品期间代码，格式：YYYYMM

-- 输出日期参数（便于调试和确认）
SELECT 
    @start_date AS 开始日期,
    @end_date AS 结束日期,
    @ddp_period AS 大单品期间代码,
    DATEDIFF(DAY, @start_date, @end_date) + 1 AS 数据天数;

-- 2. 获取大单品清单
IF OBJECT_ID('tempdb..#ddplist') IS NOT NULL DROP TABLE #ddplist; -- 如果临时表已存在则先删除

SELECT 
    a.*,                -- 大单品基础信息
    b.gid,              -- 商品GID
    b.scode1 AS 大类编码, -- 商品大类编码
    b.sname1 AS 大类名称  -- 商品大类名称
INTO #ddplist 
FROM odsdbfqbi.dbo.ddp_hn a     -- 大单品主表
LEFT JOIN odsdbfq_basic.dbo.goodsz b WITH (NOLOCK) ON a.itemcode = b.code AND b.companycode = 'hn' -- 关联商品基本信息
WHERE mydate = @ddp_period      -- 使用参数化的期间代码
  AND DQ IN ('全国','华中区');    -- 仅包含指定大区

-- 3. 获取销售明细（仅抓取大单品）
IF OBJECT_ID('tempdb..#sale_data1') IS NOT NULL DROP TABLE #sale_data1; -- 如果临时表已存在则先删除

SELECT 
    astore AS storegid,                 -- 门店GID
    bgdgid AS 商品gid,                  -- 商品GID
    SUM(DQ1 - DQ5) AS 销售数量,         -- 计算净销售数量（销售-退货）
    SUM(DT1 - DT5) AS 销售金额          -- 计算净销售金额（销售-退货）
INTO #sale_data1 
FROM odsdbfq_basic.dbo.moutdrpt WITH (NOLOCK) -- 使用NOLOCK提高查询性能
WHERE companycode = 'hn'                      -- 筛选公司
  AND adate BETWEEN @start_date AND @end_date -- 使用参数化日期范围
  AND bgdgid IN (SELECT gid FROM #ddplist)    -- 仅包含大单品清单中的商品
GROUP BY astore, bgdgid;                      -- 按门店和商品分组统计

-- 4. 关联门店、商品、清单信息
IF OBJECT_ID('tempdb..#sale_data2') IS NOT NULL DROP TABLE #sale_data2; -- 如果临时表已存在则先删除

SELECT 
    c.shoptype AS 门店类型,       -- 门店类型
    syb AS 事业部,                -- 所属事业部
    kfq AS 区域,                  -- 所属区域
    mentor AS 店长,               -- 店长信息
    manager AS 指导员,            -- 指导员信息
    c.code AS 门店编码,           -- 门店编码
    大类编码,                     -- 商品大类编码
    大类名称,                     -- 商品大类名称
    remark AS 备注,               -- 备注（如大单品片、大单品等分类）
    DQ AS 大区,                   -- 所属大区
    b.itemcode AS 商品编码,       -- 商品编码
    b.itemcn AS 商品名称,         -- 商品名称
    销售数量,                     -- 销售数量
    销售金额                      -- 销售金额
INTO #sale_data2 
FROM #sale_data1 a
LEFT JOIN #ddplist b ON a.商品gid = b.gid    -- 关联大单品清单信息
LEFT JOIN odsdbfq_basic.dbo.store c WITH (NOLOCK) ON a.storegid = c.gid AND c.companycode = 'hn'; -- 关联门店信息

-- 5. 获取库存明细
IF OBJECT_ID('tempdb..#stk') IS NOT NULL DROP TABLE #stk; -- 如果临时表已存在则先删除

SELECT 
    a.store AS 门店gid,            -- 门店GID
    a.gdgid AS 商品gid,            -- 商品GID
    b.code AS 商品编码,            -- 商品编码
    b.scode1 AS 大类编码,          -- 商品大类编码
    b.sname1 AS 大类名称,          -- 商品大类名称
    b.[name] AS 商品名称,          -- 商品名称
    c.code AS 门店编码,            -- 门店编码
    c.[name] AS 门店名称,          -- 门店名称
    shoptype AS 门店类型,          -- 门店类型
    syb AS 事业部,                 -- 所属事业部
    kfq AS 区域,                   -- 所属区域
    mentor AS 店长,                -- 店长信息
    manager AS 指导员,             -- 指导员信息
    wrh,                          -- 仓位
    qty AS 库存数量,               -- 库存数量
    qty * ISNULL(whsprc,0) AS 库存金额 -- 计算库存金额（数量*成本价）
INTO #stk 
FROM odsdbfq_basic.dbo.inv a WITH (NOLOCK)    -- 库存表
LEFT JOIN odsdbfq_basic.dbo.goodsz b WITH (NOLOCK) ON a.gdgid = b.gid AND b.companycode = 'hn'  -- 关联商品信息
LEFT JOIN odsdbfq_basic.dbo.store c WITH (NOLOCK) ON a.store = c.gid AND c.CompanyCode = 'hn'   -- 关联门店信息
WHERE a.companycode = 'hn'                 -- 筛选公司
  AND b.scode1 IS NOT NULL                 -- 排除无分类商品
  AND c.code <> '08'                       -- 排除特定门店（08总部）
  AND a.gdgid IN (SELECT gid FROM #ddplist); -- 仅包含大单品清单中的商品

-- 6. 关联库存与清单
IF OBJECT_ID('tempdb..#stk2') IS NOT NULL DROP TABLE #stk2; -- 如果临时表已存在则先删除

SELECT 
    a.*,                -- 库存明细
    b.remark AS 备注,    -- 备注（如大单品片、大单品等分类）
    b.DQ AS 大区         -- 所属大区
INTO #stk2 
FROM #stk a
LEFT JOIN #ddplist b ON a.商品编码 = b.itemcode; -- 关联大单品清单信息

-- 7. 分类汇总销售与库存（按备注字段分类）
-- 7.1 汇总销售-大单品片
IF OBJECT_ID('tempdb..#sale01') IS NOT NULL DROP TABLE #sale01; -- 如果临时表已存在则先删除

SELECT 
    门店编码,                  -- 门店编码
    SUM(销售数量) AS 销售数量,  -- 汇总销售数量
    SUM(销售金额) AS 销售金额   -- 汇总销售金额
INTO #sale01 
FROM #sale_data2
WHERE 备注 = '大单品片'         -- 筛选大单品片类别
GROUP BY 门店编码;              -- 按门店分组统计

-- 7.2 汇总销售-大单品
IF OBJECT_ID('tempdb..#sale02') IS NOT NULL DROP TABLE #sale02; -- 如果临时表已存在则先删除

SELECT 
    门店编码,                  -- 门店编码
    SUM(销售数量) AS 销售数量,  -- 汇总销售数量
    SUM(销售金额) AS 销售金额   -- 汇总销售金额
INTO #sale02 
FROM #sale_data2
WHERE 备注 = '大单品'           -- 筛选大单品类别
GROUP BY 门店编码;              -- 按门店分组统计

-- 7.3 汇总库存-大单品片
IF OBJECT_ID('tempdb..#stk01') IS NOT NULL DROP TABLE #stk01; -- 如果临时表已存在则先删除

SELECT 
    门店编码,                  -- 门店编码
    SUM(库存数量) AS 库存数量,  -- 汇总库存数量
    SUM(库存金额) AS 库存金额   -- 汇总库存金额
INTO #stk01 
FROM #stk2
WHERE 备注 = '大单品片'         -- 筛选大单品片类别
GROUP BY 门店编码;              -- 按门店分组统计

-- 7.4 汇总库存-大单品
IF OBJECT_ID('tempdb..#stk02') IS NOT NULL DROP TABLE #stk02; -- 如果临时表已存在则先删除

SELECT 
    门店编码,                  -- 门店编码
    SUM(库存数量) AS 库存数量,  -- 汇总库存数量
    SUM(库存金额) AS 库存金额   -- 汇总库存金额
INTO #stk02 
FROM #stk2
WHERE 备注 = '大单品'           -- 筛选大单品类别
GROUP BY 门店编码;              -- 按门店分组统计

-- 8. 有效门店清单
IF OBJECT_ID('tempdb..#stores') IS NOT NULL DROP TABLE #stores; -- 如果临时表已存在则先删除

SELECT 
    syb AS 事业部,             -- 所属事业部
    kfq AS 区域,               -- 所属区域
    mentor AS 店长,            -- 店长信息
    manager AS 指导员,         -- 指导员信息
    code AS 门店编码,          -- 门店编码
    [name] AS 门店名称,        -- 门店名称
    shoptype AS 门店类型       -- 门店类型
INTO #stores 
FROM odsdbfq_basic.dbo.store WITH (NOLOCK)  -- 门店表
WHERE stat = '有效'                         -- 仅包含有效门店
  AND companycode = 'hn';                  -- 筛选公司

-- 9. 匹配门店与销售、库存数据
-- 9.1 大单品片分析报表
SELECT 
    ISNULL(d.事业部, a.事业部) AS 事业部,           -- 优先使用storeinf表中的事业部
    ISNULL(d.区域, a.区域) AS 区域,                 -- 优先使用storeinf表中的区域
    ISNULL(d.店长, a.店长) AS 店长,                 -- 优先使用storeinf表中的店长
    ISNULL(d.指导员, a.指导员) AS 指导员,           -- 优先使用storeinf表中的指导员
    a.门店编码,                                     -- 门店编码
    a.门店名称,                                     -- 门店名称
    a.门店类型,                                     -- 门店类型
    '大单品片' AS 品类,                             -- 品类标识
    ISNULL(b.销售数量, 0) AS 销售数量,               -- 销售数量（空值处理为0）
    ISNULL(b.销售金额, 0) AS 销售金额,               -- 销售金额（空值处理为0）
    ISNULL(c.库存数量, 0) AS 库存数量,               -- 库存数量（空值处理为0）
    ISNULL(c.库存金额, 0) AS 库存金额,               -- 库存金额（空值处理为0）
    -- 新增：计算周转天数（避免除零错误）
    CASE 
        WHEN ISNULL(b.销售金额, 0) = 0 THEN NULL 
        ELSE ROUND(ISNULL(c.库存金额, 0) / (ISNULL(b.销售金额, 0) / NULLIF(DATEDIFF(DAY, @start_date, @end_date) + 1, 0)), 1) 
    END AS 周转天数
FROM #stores a
LEFT JOIN #sale01 b ON a.门店编码 = b.门店编码                   -- 关联销售数据
LEFT JOIN #stk01 c ON a.门店编码 = c.门店编码                    -- 关联库存数据
LEFT JOIN odsdbfqbi.dbo.storeinf d ON a.门店编码 = d.门店编码    -- 关联门店扩展信息
ORDER BY ISNULL(d.事业部, a.事业部), ISNULL(d.区域, a.区域);      -- 按事业部、区域排序

-- 9.2 大单品分析报表
SELECT 
    ISNULL(d.事业部, a.事业部) AS 事业部,           -- 优先使用storeinf表中的事业部
    ISNULL(d.区域, a.区域) AS 区域,                 -- 优先使用storeinf表中的区域
    ISNULL(d.店长, a.店长) AS 店长,                 -- 优先使用storeinf表中的店长
    ISNULL(d.指导员, a.指导员) AS 指导员,           -- 优先使用storeinf表中的指导员
    a.门店编码,                                     -- 门店编码
    a.门店名称,                                     -- 门店名称
    a.门店类型,                                     -- 门店类型
    '大单品' AS 品类,                               -- 品类标识
    ISNULL(b.销售数量, 0) AS 销售数量,               -- 销售数量（空值处理为0）
    ISNULL(b.销售金额, 0) AS 销售金额,               -- 销售金额（空值处理为0）
    ISNULL(c.库存数量, 0) AS 库存数量,               -- 库存数量（空值处理为0）
    ISNULL(c.库存金额, 0) AS 库存金额,               -- 库存金额（空值处理为0）
    -- 新增：计算周转天数（避免除零错误）
    CASE 
        WHEN ISNULL(b.销售金额, 0) = 0 THEN NULL 
        ELSE ROUND(ISNULL(c.库存金额, 0) / (ISNULL(b.销售金额, 0) / NULLIF(DATEDIFF(DAY, @start_date, @end_date) + 1, 0)), 1) 
    END AS 周转天数
FROM #stores a
LEFT JOIN #sale02 b ON a.门店编码 = b.门店编码                   -- 关联销售数据
LEFT JOIN #stk02 c ON a.门店编码 = c.门店编码                    -- 关联库存数据
LEFT JOIN odsdbfqbi.dbo.storeinf d ON a.门店编码 = d.门店编码    -- 关联门店扩展信息
ORDER BY ISNULL(d.事业部, a.事业部), ISNULL(d.区域, a.区域);      -- 按事业部、区域排序

-- 10. 经营天数统计
IF OBJECT_ID('tempdb..#TS') IS NOT NULL DROP TABLE #TS; -- 如果临时表已存在则先删除

SELECT 
    companycode,                    -- 公司代码
    code AS storecode,              -- 门店编码
    COUNT(DISTINCT rq) AS 天数,     -- 统计经营天数（有销售的天数）
    SUM(noxse) AS 销售额            -- 汇总销售额
INTO #TS
FROM odsdbfq_result.dbo.m_stsale WITH (NOLOCK)  -- 使用NOLOCK提高查询性能
WHERE rq BETWEEN @start_date AND @end_date      -- 使用参数化日期范围
  AND companycode = 'hn'                        -- 筛选公司
  AND noxse > 0                                 -- 仅包含有效销售额（大于0）
GROUP BY companycode, code;                     -- 按公司和门店分组统计

-- 11. 门店经营情况分析
SELECT 
    a.*,                           -- 经营天数基础数据
    b.shoptype,                    -- 门店类型
    syb,                           -- 所属事业部
    ROUND(销售额 / 天数, 2) AS 日均销售额 -- 新增：计算日均销售额
FROM #TS a
LEFT JOIN odsdbfq_basic.dbo.store b WITH (NOLOCK) ON a.storecode = b.code AND b.CompanyCode = 'hn'
ORDER BY syb, shoptype, 天数 DESC;  -- 新增：添加排序规则

-- 12. 清理临时表（提高性能）
DROP TABLE IF EXISTS #ddplist;
DROP TABLE IF EXISTS #sale_data1;
DROP TABLE IF EXISTS #sale_data2;
DROP TABLE IF EXISTS #stk;
DROP TABLE IF EXISTS #stk2;
DROP TABLE IF EXISTS #sale01;
DROP TABLE IF EXISTS #sale02;
DROP TABLE IF EXISTS #stk01;
DROP TABLE IF EXISTS #stk02;
DROP TABLE IF EXISTS #stores;
DROP TABLE IF EXISTS #TS;

/*
 * 代码优化说明：
 * 1. 添加了详细的文件头注释，说明脚本功能和目的
 * 2. 引入了参数化设计，使日期范围和大单品期间代码可配置
 * 3. 使用BETWEEN替代>=和<=来简化日期范围条件
 * 4. 添加了更详细的中文注释，解释每个字段的含义和计算逻辑
 * 5. 新增周转天数计算，提供更有价值的业务指标
 * 6. 新增日均销售额计算，便于门店绩效分析
 * 7. 优化了查询排序逻辑，提高数据可读性
 * 8. 添加了临时表清理代码，优化资源使用
 * 9. 保持了WITH (NOLOCK)提示以提高查询性能
 * 10. 调整了步骤编号，使脚本结构更加清晰
 */