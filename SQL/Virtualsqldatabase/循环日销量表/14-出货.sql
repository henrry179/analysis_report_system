/*
 * 文件名: 14-出货.sql
 * 功能: 出货数据分析
 * 描述: 本脚本用于分析出货数据，支持按日期、门店、商品等多维度分析，并关联大单品清单进行专项分析
 */

-- 1. 定义日期参数
DECLARE @sdate DATE;         -- 开始日期
DECLARE @edate DATE;         -- 结束日期
DECLARE @report_date VARCHAR(8); -- 报表日期（格式：YYYYMMDD）
DECLARE @ddp_period VARCHAR(6);  -- 大单品期间代码（格式：YYYYMM）

-- 智能设置日期变量（可根据需要调整）
SET @sdate = '2024-01-01';                                -- 开始日期（2024年1月1日）
SET @edate = DATEADD(DAY, DATEDIFF(DAY, 0, GETDATE()-1), 0); -- 结束日期（昨天）
SET @report_date = '20240104';                            -- 报表日期（示例：2024年1月4日）
SET @ddp_period = '202401';                              -- 大单品期间代码（2024年1月）

-- 输出日期参数（便于调试和确认）
SELECT 
    @sdate AS 开始日期,
    @edate AS 结束日期,
    @report_date AS 报表日期,
    @ddp_period AS 大单品期间代码,
    DATEDIFF(DAY, @sdate, @edate) + 1 AS 分析天数;

-- 2. 创建临时表存储出货明细数据（第一部分：出货明细）
DROP TABLE IF EXISTS #DATA1;
SELECT 
    mydate,                  -- 出货日期
    storecode,               -- 门店编码
    itemcode,                -- 商品编码
    SUM(QTY) AS QTY,         -- 汇总出货数量
    SUM(REALAMT) AS REALAMT, -- 汇总出货金额
    SUM(FAVAMT) AS FAVAMT    -- 汇总优惠金额
INTO #DATA1
FROM odsdbfqbi.dbo.hn_cx_detail WITH (NOLOCK)
WHERE mydate = @report_date  -- 使用参数化的报表日期
GROUP BY mydate, storecode, itemcode;

-- 3. 插入出货数据到正式表
PRINT '开始插入出货数据到正式表...';

BEGIN TRY
    BEGIN TRANSACTION;
    
    -- 可选：先删除同一日期的历史数据，避免重复
    -- DELETE FROM odsdbfqbi.dbo.hn_cx_shipment WHERE mydate = @report_date;
    
    INSERT INTO odsdbfqbi.dbo.hn_cx_shipment
    SELECT 
        a.mydate,                  -- 出货日期
        a.storecode,               -- 门店编码
        a.itemcode,                -- 原始商品编码
        b.code AS itemcode_new,    -- 新商品编码（经过关联后的）
        QTY,                       -- 出货数量
        REALAMT,                   -- 出货金额
        FAVAMT                     -- 优惠金额
    FROM #DATA1 a
    LEFT JOIN odsdbfq_basic.dbo.goodsz b WITH (NOLOCK) ON a.itemcode = b.code 
        AND companycode = 'hn'
    WHERE mydate = @report_date;   -- 使用参数化的报表日期
    
    PRINT '出货数据插入成功，共插入 ' + 
          CAST(@@ROWCOUNT AS VARCHAR(10)) + ' 条记录';
    
    COMMIT TRANSACTION;
END TRY
BEGIN CATCH
    IF @@TRANCOUNT > 0
        ROLLBACK TRANSACTION;
    
    PRINT '出货数据插入失败: ' + ERROR_MESSAGE();
END CATCH

-- 4. 统计门店出货数据（第二部分：门店出货汇总）
DROP TABLE IF EXISTS #CH1;
SELECT 
    companycode,                  -- 公司代码
    astore AS storecode,          -- 门店编码
    bgdgid AS 商品gid,            -- 商品GID
    bcstgid AS 门店gid,           -- 门店GID
    SUM(dq4 - dq7) AS 出货数量,    -- 计算净出货数量
    SUM(dt4 - dt7) AS 出货金额,    -- 计算净出货金额
    SUM((dt4-dt7)-(di4-di7)) AS 毛利额 -- 计算毛利额
INTO #CH1
FROM odsdbfq_basic.dbo.outdrpt WITH (NOLOCK)
WHERE adate BETWEEN @sdate AND @edate  -- 使用参数化日期范围
  AND companycode = 'HN'
GROUP BY companycode, astore, bgdgid, bcstgid;

-- 5. 提取商品基础信息
DROP TABLE IF EXISTS #itm;
SELECT 
    gid,                  -- 商品GID
    code,                 -- 商品编码
    name,                 -- 商品名称
    scode1,               -- 商品大类编码
    sname1,               -- 商品大类名称
    scode2,               -- 商品中类编码
    sname2,               -- 商品中类名称
    scode3,               -- 商品小类编码
    sname3                -- 商品小类名称
INTO #itm 
FROM odsdbfq_basic.dbo.goodsz WITH (NOLOCK)
WHERE companycode = 'hn';

-- 6. 提取门店基础信息
DROP TABLE IF EXISTS #store;
SELECT 
    gid,                  -- 门店GID
    code,                 -- 门店编码
    name,                 -- 门店名称
    shoptype,             -- 门店类型
    syb,                  -- 事业部
    kfq                   -- 经营区
INTO #store 
FROM odsdbfq_basic.dbo.store WITH (NOLOCK)
WHERE companycode = 'hn' 
  AND daqu IS NOT NULL;   -- 仅包含有大区信息的门店

-- 7. 更新零食事业部门店标识
UPDATE #store
SET syb = '零食事业部'     -- 设置为零食事业部
WHERE code IN (
    SELECT DISTINCT 编码   -- 获取零食事业部的门店编码
    FROM odsdbfqbi.dbo.storeinf
    WHERE 事业部 = '零食事业部'
);

-- 8. 获取大单品清单
DROP TABLE IF EXISTS #ddplist;
SELECT 
    a.*,                   -- 大单品基础信息
    b.gid,                 -- 商品GID
    scode1 AS 大类编码,     -- 商品大类编码
    sname1 AS 大类名称      -- 商品大类名称
INTO #ddplist 
FROM odsdbfqbi.dbo.ddp_hn a
LEFT JOIN odsdbfq_basic.dbo.goodsz b WITH (NOLOCK) ON a.itemcode = b.code 
    AND b.companycode = 'hn'
WHERE mydate = @ddp_period  -- 使用参数化的期间代码
  AND DQ = '全国';          -- 仅包含全国范围的大单品

-- 9. 出货数据多维度分析
SELECT 
    b.shoptype AS 门店类型,     -- 门店类型
    syb AS 事业部,              -- 事业部
    kfq AS 经营区,              -- 经营区
    b.code AS 门店编码,         -- 门店编码
    b.name AS 门店名称,         -- 门店名称
    c.scode1 AS 大类编码,       -- 商品大类编码
    c.sname1 AS 大类名称,       -- 商品大类名称
    c.scode2 AS 中类编码,       -- 商品中类编码
    c.sname2 AS 中类名称,       -- 商品中类名称
    c.code AS 商品编码,         -- 商品编码
    c.name AS 商品名称,         -- 商品名称
    remark AS 商品备注,         -- 商品备注
    出货数量,                   -- 出货数量
    出货金额,                   -- 出货金额
    毛利额,                     -- 毛利额
    -- 计算毛利率（避免除零错误）
    CASE 
        WHEN 出货金额 = 0 THEN NULL
        ELSE ROUND(毛利额 / 出货金额 * 100, 2)
    END AS 毛利率
FROM #CH1 a
JOIN #store b ON a.门店gid = b.gid 
JOIN #itm c ON a.商品gid = c.gid
LEFT JOIN #ddplist d ON a.商品gid = d.gid
WHERE c.gid IS NOT NULL         -- 排除无商品信息的记录
  AND b.gid IS NOT NULL         -- 排除无门店信息的记录
  AND d.gid IS NOT NULL;        -- 仅包含大单品清单中的商品

-- 10. 按大类汇总出货数据（新增）
SELECT 
    c.scode1 AS 大类编码,       -- 商品大类编码
    c.sname1 AS 大类名称,       -- 商品大类名称
    COUNT(DISTINCT b.code) AS 出货门店数,      -- 统计出货门店数量
    COUNT(DISTINCT c.code) AS 出货商品数,      -- 统计出货商品数量
    SUM(出货数量) AS 出货总数量,                -- 汇总出货数量
    SUM(出货金额) AS 出货总金额,                -- 汇总出货金额
    SUM(毛利额) AS 毛利总额,                    -- 汇总毛利额
    -- 计算汇总毛利率（避免除零错误）
    CASE 
        WHEN SUM(出货金额) = 0 THEN NULL
        ELSE ROUND(SUM(毛利额) / SUM(出货金额) * 100, 2)
    END AS 毛利率,
    -- 计算平均每个门店出货金额
    CASE 
        WHEN COUNT(DISTINCT b.code) = 0 THEN NULL
        ELSE ROUND(SUM(出货金额) / COUNT(DISTINCT b.code), 2)
    END AS 店均出货金额
FROM #CH1 a
JOIN #store b ON a.门店gid = b.gid 
JOIN #itm c ON a.商品gid = c.gid
LEFT JOIN #ddplist d ON a.商品gid = d.gid
WHERE c.gid IS NOT NULL         -- 排除无商品信息的记录
  AND b.gid IS NOT NULL         -- 排除无门店信息的记录
  AND d.gid IS NOT NULL         -- 仅包含大单品清单中的商品
GROUP BY c.scode1, c.sname1
ORDER BY 出货总金额 DESC;        -- 按出货总金额降序排列

-- 11. 按事业部汇总出货数据（新增）
SELECT 
    syb AS 事业部,              -- 事业部
    COUNT(DISTINCT b.code) AS 出货门店数,      -- 统计出货门店数量
    COUNT(DISTINCT c.code) AS 出货商品数,      -- 统计出货商品数量
    SUM(出货数量) AS 出货总数量,                -- 汇总出货数量
    SUM(出货金额) AS 出货总金额,                -- 汇总出货金额
    SUM(毛利额) AS 毛利总额,                    -- 汇总毛利额
    -- 计算汇总毛利率（避免除零错误）
    CASE 
        WHEN SUM(出货金额) = 0 THEN NULL
        ELSE ROUND(SUM(毛利额) / SUM(出货金额) * 100, 2)
    END AS 毛利率,
    -- 计算平均每个门店出货金额
    CASE 
        WHEN COUNT(DISTINCT b.code) = 0 THEN NULL
        ELSE ROUND(SUM(出货金额) / COUNT(DISTINCT b.code), 2)
    END AS 店均出货金额
FROM #CH1 a
JOIN #store b ON a.门店gid = b.gid 
JOIN #itm c ON a.商品gid = c.gid
LEFT JOIN #ddplist d ON a.商品gid = d.gid
WHERE c.gid IS NOT NULL         -- 排除无商品信息的记录
  AND b.gid IS NOT NULL         -- 排除无门店信息的记录
  AND d.gid IS NOT NULL         -- 仅包含大单品清单中的商品
GROUP BY syb
ORDER BY 出货总金额 DESC;        -- 按出货总金额降序排列

-- 12. 按商品备注汇总出货数据（新增）
SELECT 
    remark AS 商品备注,         -- 商品备注
    COUNT(DISTINCT b.code) AS 出货门店数,      -- 统计出货门店数量
    COUNT(DISTINCT c.code) AS 出货商品数,      -- 统计出货商品数量
    SUM(出货数量) AS 出货总数量,                -- 汇总出货数量
    SUM(出货金额) AS 出货总金额,                -- 汇总出货金额
    SUM(毛利额) AS 毛利总额,                    -- 汇总毛利额
    -- 计算汇总毛利率（避免除零错误）
    CASE 
        WHEN SUM(出货金额) = 0 THEN NULL
        ELSE ROUND(SUM(毛利额) / SUM(出货金额) * 100, 2)
    END AS 毛利率,
    -- 计算平均每个门店出货金额
    CASE 
        WHEN COUNT(DISTINCT b.code) = 0 THEN NULL
        ELSE ROUND(SUM(出货金额) / COUNT(DISTINCT b.code), 2)
    END AS 店均出货金额
FROM #CH1 a
JOIN #store b ON a.门店gid = b.gid 
JOIN #itm c ON a.商品gid = c.gid
LEFT JOIN #ddplist d ON a.商品gid = d.gid
WHERE c.gid IS NOT NULL         -- 排除无商品信息的记录
  AND b.gid IS NOT NULL         -- 排除无门店信息的记录
  AND d.gid IS NOT NULL         -- 仅包含大单品清单中的商品
  AND remark IS NOT NULL        -- 仅包含有备注的商品
GROUP BY remark
ORDER BY 出货总金额 DESC;        -- 按出货总金额降序排列

-- 13. 清理临时表（提高性能）
DROP TABLE IF EXISTS #DATA1;
DROP TABLE IF EXISTS #CH1;
DROP TABLE IF EXISTS #itm;
DROP TABLE IF EXISTS #store;
DROP TABLE IF EXISTS #ddplist;

/*
 * 代码优化说明：
 * 1. 添加了详细的文件头注释，说明脚本功能和目的
 * 2. 引入了参数化日期设计，便于灵活配置分析时间范围
 * 3. 修复了全部字符编码问题，确保所有中文字符正确显示
 * 4. 修复了goodsz表和store表的WITH (NOLOCK)语法错误
 * 5. 添加了更详细的中文注释，解释每个步骤和字段的含义
 * 6. 新增毛利率计算，提供更详细的出货分析维度
 * 7. 增加了错误处理机制，确保数据插入操作的可靠性
 * 8. 新增按大类、事业部和商品备注汇总分析，提供多维度分析视角
 * 9. 优化了SQL结构，使代码更加清晰易读
 * 10. 添加了临时表清理代码，优化资源使用
 */
