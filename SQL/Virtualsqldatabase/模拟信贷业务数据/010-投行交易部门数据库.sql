-- 创建投行交易部门数据库
create database hftradingdatas;
use hftradingdatas;

create database investmentbanktradingsystem;
use investmentbanktradingsystem;

/**

以下是关于投资银行交易部门的数据库示例数据集，包含了13个不同维度的数据表和20个不同类型的字段，以满足数据分析的需求。该数据集包含了交易编号、日期、时间、交易金额、交易数量、买入时间、卖出时间等相关数据字段。

投资银行交易部门数据库

- 1.交易员表 (Traders)
- 2.客户表 (Clients)
- 3.交易类型表 (TransactionTypes)
- 4.交易表 (Transactions)
- 5.证券表 (Securities)
- 6.市场表 (Markets)
- 7.交易账户表 (TradingAccounts)
- 8.买入订单表 (BuyOrders)
- 9.卖出订单表 (SellOrders)
- 10.股票持仓表 (StockPositions)
- 11.资金账户表 (CashAccounts)
- 12.资金流水表 (CashFlows)
- 13.交易日志表 (TransactionLogs)

字段类型

- INT
- VARCHAR
- DATE
- DECIMAL
- BOOLEAN
- TEXT
- DATETIME
- TIME
- FLOAT
- CHAR
- BINARY
- BLOB
- ENUM
- JSON
- SET
- YEAR
- TIMESTAMP
- MEDIUMINT
- TINYINT
- BIGINT

*/

-- 创建投行交易部门数据表

-- 交易员表
CREATE TABLE Traders (
    TraderID INT PRIMARY KEY,
    TraderName VARCHAR(100),
    Department VARCHAR(100),
    JoinDate DATE,
    Status VARCHAR(10)
);

-- 客户表
CREATE TABLE Clients (
    ClientID INT PRIMARY KEY,
    ClientName VARCHAR(100),
    Industry VARCHAR(100),
    Country VARCHAR(50),
    ContactPerson VARCHAR(100),
    ContactNumber VARCHAR(20),
    Email VARCHAR(100)
);

-- 交易类型表
CREATE TABLE TransactionTypes (
    TypeID INT PRIMARY KEY,
    TypeName VARCHAR(100),
    Description TEXT
);

-- 交易表
CREATE TABLE Transactions (
    TransactionID INT PRIMARY KEY,
    TraderID INT,
    ClientID INT,
    TransactionTypeID INT,
    SecurityID INT,
    MarketID INT,
    TransactionDate DATE,
    TransactionTime TIME,
    TransactionAmount DECIMAL(10, 2),
    TransactionQuantity INT,
    BuyTime DATETIME,
    SellTime DATETIME,
    FOREIGN KEY (TraderID) REFERENCES Traders(TraderID),
    FOREIGN KEY (ClientID) REFERENCES Clients(ClientID),
    FOREIGN KEY (TransactionTypeID) REFERENCES TransactionTypes(TypeID)
);

-- 证券表
CREATE TABLE Securities (
    SecurityID INT PRIMARY KEY,
    SecurityName VARCHAR(100),
    Symbol VARCHAR(20),
    Description TEXT,
    MarketID INT,
    InitialPrice DECIMAL(10, 2),
    InitialDate DATE,
    FOREIGN KEY (MarketID) REFERENCES Markets(MarketID)
);

-- 市场表
CREATE TABLE Markets (
    MarketID INT PRIMARY KEY,
    MarketName VARCHAR(100),
    Country VARCHAR(50),
    Exchange VARCHAR(100)
);

-- 交易账户表
CREATE TABLE TradingAccounts (
    AccountID INT PRIMARY KEY,
    ClientID INT,
    AccountType VARCHAR(10) CHECK (AccountType IN ('Cash', 'Margin')),
    Balance DECIMAL(15, 2),
    FOREIGN KEY (ClientID) REFERENCES Clients(ClientID)
);


-- 买入订单表
CREATE TABLE BuyOrders (
    OrderID INT PRIMARY KEY,
    TransactionID INT,
    OrderDate DATE,
    OrderTime TIME,
    OrderQuantity INT,
    OrderAmount DECIMAL(10, 2),
    FOREIGN KEY (TransactionID) REFERENCES Transactions(TransactionID)
);

-- 卖出订单表
CREATE TABLE SellOrders (
    OrderID INT PRIMARY KEY,
    TransactionID INT,
    OrderDate DATE,
    OrderTime TIME,
    OrderQuantity INT,
    OrderAmount DECIMAL(10, 2),
    FOREIGN KEY (TransactionID) REFERENCES Transactions(TransactionID)
);

-- 股票持仓表
CREATE TABLE StockPositions (
    PositionID INT PRIMARY KEY,
    AccountID INT,
    SecurityID INT,
    Quantity INT,
    AveragePrice DECIMAL(10, 2),
    FOREIGN KEY (AccountID) REFERENCES TradingAccounts(AccountID),
    FOREIGN KEY (SecurityID) REFERENCES Securities(SecurityID)
);

-- 资金账户表
CREATE TABLE CashAccounts (
    AccountID INT PRIMARY KEY,
    ClientID INT,
    Balance DECIMAL(15, 2),
    FOREIGN KEY (ClientID) REFERENCES Clients(ClientID)
);

-- 资金流水表
CREATE TABLE CashFlows (
    FlowID INT PRIMARY KEY,
    AccountID INT,
    TransactionID INT,
    FlowDate DATE,
    FlowTime TIME,
    Amount DECIMAL(10, 2),
    FlowType varchar(10) check (flowtype in ('Deposit', 'Withdrawal', 'Interest', 'Fee')),
    FOREIGN KEY (AccountID) REFERENCES CashAccounts(AccountID),
    FOREIGN KEY (TransactionID) REFERENCES Transactions(TransactionID)
);

-- 交易日志表
CREATE TABLE TransactionLogs (
    LogID INT PRIMARY KEY,
    TransactionID INT,
    LogDate DATE,
    LogTime TIME,
    LogDetails TEXT,
    FOREIGN KEY (TransactionID) REFERENCES Transactions(TransactionID)
);

-- 插入交易数据

-- 交易员表 (Traders)
INSERT INTO investmentbanktradingsystem.dbo.Traders (TraderID, TraderName, Department, JoinDate, Status) VALUES
(1, 'Alice Johnson', 'Equity', '2019-05-21', 1),
(2, 'Bob Smith', 'Fixed Income', '2018-11-14', 1),
(3, 'Carol White', 'Derivatives', '2020-01-10', 1),
(4, 'David King', 'Commodities', '2021-07-15', 1),
(5, 'Eve Adams', 'Foreign Exchange', '2017-09-05', 1),
(6, 'Franklin White', 'Risk Management', '2022-02-20', 1),
(7, 'George Knight', 'Equity', '2021-03-01', 1),
(8, 'Helen Lee', 'Fixed Income', '2020-06-15', 1),
(9, 'Ivan Kim', 'Derivatives', '2019-10-20', 1),
(10, 'Jackie Chan', 'Commodities', '2018-12-01', 1),
(11, 'Karen Hall', 'Foreign Exchange', '2017-08-05', 1),
(12, 'Leo Wang', 'Risk Management', '2021-11-22', 1),
(13, 'Mona Scott', 'Equity', '2022-04-14', 1),
(14, 'Nathaniel Parker', 'Fixed Income', '2020-01-19', 1),
(15, 'Olivia Adams', 'Derivatives', '2019-07-25', 1),
(16, 'Paul Martin', 'Commodities', '2018-09-30', 1),
(17, 'Quincy Zhang', 'Foreign Exchange', '2021-02-10', 1),
(18, 'Rachel Thompson', 'Risk Management', '2020-05-07', 1),
(19, 'Steve Harris', 'Equity', '2019-11-18', 1),
(20, 'Tina Turner', 'Fixed Income', '2018-03-22', 1),
(21, 'Ursula King', 'Derivatives', '2021-07-27', 1);

-- 交易表 (Transactions)
INSERT INTO investmentbanktradingsystem.dbo.Transactions (TransactionID, TraderID, ClientID, TransactionTypeID, SecurityID, MarketID, TransactionDate, TransactionTime, TransactionAmount, TransactionQuantity, BuyTime, SellTime) VALUES
(1, 1, 1, 1, 1, 1, '2023-05-01', '09:30:00', 15000.00, 100, '2023-05-01 09:30:00', NULL),
(2, 2, 2, 2, 2, 1, '2023-05-02', '10:00:00', 30000.00, 200, NULL, '2023-05-02 10:00:00'),
(3, 3, 3, 3, 3, 2, '2023-05-03', '11:30:00', 5000.00, 50, '2023-05-03 11:30:00', NULL),
(4, 4, 4, 4, 1, 3, '2023-05-04', '12:00:00', 20000.00, 100, NULL, '2023-05-04 12:00:00'),
(5, 5, 5, 5, 2, 2, '2023-05-05', '13:00:00', 25000.00, 150, '2023-05-05 13:00:00', NULL),
(6, 7, 7, 6, 4, 4, '2023-05-10', '09:30:00', 18000.00, 100, '2023-05-10 09:30:00', NULL),
(7, 8, 8, 7, 5, 5, '2023-05-11', '10:00:00', 28000.00, 200, NULL, '2023-05-11 10:00:00'),
(8, 9, 9, 8, 6, 4, '2023-05-12', '11:30:00', 3500.00, 50, '2023-05-12 11:30:00', NULL),
(9, 10, 10, 9, 4, 3, '2023-05-13', '12:00:00', 22000.00, 100, NULL, '2023-05-13 12:00:00'),
(10, 11, 11, 10, 5, 2, '2023-05-14', '13:00:00', 30000.00, 150, '2023-05-14 13:00:00', NULL),
(11, 12, 12, 11, 6, 1, '2023-05-15', '14:00:00', 15000.00, 100, '2023-05-15 14:00:00', NULL),
(12, 13, 13, 12, 4, 5, '2023-05-16', '15:00:00', 36000.00, 200, NULL, '2023-05-16 15:00:00'),
(13, 14, 14, 13, 5, 4, '2023-05-17', '16:30:00', 7200.00, 50, '2023-05-17 16:30:00', NULL),
(14, 15, 15, 14, 6, 3, '2023-05-18', '17:00:00', 21000.00, 100, NULL, '2023-05-18 17:00:00'),
(15, 16, 16, 15, 4, 2, '2023-05-19', '18:00:00', 28500.00, 150, '2023-05-19 18:00:00', NULL),
(16, 17, 17, 16, 5, 1, '2023-05-20', '09:30:00', 14400.00, 100, '2023-05-20 09:30:00', NULL),
(17, 18, 18, 17, 6, 5, '2023-05-21', '10:00:00', 36500.00, 200, NULL, '2023-05-21 10:00:00'),
(18, 19, 19, 18, 4, 4, '2023-05-22', '11:30:00', 7500.00, 50, '2023-05-22 11:30:00', NULL),
(19, 20, 20, 19, 5, 3, '2023-05-23', '12:00:00', 22000.00, 100, NULL, '2023-05-23 12:00:00'),
(20, 21, 21, 20, 6, 2, '2023-05-24', '13:00:00', 45000.00, 150, '2023-05-24 13:00:00', NULL);


-- 客户表 (Clients)
INSERT INTO investmentbanktradingsystem.dbo.Clients (ClientID, ClientName, Industry, Country, ContactPerson, ContactNumber, Email) VALUES
(1, 'Alpha Corp', 'Technology', 'USA', 'David Brown', '123-456-7890', 'david.brown@alphacorp.com'),
(2, 'Beta LLC', 'Finance', 'UK', 'Emma Green', '234-567-8901', 'emma.green@betallc.co.uk'),
(3, 'Gamma Inc', 'Healthcare', 'Germany', 'Frank Black', '345-678-9012', 'frank.black@gammainc.de'),
(4, 'Delta Partners', 'Real Estate', 'Canada', 'George White', '456-789-0123', 'george.white@deltapartners.ca'),
(5, 'Epsilon Ventures', 'Energy', 'Australia', 'Hannah Blue', '567-890-1234', 'hannah.blue@epsilonventures.au'),
(6, 'Zeta Enterprises', 'Consumer Goods', 'Japan', 'Ian Gold', '678-901-2345', 'ian.gold@zetaenterprises.jp'),
(7, 'Eta Solutions', 'Technology', 'France', 'Oscar Lewis', '789-012-3456', 'oscar.lewis@etasolutions.fr'),
(8, 'Theta Holdings', 'Finance', 'Italy', 'Patricia Lee', '890-123-4567', 'patricia.lee@thetaholdings.it'),
(9, 'Iota Group', 'Healthcare', 'Spain', 'Quincy Brown', '901-234-5678', 'quincy.brown@iotagroup.es'),
(10, 'Kappa Enterprises', 'Real Estate', 'Netherlands', 'Rachel Green', '012-345-6789', 'rachel.green@kappaenterprises.nl'),
(11, 'Lambda Investments', 'Energy', 'Sweden', 'Sarah White', '123-456-7891', 'sarah.white@lambdainvestments.se'),
(12, 'Mu Services', 'Consumer Goods', 'Switzerland', 'Thomas Black', '234-567-8902', 'thomas.black@muservices.ch'),
(13, 'Nu Technologies', 'Technology', 'Norway', 'Ursula Brown', '345-678-9013', 'ursula.brown@nutechnologies.no'),
(14, 'Xi Ventures', 'Finance', 'Denmark', 'Victor White', '456-789-0124', 'victor.white@xivertures.dk'),
(15, 'Omicron LLC', 'Healthcare', 'Belgium', 'Wendy Adams', '567-890-1235', 'wendy.adams@omicronllc.be'),
(16, 'Pi Capital', 'Real Estate', 'Finland', 'Xavier Black', '678-901-2346', 'xavier.black@picapital.fi'),
(17, 'Rho Partners', 'Energy', 'Austria', 'Yvonne Green', '789-012-3457', 'yvonne.green@rhopartners.at'),
(18, 'Sigma Consulting', 'Consumer Goods', 'Portugal', 'Zachary Brown', '890-123-4568', 'zachary.brown@sigmaconsulting.pt'),
(19, 'Tau Solutions', 'Technology', 'Greece', 'Alex Johnson', '901-234-5679', 'alex.johnson@tausolutions.gr'),
(20, 'Upsilon Advisors', 'Finance', 'Ireland', 'Barbara Lee', '012-345-6780', 'barbara.lee@upsilonadvisors.ie'),
(21, 'Phi Group', 'Healthcare', 'Luxembourg', 'Charles Kim', '123-456-7892', 'charles.kim@phigroup.lu');


-- 交易类型表 (TransactionTypes)
INSERT INTO investmentbanktradingsystem.dbo.TransactionTypes (TypeID, TypeName, Description) VALUES
(1, 'Buy', 'Purchase of securities'),
(2, 'Sell', 'Sale of securities'),
(3, 'Short Sell', 'Sale of borrowed securities'),
(4, 'Cover', 'Purchase of securities to cover a short sale'),
(5, 'Transfer', 'Transfer of funds or securities'),
(6, 'Dividend', 'Dividend payment'),
(7, 'Interest', 'Interest payment'),
(8, 'Fee', 'Transaction fee'),
(9, 'Reinvestment', 'Reinvestment of dividends'),
(10, 'Split', 'Stock split'),
(11, 'Merge', 'Company merger'),
(12, 'Spin-off', 'Company spin-off'),
(13, 'Buyback', 'Stock buyback'),
(14, 'Warrant', 'Warrant exercise'),
(15, 'Option', 'Option exercise'),
(16, 'ETF', 'ETF trade'),
(17, 'Mutual Fund', 'Mutual fund trade'),
(18, 'Bonds', 'Bond trade'),
(19, 'CD', 'Certificate of Deposit trade'),
(20, 'Futures', 'Futures trade');


-- 市场表 (Markets)
INSERT INTO investmentbanktradingsystem.dbo.Markets (MarketID, MarketName, Country, Exchange) VALUES
(1, 'New York Stock Exchange', 'USA', 'NYSE'),
(2, 'London Stock Exchange', 'UK', 'LSE'),
(3, 'Frankfurt Stock Exchange', 'Germany', 'FSE'),
(4, 'Tokyo Stock Exchange', 'Japan', 'TSE'),
(5, 'Hong Kong Stock Exchange', 'Hong Kong', 'HKEX'),
(6, 'Shanghai Stock Exchange', 'China', 'SSE'),
(7, 'National Stock Exchange of India', 'India', 'NSE'),
(8, 'Australian Securities Exchange', 'Australia', 'ASX'),
(9, 'Toronto Stock Exchange', 'Canada', 'TSX'),
(10, 'Euronext', 'Netherlands', 'ENX'),
(11, 'Borsa Italiana', 'Italy', 'BIT'),
(12, 'Swiss Exchange', 'Switzerland', 'SIX'),
(13, 'BM&FBOVESPA', 'Brazil', 'BVMF'),
(14, 'Moscow Exchange', 'Russia', 'MOEX'),
(15, 'Korea Exchange', 'South Korea', 'KRX'),
(16, 'Johannesburg Stock Exchange', 'South Africa', 'JSE'),
(17, 'Saudi Stock Exchange', 'Saudi Arabia', 'Tadawul'),
(18, 'Bursa Malaysia', 'Malaysia', 'MYX'),
(19, 'Singapore Exchange', 'Singapore', 'SGX'),
(20, 'New Zealand Exchange', 'New Zealand', 'NZX');


-- 证券表 (Securities)
INSERT INTO investmentbanktradingsystem.dbo.Securities (SecurityID, SecurityName, Symbol, Description, MarketID, InitialPrice, InitialDate) VALUES
(1, 'Apple Inc.', 'AAPL', 'Technology Company', 1, 150.00, '1980-12-12'),
(2, 'Microsoft Corp', 'MSFT', 'Software Company', 1, 250.00, '1986-03-13'),
(3, 'HSBC Holdings', 'HSBC', 'Financial Services', 2, 50.00, '1991-05-11'),
(4, 'Toyota Motor Corp', 'TM', 'Automotive Company', 3, 180.00, '1949-05-16'),
(5, 'Google Inc.', 'GOOGL', 'Technology Company', 1, 2800.00, '2004-08-19'),
(6, 'Amazon.com Inc.', 'AMZN', 'E-commerce Company', 1, 3500.00, '1997-05-15'),
(7, 'Tencent Holdings', 'TCEHY', 'Technology Company', 6, 600.00, '2004-06-16'),
(8, 'Reliance Industries', 'RELI', 'Conglomerate', 7, 1200.00, '1973-05-08'),
(9, 'BHP Billiton', 'BHP', 'Mining Company', 8, 1500.00, '2001-07-29'),
(10, 'Royal Bank of Canada', 'RY', 'Financial Services', 9, 100.00, '1869-06-22'),
(11, 'Unilever NV', 'UNA', 'Consumer Goods', 10, 50.00, '1930-07-29'),
(12, 'Enel SpA', 'ENEL', 'Energy Company', 11, 70.00, '1962-12-06'),
(13, 'Nestle SA', 'NESN', 'Food and Beverage', 12, 100.00, '1905-03-17'),
(14, 'Petrobras', 'PBR', 'Oil and Gas', 13, 25.00, '1953-10-03'),
(15, 'Gazprom', 'GAZP', 'Energy Company', 14, 40.00, '1989-08-15'),
(16, 'Samsung Electronics', '005930', 'Technology Company', 15, 1500.00, '1969-11-19'),
(17, 'Sasol', 'SOL', 'Energy and Chemical', 16, 30.00, '1950-09-26'),
(18, 'Saudi Aramco', '2222', 'Energy Company', 17, 35.00, '1988-11-08'),
(19, 'CIMB Group', 'CIMB', 'Financial Services', 18, 10.00, '1924-09-01'),
(20, 'DBS Bank', 'D05', 'Financial Services', 19, 25.00, '1968-07-16');

-- 交易账户表 (TradingAccounts)
INSERT INTO investmentbanktradingsystem.dbo.TradingAccounts (AccountID, ClientID, AccountType, Balance) VALUES
(1, 1, 'Cash', 100000.00),
(2, 2, 'Margin', 200000.00),
(3, 3, 'Cash', 150000.00),
(4, 4, 'Cash', 300000.00),
(5, 5, 'Margin', 400000.00),
(6, 6, 'Cash', 250000.00),
(7, 7, 'Cash', 350000.00),
(8, 8, 'Margin', 450000.00),
(9, 9, 'Cash', 300000.00),
(10, 10, 'Margin', 400000.00),
(11, 11, 'Cash', 200000.00),
(12, 12, 'Margin', 500000.00),
(13, 13, 'Cash', 250000.00),
(14, 14, 'Margin', 550000.00),
(15, 15, 'Cash', 150000.00),
(16, 16, 'Margin', 600000.00),
(17, 17, 'Cash', 100000.00),
(18, 18, 'Margin', 650000.00),
(19, 19, 'Cash', 75000.00),
(20, 20, 'Margin', 700000.00),
(21, 21, 'Cash', 50000.00);


-- 买入订单表 (BuyOrders)
INSERT INTO investmentbanktradingsystem.dbo.BuyOrders (OrderID, TransactionID, OrderDate, OrderTime, OrderQuantity, OrderAmount) VALUES
(1, 1, '2023-05-01', '10:00:00', 100, 15000.00),
(2, 2, '2023-05-02', '11:00:00', 200, 30000.00),
(3, 3, '2023-05-03', '11:00:00', 50, 5000.00),
(4, 4, '2023-05-04', '12:00:00', 100, 20000.00),
(5, 5, '2023-05-05', '13:00:00', 150, 22500.00),
(6, 1, '2023-05-06', '14:00:00', 200, 30000.00),
(7, 2, '2023-05-07', '15:00:00', 250, 37500.00),
(8, 3, '2023-05-08', '16:00:00', 300, 45000.00),
(9, 6, '2023-05-10', '09:35:00', 100, 18000.00),
(10, 7, '2023-05-11', '10:05:00', 200, 28000.00),
(11, 8, '2023-05-12', '11:35:00', 50, 3500.00),
(12, 9, '2023-05-13', '12:05:00', 100, 22000.00),
(13, 10, '2023-05-14', '13:05:00', 150, 30000.00),
(14, 11, '2023-05-15', '14:05:00', 100, 15000.00),
(15, 12, '2023-05-16', '15:05:00', 200, 36000.00),
(16, 13, '2023-05-17', '16:35:00', 50, 7200.00),
(17, 14, '2023-05-18', '17:05:00', 100, 21000.00),
(18, 15, '2023-05-19', '18:05:00', 150, 28500.00),
(19, 16, '2023-05-20', '09:35:00', 100, 14400.00),
(20, 17, '2023-05-21', '10:05:00', 200, 36500.00),
(21, 18, '2023-05-22', '11:35:00', 50, 7500.00),
(22, 19, '2023-05-23', '12:05:00', 100, 22000.00),
(23, 20, '2023-05-24', '13:05:00', 150, 45000.00);


-- 卖出订单表 (SellOrders)
INSERT INTO investmentbanktradingsystem.dbo.SellOrders (OrderID, TransactionID, OrderDate, OrderTime, OrderQuantity, OrderAmount) VALUES
(1, 3, '2023-05-03', '12:00:00', 50, 7500.00),
(2, 4, '2023-05-04', '13:00:00', 100, 20000.00),
(3, 5, '2023-05-05', '14:00:00', 150, 22500.00),
(4, 1, '2023-05-06', '15:00:00', 200, 30000.00),
(5, 2, '2023-05-07', '16:00:00', 250, 37500.00),
(6, 3, '2023-05-08', '17:00:00', 300, 45000.00),
(7, 4, '2023-05-09', '18:00:00', 350, 52500.00),
(8, 6, '2023-05-10', '09:35:00', 100, 18000.00),
(9, 7, '2023-05-11', '10:05:00', 200, 28000.00),
(10, 8, '2023-05-12', '11:35:00', 50, 3500.00),
(11, 9, '2023-05-13', '12:05:00', 100, 22000.00),
(12, 10, '2023-05-14', '13:05:00', 150, 30000.00),
(13, 11, '2023-05-15', '14:05:00', 100, 15000.00),
(14, 12, '2023-05-16', '15:05:00', 200, 36000.00),
(15, 13, '2023-05-17', '16:35:00', 50, 7200.00),
(16, 14, '2023-05-18', '17:05:00', 100, 21000.00),
(17, 15, '2023-05-19', '18:05:00', 150, 28500.00),
(18, 16, '2023-05-20', '09:35:00', 100, 14400.00),
(19, 17, '2023-05-21', '10:05:00', 200, 36500.00),
(20, 18, '2023-05-22', '11:35:00', 50, 7500.00),
(21, 19, '2023-05-23', '12:05:00', 100, 22000.00),
(22, 20, '2023-05-24', '13:05:00', 150, 45000.00);

-- 股票持仓表 (StockPositions)
INSERT INTO investmentbanktradingsystem.dbo.StockPositions (PositionID, AccountID, SecurityID, Quantity, AveragePrice) VALUES
(1, 1, 1, 100, 150.00),
(2, 2, 2, 200, 250.00),
(3, 3, 3, 150, 50.00),
(4, 4, 4, 100, 180.00),
(5, 5, 5, 200, 2800.00),
(6, 6, 6, 300, 3500.00),
(7, 7, 7, 150, 600.00),
(8, 8, 8, 200, 1200.00),
(9, 9, 9, 100, 1500.00),
(10, 10, 10, 100, 100.00),
(11, 11, 11, 150, 50.00),
(12, 12, 12, 100, 70.00),
(13, 13, 13, 200, 100.00),
(14, 14, 14, 50, 25.00),
(15, 15, 15, 100, 40.00),
(16, 16, 16, 150, 1500.00),
(17, 17, 17, 100, 30.00),
(18, 18, 18, 200, 35.00),
(19, 19, 19, 50, 10.00),
(20, 20, 20, 100, 25.00),
(21, 21, 1, 150, 50.00);



-- 资金账户表 (CashAccounts)
INSERT INTO investmentbanktradingsystem.dbo.CashAccounts (AccountID, ClientID, Balance) VALUES
(1, 1, 50000.00),
(2, 2, 100000.00),
(3, 3, 75000.00),
(4, 4, 120000.00),
(5, 5, 180000.00),
(6, 6, 90000.00),
(7, 7, 150000.00),
(8, 8, 200000.00),
(9, 9, 180000.00),
(10, 10, 175000.00),
(11, 11, 220000.00),
(12, 12, 160000.00),
(13, 13, 190000.00),
(14, 14, 210000.00),
(15, 15, 195000.00),
(16, 16, 170000.00),
(17, 17, 185000.00),
(18, 18, 165000.00),
(19, 19, 155000.00),
(20, 20, 175000.00),
(21, 21, 140000.00);


-- 资金流水表 (CashFlows)
INSERT INTO investmentbanktradingsystem.dbo.CashFlows (FlowID, AccountID, TransactionID, FlowDate, FlowTime, Amount, FlowType) VALUES
(1, 1, 1, '2023-05-01', '10:00:00', 15000.00, 'Deposit'),
(2, 2, 2, '2023-05-02', '11:00:00', 30000.00, 'Deposit'),
(3, 1, 3, '2023-05-03', '11:30:00', 5000.00, 'Deposit'),
(4, 2, 4, '2023-05-04', '12:30:00', 20000.00, 'Withdrawal'),
(5, 3, 5, '2023-05-05', '13:30:00', 25000.00, 'Deposit'),
(6, 4, 1, '2023-05-06', '14:30:00', 30000.00, 'Withdrawal'),
(7, 5, 2, '2023-05-07', '15:30:00', 37500.00, 'Deposit'),
(8, 6, 3, '2023-05-08', '16:30:00', 45000.00, 'Withdrawal'),
(9, 1, 6, '2023-05-10', '10:00:00', 18000.00, 'Deposit'),
(10, 2, 7, '2023-05-11', '11:00:00', 28000.00, 'Withdrawal'),
(11, 3, 8, '2023-05-12', '12:00:00', 3500.00, 'Deposit'),
(12, 4, 9, '2023-05-13', '13:00:00', 22000.00, 'Withdrawal'),
(13, 5, 10, '2023-05-14', '14:00:00', 30000.00, 'Deposit'),
(14, 6, 11, '2023-05-15', '15:00:00', 15000.00, 'Withdrawal'),
(15, 7, 12, '2023-05-16', '16:00:00', 36000.00, 'Deposit'),
(16, 8, 13, '2023-05-17', '17:00:00', 7200.00, 'Withdrawal'),
(17, 9, 14, '2023-05-18', '18:00:00', 21000.00, 'Deposit'),
(18, 10, 15, '2023-05-19', '19:00:00', 28500.00, 'Withdrawal'),
(19, 11, 16, '2023-05-20', '09:00:00', 14400.00, 'Deposit'),
(20, 12, 17, '2023-05-21', '10:00:00', 36500.00, 'Withdrawal'),
(21, 13, 18, '2023-05-22', '11:00:00', 7500.00, 'Deposit'),
(22, 14, 19, '2023-05-23', '12:00:00', 22000.00, 'Withdrawal'),
(23, 15, 20, '2023-05-24', '13:00:00', 45000.00, 'Deposit');

-- 交易日志表 (TransactionLogs)
INSERT INTO investmentbanktradingsystem.dbo.TransactionLogs (LogID, TransactionID, LogDate, LogTime, LogDetails) VALUES
(1, 1, '2023-05-01', '10:05:00', 'Buy order executed'),
(2, 2, '2023-05-02', '11:05:00', 'Buy order executed'),
(3, 3, '2023-05-03', '11:45:00', 'Sell order executed'),
(4, 4, '2023-05-04', '12:45:00', 'Buy order executed'),
(5, 5, '2023-05-05', '13:45:00', 'Sell order executed'),
(6, 1, '2023-05-06', '14:45:00', 'Buy order executed'),
(7, 2, '2023-05-07', '15:45:00', 'Sell order executed'),
(8, 3, '2023-05-08', '16:45:00', 'Buy order executed'),
(9, 6, '2023-05-10', '10:05:00', 'Dividend payment received'),
(10, 7, '2023-05-11', '11:05:00', 'Interest payment received'),
(11, 8, '2023-05-12', '12:05:00', 'Fee payment made'),
(12, 9, '2023-05-13', '13:05:00', 'Reinvestment executed'),
(13, 10, '2023-05-14', '14:05:00', 'Stock split executed'),
(14, 11, '2023-05-15', '15:05:00', 'Company merger completed'),
(15, 12, '2023-05-16', '16:05:00', 'Spin-off completed'),
(16, 13, '2023-05-17', '17:05:00', 'Stock buyback executed'),
(17, 14, '2023-05-18', '18:05:00', 'Warrant exercised'),
(18, 15, '2023-05-19', '19:05:00', 'Option exercised'),
(19, 16, '2023-05-20', '09:05:00', 'ETF trade executed'),
(20, 17, '2023-05-21', '10:05:00', 'Mutual fund trade executed'),
(21, 18, '2023-05-22', '11:05:00', 'Bond trade executed'),
(22, 19, '2023-05-23', '12:05:00', 'Certificate of Deposit trade executed'),
(23, 20, '2023-05-24', '13:05:00', 'Futures trade executed');

