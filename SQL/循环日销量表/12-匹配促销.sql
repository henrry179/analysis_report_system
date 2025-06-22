/*
 * 文件名: 12-匹配促销.sql
 * 功能: 促销数据匹配与分析
 * 描述: 本脚本用于匹配促销数据并进行多维度分析，支持按日期、门店、商品等维度进行统计，结果存入匹配表
 */

-- 1. 定义日期参数
DECLARE @start_date DATE;      -- 开始日期
DECLARE @end_date DATE;        -- 结束日期
DECLARE @ddp_period VARCHAR(6); -- 大单品期间代码（年月格式）
DECLARE @middate VARCHAR(20);  -- 月中日期（用于上下半月划分）

-- 智能设置日期变量（可根据需要调整）
SET @start_date = DATEADD(DAY, -30, GETDATE());      -- 默认查询最近30天数据
SET @end_date = DATEADD(DAY, -1, GETDATE());         -- 截止到昨天
SET @ddp_period = '202401';                          -- 大单品期间代码

-- 获取促销明细表中最早的日期，用于上下半月划分
SET @middate = (SELECT MIN(mydate) FROM odsdbfqbi.dbo.hn_cx_detail);
PRINT '月中划分日期: ' + CONVERT(VARCHAR(20), DATEADD(DAY, 16, EOMONTH(@middate, -1)), 112);

-- 输出日期参数（便于调试和确认）
SELECT 
    @start_date AS 开始日期,
    @end_date AS 结束日期,
    @ddp_period AS 大单品期间代码,
    @middate AS 促销开始日期,
    CONVERT(VARCHAR(20), DATEADD(DAY, 16, EOMONTH(@middate, -1)), 112) AS 月中划分日期;

-- 2. 创建临时表存储促销数据（第一部分：基础促销数据）
DROP TABLE IF EXISTS #promotion_data;
SELECT 
    a.adate AS 日期,                     -- 促销日期
    a.astore AS 门店gid,                 -- 门店ID
    a.bgdgid AS 商品gid,                 -- 商品ID
    b.code AS 商品编码,                   -- 商品编码
    b.[name] AS 商品名称,                 -- 商品名称
    b.scode1 AS 大类,                     -- 商品大类编码
    b.sname1 AS 大类名,                   -- 商品大类名称
    c.code AS 门店编码,                   -- 门店编码
    c.[name] AS 门店名称,                 -- 门店名称
    c.shoptype AS 门店类型,               -- 门店类型
    c.syb AS 事业部,                      -- 所属事业部
    c.kfq AS 经营区,                      -- 所属经营区
    c.mentor AS 区长,                     -- 区长信息
    c.manager AS 指导员,                  -- 指导员信息
    a.dq1 AS 促销前数量,                  -- 促销前销售数量
    a.dq5 AS 促销后数量,                  -- 促销后销售数量
    a.dt1 AS 促销前金额,                  -- 促销前销售金额
    a.dt5 AS 促销后金额,                  -- 促销后销售金额
    a.dq1 - a.dq5 AS 促销数量,            -- 计算促销净数量
    a.dt1 - a.dt5 AS 促销金额,            -- 计算促销净金额
    -- 计算单品促销折扣率（避免除零错误）
    CASE 
        WHEN a.dt1 = 0 OR a.dq1 = 0 THEN NULL
        WHEN (a.dt5 / NULLIF(a.dq5, 0)) = 0 THEN NULL
        ELSE ROUND(100 - ((a.dt5 / NULLIF(a.dq5, 0)) / (a.dt1 / NULLIF(a.dq1, 0)) * 100), 2)
    END AS 折扣率
INTO #promotion_data
FROM odsdbfqbi.dbo.hn_cx_promotion a
LEFT JOIN odsdbfq_basic.dbo.goodsz b WITH (NOLOCK) ON a.bgdgid = b.gid 
    AND b.companycode = 'hn'
LEFT JOIN odsdbfq_basic.dbo.store c WITH (NOLOCK) ON a.astore = c.gid 
    AND c.companycode = 'hn'
WHERE a.companycode = 'hn'
  AND a.adate BETWEEN @start_date AND @end_date;  -- 使用参数化日期范围

-- 3. 获取大单品清单（第二部分：大单品数据）
DROP TABLE IF EXISTS #ddplist;
SELECT 
    a.*,                        -- 大单品基础信息
    b.gid,                      -- 商品GID
    scode1 AS 大类,             -- 商品大类编码
    sname1 AS 大类名             -- 商品大类名称
INTO #ddplist 
FROM odsdbfqbi.dbo.ddp_hn a
LEFT JOIN odsdbfq_basic.dbo.goodsz b WITH (NOLOCK) ON a.itemcode = b.code 
    AND b.companycode = 'hn'
WHERE mydate = @ddp_period                  -- 使用参数化的期间代码
  AND DQ IN ('全国', '上半月', '下半月');    -- 筛选范围

-- 4. 统计下半月促销数据
DROP TABLE IF EXISTS #cx_xia;
SELECT 
    '下半月' AS 区域,            -- 下半月标识
    storecode,                 -- 门店编码
    gid,                       -- 商品ID
    itemcode,                  -- 商品编码
    SUM(realamt) AS proamt     -- 促销金额
INTO #cx_xia
FROM odsdbfqbi.dbo.hn_cx_detail
WHERE mydate >= CONVERT(VARCHAR(20), DATEADD(DAY, 16, EOMONTH(@middate, -1)), 112)  -- 16号及以后为下半月
GROUP BY storecode, gid, itemcode;

-- 5. 统计上半月促销数据
DROP TABLE IF EXISTS #cx_shang;
SELECT 
    '上半月' AS 区域,            -- 上半月标识
    storecode,                 -- 门店编码
    gid,                       -- 商品ID
    itemcode,                  -- 商品编码
    SUM(realamt) AS proamt     -- 促销金额
INTO #cx_shang
FROM odsdbfqbi.dbo.hn_cx_detail
WHERE mydate < CONVERT(VARCHAR(20), DATEADD(DAY, 16, EOMONTH(@middate, -1)), 112)  -- 16号以前为上半月
GROUP BY storecode, gid, itemcode;

-- 6. 统计全月促销数据
DROP TABLE IF EXISTS #cx_quan;
SELECT 
    '全国' AS 区域,              -- 全国标识
    storecode,                 -- 门店编码
    gid,                       -- 商品ID
    itemcode,                  -- 商品编码
    SUM(realamt) AS proamt     -- 促销金额
INTO #cx_quan
FROM odsdbfqbi.dbo.hn_cx_detail
GROUP BY storecode, gid, itemcode;

-- 7. 合并所有促销数据
DROP TABLE IF EXISTS #cx_tt;
SELECT * INTO #cx_tt FROM #cx_xia
UNION ALL
SELECT * FROM #cx_shang
UNION ALL
SELECT * FROM #cx_quan;

-- 8. 获取有效门店信息
DROP TABLE IF EXISTS #store;
SELECT 
    code,                      -- 门店编码
    syb                        -- 事业部
INTO #store 
FROM odsdbfq_basic.dbo.store WITH (NOLOCK)
WHERE stat = '有效'             -- 仅包含有效门店
  AND companycode = 'hn';      -- 筛选公司

-- 9. 更新零食事业部门店标识
UPDATE #store
SET syb = '零食事业部'          -- 设置为零食事业部
WHERE code IN (
    SELECT DISTINCT 编码        -- 获取零食事业部的门店编码
    FROM odsdbfqbi.dbo.storeinf
    WHERE 事业部 = '零食事业部'
);

-- 10. 插入匹配后的促销数据到正式表
PRINT '开始插入匹配数据到正式表...';

BEGIN TRY
    BEGIN TRANSACTION;
    
    INSERT INTO odsdbfqbi.dbo.hn_cx_matched
    SELECT 
        日期,                      -- 促销日期
        门店gid,                   -- 门店ID
        商品gid,                   -- 商品ID
        商品编码,                   -- 商品编码
        商品名称,                   -- 商品名称
        大类,                      -- 商品大类编码
        大类名,                     -- 商品大类名称
        门店编码,                   -- 门店编码
        门店名称,                   -- 门店名称
        门店类型,                   -- 门店类型
        事业部,                     -- 所属事业部
        经营区,                     -- 所属经营区
        区长,                      -- 区长信息
        指导员,                     -- 指导员信息
        促销前数量,                  -- 促销前销售数量
        促销后数量,                  -- 促销后销售数量
        促销前金额,                  -- 促销前销售金额
        促销后金额,                  -- 促销后销售金额
        促销数量,                   -- 计算促销净数量
        促销金额,                   -- 计算促销净金额
        GETDATE() AS 匹配时间       -- 当前时间为匹配时间
    FROM #promotion_data
    WHERE 促销数量 > 0              -- 仅包含有有效促销的数据
        OR 促销金额 > 0;
    
    PRINT '匹配数据插入成功，共插入 ' + 
          CAST(@@ROWCOUNT AS VARCHAR(10)) + ' 条记录';
    
    COMMIT TRANSACTION;
END TRY
BEGIN CATCH
    IF @@TRANCOUNT > 0
        ROLLBACK TRANSACTION;
    
    PRINT '匹配数据插入失败: ' + ERROR_MESSAGE();
END CATCH

-- 11. 按门店统计促销效果
SELECT 
    事业部 AS '事业部',              -- 所属事业部
    经营区 AS '经营区',              -- 所属经营区
    区长 AS '区长',                  -- 区长信息
    指导员 AS '指导员',              -- 指导员信息
    门店编码 AS '门店编码',           -- 门店编码
    门店名称 AS '门店名称',           -- 门店名称
    门店类型 AS '门店类型',           -- 门店类型
    COUNT(DISTINCT 日期) AS '促销天数',              -- 统计促销活动天数
    COUNT(DISTINCT 商品编码) AS '促销商品数',         -- 统计促销商品数量
    SUM(促销数量) AS '促销总数量',                    -- 汇总促销销售数量
    SUM(促销金额) AS '促销总金额',                    -- 汇总促销销售金额
    -- 新增：计算平均每天促销金额
    ROUND(SUM(促销金额) / NULLIF(COUNT(DISTINCT 日期), 0), 2) AS '日均促销金额',
    -- 新增：计算平均每个商品促销金额
    ROUND(SUM(促销金额) / NULLIF(COUNT(DISTINCT 商品编码), 0), 2) AS '单品平均促销金额',
    -- 新增：计算平均折扣率
    AVG(折扣率) AS '平均折扣率'
FROM #promotion_data
WHERE 促销数量 > 0                  -- 仅包含有有效促销的数据
    OR 促销金额 > 0
GROUP BY 
    事业部,
    经营区,
    区长,
    指导员,
    门店编码,
    门店名称,
    门店类型
ORDER BY 
    事业部,
    经营区,
    '促销总金额' DESC;               -- 按事业部、经营区和促销总金额排序

-- 12. 按区域、备注统计促销效果
SELECT 
    syb AS '事业部',                -- 所属事业部
    storecode AS '门店编码',         -- 门店编码
    remark AS '备注',               -- 商品备注
    SUM(proamt) AS '促销金额',       -- 汇总促销金额
    区域 AS '区域'                   -- 区域划分（上半月/下半月/全国）
FROM (
    SELECT 
        a.*,                       -- 促销基础数据
        b.itemcn,                  -- 商品名称
        b.remark,                  -- 商品备注
        syb                        -- 事业部
    FROM #cx_tt a
    LEFT JOIN #ddplist b ON a.itemcode = b.itemcode AND a.区域 = b.DQ
    LEFT JOIN #store c ON a.storecode = c.code
    WHERE b.remark IS NOT NULL     -- 仅包含有备注的记录
) a
WHERE syb IS NOT NULL              -- 仅包含有事业部的记录
GROUP BY syb, storecode, remark, 区域
ORDER BY syb, storecode, 区域;      -- 按事业部、门店编码和区域排序

-- 13. 统计各备注类型在不同区域的促销效果（新增）
SELECT 
    remark AS '备注',               -- 商品备注
    区域 AS '区域',                  -- 区域划分（上半月/下半月/全国）
    COUNT(DISTINCT storecode) AS '门店数',           -- 统计门店数量
    COUNT(DISTINCT itemcode) AS '商品数',            -- 统计商品数量
    SUM(proamt) AS '促销金额',                       -- 汇总促销金额
    -- 新增：计算平均每店促销金额
    ROUND(SUM(proamt) / NULLIF(COUNT(DISTINCT storecode), 0), 2) AS '店均促销金额',
    -- 新增：计算平均每个商品促销金额
    ROUND(SUM(proamt) / NULLIF(COUNT(DISTINCT itemcode), 0), 2) AS '单品促销金额'
FROM (
    SELECT 
        a.*,                       -- 促销基础数据
        b.itemcn,                  -- 商品名称
        b.remark,                  -- 商品备注
        syb                        -- 事业部
    FROM #cx_tt a
    LEFT JOIN #ddplist b ON a.itemcode = b.itemcode AND a.区域 = b.DQ
    LEFT JOIN #store c ON a.storecode = c.code
    WHERE b.remark IS NOT NULL     -- 仅包含有备注的记录
) a
WHERE syb IS NOT NULL              -- 仅包含有事业部的记录
GROUP BY remark, 区域
ORDER BY 区域, '促销金额' DESC;      -- 按区域和促销金额排序

-- 14. 清理临时表（提高性能）
DROP TABLE IF EXISTS #promotion_data;
DROP TABLE IF EXISTS #ddplist;
DROP TABLE IF EXISTS #cx_xia;
DROP TABLE IF EXISTS #cx_shang; 
DROP TABLE IF EXISTS #cx_quan;
DROP TABLE IF EXISTS #cx_tt;
DROP TABLE IF EXISTS #store;

/*
 * 代码优化说明：
 * 1. 添加了详细的文件头注释，说明脚本功能和目的
 * 2. 引入了参数化日期设计，便于灵活配置分析时间范围
 * 3. 修复了全部字符编码问题，确保所有中文字符正确显示
 * 4. 修复了goodsz表和store表的WITH (NOLOCK)语法错误
 * 5. 添加了更详细的中文注释，解释每个步骤和字段的含义
 * 6. 新增折扣率计算，提供促销效果分析
 * 7. 增加了错误处理机制，确保数据插入操作的可靠性
 * 8. 新增统计分析维度，按备注和区域交叉分析促销效果
 * 9. 优化了SQL结构，使代码更加清晰易读
 * 10. 添加了临时表清理代码，优化资源使用
 * 11. 添加了插入操作的提示信息，便于判断执行状态
 */