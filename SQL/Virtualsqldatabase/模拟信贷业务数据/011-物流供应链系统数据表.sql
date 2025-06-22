
-- 使用指定数据库
create DATABASE logisticsystem;
use logisticsystem;

-- 物流供应链系统数据库的数据表

/**
物流供应链系统
客户表 (Customers)
订单表 (Orders)
产品表 (Products)
供应商表 (Suppliers)
库存表 (Inventory)
运输表 (Shipping)
仓库表 (Warehouses)
发票表 (Invoices)
支付表 (Payments)
退货表 (Returns)
*/

-- 第一种方法创建新表并插入数据
-- 创建新表
-- 客户表
CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    CustomerName VARCHAR(100),
    ContactName VARCHAR(100),
    Country VARCHAR(50)
);

-- 订单表
CREATE TABLE Orders (
    OrderID INT PRIMARY KEY,
    CustomerID INT,
    OrderDate DATE,
    ShipDate DATE,
    Status VARCHAR(50),
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

-- 产品表
CREATE TABLE Products (
    ProductID INT PRIMARY KEY,
    ProductName VARCHAR(100),
    SupplierID INT,
    UnitPrice DECIMAL(10, 2),
    UnitsInStock INT
);

-- 供应商表
CREATE TABLE Suppliers (
    SupplierID INT PRIMARY KEY,
    SupplierName VARCHAR(100),
    ContactName VARCHAR(100),
    Country VARCHAR(50)
);

-- 库存表
CREATE TABLE Inventory (
    InventoryID INT PRIMARY KEY,
    ProductID INT,
    WarehouseID INT,
    Quantity INT,
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

-- 运输表
CREATE TABLE Shipping (
    ShippingID INT PRIMARY KEY,
    OrderID INT,
    ShipDate DATE,
    Carrier VARCHAR(100),
    TrackingNumber VARCHAR(100),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID)
);

-- 仓库表
CREATE TABLE Warehouses (
    WarehouseID INT PRIMARY KEY,
    WarehouseName VARCHAR(100),
    Location VARCHAR(100)
);

-- 发票表
CREATE TABLE Invoices (
    InvoiceID INT PRIMARY KEY,
    OrderID INT,
    InvoiceDate DATE,
    TotalAmount DECIMAL(10, 2),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID)
);

-- 支付表
CREATE TABLE Payments (
    PaymentID INT PRIMARY KEY,
    InvoiceID INT,
    PaymentDate DATE,
    Amount DECIMAL(10, 2),
    PaymentMethod VARCHAR(50),
    FOREIGN KEY (InvoiceID) REFERENCES Invoices(InvoiceID)
);

-- 退货表
CREATE TABLE Returns (
    ReturnID INT PRIMARY KEY,
    OrderID INT,
    ProductID INT,
    ReturnDate DATE,
    Quantity INT,
    Reason VARCHAR(255),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

-- 插入数据
-- 插入客户数据
INSERT INTO Customers (CustomerID, CustomerName, ContactName, Country) VALUES
(1, 'ABC Corp', 'John Doe', 'USA'),
(2, 'XYZ Ltd', 'Jane Smith', 'UK'),
(3, 'Acme Inc', 'Bob Johnson', 'Canada');

-- 插入订单数据
INSERT INTO Orders (OrderID, CustomerID, OrderDate, ShipDate, Status) VALUES
(1, 1, '2023-01-15', '2023-01-20', 'Shipped'),
(2, 2, '2023-01-17', '2023-01-22', 'Pending'),
(3, 3, '2023-01-18', '2023-01-23', 'Shipped');

-- 插入产品数据
INSERT INTO Products (ProductID, ProductName, SupplierID, UnitPrice, UnitsInStock) VALUES
(1, 'Laptop', 1, 800.00, 50),
(2, 'Smartphone', 2, 600.00, 100),
(3, 'Tablet', 3, 300.00, 150);

-- 插入供应商数据
INSERT INTO Suppliers (SupplierID, SupplierName, ContactName, Country) VALUES
(1, 'Tech Supplies Inc', 'Alice Brown', 'China'),
(2, 'Gadget World', 'David Green', 'Japan'),
(3, 'Device Hub', 'Emma White', 'Germany');

-- 插入库存数据
INSERT INTO Inventory (InventoryID, ProductID, WarehouseID, Quantity) VALUES
(1, 1, 1, 20),
(2, 2, 2, 50),
(3, 3, 3, 30);

-- 插入运输数据
INSERT INTO Shipping (ShippingID, OrderID, ShipDate, Carrier, TrackingNumber) VALUES
(1, 1, '2023-01-20', 'FedEx', '1234567890'),
(2, 3, '2023-01-23', 'UPS', '0987654321');

-- 插入仓库数据
INSERT INTO Warehouses (WarehouseID, WarehouseName, Location) VALUES
(1, 'Main Warehouse', 'New York'),
(2, 'Secondary Warehouse', 'Los Angeles'),
(3, 'Backup Warehouse', 'Chicago');

-- 插入发票数据
INSERT INTO Invoices (InvoiceID, OrderID, InvoiceDate, TotalAmount) VALUES
(1, 1, '2023-01-20', 1600.00),
(2, 2, '2023-01-22', 1200.00),
(3, 3, '2023-01-23', 900.00);

-- 插入支付数据
INSERT INTO Payments (PaymentID, InvoiceID, PaymentDate, Amount, PaymentMethod) VALUES
(1, 1, '2023-01-21', 1600.00, 'Credit Card'),
(2, 2, '2023-01-23', 1200.00, 'PayPal'),
(3, 3, '2023-01-24', 900.00, 'Bank Transfer');

-- 插入退货数据
INSERT INTO Returns (ReturnID, OrderID, ProductID, ReturnDate, Quantity, Reason) VALUES
(1, 1, 1, '2023-01-25', 1, 'Defective product'),
(2, 3, 2, '2023-01-26', 2, 'Ordered by mistake');

-- 第二种方法创建新表并插入数据
-- 创建 Suppliers 表
CREATE TABLE Suppliers (
    SupplierID INT PRIMARY KEY,
    SupplierName VARCHAR(100),
    ContactName VARCHAR(100),
    Phone VARCHAR(15)
);

INSERT INTO Suppliers (SupplierID, SupplierName, ContactName, Phone) VALUES
(1, 'Supplier A', 'John Doe', '123-456-7890'),
(2, 'Supplier B', 'Jane Smith', '234-567-8901');

-- 创建 Products 表
CREATE TABLE Products (
    ProductID INT PRIMARY KEY,
    ProductName VARCHAR(100),
    SupplierID INT,
    Price DECIMAL(10, 2),
    FOREIGN KEY (SupplierID) REFERENCES Suppliers(SupplierID)
);

INSERT INTO Products (ProductID, ProductName, SupplierID, Price) VALUES
(1, 'Product 1', 1, 10.50),
(2, 'Product 2', 2, 20.75);

-- 创建 Warehouses 表
CREATE TABLE Warehouses (
    WarehouseID INT PRIMARY KEY,
    WarehouseName VARCHAR(100),
    Location VARCHAR(100)
);

INSERT INTO Warehouses (WarehouseID, WarehouseName, Location) VALUES
(1, 'Warehouse A', 'Location 1'),
(2, 'Warehouse B', 'Location 2');

-- 创建 Customers 表
CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    CustomerName VARCHAR(100),
    ContactName VARCHAR(100),
    Phone VARCHAR(15)
);

INSERT INTO Customers (CustomerID, CustomerName, ContactName, Phone) VALUES
(1, 'Customer A', 'Alice Brown', '345-678-9012'),
(2, 'Customer B', 'Bob White', '456-789-0123');

-- 创建 Orders 表
CREATE TABLE Orders (
    OrderID INT PRIMARY KEY,
    CustomerID INT,
    OrderDate DATE,
    TotalAmount DECIMAL(10, 2),
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

INSERT INTO Orders (OrderID, CustomerID, OrderDate, TotalAmount) VALUES
(1, 1, '2024-01-15', 100.50),
(2, 2, '2024-01-20', 200.75);

-- 创建 OrderDetails 表
CREATE TABLE OrderDetails (
    OrderDetailID INT PRIMARY KEY,
    OrderID INT,
    ProductID INT,
    Quantity INT,
    UnitPrice DECIMAL(10, 2),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

INSERT INTO OrderDetails (OrderDetailID, OrderID, ProductID, Quantity, UnitPrice) VALUES
(1, 1, 1, 2, 10.50),
(2, 2, 2, 3, 20.75);

-- 创建 Shipments 表
CREATE TABLE Shipments (
    ShipmentID INT PRIMARY KEY,
    OrderID INT,
    ShipmentDate DATE,
    CarrierID INT,
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID)
);

INSERT INTO Shipments (ShipmentID, OrderID, ShipmentDate, CarrierID) VALUES
(1, 1, '2024-01-18', 1),
(2, 2, '2024-01-25', 2);

-- 创建 Inventory 表
CREATE TABLE Inventory (
    InventoryID INT PRIMARY KEY,
    WarehouseID INT,
    ProductID INT,
    Quantity INT,
    FOREIGN KEY (WarehouseID) REFERENCES Warehouses(WarehouseID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

INSERT INTO Inventory (InventoryID, WarehouseID, ProductID, Quantity) VALUES
(1, 1, 1, 100),
(2, 2, 2, 200);

-- 创建 Carriers 表
CREATE TABLE Carriers (
    CarrierID INT PRIMARY KEY,
    CarrierName VARCHAR(100),
    Phone VARCHAR(15)
);

INSERT INTO Carriers (CarrierID, CarrierName, Phone) VALUES
(1, 'Carrier A', '567-890-1234'),
(2, 'Carrier B', '678-901-2345');

-- 创建 Routes 表
CREATE TABLE Routes (
    RouteID INT PRIMARY KEY,
    Origin VARCHAR(100),
    Destination VARCHAR(100),
    Distance INT
);

INSERT INTO Routes (RouteID, Origin, Destination, Distance) VALUES
(1, 'Location 1', 'Location 2', 50),
(2, 'Location 2', 'Location 3', 75);
