#!/usr/bin/env python3
"""
数据库管理模块
提供SQLAlchemy数据库连接、会话管理和迁移功能
"""

from typing import Generator, Optional, Dict, Any
from contextlib import contextmanager
from pathlib import Path
import logging

from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.pool import StaticPool

from .models import Base
from ..config.settings import settings

logger = logging.getLogger(__name__)

class DatabaseManager:
    """数据库管理器"""

    def __init__(self, database_url: Optional[str] = None):
        """
        初始化数据库管理器

        Args:
            database_url: 数据库连接URL，如果不提供则使用配置文件中的设置
        """
        self.database_url = database_url or settings.DATABASE_URL
        self.engine = None
        self.SessionLocal = None
        self._init_engine()

    def _init_engine(self):
        """初始化数据库引擎"""
        try:
            # 根据数据库类型配置不同的连接参数
            if self.database_url.startswith("sqlite"):
                # SQLite配置
                self.engine = create_engine(
                    self.database_url,
                    connect_args={"check_same_thread": False},
                    poolclass=StaticPool,
                    echo=settings.DEBUG
                )
            elif self.database_url.startswith("postgresql"):
                # PostgreSQL配置
                self.engine = create_engine(
                    self.database_url,
                    pool_pre_ping=True,
                    pool_recycle=3600,
                    pool_size=10,
                    max_overflow=20,
                    echo=settings.DEBUG
                )
            else:
                # 默认配置
                self.engine = create_engine(
                    self.database_url,
                    echo=settings.DEBUG
                )

            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )

            logger.info(f"数据库引擎初始化成功: {self.database_url.split('://')[0]}")

        except Exception as e:
            logger.error(f"数据库引擎初始化失败: {str(e)}")
            raise

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """
        获取数据库会话的上下文管理器

        Yields:
            Session: SQLAlchemy会话对象
        """
        session = self.SessionLocal()
        try:
            yield session
        except Exception as e:
            logger.error(f"数据库会话错误: {str(e)}")
            session.rollback()
            raise
        finally:
            session.close()

    def create_tables(self):
        """创建所有表"""
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("数据库表创建成功")
        except Exception as e:
            logger.error(f"创建数据库表失败: {str(e)}")
            raise

    def drop_tables(self):
        """删除所有表"""
        try:
            Base.metadata.drop_all(bind=self.engine)
            logger.info("数据库表删除成功")
        except Exception as e:
            logger.error(f"删除数据库表失败: {str(e)}")
            raise

    def reset_database(self):
        """重置数据库（删除所有表后重新创建）"""
        try:
            self.drop_tables()
            self.create_tables()
            logger.info("数据库重置成功")
        except Exception as e:
            logger.error(f"数据库重置失败: {str(e)}")
            raise

    def execute_sql_file(self, file_path: Path):
        """
        执行SQL文件

        Args:
            file_path: SQL文件路径
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                sql_content = f.read()

            with self.get_session() as session:
                session.execute(text(sql_content))
                session.commit()

            logger.info(f"SQL文件执行成功: {file_path}")

        except Exception as e:
            logger.error(f"SQL文件执行失败: {str(e)}")
            raise

    def init_database(self):
        """初始化数据库（创建表和基础数据）"""
        try:
            # 创建表
            self.create_tables()

            # 执行初始化SQL脚本（如果存在）
            init_sql_path = Path(__file__).parent.parent.parent / "scripts" / "init_db.sql"
            if init_sql_path.exists():
                self.execute_sql_file(init_sql_path)
                logger.info("数据库初始化脚本执行成功")
            else:
                logger.warning("数据库初始化脚本不存在")

        except Exception as e:
            logger.error(f"数据库初始化失败: {str(e)}")
            raise

    def get_table_info(self) -> Dict[str, Any]:
        """获取数据库表信息"""
        try:
            metadata = MetaData()
            metadata.reflect(bind=self.engine)

            table_info = {}
            for table_name, table in metadata.tables.items():
                table_info[table_name] = {
                    'columns': [column.name for column in table.columns],
                    'primary_keys': [pk.name for pk in table.primary_key.columns],
                    'foreign_keys': [fk.target_fullname for fk in table.foreign_keys]
                }

            return table_info

        except Exception as e:
            logger.error(f"获取数据库表信息失败: {str(e)}")
            return {}

    def health_check(self) -> Dict[str, Any]:
        """数据库健康检查"""
        try:
            with self.get_session() as session:
                # 执行简单查询测试连接
                result = session.execute(text("SELECT 1 as test")).scalar()

                return {
                    'status': 'healthy',
                    'database_type': self.database_url.split('://')[0],
                    'connection_test': result == 1
                }

        except Exception as e:
            logger.error(f"数据库健康检查失败: {str(e)}")
            return {
                'status': 'unhealthy',
                'error': str(e)
            }

    def backup_database(self, backup_path: Path):
        """
        备份数据库（仅SQLite支持）

        Args:
            backup_path: 备份文件路径
        """
        if not self.database_url.startswith("sqlite"):
            raise NotImplementedError("仅SQLite数据库支持备份功能")

        try:
            import shutil
            db_path = self.database_url.replace("sqlite:///", "")
            shutil.copy2(db_path, backup_path)
            logger.info(f"数据库备份成功: {backup_path}")

        except Exception as e:
            logger.error(f"数据库备份失败: {str(e)}")
            raise

    def restore_database(self, backup_path: Path):
        """
        恢复数据库（仅SQLite支持）

        Args:
            backup_path: 备份文件路径
        """
        if not self.database_url.startswith("sqlite"):
            raise NotImplementedError("仅SQLite数据库支持恢复功能")

        try:
            import shutil
            db_path = self.database_url.replace("sqlite:///", "")
            shutil.copy2(backup_path, db_path)
            logger.info(f"数据库恢复成功: {backup_path}")

        except Exception as e:
            logger.error(f"数据库恢复失败: {str(e)}")
            raise


# 全局数据库管理器实例
db_manager = DatabaseManager()

# 便捷函数
def get_db() -> Generator[Session, None, None]:
    """获取数据库会话的便捷函数"""
    with db_manager.get_session() as session:
        yield session


def init_database():
    """初始化数据库的便捷函数"""
    db_manager.init_database()


def reset_database():
    """重置数据库的便捷函数"""
    db_manager.reset_database()
