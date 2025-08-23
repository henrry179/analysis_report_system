"""
Alembic环境配置文件
配置数据库迁移环境
"""

import sys
from logging.config import fileConfig
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import create_engine
from src.config.settings import settings
from src.core.models import Base

# 读取alembic.ini配置
config = sys.modules['alembic'].context.config

# 配置日志
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 设置数据库URL
database_url = settings.DATABASE_URL
config.set_main_option("sqlalchemy.url", database_url)

# 设置目标元数据
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """离线模式运行迁移"""
    url = config.get_main_option("sqlalchemy.url")
    context = sys.modules['alembic'].context
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """在线模式运行迁移"""
    # 创建数据库引擎
    connectable = create_engine(database_url, echo=settings.DEBUG)

    with connectable.connect() as connection:
        context = sys.modules['alembic'].context
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
            include_schemas=True,
            version_table_schema=None,
        )

        with context.begin_transaction():
            context.run_migrations()


if sys.modules['alembic'].context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
