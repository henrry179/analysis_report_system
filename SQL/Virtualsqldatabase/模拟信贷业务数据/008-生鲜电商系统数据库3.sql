-- 创建生鲜电商系统数据库:Fresh Food E-commerce System
create database FreshFoodEcommerceSystem;
use FreshFoodEcommerceSystem;

/**
-- 生鲜电商数据库

1.客户表 (Customers)
2.订单表 (Orders)
3.产品表 (Products)
4.类别表 (Categories)
5.供应商表 (Suppliers)
6.库存表 (Inventory)
7.运输表 (Shipping)
8.仓库表 (Warehouses)
9.发票表 (Invoices)
10.支付表 (Payments)
11.评论表 (Reviews)
12.退货表 (Returns)
13.优惠券表 (Coupons)

字段类型

1.INT
2.VARCHAR
3.DATE
4.DECIMAL
5.BOOLEAN
6.TEXT
7.DATETIME
8.TIME
9.FLOAT
10.CHAR
11.BINARY
12.BLOB
13.ENUM
14.JSON
15.SET
16.YEAR
17.TIMESTAMP
18.MEDIUMINT
19.TINYINT
20.BIGINT

*/

-- 1.客户表
CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    CustomerName VARCHAR(100),
    Email VARCHAR(100),
    Password CHAR(60),
    Phone VARCHAR(20),
    Address TEXT,
    RegisterDate DATE,
    Status varchar(10) check (status in (1, 0))
);

-- 2.订单表
CREATE TABLE Orders (
    OrderID INT PRIMARY KEY,
    CustomerID INT,
    OrderDate DATETIME,
    TotalAmount DECIMAL(10, 2),
    Status varchar(10) check (status in ('Pending', 'Shipped', 'Delivered', 'Cancelled')),
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

-- 3.产品表
CREATE TABLE Products (
    ProductID INT PRIMARY KEY,
    ProductName VARCHAR(100),
    CategoryID INT,
    SupplierID INT,
    UnitPrice DECIMAL(10, 2),
    UnitsInStock INT,
    Description TEXT,
    Image varchar(100),
    FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID),
    FOREIGN KEY (SupplierID) REFERENCES Suppliers(SupplierID)
);

-- 4.类别表
CREATE TABLE Categories (
    CategoryID INT PRIMARY KEY,
    CategoryName VARCHAR(100),
    Description TEXT
);

-- 5.供应商表
CREATE TABLE Suppliers (
    SupplierID INT PRIMARY KEY,
    SupplierName VARCHAR(100),
    ContactName VARCHAR(100),
    Country VARCHAR(50),
    Phone VARCHAR(20)
);

-- 6.库存表
CREATE TABLE Inventory (
    InventoryID INT PRIMARY KEY,
    ProductID INT,
    WarehouseID INT,
    Quantity INT,
    LastRestock DATE,
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

-- 7.运输表
CREATE TABLE Shipping (
    ShippingID INT PRIMARY KEY,
    OrderID INT,
    ShipDate DATE,
    Carrier VARCHAR(100),
    TrackingNumber VARCHAR(100),
    EstimatedArrival DATE,
    ShippingCost DECIMAL(10, 2),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID)
);

-- 8.仓库表
CREATE TABLE Warehouses (
    WarehouseID INT PRIMARY KEY,
    WarehouseName VARCHAR(100),
    Location VARCHAR(100),
    Capacity INT
);

-- 9.发票表
CREATE TABLE Invoices (
    InvoiceID INT PRIMARY KEY,
    OrderID INT,
    InvoiceDate DATE,
    TotalAmount DECIMAL(10, 2),
    Tax DECIMAL(5, 2),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID)
);

-- 10.支付表
delete from FreshFoodEcommerceSystem.dbo.Payments;

CREATE TABLE Payments (
    PaymentID INT PRIMARY KEY,
    InvoiceID INT,
    PaymentDate DATE,
    Amount DECIMAL(10, 2),
    PaymentMethod varchar(50) check (PaymentMethod in ('Credit Card', 'PayPal', 'Bank Transfer', 'Cash')),
    FOREIGN KEY (InvoiceID) REFERENCES Invoices(InvoiceID)
);

-- 11.评论表
CREATE TABLE Reviews (
    ReviewID INT PRIMARY KEY,
    ProductID INT,
    CustomerID INT,
    Rating TINYINT,
    ReviewText TEXT,
    ReviewDate DATETIME,
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID),
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

-- 12.退货表
CREATE TABLE Returns (
    ReturnID INT PRIMARY KEY,
    OrderID INT,
    ProductID INT,
    ReturnDate DATE,
    Quantity INT,
    Reason VARCHAR(255),
    Status varchar(10) check (status in ('Pending', 'Approved', 'Rejected')),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

-- 13.优惠券表
CREATE TABLE Coupons (
    CouponID INT PRIMARY KEY,
    Code VARCHAR(50),
    Discount DECIMAL(5, 2),
    ExpiryDate DATE,
    UsageLimit INT,
    Used INT,
    Status varchar(10) check (status in (1, 0))
);

-- 插入数据表数据
-- 插入客户数据
INSERT INTO Customers (CustomerID, CustomerName, Email, Password, Phone, Address, RegisterDate, Status) VALUES
(1, 'Alice Johnson', 'alice@example.com', 'password_hash', '1234567890', '123 Main St, New York, NY', '2023-01-01', 1),
(2, 'Bob Smith', 'bob@example.com', 'password_hash', '0987654321', '456 Elm St, Los Angeles, CA', '2023-02-01', 1),
(3, 'Charlie Brown', 'charlie@example.com', 'password_hash', '1112223333', '789 Pine St, San Francisco, CA', '2023-03-01', 1),
(4, 'Diana Prince', 'diana@example.com', 'password_hash', '2223334444', '123 Oak St, Boston, MA', '2023-04-01', 1),
(5, 'Edward Elric', 'edward@example.com', 'password_hash', '3334445555', '456 Maple St, Seattle, WA', '2023-05-01', 1),
(6, 'Fiona Gallagher', 'fiona@example.com', 'password_hash', '4445556666', '789 Birch St, Denver, CO', '2023-06-01', 1),
(7, 'George Weasley', 'george@example.com', 'password_hash', '5556667777', '123 Cedar St, Miami, FL', '2023-07-01', 1),
(8, 'Harry Potter', 'harry@example.com', 'password_hash', '6667778888', '456 Spruce St, Orlando, FL', '2023-08-01', 1),
(9, 'Irene Adler', 'irene@example.com', 'password_hash', '7778889999', '789 Redwood St, Austin, TX', '2023-09-01', 1),
(10, 'Jack Sparrow', 'jack@example.com', 'password_hash', '8889990000', '123 Ash St, Dallas, TX', '2023-10-01', 1),
(11, 'Kara Zor-El', 'kara@example.com', 'password_hash', '9990001111', '456 Fir St, Houston, TX', '2023-11-01', 1),
(12, 'Luna Lovegood', 'luna@example.com', 'password_hash', '0001112222', '789 Cypress St, Atlanta, GA', '2023-12-01', 1),
(13, 'Miles Morales', 'miles@example.com', 'password_hash', '1112223334', '123 Dogwood St, Philadelphia, PA', '2024-01-01', 1),
(14, 'Natasha Romanoff', 'natasha@example.com', 'password_hash', '2223334445', '456 Willow St, Phoenix, AZ', '2024-02-01', 1),
(15, 'Oliver Queen', 'oliver@example.com', 'password_hash', '3334445556', '789 Poplar St, Portland, OR', '2024-03-01', 1);

-- 插入订单数据
INSERT INTO Orders (OrderID, CustomerID, OrderDate, TotalAmount, Status) VALUES
(1, 1, '2023-01-15 14:30:00', 150.00, 'Pending'),
(2, 2, '2023-01-17 10:45:00', 200.00, 'Shipped'),
(3, 3, '2023-01-18 15:00:00', 250.00, 'Delivered'),
(4, 4, '2023-01-19 16:30:00', 175.00, 'Cancelled'),
(5, 5, '2023-01-20 17:45:00', 300.00, 'Pending'),
(6, 6, '2023-01-21 18:15:00', 225.00, 'Shipped'),
(7, 7, '2023-01-22 19:00:00', 350.00, 'Delivered'),
(8, 8, '2023-01-23 20:30:00', 400.00, 'Pending'),
(9, 9, '2023-01-24 21:45:00', 275.00, 'Cancelled'),
(10, 10, '2023-01-25 22:15:00', 500.00, 'Shipped'),
(11, 11, '2023-01-26 23:00:00', 450.00, 'Delivered'),
(12, 12, '2023-01-27 23:45:00', 325.00, 'Pending'),
(13, 13, '2023-01-28 10:30:00', 600.00, 'Cancelled'),
(14, 14, '2023-01-29 11:15:00', 700.00, 'Shipped'),
(15, 15, '2023-01-30 12:00:00', 800.00, 'Delivered');

-- 插入产品数据
INSERT INTO Products (ProductID, ProductName, CategoryID, SupplierID, UnitPrice, UnitsInStock, Description, Image) VALUES
(1, 'Fresh Apple', 1, 1, 1.50, 100, 'Fresh organic apples.', NULL),
(2, 'Banana', 1, 2, 0.50, 200, 'Fresh ripe bananas.', NULL),
(3, 'Carrot', 2, 1, 1.00, 150, 'Fresh organic carrots.', NULL),
(4, 'Broccoli', 2, 2, 1.50, 100, 'Fresh green broccoli.', NULL),
(5, 'Chicken Breast', 3, 3, 5.00, 50, 'Fresh organic chicken breast.', NULL),
(6, 'Salmon Fillet', 3, 4, 10.00, 40, 'Fresh wild-caught salmon.', NULL),
(7, 'Orange', 1, 1, 1.20, 120, 'Juicy fresh oranges.', NULL),
(8, 'Potato', 2, 2, 0.80, 200, 'Fresh organic potatoes.', NULL),
(9, 'Beef Steak', 3, 3, 12.00, 30, 'Grass-fed beef steak.', NULL),
(10, 'Pork Chops', 3, 4, 8.00, 60, 'Organic pork chops.', NULL),
(11, 'Grapes', 1, 1, 2.50, 80, 'Fresh seedless grapes.', NULL),
(12, 'Strawberries', 1, 2, 3.00, 90, 'Sweet fresh strawberries.', NULL),
(13, 'Spinach', 2, 3, 1.75, 110, 'Fresh organic spinach.', NULL),
(14, 'Tomato', 2, 4, 2.00, 130, 'Juicy ripe tomatoes.', NULL),
(15, 'Cod Fillet', 3, 4, 9.00, 70, 'Fresh wild-caught cod.', NULL);

-- 插入类别数据
INSERT INTO Categories (CategoryID, CategoryName, Description) VALUES
(1, 'Fruits', 'All kinds of fresh fruits.'),
(2, 'Vegetables', 'All kinds of fresh vegetables.'),
(3, 'Meat', 'Fresh organic meats.'),
(4, 'Fish', 'Fresh wild-caught fish.'),
(5, 'Fruits', 'All kinds of fresh fruits.'),
(6, 'Vegetables', 'All kinds of fresh vegetables.'),
(7, 'Meat', 'Fresh organic meats.'),
(8, 'Fish', 'Fresh wild-caught fish.'),
(9, 'Fruits', 'All kinds of fresh fruits.'),
(10, 'Vegetables', 'All kinds of fresh vegetables.'),
(11, 'Meat', 'Fresh organic meats.'),
(12, 'Fish', 'Fresh wild-caught fish.'),
(13, 'Meat', 'Fresh organic meats.'),
(14, 'Fish', 'Fresh wild-caught fish.'),
(15, 'Dairy', 'Fresh organic dairy products.');

-- 插入供应商数据
INSERT INTO Suppliers (SupplierID, SupplierName, ContactName, Country, Phone) VALUES
(1, 'Fresh Farms', 'John Doe', 'USA', '1111111111'),
(2, 'Green Valley', 'Jane Smith', 'Canada', '2222222222'),
(3, 'Healthy Meats', 'Richard Roe', 'Australia', '3333333333'),
(4, 'Seafood Delights', 'Mary Major', 'Norway', '4444444444'),
(5, 'Fresh Farms', 'John Doe', 'USA', '1111111111'),
(6, 'Green Valley', 'Jane Smith', 'Canada', '2222222222'),
(7, 'Healthy Meats', 'Richard Roe', 'Australia', '3333333333'),
(8, 'Seafood Delights', 'Mary Major', 'Norway', '4444444444'),
(9, 'Fresh Farms', 'John Doe', 'USA', '1111111111'),
(10, 'Green Valley', 'Jane Smith', 'Canada', '2222222222'),
(11, 'Healthy Meats', 'Richard Roe', 'Australia', '3333333333'),
(12, 'Seafood Delights', 'Mary Major', 'Norway', '4444444444'),
(13, 'Fresh Farms', 'John Doe', 'USA', '1111111111'),
(14, 'Green Valley', 'Jane Smith', 'Canada', '2222222222'),
(15, 'Healthy Meats', 'Richard Roe', 'Australia', '3333333333'),
(16, 'Seafood Delights', 'Mary Major', 'Norway', '4444444444'),
(17, 'Dairy Fresh', 'Paul Simon', 'Netherlands', '5555555555');

-- 插入库存数据
INSERT INTO Inventory (InventoryID, ProductID, WarehouseID, Quantity, LastRestock) VALUES
(1, 1, 1, 100, '2023-01-10'),
(2, 2, 2, 200, '2023-01-12'),
(3, 3, 1, 150, '2023-01-11'),
(4, 4, 2, 100, '2023-01-13'),
(5, 5, 1, 50, '2023-01-14'),
(6, 6, 2, 40, '2023-01-15'),
(7, 7, 1, 120, '2023-01-16'),
(8, 8, 2, 200, '2023-01-17'),
(9, 9, 1, 30, '2023-01-18'),
(10, 10, 2, 60, '2023-01-19'),
(11, 11, 1, 80, '2023-01-20'),
(12, 12, 2, 90, '2023-01-21'),
(13, 13, 1, 110, '2023-01-22'),
(14, 14, 2, 130, '2023-01-23'),
(15, 15, 1, 70, '2023-01-24');

-- 插入运输数据
INSERT INTO Shipping (ShippingID, OrderID, ShipDate, Carrier, TrackingNumber, EstimatedArrival, ShippingCost) VALUES
(1, 1, '2023-01-16', 'FedEx', '1234567890', '2023-01-18', 10.00),
(2, 2, '2023-01-18', 'UPS', '0987654321', '2023-01-20', 15.00),
(3, 3, '2023-01-18', 'DHL', '1122334455', '2023-01-20', 12.00),
(4, 4, '2023-01-19', 'USPS', '6677889900', '2023-01-21', 8.00),
(5, 5, '2023-01-20', 'FedEx', '2233445566', '2023-01-22', 10.00),
(6, 6, '2023-01-21', 'UPS', '7788990011', '2023-01-23', 15.00),
(7, 7, '2023-01-22', 'DHL', '3344556677', '2023-01-24', 12.00),
(8, 8, '2023-01-23', 'USPS', '8899001122', '2023-01-25', 8.00),
(9, 9, '2023-01-24', 'FedEx', '4455667788', '2023-01-26', 10.00),
(10, 10, '2023-01-25', 'UPS', '9900112233', '2023-01-27', 15.00),
(11, 11, '2023-01-26', 'DHL', '5566778899', '2023-01-28', 12.00),
(12, 12, '2023-01-27', 'USPS', '0011223344', '2023-01-29', 8.00),
(13, 13, '2023-01-28', 'FedEx', '6677889911', '2023-01-30', 10.00),
(14, 14, '2023-01-29', 'UPS', '2233445577', '2023-01-31', 15.00),
(15, 15, '2023-01-30', 'DHL', '8899001144', '2023-02-01', 12.00);

-- 插入仓库数据
INSERT INTO Warehouses (WarehouseID, WarehouseName, Location, Capacity) VALUES
(1, 'Main Warehouse', 'New York', 1000),
(2, 'Secondary Warehouse', 'Los Angeles', 2000),
(3, 'Tertiary Warehouse', 'San Francisco', 1500),
(4, 'Quaternary Warehouse', 'Chicago', 1200),
(5, 'Quinary Warehouse', 'Boston', 1800),
(6, 'Main Warehouse', 'New York', 1000),
(7, 'Secondary Warehouse', 'Los Angeles', 2000),
(8, 'Tertiary Warehouse', 'San Francisco', 1500),
(9, 'Quaternary Warehouse', 'Chicago', 1200),
(10, 'Quinary Warehouse', 'Boston', 1800),
(11, 'Main Warehouse', 'New York', 1000),
(12, 'Secondary Warehouse', 'Los Angeles', 2000),
(13, 'Tertiary Warehouse', 'San Francisco', 1500),
(14, 'Quaternary Warehouse', 'Chicago', 1200),
(15, 'Quinary Warehouse', 'Boston', 1800);

-- 插入发票数据
INSERT INTO Invoices (InvoiceID, OrderID, InvoiceDate, TotalAmount, Tax) VALUES
(1, 1, '2023-01-15', 150.00, 7.50),
(2, 2, '2023-01-17', 200.00, 10.00),
(3, 3, '2023-01-18', 250.00, 12.50),
(4, 4, '2023-01-19', 175.00, 8.75),
(5, 5, '2023-01-20', 300.00, 15.00),
(6, 6, '2023-01-21', 225.00, 11.25),
(7, 7, '2023-01-22', 350.00, 17.50),
(8, 8, '2023-01-23', 400.00, 20.00),
(9, 9, '2023-01-24', 275.00, 13.75),
(10, 10, '2023-01-25', 500.00, 25.00),
(11, 11, '2023-01-26', 450.00, 22.50),
(12, 12, '2023-01-27', 325.00, 16.25),
(13, 13, '2023-01-28', 600.00, 30.00),
(14, 14, '2023-01-29', 700.00, 35.00),
(15, 15, '2023-01-30', 800.00, 40.00);

-- 插入支付数据
INSERT INTO Payments (PaymentID, InvoiceID, PaymentDate, Amount, PaymentMethod) VALUES
(1, 1, '2023-01-16', 157.50, 'Credit Card'),
(2, 2, '2023-01-18', 210.00, 'PayPal'),
(3, 3, '2023-01-19', 262.50, 'Bank Transfer'),
(4, 4, '2023-01-20', 183.75, 'Cash'),
(5, 5, '2023-01-21', 315.00, 'Credit Card'),
(6, 6, '2023-01-22', 236.25, 'PayPal'),
(7, 7, '2023-01-23', 367.50, 'Bank Transfer'),
(8, 8, '2023-01-24', 420.00, 'Cash'),
(9, 9, '2023-01-25', 288.75, 'Credit Card'),
(10, 10, '2023-01-26', 525.00, 'PayPal'),
(11, 11, '2023-01-27', 472.50, 'Bank Transfer'),
(12, 12, '2023-01-28', 341.25, 'Cash'),
(13, 13, '2023-01-29', 630.00, 'Credit Card'),
(14, 14, '2023-01-30', 735.00, 'PayPal'),
(15, 15, '2023-01-31', 840.00, 'Bank Transfer');

-- 插入评论数据
INSERT INTO Reviews (ReviewID, ProductID, CustomerID, Rating, ReviewText, ReviewDate) VALUES
(1, 1, 1, 5, 'Excellent quality!', '2023-01-20 10:00:00'),
(2, 2, 2, 4, 'Very good.', '2023-01-21 12:30:00'),
(3, 3, 3, 5, 'Very fresh and tasty.', '2023-01-22 13:00:00'),
(4, 4, 4, 4, 'Good quality.', '2023-01-23 14:30:00'),
(5, 5, 5, 3, 'Average quality.', '2023-01-24 15:45:00'),
(6, 6, 6, 5, 'Excellent taste.', '2023-01-25 16:15:00'),
(7, 7, 7, 4, 'Good value for money.', '2023-01-26 17:00:00'),
(8, 8, 8, 3, 'Not bad.', '2023-01-27 18:30:00'),
(9, 9, 9, 5, 'Highly recommended!', '2023-01-28 19:45:00'),
(10, 10, 10, 4, 'Will buy again.', '2023-01-29 20:15:00'),
(11, 11, 11, 5, 'Very delicious.', '2023-01-30 21:00:00'),
(12, 12, 12, 4, 'Quite good.', '2023-01-31 22:45:00'),
(13, 13, 13, 3, 'Its okay.', '2024-01-01 10:30:00'),
(14, 14, 14, 5, 'Fantastic!', '2024-01-02 11:15:00'),
(15, 15, 15, 4, 'Pretty good.', '2024-01-03 12:00:00');

-- 插入退货数据
INSERT INTO Returns (ReturnID, OrderID, ProductID, ReturnDate, Quantity, Reason, Status) VALUES
(1, 1, 1, '2023-01-22', 2, 'Damaged on arrival', 'Pending'),
(2, 2, 2, '2023-01-23', 1, 'Not as described', 'Approved'),
(3, 3, 3, '2023-01-25', 2, 'Expired', 'Approved'),
(4, 4, 4, '2023-01-26', 1, 'Wrong item', 'Rejected'),
(5, 5, 5, '2023-01-27', 3, 'Quality issue', 'Pending'),
(6, 6, 6, '2023-01-28', 2, 'Not fresh', 'Approved'),
(7, 7, 7, '2023-01-29', 1, 'Damaged', 'Rejected'),
(8, 8, 8, '2023-01-30', 3, 'Not as described', 'Pending'),
(9, 9, 9, '2023-01-31', 2, 'Packaging issue', 'Approved'),
(10, 10, 10, '2024-01-01', 1, 'Late delivery', 'Rejected'),
(11, 11, 11, '2024-01-02', 3, 'Wrong item', 'Pending'),
(12, 12, 12, '2024-01-03', 2, 'Quality issue', 'Approved'),
(13, 13, 13, '2024-01-04', 1, 'Not fresh', 'Rejected'),
(14, 14, 14, '2024-01-05', 3, 'Damaged', 'Pending'),
(15, 15, 15, '2024-01-06', 2, 'Expired', 'Approved');

-- 插入优惠券数据
INSERT INTO Coupons (CouponID, Code, Discount, ExpiryDate, UsageLimit, Used, Status) VALUES
(1, 'SAVE10', 10.00, '2023-12-31', 100, 10, 1),
(2, 'FRESH20', 20.00, '2023-06-30', 50, 5, 1),
(3, 'DISCOUNT5', 5.00, '2024-01-31', 150, 20, 1),
(4, 'WELCOME10', 10.00, '2023-12-31', 200, 30, 1),
(5, 'SUMMER15', 15.00, '2023-06-30', 100, 50, 1),
(6, 'AUTUMN25', 25.00, '2023-09-30', 80, 40, 1),
(7, 'WINTER50', 50.00, '2023-12-31', 50, 10, 1),
(8, 'NEWYEAR10', 10.00, '2024-01-01', 120, 60, 1),
(9, 'BLACKFRIDAY30', 30.00, '2023-11-25', 70, 35, 1),
(10, 'CYBERMONDAY20', 20.00, '2023-11-28', 100, 50, 1),
(11, 'FLASHSALE40', 40.00, '2023-07-15', 60, 20, 1),
(12, 'SPRING25', 25.00, '2024-03-31', 90, 45, 1),
(13, 'FALLDISCOUNT15', 15.00, '2023-10-31', 110, 55, 0),
(14, 'NEWCUSTOMER20', 20.00, '2024-01-15', 130, 65, 1),
(15, 'LOYALTY30', 30.00, '2024-02-28', 140, 70, 1);
