drop database mydatas

-- 
SELECT * FROM sys.dm_exec_sessions;

-- 
SELECT r.session_id, r.status, r.command, r.cpu_time, r.total_elapsed_time
FROM sys.dm_exec_requests r
WHERE r.database_id = DB_ID(N'hftradingdatas');


USE master;
DROP DATABASE mydatas;

use master;
drop database hftradingdatas;


-- 1.python代码执行清空SQL 数据库的操作
/**
-- python代码执行清空SQL 数据库的操作

import pyodbc

# 连接到 SQL Server
def connect_to_sql_server(server, database):
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=' + server + ';'
        'DATABASE=' + database + ';'
        'Trusted_Connection=yes;'
    )
    return conn

# 清空数据库中的所有表
def clear_database(conn):
    cursor = conn.cursor()
    
    # 获取所有表名
    cursor.execute("""
        SELECT TABLE_NAME
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_TYPE = 'BASE TABLE'
    """)
    tables = cursor.fetchall()

    # 删除所有表
    for table in tables:
        table_name = table[0]
        drop_table_query = f"DROP TABLE [{table_name}]"
        try:
            cursor.execute(drop_table_query)
            print(f"Table {table_name} dropped successfully.")
        except Exception as e:
            print(f"Failed to drop table {table_name}. Error: {e}")

    conn.commit()
    cursor.close()

# 配置参数
server = 'localhost'
database = 'hftradingdatas'

# 连接到 SQL Server 并指定数据库
conn = connect_to_sql_server(server, database)

# 清空数据库
clear_database(conn)

# 关闭连接
conn.close()
print("All tables dropped successfully.")

*/


-- 2.强制清空数据库中的所有数据表，包含拥有外键的数据库
/**
import pyodbc

# 连接到 SQL Server
def connect_to_sql_server(server, database):
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=' + server + ';'
        'DATABASE=' + database + ';'
        'Trusted_Connection=yes;'
    )
    return conn

# 删除所有外键约束
def drop_foreign_keys(conn):
    cursor = conn.cursor()
    
    # 获取所有外键约束
    cursor.execute("""
        SELECT
            fk.name AS FK_Name,
            tp.name AS Table_Name
        FROM
            sys.foreign_keys AS fk
            INNER JOIN sys.tables AS tp ON fk.parent_object_id = tp.object_id
    """)
    foreign_keys = cursor.fetchall()

    # 删除所有外键约束
    for fk in foreign_keys:
        drop_fk_query = f"ALTER TABLE [{fk.Table_Name}] DROP CONSTRAINT [{fk.FK_Name}]"
        try:
            cursor.execute(drop_fk_query)
            print(f"Foreign key {fk.FK_Name} dropped successfully from table {fk.Table_Name}.")
        except Exception as e:
            print(f"Failed to drop foreign key {fk.FK_Name} from table {fk.Table_Name}. Error: {e}")

    conn.commit()
    cursor.close()

# 清空数据库中的所有表
def clear_database(conn):
    cursor = conn.cursor()
    
    # 获取所有表名
    cursor.execute("""
        SELECT TABLE_NAME
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_TYPE = 'BASE TABLE'
    """)
    tables = cursor.fetchall()

    # 删除所有表
    for table in tables:
        table_name = table[0]
        drop_table_query = f"DROP TABLE [{table_name}]"
        try:
            cursor.execute(drop_table_query)
            print(f"Table {table_name} dropped successfully.")
        except Exception as e:
            print(f"Failed to drop table {table_name}. Error: {e}")

    conn.commit()
    cursor.close()

# 配置参数
server = 'localhost'
database = 'tradingdatas'

# 连接到 SQL Server 并指定数据库
conn = connect_to_sql_server(server, database)

# 删除所有外键约束
drop_foreign_keys(conn)

# 清空数据库
clear_database(conn)

# 关闭连接
conn.close()
print("All tables and foreign keys dropped successfully.")


*/