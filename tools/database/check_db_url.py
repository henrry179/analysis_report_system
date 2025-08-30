#!/usr/bin/env python3
"""
检查数据库URL配置
"""

from src.config.settings import settings
from src.core.database import db_manager
import os

def check_db_config():
    """检查数据库配置"""
    print("当前工作目录:", os.getcwd())
    print("数据库URL:", settings.DATABASE_URL)
    print("数据库引擎:", db_manager.engine)
    print("数据库URL (from engine):", db_manager.database_url)

    # 检查数据库文件是否存在
    if "analysis_system.db" in settings.DATABASE_URL:
        db_path = settings.DATABASE_URL.replace("sqlite:///", "")
        print("数据库文件路径:", db_path)
        print("数据库文件是否存在:", os.path.exists(db_path))

        # 如果不存在，尝试创建
        if not os.path.exists(db_path):
            print("正在创建数据库文件...")
            try:
                db_manager.init_database()
                print("✅ 数据库创建成功")
            except Exception as e:
                print(f"❌ 数据库创建失败: {e}")

if __name__ == "__main__":
    check_db_config()
