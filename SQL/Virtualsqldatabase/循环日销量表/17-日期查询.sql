/*
 * 文件名: 17-日期查询.sql
 * 功能: 日期查询函数集合
 * 描述: 本脚本提供常用的日期查询函数，用于获取各种时间维度的日期，支持业务分析和报表生成
 */

-- 1. 基础日期函数
SELECT 
    GETDATE() AS 当前日期时间,                    -- 获取系统当前日期时间
    CAST(GETDATE() AS DATE) AS 当前日期,          -- 获取系统当前日期（不含时间）
    CAST(GETDATE() AS TIME) AS 当前时间;          -- 获取系统当前时间（不含日期）

-- 2. 本月相关日期
SELECT 
    DATEADD(DAY, -DAY(GETDATE())+1, GETDATE()) AS 本月第一天,  -- 获取本月第一天
    DATEADD(MONTH, DATEDIFF(MONTH, 0, DATEADD(MONTH, 1, GETDATE())), -1) AS 本月最后一天,  -- 获取本月最后一天
    DATEDIFF(DAY, DATEADD(DAY, -DAY(GETDATE())+1, GETDATE()), 
             DATEADD(MONTH, DATEDIFF(MONTH, 0, DATEADD(MONTH, 1, GETDATE())), -1)) + 1 AS 本月天数;  -- 计算本月总天数

-- 3. 本年相关日期
SELECT 
    DATEADD(YEAR, DATEDIFF(YEAR, 0, GETDATE()), 0) AS 本年第一天,  -- 获取本年第一天
    DATEADD(YEAR, DATEDIFF(YEAR, 0, DATEADD(YEAR, 1, GETDATE())), -1) AS 本年最后一天,  -- 获取本年最后一天
    DATEDIFF(DAY, DATEADD(YEAR, DATEDIFF(YEAR, 0, GETDATE()), 0),
             DATEADD(YEAR, DATEDIFF(YEAR, 0, DATEADD(YEAR, 1, GETDATE())), -1)) + 1 AS 本年天数;  -- 计算本年总天数

-- 4. 下年相关日期
SELECT 
    DATEADD(YEAR, DATEDIFF(YEAR, 0, DATEADD(YEAR, 1, GETDATE())), 0) AS 下年第一天,  -- 获取下年第一天
    DATEADD(YEAR, DATEDIFF(YEAR, 0, DATEADD(YEAR, 2, GETDATE())), -1) AS 下年最后一天;  -- 获取下年最后一天

-- 5. 上年相关日期
SELECT 
    DATEADD(YEAR, DATEDIFF(YEAR, 0, DATEADD(YEAR, -1, GETDATE())), 0) AS 上年第一天,  -- 获取上年第一天
    DATEADD(YEAR, DATEDIFF(YEAR, 0, GETDATE()), -1) AS 上年最后一天;  -- 获取上年最后一天

-- 6. 季度相关日期
SELECT 
    DATEADD(QUARTER, DATEDIFF(QUARTER, 0, GETDATE()), 0) AS 本季度第一天,  -- 获取本季度第一天
    DATEADD(QUARTER, DATEDIFF(QUARTER, 0, DATEADD(QUARTER, 1, GETDATE())), -1) AS 本季度最后一天,  -- 获取本季度最后一天
    DATEPART(QUARTER, GETDATE()) AS 当前季度;  -- 获取当前季度（1-4）

-- 7. 周相关日期
SELECT 
    DATEADD(DAY, -DATEPART(WEEKDAY, GETDATE())+1, GETDATE()) AS 本周一,  -- 获取本周一
    DATEADD(DAY, -DATEPART(WEEKDAY, GETDATE())+7, GETDATE()) AS 本周日,  -- 获取本周日
    DATEPART(WEEK, GETDATE()) AS 当前周数;  -- 获取当前是第几周

-- 8. 日期偏移计算
SELECT 
    DATEADD(DAY, -1, GETDATE()) AS 昨天,  -- 获取昨天
    DATEADD(DAY, 1, GETDATE()) AS 明天,   -- 获取明天
    DATEADD(WEEK, -1, GETDATE()) AS 上周同日,  -- 获取上周同日
    DATEADD(WEEK, 1, GETDATE()) AS 下周同日,  -- 获取下周同日
    DATEADD(MONTH, -1, GETDATE()) AS 上月同日,  -- 获取上月同日
    DATEADD(MONTH, 1, GETDATE()) AS 下月同日;  -- 获取下月同日

-- 9. 日期格式化
SELECT 
    CONVERT(VARCHAR(10), GETDATE(), 23) AS 标准日期格式,  -- 格式：YYYY-MM-DD
    CONVERT(VARCHAR(10), GETDATE(), 112) AS 紧凑日期格式,  -- 格式：YYYYMMDD
    CONVERT(VARCHAR(20), GETDATE(), 120) AS 标准日期时间格式;  -- 格式：YYYY-MM-DD HH:MI:SS

-- 10. 日期差值计算
SELECT 
    DATEDIFF(DAY, DATEADD(MONTH, -1, GETDATE()), GETDATE()) AS 距上月天数,  -- 计算距离上月的天数
    DATEDIFF(DAY, GETDATE(), DATEADD(MONTH, 1, GETDATE())) AS 距下月天数,  -- 计算距离下月的天数
    DATEDIFF(WEEK, DATEADD(MONTH, -1, GETDATE()), GETDATE()) AS 距上月周数,  -- 计算距离上月的周数
    DATEDIFF(MONTH, DATEADD(YEAR, -1, GETDATE()), GETDATE()) AS 距上年月数;  -- 计算距离上年的月数

/*
 * 代码优化说明：
 * 1. 添加了详细的文件头注释，说明脚本功能和目的
 * 2. 将日期函数按功能分类，提高代码可读性
 * 3. 为每个函数添加了详细的中文注释，说明其用途
 * 4. 新增了更多实用的日期函数，如季度、周相关函数
 * 5. 添加了日期格式化和差值计算函数
 * 6. 优化了代码结构，使用SELECT语句组合相关函数
 * 7. 添加了代码优化说明，便于后续维护
 */
