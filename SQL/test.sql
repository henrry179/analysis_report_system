-- =====================================================
-- 生鲜社区行业品类商品明细数据生成系统
-- CTE多表连接架构 - 50000行商品明细数据
-- 创建时间: 2025-01-27 10:30:15
-- 数据表维度: 20张核心业务表
-- =====================================================

-- 1. 数字序列生成器
WITH RECURSIVE numbers AS (
    SELECT 1 as n
    UNION ALL
    SELECT n + 1 FROM numbers WHERE n < 50000
),

-- 2. 商品基础信息表
product_base AS (
    SELECT 
        n as product_id,
        CASE 
            WHEN n % 10 = 0 THEN '蔬菜类'
            WHEN n % 10 = 1 THEN '水果类'
            WHEN n % 10 = 2 THEN '肉禽蛋类'
            WHEN n % 10 = 3 THEN '水产海鲜'
            WHEN n % 10 = 4 THEN '乳制品'
            WHEN n % 10 = 5 THEN '粮油调料'
            WHEN n % 10 = 6 THEN '冷冻食品'
            WHEN n % 10 = 7 THEN '豆制品'
            WHEN n % 10 = 8 THEN '熟食卤味'
            ELSE '其他生鲜'
        END as category_name,
        CONCAT('商品_', LPAD(n, 6, '0')) as product_name,
        ROUND((n % 50) + 5, 2) as base_price,
        CASE 
            WHEN n % 5 = 0 THEN '有机'
            WHEN n % 5 = 1 THEN '绿色'
            WHEN n % 5 = 2 THEN '无公害'
            ELSE '普通'
        END as quality_grade,
        DATE_SUB(CURDATE(), INTERVAL (n % 365) DAY) as create_date
    FROM numbers
    WHERE n <= 50000
),

-- 3. 供应商信息表
supplier_info AS (
    SELECT 
        n as supplier_id,
        CONCAT('供应商_', CHAR(65 + (n % 26)), LPAD(n, 4, '0')) as supplier_name,
        CASE 
            WHEN n % 5 = 0 THEN '北京市'
            WHEN n % 5 = 1 THEN '上海市'
            WHEN n % 5 = 2 THEN '广州市'
            WHEN n % 5 = 3 THEN '深圳市'
            ELSE '杭州市'
        END as supplier_city,
        ROUND((n % 3) + 3, 1) as supplier_rating,
        CASE 
            WHEN n % 4 = 0 THEN '金牌供应商'
            WHEN n % 4 = 1 THEN '银牌供应商'
            WHEN n % 4 = 2 THEN '铜牌供应商'
            ELSE '普通供应商'
        END as supplier_level
    FROM numbers
    WHERE n <= 500
),

-- 4. 社区门店信息表
community_store AS (
    SELECT 
        n as store_id,
        CONCAT('社区店_', LPAD(n, 4, '0')) as store_name,
        CASE 
            WHEN n % 3 = 0 THEN '一线城市'
            WHEN n % 3 = 1 THEN '二线城市'
            ELSE '三线城市'
        END as city_level,
        CASE 
            WHEN n % 3 = 0 THEN '高档社区'
            WHEN n % 3 = 1 THEN '中档社区'
            ELSE '普通社区'
        END as community_type,
        (n % 500) + 100 as store_area_sqm,
        (n % 20000) + 5000 as daily_customer_flow
    FROM numbers
    WHERE n <= 200
),

-- 5. 品类管理表
category_management AS (
    SELECT 
        ROW_NUMBER() OVER (ORDER BY category_name) as category_id,
        category_name,
        CASE category_name
            WHEN '蔬菜类' THEN '生鲜蔬菜'
            WHEN '水果类' THEN '新鲜水果'
            WHEN '肉禽蛋类' THEN '肉类蛋白'
            WHEN '水产海鲜' THEN '海鲜水产'
            WHEN '乳制品' THEN '奶制品类'
            WHEN '粮油调料' THEN '厨房必需'
            WHEN '冷冻食品' THEN '速冻便民'
            WHEN '豆制品' THEN '植物蛋白'
            WHEN '熟食卤味' THEN '即食熟食'
            ELSE '其他分类'
        END as category_desc,
        CASE category_name
            WHEN '蔬菜类' THEN 0.15
            WHEN '水果类' THEN 0.25
            WHEN '肉禽蛋类' THEN 0.20
            WHEN '水产海鲜' THEN 0.30
            WHEN '乳制品' THEN 0.18
            WHEN '粮油调料' THEN 0.12
            WHEN '冷冻食品' THEN 0.22
            WHEN '豆制品' THEN 0.16
            WHEN '熟食卤味' THEN 0.35
            ELSE 0.20
        END as category_margin_rate,
        CASE category_name
            WHEN '蔬菜类' THEN 1
            WHEN '水果类' THEN 2
            WHEN '肉禽蛋类' THEN 0.5
            ELSE 3
        END as shelf_life_days
    FROM (
        SELECT DISTINCT category_name FROM product_base
    ) cat
),

-- 6. 库存管理表
inventory_management AS (
    SELECT 
        pb.product_id,
        pb.product_name,
        cs.store_id,
        (pb.product_id % 1000) + 50 as current_stock,
        (pb.product_id % 200) + 20 as min_stock_alert,
        (pb.product_id % 2000) + 500 as max_stock_limit,
        DATE_SUB(CURDATE(), INTERVAL (pb.product_id % 30) DAY) as last_restock_date,
        CASE 
            WHEN pb.product_id % 5 = 0 THEN '库存充足'
            WHEN pb.product_id % 5 = 1 THEN '库存正常'
            WHEN pb.product_id % 5 = 2 THEN '库存偏低'
            ELSE '急需补货'
        END as stock_status
    FROM product_base pb
    CROSS JOIN community_store cs
    WHERE pb.product_id % 5 = 0  -- 只选择部分组合以控制数据量
    LIMIT 10000
),

-- 7. 价格策略表
pricing_strategy AS (
    SELECT 
        pb.product_id,
        pb.base_price,
        ROUND(pb.base_price * 1.3, 2) as market_price,
        ROUND(pb.base_price * 0.9, 2) as promotion_price,
        CASE 
            WHEN pb.product_id % 4 = 0 THEN '会员专享'
            WHEN pb.product_id % 4 = 1 THEN '限时特价'
            WHEN pb.product_id % 4 = 2 THEN '满减优惠'
            ELSE '正常售价'
        END as pricing_type,
        DATE_ADD(CURDATE(), INTERVAL (pb.product_id % 30) DAY) as price_valid_until
    FROM product_base pb
),

-- 8. 销售订单表
sales_order AS (
    SELECT 
        n as order_id,
        CONCAT('ORD_', DATE_FORMAT(NOW(), '%Y%m%d'), '_', LPAD(n, 8, '0')) as order_no,
        (n % 200) + 1 as store_id,
        (n % 10000) + 1 as customer_id,
        DATE_SUB(CURDATE(), INTERVAL (n % 90) DAY) as order_date,
        CASE 
            WHEN n % 5 = 0 THEN '已完成'
            WHEN n % 5 = 1 THEN '配送中'
            WHEN n % 5 = 2 THEN '待配送'
            WHEN n % 5 = 3 THEN '已支付'
            ELSE '待支付'
        END as order_status,
        ROUND((n % 200) + 20, 2) as order_amount
    FROM numbers
    WHERE n <= 25000
),

-- 9. 客户信息表
customer_info AS (
    SELECT 
        n as customer_id,
        CONCAT('客户_', LPAD(n, 6, '0')) as customer_name,
        CASE 
            WHEN n % 2 = 0 THEN '女'
            ELSE '男'
        END as gender,
        (n % 50) + 20 as age,
        CASE 
            WHEN n % 3 = 0 THEN '高消费'
            WHEN n % 3 = 1 THEN '中消费'
            ELSE '低消费'
        END as consumption_level,
        ROUND((n % 5000) + 500, 2) as monthly_spend,
        DATE_SUB(CURDATE(), INTERVAL (n % 1000) DAY) as register_date
    FROM numbers
    WHERE n <= 10000
),

-- 10. 促销活动表
promotion_activity AS (
    SELECT 
        n as promotion_id,
        CONCAT('促销_', DATE_FORMAT(CURDATE(), '%Y%m'), '_', LPAD(n, 3, '0')) as promotion_name,
        CASE 
            WHEN n % 4 = 0 THEN '满减活动'
            WHEN n % 4 = 1 THEN '买赠活动'
            WHEN n % 4 = 2 THEN '折扣活动'
            ELSE '秒杀活动'
        END as promotion_type,
        ROUND((n % 40) / 100.0 + 0.1, 2) as discount_rate,
        DATE_SUB(CURDATE(), INTERVAL (n % 30) DAY) as start_date,
        DATE_ADD(CURDATE(), INTERVAL (n % 60) DAY) as end_date,
        CASE 
            WHEN n % 3 = 0 THEN '进行中'
            WHEN n % 3 = 1 THEN '已结束'
            ELSE '未开始'
        END as promotion_status
    FROM numbers
    WHERE n <= 100
),

-- 11. 配送信息表
delivery_info AS (
    SELECT 
        so.order_id,
        CONCAT('配送员_', LPAD((so.order_id % 200) + 1, 3, '0')) as delivery_person,
        CASE 
            WHEN so.order_id % 4 = 0 THEN '30分钟达'
            WHEN so.order_id % 4 = 1 THEN '1小时达'
            WHEN so.order_id % 4 = 2 THEN '2小时达'
            ELSE '次日达'
        END as delivery_type,
        ROUND((so.order_id % 10) + 2, 2) as delivery_fee,
        CASE 
            WHEN so.order_id % 4 = 0 THEN '已送达'
            WHEN so.order_id % 4 = 1 THEN '配送中'
            WHEN so.order_id % 4 = 2 THEN '待配送'
            ELSE '配送异常'
        END as delivery_status,
        DATE_ADD(so.order_date, INTERVAL (so.order_id % 3) HOUR) as delivery_time
    FROM sales_order so
    WHERE so.order_status IN ('已完成', '配送中', '待配送')
),

-- 12. 商品评价表
product_review AS (
    SELECT 
        pb.product_id,
        (pb.product_id % 10000) + 1 as customer_id,
        ROUND((pb.product_id % 2) + 3, 1) as rating_score,
        CASE 
            WHEN pb.product_id % 5 = 0 THEN '商品新鲜，质量很好'
            WHEN pb.product_id % 5 = 1 THEN '性价比不错，会再购买'
            WHEN pb.product_id % 5 = 2 THEN '配送及时，包装完好'
            WHEN pb.product_id % 5 = 3 THEN '口感一般，价格偏高'
            ELSE '质量有待提升'
        END as review_content,
        DATE_SUB(CURDATE(), INTERVAL (pb.product_id % 180) DAY) as review_date
    FROM product_base pb
    WHERE pb.product_id % 3 = 0  -- 只选择部分商品有评价
    LIMIT 15000
),

-- 13. 采购管理表
purchase_management AS (
    SELECT 
        ROW_NUMBER() OVER (ORDER BY pb.product_id, si.supplier_id) as purchase_id,
        pb.product_id,
        si.supplier_id,
        (pb.product_id % 5000) + 100 as purchase_quantity,
        ROUND(pb.base_price * 0.7, 2) as purchase_price,
        DATE_SUB(CURDATE(), INTERVAL (pb.product_id % 60) DAY) as purchase_date,
        CASE 
            WHEN pb.product_id % 4 = 0 THEN '已到货'
            WHEN pb.product_id % 4 = 1 THEN '在途中'
            WHEN pb.product_id % 4 = 2 THEN '已下单'
            ELSE '待审核'
        END as purchase_status
    FROM product_base pb
    CROSS JOIN supplier_info si
    WHERE pb.product_id % 10 = 0  -- 控制采购记录数量
    LIMIT 8000
),

-- 14. 损耗管理表
loss_management AS (
    SELECT 
        pb.product_id,
        cs.store_id,
        (pb.product_id % 50) + 1 as loss_quantity,
        CASE 
            WHEN pb.product_id % 4 = 0 THEN '过期损耗'
            WHEN pb.product_id % 4 = 1 THEN '运输损耗'
            WHEN pb.product_id % 4 = 2 THEN '储存损耗'
            ELSE '其他损耗'
        END as loss_reason,
        ROUND(pb.base_price * ((pb.product_id % 50) + 1), 2) as loss_amount,
        DATE_SUB(CURDATE(), INTERVAL (pb.product_id % 30) DAY) as loss_date
    FROM product_base pb
    CROSS JOIN community_store cs
    WHERE pb.product_id % 20 = 0  -- 控制损耗记录数量
    LIMIT 3000
),

-- 15. 会员管理表
member_management AS (
    SELECT 
        ci.customer_id,
        CASE 
            WHEN ci.monthly_spend > 3000 THEN '钻石会员'
            WHEN ci.monthly_spend > 2000 THEN '金牌会员'
            WHEN ci.monthly_spend > 1000 THEN '银牌会员'
            ELSE '普通会员'
        END as member_level,
        ROUND(ci.monthly_spend * 0.05, 0) as points_balance,
        CASE 
            WHEN ci.customer_id % 5 = 0 THEN 0.15
            WHEN ci.customer_id % 5 = 1 THEN 0.10
            WHEN ci.customer_id % 5 = 2 THEN 0.08
            ELSE 0.05
        END as discount_rate,
        DATE_ADD(ci.register_date, INTERVAL 365 DAY) as membership_expire_date
    FROM customer_info ci
),

-- 16. 季节性销售表
seasonal_sales AS (
    SELECT 
        pb.product_id,
        CASE 
            WHEN pb.category_name IN ('蔬菜类', '水果类') THEN
                CASE MONTH(CURDATE())
                    WHEN 1 THEN 0.8
                    WHEN 2 THEN 0.9
                    WHEN 3 THEN 1.2
                    WHEN 4 THEN 1.3
                    WHEN 5 THEN 1.4
                    WHEN 6 THEN 1.5
                    WHEN 7 THEN 1.6
                    WHEN 8 THEN 1.5
                    WHEN 9 THEN 1.3
                    WHEN 10 THEN 1.2
                    WHEN 11 THEN 1.0
                    ELSE 0.9
                END
            ELSE 1.0
        END as seasonal_factor,
        CASE MONTH(CURDATE())
            WHEN 1 THEN '冬季淡季'
            WHEN 2 THEN '春节旺季'
            WHEN 3 THEN '春季回暖'
            WHEN 4 THEN '春季旺季'
            WHEN 5 THEN '春夏过渡'
            WHEN 6 THEN '夏季开始'
            WHEN 7 THEN '夏季旺季'
            WHEN 8 THEN '夏季高峰'
            WHEN 9 THEN '秋季开始'
            WHEN 10 THEN '秋季旺季'
            WHEN 11 THEN '秋冬过渡'
            ELSE '冬季淡季'
        END as season_desc
    FROM product_base pb
),

-- 17. 竞争对手价格表
competitor_price AS (
    SELECT 
        pb.product_id,
        CONCAT('竞争对手_', CHAR(65 + (pb.product_id % 5))) as competitor_name,
        ROUND(pb.base_price * 1.1, 2) as competitor_price,
        CASE 
            WHEN pb.product_id % 3 = 0 THEN '价格优势'
            WHEN pb.product_id % 3 = 1 THEN '价格持平'
            ELSE '价格劣势'
        END as price_position,
        DATE_SUB(CURDATE(), INTERVAL (pb.product_id % 7) DAY) as price_update_date
    FROM product_base pb
    WHERE pb.product_id % 3 = 0  -- 只选择部分商品有竞对价格
    LIMIT 20000
),

-- 18. 质量检测表
quality_inspection AS (
    SELECT 
        pb.product_id,
        si.supplier_id,
        CASE 
            WHEN (pb.product_id + si.supplier_id) % 4 = 0 THEN '优秀'
            WHEN (pb.product_id + si.supplier_id) % 4 = 1 THEN '良好'
            WHEN (pb.product_id + si.supplier_id) % 4 = 2 THEN '合格'
            ELSE '待改进'
        END as quality_grade,
        ROUND((pb.product_id % 10) + 90, 1) as quality_score,
        DATE_SUB(CURDATE(), INTERVAL (pb.product_id % 30) DAY) as inspection_date,
        CASE 
            WHEN pb.product_id % 5 = 0 THEN '通过'
            ELSE '需复检'
        END as inspection_result
    FROM product_base pb
    CROSS JOIN supplier_info si
    WHERE pb.product_id % 20 = 0  -- 控制检测记录数量
    LIMIT 5000
),

-- 19. 营销活动效果表
marketing_effect AS (
    SELECT 
        pa.promotion_id,
        pb.product_id,
        (pb.product_id % 1000) + 50 as promotion_sales_qty,
        ROUND((pb.product_id % 10000) + 1000, 2) as promotion_sales_amount,
        ROUND((pb.product_id % 30) / 100.0 + 0.1, 2) as conversion_rate,
        ROUND((pb.product_id % 50) + 10, 2) as customer_acquisition_cost,
        CASE 
            WHEN pb.product_id % 3 = 0 THEN '效果显著'
            WHEN pb.product_id % 3 = 1 THEN '效果一般'
            ELSE '效果不佳'
        END as effect_evaluation
    FROM promotion_activity pa
    CROSS JOIN product_base pb
    WHERE pb.product_id % 50 = 0  -- 控制营销效果记录数量
    LIMIT 2000
),

-- 20. 供应链物流表
supply_chain_logistics AS (
    SELECT 
        pm.purchase_id,
        CONCAT('物流_', CHAR(65 + (pm.purchase_id % 3)), LPAD((pm.purchase_id % 100) + 1, 3, '0')) as logistics_company,
        ROUND((pm.purchase_id % 500) + 50, 2) as logistics_cost,
        (pm.purchase_id % 5) + 1 as transport_days,
        CASE 
            WHEN pm.purchase_id % 3 = 0 THEN '冷链运输'
            WHEN pm.purchase_id % 3 = 1 THEN '常温运输'
            ELSE '混合运输'
        END as transport_type,
        CASE 
            WHEN pm.purchase_id % 10 = 0 THEN '运输异常'
            ELSE '运输正常'
        END as transport_status
    FROM purchase_management pm
    WHERE pm.purchase_status IN ('在途中', '已到货')
),

-- 21. 财务结算表
financial_settlement AS (
    SELECT 
        so.order_id,
        so.order_amount,
        ROUND(so.order_amount * 0.03, 2) as platform_commission,
        ROUND(so.order_amount * 0.02, 2) as payment_fee,
        ROUND(so.order_amount * 0.15, 2) as cost_of_goods,
        ROUND(so.order_amount * 0.80, 2) as net_revenue,
        CASE 
            WHEN so.order_id % 3 = 0 THEN '已结算'
            WHEN so.order_id % 3 = 1 THEN '待结算'
            ELSE '结算中'
        END as settlement_status,
        DATE_ADD(so.order_date, INTERVAL 7 DAY) as settlement_date
    FROM sales_order so
    WHERE so.order_status = '已完成'
)

-- =====================================================
-- 主查询：生成50000行商品明细数据
-- 多表连接汇总分析
-- =====================================================
SELECT 
    -- 基础商品信息
    pb.product_id,
    pb.product_name,
    pb.category_name,
    pb.base_price,
    pb.quality_grade,
    pb.create_date,
    
    -- 供应商信息
    si.supplier_name,
    si.supplier_city,
    si.supplier_rating,
    si.supplier_level,
    
    -- 门店信息
    cs.store_name,
    cs.city_level,
    cs.community_type,
    cs.store_area_sqm,
    cs.daily_customer_flow,
    
    -- 品类管理
    cm.category_desc,
    cm.category_margin_rate,
    cm.shelf_life_days,
    
    -- 库存信息
    COALESCE(im.current_stock, 0) as current_stock,
    COALESCE(im.stock_status, '无库存') as stock_status,
    
    -- 价格策略
    ps.market_price,
    ps.promotion_price,
    ps.pricing_type,
    
    -- 销售数据
    COALESCE(so.order_amount, 0) as latest_order_amount,
    COALESCE(so.order_status, '无订单') as latest_order_status,
    
    -- 客户信息
    COALESCE(ci.consumption_level, '未知') as customer_consumption_level,
    COALESCE(ci.monthly_spend, 0) as customer_monthly_spend,
    
    -- 促销活动
    COALESCE(pa.promotion_name, '无促销') as active_promotion,
    COALESCE(pa.discount_rate, 0) as promotion_discount_rate,
    
    -- 配送信息
    COALESCE(di.delivery_type, '无配送') as delivery_type,
    COALESCE(di.delivery_fee, 0) as delivery_fee,
    
    -- 商品评价
    COALESCE(pr.rating_score, 0) as avg_rating_score,
    COALESCE(pr.review_content, '暂无评价') as latest_review,
    
    -- 采购信息
    COALESCE(pm.purchase_price, 0) as latest_purchase_price,
    COALESCE(pm.purchase_status, '无采购') as purchase_status,
    
    -- 损耗信息
    COALESCE(lm.loss_amount, 0) as total_loss_amount,
    COALESCE(lm.loss_reason, '无损耗') as main_loss_reason,
    
    -- 会员信息
    COALESCE(mm.member_level, '非会员') as customer_member_level,
    COALESCE(mm.discount_rate, 0) as member_discount_rate,
    
    -- 季节性因子
    ss.seasonal_factor,
    ss.season_desc,
    
    -- 竞争对手价格
    COALESCE(cp.competitor_price, 0) as competitor_avg_price,
    COALESCE(cp.price_position, '无对比') as price_competitive_position,
    
    -- 质量检测
    COALESCE(qi.quality_score, 0) as quality_inspection_score,
    COALESCE(qi.inspection_result, '未检测') as quality_status,
    
    -- 营销效果
    COALESCE(me.conversion_rate, 0) as marketing_conversion_rate,
    COALESCE(me.effect_evaluation, '无营销') as marketing_effectiveness,
    
    -- 物流信息
    COALESCE(scl.logistics_cost, 0) as logistics_cost,
    COALESCE(scl.transport_type, '无物流') as transport_method,
    
    -- 财务结算
    COALESCE(fs.net_revenue, 0) as net_revenue,
    COALESCE(fs.settlement_status, '无结算') as financial_settlement_status,
    
    -- 计算字段
    ROUND((ps.market_price - pb.base_price) / pb.base_price * 100, 2) as price_markup_percentage,
    ROUND(COALESCE(im.current_stock, 0) * pb.base_price, 2) as inventory_value,
    CASE 
        WHEN COALESCE(im.current_stock, 0) < COALESCE(im.min_stock_alert, 20) THEN '库存预警'
        WHEN COALESCE(im.current_stock, 0) > COALESCE(im.max_stock_limit, 1000) THEN '库存过量'
        ELSE '库存正常'
    END as inventory_alert_status,
    
    -- 综合评分 (基于多个维度)
    ROUND(
        (COALESCE(pr.rating_score, 3) * 0.3 + 
         si.supplier_rating * 0.2 + 
         COALESCE(qi.quality_score, 80) / 20 * 0.3 + 
         (CASE WHEN ps.pricing_type = '会员专享' THEN 5 ELSE 3 END) * 0.2), 1
    ) as comprehensive_score,
    
    -- 数据生成时间戳
    NOW() as data_generated_time,
    
    -- 行号标识
    ROW_NUMBER() OVER (ORDER BY pb.product_id, cs.store_id) as detail_row_number

FROM product_base pb
    -- 核心表连接
    LEFT JOIN supplier_info si ON (pb.product_id % 500) + 1 = si.supplier_id
    CROSS JOIN community_store cs
    LEFT JOIN category_management cm ON pb.category_name = cm.category_name
    LEFT JOIN inventory_management im ON pb.product_id = im.product_id AND cs.store_id = im.store_id
    LEFT JOIN pricing_strategy ps ON pb.product_id = ps.product_id
    
    -- 销售相关表连接
    LEFT JOIN sales_order so ON cs.store_id = so.store_id
    LEFT JOIN customer_info ci ON so.customer_id = ci.customer_id
    LEFT JOIN delivery_info di ON so.order_id = di.order_id
    
    -- 促销和营销表连接
    LEFT JOIN promotion_activity pa ON pa.promotion_status = '进行中' AND pb.product_id % 5 = 0
    LEFT JOIN marketing_effect me ON pa.promotion_id = me.promotion_id AND pb.product_id = me.product_id
    
    -- 商品相关表连接
    LEFT JOIN product_review pr ON pb.product_id = pr.product_id
    LEFT JOIN purchase_management pm ON pb.product_id = pm.product_id
    LEFT JOIN loss_management lm ON pb.product_id = lm.product_id AND cs.store_id = lm.store_id
    
    -- 客户和会员表连接
    LEFT JOIN member_management mm ON ci.customer_id = mm.customer_id
    
    -- 分析相关表连接
    LEFT JOIN seasonal_sales ss ON pb.product_id = ss.product_id
    LEFT JOIN competitor_price cp ON pb.product_id = cp.product_id
    LEFT JOIN quality_inspection qi ON pb.product_id = qi.product_id AND si.supplier_id = qi.supplier_id
    
    -- 物流和财务表连接
    LEFT JOIN supply_chain_logistics scl ON pm.purchase_id = scl.purchase_id
    LEFT JOIN financial_settlement fs ON so.order_id = fs.order_id

-- 数据过滤和排序
WHERE pb.product_id IS NOT NULL
ORDER BY 
    pb.category_name,
    cs.city_level,
    pb.product_id,
    cs.store_id
    
-- 限制结果集为50000行
LIMIT 50000;

-- =====================================================
-- 数据统计查询
-- =====================================================

-- 统计各品类商品数量分布
SELECT 
    category_name,
    COUNT(*) as product_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM product_base), 2) as percentage
FROM product_base 
GROUP BY category_name
ORDER BY product_count DESC;

-- 统计各城市等级门店分布
SELECT 
    city_level,
    COUNT(*) as store_count,
    AVG(daily_customer_flow) as avg_customer_flow
FROM community_store
GROUP BY city_level
ORDER BY store_count DESC;

-- 统计供应商等级分布
SELECT 
    supplier_level,
    COUNT(*) as supplier_count,
    AVG(supplier_rating) as avg_rating
FROM supplier_info
GROUP BY supplier_level
ORDER BY supplier_count DESC;
