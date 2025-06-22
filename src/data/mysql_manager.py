#!/usr/bin/env python3
"""
MySQL数据库管理器
集成数据库配置、虚拟数据生成和数据导入功能
"""

import os
import sys
import logging
from typing import Dict, Any, Optional, List
import pandas as pd
from datetime import datetime

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.config.database_config import DatabaseConfig, init_database
from src.data.virtual_data_generator import VirtualDataGenerator

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MySQLManager:
    """MySQL数据库管理器"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化MySQL管理器
        
        Args:
            config: 数据库配置
        """
        self.db_config = None
        self.data_generator = VirtualDataGenerator(seed=42)
        
        # 默认配置
        self.default_config = {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': '',
            'database': 'analysis_system',
            'charset': 'utf8mb4'
        }
        
        if config:
            self.default_config.update(config)
    
    def setup_database(self, password: str = None) -> bool:
        """
        设置数据库连接
        
        Args:
            password: MySQL密码
            
        Returns:
            bool: 设置是否成功
        """
        try:
            if password:
                self.default_config['password'] = password
            
            logger.info("🔧 开始设置MySQL数据库连接...")
            
            # 初始化数据库配置
            self.db_config = init_database(self.default_config)
            
            logger.info("✅ MySQL数据库连接设置成功")
            return True
            
        except Exception as e:
            logger.error(f"❌ MySQL数据库连接设置失败: {str(e)}")
            return False
    
    def test_connection(self) -> bool:
        """
        测试数据库连接
        
        Returns:
            bool: 连接是否成功
        """
        if not self.db_config:
            logger.error("❌ 数据库未初始化，请先调用setup_database()")
            return False
        
        return self.db_config.test_connection()
    
    def generate_and_import_data(self) -> bool:
        """
        生成并导入虚拟数据
        
        Returns:
            bool: 导入是否成功
        """
        try:
            if not self.db_config:
                logger.error("❌ 数据库未初始化，请先调用setup_database()")
                return False
            
            logger.info("🚀 开始生成虚拟数据...")
            
            # 生成虚拟数据
            all_data = self.data_generator.generate_all_data()
            
            # 导入数据到MySQL
            success = self._import_data_to_mysql(all_data)
            
            if success:
                logger.info("🎉 虚拟数据生成并导入成功！")
                self._show_data_statistics()
            
            return success
            
        except Exception as e:
            logger.error(f"❌ 虚拟数据生成和导入失败: {str(e)}")
            return False
    
    def _import_data_to_mysql(self, data: Dict[str, pd.DataFrame]) -> bool:
        """
        将数据导入到MySQL数据库
        
        Args:
            data: 数据字典
            
        Returns:
            bool: 导入是否成功
        """
        try:
            logger.info("📥 开始导入数据到MySQL数据库...")
            
            # 获取数据库引擎
            engine = self.db_config.engine
            
            # 导入各个表的数据
            for table_name, df in data.items():
                logger.info(f"导入表 {table_name}...")
                
                # 清空现有数据（可选）
                with engine.connect() as conn:
                    conn.execute(f"DELETE FROM {table_name}")
                    conn.commit()
                
                # 导入新数据
                df.to_sql(table_name, engine, if_exists='append', index=False)
                logger.info(f"✅ 表 {table_name} 导入完成，共 {len(df)} 条记录")
            
            logger.info("✅ 所有数据导入完成")
            return True
            
        except Exception as e:
            logger.error(f"❌ 数据导入失败: {str(e)}")
            return False
    
    def _show_data_statistics(self):
        """显示数据库统计信息"""
        try:
            logger.info("📊 数据库统计信息:")
            logger.info("=" * 50)
            
            engine = self.db_config.engine
            
            # 查询各表记录数
            tables = ['business_data', 'users', 'financial_data', 'ai_agent_data', 
                     'community_group_buying', 'system_logs', 'reports']
            
            with engine.connect() as conn:
                for table in tables:
                    try:
                        result = conn.execute(f"SELECT COUNT(*) FROM {table}")
                        count = result.fetchone()[0]
                        logger.info(f"{table:25} : {count:6} 条记录")
                    except Exception as e:
                        logger.warning(f"查询表 {table} 失败: {str(e)}")
            
        except Exception as e:
            logger.error(f"❌ 获取统计信息失败: {str(e)}")
    
    def query_data(self, sql: str) -> Optional[pd.DataFrame]:
        """
        执行SQL查询
        
        Args:
            sql: SQL查询语句
            
        Returns:
            DataFrame: 查询结果
        """
        try:
            if not self.db_config:
                logger.error("❌ 数据库未初始化")
                return None
            
            df = pd.read_sql(sql, self.db_config.engine)
            logger.info(f"✅ 查询完成，返回 {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"❌ 查询失败: {str(e)}")
            return None
    
    def get_business_data(self, limit: int = 100) -> Optional[pd.DataFrame]:
        """
        获取业务数据
        
        Args:
            limit: 限制返回记录数
            
        Returns:
            DataFrame: 业务数据
        """
        sql = f"""
        SELECT date, category, region, gmv, dau, order_price, conversion_rate
        FROM business_data
        ORDER BY date DESC
        LIMIT {limit}
        """
        return self.query_data(sql)
    
    def get_financial_summary(self) -> Optional[pd.DataFrame]:
        """
        获取金融数据汇总
        
        Returns:
            DataFrame: 金融汇总数据
        """
        sql = """
        SELECT 
            transaction_type,
            currency,
            COUNT(*) as transaction_count,
            SUM(amount) as total_amount,
            AVG(amount) as avg_amount,
            SUM(fee) as total_fee
        FROM financial_data
        WHERE status = '成功'
        GROUP BY transaction_type, currency
        ORDER BY total_amount DESC
        """
        return self.query_data(sql)
    
    def get_ai_agent_performance(self) -> Optional[pd.DataFrame]:
        """
        获取AI代理性能数据
        
        Returns:
            DataFrame: AI代理性能数据
        """
        sql = """
        SELECT 
            agent_type,
            model,
            AVG(accuracy) as avg_accuracy,
            AVG(response_time) as avg_response_time,
            AVG(success_rate) as avg_success_rate,
            SUM(daily_requests) as total_requests,
            SUM(monthly_cost) as total_cost
        FROM ai_agent_data
        GROUP BY agent_type, model
        ORDER BY avg_accuracy DESC
        """
        return self.query_data(sql)
    
    def backup_database(self, backup_file: str = None) -> bool:
        """
        备份数据库
        
        Args:
            backup_file: 备份文件路径
            
        Returns:
            bool: 备份是否成功
        """
        try:
            if not backup_file:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_file = f"backup/mysql_backup_{timestamp}.sql"
            
            # 创建备份目录
            os.makedirs(os.path.dirname(backup_file), exist_ok=True)
            
            # 执行mysqldump命令
            config = self.db_config.config
            cmd = (
                f"mysqldump -h{config['host']} -P{config['port']} "
                f"-u{config['user']} -p{config['password']} "
                f"{config['database']} > {backup_file}"
            )
            
            result = os.system(cmd)
            
            if result == 0:
                logger.info(f"✅ 数据库备份成功: {backup_file}")
                return True
            else:
                logger.error("❌ 数据库备份失败")
                return False
                
        except Exception as e:
            logger.error(f"❌ 数据库备份失败: {str(e)}")
            return False
    
    def close_connection(self):
        """关闭数据库连接"""
        if self.db_config:
            self.db_config.close_engine()
            logger.info("✅ 数据库连接已关闭")


def interactive_setup():
    """交互式设置MySQL数据库"""
    print("🔧 MySQL数据库设置向导")
    print("=" * 40)
    
    # 获取数据库配置
    host = input("数据库主机 (默认: localhost): ") or "localhost"
    port = input("数据库端口 (默认: 3306): ") or "3306"
    user = input("数据库用户名 (默认: root): ") or "root"
    password = input("数据库密码: ")
    database = input("数据库名称 (默认: analysis_system): ") or "analysis_system"
    
    config = {
        'host': host,
        'port': int(port),
        'user': user,
        'password': password,
        'database': database
    }
    
    # 初始化管理器
    manager = MySQLManager(config)
    
    # 设置数据库
    if not manager.setup_database():
        print("❌ 数据库设置失败")
        return None
    
    # 测试连接
    if not manager.test_connection():
        print("❌ 数据库连接测试失败")
        return None
    
    print("✅ 数据库连接成功")
    
    # 询问是否生成虚拟数据
    generate_data = input("是否生成并导入虚拟数据？(y/n): ").lower() == 'y'
    
    if generate_data:
        if manager.generate_and_import_data():
            print("🎉 虚拟数据生成并导入成功！")
        else:
            print("❌ 虚拟数据生成或导入失败")
    
    return manager


def main():
    """主函数"""
    print("🚀 MySQL数据库管理器")
    print("=" * 40)
    
    # 交互式设置
    manager = interactive_setup()
    
    if manager:
        print("\n📊 可用操作:")
        print("1. 查看业务数据")
        print("2. 查看金融汇总")
        print("3. 查看AI代理性能")
        print("4. 备份数据库")
        print("5. 退出")
        
        while True:
            choice = input("\n请选择操作 (1-5): ")
            
            if choice == '1':
                data = manager.get_business_data(10)
                if data is not None:
                    print("\n📈 业务数据 (最近10条):")
                    print(data.to_string(index=False))
            
            elif choice == '2':
                data = manager.get_financial_summary()
                if data is not None:
                    print("\n💰 金融数据汇总:")
                    print(data.to_string(index=False))
            
            elif choice == '3':
                data = manager.get_ai_agent_performance()
                if data is not None:
                    print("\n🤖 AI代理性能:")
                    print(data.to_string(index=False))
            
            elif choice == '4':
                if manager.backup_database():
                    print("✅ 数据库备份完成")
                else:
                    print("❌ 数据库备份失败")
            
            elif choice == '5':
                manager.close_connection()
                print("👋 再见！")
                break
            
            else:
                print("❌ 无效选择，请重新输入")


if __name__ == "__main__":
    main() 