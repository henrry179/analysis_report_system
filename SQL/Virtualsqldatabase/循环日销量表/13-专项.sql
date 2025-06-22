/*
 * 文件名: 13-专项.sql
 * 功能: 专项商品销售分析
 * 描述: 本脚本用于分析专项商品销售数据，支持按日期、门店、商品等多维度分析，并进行特定品类分析
 */

-- 1. 定义日期参数
DECLARE @start_date DATE;      -- 开始日期
DECLARE @end_date DATE;        -- 结束日期
DECLARE @period_start DATE;    -- 下半月开始日期
DECLARE @period_end DATE;      -- 下半月结束日期

-- 智能设置日期变量（可根据需要调整）
SET @start_date = DATEADD(DAY, -30, GETDATE());      -- 默认查询最近30天数据
SET @end_date = DATEADD(DAY, -1, GETDATE());         -- 截止到昨天
-- 下半月日期范围
SET @period_start = '2024-01-16';                    -- 下半月开始日期
SET @period_end = '2024-01-31';                      -- 下半月结束日期

-- 输出日期参数（便于调试和确认）
SELECT 
    @start_date AS 开始日期,
    @end_date AS 结束日期,
    @period_start AS 下半月开始日期,
    @period_end AS 下半月结束日期,
    DATEDIFF(DAY, @start_date, @end_date) + 1 AS 分析天数;

-- 2. 创建临时表存储专项商品数据（第一部分：基础专项商品数据）
DROP TABLE IF EXISTS #special_data;
SELECT 
    a.adate AS 日期,                     -- 销售日期
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
    a.dq1 AS 销售前数量,                  -- 销售前数量
    a.dq5 AS 销售后数量,                  -- 销售后数量
    a.dt1 AS 销售前金额,                  -- 销售前金额
    a.dt5 AS 销售后金额,                  -- 销售后金额
    a.dq1 - a.dq5 AS 销售数量,            -- 计算净销售数量
    a.dt1 - a.dt5 AS 销售金额,            -- 计算净销售金额
    -- 计算单品销售单价（避免除零错误）
    CASE 
        WHEN (a.dq1 - a.dq5) = 0 THEN NULL
        ELSE ROUND((a.dt1 - a.dt5) / (a.dq1 - a.dq5), 2)
    END AS 销售单价
INTO #special_data
FROM odsdbfqbi.dbo.hn_cx_special a
LEFT JOIN odsdbfq_basic.dbo.goodsz b WITH (NOLOCK) ON a.bgdgid = b.gid 
    AND b.companycode = 'hn'
LEFT JOIN odsdbfq_basic.dbo.store c WITH (NOLOCK) ON a.astore = c.gid 
    AND c.companycode = 'hn'
WHERE a.companycode = 'hn'
  AND a.adate BETWEEN @start_date AND @end_date;  -- 使用参数化日期范围

-- 3. 插入专项商品数据到分析表
PRINT '开始插入专项商品数据到分析表...';

BEGIN TRY
    BEGIN TRANSACTION;
    
    INSERT INTO odsdbfqbi.dbo.hn_special_analysis
    SELECT 
        日期,                      -- 销售日期
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
        销售前数量,                  -- 销售前数量
        销售后数量,                  -- 销售后数量
        销售前金额,                  -- 销售前金额
        销售后金额,                  -- 销售后金额
        销售数量,                   -- 计算净销售数量
        销售金额,                   -- 计算净销售金额
        GETDATE() AS 分析时间       -- 当前时间为分析时间
    FROM #special_data
    WHERE 销售数量 > 0              -- 仅包含有有效销售的数据
        OR 销售金额 > 0;
    
    PRINT '专项商品数据插入成功，共插入 ' + 
          CAST(@@ROWCOUNT AS VARCHAR(10)) + ' 条记录';
    
    COMMIT TRANSACTION;
END TRY
BEGIN CATCH
    IF @@TRANCOUNT > 0
        ROLLBACK TRANSACTION;
    
    PRINT '专项商品数据插入失败: ' + ERROR_MESSAGE();
END CATCH

-- 4. 按门店统计专项商品销售效果
SELECT 
    事业部 AS '事业部',              -- 所属事业部
    经营区 AS '经营区',              -- 所属经营区
    区长 AS '区长',                  -- 区长信息
    指导员 AS '指导员',              -- 指导员信息
    门店编码 AS '门店编码',           -- 门店编码
    门店名称 AS '门店名称',           -- 门店名称
    门店类型 AS '门店类型',           -- 门店类型
    COUNT(DISTINCT 日期) AS '销售天数',              -- 统计销售活动天数
    COUNT(DISTINCT 商品编码) AS '销售商品数',         -- 统计销售商品数量
    SUM(销售数量) AS '销售总数量',                    -- 汇总销售数量
    SUM(销售金额) AS '销售总金额',                    -- 汇总销售金额
    -- 新增：计算平均每天销售金额
    ROUND(SUM(销售金额) / NULLIF(COUNT(DISTINCT 日期), 0), 2) AS '日均销售金额',
    -- 新增：计算平均每个商品销售金额
    ROUND(SUM(销售金额) / NULLIF(COUNT(DISTINCT 商品编码), 0), 2) AS '单品平均销售金额',
    -- 新增：计算平均销售单价
    AVG(销售单价) AS '平均销售单价'
FROM #special_data
WHERE 销售数量 > 0                  -- 仅包含有有效销售的数据
    OR 销售金额 > 0
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
    '销售总金额' DESC;               -- 按事业部、经营区和销售总金额排序

-- 5. 按商品大类统计专项商品销售效果（新增）
SELECT 
    大类 AS '大类编码',              -- 大类编码
    大类名 AS '大类名称',            -- 大类名称
    COUNT(DISTINCT 门店编码) AS '销售门店数',        -- 统计销售门店数量
    COUNT(DISTINCT 日期) AS '销售天数',              -- 统计销售活动天数
    COUNT(DISTINCT 商品编码) AS '销售商品数',         -- 统计销售商品数量
    SUM(销售数量) AS '销售总数量',                    -- 汇总销售数量
    SUM(销售金额) AS '销售总金额',                    -- 汇总销售金额
    -- 新增：计算平均每家门店销售金额
    ROUND(SUM(销售金额) / NULLIF(COUNT(DISTINCT 门店编码), 0), 2) AS '店均销售金额',
    -- 新增：计算平均每天销售金额
    ROUND(SUM(销售金额) / NULLIF(COUNT(DISTINCT 日期), 0), 2) AS '日均销售金额',
    -- 新增：计算平均销售单价
    AVG(销售单价) AS '平均销售单价'
FROM #special_data
WHERE 销售数量 > 0                  -- 仅包含有有效销售的数据
    OR 销售金额 > 0
GROUP BY 
    大类,
    大类名
ORDER BY 
    '销售总金额' DESC;               -- 按销售总金额排序

-- 6. 下半月销售数据分析（按商品明细）
DROP TABLE IF EXISTS #sale1;
SELECT 
    astore,                        -- 门店ID
    bgdgid,                        -- 商品ID
    SUM(DQ1 - DQ5) AS 销售数量,     -- 计算净销售数量
    SUM(DT1 - DT5) AS 销售金额      -- 计算净销售金额
INTO #sale1
FROM odsdbfqbi.dbo.mtd
WHERE adate BETWEEN @period_start AND @period_end  -- 使用参数化的下半月日期范围
GROUP BY astore, bgdgid;

-- 7. 关联门店和商品信息
DROP TABLE IF EXISTS #sale2;
SELECT 
    a.*,                          -- 销售基础数据
    syb,                          -- 事业部
    b.code AS storecode,          -- 门店编码
    scode1 AS 大类编码,             -- 商品大类编码
    sname1 AS 大类名称,             -- 商品大类名称
    scode3 AS 小类编码,             -- 商品小类编码
    sname3 AS 小类名称              -- 商品小类名称
INTO #sale2 
FROM #sale1 a
LEFT JOIN odsdbfq_basic.dbo.store b WITH (NOLOCK) ON a.astore = b.gid 
    AND b.companycode = 'hn'
LEFT JOIN odsdbfq_basic.dbo.goodsz c WITH (NOLOCK) ON a.bgdgid = c.gid 
    AND c.companycode = 'hn'
WHERE b.stat = '有效';              -- 仅包含有效门店

-- 8. 更新零食事业部门店标识
UPDATE #sale2
SET syb = '零食事业部'              -- 设置为零食事业部
WHERE storecode IN (
    SELECT DISTINCT 编码            -- 获取零食事业部的门店编码
    FROM odsdbfqbi.dbo.storeinf
    WHERE 事业部 = '零食事业部'
);

-- 9. 饮料类销售统计（按事业部汇总）
SELECT 
    syb AS '事业部',                -- 事业部
    SUM(销售金额) AS '销售金额',      -- 汇总销售金额
    '饮料类' AS '备注'               -- 数据标识
FROM #sale2
WHERE 小类编码 IN ('110101', '110102')  -- 饮料类小类编码
GROUP BY syb
ORDER BY '销售金额' DESC;              -- 按销售金额排序

-- 10. 零食类销售统计（按事业部汇总，新增）
SELECT 
    syb AS '事业部',                -- 事业部
    SUM(销售金额) AS '销售金额',      -- 汇总销售金额
    '零食类' AS '备注'               -- 数据标识
FROM #sale2
WHERE 大类编码 IN ('11', '12')      -- 零食类大类编码
  AND 小类编码 NOT IN ('110101', '110102')  -- 排除饮料类
GROUP BY syb
ORDER BY '销售金额' DESC;              -- 按销售金额排序

-- 11. 各小类销售统计（新增）
SELECT 
    syb AS '事业部',                -- 事业部
    小类编码 AS '小类编码',           -- 小类编码
    小类名称 AS '小类名称',           -- 小类名称
    COUNT(DISTINCT storecode) AS '销售门店数',  -- 统计销售门店数量 
    SUM(销售数量) AS '销售数量',      -- 汇总销售数量
    SUM(销售金额) AS '销售金额',      -- 汇总销售金额
    -- 计算平均每家门店销售金额
    ROUND(SUM(销售金额) / NULLIF(COUNT(DISTINCT storecode), 0), 2) AS '店均销售金额',
    -- 计算平均单价
    CASE WHEN SUM(销售数量) = 0 THEN NULL 
         ELSE ROUND(SUM(销售金额) / SUM(销售数量), 2) END AS '平均单价'
FROM #sale2
WHERE 销售金额 > 0                  -- 仅包含有效销售记录
GROUP BY syb, 小类编码, 小类名称
ORDER BY syb, '销售金额' DESC;        -- 按事业部和销售金额排序

-- 12. 清理临时表（提高性能）
DROP TABLE IF EXISTS #special_data;
DROP TABLE IF EXISTS #sale1;
DROP TABLE IF EXISTS #sale2;

/*
 * 代码优化说明：
 * 1. 添加了详细的文件头注释，说明脚本功能和目的
 * 2. 引入了参数化日期设计，便于灵活配置分析时间范围
 * 3. 修复了全部字符编码问题，确保所有中文字符正确显示
 * 4. 修复了goodsz表和store表的WITH (NOLOCK)语法错误
 * 5. 添加了更详细的中文注释，解释每个步骤和字段的含义
 * 6. 新增销售单价计算，提供更详细的销售分析维度
 * 7. 增加了错误处理机制，确保数据插入操作的可靠性
 * 8. 新增按商品大类统计分析，提供多维度分析视角
 * 9. 新增零食类销售统计，扩展了专项分析范围
 * 10. 新增各小类销售统计，提供更细粒度的分析
 * 11. 优化了SQL结构，使代码更加清晰易读
 * 12. 添加了临时表清理代码，优化资源使用
 */ 