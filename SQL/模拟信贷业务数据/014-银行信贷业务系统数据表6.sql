-- 使用指定的数据库
create database banksystem;
use banksystem;

-- 银行信贷业务系统数据库的数据表
/**
客户表 (BankCustomers)
账户表 (BankAccounts)
贷款表 (Loans)
抵押表 (Collateral)
还款表 (Repayments)
交易表 (Transactions)
分行表 (Branches)
员工表 (Employees)
信用评分表 (CreditScores)
担保人表 (Guarantors)
*/

-- 第一种方法创建新表并插入数据
-- 创建新表
-- 客户表
CREATE TABLE BankCustomers (
    CustomerID INT PRIMARY KEY,
    CustomerName VARCHAR(100),
    ContactInfo VARCHAR(100),
    Address VARCHAR(255)
);

-- 账户表
CREATE TABLE BankAccounts (
    AccountID INT PRIMARY KEY,
    CustomerID INT,
    AccountType VARCHAR(50),
    Balance DECIMAL(10, 2),
    BranchID INT,
    FOREIGN KEY (CustomerID) REFERENCES BankCustomers(CustomerID)
);

-- 贷款表
CREATE TABLE Loans (
    LoanID INT PRIMARY KEY,
    CustomerID INT,
    LoanAmount DECIMAL(10, 2),
    InterestRate DECIMAL(5, 2),
    LoanTerm INT,
    StartDate DATE,
    FOREIGN KEY (CustomerID) REFERENCES BankCustomers(CustomerID)
);

-- 抵押表
CREATE TABLE Collateral (
    CollateralID INT PRIMARY KEY,
    LoanID INT,
    CollateralType VARCHAR(100),
    CollateralValue DECIMAL(10, 2),
    FOREIGN KEY (LoanID) REFERENCES Loans(LoanID)
);

-- 还款表
CREATE TABLE Repayments (
    RepaymentID INT PRIMARY KEY,
    LoanID INT,
    RepaymentDate DATE,
    Amount DECIMAL(10, 2),
    FOREIGN KEY (LoanID) REFERENCES Loans(LoanID)
);

-- 交易表
CREATE TABLE Transactions (
    TransactionID INT PRIMARY KEY,
    AccountID INT,
    TransactionDate DATE,
    Amount DECIMAL(10, 2),
    TransactionType VARCHAR(50),
    FOREIGN KEY (AccountID) REFERENCES BankAccounts(AccountID)
);

-- 分行表
CREATE TABLE Branches (
    BranchID INT PRIMARY KEY,
    BranchName VARCHAR(100),
    Location VARCHAR(100)
);

-- 员工表
CREATE TABLE Employees (
    EmployeeID INT PRIMARY KEY,
    EmployeeName VARCHAR(100),
    BranchID INT,
    Position VARCHAR(50),
    FOREIGN KEY (BranchID) REFERENCES Branches(BranchID)
);

-- 信用评分表
CREATE TABLE CreditScores (
    CreditScoreID INT PRIMARY KEY,
    CustomerID INT,
    Score INT,
    EvaluationDate DATE,
    FOREIGN KEY (CustomerID) REFERENCES BankCustomers(CustomerID)
);

-- 担保人表
CREATE TABLE Guarantors (
    GuarantorID INT PRIMARY KEY,
    LoanID INT,
    GuarantorName VARCHAR(100),
    ContactInfo VARCHAR(100),
    FOREIGN KEY (LoanID) REFERENCES Loans(LoanID)
);

-- 插入数据
-- 插入客户数据
INSERT INTO BankCustomers (CustomerID, CustomerName, ContactInfo, Address) VALUES
(1, 'John Doe', 'john@example.com', '123 Main St, New York, NY'),
(2, 'Jane Smith', 'jane@example.com', '456 Elm St, Los Angeles, CA'),
(3, 'Bob Johnson', 'bob@example.com', '789 Oak St, Chicago, IL');

-- 插入账户数据
INSERT INTO BankAccounts (AccountID, CustomerID, AccountType, Balance, BranchID) VALUES
(1, 1, 'Checking', 1500.00, 1),
(2, 2, 'Savings', 2000.00, 2),
(3, 3, 'Checking', 3000.00, 3);

-- 插入贷款数据
INSERT INTO Loans (LoanID, CustomerID, LoanAmount, InterestRate, LoanTerm, StartDate) VALUES
(1, 1, 50000.00, 5.5, 60, '2023-01-01'),
(2, 2, 75000.00, 4.5, 72, '2023-02-01'),
(3, 3, 100000.00, 6.0, 84, '2023-03-01');

-- 插入抵押数据
INSERT INTO Collateral (CollateralID, LoanID, CollateralType, CollateralValue) VALUES
(1, 1, 'Real Estate', 60000.00),
(2, 2, 'Vehicle', 80000.00),
(3, 3, 'Equipment', 120000.00);

-- 插入还款数据
INSERT INTO Repayments (RepaymentID, LoanID, RepaymentDate, Amount) VALUES
(1, 1, '2023-02-01', 1000.00),
(2, 2, '2023-03-01', 1500.00),
(3, 3, '2023-04-01', 2000.00);

-- 插入交易数据
INSERT INTO Transactions (TransactionID, AccountID, TransactionDate, Amount, TransactionType) VALUES
(1, 1, '2023-01-15', 500.00, 'Deposit'),
(2, 2, '2023-01-16', 1000.00, 'Withdrawal'),
(3, 3, '2023-01-17', 1500.00, 'Deposit');

-- 插入分行数据
INSERT INTO Branches (BranchID, BranchName, Location) VALUES
(1, 'Main Branch', 'New York'),
(2, 'West Branch', 'Los Angeles'),
(3, 'North Branch', 'Chicago');

-- 插入员工数据
INSERT INTO Employees (EmployeeID, EmployeeName, BranchID, Position) VALUES
(1, 'Alice Brown', 1, 'Manager'),
(2, 'David Green', 2, 'Teller'),
(3, 'Emma White', 3, 'Loan Officer');

-- 插入信用评分数据
INSERT INTO CreditScores (CreditScoreID, CustomerID, Score, EvaluationDate) VALUES
(1, 1, 750, '2023-01-01'),
(2, 2, 800, '2023-02-01'),
(3, 3, 700, '2023-03-01');

-- 插入担保人数据
INSERT INTO Guarantors (GuarantorID, LoanID, GuarantorName, ContactInfo) VALUES
(1, 1, 'Charles Black', 'charles@example.com'),
(2, 2, 'Nancy White', 'nancy@example.com'),
(3, 3, 'Mark Blue', 'mark@example.com');

