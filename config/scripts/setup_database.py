#!/usr/bin/env python3
"""
数据库初始化脚本
设置和初始化项目数据库
"""

import sys
import logging
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.config.settings import settings
from src.core.database import db_manager, init_database, reset_database
from src.core.migration import migration_manager, init_migrations
from src.core.database_service import user_service

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_database():
    """设置数据库"""
    try:
        logger.info("开始数据库设置...")

        # 1. 初始化数据库管理器
        logger.info(f"数据库URL: {settings.DATABASE_URL}")
        logger.info(f"数据库类型: {settings.DATABASE_URL.split('://')[0]}")

        # 2. 初始化数据库表
        logger.info("创建数据库表...")
        init_database()

        # 3. 初始化Alembic迁移
        logger.info("初始化数据库迁移...")
        init_migrations()

        # 4. 检查数据库连接
        logger.info("检查数据库连接...")
        health = db_manager.health_check()
        if health['status'] == 'healthy':
            logger.info("✅ 数据库连接正常")
        else:
            logger.error(f"❌ 数据库连接异常: {health.get('error')}")
            return False

        # 5. 创建默认管理员用户（如果不存在）
        logger.info("检查默认管理员用户...")
        with db_manager.get_session() as session:
            admin_user = user_service.get_user_by_username(session, "admin")
            if not admin_user:
                # 创建默认管理员用户
                from passlib.context import CryptContext

                pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
                hashed_password = pwd_context.hash("adminpass")

                admin_data = {
                    "username": "admin",
                    "email": "admin@example.com",
                    "hashed_password": hashed_password,
                    "full_name": "System Administrator",
                    "is_superuser": True,
                    "is_active": True
                }

                admin_user = user_service.create_user(session, admin_data)
                logger.info("✅ 默认管理员用户创建成功")
            else:
                logger.info("ℹ️  默认管理员用户已存在")

        # 6. 显示数据库信息
        logger.info("获取数据库表信息...")
        table_info = db_manager.get_table_info()
        logger.info(f"创建的表数量: {len(table_info)}")
        for table_name in table_info.keys():
            logger.info(f"  - {table_name}")

        logger.info("✅ 数据库设置完成！")
        return True

    except Exception as e:
        logger.error(f"❌ 数据库设置失败: {str(e)}")
        return False

def reset_database_data():
    """重置数据库数据"""
    try:
        logger.warning("开始重置数据库...")
        confirm = input("⚠️  此操作将删除所有数据！确认继续？(yes/no): ")
        if confirm.lower() != 'yes':
            logger.info("操作已取消")
            return False

        reset_database()
        logger.info("✅ 数据库重置完成")
        return True

    except Exception as e:
        logger.error(f"❌ 数据库重置失败: {str(e)}")
        return False

def show_database_info():
    """显示数据库信息"""
    try:
        logger.info("数据库信息:")
        logger.info(f"  URL: {settings.DATABASE_URL}")
        logger.info(f"  类型: {settings.DATABASE_URL.split('://')[0]}")

        # 检查迁移状态
        migration_state = migration_manager.check_migration_state()
        logger.info(f"  当前版本: {migration_state.get('current_revision')}")
        logger.info(f"  最新版本: {migration_state.get('head_revision')}")
        logger.info(f"  状态: {'✅ 最新' if migration_state.get('is_up_to_date') else '⚠️ 需要升级'}")

        # 检查连接
        health = db_manager.health_check()
        logger.info(f"  连接状态: {'✅ 正常' if health['status'] == 'healthy' else '❌ 异常'}")

        # 表信息
        table_info = db_manager.get_table_info()
        logger.info(f"  表数量: {len(table_info)}")
        for table_name in table_info.keys():
            logger.info(f"    - {table_name}")

    except Exception as e:
        logger.error(f"获取数据库信息失败: {str(e)}")

def main():
    """主函数"""
    if len(sys.argv) > 1:
        action = sys.argv[1].lower()
    else:
        action = "setup"

    if action == "setup":
        success = setup_database()
        sys.exit(0 if success else 1)

    elif action == "reset":
        success = reset_database_data()
        sys.exit(0 if success else 1)

    elif action == "info":
        show_database_info()
        sys.exit(0)

    elif action == "help":
        print("数据库管理脚本")
        print()
        print("用法:")
        print("  python setup_database.py setup   # 设置数据库")
        print("  python setup_database.py reset   # 重置数据库")
        print("  python setup_database.py info    # 显示数据库信息")
        print("  python setup_database.py help    # 显示帮助")
        print()
        sys.exit(0)

    else:
        print(f"未知命令: {action}")
        print("运行 'python setup_database.py help' 查看帮助")
        sys.exit(1)

if __name__ == "__main__":
    main()
