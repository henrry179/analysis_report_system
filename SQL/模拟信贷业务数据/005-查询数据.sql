-- 创建数据库
create DATABASE myjdatas;
use myjdatas;

-- 创建统计年鉴数据库
create database tjnjdatas;
use tjnjdatas;

-- 创建数据库
create database yqcydatas;
use yqcydatas;

select * from [yqcydatas].[dbo].[Combined_Report];

-- 查询mydatas数据库信息
select * from [mydatas].[dbo].[Categories];
select * from [mydatas].[dbo].[Customers];
select * from [mydatas].[dbo].[Employees];
select * from [mydatas].[dbo].[Inventory];
select * from [mydatas].[dbo].[OrderDetails];
select * from [mydatas].[dbo].[Orders];
select * from [mydatas].[dbo].[Payments];
select * from [mydatas].[dbo].[Products];
select * from [mydatas].[dbo].[Returns];
select * from [mydatas].[dbo].[Shippers];
select * from [mydatas].[dbo].[Suppliers];

-- 查询物流系统数据库信息
select * from [logisticsystem].[dbo].[Invoices];
select * from [logisticsystem].[dbo].[Customers];
select * from [logisticsystem].[dbo].[Inventory];
select * from [logisticsystem].[dbo].[Orders];
select * from [logisticsystem].[dbo].[Payments];
select * from [logisticsystem].[dbo].[Products];
select * from [logisticsystem].[dbo].[Returns];
select * from [logisticsystem].[dbo].[Shipping];
select * from [logisticsystem].[dbo].[Suppliers];
select * from [logisticsystem].[dbo].[warehouses];

-- 查询银行信贷系统数据库信息
select * from [banksystem].[dbo].[BankAccounts];
select * from [banksystem].[dbo].[BankCustomers];
select * from [banksystem].[dbo].[Branches];
select * from [banksystem].[dbo].[Collateral];
select * from [banksystem].[dbo].[CreditScores];
select * from [banksystem].[dbo].[Employees];
select * from [banksystem].[dbo].[Guarantors];
select * from [banksystem].[dbo].[Loans];
select * from [banksystem].[dbo].[Repayments];
select * from [banksystem].[dbo].[Transactions];

-- 查询投资银行交易系统数据库信息
select * from [investmentbanktradingsystem].[dbo].[Buyorders];
select * from [investmentbanktradingsystem].[dbo].[Clients];
select * from [investmentbanktradingsystem].[dbo].[Markets];
select * from [investmentbanktradingsystem].[dbo].[Securities];
select * from [investmentbanktradingsystem].[dbo].[SellOrders];
select * from [investmentbanktradingsystem].[dbo].[StockPositions];
select * from [investmentbanktradingsystem].[dbo].[Traders];
select * from [investmentbanktradingsystem].[dbo].[TradingAccounts];
select * from [investmentbanktradingsystem].[dbo].[TransactionLogs];
select * from [investmentbanktradingsystem].[dbo].[Transactions];
select * from [investmentbanktradingsystem].[dbo].[TransactionTypes];

-- 查询电商餐饮系统数据库信息
select * from [FreshFoodEcommerceSystem].[dbo].[Categories];
select * from [FreshFoodEcommerceSystem].[dbo].[Coupons];
select * from [FreshFoodEcommerceSystem].[dbo].[Customers];
select * from [FreshFoodEcommerceSystem].[dbo].[Inventory];
select * from [FreshFoodEcommerceSystem].[dbo].[Invoices];
select * from [FreshFoodEcommerceSystem].[dbo].[Orders];
select * from [FreshFoodEcommerceSystem].[dbo].[Payments];
select * from [FreshFoodEcommerceSystem].[dbo].[Products];
select * from [FreshFoodEcommerceSystem].[dbo].[Returns];
select * from [FreshFoodEcommerceSystem].[dbo].[Reviews];
select * from [FreshFoodEcommerceSystem].[dbo].[Shipping];
select * from [FreshFoodEcommerceSystem].[dbo].[Suppliers];
select * from [FreshFoodEcommerceSystem].[dbo].[Warehouses];

-- 查询交易数据库信息
select * from [Tradingdatas].[dbo].[Trades];
select * from [Tradingdatas].[dbo].[Traders];
select * from [Tradingdatas].[dbo].[TradeDetails];
select * from [Tradingdatas].[dbo].[TradePerformance];
select * from [Tradingdatas].[dbo].[Transactions];
select * from [Tradingdatas].[dbo].[Allocations];
select * from [Tradingdatas].[dbo].[Benchmarks];
select * from [Tradingdatas].[dbo].[Clients];
select * from [Tradingdatas].[dbo].[Compliance];
select * from [Tradingdatas].[dbo].[Dividends];
select * from [Tradingdatas].[dbo].[Fees];
select * from [Tradingdatas].[dbo].[InterestRates];
select * from [Tradingdatas].[dbo].[KellyRatios];
select * from [Tradingdatas].[dbo].[MarketData];
select * from [Tradingdatas].[dbo].[Orders];
select * from [Tradingdatas].[dbo].[Portfolios];
select * from [Tradingdatas].[dbo].[Positions];
select * from [Tradingdatas].[dbo].[Reports];
select * from [Tradingdatas].[dbo].[RiskMetrics];
select * from [Tradingdatas].[dbo].[Strategies];
select * from [Tradingdatas].[dbo].[Accounts];

select * from [hftradingdatas].[dbo].[local_Trade_report_1];
select * from [hftradingdatas].[dbo].[local_Trade_report_2];
select * from [hftradingdatas].[dbo].[local_Trade_report_3];
select * from [hftradingdatas].[dbo].[local_Trade_report_4];
select * from [hftradingdatas].[dbo].[local_Trade_report_5];
select * from [hftradingdatas].[dbo].[local_Trade_report_6];
select * from [hftradingdatas].[dbo].[local_Trade_report_7];
select * from [hftradingdatas].[dbo].[local_Trade_report_8];
select * from [hftradingdatas].[dbo].[local_Trade_report_9];
select * from [hftradingdatas].[dbo].[local_Trade_report_10];
select * from [hftradingdatas].[dbo].[local_Trade_report_11];
select * from [hftradingdatas].[dbo].[local_Trade_report_12];
select * from [hftradingdatas].[dbo].[local_Trade_report_13];
select * from [hftradingdatas].[dbo].[local_Trade_report_14];
select * from [hftradingdatas].[dbo].[local_Trade_report_15];
select * from [hftradingdatas].[dbo].[local_Trade_report_16];
select * from [hftradingdatas].[dbo].[local_Trade_report_17];
select * from [hftradingdatas].[dbo].[local_Trade_report_18];
select * from [hftradingdatas].[dbo].[local_Trade_report_19];
select * from [hftradingdatas].[dbo].[local_Trade_report_20];
select * from [hftradingdatas].[dbo].[local_Trade_report_21];
select * from [hftradingdatas].[dbo].[local_Trade_report_22];
select * from [hftradingdatas].[dbo].[Combined_Trade_Report1];

select * from [myjdatas].[dbo].[23年全年单店单品销售明细];

select * from [myjdatas].[dbo].[23年1月单店单品销售明细];

select * from [myjdatas].dbo.[Combined_myj_Report];
select * from [myjdatas].dbo.[演示数据百万条];