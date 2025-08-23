#!/usr/bin/env python3
"""
直接创建SQLite数据库
"""

import sqlite3
import os
from datetime import datetime

def create_database():
    """创建SQLite数据库"""
    db_path = "analysis_system.db"

    print(f"正在创建数据库: {db_path}")

    # 连接数据库（如果不存在会自动创建）
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 创建用户表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        hashed_password TEXT NOT NULL,
        full_name TEXT,
        is_active BOOLEAN DEFAULT 1,
        is_superuser BOOLEAN DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_login TIMESTAMP
    )
    ''')

    # 创建其他表...
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reports (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        industry TEXT DEFAULT 'retail',
        report_type TEXT DEFAULT 'monthly',
        status TEXT DEFAULT 'draft',
        content TEXT,
        metadata TEXT,
        file_path TEXT,
        created_by TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # 插入默认管理员用户
    try:
        cursor.execute('''
        INSERT INTO users (id, username, email, hashed_password, full_name, is_superuser)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            'admin-uuid-123',
            'admin',
            'admin@example.com',
            '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj8xPL/OgZZq',
            'System Administrator',
            1
        ))
        print("✅ 默认管理员用户创建成功")
    except sqlite3.IntegrityError:
        print("ℹ️ 管理员用户已存在")

    # 提交更改
    conn.commit()
    conn.close()

    print(f"✅ 数据库创建完成: {db_path}")
    print(f"文件大小: {os.path.getsize(db_path)} bytes")

if __name__ == "__main__":
    create_database()
