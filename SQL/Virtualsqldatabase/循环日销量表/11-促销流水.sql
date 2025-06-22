/*
 * 文件名: 11-促销流水.sql
 * 功能: 促销活动多维度分析
 * 描述: 本脚本用于分析促销活动数据，支持按日期、门店、商品等多维度分析，帮助评估促销效果
 */

-- 1. 定义日期参数
DECLARE @start_date DATE;      -- 开始日期
DECLARE @end_date DATE;        -- 结束日期

-- 智能设置日期变量（可根据需要调整）
SET @start_date = DATEADD(DAY, -30, GETDATE());  -- 默认查询最近30天数据
SET @end_date = DATEADD(DAY, -1, GETDATE());     -- 截止到昨天

-- 输出日期参数（便于调试和确认）
SELECT 
    @start_date AS 开始日期,
    @end_date AS 结束日期,
    DATEDIFF(DAY, @start_date, @end_date) + 1 AS 统计天数;

-- 2. 创建索引（提高查询性能）
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_odsdbfqbi_dbo_hn_cx_promotion_1' AND object_id = OBJECT_ID('odsdbfqbi.dbo.hn_cx_promotion'))
BEGIN
    PRINT '正在创建促销表索引...';
    CREATE INDEX IX_odsdbfqbi_dbo_hn_cx_promotion_1 
    ON odsdbfqbi.dbo.hn_cx_promotion (adate, astore, bgdgid);
    PRINT '促销表索引创建成功';
END
ELSE
BEGIN
    PRINT '促销表索引已存在，无需创建';
END

-- 3. 获取促销数据
DROP TABLE IF EXISTS #promotion_data;
SELECT 
    a.adate AS 日期,                      -- 促销日期
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
  AND a.adate BETWEEN @start_date AND @end_date  -- 使用参数化日期范围
  AND (a.dq1 - a.dq5) > 0;                      -- 只筛选有效促销数据（净销售量大于0）

-- 4. 统计门店促销数据
DROP TABLE IF EXISTS #store_promotion;
SELECT 
    门店编码,                               -- 门店编码
    门店名称,                               -- 门店名称
    门店类型,                               -- 门店类型
    事业部,                                 -- 所属事业部
    经营区,                                 -- 所属经营区
    区长,                                   -- 区长信息
    指导员,                                 -- 指导员信息
    COUNT(DISTINCT 日期) AS 促销天数,       -- 统计促销活动天数
    COUNT(DISTINCT 商品编码) AS 促销商品数,  -- 统计促销商品数量
    SUM(促销数量) AS 促销总数量,             -- 汇总促销销售数量
    SUM(促销金额) AS 促销总金额,             -- 汇总促销销售金额
    -- 新增：计算平均每天促销金额
    ROUND(SUM(促销金额) / NULLIF(COUNT(DISTINCT 日期), 0), 2) AS 日均促销金额,
    -- 新增：计算平均每个商品促销金额
    ROUND(SUM(促销金额) / NULLIF(COUNT(DISTINCT 商品编码), 0), 2) AS 单品平均促销金额,
    -- 新增：计算平均折扣率
    AVG(折扣率) AS 平均折扣率
INTO #store_promotion
FROM #promotion_data
GROUP BY 
    门店编码,
    门店名称,
    门店类型,
    事业部,
    经营区,
    区长,
    指导员;

-- 5. 统计商品促销数据
DROP TABLE IF EXISTS #item_promotion;
SELECT 
    商品编码,                               -- 商品编码
    商品名称,                               -- 商品名称
    大类,                                   -- 商品大类编码
    大类名,                                 -- 商品大类名称
    COUNT(DISTINCT 日期) AS 促销天数,       -- 统计促销活动天数
    COUNT(DISTINCT 门店编码) AS 促销门店数,  -- 统计参与促销的门店数
    SUM(促销数量) AS 促销总数量,             -- 汇总促销销售数量
    SUM(促销金额) AS 促销总金额,             -- 汇总促销销售金额
    -- 新增：计算平均每天促销金额
    ROUND(SUM(促销金额) / NULLIF(COUNT(DISTINCT 日期), 0), 2) AS 日均促销金额,
    -- 新增：计算平均每个门店促销金额
    ROUND(SUM(促销金额) / NULLIF(COUNT(DISTINCT 门店编码), 0), 2) AS 门店平均促销金额,
    -- 新增：计算平均折扣率
    AVG(折扣率) AS 平均折扣率
INTO #item_promotion
FROM #promotion_data
GROUP BY 
    商品编码,
    商品名称,
    大类,
    大类名;

-- 6. 统计大类促销数据（新增）
DROP TABLE IF EXISTS #category_promotion;
SELECT 
    大类,                                   -- 商品大类编码
    大类名,                                 -- 商品大类名称
    COUNT(DISTINCT 日期) AS 促销天数,       -- 统计促销活动天数
    COUNT(DISTINCT 门店编码) AS 促销门店数,  -- 统计参与促销的门店数
    COUNT(DISTINCT 商品编码) AS 促销商品数,  -- 统计促销商品数量
    SUM(促销数量) AS 促销总数量,             -- 汇总促销销售数量
    SUM(促销金额) AS 促销总金额,             -- 汇总促销销售金额
    -- 新增：计算平均每天促销金额
    ROUND(SUM(促销金额) / NULLIF(COUNT(DISTINCT 日期), 0), 2) AS 日均促销金额,
    -- 新增：计算平均每个商品促销金额
    ROUND(SUM(促销金额) / NULLIF(COUNT(DISTINCT 商品编码), 0), 2) AS 单品平均促销金额,
    -- 新增：计算平均折扣率
    AVG(折扣率) AS 平均折扣率
INTO #category_promotion
FROM #promotion_data
GROUP BY 
    大类,
    大类名;

-- 7. 输出门店促销汇总
SELECT 
    a.*,                       -- 门店促销数据
    b.有效门店数,               -- 有效门店总数
    CASE 
        WHEN b.有效门店数 > 0 THEN 
            ROUND(a.促销总金额 / b.有效门店数, 2) 
        ELSE NULL 
    END AS 平均每门店促销金额,  -- 新增：事业部平均每门店促销金额
    CONVERT(VARCHAR(10), ROUND(100.0 * a.促销商品数 / NULLIF(c.品类商品总数, 0), 2)) + '%' AS 商品覆盖率  -- 新增：促销商品覆盖率
FROM #store_promotion a
LEFT JOIN (
    -- 计算各事业部有效门店数
    SELECT 
        事业部,
        COUNT(*) AS 有效门店数
    FROM odsdbfq_basic.dbo.store WITH (NOLOCK)
    WHERE companycode = 'hn' 
        AND stat = '有效'
    GROUP BY 事业部
) b ON a.事业部 = b.事业部
LEFT JOIN (
    -- 计算各事业部商品总数（用于计算覆盖率）
    SELECT 
        c.syb AS 事业部,
        COUNT(DISTINCT b.code) AS 品类商品总数
    FROM odsdbfq_basic.dbo.goodsz b WITH (NOLOCK)
    CROSS JOIN (SELECT DISTINCT syb FROM odsdbfq_basic.dbo.store WHERE companycode = 'hn') c
    WHERE b.companycode = 'hn'
    GROUP BY c.syb
) c ON a.事业部 = c.事业部
ORDER BY a.事业部, a.经营区, a.促销总金额 DESC;  -- 按事业部、经营区和促销总金额排序

-- 8. 输出商品促销汇总
SELECT 
    a.*,
    b.品类商品总数,
    CONVERT(VARCHAR(10), ROUND(100.0 * a.促销门店数 / NULLIF(c.门店总数, 0), 2)) + '%' AS 门店覆盖率  -- 新增：门店覆盖率
FROM #item_promotion a
LEFT JOIN (
    -- 计算各大类商品总数
    SELECT 
        scode1 AS 大类,
        COUNT(DISTINCT code) AS 品类商品总数
    FROM odsdbfq_basic.dbo.goodsz WITH (NOLOCK)
    WHERE companycode = 'hn'
    GROUP BY scode1
) b ON a.大类 = b.大类
LEFT JOIN (
    -- 计算总门店数
    SELECT COUNT(*) AS 门店总数
    FROM odsdbfq_basic.dbo.store WITH (NOLOCK)
    WHERE companycode = 'hn' 
        AND stat = '有效'
) c ON 1=1
ORDER BY a.促销总金额 DESC;  -- 按促销总金额降序排列

-- 9. 输出大类促销汇总（新增）
SELECT 
    a.*,
    b.品类商品总数,
    CONVERT(VARCHAR(10), ROUND(100.0 * a.促销商品数 / NULLIF(b.品类商品总数, 0), 2)) + '%' AS 商品覆盖率,  -- 计算商品覆盖率
    CONVERT(VARCHAR(10), ROUND(100.0 * a.促销门店数 / NULLIF(c.门店总数, 0), 2)) + '%' AS 门店覆盖率      -- 计算门店覆盖率
FROM #category_promotion a
LEFT JOIN (
    -- 计算各大类商品总数
    SELECT 
        scode1 AS 大类,
        COUNT(DISTINCT code) AS 品类商品总数
    FROM odsdbfq_basic.dbo.goodsz WITH (NOLOCK)
    WHERE companycode = 'hn'
    GROUP BY scode1
) b ON a.大类 = b.大类
LEFT JOIN (
    -- 计算总门店数
    SELECT COUNT(*) AS 门店总数
    FROM odsdbfq_basic.dbo.store WITH (NOLOCK)
    WHERE companycode = 'hn' 
        AND stat = '有效'
) c ON 1=1
ORDER BY a.促销总金额 DESC;  -- 按促销总金额降序排列

-- 10. 输出促销明细（最近100条，避免数据过多）
SELECT TOP 100 
    日期,
    门店编码,
    门店名称,
    事业部,
    经营区,
    商品编码,
    商品名称,
    大类,
    大类名,
    促销前数量,
    促销后数量,
    促销数量,
    促销前金额,
    促销后金额,
    促销金额,
    折扣率
FROM #promotion_data
ORDER BY 日期 DESC, 促销金额 DESC;  -- 按日期降序和促销金额降序排列

-- 11. 清理临时表（提高性能）
DROP TABLE IF EXISTS #promotion_data;
DROP TABLE IF EXISTS #store_promotion;
DROP TABLE IF EXISTS #item_promotion;
DROP TABLE IF EXISTS #category_promotion;

/*
 * 代码优化说明：
 * 1. 添加了详细的文件头注释，说明脚本功能和目的
 * 2. 引入了参数化日期设计，使查询时间范围可灵活配置
 * 3. 修复了goodsz表和store表的WITH (NOLOCK)语法错误
 * 4. 添加了更详细的中文注释，解释每个字段的含义和计算逻辑
 * 5. 新增折扣率计算，提供更多促销效果分析维度
 * 6. 新增大类维度分析，便于从更高层面评估促销效果
 * 7. 新增覆盖率分析，计算促销商品和门店的覆盖情况
 * 8. 新增日均促销金额等衍生指标，提供更多分析视角
 * 9. 优化输出结果排序，更直观展示重要数据
 * 10. 限制明细数据输出数量，避免数据量过大影响性能
 * 11. 添加了临时表清理代码，优化资源使用
 * 12. 添加了索引创建时的提示信息，便于判断执行状态
 */
