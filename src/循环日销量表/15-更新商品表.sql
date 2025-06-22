/*
 * 文件名: 15-更新商品表.sql
 * 功能: 特定商品销售分析
 * 描述: 本脚本用于分析特定商品（脉动和东方树叶）在各事业部的销售情况，包括销售门店数和销售金额
 */

-- 1. 定义日期参数
DECLARE @start_date DATE;        -- 开始日期
DECLARE @end_date DATE;          -- 结束日期
DECLARE @product_code1 VARCHAR(10) = '15062241';  -- 商品1编码（脉动）
DECLARE @product_code2 VARCHAR(10) = '27060407';  -- 商品2编码（东方树叶）

-- 智能设置日期变量（可根据需要调整）
SET @start_date = '2024-01-16';                    -- 开始日期
SET @end_date = DATEADD(DAY, -1, GETDATE());       -- 截止到昨天

-- 输出分析参数信息
SELECT 
    @start_date AS 开始日期,
    @end_date AS 结束日期,
    @product_code1 AS 商品1编码,
    @product_code2 AS 商品2编码,
    DATEDIFF(DAY, @start_date, @end_date) + 1 AS 分析天数;

-- 2. 汇总商品销售数据
DROP TABLE IF EXISTS #sales;

SELECT 
    LEFT(posno, LEN(RTRIM(posno))-2) AS storecode,   -- 提取门店编码（去除后两位）
    gdcode AS 商品编码,                               -- 商品编码
    SUM(realamt) AS 实际销售                          -- 销售金额汇总
INTO #sales
FROM odsdbfq_basic.dbo.buy2_biggoods WITH (NOLOCK)
WHERE CompanyCode = 'HN'                            -- 筛选湖南公司
  AND fildate BETWEEN @start_date AND @end_date     -- 使用参数化日期范围
  AND gdcode IN (@product_code1, @product_code2)    -- 筛选特定商品
GROUP BY LEFT(posno, LEN(RTRIM(posno))-2), gdcode;

-- 3. 关联门店信息
DROP TABLE IF EXISTS #sales2;

SELECT 
    a.*,                   -- 销售基础数据
    b.syb AS 事业部         -- 门店所属事业部
INTO #sales2 
FROM #sales a
LEFT JOIN odsdbfq_basic.dbo.store b WITH (NOLOCK) ON a.storecode = b.code 
    AND b.companycode = 'hn'
WHERE b.stat = '有效';     -- 仅包含有效门店

-- 4. 更新零食事业部门店标识
UPDATE #sales2
SET 事业部 = '零食事业部'     -- 设置为零食事业部
WHERE storecode IN (
    SELECT DISTINCT 编码     -- 获取零食事业部的门店编码
    FROM odsdbfqbi.dbo.storeinf
    WHERE 事业部 = '零食事业部'
);

-- 5. 按事业部汇总分析
SELECT 
    事业部,                -- 事业部名称
    -- 计算销售脉动的门店数
    COUNT(CASE WHEN 实际销售 > 0 AND 商品编码 = @product_code1 THEN storecode ELSE NULL END) AS 脉动门店数,
    -- 计算销售东方树叶的门店数
    COUNT(CASE WHEN 实际销售 > 0 AND 商品编码 = @product_code2 THEN storecode ELSE NULL END) AS 东方树叶门店数,
    -- 计算脉动销售金额
    SUM(CASE WHEN 商品编码 = @product_code1 THEN 实际销售 ELSE 0 END) AS 脉动销售额,
    -- 计算东方树叶销售金额
    SUM(CASE WHEN 商品编码 = @product_code2 THEN 实际销售 ELSE 0 END) AS 东方树叶销售额,
    -- 新增：计算两个品牌销售总额
    SUM(实际销售) AS 销售总额,
    -- 新增：计算脉动销售占比
    CASE 
        WHEN SUM(实际销售) = 0 THEN 0
        ELSE ROUND(SUM(CASE WHEN 商品编码 = @product_code1 THEN 实际销售 ELSE 0 END) * 100.0 / SUM(实际销售), 2)
    END AS 脉动销售占比,
    -- 新增：获取有效门店总数（用于计算覆盖率）
    (
        SELECT COUNT(*) 
        FROM odsdbfq_basic.dbo.store WITH (NOLOCK)
        WHERE companycode = 'hn' AND stat = '有效' AND syb = #sales2.事业部
        GROUP BY syb
    ) AS 事业部门店总数,
    -- 新增：计算脉动门店覆盖率
    CASE 
        WHEN (
            SELECT COUNT(*) 
            FROM odsdbfq_basic.dbo.store WITH (NOLOCK)
            WHERE companycode = 'hn' AND stat = '有效' AND syb = #sales2.事业部
            GROUP BY syb
        ) = 0 THEN 0
        ELSE ROUND(
            COUNT(CASE WHEN 实际销售 > 0 AND 商品编码 = @product_code1 THEN storecode ELSE NULL END) * 100.0 / 
            (
                SELECT COUNT(*) 
                FROM odsdbfq_basic.dbo.store WITH (NOLOCK)
                WHERE companycode = 'hn' AND stat = '有效' AND syb = #sales2.事业部
                GROUP BY syb
            ), 2)
    END AS 脉动覆盖率
FROM #sales2
GROUP BY 事业部
ORDER BY 销售总额 DESC; -- 按销售总额降序排序

-- 6. 门店详细分析（新增）
SELECT 
    a.storecode AS 门店编码,
    b.name AS 门店名称,
    a.事业部,
    b.shoptype AS 门店类型,
    b.kfq AS 经营区,
    -- 脉动销售信息
    SUM(CASE WHEN 商品编码 = @product_code1 THEN 实际销售 ELSE 0 END) AS 脉动销售额,
    CASE WHEN SUM(CASE WHEN 商品编码 = @product_code1 THEN 实际销售 ELSE 0 END) > 0 THEN '是' ELSE '否' END AS 是否销售脉动,
    -- 东方树叶销售信息
    SUM(CASE WHEN 商品编码 = @product_code2 THEN 实际销售 ELSE 0 END) AS 东方树叶销售额,
    CASE WHEN SUM(CASE WHEN 商品编码 = @product_code2 THEN 实际销售 ELSE 0 END) > 0 THEN '是' ELSE '否' END AS 是否销售东方树叶,
    -- 总销售额
    SUM(实际销售) AS 销售总额
FROM #sales2 a
LEFT JOIN odsdbfq_basic.dbo.store b WITH (NOLOCK) ON a.storecode = b.code 
    AND b.companycode = 'hn'
GROUP BY a.storecode, b.name, a.事业部, b.shoptype, b.kfq
ORDER BY a.事业部, 销售总额 DESC; -- 按事业部和销售总额降序排序

-- 7. 清理临时表
DROP TABLE IF EXISTS #sales;
DROP TABLE IF EXISTS #sales2;

/*
 * 代码优化说明：
 * 1. 添加了详细的文件头注释，说明脚本功能和目的
 * 2. 引入了参数化日期设计，便于灵活配置分析时间范围
 * 3. 修复了全部字符编码问题，确保所有中文字符正确显示
 * 4. 修复了store表的WITH (NOLOCK)语法错误
 * 5. 添加了更详细的中文注释，解释每个步骤和字段的含义
 * 6. 新增销售占比计算，提供更详细的销售分析维度
 * 7. 新增门店覆盖率计算，评估商品在各事业部的覆盖情况
 * 8. 新增门店详细分析报表，提供更细粒度的分析视角
 * 9. 优化了SQL结构，使代码更加清晰易读
 * 10. 添加了临时表清理代码，优化资源使用
 */
