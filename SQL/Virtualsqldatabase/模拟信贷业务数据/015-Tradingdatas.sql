
-- 下面是给以上示例数据报表的中文注释，包括报表名称和数据字段的中文注释：
/**

### 1.Traders 表（交易员表）

- `TraderID`：交易员ID
- `TraderName`：交易员姓名
- `Department`：部门
- `JoinDate`：加入日期
- `Status`：状态

### 2.Trades 表（交易表）

- `TradeID`：交易ID
- `TraderID`：交易员ID
- `TradeDate`：交易日期
- `BuySell`：买卖类型
- `Quantity`：数量
- `Price`：价格
- `Symbol`：股票代码
- `Market`：市场
- `TradeType`：交易类型

### 3.TradeDetails 表（交易细节表）

- `DetailID`：细节ID
- `TradeID`：交易ID
- `SettlementDate`：结算日期
- `Commission`：佣金
- `NetAmount`：净金额
- `Tax`：税

### 4.TradePerformance 表（交易表现表）

- `PerformanceID`：表现ID
- `TradeID`：交易ID
- `PnL`：盈亏
- `ReturnRate`：回报率
- `HoldingPeriod`：持有期

### 5.MarketData 表（市场数据表）

- `MarketDataID`：市场数据ID
- `Symbol`：股票代码
- `TradeDate`：交易日期
- `OpenPrice`：开盘价
- `HighPrice`：最高价
- `LowPrice`：最低价
- `ClosePrice`：收盘价
- `Volume`：成交量

### 6.Orders 表（订单表）

- `OrderID`：订单ID
- `TraderID`：交易员ID
- `Symbol`：股票代码
- `OrderDate`：订单日期
- `OrderType`：订单类型
- `Quantity`：数量
- `Price`：价格
- `Status`：状态

### 7.Positions 表（持仓表）

- `PositionID`：持仓ID
- `TraderID`：交易员ID
- `Symbol`：股票代码
- `Quantity`：数量
- `AveragePrice`：平均价格
- `MarketValue`：市值

### 8.RiskMetrics 表（风险度量表）

- `RiskMetricID`：风险度量ID
- `TraderID`：交易员ID
- `VaR`：价值-at-Risk
- `Beta`：贝塔
- `SharpeRatio`：夏普比率

### 9.Compliance 表（合规表）

- `ComplianceID`：合规ID
- `TraderID`：交易员ID
- `AuditDate`：审计日期
- `IssueDescription`：问题描述
- `Resolution`：解决方案
- `Status`：状态

### 10.Clients 表（客户表）

- `ClientID`：客户ID
- `ClientName`：客户姓名
- `ClientType`：客- `ClientType`：客户类型
- `JoinDate`：加入日期
- `Status`：状态

### 11.Accounts 表（账户表）

- `AccountID`：账户ID
- `ClientID`：客户ID
- `AccountType`：账户类型
- `Balance`：余额
- `Status`：状态

### 12.Transactions 表（交易记录表）

- `TransactionID`：交易记录ID
- `AccountID`：账户ID
- `TransactionDate`：交易日期
- `Amount`：金额
- `TransactionType`：交易类型

### 13.Fees 表（费用表）

- `FeeID`：费用ID
- `TransactionID`：交易记录ID
- `FeeAmount`：费用金额
- `FeeType`：费用类型

### 14.Dividends 表（分红表）

- `DividendID`：分红ID
- `AccountID`：账户ID
- `Symbol`：股票代码
- `DividendDate`：分红日期
- `DividendAmount`：分红金额

### 15.InterestRates 表（利率表）

- `RateID`：利率ID
- `RateDate`：利率日期
- `Rate`：利率
- `Description`：描述

### 16.Strategies 表（策略表）

- `StrategyID`：策略ID
- `StrategyName`：策略名称
- `Description`：描述
- `RiskLevel`：风险等级

### 17.Reports 表（报告表）

- `ReportID`：报告ID
- `TraderID`：交易员ID
- `ReportDate`：报告日期
- `ReportType`：报告类型
- `Content`：内容

### 18.Benchmarks 表（基准表）

- `BenchmarkID`：基准ID
- `BenchmarkDate`：基准日期
- `BenchmarkValue`：基准值
- `Description`：描述

### 19.Allocations 表（分配表）

- `AllocationID`：分配ID
- `TraderID`：交易员ID
- `Symbol`：股票代码
- `AllocationDate`：分配日期
- `AllocationAmount`：分配金额

### 20.Portfolios 表（投资组合表）

- `PortfolioID`：投资组合ID
- `TraderID`：交易员ID
- `PortfolioName`：投资组合名称
- `CreationDate`：创建日期
- `Status`：状态

*/

-- 创建数据库Tradingdatas，并使用该数据库。
create database Tradingdatas;
use Tradingdatas;

-- 通过这些报表和字段的中文注释，可以帮助您更好地理解对冲基金交易员的交易数据报表。

-- 1.Traders 表（交易员表）
CREATE TABLE Traders (
    TraderID INT PRIMARY KEY,
    TraderName VARCHAR(100),
    Department VARCHAR(100),
    JoinDate DATE,
    Status VARCHAR(10)
);

-- 2.Trades 表（交易表）
CREATE TABLE Trades (
    TradeID INT PRIMARY KEY,
    TraderID INT,
    TradeDate DATE,
    BuySell VARCHAR(10),
    Quantity INT,
    Price DECIMAL(10, 2),
    Symbol VARCHAR(10),
    Market VARCHAR(50),
    TradeType VARCHAR(50),
    FOREIGN KEY (TraderID) REFERENCES Traders(TraderID)
);

-- 3.TradeDetails 表（交易细节表）
CREATE TABLE TradeDetails (
    DetailID INT PRIMARY KEY,
    TradeID INT,
    SettlementDate DATE,
    Commission DECIMAL(10, 2),
    NetAmount DECIMAL(10, 2),
    Tax DECIMAL(10, 2),
    FOREIGN KEY (TradeID) REFERENCES Trades(TradeID)
);

-- 4.TradePerformance 表（交易表现表）
CREATE TABLE TradePerformance (
    PerformanceID INT PRIMARY KEY,
    TradeID INT,
    PnL DECIMAL(10, 2),
    ReturnRate DECIMAL(5, 2),
    HoldingPeriod INT,
    FOREIGN KEY (TradeID) REFERENCES Trades(TradeID)
);

-- 5.MarketData 表（市场数据表）
CREATE TABLE MarketData (
    MarketDataID INT PRIMARY KEY,
    Symbol VARCHAR(10),
    TradeDate DATE,
    OpenPrice DECIMAL(10, 2),
    HighPrice DECIMAL(10, 2),
    LowPrice DECIMAL(10, 2),
    ClosePrice DECIMAL(10, 2),
    Volume INT
);

-- 6.Orders 表（订单表）
CREATE TABLE Orders (
    OrderID INT PRIMARY KEY,
    TraderID INT,
    Symbol VARCHAR(10),
    OrderDate DATE,
    OrderType VARCHAR(50),
    Quantity INT,
    Price DECIMAL(10, 2),
    Status VARCHAR(20),
    FOREIGN KEY (TraderID) REFERENCES Traders(TraderID)
);

-- 7.Positions 表（持仓表）
CREATE TABLE Positions (
    PositionID INT PRIMARY KEY,
    TraderID INT,
    Symbol VARCHAR(10),
    Quantity INT,
    AveragePrice DECIMAL(10, 2),
    MarketValue DECIMAL(10, 2),
    FOREIGN KEY (TraderID) REFERENCES Traders(TraderID)
);

-- 8.RiskMetrics 表（风险度量表）
CREATE TABLE RiskMetrics (
    RiskMetricID INT PRIMARY KEY,
    TraderID INT,
    VaR DECIMAL(10, 2),
    Beta DECIMAL(5, 2),
    SharpeRatio DECIMAL(5, 2),
    FOREIGN KEY (TraderID) REFERENCES Traders(TraderID)
);

-- 9.Compliance 表（合规表）
CREATE TABLE Compliance (
    ComplianceID INT PRIMARY KEY,
    TraderID INT,
    AuditDate DATE,
    IssueDescription VARCHAR(255),
    Resolution VARCHAR(255),
    Status VARCHAR(20),
    FOREIGN KEY (TraderID) REFERENCES Traders(TraderID)
);

-- 10.Clients 表（客户表）
CREATE TABLE Clients (
    ClientID INT PRIMARY KEY,
    ClientName VARCHAR(100),
    ClientType VARCHAR(50),
    JoinDate DATE,
    Status VARCHAR(20)
);

-- 11.Accounts 表（账户表）
CREATE TABLE Accounts (
    AccountID INT PRIMARY KEY,
    ClientID INT,
    AccountType VARCHAR(50),
    Balance DECIMAL(15, 2),
    Status VARCHAR(20),
    FOREIGN KEY (ClientID) REFERENCES Clients(ClientID)
);

-- 12.Transactions 表（交易记录表）
CREATE TABLE Transactions (
    TransactionID INT PRIMARY KEY,
    AccountID INT,
    TransactionDate DATE,
    Amount DECIMAL(10, 2),
    TransactionType VARCHAR(50),
    FOREIGN KEY (AccountID) REFERENCES Accounts(AccountID)
);

-- 13.Fees 表（费用表）
CREATE TABLE Fees (
    FeeID INT PRIMARY KEY,
    TransactionID INT,
    FeeAmount DECIMAL(10, 2),
    FeeType VARCHAR(50),
    FOREIGN KEY (TransactionID) REFERENCES Transactions(TransactionID)
);

-- 14.Dividends 表（分红表）
CREATE TABLE Dividends (
    DividendID INT PRIMARY KEY,
    AccountID INT,
    Symbol VARCHAR(10),
    DividendDate DATE,
    DividendAmount DECIMAL(10, 2),
    FOREIGN KEY (AccountID) REFERENCES Accounts(AccountID)
);

-- 15.InterestRates 表（利率表）
CREATE TABLE InterestRates (
    RateID INT PRIMARY KEY,
    RateDate DATE,
    Rate DECIMAL(5, 2),
    Description VARCHAR(255)
);

-- 16.Strategies 表（策略表）
CREATE TABLE Strategies (
    StrategyID INT PRIMARY KEY,
    StrategyName VARCHAR(100),
    Description VARCHAR(255),
    RiskLevel VARCHAR(20)
);

-- 17.Reports 表（报告表）
CREATE TABLE Reports (
    ReportID INT PRIMARY KEY,
    TraderID INT,
    ReportDate DATE,
    ReportType VARCHAR(50),
    Content TEXT,
    FOREIGN KEY (TraderID) REFERENCES Traders(TraderID)
);

-- 18.Benchmarks 表（基准表）
CREATE TABLE Benchmarks (
    BenchmarkID INT PRIMARY KEY,
    BenchmarkDate DATE,
    BenchmarkValue DECIMAL(10, 2),
    Description VARCHAR(255)
);

-- 19.Allocations 表（分配表）
CREATE TABLE Allocations (
    AllocationID INT PRIMARY KEY,
    TraderID INT,
    Symbol VARCHAR(10),
    AllocationDate DATE,
    AllocationAmount DECIMAL(10, 2),
    FOREIGN KEY (TraderID) REFERENCES Traders(TraderID)
);

-- 20.Portfolios 表（投资组合表）
CREATE TABLE Portfolios (
    PortfolioID INT PRIMARY KEY,
    TraderID INT,
    PortfolioName VARCHAR(100),
    CreationDate DATE,
    Status VARCHAR(20),
    FOREIGN KEY (TraderID) REFERENCES Traders(TraderID)
);

-- 插入数据表数据
-- 1.Traders 表（交易员表）
INSERT INTO Tradingdatas.dbo.Traders (TraderID, TraderName, Department, JoinDate, Status) VALUES
(1, 'Alice Johnson', 'Equity', '2019-05-21', 'Active'),
(2, 'Bob Smith', 'Fixed Income', '2018-11-14', 'Active'),
(3, 'Carol White', 'Derivatives', '2020-01-10', 'Active'),
(4, 'David King', 'Commodities', '2021-07-15', 'Active'),
(5, 'Eve Adams', 'Foreign Exchange', '2017-09-05', 'Active'),
(6, 'Franklin White', 'Risk Management', '2022-02-20', 'Active'),
(7, 'George Knight', 'Equity', '2021-03-01', 'Active'),
(8, 'Helen Lee', 'Fixed Income', '2020-06-15', 'Active'),
(9, 'Ivan Kim', 'Derivatives', '2019-10-20', 'Active'),
(10, 'Jackie Chan', 'Commodities', '2018-12-01', 'Active'),
(11, 'Karen Hall', 'Foreign Exchange', '2017-08-05', 'Active'),
(12, 'Leo Wang', 'Risk Management', '2021-11-22', 'Active'),
(13, 'Mona Scott', 'Equity', '2022-04-14', 'Active'),
(14, 'Nathaniel Parker', 'Fixed Income', '2020-01-19', 'Active'),
(15, 'Olivia Adams', 'Derivatives', '2019-07-25', 'Active'),
(16, 'Paul Martin', 'Commodities', '2018-09-30', 'Active'),
(17, 'Quincy Zhang', 'Foreign Exchange', '2021-02-10', 'Active'),
(18, 'Rachel Thompson', 'Risk Management', '2020-05-07', 'Active'),
(19, 'Steve Harris', 'Equity', '2019-11-18', 'Active'),
(20, 'Tina Turner', 'Fixed Income', '2018-03-22', 'Active');

-- 2.Trades 表（交易表）
INSERT INTO Tradingdatas.dbo.Trades (TradeID, TraderID, TradeDate, BuySell, Quantity, Price, Symbol, Market, TradeType) VALUES
(1, 1, '2023-05-15', 'Buy', 100, 150.50, 'AAPL', 'NASDAQ', 'Equity'),
(2, 2, '2023-05-16', 'Sell', 200, 250.75, 'GOOGL', 'NASDAQ', 'Equity'),
(3, 3, '2023-05-17', 'Buy', 150, 50.30, 'MSFT', 'NASDAQ', 'Equity'),
(4, 4, '2023-05-18', 'Sell', 300, 120.10, 'AMZN', 'NASDAQ', 'Equity'),
(5, 5, '2023-05-19', 'Buy', 250, 350.60, 'TSLA', 'NASDAQ', 'Equity'),
(6, 6, '2023-05-20', 'Sell', 180, 450.70, 'FB', 'NASDAQ', 'Equity'),
(7, 7, '2023-05-21', 'Buy', 220, 500.80, 'NFLX', 'NASDAQ', 'Equity'),
(8, 8, '2023-05-22', 'Sell', 130, 550.90, 'AAPL', 'NASDAQ', 'Equity'),
(9, 9, '2023-05-23', 'Buy', 210, 600.00, 'GOOGL', 'NASDAQ', 'Equity'),
(10, 10, '2023-05-24', 'Sell', 240, 650.10, 'MSFT', 'NASDAQ', 'Equity'),
(11, 11, '2023-05-25', 'Buy', 260, 700.20, 'AMZN', 'NASDAQ', 'Equity'),
(12, 12, '2023-05-26', 'Sell', 270, 750.30, 'TSLA', 'NASDAQ', 'Equity'),
(13, 13, '2023-05-27', 'Buy', 280, 800.40, 'FB', 'NASDAQ', 'Equity'),
(14, 14, '2023-05-28', 'Sell', 290, 850.50, 'NFLX', 'NASDAQ', 'Equity'),
(15, 15, '2023-05-29', 'Buy', 300, 900.60, 'AAPL', 'NASDAQ', 'Equity'),
(16, 16, '2023-05-30', 'Sell', 310, 950.70, 'GOOGL', 'NASDAQ', 'Equity'),
(17, 17, '2023-05-31', 'Buy', 320, 1000.80, 'MSFT', 'NASDAQ', 'Equity'),
(18, 18, '2023-06-01', 'Sell', 330, 1050.90, 'AMZN', 'NASDAQ', 'Equity'),
(19, 19, '2023-06-02', 'Buy', 340, 1100.00, 'TSLA', 'NASDAQ', 'Equity'),
(20, 20, '2023-06-03', 'Sell', 350, 1150.10, 'FB', 'NASDAQ', 'Equity');

-- 3.TradeDetails 表（交易细节表）
INSERT INTO Tradingdatas.dbo.TradeDetails (DetailID, TradeID, SettlementDate, Commission, NetAmount, Tax) VALUES
(1, 1, '2023-05-16', 15.50, 14985.00, 5.00),
(2, 2, '2023-05-17', 20.75, 49929.25, 7.00),
(3, 3, '2023-05-18', 10.30, 7544.70, 3.00),
(4, 4, '2023-05-19', 25.10, 35984.90, 9.00),
(5, 5, '2023-05-20', 35.60, 87414.40, 11.00),
(6, 6, '2023-05-21', 45.70, 80504.30, 13.00),
(7, 7, '2023-05-22', 50.80, 110956.20, 15.00),
(8, 8, '2023-05-23', 55.90, 71658.10, 17.00),
(9, 9, '2023-05-24', 60.00, 125040.00, 19.00),
(10, 10, '2023-05-25', 65.10, 156087.90, 21.00),
(11, 11, '2023-05-26', 70.20, 181029.80, 23.00),
(12, 12, '2023-05-27', 75.30, 202048.70, 25.00),
(13, 13, '2023-05-28', 80.40, 224111.60, 27.00),
(14, 14, '2023-05-29', 85.50, 246214.50, 29.00),
(15, 15, '2023-05-30', 90.60, 270114.40, 31.00),
(16, 16, '2023-05-31', 95.70, 294812.30, 33.00),
(17, 17, '2023-06-01', 100.80, 320307.20, 35.00),
(18, 18, '2023-06-02', 105.90, 346598.10, 37.00),
(19, 19, '2023-06-03', 110.00, 373684.00, 39.00),
(20, 20, '2023-06-04', 115.10, 401564.90, 41.00);

-- 4.TradePerformance 表（交易表现表）
INSERT INTO Tradingdatas.dbo.TradePerformance (PerformanceID, TradeID, PnL, ReturnRate, HoldingPeriod) VALUES
(1, 1, 200.00, 1.33, 2),
(2, 2, 300.00, 2.00, 4),
(3, 3, 400.00, 2.67, 6),
(4, 4, 500.00, 3.33, 8),
(5, 5, 600.00, 4.00, 10),
(6, 6, 700.00, 4.67, 12),
(7, 7, 800.00, 5.33, 14),
(8, 8, 900.00, 6.00, 16),
(9, 9, 1000.00, 6.67, 18),
(10, 10, 1100.00, 7.33, 20),
(11, 11, 1200.00, 8.00, 22),
(12, 12, 1300.00, 8.67, 24),
(13, 13, 1400.00, 9.33, 26),
(14, 14, 1500.00, 10.00, 28),
(15, 15, 1600.00, 10.67, 30),
(16, 16, 1700.00, 11.33, 32),
(17, 17, 1800.00, 12.00, 34),
(18, 18, 1900.00, 12.67, 36),
(19, 19, 2000.00, 13.33, 38),
(20, 20, 2100.00, 14.00, 40);

-- 5.MarketData 表（市场数据表）
INSERT INTO Tradingdatas.dbo.MarketData (MarketDataID, Symbol, TradeDate, OpenPrice, HighPrice, LowPrice, ClosePrice, Volume) VALUES
(1, 'AAPL', '2023-05-15', 150.00, 155.00, 149.00, 150.50, 1000000),
(2, 'GOOGL', '2023-05-16', 250.00, 260.00, 240.00, 250.75, 2000000),
(3, 'MSFT', '2023-05-17', 50.00, 52.00, 48.00, 50.30, 1500000),
(4, 'AMZN', '2023-05-18', 120.00, 125.00, 115.00, 120.10, 3000000),
(5, 'TSLA', '2023-05-19', 350.00, 360.00, 340.00, 350.60, 2500000),
(6, 'FB', '2023-05-20', 450.00, 460.00, 440.00, 450.70, 1800000),
(7, 'NFLX', '2023-05-21', 500.00, 510.00, 490.00, 500.80, 2200000),
(8, 'AAPL', '2023-05-22', 550.00, 560.00, 540.00, 550.90, 1300000),
(9, 'GOOGL', '2023-05-23', 600.00, 610.00, 590.00, 600.00, 2100000),
(10, 'MSFT', '2023-05-24', 650.00, 660.00, 640.00, 650.10, 2400000),
(11, 'AMZN', '2023-05-25', 700.00, 710.00, 690.00, 700.20, 2600000),
(12, 'TSLA', '2023-05-26', 750.00, 760.00, 740.00, 750.30, 2700000),
(13, 'FB', '2023-05-27', 800.00, 810.00, 790.00, 800.40, 2800000),
(14, 'NFLX', '2023-05-28', 850.00, 860.00, 840.00, 850.50, 2900000),
(15, 'AAPL', '2023-05-29', 900.00, 910.00, 890.00, 900.60, 3000000),
(16, 'GOOGL', '2023-05-30', 950.00, 960.00, 940.00, 950.70, 3100000),
(17, 'MSFT', '2023-05-31', 1000.00, 1010.00, 990.00, 1000.80, 3200000),
(18, 'AMZN', '2023-06-01', 1050.00, 1060.00, 1040.00, 1050.90, 3300000),
(19, 'TSLA', '2023-06-02', 1100.00, 1110.00, 1090.00, 1100.00, 3400000),
(20, 'FB', '2023-06-03', 1150.00, 1160.00, 1140.00, 1150.10, 3500000);

-- 6.Orders 表（订单表）
INSERT INTO Tradingdatas.dbo.Orders (OrderID, TraderID, Symbol, OrderDate, OrderType, Quantity, Price, Status) VALUES
(1, 1, 'AAPL', '2023-05-15', 'Limit', 100, 150.00, 'Filled'),
(2, 2, 'GOOGL', '2023-05-16', 'Market', 200, 250.00, 'Filled'),
(3, 3, 'MSFT', '2023-05-17', 'Limit', 150, 50.00, 'Filled'),
(4, 4, 'AMZN', '2023-05-18', 'Market', 300, 120.00, 'Filled'),
(5, 5, 'TSLA', '2023-05-19', 'Limit', 250, 350.00, 'Filled'),
(6, 6, 'FB', '2023-05-20', 'Market', 180, 450.00, 'Filled'),
(7, 7, 'NFLX', '2023-05-21', 'Limit', 220, 500.00, 'Filled'),
(8, 8, 'AAPL', '2023-05-22', 'Market', 130, 550.00, 'Filled'),
(9, 9, 'GOOGL', '2023-05-23', 'Limit', 210, 600.00, 'Filled'),
(10, 10, 'MSFT', '2023-05-24', 'Market', 240, 650.00, 'Filled'),
(11, 11, 'AMZN', '2023-05-25', 'Limit', 260, 700.00, 'Filled'),
(12, 12, 'TSLA', '2023-05-26', 'Market', 270, 750.00, 'Filled'),
(13, 13, 'FB', '2023-05-27', 'Limit', 280, 800.00, 'Filled'),
(14, 14, 'NFLX', '2023-05-28', 'Market', 290, 850.00, 'Filled'),
(15, 15, 'AAPL', '2023-05-29', 'Limit', 300, 900.00, 'Filled'),
(16, 16, 'GOOGL', '2023-05-30', 'Market', 310, 950.00, 'Filled'),
(17, 17, 'MSFT', '2023-05-31', 'Limit', 320, 1000.00, 'Filled'),
(18, 18, 'AMZN', '2023-06-01', 'Market', 330, 1050.00, 'Filled'),
(19, 19, 'TSLA', '2023-06-02', 'Limit', 340, 1100.00, 'Filled'),
(20, 20, 'FB', '2023-06-03', 'Market', 350, 1150.00, 'Filled');

-- 7.Positions 表（持仓表）
INSERT INTO Tradingdatas.dbo.Positions (PositionID, TraderID, Symbol, Quantity, AveragePrice, MarketValue) VALUES
(1, 1, 'AAPL', 100, 150.00, 15000.00),
(2, 2, 'GOOGL', 200, 250.00, 50000.00),
(3, 3, 'MSFT', 150, 50.00, 7500.00),
(4, 4, 'AMZN', 300, 120.00, 36000.00),
(5, 5, 'TSLA', 250, 350.00, 87500.00),
(6, 6, 'FB', 180, 450.00, 81000.00),
(7, 7, 'NFLX', 220, 500.00, 110000.00),
(8, 8, 'AAPL', 130, 550.00, 71500.00),
(9, 9, 'GOOGL', 210, 600.00, 126000.00),
(10, 10, 'MSFT', 240, 650.00, 156000.00),
(11, 11, 'AMZN', 260, 700.00, 182000.00),
(12, 12, 'TSLA', 270, 750.00, 202500.00),
(13, 13, 'FB', 280, 800.00, 224000.00),
(14, 14, 'NFLX', 290, 850.00, 246500.00),
(15, 15, 'AAPL', 300, 900.00, 270000.00),
(16, 16, 'GOOGL', 310, 950.00, 294500.00),
(17, 17, 'MSFT', 320, 1000.00, 320000.00),
(18, 18, 'AMZN', 330, 1050.00, 346500.00),
(19, 19, 'TSLA', 340, 1100.00, 374000.00),
(20, 20, 'FB', 350, 1150.00, 402500.00);

-- 8.RiskMetrics 表（风险度量表）
INSERT INTO Tradingdatas.dbo.RiskMetrics (RiskMetricID, TraderID, VaR, Beta, SharpeRatio) VALUES
(1, 1, 2000.00, 1.20, 1.50),
(2, 2, 2500.00, 1.25, 1.55),
(3, 3, 1500.00, 1.30, 1.60),
(4, 4, 3000.00, 1.35, 1.65),
(5, 5, 3500.00, 1.40, 1.70),
(6, 6, 1800.00, 1.45, 1.75),
(7, 7, 2200.00, 1.50, 1.80),
(8, 8, 2800.00, 1.55, 1.85),
(9, 9, 2600.00, 1.60, 1.90),
(10, 10, 2400.00, 1.65, 1.95),
(11, 11, 3200.00, 1.70, 2.00),
(12, 12, 3400.00, 1.75, 2.05),
(13, 13, 3600.00, 1.80, 2.10),
(14, 14, 3800.00, 1.85, 2.15),
(15, 15, 4000.00, 1.90, 2.20),
(16, 16, 4200.00, 1.95, 2.25),
(17, 17, 4400.00, 2.00, 2.30),
(18, 18, 4600.00, 2.05, 2.35),
(19, 19, 4800.00, 2.10, 2.40),
(20, 20, 5000.00, 2.15, 2.45);

-- 9.Compliance 表（合规表）
INSERT INTO Tradingdatas.dbo.Compliance (ComplianceID, TraderID, AuditDate, IssueDescription, Resolution, Status) VALUES
(1, 1, '2023-05-15', 'Late trade reporting', 'Training provided', 'Resolved'),
(2, 2, '2023-05-16', 'Excessive risk exposure', 'Risk limits enforced', 'Resolved'),
(3, 3, '2023-05-17', 'Unauthorized trade', 'Trade reversed', 'Resolved'),
(4, 4, '2023-05-18', 'Compliance training missed', 'Make-up session attended', 'Resolved'),
(5, 5, '2023-05-19', 'Documentation issue', 'Documentation corrected', 'Resolved'),
(6, 6, '2023-05-20', 'Data privacy breach', 'Data secured', 'Resolved'),
(7, 7, '2023-05-21', 'Late filing', 'Filed on time', 'Resolved'),
(8, 8, '2023-05-22', 'Conflict of interest', 'Conflict managed', 'Resolved'),
(9, 9, '2023-05-23', 'Trading limit breach', 'Limit adjusted', 'Resolved'),
(10, 10, '2023-05-24', 'Unreported trade', 'Trade reported', 'Resolved'),
(11, 11, '2023-05-25', 'Policy violation', 'Policy revised', 'Resolved'),
(12, 12, '2023-05-26', 'Improper disclosure', 'Disclosure corrected', 'Resolved'),
(13, 13, '2023-05-27', 'Internal control issue', 'Control strengthened', 'Resolved'),
(14, 14, '2023-05-28', 'Incorrect pricing', 'Pricing corrected', 'Resolved'),
(15, 15, '2023-05-29', 'Fraudulent activity', 'Activity halted', 'Resolved'),
(16, 16, '2023-05-30', 'Record-keeping issue', 'Records updated', 'Resolved'),
(17, 17, '2023-05-31', 'Compliance breach', 'Breach addressed', 'Resolved'),
(18, 18, '2023-06-01', 'Market manipulation', 'Manipulation halted', 'Resolved'),
(19, 19, '2023-06-02', 'Insider trading', 'Investigation closed', 'Resolved'),
(20, 20, '2023-06-03', 'Inaccurate reporting', 'Reporting corrected', 'Resolved');

-- 10.Clients 表（客户表）
INSERT INTO Tradingdatas.dbo.Clients (ClientID, ClientName, ClientType, JoinDate, Status) VALUES
(1, 'John Doe', 'Individual', '2020-01-15', 'Active'),
(2, 'Jane Smith', 'Individual', '2020-02-20', 'Active'),
(3, 'Acme Corp', 'Institutional', '2020-03-25', 'Active'),
(4, 'Globex Inc', 'Institutional', '2020-04-30', 'Active'),
(5, 'XYZ Ltd', 'Institutional', '2020-05-05', 'Active'),
(6, 'Tech Ventures', 'Institutional', '2020-06-10', 'Active'),
(7, 'Jane Brown', 'Individual', '2020-07-15', 'Active'),
(8, 'John Black', 'Individual', '2020-08-20', 'Active'),
(9, 'Alpha Investments', 'Institutional', '2020-09-25', 'Active'),
(10, 'Beta Holdings', 'Institutional', '2020-10-30', 'Active'),
(11, 'Gamma Partners', 'Institutional', '2020-11-05', 'Active'),
(12, 'Delta Funds', 'Institutional', '2020-12-10', 'Active'),
(13, 'Jane White', 'Individual', '2021-01-15', 'Active'),
(14, 'John Green', 'Individual', '2021-02-20', 'Active'),
(15, 'Omega Trust', 'Institutional', '2021-03-25', 'Active'),
(16, 'Zeta Capital', 'Institutional', '2021-04-30', 'Active'),
(17, 'Theta Associates', 'Institutional', '2021-05-05', 'Active'),
(18, 'Sigma Financial', 'Institutional', '2021-06-10', 'Active'),
(19, 'Jane Red', 'Individual', '2021-07-15', 'Active'),
(20, 'John Blue', 'Individual', '2021-08-20', 'Active');

-- 11.Accounts 表（账户表）
INSERT INTO Tradingdatas.dbo.Accounts (AccountID, ClientID, AccountType, Balance, Status) VALUES
(1, 1, 'Savings', 10000.00, 'Active'),
(2, 2, 'Checking', 15000.00, 'Active'),
(3, 3, 'Corporate', 200000.00, 'Active'),
(4, 4, 'Corporate', 250000.00, 'Active'),
(5, 5, 'Corporate', 300000.00, 'Active'),
(6, 6, 'Corporate', 350000.00, 'Active'),
(7, 7, 'Savings', 12000.00, 'Active'),
(8, 8, 'Checking', 18000.00, 'Active'),
(9, 9, 'Corporate', 400000.00, 'Active'),
(10, 10, 'Corporate', 450000.00, 'Active'),
(11, 11, 'Corporate', 500000.00, 'Active'),
(12, 12, 'Corporate', 550000.00, 'Active'),
(13, 13, 'Savings', 14000.00, 'Active'),
(14, 14, 'Checking', 20000.00, 'Active'),
(15, 15, 'Corporate', 600000.00, 'Active'),
(16, 16, 'Corporate', 650000.00, 'Active'),
(17, 17, 'Corporate', 700000.00, 'Active'),
(18, 18, 'Corporate', 750000.00, 'Active'),
(19, 19, 'Savings', 16000.00, 'Active'),
(20, 20, 'Checking', 22000.00, 'Active');

-- 12.Transactions 表（交易记录表）
INSERT INTO Tradingdatas.dbo.Transactions (TransactionID, AccountID, TransactionDate, Amount, TransactionType) VALUES
(1, 1, '2023-05-15', 1000.00, 'Deposit'),
(2, 2, '2023-05-16', 2000.00, 'Withdrawal'),
(3, 3, '2023-05-17', 30000.00, 'Deposit'),
(4, 4, '2023-05-18', 40000.00, 'Withdrawal'),
(5, 5, '2023-05-19', 50000.00, 'Deposit'),
(6, 6, '2023-05-20', 60000.00, 'Withdrawal'),
(7, 7, '2023-05-21', 7000.00, 'Deposit'),
(8, 8, '2023-05-22', 8000.00, 'Withdrawal'),
(9, 9, '2023-05-23', 90000.00, 'Deposit'),
(10, 10, '2023-05-24', 100000.00, 'Withdrawal'),
(11, 11, '2023-05-25', 110000.00, 'Deposit'),
(12, 12, '2023-05-26', 120000.00, 'Withdrawal'),
(13, 13, '2023-05-27', 13000.00, 'Deposit'),
(14, 14, '2023-05-28', 14000.00, 'Withdrawal'),
(15, 15, '2023-05-29', 150000.00, 'Deposit'),
(16, 16, '2023-05-30', 160000.00, 'Withdrawal'),
(17, 17, '2023-05-31', 170000.00, 'Deposit'),
(18, 18, '2023-06-01', 180000.00, 'Withdrawal'),
(19, 19, '2023-06-02', 19000.00, 'Deposit'),
(20, 20, '2023-06-03', 20000.00, 'Withdrawal');

-- 13.Fees 表（费用表）
INSERT INTO Tradingdatas.dbo.Fees (FeeID, TransactionID, FeeAmount, FeeType) VALUES
(1, 1, 10.00, 'Transaction Fee'),
(2, 2, 20.00, 'Transaction Fee'),
(3, 3, 30.00, 'Transaction Fee'),
(4, 4, 40.00, 'Transaction Fee'),
(5, 5, 50.00, 'Transaction Fee'),
(6, 6, 60.00, 'Transaction Fee'),
(7, 7, 70.00, 'Transaction Fee'),
(8, 8, 80.00, 'Transaction Fee'),
(9, 9, 90.00, 'Transaction Fee'),
(10, 10, 100.00, 'Transaction Fee'),
(11, 11, 110.00, 'Transaction Fee'),
(12, 12, 120.00, 'Transaction Fee'),
(13, 13, 130.00, 'Transaction Fee'),
(14, 14, 140.00, 'Transaction Fee'),
(15, 15, 150.00, 'Transaction Fee'),
(16, 16, 160.00, 'Transaction Fee'),
(17, 17, 170.00, 'Transaction Fee'),
(18, 18, 180.00, 'Transaction Fee'),
(19, 19, 190.00, 'Transaction Fee'),
(20, 20, 200.00, 'Transaction Fee');

-- 14.Dividends 表（分红表）
INSERT INTO Tradingdatas.dbo.Dividends (DividendID, AccountID, Symbol, DividendDate, DividendAmount) VALUES
(1, 1, 'AAPL', '2023-05-15', 50.00),
(2, 2, 'GOOGL', '2023-05-16', 75.00),
(3, 3, 'MSFT', '2023-05-17', 25.00),
(4, 4, 'AMZN', '2023-05-18', 100.00),
(5, 5, 'TSLA', '2023-05-19', 150.00),
(6, 6, 'FB', '2023-05-20', 125.00),
(7, 7, 'NFLX', '2023-05-21', 200.00),
(8, 8, 'AAPL', '2023-05-22', 250.00),
(9, 9, 'GOOGL', '2023-05-23', 275.00),
(10, 10, 'MSFT', '2023-05-24', 300.00),
(11, 11, 'AMZN', '2023-05-25', 350.00),
(12, 12, 'TSLA', '2023-05-26', 400.00),
(13, 13, 'FB', '2023-05-27', 450.00),
(14, 14, 'NFLX', '2023-05-28', 500.00),
(15, 15, 'AAPL', '2023-05-29', 550.00),
(16, 16, 'GOOGL', '2023-05-30', 600.00),
(17, 17, 'MSFT', '2023-05-31', 650.00),
(18, 18, 'AMZN', '2023-06-01', 700.00),
(19, 19, 'TSLA', '2023-06-02', 750.00),
(20, 20, 'FB', '2023-06-03', 800.00);

-- 15.InterestRates 表（利率表）
INSERT INTO Tradingdatas.dbo.InterestRates (RateID, RateDate, Rate, Description) VALUES
(1, '2023-05-15', 0.50, 'Monthly rate'),
(2, '2023-05-16', 0.55, 'Monthly rate'),
(3, '2023-05-17', 0.60, 'Monthly rate'),
(4, '2023-05-18', 0.65, 'Monthly rate'),
(5, '2023-05-19', 0.70, 'Monthly rate'),
(6, '2023-05-20', 0.75, 'Monthly rate'),
(7, '2023-05-21', 0.80, 'Monthly rate'),
(8, '2023-05-22', 0.85, 'Monthly rate'),
(9, '2023-05-23', 0.90, 'Monthly rate'),
(10, '2023-05-24', 0.95, 'Monthly rate'),
(11, '2023-05-25', 1.00, 'Monthly rate'),
(12, '2023-05-26', 1.05, 'Monthly rate'),
(13, '2023-05-27', 1.10, 'Monthly rate'),
(14, '2023-05-28', 1.15, 'Monthly rate'),
(15, '2023-05-29', 1.20, 'Monthly rate'),
(16, '2023-05-30', 1.25, 'Monthly rate'),
(17, '2023-05-31', 1.30, 'Monthly rate'),
(18, '2023-06-01', 1.35, 'Monthly rate'),
(19, '2023-06-02', 1.40, 'Monthly rate'),
(20, '2023-06-03', 1.45, 'Monthly rate');

-- 16.Strategies 表（策略表）
INSERT INTO Tradingdatas.dbo.Strategies (StrategyID, StrategyName, Description, RiskLevel) VALUES
(1, 'Growth', 'Focus on capital appreciation', 'High'),
(2, 'Income', 'Focus on generating income', 'Low'),
(3, 'Balanced', 'Mix of growth and income', 'Medium'),
(4, 'Aggressive Growth', 'High risk, high reward', 'High'),
(5, 'Conservative', 'Focus on capital preservation', 'Low'),
(6, 'Index', 'Track a market index', 'Medium'),
(7, 'Dividend', 'Focus on dividend-paying stocks', 'Low'),
(8, 'Value', 'Focus on undervalued stocks', 'Medium'),
(9, 'Sector', 'Focus on specific sectors', 'High'),
(10, 'International', 'Focus on international stocks', 'High'),
(11, 'Hedge Fund', 'Alternative investment strategies', 'High'),
(12, 'Arbitrage', 'Take advantage of price differences', 'High'),
(13, 'Event-Driven', 'Focus on corporate events', 'Medium'),
(14, 'Quantitative', 'Use of quantitative models', 'High'),
(15, 'Ethical', 'Focus on socially responsible investments', 'Low'),
(16, 'Growth & Income', 'Mix of growth and income', 'Medium'),
(17, 'Emerging Markets', 'Focus on emerging markets', 'High'),
(18, 'Real Estate', 'Focus on real estate investments', 'Medium'),
(19, 'Commodities', 'Focus on commodities', 'High'),
(20, 'Fixed Income', 'Focus on bonds and fixed income', 'Low');

-- 17.Reports 表（报告表）
INSERT INTO Tradingdatas.dbo.Reports (ReportID, TraderID, ReportDate, ReportType, Content) VALUES
(1, 1, '2023-05-15', 'Daily', 'Daily report content'),
(2, 2, '2023-05-16', 'Weekly', 'Weekly report content'),
(3, 3, '2023-05-17', 'Monthly', 'Monthly report content'),
(4, 4, '2023-05-18', 'Quarterly', 'Quarterly report content'),
(5, 5, '2023-05-19', 'Annual', 'Annual report content'),
(6, 6, '2023-05-20', 'Daily', 'Daily report content'),
(7, 7, '2023-05-21', 'Weekly', 'Weekly report content'),
(8, 8, '2023-05-22', 'Monthly', 'Monthly report content'),
(9, 9, '2023-05-23', 'Quarterly', 'Quarterly report content'),
(10, 10, '2023-05-24', 'Annual', 'Annual report content'),
(11, 11, '2023-05-25', 'Daily', 'Daily report content'),
(12, 12, '2023-05-26', 'Weekly', 'Weekly report content'),
(13, 13, '2023-05-27', 'Monthly', 'Monthly report content'),
(14, 14, '2023-05-28', 'Quarterly', 'Quarterly report content'),
(15, 15, '2023-05-29', 'Annual', 'Annual report content'),
(16, 16, '2023-05-30', 'Daily', 'Daily report content'),
(17, 17, '2023-05-31', 'Weekly', 'Weekly report content'),
(18, 18, '2023-06-01', 'Monthly', 'Monthly report content'),
(19, 19, '2023-06-02', 'Quarterly', 'Quarterly report content'),
(20, 20, '2023-06-03', 'Annual', 'Annual report content');

-- 18.Benchmarks 表（基准表）
INSERT INTO Tradingdatas.dbo.Benchmarks (BenchmarkID, BenchmarkDate, BenchmarkValue, Description) VALUES
(1, '2023-05-15', 1000.00, 'S&P 500'),
(2, '2023-05-16', 1050.00, 'S&P 500'),
(3, '2023-05-17', 1100.00, 'S&P 500'),
(4, '2023-05-18', 1150.00, 'S&P 500'),
(5, '2023-05-19', 1200.00, 'S&P 500'),
(6, '2023-05-20', 1250.00, 'S&P 500'),
(7, '2023-05-21', 1300.00, 'S&P 500'),
(8, '2023-05-22', 1350.00, 'S&P 500'),
(9, '2023-05-23', 1400.00, 'S&P 500'),
(10, '2023-05-24', 1450.00, 'S&P 500'),
(11, '2023-05-25', 1500.00, 'S&P 500'),
(12, '2023-05-26', 1550.00, 'S&P 500'),
(13, '2023-05-27', 1600.00, 'S&P 500'),
(14, '2023-05-28', 1650.00, 'S&P 500'),
(15, '2023-05-29', 1700.00, 'S&P 500'),
(16, '2023-05-30', 1750.00, 'S&P 500'),
(17, '2023-05-31', 1800.00, 'S&P 500'),
(18, '2023-06-01', 1850.00, 'S&P 500'),
(19, '2023-06-02', 1900.00, 'S&P 500'),
(20, '2023-06-03', 1950.00, 'S&P 500');

-- 19.Allocations 表（分配表）
INSERT INTO Tradingdatas.dbo.Allocations (AllocationID, TraderID, Symbol, AllocationDate, AllocationAmount) VALUES
(1, 1, 'AAPL', '2023-05-15', 5000.00),
(2, 2, 'GOOGL', '2023-05-16', 10000.00),
(3, 3, 'MSFT', '2023-05-17', 15000.00),
(4, 4, 'AMZN', '2023-05-18', 20000.00),
(5, 5, 'TSLA', '2023-05-19', 25000.00),
(6, 6, 'FB', '2023-05-20', 30000.00),
(7, 7, 'NFLX', '2023-05-21', 35000.00),
(8, 8, 'AAPL', '2023-05-22', 40000.00),
(9, 9, 'GOOGL', '2023-05-23', 45000.00),
(10, 10, 'MSFT', '2023-05-24', 50000.00),
(11, 11, 'AMZN', '2023-05-25', 55000.00),
(12, 12, 'TSLA', '2023-05-26', 60000.00),
(13, 13, 'FB', '2023-05-27', 65000.00),
(14, 14, 'NFLX', '2023-05-28', 70000.00),
(15, 15, 'AAPL', '2023-05-29', 75000.00),
(16, 16, 'GOOGL', '2023-05-30', 80000.00),
(17, 17, 'MSFT', '2023-05-31', 85000.00),
(18, 18, 'AMZN', '2023-06-01', 90000.00),
(19, 19, 'TSLA', '2023-06-02', 95000.00),
(20, 20, 'FB', '2023-06-03', 100000.00);

-- 20.Portfolios 表（投资组合表）
INSERT INTO Tradingdatas.dbo.Portfolios (PortfolioID, TraderID, PortfolioName, CreationDate, Status) VALUES
(1, 1, 'Tech Growth', '2023-01-01', 'Active'),
(2, 2, 'Income Fund', '2023-01-02', 'Active'),
(3, 3, 'Balanced Fund', '2023-01-03', 'Active'),
(4, 4, 'Aggressive Growth', '2023-01-04', 'Active'),
(5, 5, 'Conservative Fund', '2023-01-05', 'Active'),
(6, 6, 'Index Fund', '2023-01-06', 'Active'),
(7, 7, 'Dividend Fund', '2023-01-07', 'Active'),
(8, 8, 'Value Fund', '2023-01-08', 'Active'),
(9, 9, 'Sector Fund', '2023-01-09', 'Active'),
(10, 10, 'International Fund', '2023-01-10', 'Active'),
(11, 11, 'Hedge Fund', '2023-01-11', 'Active'),
(12, 12, 'Arbitrage Fund', '2023-01-12', 'Active'),
(13, 13, 'Event-Driven Fund', '2023-01-13', 'Active'),
(14, 14, 'Quantitative Fund', '2023-01-14', 'Active'),
(15, 15, 'Ethical Fund', '2023-01-15', 'Active'),
(16, 16, 'Growth & Income Fund', '2023-01-16', 'Active'),
(17, 17, 'Emerging Markets Fund', '2023-01-17', 'Active'),
(18, 18, 'Real Estate Fund', '2023-01-18', 'Active'),
(19, 19, 'Commodities Fund', '2023-01-19', 'Active'),
(20, 20, 'Fixed Income Fund', '2023-01-20', 'Active');

-- 为了创建一个包含凯利公式比例和关联交易数据的表，我们首先需要了解凯利公式的定义。

/**
- 凯利公式通常用于确定最佳投注比例，具体公式为：

\[ f^* = \frac{bp - q}{b} \]

其中：
- \( f^* \) 是凯利公式比例（Kelly Fraction）。
- \( b \) 是赔率（Odds）。
- \( p \) 是获胜概率（Probability of Win）。
- \( q \) 是失败概率（Probability of Loss），即 \( 1 - p \)。

为了实现这个需求，我们将创建一个新的表 `KellyRatios`，该表将包含计算的凯利公式比例，并关联到 `Trades` 表。表格的结构可能如下所示：

- `KellyID`：唯一标识符。
- `TradeID`：引用关联的交易（外键）。
- `Odds`：赔率。
- `ProbabilityOfWin`：获胜概率。
- `KellyFraction`：计算的凯利公式比例。

请在 SQL Server 中运行上述 SQL 脚本来创建并填充 `KellyRatios` 表。如果需要更多帮助或有任何问题，请告诉我！
*/

-- 创建 KellyRatios 表
CREATE TABLE KellyRatios (
    KellyID INT PRIMARY KEY,
    TradeID INT FOREIGN KEY REFERENCES Trades(TradeID),
    Odds DECIMAL(5, 2),
    ProbabilityOfWin DECIMAL(5, 4),
    KellyFraction DECIMAL(5, 4)
);

-- 插入示例数据
INSERT INTO Tradingdatas.dbo.KellyRatios (KellyID, TradeID, Odds, ProbabilityOfWin, KellyFraction) VALUES
(1, 1, 2.50, 0.60, (2.50 * 0.60 - 0.40) / 2.50),
(2, 2, 3.00, 0.50, (3.00 * 0.50 - 0.50) / 3.00),
(3, 3, 1.75, 0.70, (1.75 * 0.70 - 0.30) / 1.75),
(4, 4, 2.00, 0.55, (2.00 * 0.55 - 0.45) / 2.00),
(5, 5, 2.25, 0.65, (2.25 * 0.65 - 0.35) / 2.25),
(6, 6, 1.50, 0.80, (1.50 * 0.80 - 0.20) / 1.50),
(7, 7, 2.75, 0.45, (2.75 * 0.45 - 0.55) / 2.75),
(8, 8, 3.50, 0.30, (3.50 * 0.30 - 0.70) / 3.50),
(9, 9, 2.10, 0.60, (2.10 * 0.60 - 0.40) / 2.10),
(10, 10, 1.80, 0.75, (1.80 * 0.75 - 0.25) / 1.80),
(11, 11, 2.40, 0.55, (2.40 * 0.55 - 0.45) / 2.40),
(12, 12, 3.20, 0.40, (3.20 * 0.40 - 0.60) / 3.20),
(13, 13, 2.65, 0.50, (2.65 * 0.50 - 0.50) / 2.65),
(14, 14, 1.90, 0.70, (1.90 * 0.70 - 0.30) / 1.90),
(15, 15, 2.85, 0.60, (2.85 * 0.60 - 0.40) / 2.85);
