#!/usr/bin/env python3
"""
数据库测试脚本
"""

from src.core.database import db_manager

def test_database():
    """测试数据库连接"""
    try:
        print("正在测试数据库连接...")

        # 检查数据库健康状态
        health = db_manager.health_check()
        print(f"数据库状态: {health}")

        # 获取表信息
        table_info = db_manager.get_table_info()
        print(f"数据库表数量: {len(table_info)}")
        print("表列表:", list(table_info.keys()))

        # 测试会话
        with db_manager.get_session() as session:
            print("数据库会话测试成功")

        print("✅ 数据库测试完成")

    except Exception as e:
        print(f"❌ 数据库测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_database()
