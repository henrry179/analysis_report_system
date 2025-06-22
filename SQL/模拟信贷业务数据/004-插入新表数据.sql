-- 1.Suppliers 表

INSERT INTO mydatas.dbo.Suppliers (SupplierID, SupplierName, ContactName, Address, Phone, Email, Website, Established, Type, Notes, LastOrderDate)
VALUES
(3341, 'Alpha Corp', 'Alice Smith', '123 Alpha St.', '555-0100', 'alice@alpha.com', 'www.alpha.com', '2000-01-01', 'Manufacturer', 'Premium supplier', '2024-01-15'),
(3342, 'Beta Inc', 'Bob Johnson', '456 Beta Ave.', '555-0200', 'bob@beta.com', 'www.beta.com', '2000-01-01', 'Distributor', 'Regional supplier', '2024-02-20'),
(3343, 'Alpha Corp', 'Alice Smith', '123 Alpha St.', '555-0100', 'alice@alpha.com', 'www.alpha.com', '2000-01-01', 'Manufacturer', 'Premium supplier', '2024-01-15'),
(3344, 'Beta Inc', 'Bob Johnson', '456 Beta Ave.', '555-0200', 'bob@beta.com', 'www.beta.com', '2000-01-01', 'Distributor', 'Regional supplier', '2024-02-20'),
(3345, 'Alpha Corp', 'Alice Smith', '123 Alpha St.', '555-0100', 'alice@alpha.com', 'www.alpha.com', '2000-01-01', 'Manufacturer', 'Premium supplier', '2024-01-15'),
(3346, 'Beta Inc', 'Bob Johnson', '456 Beta Ave.', '555-0200', 'bob@beta.com', 'www.beta.com', '2000-01-01', 'Distributor', 'Regional supplier', '2024-02-20'),
(3347, 'Alpha Corp', 'Alice Smith', '123 Alpha St.', '555-0100', 'alice@alpha.com', 'www.alpha.com', '2000-01-01', 'Manufacturer', 'Premium supplier', '2024-01-15'),
(3348, 'Beta Inc', 'Bob Johnson', '456 Beta Ave.', '555-0200', 'bob@beta.com', 'www.beta.com', '2000-01-01', 'Distributor', 'Regional supplier', '2024-02-20'),
(3349, 'Alpha Corp', 'Alice Smith', '123 Alpha St.', '555-0100', 'alice@alpha.com', 'www.alpha.com', '2000-01-01', 'Manufacturer', 'Premium supplier', '2024-01-15'),
(33410, 'Beta Inc', 'Bob Johnson', '456 Beta Ave.', '555-0200', 'bob@beta.com', 'www.beta.com', '2000-01-01', 'Distributor', 'Regional supplier', '2024-02-20'),
(33411, 'Alpha Corp', 'Alice Smith', '123 Alpha St.', '555-0100', 'alice@alpha.com', 'www.alpha.com', '2000-01-01', 'Manufacturer', 'Premium supplier', '2024-01-15'),
(33412, 'Beta Inc', 'Bob Johnson', '456 Beta Ave.', '555-0200', 'bob@beta.com', 'www.beta.com', '2000-01-01', 'Distributor', 'Regional supplier', '2024-02-20'),
(33413, 'Alpha Corp', 'Alice Smith', '123 Alpha St.', '555-0100', 'alice@alpha.com', 'www.alpha.com', '2000-01-01', 'Manufacturer', 'Premium supplier', '2024-01-15'),
(33414, 'Beta Inc', 'Bob Johnson', '456 Beta Ave.', '555-0200', 'bob@beta.com', 'www.beta.com', '2000-01-01', 'Distributor', 'Regional supplier', '2024-02-20'),
(33415, 'Alpha Corp', 'Alice Smith', '123 Alpha St.', '555-0100', 'alice@alpha.com', 'www.alpha.com','2000-01-01', 'Manufacturer', 'Premium supplier', '2024-01-15'),
(33416, 'Beta Inc', 'Bob Johnson', '456 Beta Ave.', '555-0200', 'bob@beta.com', 'www.beta.com', '2000-01-01', 'Distributor', 'Regional supplier', '2024-02-20'),
(33417, 'Alpha Corp', 'Alice Smith', '123 Alpha St.', '555-0100', 'alice@alpha.com', 'www.alpha.com', '2000-01-01', 'Manufacturer', 'Premium supplier', '2024-01-15'),
(33418, 'Beta Inc', 'Bob Johnson', '456 Beta Ave.', '555-0200', 'bob@beta.com', 'www.beta.com', '2000-01-01', 'Distributor', 'Regional supplier', '2024-02-20'),
(33419, 'Beta Inc', 'Bob Johnson', '456 Beta Ave.', '555-0200', 'bob@beta.com', 'www.beta.com', '2000-01-01', 'Distributor', 'Regional supplier', '2024-02-20'),
(33420, 'Kappa Ltd', 'Karl Brown', '987 Kappa Rd.', '555-0900', 'karl@kappa.com', 'www.kappa.com', '2000-01-01', 'Retailer', 'Local supplier', '2024-04-25');

-- 2.Products 表

INSERT INTO mydatas.dbo.Products (ProductID, ProductName, SupplierID, CategoryID, UnitPrice, UnitsInStock, Discontinued, ProductCode, Description, Weight, LastSupplyDate)
VALUES
(981, 'Gadget Pro', 1, 1, 299.99, 50, 0, 'GADPRO001', 'Advanced gadget', 0.5, '2024-03-01'),
(982, 'Widget 2000', 2, 2, 19.99, 150, 0, 'WID2000', 'Standard widget', 1.2, '2024-03-05'),
(983, 'Gadget Pro', 1, 1, 299.99, 50, 0, 'GADPRO001', 'Advanced gadget', 0.5, '2024-03-01'),
(984, 'Widget 2000', 2, 2, 19.99, 150, 0, 'WID2000', 'Standard widget', 1.2, '2024-03-05'),
(985, 'Gadget Pro', 1, 1, 299.99, 50, 0, 'GADPRO001', 'Advanced gadget', 0.5, '2024-03-01'),
(986, 'Widget 2000', 2, 2, 19.99, 150, 0, 'WID2000', 'Standard widget', 1.2, '2024-03-05'),
(987, 'Gadget Pro', 1, 1, 299.99, 50, 0, 'GADPRO001', 'Advanced gadget', 0.5, '2024-03-01'),
(988, 'Widget 2000', 2, 2, 19.99, 150, 0, 'WID2000', 'Standard widget', 1.2, '2024-03-05'),
(989, 'Gadget Pro', 1, 1, 299.99, 50, 0, 'GADPRO001', 'Advanced gadget', 0.5, '2024-03-01'),
(9810, 'Widget 2000', 2, 2, 19.99, 150, 0, 'WID2000', 'Standard widget', 1.2, '2024-03-05'),
(9811, 'Gadget Pro', 1, 1, 299.99, 50, 0, 'GADPRO001', 'Advanced gadget', 0.5, '2024-03-01'),
(9812, 'Widget 2000', 2, 2, 19.99, 150, 0, 'WID2000', 'Standard widget', 1.2, '2024-03-05'),
(9813, 'Gadget Pro', 1, 1, 299.99, 50, 0, 'GADPRO001', 'Advanced gadget', 0.5, '2024-03-01'),
(9814, 'Widget 2000', 2, 2, 19.99, 150, 0, 'WID2000', 'Standard widget', 1.2, '2024-03-05'),
(9815, 'Gadget Pro', 1, 1, 299.99, 50, 0, 'GADPRO001', 'Advanced gadget', 0.5, '2024-03-01'),
(9816, 'Widget 2000', 2, 2, 19.99, 150, 0, 'WID2000', 'Standard widget', 1.2, '2024-03-05'),
(9817, 'Widget 2000', 2, 2, 19.99, 150, 0, 'WID2000', 'Standard widget', 1.2, '2024-03-05'),
(9818, 'Gadget Pro', 1, 1, 299.99, 50, 0, 'GADPRO001', 'Advanced gadget', 0.5, '2024-03-01'),
(9819, 'Widget 2000', 2, 2, 19.99, 150, 0, 'WID2000', 'Standard widget', 1.2, '2024-03-05'),
(9820, 'Doodad X', 20, 5, 49.95, 75, 0, 'DOODX100', 'Extra feature doodad', 0.3, '2024-04-10');

-- 3.Categories 表

INSERT INTO mydatas.dbo.Categories (CategoryID, CategoryName, Description, ParentCategoryID, ValidFrom, ValidTo)
VALUES
(961, 'Electronics', 'Electronic gadgets', NULL, '2024-01-01', NULL),
(962, 'Home & Garden', 'Items for home improvement', NULL, '2024-01-01', NULL),
(963, 'Electronics', 'Electronic gadgets', NULL, '2024-01-01', NULL),
(964, 'Home & Garden', 'Items for home improvement', NULL, '2024-01-01', NULL),
(965, 'Electronics', 'Electronic gadgets', NULL, '2024-01-01', NULL),
(966, 'Home & Garden', 'Items for home improvement', NULL, '2024-01-01', NULL),
(967, 'Electronics', 'Electronic gadgets', NULL, '2024-01-01', NULL),
(968, 'Home & Garden', 'Items for home improvement', NULL, '2024-01-01', NULL),
(969, 'Electronics', 'Electronic gadgets', NULL, '2024-01-01', NULL),
(9610, 'Home & Garden', 'Items for home improvement', NULL, '2024-01-01', NULL),
(9611, 'Electronics', 'Electronic gadgets', NULL, '2024-01-01', NULL),
(9612, 'Home & Garden', 'Items for home improvement', NULL, '2024-01-01', NULL),
(9613, 'Electronics', 'Electronic gadgets', NULL, '2024-01-01', NULL),
(9614, 'Home & Garden', 'Items for home improvement', NULL, '2024-01-01', NULL),
(9615, 'Electronics', 'Electronic gadgets', NULL, '2024-01-01', NULL),
(9616, 'Home & Garden', 'Items for home improvement', NULL, '2024-01-01', NULL),
(9617, 'Electronics', 'Electronic gadgets', NULL, '2024-01-01', NULL),
(9618, 'Home & Garden', 'Items for home improvement', NULL, '2024-01-01', NULL),
(9619, 'Electronics', 'Electronic gadgets', NULL, '2024-01-01', NULL),
(9620, 'Home & Garden', 'Items for home improvement', NULL, '2024-01-01', NULL),
(9621, 'Electronics', 'Electronic gadgets', NULL, '2024-01-01', NULL),
(9622, 'Home & Garden', 'Items for home improvement', NULL, '2024-01-01', NULL),
(9623, 'Electronics', 'Electronic gadgets', NULL, '2024-01-01', NULL),
(9624, 'Home & Garden', 'Items for home improvement', NULL, '2024-01-01', NULL),
(9625, 'Electronics', 'Electronic gadgets', NULL, '2024-01-01', NULL),
(9626, 'Home & Garden', 'Items for home improvement', NULL, '2024-01-01', NULL),
(9627, 'Outdoors', 'Outdoor equipment and gear', NULL, '2024-01-01', NULL);

-- 4.Orders 表

INSERT INTO mydatas.dbo.Orders (OrderID, CustomerID, EmployeeID, OrderDate, RequiredDate, ShippedDate, ShipperID, Freight, ShipName, ShipAddress, ShipCity)
VALUES
(6581, 1, 1, '2024-05-01', '2024-05-10', '2024-05-03', 1, 10.50, 'Alice Smith', '123 Alpha St.', 'Alphaville'),
(6582, 2, 2, '2024-05-02', '2024-05-11', '2024-05-04', 2, 15.75, 'Bob Johnson', '456 Beta Ave.', 'Betatown'),
(6583, 1, 1, '2024-05-01', '2024-05-10', '2024-05-03', 1, 10.50, 'Alice Smith', '123 Alpha St.', 'Alphaville'),
(6584, 2, 2, '2024-05-02', '2024-05-11', '2024-05-04', 2, 15.75, 'Bob Johnson', '456 Beta Ave.', 'Betatown'),
(6585, 1, 1, '2024-05-01', '2024-05-10', '2024-05-03', 1, 10.50, 'Alice Smith', '123 Alpha St.', 'Alphaville'),
(6586, 2, 2, '2024-05-02', '2024-05-11', '2024-05-04', 2, 15.75, 'Bob Johnson', '456 Beta Ave.', 'Betatown'),
(6587, 1, 1, '2024-05-01', '2024-05-10', '2024-05-03', 1, 10.50, 'Alice Smith', '123 Alpha St.', 'Alphaville'),
(6588, 2, 2, '2024-05-02', '2024-05-11', '2024-05-04', 2, 15.75, 'Bob Johnson', '456 Beta Ave.', 'Betatown'),
(6589, 1, 1, '2024-05-01', '2024-05-10', '2024-05-03', 1, 10.50, 'Alice Smith', '123 Alpha St.', 'Alphaville'),
(65810, 2, 2, '2024-05-02', '2024-05-11', '2024-05-04', 2, 15.75, 'Bob Johnson', '456 Beta Ave.', 'Betatown'),
(65811, 1, 1, '2024-05-01', '2024-05-10', '2024-05-03', 1, 10.50, 'Alice Smith', '123 Alpha St.', 'Alphaville'),
(65812, 2, 2, '2024-05-02', '2024-05-11', '2024-05-04', 2, 15.75, 'Bob Johnson', '456 Beta Ave.', 'Betatown'),
(65813, 1, 1, '2024-05-01', '2024-05-10', '2024-05-03', 1, 10.50, 'Alice Smith', '123 Alpha St.', 'Alphaville'),
(65814, 2, 2, '2024-05-02', '2024-05-11', '2024-05-04', 2, 15.75, 'Bob Johnson', '456 Beta Ave.', 'Betatown'),
(65815, 1, 1, '2024-05-01', '2024-05-10', '2024-05-03', 1, 10.50, 'Alice Smith', '123 Alpha St.', 'Alphaville'),
(65816, 2, 2, '2024-05-02', '2024-05-11', '2024-05-04', 2, 15.75, 'Bob Johnson', '456 Beta Ave.', 'Betatown'),
(65817, 1, 1, '2024-05-01', '2024-05-10', '2024-05-03', 1, 10.50, 'Alice Smith', '123 Alpha St.', 'Alphaville'),
(65818, 2, 2, '2024-05-02', '2024-05-11', '2024-05-04', 2, 15.75, 'Bob Johnson', '456 Beta Ave.', 'Betatown'),
(65819, 1, 1, '2024-05-01', '2024-05-10', '2024-05-03', 1, 10.50, 'Alice Smith', '123 Alpha St.', 'Alphaville'),
(65820, 2, 2, '2024-05-02', '2024-05-11', '2024-05-04', 2, 15.75, 'Bob Johnson', '456 Beta Ave.', 'Betatown'),
(65821, 1, 1, '2024-05-01', '2024-05-10', '2024-05-03', 1, 10.50, 'Alice Smith', '123 Alpha St.', 'Alphaville'),
(65822, 2, 2, '2024-05-02', '2024-05-11', '2024-05-04', 2, 15.75, 'Bob Johnson', '456 Beta Ave.', 'Betatown'),
(65823, 1, 1, '2024-05-01', '2024-05-10', '2024-05-03', 1, 10.50, 'Alice Smith', '123 Alpha St.', 'Alphaville'),
(65824, 2, 2, '2024-05-02', '2024-05-11', '2024-05-04', 2, 15.75, 'Bob Johnson', '456 Beta Ave.', 'Betatown'),
(65825, 1, 1, '2024-05-01', '2024-05-10', '2024-05-03', 1, 10.50, 'Alice Smith', '123 Alpha St.', 'Alphaville'),
(65826, 2, 2, '2024-05-02', '2024-05-11', '2024-05-04', 2, 15.75, 'Bob Johnson', '456 Beta Ave.', 'Betatown'),
(65827, 1, 1, '2024-05-01', '2024-05-10', '2024-05-03', 1, 10.50, 'Alice Smith', '123 Alpha St.', 'Alphaville'),
(65828, 2, 2, '2024-05-02', '2024-05-11', '2024-05-04', 2, 15.75, 'Bob Johnson', '456 Beta Ave.', 'Betatown'),
(65829, 1, 1, '2024-05-01', '2024-05-10', '2024-05-03', 1, 10.50, 'Alice Smith', '123 Alpha St.', 'Alphaville'),
(65830, 2, 2, '2024-05-02', '2024-05-11', '2024-05-04', 2, 15.75, 'Bob Johnson', '456 Beta Ave.', 'Betatown'),
(65831, 1, 1, '2024-05-01', '2024-05-10', '2024-05-03', 1, 10.50, 'Alice Smith', '123 Alpha St.', 'Alphaville'),
(65832, 2, 2, '2024-05-02', '2024-05-11', '2024-05-04', 2, 15.75, 'Bob Johnson', '456 Beta Ave.', 'Betatown'),
(65833, 20, 10, '2024-06-01', '2024-06-20', '2024-06-03', 5, 8.25, 'Karl Brown', '987 Kappa Rd.', 'Kappacity');

-- 5.OrderDetails 表

INSERT INTO mydatas.dbo.OrderDetails (OrderDetailID, OrderID, ProductID, Quantity, UnitPrice, Discount, Notes)
VALUES
(2161, 1, 1, 2, 299.99, 0.00, 'Order priority'),
(2162, 2, 2, 5, 19.99, 0.10, 'Bulk order'),
(2164, 1, 1, 2, 299.99, 0.00, 'Order priority'),
(2165, 2, 2, 5, 19.99, 0.10, 'Bulk order'),
(2166, 1, 1, 2, 299.99, 0.00, 'Order priority'),
(2167, 2, 2, 5, 19.99, 0.10, 'Bulk order'),
(2168, 1, 1, 2, 299.99, 0.00, 'Order priority'),
(2169, 2, 2, 5, 19.99, 0.10, 'Bulk order'),
(21610, 1, 1, 2, 299.99, 0.00, 'Order priority'),
(21611, 2, 2, 5, 19.99, 0.10, 'Bulk order'),
(21612, 1, 1, 2, 299.99, 0.00, 'Order priority'),
(21613, 2, 2, 5, 19.99, 0.10, 'Bulk order'),
(21614, 1, 1, 2, 299.99, 0.00, 'Order priority'),
(21615, 2, 2, 5, 19.99, 0.10, 'Bulk order'),
(21616, 1, 1, 2, 299.99, 0.00, 'Order priority'),
(21617, 2, 2, 5, 19.99, 0.10, 'Bulk order'),
(21618, 1, 1, 2, 299.99, 0.00, 'Order priority'),
(21619, 2, 2, 5, 19.99, 0.10, 'Bulk order'),
(21620, 20, 20, 3, 49.95, 0.00, 'Regular customer');

-- 6.Customers 表

INSERT INTO mydatas.dbo.Customers (CustomerID, CustomerName, ContactName, Address, Phone, Email, CreditLimit)
VALUES
(90351, 'Acme Corp', 'John Doe', '101 Acme St.', '555-1111', 'john@acme.com', 50000.00),
(90352, 'Beta Inc', 'Jane Doe', '202 Beta Ave.', '555-2222', 'jane@beta.com', 75000.00),
(90353, 'Acme Corp', 'John Doe', '101 Acme St.', '555-1111', 'john@acme.com', 50000.00),
(90354, 'Beta Inc', 'Jane Doe', '202 Beta Ave.', '555-2222', 'jane@beta.com', 75000.00),
(90355, 'Acme Corp', 'John Doe', '101 Acme St.', '555-1111', 'john@acme.com', 50000.00),
(90356, 'Beta Inc', 'Jane Doe', '202 Beta Ave.', '555-2222', 'jane@beta.com', 75000.00),
(90357, 'Acme Corp', 'John Doe', '101 Acme St.', '555-1111', 'john@acme.com', 50000.00),
(90358, 'Beta Inc', 'Jane Doe', '202 Beta Ave.', '555-2222', 'jane@beta.com', 75000.00),
(90359, 'Acme Corp', 'John Doe', '101 Acme St.', '555-1111', 'john@acme.com', 50000.00),
(903510, 'Beta Inc', 'Jane Doe', '202 Beta Ave.', '555-2222', 'jane@beta.com', 75000.00),
(903511, 'Acme Corp', 'John Doe', '101 Acme St.', '555-1111', 'john@acme.com', 50000.00),
(903512, 'Beta Inc', 'Jane Doe', '202 Beta Ave.', '555-2222', 'jane@beta.com', 75000.00),
(903513, 'Acme Corp', 'John Doe', '101 Acme St.', '555-1111', 'john@acme.com', 50000.00),
(903514, 'Beta Inc', 'Jane Doe', '202 Beta Ave.', '555-2222', 'jane@beta.com', 75000.00),
(903515, 'Acme Corp', 'John Doe', '101 Acme St.', '555-1111', 'john@acme.com', 50000.00),
(903516, 'Beta Inc', 'Jane Doe', '202 Beta Ave.', '555-2222', 'jane@beta.com', 75000.00),
(903517, 'Acme Corp', 'John Doe', '101 Acme St.', '555-1111', 'john@acme.com', 50000.00),
(903518, 'Beta Inc', 'Jane Doe', '202 Beta Ave.', '555-2222', 'jane@beta.com', 75000.00),
(903519, 'Acme Corp', 'John Doe', '101 Acme St.', '555-1111', 'john@acme.com', 50000.00),
(903520, 'Beta Inc', 'Jane Doe', '202 Beta Ave.', '555-2222', 'jane@beta.com', 75000.00),
(903521, 'Acme Corp', 'John Doe', '101 Acme St.', '555-1111', 'john@acme.com', 50000.00),
(903522, 'Beta Inc', 'Jane Doe', '202 Beta Ave.', '555-2222', 'jane@beta.com', 75000.00),
(903523, 'Acme Corp', 'John Doe', '101 Acme St.', '555-1111', 'john@acme.com', 50000.00),
(903524, 'Beta Inc', 'Jane Doe', '202 Beta Ave.', '555-2222', 'jane@beta.com', 75000.00),
(903525, 'Zeta Enterprises', 'Zoe Young', '909 Zeta Blvd.', '555-9090', 'zoe@zeta.com', 30000.00);

-- 7.Employees 表

INSERT INTO mydatas.dbo.Employees (EmployeeID, EmployeeName, Position, HireDate, OfficePhone, CellPhone, Department)
VALUES
(9761, 'John Manager', 'Manager', '2023-01-10', '555-1000', '555-2000', 'Sales'),
(9762, 'Jane Analyst', 'Data Analyst', '2023-02-15', '555-1100', '555-2100', 'Marketing'),
(9763, 'John Manager', 'Manager', '2023-01-10', '555-1000', '555-2000', 'Sales'),
(9764, 'Jane Analyst', 'Data Analyst', '2023-02-15', '555-1100', '555-2100', 'Marketing'),
(9765, 'John Manager', 'Manager', '2023-01-10', '555-1000', '555-2000', 'Sales'),
(9766, 'Jane Analyst', 'Data Analyst', '2023-02-15', '555-1100', '555-2100', 'Marketing'),
(9767, 'John Manager', 'Manager', '2023-01-10', '555-1000', '555-2000', 'Sales'),
(9768, 'Jane Analyst', 'Data Analyst', '2023-02-15', '555-1100', '555-2100', 'Marketing'),
(9769, 'John Manager', 'Manager', '2023-01-10', '555-1000', '555-2000', 'Sales'),
(97610, 'Jane Analyst', 'Data Analyst', '2023-02-15', '555-1100', '555-2100', 'Marketing'),
(97611, 'John Manager', 'Manager', '2023-01-10', '555-1000', '555-2000', 'Sales'),
(97612, 'Jane Analyst', 'Data Analyst', '2023-02-15', '555-1100', '555-2100', 'Marketing'),
(97613, 'John Manager', 'Manager', '2023-01-10', '555-1000', '555-2000', 'Sales'),
(97614, 'Jane Analyst', 'Data Analyst', '2023-02-15', '555-1100', '555-2100', 'Marketing'),
(97615, 'John Manager', 'Manager', '2023-01-10', '555-1000', '555-2000', 'Sales'),
(97616, 'Jane Analyst', 'Data Analyst', '2023-02-15', '555-1100', '555-2100', 'Marketing'),
(97617, 'Zack Developer', 'Software Developer', '2023-07-22', '555-1200', '555-2200', 'IT');

-- 8.Shippers 表

INSERT INTO mydatas.dbo.Shippers (ShipperID, ShipperName, Contact, Phone, Active)
VALUES
(4651, 'FastShip Inc', 'Alice Fast', '555-5000', 1),
(4652, 'QuickDelivery Ltd', 'Bob Quick', '555-6000', 1),
(4653, 'FastShip Inc', 'Alice Fast', '555-5000', 1),
(4654, 'QuickDelivery Ltd', 'Bob Quick', '555-6000', 1),
(4655, 'FastShip Inc', 'Alice Fast', '555-5000', 1),
(4656, 'QuickDelivery Ltd', 'Bob Quick', '555-6000', 1),
(4657, 'FastShip Inc', 'Alice Fast', '555-5000', 1),
(4658, 'QuickDelivery Ltd', 'Bob Quick', '555-6000', 1),
(4659, 'FastShip Inc', 'Alice Fast', '555-5000', 1),
(46510, 'QuickDelivery Ltd', 'Bob Quick', '555-6000', 1),
(46511, 'FastShip Inc', 'Alice Fast', '555-5000', 1),
(46512, 'QuickDelivery Ltd', 'Bob Quick', '555-6000', 1),
(46513, 'FastShip Inc', 'Alice Fast', '555-5000', 1),
(46514, 'QuickDelivery Ltd', 'Bob Quick', '555-6000', 1),
(46515, 'FastShip Inc', 'Alice Fast', '555-5000', 1),
(46516, 'QuickDelivery Ltd', 'Bob Quick', '555-6000', 1),
(46517, 'SpeedyCargo Co', 'Zoe Speed', '555-7000', 1);

-- 9.Inventory 表

INSERT INTO mydatas.dbo.Inventory (InventoryID, ProductID, Quantity, ReorderLevel, LastStockDate)
VALUES
(5431, 1, 50, 10, '2024-04-01'),
(5432, 2, 150, 20, '2024-04-02'),
(5433, 1, 50, 10, '2024-04-01'),
(5434, 2, 150, 20, '2024-04-02'),
(5435, 1, 50, 10, '2024-04-01'),
(5436, 2, 150, 20, '2024-04-02'),
(5437, 1, 50, 10, '2024-04-01'),
(5438, 2, 150, 20, '2024-04-02'),
(5439, 1, 50, 10, '2024-04-01'),
(54310, 2, 150, 20, '2024-04-02'),
(54311, 1, 50, 10, '2024-04-01'),
(54312, 2, 150, 20, '2024-04-02'),
(54313, 1, 50, 10, '2024-04-01'),
(54314, 2, 150, 20, '2024-04-02'),
(54315, 1, 50, 10, '2024-04-01'),
(54316, 2, 150, 20, '2024-04-02'),
(54317, 1, 50, 10, '2024-04-01'),
(54318, 20, 75, 5, '2024-05-20');

-- 10.Payments 表

INSERT INTO mydatas.dbo.Payments (PaymentID, OrderID, PaymentDate, Amount)
VALUES
(4891, 1, '2024-05-05', 600.00),
(4892, 2, '2024-05-06', 99.95),
(4893, 1, '2024-05-05', 600.00),
(4894, 2, '2024-05-06', 99.95),
(4895, 1, '2024-05-05', 600.00),
(4896, 2, '2024-05-06', 99.95),
(4897, 1, '2024-05-05', 600.00),
(4898, 2, '2024-05-06', 99.95),
(4899, 1, '2024-05-05', 600.00),
(48910, 2, '2024-05-06', 99.95),
(48911, 1, '2024-05-05', 600.00),
(48912, 2, '2024-05-06', 99.95),
(48913, 1, '2024-05-05', 600.00),
(48914, 2, '2024-05-06', 99.95),
(48915, 1, '2024-05-05', 600.00),
(48916, 2, '2024-05-06', 99.95),
(48917, 1, '2024-05-05', 600.00),
(48918, 2, '2024-05-06', 99.95),
(48919, 2, '2024-05-06', 99.95),
(48951, 1, '2024-05-05', 600.00),
(48952, 2, '2024-05-06', 99.95),
(48953, 1, '2024-05-05', 600.00),
(48954, 2, '2024-05-06', 99.95),
(48955, 1, '2024-05-05', 600.00),
(48956, 2, '2024-05-06', 99.95),
(48957, 1, '2024-05-05', 600.00),
(48958, 2, '2024-05-06', 99.95),
(48959, 1, '2024-05-05', 600.00),
(489510, 2, '2024-05-06', 99.95),
(489511, 1, '2024-05-05', 600.00),
(489512, 2, '2024-05-06', 99.95),
(489513, 1, '2024-05-05', 600.00),
(489514, 2, '2024-05-06', 99.95),
(489515, 1, '2024-05-05', 600.00),
(489516, 2, '2024-05-06', 99.95),
(489517, 1, '2024-05-05', 600.00),
(489518, 2, '2024-05-06', 99.95),
(489519, 2, '2024-05-06', 99.95),
(489520, 20, '2024-06-05', 150.00);

-- 11.Returns 表

INSERT INTO mydatas.dbo.Returns (ReturnID, OrderID, ProductID, Quantity, ReturnDate, Reason)
VALUES
(3031, 1, 1, 1, '2024-05-10', 'Damaged product'),
(3032, 2, 2, 2, '2024-05-11', 'Wrong item'),
(3033, 1, 1, 1, '2024-05-10', 'Damaged product'),
(3034, 2, 2, 2, '2024-05-11', 'Wrong item'),
(3035, 1, 1, 1, '2024-05-10', 'Damaged product'),
(3036, 2, 2, 2, '2024-05-11', 'Wrong item'),
(3037, 1, 1, 1, '2024-05-10', 'Damaged product'),
(3038, 2, 2, 2, '2024-05-11', 'Wrong item'),
(3039, 1, 1, 1, '2024-05-10', 'Damaged product'),
(30310, 2, 2, 2, '2024-05-11', 'Wrong item'),
(30311, 1, 1, 1, '2024-05-10', 'Damaged product'),
(30312, 2, 2, 2, '2024-05-11', 'Wrong item'),
(30313, 1, 1, 1, '2024-05-10', 'Damaged product'),
(30314, 2, 2, 2, '2024-05-11', 'Wrong item'),
(30315, 1, 1, 1, '2024-05-10', 'Damaged product'),
(30316, 2, 2, 2, '2024-05-11', 'Wrong item'),
(30317, 2, 2, 2, '2024-05-11', 'Wrong item'),
(30318, 1, 1, 1, '2024-05-10', 'Damaged product'),
(30319, 2, 2, 2, '2024-05-11', 'Wrong item'),
(30321, 1, 1, 1, '2024-05-10', 'Damaged product'),
(30322, 2, 2, 2, '2024-05-11', 'Wrong item'),
(30323, 1, 1, 1, '2024-05-10', 'Damaged product'),
(30324, 2, 2, 2, '2024-05-11', 'Wrong item'),
(30325, 1, 1, 1, '2024-05-10', 'Damaged product'),
(30326, 2, 2, 2, '2024-05-11', 'Wrong item'),
(30327, 1, 1, 1, '2024-05-10', 'Damaged product'),
(30328, 2, 2, 2, '2024-05-11', 'Wrong item'),
(30329, 1, 1, 1, '2024-05-10', 'Damaged product'),
(300, 2, 2, 2, '2024-05-11', 'Wrong item'),
(301, 1, 1, 1, '2024-05-10', 'Damaged product'),
(302, 2, 2, 2, '2024-05-11', 'Wrong item'),
(303, 1, 1, 1, '2024-05-10', 'Damaged product'),
(304, 2, 2, 2, '2024-05-11', 'Wrong item'),
(305, 1, 1, 1, '2024-05-10', 'Damaged product'),
(306, 2, 2, 2, '2024-05-11', 'Wrong item'),
(307, 2, 2, 2, '2024-05-11', 'Wrong item'),
(308, 1, 1, 1, '2024-05-10', 'Damaged product'),
(309, 2, 2, 2, '2024-05-11', 'Wrong item'),
(3030, 20, 20, 1, '2024-06-10', 'Customer changed mind');


-- 插入物流系统数据库和银行信贷系统数据库表
-- 插入 `Orders` 表的虚拟数据

INSERT INTO logisticsystem.dbo.Orders (
    OrderID, 
    CustomerID, 
    OrderDate, 
    RequiredDate, 
    ShippedDate, 
    ShipVia, Freight, 
    ShipName, ShipAddress, 
    ShipCity, 
    ShipRegion, 
    ShipPostalCode, 
    ShipCountry

) VALUES 

(1, 100, '2024-05-01', '2024-05-15', '2024-05-05', 1, 200.00, 'Alice''s Cafe', '123 Baker St.', 'New York', 'NY', '10001', 'USA'),
(2, 101, '2024-05-02', '2024-05-20', '2024-05-07', 2, 150.00, 'Bob''s Burgers', '456 Maple Ave.', 'Los Angeles', 'CA', '90001', 'USA');


-- 插入 `Customers` 表的虚拟数据

INSERT INTO logisticsystem.dbo.Customers (
    CustomerID, 
    FirstName, 
    LastName, 
    MiddleName, 
    Gender, 
    DateOfBirth, 
    Address, 
    City, 
    Region, 
    PostalCode, 
    Country, 
    Phone, 
    Email
    
)VALUES (
    100, 
    'Alice', 
    'Cafe', 
    NULL, 
    'Female', 
    '1985-06-12', 
    '123 Baker St.', 
    'New York', 
    'NY', 
    '10001', 
    'USA', 
    '212-555-0100', 
    'alice.cafe@example.com'),
(
    101, 
    'Bob', 
    'Burgers', 
    NULL, 
    'Male', 
    '1990-07-23', 
    '456 Maple Ave.', 
    'Los Angeles', 
    'CA', 
    '90001', 
    'USA', 
    '213-555-0200', 
    'bob.burgers@example.com'
    );

-- 物流供应链系统的 `Suppliers` 表插入数据示例

INSERT INTO logisticsystem.dbo.Suppliers(
    SupplierID,
    CompanyName,
    ContactName,
    ContactTitle,
    Address,
    City,
    PostalCode,
    Country,
    Phone,
    Fax,
    Email,
    HomePage
) VALUES (
    1,
    'Green Fields Ltd',
    'Maria Anders',
    'Sales Manager',
    'Obere Str. 57',
    'Berlin',
    '10787',
    'Germany',
    '<PHONE_NUMBER>',
    '<PHONE_NUMBER>',
    '<EMAIL_ADDRESS>',
    'http://www.greenfields.de'
);


-- 物流供应链系统的 `Products` 表插入数据示例

INSERT INTO logisticsystem.dbo.Products (
    ProductID,
    ProductName,
    Description,
    StandardCost,
    ListPrice,
    Weight,
    Size,
    ProductCategory,
    ProductModel,
    SellStartDate,
    SellEndDate,
    Discontinued
) VALUES (
    1,
    'Organic Apples',
    'Freshly picked organic apples.',
    0.75,
    1.29,
    0.5,
    'Medium',
    'Fruit',
    'Apple',
    '2024-01-01',
    NULL,
    0
), (
    2,
    'Free Range Eggs',
    'Eggs laid by free range hens.',
    1.50,
    2.99,
    1.0,
    'Large',
    'Dairy',
    'Egg',
    '2024-01-01',
    NULL,
    0
), (
    3,
    'Organic Bread Loaf',
    'A loaf of freshly baked organic bread.',
    2.00,
    3.49,
    0.75,
    'Large',
    'Bakery',
    'Bread',
    '2024-01-01',
    NULL,
    0
);


-- 物流供应链系统的 `Employees` 表插入数据示例

INSERT INTO logisticsystem.dbo.Employees (
    EmployeeID,
    LastName,
    FirstName,
    Title,
    TitleOfCourtesy,
    BirthDate,
    HireDate,
    Address,
    City,
    PostalCode,
    Country,
    Phone,
    Fax,
    Email
) VALUES (
    1,
    'Davolio',
    'Nancy',
    'Sales Representative',
    'Ms.',
    '1948-12-08',
    '1992-05-01',
    '507 - 20th Ave. E. Apt. 2A',
    'Seattle',
    '98122',
    'USA',
    '(206) 555-9857',
    '(206) 555-9741',
    '[Nancy@northwind.com](mailto:Nancy@northwind.com)'
), (
    2,
    'Fuller',
    'Andrew',
    'Vice President, Sales',
    'Dr.',
    '1952-02-19',
    '1992-08-14',
    '908 W. Capital Way',
    'Tacoma',
    '98401',
    'USA',
    '(206) 555-9482',
    '(206) 555-9087',
    '[Andrew@northwind.com](mailto:Andrew@northwind.com)'
);


-- 物流供应链系统的 `Shippers` 表插入数据示例

INSERT INTO logisticsystem.dbo.Shippers (
    ShipperID,
    CompanyName,
    Phone,
    ServiceLevel,
    DeliveryTime,
    Active
) VALUES (
    1,
    'Federal Shipping',
    '(123) 456-7890',
    'Standard',
    '2-5 days',
    1
), (
    2,
    'Blue Ribbon Express',
    '(234) 567-8901',
    'Premium',
    'Overnight',
    1
), (
    3,
    'Speedy Deliveries',
    '(345) 678-9012',
    'Economy',
    '5-7 days',
    0  -- Assuming this shipper is no longer active
);

-- 物流供应链系统的 `Inventory` 表插入数据示例

INSERT INTO logisticsystem.dbo.Inventoryid (
    InventoryID,
    ProductID,
    WarehouseID,
    QuantityAvailable,
    WarehouseLocation,
    LastStockCheck,
    ShelfLife
) VALUES (
    1,
    1,
    1,
    150,
    'Aisle 1, Shelf 1',
    '2024-05-01 10:00:00',
    90
), (
    2,
    2,
    1,
    200,
    'Aisle 2, Shelf 2',
    '2024-05-02 10:00:00',
    30
), (
    3,
    3,
    2,
    180,
    'Warehouse 2, Section B',
    '2024-05-03 10:00:00',
    60
);

-- 物流供应链系统的 `PurchaseOrders` 表插入数据示例

INSERT INTO logisticsystem.dbo.PurchaseOrders (
    PurchaseOrderID,
    SupplierID,
    OrderDate,
    DeliveryDate,
    Status,
    Amount
) VALUES (
    1,
    1,
    '2024-04-01',
    '2024-04-15',
    'Pending',
    1500.00
), (
    2,
    2,
    '2024-04-02',
    '2024-04-20',
    'Delivered',
    2000.00
);

-- 物流供应链系统的 `Transportation` 表插入数据示例

INSERT INTO logisticsystem.dbo.Transportationid (
    TransportationID,
    ShipperID,
    VehicleType,
    LicensePlate,
    Capacity,
    DriverName
) VALUES (
    1,
    1,
    'Truck',
    'TRK-1234',
    15000,
    'John Doe'
), (
    2,
    2,
    'Van',
    'VAN-5678',
    3000,
    'Jane Smith'
);

-- 物流供应链系统的 `Warehouses` 表插入数据示例

INSERT INTO logisticsystem.dbo.Warehouses (
    WarehouseID,
    WarehouseName,
    ManagerID,
    Address,
    City,
    PostalCode,
    Country
) VALUES (
    1,
    'Central Distribution Center',
    1,
    '1234 Storage Ave',
    'Chicago',
    '60601',
    'USA'
), (
    2,
    'West Coast Warehouse',
    2,
    '5678 Shipping Rd',
    'Los Angeles',
    '90001',
    'USA'
);

-- 物流供应链系统的 `Returns` 表插入数据示例

INSERT INTO logisticsystem.dbo.Returnid (
    ReturnID,
    OrderID,
    ProductID,
    ReturnDate,
    Quantity,
    Reason
) VALUES (
    1,
    1,
    1,
    '2024-05-10',
    2,
    'Damaged during transport'
);

-- 物流供应链系统的 `Sales` 表插入数据示例

INSERT INTO logisticsystem.dbo.Sales (
    SaleID,
    EmployeeID,
    CustomerID,
    SaleDate,
    TotalAmount,
    PaymentMethod
) VALUES (
    1,
    1,
    100,
    '2024-05-05',
    250.00,
    'Credit Card'
), (
    2,
    2,
    101,
    '2024-05-06',
    450.00,
    'Cash'
);

---

-- 银行信贷业务的 `Transactions` 表插入数据示例

-- 假设我们已经有一个 `Accounts` 表，其中包含 `AccountID` 字段。

-- 假设Accounts表的AccountID为101
INSERT INTO banksystem.dbo.TRANSACTIONid (
    TransactionID,
    AccountID,
    TransactionType,
    Amount,
    TransactionDate,
    BalanceAfter
) VALUES (
    1,
    101,
    'Deposit',
    500.00,
    '2024-05-01 10:00:00',
    500.00
), (
    2,
    101,
    'Withdrawal',
    100.00,
    '2024-05-02 14:30:00',
    400.00
), (
    3,
    101,
    'Transfer',
    -200.00,
    '2024-05-03 09:15:00',
    200.00
), (
    4,
    101,
    'Interest',
    10.00,
    '2024-05-04 00:00:00',
    210.00
);


-- 银行信贷业务的 `AccountTypes` 表插入数据示例

INSERT INTO AccountTypes (
    AccountTypeID,
    TypeName,
    Description,
    InterestRate,
    MinimumBalance
) VALUES (
    1,
    'Checking',
    'Standard checking account with no minimum balance requirement.',
    0.01, -- 1% interest rate
    0.00
), (
    2,
    'Savings',
    'Interest-bearing account with a variable interest rate.',
    0.03, -- 3% interest rate
    100.00
), (
    3,
    'Money Market',
    'High-yield savings account with some check-writing capabilities.',
    0.04, -- 4% interest rate
    1000.00
);

--  银行信贷业务的 `Branches` 表插入数据示例

INSERT INTO Branches (
    BranchID,
    BranchName,
    Address,
    City,
    PostalCode,
    Country,
    ManagerID
) VALUES (
    1,
    'Downtown HQ',
    '120 North Main St',
    'New York',
    '10001',
    'USA',
    1
), (
    2,
    'Uptown Branch',
    '345 East 5th St',
    'New York',
    '10002',
    'USA',
    2
), (
    3,
    'Downtown West',
    '678 South Ave',
    'Los Angeles',
    '90001',
    'USA',
    3
);

-- 银行信贷业务的 `CreditCards` 表插入数据示例

INSERT INTO CreditCards (
    CardID,
    CardNumber,
    CustomerID,
    CardType,
    ExpiryDate,
    CVV,
    CreditLimit,
    CurrentBalance
) VALUES (
    1,
    '1234-5678-9101-1121',
    100,
    'Gold',
    '2026-12-31',
    123,
    5000.00,
    450.00
), (
    2,
    '3456-7890-2121-0987',
    101,
    'Platinum',
    '2027-01-15',
    987,
    10000.00,
    800.00
);

-- 银行信贷业务的 `Transactions` 表插入数据示例（续）

-- Assuming AccountID is linked to an actual account in the Accounts table
INSERT INTO Transactions (
    TransactionID,
    AccountID,
    TransactionType,
    Amount,
    TransactionDate,
    BalanceAfter
) VALUES (
    5,
    102, -- Assuming 102 is a valid AccountID for another account
    'Deposit',
    300.00,
    '2024-05-05 14:00:00',
    800.00
), (
    6,
    103,
    'Withdrawal',
    500.00,
    '2024-05-06 16:20:00',
    2000.00
);

-- 银行信贷业务的 `Branches` 表插入数据示例（续）

-- Assuming ManagerID is linked to an actual employee in the Employees table
INSERT INTO Branches (
    BranchID,
    BranchName,
    Address,
    City,
    PostalCode,
    Country,
    ManagerID
) VALUES (
    4,
    'East Side Branch',
    '9876 East St',
    'Miami',
    '33101',
    'USA',
    4
);

-- 银行信贷业务的 `Deposits` 表插入数据示例

INSERT INTO Deposits (
    DepositID,
    AccountID,
    DepositDate,
    Amount,
    MaturityDate
) VALUES (
    1,
    101, -- Assuming 101 is a valid AccountID
    '2024-05-01',
    1000.00,
    '2025-05-01'
), (
    2,
    102,
    '2024-05-02',
    1500.00,
    '2026-05-02'
);

-- 银行信贷业务的 `Investments` 表插入数据示例

INSERT INTO Investments (
    InvestmentID,
    CustomerID,
    InvestmentType,
    InvestmentDate,
    Amount,
    ExpectedReturn
) VALUES (
    1,
    100,
    'Stocks',
    '2024-04-20',
    5000.00,
    0.08 -- 8% expected return
), (
    2,
    101,
    'Bonds',
    '2024-04-21',
    10000.00,
    0.05 -- 5% expected return
);

-- 银行信贷业务的 `InsurancePolicies` 表插入数据示例

INSERT INTO InsurancePolicies (
    PolicyID,
    CustomerID,
    PolicyType,
    CoverageAmount,
    Premium,
    StartDate,
    EndDate
) VALUES (
    1,
    100,
    'Life',
    500000.00,
    500.00,
    '2024-05-01',
    '2050-05-01'
), (
    2,
    101,
    'Health',
    300000.00,
    750.00,
    '2024-05-02',
    '2030-05-02'
);

-- 银行信贷业务的 `PaymentMethods` 表插入数据示例

INSERT INTO PaymentMethods (
    PaymentMethodID,
    MethodName,
    Description,
    IsActive
) VALUES (
    1,
    'Credit Card',
    'Payment via credit card.',
    1
), (
    2,
    'Direct Debit',
    'Automatic payment from linked bank account.',
    1
), (
    3,
    'Cash',
    'In-person cash payment.',
    1
);

-- 银行信贷业务的 `CustomerService` 表插入数据示例

INSERT INTO CustomerService (
    ServiceID,
    CustomerID,
    IssueType,
    DateReported,
    DateResolved,
    ResolutionStatus
) VALUES (
    1,
    100,
    'Account Inquiry',
    '2024-05-01 09:00:00',
    '2024-05-01 10:00:00',
    'Resolved'), 
    (
     2,
     101,
     'Payment Dispute',
     '2024-05-02 12:00:00',
     NULL, -- Assuming the issue is not yet resolved
     'Pending'
);

