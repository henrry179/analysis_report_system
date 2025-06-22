-- 查询所有交易员及其对应的交易记录
use Tradingdatas;

-- 查询所有交易员及其对应的交易记录
SELECT T.TraderName, TR.TradeDate, TR.Symbol, TR.Quantity, TR.Price
FROM Traders T
JOIN Trades TR ON T.TraderID = TR.TraderID
ORDER BY T.TraderName, TR.TradeDate;
-- 连接 Traders 表和 Trades 表，根据 TraderID 关联，按交易员姓名和交易日期排序

-- 查询交易员ID为1的所有交易记录，并按交易日期排序
SELECT TR.TradeID, TR.TradeDate, TR.Symbol, TR.Quantity, TR.Price
FROM Trades TR
WHERE TR.TraderID = 1
ORDER BY TR.TradeDate DESC;
-- 查询交易员ID为1的所有交易记录，并按交易日期降序排序

-- 查询每个交易员的总交易数量和总交易金额
SELECT T.TraderName, SUM(TR.Quantity) AS TotalQuantity, SUM(TR.Quantity * TR.Price) AS TotalAmount
FROM Traders T
JOIN Trades TR ON T.TraderID = TR.TraderID
GROUP BY T.TraderName
ORDER BY TotalAmount DESC;
-- 连接 Traders 表和 Trades 表，根据 TraderID 关联，计算每个交易员的总交易数量和总交易金额，并按总金额降序排序

-- 查询每个市场的总交易量和平均价格
SELECT TR.Market, SUM(TR.Quantity) AS TotalVolume, AVG(TR.Price) AS AveragePrice
FROM Trades TR
GROUP BY TR.Market
ORDER BY TotalVolume DESC;
-- 按市场分组，计算总交易量和平均价格，并按总交易量降序排序

-- 查询交易金额大于10000的交易记录及其交易员信息
SELECT TR.TradeID, TR.TradeDate, TR.Symbol, TR.Quantity, TR.Price, TR.Quantity * TR.Price AS TotalAmount, T.TraderName
FROM Trades TR
JOIN Traders T ON TR.TraderID = T.TraderID
WHERE TR.TradeID IN (
    SELECT TradeID
    FROM Trades
    WHERE Quantity * Price > 10000
)
ORDER BY TR.TradeDate DESC;

-- 使用子查询筛选交易金额大于10000的交易记录，并获取对应的交易员信息，按交易日期降序排序

-- 查询每个交易员的每月平均交易数量
SELECT T.TraderName, YEAR(TR.TradeDate) AS TradeYear, MONTH(TR.TradeDate) AS TradeMonth, AVG(TR.Quantity) OVER (PARTITION BY T.TraderName, YEAR(TR.TradeDate), MONTH(TR.TradeDate)) AS AvgMonthlyQuantity
FROM Trades TR
JOIN Traders T ON TR.TraderID = T.TraderID
ORDER BY T.TraderName, TradeYear, TradeMonth;

-- 连接 Traders 表和 Trades 表，根据 TraderID 关联，使用窗口函数计算每个交易员每月的平均交易数量，并按交易员姓名、年份和月份排序

-- 查询每个客户的账户总余额和交易次数
SELECT C.ClientName, SUM(A.Balance) AS TotalBalance, COUNT(T.TransactionID) AS TotalTransactions
FROM Clients C
JOIN Accounts A ON C.ClientID = A.ClientID
LEFT JOIN Transactions T ON A.AccountID = T.AccountID
GROUP BY C.ClientName
ORDER BY TotalBalance DESC;

-- 连接 Clients 表和 Accounts 表，根据 ClientID 关联，再左连接 Transactions 表，计算每个客户的账户总余额和交易次数，并按总余额降序排序

-- 查询每笔交易的盈亏情况
SELECT TR.TradeID, TR.TradeDate, TR.Symbol, TR.Quantity, TR.Price, 
    CASE 
        WHEN TP.PnL > 0 THEN 'Profit'
        WHEN TP.PnL < 0 THEN 'Loss'
        ELSE 'Break Even'
    END AS PnLStatus
FROM Trades TR
JOIN TradePerformance TP ON TR.TradeID = TP.TradeID
ORDER BY TR.TradeDate;

-- 连接 Trades 表和 TradePerformance 表，根据 TradeID 关联，使用 CASE 语句判断每笔交易的盈亏情况，并按交易日期排序

-- 查询每个交易员的累计交易金额
SELECT TR.TraderID, T.TraderName, TR.TradeDate, TR.Quantity * TR.Price AS TradeAmount,
       SUM(TR.Quantity * TR.Price) OVER (PARTITION BY TR.TraderID ORDER BY TR.TradeDate) AS CumulativeTradeAmount
FROM Trades TR
JOIN Traders T ON TR.TraderID = T.TraderID
ORDER BY TR.TraderID, TR.TradeDate;

-- 连接 Trades 表和 Traders 表，根据 TraderID 关联，使用窗口函数计算每个交易员的累计交易金额，并按 TraderID 和交易日期排序

-- 查询每个交易员每月的交易总量和交易总金额
WITH MonthlyTrades AS (
    SELECT TR.TraderID, T.TraderName, YEAR(TR.TradeDate) AS TradeYear, MONTH(TR.TradeDate) AS TradeMonth,
           SUM(TR.Quantity) AS TotalQuantity, SUM(TR.Quantity * TR.Price) AS TotalAmount
    FROM Trades TR
    JOIN Traders T ON TR.TraderID = T.TraderID
    GROUP BY TR.TraderID, T.TraderName, YEAR(TR.TradeDate), MONTH(TR.TradeDate)
)
SELECT * FROM MonthlyTrades
ORDER BY TraderID, TradeYear, TradeMonth;

-- 使用 CTE 计算每个交易员每月的交易总量和交易总金额，并按 TraderID、年份和月份排序

-- 使用递归 CTE 查询所有交易及其关联的交易记录，并按 TradeID 排序

-- 动态生成和执行SQL语句
DECLARE @TableName NVARCHAR(100) = 'Trades';
DECLARE @SQL NVARCHAR(MAX);

SET @SQL = N'SELECT * FROM ' + QUOTENAME(@TableName);
EXEC sp_executesql @SQL;

-- 动态生成查询 Trades 表的 SQL 语句，并执行

-- 查询每个交易员的交易数量排名和累计交易金额
SELECT TR.TraderID, T.TraderName, 
        COUNT(*) OVER (PARTITION BY TR.TraderID) AS TradeCount,
       SUM(TR.Quantity * TR.Price) OVER (PARTITION BY TR.TraderID ORDER BY TR.TradeDate) AS CumulativeTradeAmount,
       RANK() OVER (ORDER BY COUNT(*) OVER (PARTITION BY TR.TraderID) DESC) AS TradeRank
FROM Trades TR
JOIN Traders T ON TR.TraderID = T.TraderID
ORDER BY TradeRank, TR.TraderID;

-- 使用窗口函数计算每个交易员的交易数量、累计交易金额，并按交易数量进行排名，最终按排名和 TraderID 排序

-- 查询每个交易员在特定日期范围内的最大单笔交易金额
SELECT T.TraderID, T.TraderName, (
    SELECT MAX(TR.Quantity * TR.Price)
    FROM Trades TR
    WHERE TR.TraderID = T.TraderID AND TR.TradeDate BETWEEN '2023-01-01' AND '2023-12-31'
) AS MaxTradeAmount
FROM Traders T
ORDER BY MaxTradeAmount DESC;

-- 使用子查询计算每个交易员在特定日期范围内的最大单笔交易金额，并按最大交易金额降序排序

-- 查询每个交易员的盈利和亏损交易总额
SELECT T.TraderID, T.TraderName,
       SUM(CASE WHEN TP.PnL > 0 THEN TP.PnL ELSE 0 END) AS TotalProfit,
       SUM(CASE WHEN TP.PnL < 0 THEN TP.PnL ELSE 0 END) AS TotalLoss
FROM Traders T
JOIN Trades TR ON T.TraderID = TR.TraderID
JOIN TradePerformance TP ON TR.TradeID = TP.TradeID
GROUP BY T.TraderID, T.TraderName
ORDER BY TotalProfit DESC;

-- 这些查询操作结合了CTE、多表关联、聚合函数、开窗函数、日期查询、过滤和条件判断等多个高级SQL操作，能够提供全面的交易数据分析。

-- 示例1：计算每个交易员的年度交易表现
-- 1. **TraderTradeSummary**：计算每个交易员的年度交易表现，包括盈利和亏损交易数量、总交易金额和总盈亏。
-- 2. **RankedTraderSummary**：基于交易表现数据，对每个交易员按年度进行排名。

WITH TraderTradeSummary AS (
    SELECT 
        T.TraderID,
        T.TraderName,
        YEAR(TR.TradeDate) AS TradeYear,
        SUM(CASE WHEN TP.PnL > 0 THEN 1 ELSE 0 END) AS ProfitableTrades,
        SUM(CASE WHEN TP.PnL < 0 THEN 1 ELSE 0 END) AS LossMakingTrades,
        SUM(TR.Quantity * TR.Price) AS TotalTradeAmount,
        SUM(TP.PnL) AS TotalPnL
    FROM 
        Traders T
    JOIN 
        Trades TR ON T.TraderID = TR.TraderID
    JOIN 
        TradePerformance TP ON TR.TradeID = TP.TradeID
    WHERE 
        TR.TradeDate BETWEEN '2023-01-01' AND '2023-12-31'
    GROUP BY 
        T.TraderID, T.TraderName, YEAR(TR.TradeDate)
),
RankedTraderSummary AS (
    SELECT 
        TTS.*,
        RANK() OVER (PARTITION BY TTS.TradeYear ORDER BY TTS.TotalPnL DESC) AS PnLRank,
        RANK() OVER (PARTITION BY TTS.TradeYear ORDER BY TTS.ProfitableTrades DESC) AS ProfitableTradesRank,
        RANK() OVER (PARTITION BY TTS.TradeYear ORDER BY TTS.LossMakingTrades ASC) AS LossMakingTradesRank
    FROM 
        TraderTradeSummary TTS
)
SELECT 
    * 
FROM 
    RankedTraderSummary
ORDER BY 
    TradeYear, PnLRank;

-- 示例2：计算每个交易员每个月的平均交易量和总交易额
-- 3. **MonthlyTradeSummary**：计算每个交易员每个月的平均交易量和总交易额。
WITH MonthlyTradeSummary AS (
    SELECT 
        T.TraderID,
        T.TraderName,
        DATEPART(YEAR, TR.TradeDate) AS TradeYear,
        DATEPART(MONTH, TR.TradeDate) AS TradeMonth,
        AVG(TR.Quantity) AS AvgQuantity,
        SUM(TR.Quantity * TR.Price) AS TotalTradeAmount
    FROM 
        Traders T
    JOIN 
        Trades TR ON T.TraderID = TR.TraderID
    GROUP BY 
        T.TraderID, T.TraderName, DATEPART(YEAR, TR.TradeDate), DATEPART(MONTH, TR.TradeDate)
)
SELECT 
    * 
FROM 
    MonthlyTradeSummary
ORDER BY 
    TradeYear, TradeMonth, TraderID;

-- 示例3：计算每个交易员的持仓信息和风险指标
-- 4. **PositionRiskSummary**：计算每个交易员的持仓信息和风险指标，包括VaR、Beta和Sharpe Ratio。
WITH PositionRiskSummary AS (
    SELECT 
        P.TraderID,
        T.TraderName,
        P.Symbol,
        P.Quantity,
        P.AveragePrice,
        P.MarketValue,
        RM.VaR,
        RM.Beta,
        RM.SharpeRatio
    FROM 
        Positions P
    JOIN 
        Traders T ON P.TraderID = T.TraderID
    JOIN 
        RiskMetrics RM ON P.TraderID = RM.TraderID
)
SELECT 
    * 
FROM 
    PositionRiskSummary
ORDER BY 
    TraderID, Symbol;


-- 示例4：计算每个交易员的年度交易手续费和分红
-- 5. **AnnualFeeDividendSummary**：计算每个交易员的年度交易手续费和分红。
WITH AnnualFeeDividendSummary AS (
    SELECT 
        T.TraderID,
        T.TraderName,
        YEAR(TR.TradeDate) AS TradeYear,
        SUM(F.FeeAmount) AS TotalFees,
        SUM(D.DividendAmount) AS TotalDividends
    FROM 
        Traders T
    JOIN 
        Trades TR ON T.TraderID = TR.TraderID
    JOIN 
        Fees F ON TR.TradeID = F.TransactionID
    JOIN 
        Dividends D ON TR.TraderID = D.AccountID
    WHERE 
        TR.TradeDate BETWEEN '2023-01-01' AND '2023-12-31'
    GROUP BY 
        T.TraderID, T.TraderName, YEAR(TR.TradeDate)
)
SELECT 
    * 
FROM 
    AnnualFeeDividendSummary
ORDER BY 
    TradeYear, TraderID;

-- 示例5：计算每个交易员的月度交易表现，包括收益率和排名
-- 6. **MonthlyPerformance**：计算每个交易员的月度交易表现，包括收益率和排名。
WITH MonthlyPerformance AS (
    SELECT 
        T.TraderID,
        T.TraderName,
        DATEPART(YEAR, TR.TradeDate) AS TradeYear,
        DATEPART(MONTH, TR.TradeDate) AS TradeMonth,
        SUM(TP.PnL) AS TotalPnL,
        AVG(TP.ReturnRate) AS AvgReturnRate,
        ROW_NUMBER() OVER (PARTITION BY DATEPART(YEAR, TR.TradeDate), DATEPART(MONTH, TR.TradeDate) ORDER BY SUM(TP.PnL) DESC) AS PnLRank
    FROM 
        Traders T
    JOIN 
        Trades TR ON T.TraderID = TR.TraderID
    JOIN 
        TradePerformance TP ON TR.TradeID = TP.TradeID
    GROUP BY 
        T.TraderID, T.TraderName, DATEPART(YEAR, TR.TradeDate), DATEPART(MONTH, TR.TradeDate)
)
SELECT 
    * 
FROM 
    MonthlyPerformance
ORDER BY 
    TradeYear, TradeMonth, PnLRank;

-- 以下是对上述各个示例的代码逻辑解释：

-- 示例6：计算每个交易员的年度交易频率和总交易量


WITH AnnualTradeFrequency AS (
    SELECT 
        T.TraderID,                          -- 选择交易员ID
        T.TraderName,                        -- 选择交易员姓名
        YEAR(TR.TradeDate) AS TradeYear,     -- 提取交易年份
        COUNT(TR.TradeID) AS TradeCount,     -- 计算交易次数
        SUM(TR.Quantity) AS TotalQuantity    -- 计算总交易量
    FROM 
        Traders T
    JOIN 
        Trades TR ON T.TraderID = TR.TraderID
    GROUP BY 
        T.TraderID, T.TraderName, YEAR(TR.TradeDate)   -- 按交易员和年份分组
)
SELECT 
    * 
FROM 
    AnnualTradeFrequency
ORDER BY 
    TradeYear, TradeCount DESC;              -- 按年份和交易次数排序

/**

**逻辑解释：**
1. 使用CTE（Common Table Expression）计算每个交易员每年的交易频率和总交易量。
2. 通过`JOIN`将交易员表和交易表关联，按交易员ID和交易年份分组。
3. 计算每年的交易次数和总交易量。
4. 最终结果按年份和交易次数降序排序。

*/

-- 示例7：计算每个交易员每个季度的盈亏和平均持有期
WITH QuarterlyPerformance AS (
    SELECT 
        T.TraderID,                              -- 选择交易员ID
        T.TraderName,                            -- 选择交易员姓名
        YEAR(TR.TradeDate) AS TradeYear,         -- 提取交易年份
        DATEPART(QUARTER, TR.TradeDate) AS TradeQuarter,  -- 提取交易季度
        SUM(TP.PnL) AS TotalPnL,                 -- 计算总盈亏
        AVG(TP.HoldingPeriod) AS AvgHoldingPeriod -- 计算平均持有期
    FROM 
        Traders T
    JOIN 
        Trades TR ON T.TraderID = TR.TraderID
    JOIN 
        TradePerformance TP ON TR.TradeID = TP.TradeID
    GROUP BY 
        T.TraderID, T.TraderName, YEAR(TR.TradeDate), DATEPART(QUARTER, TR.TradeDate)
)
SELECT 
    * 
FROM 
    QuarterlyPerformance
ORDER BY 
    TradeYear, TradeQuarter, TotalPnL DESC;   -- 按年份、季度和总盈亏排序

/**
**逻辑解释：**
1. 通过CTE计算每个交易员每个季度的总盈亏和平均持有期。
2. 通过多次`JOIN`关联交易员表、交易表和交易表现表。
3. 按交易员ID、交易年份和季度分组，计算总盈亏和平均持有期。
4. 最终结果按年份、季度和总盈亏降序排序。
*/

-- 示例8：计算每个交易员每月的平均交易成本和总交易金额

WITH MonthlyTradeCost AS (
    SELECT 
        T.TraderID,                                  -- 选择交易员ID
        T.TraderName,                                -- 选择交易员姓名
        DATEPART(YEAR, TR.TradeDate) AS TradeYear,   -- 提取交易年份
        DATEPART(MONTH, TR.TradeDate) AS TradeMonth, -- 提取交易月份
        AVG(TR.Price * TR.Quantity) AS AvgTradeCost, -- 计算平均交易成本
        SUM(TR.Price * TR.Quantity) AS TotalTradeAmount -- 计算总交易金额
    FROM 
        Traders T
    JOIN 
        Trades TR ON T.TraderID = TR.TraderID
    GROUP BY 
        T.TraderID, T.TraderName, DATEPART(YEAR, TR.TradeDate), DATEPART(MONTH, TR.TradeDate)
)
SELECT 
    * 
FROM 
    MonthlyTradeCost
ORDER BY 
    TradeYear, TradeMonth, TotalTradeAmount DESC; -- 按年份、月份和总交易金额排序

/**
**逻辑解释：**
1. 使用CTE计算每个交易员每月的平均交易成本和总交易金额。
2. 通过`JOIN`关联交易员表和交易表。
3. 按交易员ID、交易年份和月份分组，计算平均交易成本和总交易金额。
4. 最终结果按年份、月份和总交易金额降序排序。
*/

-- 示例9：计算每个交易员每年的最大单笔交易盈亏

WITH MaxTradePnL AS (
    SELECT 
        T.TraderID,                                  -- 选择交易员ID
        T.TraderName,                                -- 选择交易员姓名
        YEAR(TR.TradeDate) AS TradeYear,             -- 提取交易年份
        MAX(TP.PnL) AS MaxPnL,                       -- 计算最大盈亏
        MIN(TP.PnL) AS MinPnL                        -- 计算最小盈亏
    FROM 
        Traders T
    JOIN 
        Trades TR ON T.TraderID = TR.TraderID
    JOIN 
        TradePerformance TP ON TR.TradeID = TP.TradeID
    GROUP BY 
        T.TraderID, T.TraderName, YEAR(TR.TradeDate)
)
SELECT 
    * 
FROM 
    MaxTradePnL
ORDER BY 
    TradeYear, MaxPnL DESC;                         -- 按年份和最大盈亏排序

/**
**逻辑解释：**
1. 使用CTE计算每个交易员每年的最大和最小单笔交易盈亏。
2. 通过多次`JOIN`关联交易员表、交易表和交易表现表。
3. 按交易员ID和交易年份分组，计算最大和最小盈亏。
4. 最终结果按年份和最大盈亏降序排序。
*/

-- 示例10：计算每个交易员的持仓和风险评估信息

WITH PositionRiskAssessment AS (
    SELECT 
        P.TraderID,                                    -- 选择交易员ID
        T.TraderName,                                  -- 选择交易员姓名
        P.Symbol,                                      -- 选择股票代码
        P.Quantity,                                    -- 选择持仓数量
        P.AveragePrice,                                -- 选择平均持仓价格
        P.MarketValue,                                 -- 选择市场价值
        RM.VaR,                                        -- 选择风险价值
        RM.Beta,                                       -- 选择贝塔值
        RM.SharpeRatio,                                -- 选择夏普比率
        (P.MarketValue * RM.Beta) AS AdjustedMarketValue -- 计算调整后市场价值
    FROM 
        Positions P
    JOIN 
        Traders T ON P.TraderID = T.TraderID
    JOIN 
        RiskMetrics RM ON P.TraderID = RM.TraderID
)
SELECT 
    * 
FROM 
    PositionRiskAssessment
ORDER BY 
    TraderID, Symbol;                                 -- 按交易员ID和股票代码排序

/**
**逻辑解释：**
1. 使用CTE计算每个交易员的持仓和风险评估信息。
2. 通过多次`JOIN`关联持仓表、交易员表和风险度量表。
3. 计算调整后的市场价值。
4. 最终结果按交易员ID和股票代码排序。
*/

-- 示例11：计算每个交易员的合规问题统计

WITH ComplianceIssues AS (
    SELECT 
        C.TraderID,                                   -- 选择交易员ID
        T.TraderName,                                 -- 选择交易员姓名
        COUNT(C.ComplianceID) AS IssueCount,          -- 计算合规问题数量
        SUM(CASE WHEN C.Status = 'Resolved' THEN 1 ELSE 0 END) AS ResolvedIssues, -- 计算已解决问题数量
        SUM(CASE WHEN C.Status = 'Open' THEN 1 ELSE 0 END) AS OpenIssues         -- 计算未解决问题数量
    FROM 
        Compliance C
    JOIN 
        Traders T ON C.TraderID = T.TraderID
    GROUP BY 
        C.TraderID, T.TraderName
)
SELECT 
    * 
FROM 
    ComplianceIssues
ORDER BY 
    IssueCount DESC, ResolvedIssues DESC;              -- 按问题数量和已解决问题数量排序

/**
**逻辑解释：**
1. 使用CTE计算每个交易员的合规问题统计。
2. 通过`JOIN`关联合规表和交易员表。
3. 计算每个交易员的合规问题数量、已解决问题数量和未解决问题数量。
4. 最终结果按问题数量和已解决问题数量降序排序。
*/

-- 示例12：计算每个客户账户的交易活动统计

WITH AccountActivity AS (
    SELECT 
        A.ClientID,                                   -- 选择客户ID
        C.ClientName,                                 -- 选择客户姓名
        A.AccountID,                                  -- 选择账户ID
        COUNT(T.TransactionID) AS TransactionCount,   -- 计算交易数量
        SUM(T.Amount) AS TotalAmount,                 -- 计算总交易金额
        AVG(T.Amount) AS AvgAmount                    -- 计算平均交易金额
    FROM 
        Accounts A
    JOIN 
        Clients C ON A.ClientID = C.ClientID
    JOIN 
        Transactions T ON

 A.AccountID = T.AccountID
    GROUP BY 
        A.ClientID, C.ClientName, A.AccountID
)
SELECT 
    * 
FROM 
    AccountActivity
ORDER BY 
    TransactionCount DESC, TotalAmount DESC;           -- 按交易数量和总交易金额排序

/**
**逻辑解释：**
1. 使用CTE计算每个客户账户的交易活动统计。
2. 通过多次`JOIN`关联账户表、客户表和交易表。
3. 计算每个账户的交易数量、总交易金额和平均交易金额。
4. 最终结果按交易数量和总交易金额降序排序。
*/

-- 示例14：计算每个交易员的持仓分布和市场价值

WITH PositionDistribution AS (
    SELECT 
        P.TraderID,                                   -- 选择交易员ID
        T.TraderName,                                 -- 选择交易员姓名
        P.Symbol,                                     -- 选择股票代码
        P.Quantity,                                   -- 选择持仓数量
        P.MarketValue,                                -- 选择市场价值
        SUM(P.MarketValue) OVER (PARTITION BY P.TraderID) AS TotalMarketValue, -- 计算总市场价值
        (P.MarketValue / SUM(P.MarketValue) OVER (PARTITION BY P.TraderID)) * 100 AS MarketValuePercentage -- 计算市场价值百分比
    FROM 
        Positions P
    JOIN 
        Traders T ON P.TraderID = T.TraderID
)
SELECT 
    * 
FROM 
    PositionDistribution
ORDER BY 
    TraderID, MarketValuePercentage DESC;              -- 按交易员ID和市场价值百分比排序

/**
**逻辑解释：**
1. 使用CTE计算每个交易员的持仓分布和市场价值百分比。
2. 通过`JOIN`关联持仓表和交易员表。
3. 使用窗口函数计算每个交易员的总市场价值和单个持仓的市场价值百分比。
4. 最终结果按交易员ID和市场价值百分比降序排序。
*/

-- 示例15：计算每个交易员的交易回报率和排名

WITH TraderReturnRate AS (
    SELECT 
        T.TraderID,                                   -- 选择交易员ID
        T.TraderName,                                 -- 选择交易员姓名
        YEAR(TR.TradeDate) AS TradeYear,              -- 提取交易年份
        AVG(TP.ReturnRate) AS AvgReturnRate,          -- 计算平均回报率
        RANK() OVER (PARTITION BY YEAR(TR.TradeDate) ORDER BY AVG(TP.ReturnRate) DESC) AS ReturnRateRank -- 按年份计算回报率排名
    FROM 
        Traders T
    JOIN 
        Trades TR ON T.TraderID = TR.TraderID
    JOIN 
        TradePerformance TP ON TR.TradeID = TP.TradeID
    GROUP BY 
        T.TraderID, T.TraderName, YEAR(TR.TradeDate)
)
SELECT 
    * 
FROM 
    TraderReturnRate
ORDER BY 
    TradeYear, ReturnRateRank;                          -- 按年份和回报率排名排序

/**
**逻辑解释：**
1. 使用CTE计算每个交易员每年的平均回报率和排名。
2. 通过多次`JOIN`关联交易员表、交易表和交易表现表。
3. 使用窗口函数按年份计算回报率排名。
4. 最终结果按年份和回报率排名排序。
*/

-- 示例16：计算每个交易员每月的盈利交易和亏损交易

WITH MonthlyTradeOutcome AS (
    SELECT 
        T.TraderID,                                  -- 选择交易员ID
        T.TraderName,                                -- 选择交易员姓名
        DATEPART(YEAR, TR.TradeDate) AS TradeYear,   -- 提取交易年份
        DATEPART(MONTH, TR.TradeDate) AS TradeMonth, -- 提取交易月份
        SUM(CASE WHEN TP.PnL > 0 THEN 1 ELSE 0 END) AS ProfitableTrades, -- 计算盈利交易数量
        SUM(CASE WHEN TP.PnL < 0 THEN 1 ELSE 0 END) AS LossMakingTrades  -- 计算亏损交易数量
    FROM 
        Traders T
    JOIN 
        Trades TR ON T.TraderID = TR.TraderID
    JOIN 
        TradePerformance TP ON TR.TradeID = TP.TradeID
    GROUP BY 
        T.TraderID, T.TraderName, DATEPART(YEAR, TR.TradeDate), DATEPART(MONTH, TR.TradeDate)
)
SELECT 
    * 
FROM 
    MonthlyTradeOutcome
ORDER BY 
    TradeYear, TradeMonth, ProfitableTrades DESC;      -- 按年份、月份和盈利交易数量排序

/**
**逻辑解释：**
1. 使用CTE计算每个交易员每月的盈利交易和亏损交易数量。
2. 通过多次`JOIN`关联交易员表、交易表和交易表现表。
3. 使用条件判断计算盈利和亏损交易数量。
4. 最终结果按年份、月份和盈利交易数量降序排序。

这些解释展示了如何使用CTE来编写复杂的多维度、多表关联和高级计算操作的SQL查询，每个查询示例都包含聚合函数、开窗函数、日期查询、过滤和条件判断等多个SQL操作。
*/


