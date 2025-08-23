#!/usr/bin/env python3
"""
数据库迁移管理模块
使用Alembic管理数据库版本和迁移
"""

import os
import logging
from pathlib import Path
from typing import Optional

from alembic import command
from alembic.config import Config
from alembic.migration import MigrationContext
from alembic.script import ScriptDirectory
from sqlalchemy import create_engine, text

from .database import db_manager
from ..config.settings import settings

logger = logging.getLogger(__name__)

class MigrationManager:
    """数据库迁移管理器"""

    def __init__(self, alembic_ini_path: Optional[Path] = None):
        """
        初始化迁移管理器

        Args:
            alembic_ini_path: alembic.ini文件路径
        """
        self.project_root = Path(__file__).parent.parent.parent
        self.alembic_ini_path = alembic_ini_path or self.project_root / "alembic.ini"
        self.versions_dir = self.project_root / "migrations" / "versions"

    def init_alembic(self):
        """初始化Alembic配置"""
        try:
            if not self.alembic_ini_path.exists():
                self._create_alembic_ini()

            if not self.versions_dir.exists():
                self.versions_dir.mkdir(parents=True, exist_ok=True)

            logger.info("Alembic配置初始化成功")

        except Exception as e:
            logger.error(f"Alembic配置初始化失败: {str(e)}")
            raise

    def _create_alembic_ini(self):
        """创建alembic.ini配置文件"""
        alembic_ini_content = f"""
# A generic, single database configuration.

[alembic]
# path to migration scripts
script_location = migrations

# template used to generate migration files
# file_template = %%(rev)s_%%(slug)s

# sys.path path, will be prepended to sys.path if present.
# defaults to the current working directory.
prepend_sys_path = .

# timezone to use when rendering the date within the migration file
# as well as the filename.
# If specified, requires the python-dateutil library that can be
# installed by adding `alembic[tz]` to the pip requirements
# string value is passed to dateutil.tz.gettz()
timezone = UTC

# max length of characters to apply to the
# "slug" field
# truncate_slug_length = 40

# set to 'true' to run the environment file as a script, rather than importing it
run_as_script = true

# set to 'true' to force empty revision file creation
# force_empty_revisions = false

# template used to generate migration files
# file_template = %%(rev)s_%%(slug)s

# file_template = %%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d%%(second).2d_%%(slug)s
file_template = %%(year)d%%(month).2d%%(day).2d_%%(hour).2d%%(minute).2d%%(second).2d_%%(slug)s

# own function for generating new revision files
# revision_environment = false

# [logging]
# logging configuration
# logging = logging.conf

# This setting is only used in a 'pending' state to suppress the generation of a new migration file
# when alembic check is run.
# check_suppress_on = true

[post_write_hooks]
# post_write_hooks defines scripts or Python functions that are run
# on newly generated revision scripts.  See the documentation for further
# detail and examples

# format using "black" - use the console_scripts runner, against the "black" entrypoint:
# hooks = black
# black.type = console_scripts
# black.entrypoint = black
# black.options = -l 79

# Logging configuration
[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %%(levelname)-5.5s [%%(name)s] %%(message)s
datefmt = %%H:%%M:%%S

[database]
# Database URL for migrations
url = {settings.DATABASE_URL}
"""

        with open(self.alembic_ini_path, 'w', encoding='utf-8') as f:
            f.write(alembic_ini_content)

        logger.info(f"创建alembic.ini配置文件: {self.alembic_ini_path}")

    def _get_alembic_config(self) -> Config:
        """获取Alembic配置对象"""
        if not self.alembic_ini_path.exists():
            raise FileNotFoundError(f"Alembic配置文件不存在: {self.alembic_ini_path}")

        config = Config(str(self.alembic_ini_path))
        config.set_main_option("script_location", "migrations")
        config.set_main_option("url", settings.DATABASE_URL)

        return config

    def create_migration(self, message: str = "auto"):
        """
        创建新的迁移文件

        Args:
            message: 迁移消息
        """
        try:
            config = self._get_alembic_config()
            command.revision(config, message=message, autogenerate=True)
            logger.info(f"数据库迁移文件创建成功: {message}")

        except Exception as e:
            logger.error(f"创建数据库迁移失败: {str(e)}")
            raise

    def upgrade_database(self, revision: str = "head"):
        """
        升级数据库到指定版本

        Args:
            revision: 目标版本，默认为最新版本
        """
        try:
            config = self._get_alembic_config()
            command.upgrade(config, revision)
            logger.info(f"数据库升级成功: {revision}")

        except Exception as e:
            logger.error(f"数据库升级失败: {str(e)}")
            raise

    def downgrade_database(self, revision: str = "-1"):
        """
        降级数据库到指定版本

        Args:
            revision: 目标版本
        """
        try:
            config = self._get_alembic_config()
            command.downgrade(config, revision)
            logger.info(f"数据库降级成功: {revision}")

        except Exception as e:
            logger.error(f"数据库降级失败: {str(e)}")
            raise

    def get_current_revision(self) -> str:
        """获取当前数据库版本"""
        try:
            config = self._get_alembic_config()
            with db_manager.engine.connect() as conn:
                context = MigrationContext.configure(conn)
                return context.get_current_revision()

        except Exception as e:
            logger.error(f"获取当前数据库版本失败: {str(e)}")
            return "unknown"

    def get_migration_history(self) -> list:
        """获取迁移历史"""
        try:
            config = self._get_alembic_config()
            script_dir = ScriptDirectory.from_config(config)

            history = []
            for script in script_dir.walk_revisions():
                history.append({
                    'revision': script.revision,
                    'down_revision': script.down_revision,
                    'doc': script.doc,
                    'created_at': getattr(script, 'create_date', None)
                })

            return history

        except Exception as e:
            logger.error(f"获取迁移历史失败: {str(e)}")
            return []

    def check_migration_state(self) -> Dict[str, Any]:
        """检查迁移状态"""
        try:
            config = self._get_alembic_config()

            # 获取当前数据库版本
            current_rev = self.get_current_revision()

            # 获取最新迁移版本
            script_dir = ScriptDirectory.from_config(config)
            head_rev = script_dir.get_current_head()

            return {
                'current_revision': current_rev,
                'head_revision': head_rev,
                'is_up_to_date': current_rev == head_rev,
                'needs_upgrade': current_rev != head_rev
            }

        except Exception as e:
            logger.error(f"检查迁移状态失败: {str(e)}")
            return {
                'current_revision': 'unknown',
                'head_revision': 'unknown',
                'is_up_to_date': False,
                'needs_upgrade': True,
                'error': str(e)
            }


# 全局迁移管理器实例
migration_manager = MigrationManager()

# 便捷函数
def init_migrations():
    """初始化数据库迁移的便捷函数"""
    migration_manager.init_alembic()


def create_migration(message: str = "auto"):
    """创建迁移的便捷函数"""
    migration_manager.create_migration(message)


def upgrade_database(revision: str = "head"):
    """升级数据库的便捷函数"""
    migration_manager.upgrade_database(revision)


def check_migration_state():
    """检查迁移状态的便捷函数"""
    return migration_manager.check_migration_state()
