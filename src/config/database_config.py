#!/usr/bin/env python3
"""
MySQL数据库配置和管理模块
支持本地MySQL数据库连接和数据管理
"""

import os
import logging
from typing import Dict, Any, Optional
from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import pymysql
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# SQLAlchemy Base
Base = declarative_base()

class DatabaseConfig:
    """MySQL数据库配置类"""
    
    # 默认配置
    DEFAULT_CONFIG = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': '',  # 需要用户设置
        'database': 'analysis_system',
        'charset': 'utf8mb4',
        'autocommit': True,
        'pool_size': 10,
        'max_overflow': 20,
        'pool_recycle': 3600,
        'echo': False  # 生产环境设为False
    }
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化数据库配置
        
        Args:
            config: 自定义配置字典
        """
        self.config = {**self.DEFAULT_CONFIG}
        if config:
            self.config.update(config)
        
        self.engine = None
        self.Session = None
        self.metadata = MetaData()
    
    def get_connection_string(self) -> str:
        """获取MySQL连接字符串"""
        return (
            f"mysql+pymysql://{self.config['user']}:{self.config['password']}"
            f"@{self.config['host']}:{self.config['port']}"
            f"/{self.config['database']}?charset={self.config['charset']}"
        )
    
    def create_engine(self):
        """创建数据库引擎"""
        try:
            connection_string = self.get_connection_string()
            self.engine = create_engine(
                connection_string,
                pool_size=self.config['pool_size'],
                max_overflow=self.config['max_overflow'],
                pool_recycle=self.config['pool_recycle'],
                echo=self.config['echo']
            )
            
            # 创建Session工厂
            self.Session = sessionmaker(bind=self.engine)
            
            logger.info("✅ MySQL数据库引擎创建成功")
            return self.engine
            
        except Exception as e:
            logger.error(f"❌ 数据库引擎创建失败: {str(e)}")
            raise
    
    def test_connection(self) -> bool:
        """测试数据库连接"""
        try:
            if not self.engine:
                self.create_engine()
            
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                result.fetchone()
            
            logger.info("✅ 数据库连接测试成功")
            return True
            
        except Exception as e:
            logger.error(f"❌ 数据库连接测试失败: {str(e)}")
            return False
    
    def create_database_if_not_exists(self):
        """创建数据库（如果不存在）"""
        try:
            # 连接到MySQL服务器（不指定数据库）
            server_config = self.config.copy()
            server_config.pop('database', None)
            
            server_connection_string = (
                f"mysql+pymysql://{server_config['user']}:{server_config['password']}"
                f"@{server_config['host']}:{server_config['port']}"
                f"?charset={server_config['charset']}"
            )
            
            server_engine = create_engine(server_connection_string)
            
            with server_engine.connect() as conn:
                # 创建数据库
                conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {self.config['database']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
                conn.commit()
            
            logger.info(f"✅ 数据库 '{self.config['database']}' 创建成功")
            
        except Exception as e:
            logger.error(f"❌ 数据库创建失败: {str(e)}")
            raise
    
    def initialize_tables(self):
        """初始化数据表结构"""
        try:
            if not self.engine:
                self.create_engine()
            
            # 创建业务数据表
            business_data_table = Table(
                'business_data', self.metadata,
                Column('id', Integer, primary_key=True, autoincrement=True),
                Column('date', DateTime, nullable=False, comment='日期'),
                Column('category', String(100), nullable=False, comment='业务类别'),
                Column('region', String(100), nullable=False, comment='地区'),
                Column('gmv', Float, nullable=False, comment='GMV'),
                Column('dau', Integer, nullable=False, comment='日活跃用户数'),
                Column('order_price', Float, nullable=False, comment='订单均价'),
                Column('conversion_rate', Float, nullable=False, comment='转化率'),
                Column('created_at', DateTime, default=datetime.now, comment='创建时间'),
                Column('updated_at', DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间'),
                mysql_engine='InnoDB',
                mysql_charset='utf8mb4'
            )
            
            # 创建用户数据表
            users_table = Table(
                'users', self.metadata,
                Column('id', Integer, primary_key=True, autoincrement=True),
                Column('username', String(50), unique=True, nullable=False, comment='用户名'),
                Column('email', String(100), unique=True, nullable=True, comment='邮箱'),
                Column('password_hash', String(255), nullable=False, comment='密码哈希'),
                Column('role', String(20), default='user', comment='用户角色'),
                Column('is_active', Integer, default=1, comment='是否激活'),
                Column('created_at', DateTime, default=datetime.now, comment='创建时间'),
                Column('last_login', DateTime, nullable=True, comment='最后登录时间'),
                mysql_engine='InnoDB',
                mysql_charset='utf8mb4'
            )
            
            # 创建报告数据表
            reports_table = Table(
                'reports', self.metadata,
                Column('id', Integer, primary_key=True, autoincrement=True),
                Column('title', String(200), nullable=False, comment='报告标题'),
                Column('type', String(50), nullable=False, comment='报告类型'),
                Column('content', Text, nullable=True, comment='报告内容'),
                Column('status', String(20), default='draft', comment='报告状态'),
                Column('created_by', String(50), nullable=False, comment='创建者'),
                Column('created_at', DateTime, default=datetime.now, comment='创建时间'),
                Column('updated_at', DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间'),
                mysql_engine='InnoDB',
                mysql_charset='utf8mb4'
            )
            
            # 创建系统日志表
            system_logs_table = Table(
                'system_logs', self.metadata,
                Column('id', Integer, primary_key=True, autoincrement=True),
                Column('level', String(20), nullable=False, comment='日志级别'),
                Column('message', Text, nullable=False, comment='日志消息'),
                Column('module', String(100), nullable=True, comment='模块名'),
                Column('user_id', String(50), nullable=True, comment='用户ID'),
                Column('ip_address', String(45), nullable=True, comment='IP地址'),
                Column('created_at', DateTime, default=datetime.now, comment='创建时间'),
                mysql_engine='InnoDB',
                mysql_charset='utf8mb4'
            )
            
            # 创建所有表
            self.metadata.create_all(self.engine)
            
            logger.info("✅ 数据表初始化成功")
            
        except Exception as e:
            logger.error(f"❌ 数据表初始化失败: {str(e)}")
            raise
    
    def get_session(self):
        """获取数据库会话"""
        if not self.Session:
            self.create_engine()
        return self.Session()
    
    def close_engine(self):
        """关闭数据库引擎"""
        if self.engine:
            self.engine.dispose()
            logger.info("✅ 数据库连接已关闭")


# 全局数据库配置实例
db_config = DatabaseConfig()

def get_database_config() -> DatabaseConfig:
    """获取数据库配置实例"""
    return db_config

def init_database(config: Optional[Dict[str, Any]] = None) -> DatabaseConfig:
    """
    初始化数据库
    
    Args:
        config: 数据库配置字典
        
    Returns:
        DatabaseConfig: 数据库配置实例
    """
    global db_config
    
    if config:
        db_config = DatabaseConfig(config)
    
    try:
        # 创建数据库
        db_config.create_database_if_not_exists()
        
        # 创建引擎
        db_config.create_engine()
        
        # 测试连接
        if not db_config.test_connection():
            raise Exception("数据库连接测试失败")
        
        # 初始化表结构
        db_config.initialize_tables()
        
        logger.info("🎉 数据库初始化完成")
        return db_config
        
    except Exception as e:
        logger.error(f"❌ 数据库初始化失败: {str(e)}")
        raise


if __name__ == "__main__":
    # 测试数据库配置
    test_config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': 'your_password',  # 请设置实际密码
        'database': 'analysis_system_test'
    }
    
    try:
        db = init_database(test_config)
        print("数据库初始化测试成功！")
    except Exception as e:
        print(f"数据库初始化测试失败: {e}") 