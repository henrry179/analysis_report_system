#!/usr/bin/env python3
"""
SQL工作空间管理器
整合SQL代码管理和个性化数据集功能的统一入口
"""

import os
import sys
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional

# 添加项目根目录到路径
sys.path.append(os.path.dirname(__file__))

from src.data.sql_manager import SQLManager, interactive_sql_manager
from src.data.custom_dataset_generator import CustomDatasetGenerator, interactive_dataset_generator
from src.data.mysql_manager import MySQLManager

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SQLWorkspaceManager:
    """SQL工作空间管理器"""
    
    def __init__(self):
        """初始化工作空间管理器"""
        self.config = None
        self.sql_manager = None
        self.dataset_generator = None
        self.mysql_manager = None
        
        # 创建工作空间目录
        self._create_workspace()
    
    def _create_workspace(self):
        """创建工作空间目录结构"""
        directories = [
            "sql_scripts",
            "sql_scripts/queries",
            "sql_scripts/schema", 
            "sql_scripts/procedures",
            "sql_scripts/functions",
            "custom_datasets",
            "custom_datasets/csv",
            "custom_datasets/json", 
            "custom_datasets/excel",
            "sql_templates",
            "dataset_templates",
            "exports",
            "backups"
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
        
        logger.info("✅ SQL工作空间目录结构创建完成")
    
    def load_database_config(self, config_file: str = "mysql_config.json") -> bool:
        """
        加载数据库配置
        
        Args:
            config_file: 配置文件路径
            
        Returns:
            bool: 加载是否成功
        """
        try:
            if os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                
                # 如果密码被隐藏，需要重新输入
                if self.config.get('password') == '***':
                    password = input("请输入MySQL密码: ")
                    self.config['password'] = password
                
                logger.info(f"✅ 数据库配置加载成功: {config_file}")
                return True
            else:
                logger.warning(f"⚠️ 配置文件不存在: {config_file}")
                return False
                
        except Exception as e:
            logger.error(f"❌ 数据库配置加载失败: {str(e)}")
            return False
    
    def setup_database_connection(self) -> bool:
        """
        设置数据库连接
        
        Returns:
            bool: 设置是否成功
        """
        try:
            if not self.config:
                print("⚠️ 请先配置数据库连接信息")
                return self._interactive_database_setup()
            
            # 创建MySQL管理器
            self.mysql_manager = MySQLManager(self.config)
            
            if self.mysql_manager.setup_database():
                if self.mysql_manager.test_connection():
                    logger.info("✅ 数据库连接设置成功")
                    return True
            
            logger.error("❌ 数据库连接设置失败")
            return False
            
        except Exception as e:
            logger.error(f"❌ 数据库连接设置失败: {str(e)}")
            return False
    
    def _interactive_database_setup(self) -> bool:
        """交互式数据库设置"""
        print("\n🔧 数据库连接配置")
        print("=" * 50)
        
        print("选择配置方式:")
        print("1. 快速配置 (localhost:3306, root用户)")
        print("2. 自定义配置")
        
        choice = input("请选择 (1-2): ").strip()
        
        if choice == '1':
            # 快速配置
            password = input("请输入MySQL root密码: ")
            self.config = {
                'host': 'localhost',
                'port': 3306,
                'user': 'root',
                'password': password,
                'database': 'analysis_system',
                'charset': 'utf8mb4'
            }
        
        elif choice == '2':
            # 自定义配置
            host = input("数据库主机 (默认: localhost): ") or "localhost"
            port = input("数据库端口 (默认: 3306): ") or "3306"
            user = input("数据库用户名 (默认: root): ") or "root"
            password = input("数据库密码: ")
            database = input("数据库名称 (默认: analysis_system): ") or "analysis_system"
            
            self.config = {
                'host': host,
                'port': int(port),
                'user': user,
                'password': password,
                'database': database,
                'charset': 'utf8mb4'
            }
        
        else:
            print("❌ 无效选择")
            return False
        
        # 保存配置
        self._save_database_config()
        
        # 设置连接
        return self.setup_database_connection()
    
    def _save_database_config(self):
        """保存数据库配置"""
        try:
            # 创建安全的配置副本（隐藏密码）
            safe_config = self.config.copy()
            safe_config['password'] = '***'
            
            with open('mysql_config.json', 'w', encoding='utf-8') as f:
                json.dump(safe_config, f, ensure_ascii=False, indent=2)
            
            logger.info("✅ 数据库配置已保存到 mysql_config.json")
            
        except Exception as e:
            logger.error(f"❌ 数据库配置保存失败: {str(e)}")
    
    def initialize_managers(self):
        """初始化管理器"""
        try:
            # 初始化SQL管理器
            self.sql_manager = SQLManager(self.config)
            
            # 初始化数据集生成器
            self.dataset_generator = CustomDatasetGenerator()
            
            # 生成SQL模板
            self.sql_manager.generate_sql_templates()
            
            logger.info("✅ 管理器初始化完成")
            
        except Exception as e:
            logger.error(f"❌ 管理器初始化失败: {str(e)}")
    
    def create_sample_sql_files(self):
        """创建示例SQL文件"""
        sample_sqls = {
            'business_analysis.sql': """-- 商业数据分析示例
SELECT 
    DATE(date) as analysis_date,
    category,
    region,
    SUM(gmv) as total_gmv,
    AVG(order_price) as avg_order_price,
    SUM(dau) as total_dau,
    AVG(conversion_rate) as avg_conversion_rate
FROM business_data
WHERE date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
GROUP BY DATE(date), category, region
ORDER BY analysis_date DESC, total_gmv DESC;""",
            
            'user_profile_analysis.sql': """-- 用户画像分析示例
SELECT 
    age_group,
    gender,
    user_level,
    COUNT(*) as user_count,
    AVG(total_amount) as avg_spending,
    AVG(credit_score) as avg_credit_score
FROM (
    SELECT 
        *,
        CASE 
            WHEN age BETWEEN 18 AND 25 THEN '18-25'
            WHEN age BETWEEN 26 AND 35 THEN '26-35'
            WHEN age BETWEEN 36 AND 45 THEN '36-45'
            ELSE '45+'
        END as age_group
    FROM user_data
) u
GROUP BY age_group, gender, user_level
ORDER BY user_count DESC;""",
            
            'product_performance.sql': """-- 产品销售表现分析
SELECT 
    category,
    brand,
    COUNT(*) as product_count,
    AVG(rating) as avg_rating,
    SUM(sold_quantity) as total_sold,
    AVG(selling_price) as avg_price,
    SUM(sold_quantity * selling_price) as total_revenue
FROM product_data
WHERE is_active = 1
GROUP BY category, brand
HAVING total_sold > 0
ORDER BY total_revenue DESC;""",
            
            'financial_risk_analysis.sql': """-- 财务风险分析示例
SELECT 
    DATE(transaction_date) as trans_date,
    transaction_type,
    COUNT(*) as transaction_count,
    SUM(amount) as total_amount,
    AVG(risk_score) as avg_risk_score,
    SUM(CASE WHEN is_suspicious = 1 THEN 1 ELSE 0 END) as suspicious_count,
    ROUND(SUM(CASE WHEN is_suspicious = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as suspicious_rate
FROM financial_data
WHERE transaction_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
GROUP BY DATE(transaction_date), transaction_type
ORDER BY trans_date DESC, suspicious_rate DESC;"""
        }
        
        for filename, content in sample_sqls.items():
            if self.sql_manager:
                self.sql_manager.create_sql_file(filename, content, "queries")
        
        logger.info("✅ 示例SQL文件创建完成")
    
    def create_sample_datasets(self):
        """创建示例数据集"""
        if not self.dataset_generator:
            return
        
        print("🚀 开始创建示例数据集...")
        
        # 创建商业数据集
        business_df = self.dataset_generator.create_business_dataset("sample_business_data", 500, 180)
        if not business_df.empty:
            print(f"✅ 商业数据集创建完成: {len(business_df)} 条数据")
        
        # 创建用户数据集
        user_df = self.dataset_generator.create_user_dataset("sample_user_data", 300)
        if not user_df.empty:
            print(f"✅ 用户数据集创建完成: {len(user_df)} 条数据")
        
        # 创建产品数据集
        product_df = self.dataset_generator.create_product_dataset("sample_product_data", 200)
        if not product_df.empty:
            print(f"✅ 产品数据集创建完成: {len(product_df)} 条数据")
        
        # 创建财务数据集
        financial_df = self.dataset_generator.create_financial_dataset("sample_financial_data", 400)
        if not financial_df.empty:
            print(f"✅ 财务数据集创建完成: {len(financial_df)} 条数据")
        
        print("🎉 示例数据集创建完成！")
    
    def import_datasets_to_database(self):
        """将数据集导入到数据库"""
        if not self.sql_manager or not self.mysql_manager:
            print("❌ 数据库连接未初始化")
            return
        
        dataset_files = [
            ("custom_datasets/sample_business_data.csv", "business_data"),
            ("custom_datasets/sample_user_data.csv", "user_data"),
            ("custom_datasets/sample_product_data.csv", "product_data"),
            ("custom_datasets/sample_financial_data.csv", "financial_data")
        ]
        
        for file_path, table_name in dataset_files:
            if os.path.exists(file_path):
                print(f"📥 导入数据集: {file_path} -> {table_name}")
                if self.sql_manager.import_custom_dataset(file_path, table_name):
                    print(f"✅ 数据集导入成功: {table_name}")
                else:
                    print(f"❌ 数据集导入失败: {table_name}")
            else:
                print(f"⚠️ 数据集文件不存在: {file_path}")
    
    def show_workspace_status(self):
        """显示工作空间状态"""
        print("\n📊 SQL工作空间状态")
        print("=" * 60)
        
        # 显示数据库连接状态
        if self.mysql_manager and self.mysql_manager.test_connection():
            print("🟢 数据库连接: 正常")
            print(f"   主机: {self.config['host']}:{self.config['port']}")
            print(f"   数据库: {self.config['database']}")
        else:
            print("🔴 数据库连接: 未连接")
        
        # 显示SQL文件统计
        if self.sql_manager:
            sql_files = self.sql_manager.list_sql_files()
            print(f"📁 SQL文件: {len(sql_files)} 个")
            
            file_types = {}
            for file in sql_files:
                file_type = file['type']
                file_types[file_type] = file_types.get(file_type, 0) + 1
            
            for file_type, count in file_types.items():
                print(f"   {file_type}: {count} 个")
        
        # 显示数据集统计
        dataset_dir = "custom_datasets"
        if os.path.exists(dataset_dir):
            csv_files = [f for f in os.listdir(dataset_dir) if f.endswith('.csv')]
            json_files = [f for f in os.listdir(dataset_dir) if f.endswith('.json')]
            excel_files = [f for f in os.listdir(dataset_dir) if f.endswith('.xlsx')]
            
            print(f"📊 数据集文件: {len(csv_files + json_files + excel_files)} 个")
            print(f"   CSV: {len(csv_files)} 个")
            print(f"   JSON: {len(json_files)} 个")
            print(f"   Excel: {len(excel_files)} 个")
        
        # 显示模板统计
        if self.dataset_generator:
            templates = self.dataset_generator.list_templates()
            print(f"📋 数据模板: {len(templates)} 个")
    
    def run_interactive_menu(self):
        """运行交互式菜单"""
        while True:
            print("\n🎯 SQL工作空间管理器")
            print("=" * 60)
            print("1. 数据库连接管理")
            print("2. SQL代码管理")
            print("3. 数据集生成器")
            print("4. 创建示例数据")
            print("5. 导入数据到数据库")
            print("6. 工作空间状态")
            print("7. 快速开始向导")
            print("8. 退出")
            
            choice = input("\n请选择操作 (1-8): ").strip()
            
            if choice == '1':
                # 数据库连接管理
                print("\n数据库连接管理:")
                print("1. 测试连接")
                print("2. 重新配置")
                print("3. 查看配置")
                
                sub_choice = input("选择 (1-3): ").strip()
                
                if sub_choice == '1':
                    if self.mysql_manager and self.mysql_manager.test_connection():
                        print("✅ 数据库连接正常")
                    else:
                        print("❌ 数据库连接失败")
                
                elif sub_choice == '2':
                    self._interactive_database_setup()
                    self.initialize_managers()
                
                elif sub_choice == '3':
                    if self.config:
                        safe_config = self.config.copy()
                        safe_config['password'] = '***'
                        print("当前数据库配置:")
                        print(json.dumps(safe_config, ensure_ascii=False, indent=2))
                    else:
                        print("❌ 未找到数据库配置")
            
            elif choice == '2':
                # SQL代码管理
                if self.sql_manager:
                    interactive_sql_manager()
                else:
                    print("❌ SQL管理器未初始化")
            
            elif choice == '3':
                # 数据集生成器
                if self.dataset_generator:
                    interactive_dataset_generator()
                else:
                    print("❌ 数据集生成器未初始化")
            
            elif choice == '4':
                # 创建示例数据
                self.create_sample_datasets()
                self.create_sample_sql_files()
            
            elif choice == '5':
                # 导入数据到数据库
                self.import_datasets_to_database()
            
            elif choice == '6':
                # 工作空间状态
                self.show_workspace_status()
            
            elif choice == '7':
                # 快速开始向导
                self.quick_start_wizard()
            
            elif choice == '8':
                print("👋 感谢使用SQL工作空间管理器")
                break
            
            else:
                print("❌ 无效选择，请重试")
    
    def quick_start_wizard(self):
        """快速开始向导"""
        print("\n🚀 快速开始向导")
        print("=" * 50)
        print("这个向导将帮助您快速设置SQL工作空间")
        
        # 步骤1: 数据库配置
        print("\n📋 步骤 1/4: 数据库配置")
        if not self.config:
            if not self._interactive_database_setup():
                print("❌ 数据库配置失败，向导终止")
                return
        else:
            print("✅ 数据库配置已存在")
        
        # 步骤2: 初始化管理器
        print("\n📋 步骤 2/4: 初始化管理器")
        self.initialize_managers()
        
        # 步骤3: 创建示例数据
        print("\n📋 步骤 3/4: 创建示例数据")
        create_samples = input("是否创建示例数据集和SQL文件? (y/n): ").lower() == 'y'
        if create_samples:
            self.create_sample_datasets()
            self.create_sample_sql_files()
        
        # 步骤4: 导入数据到数据库
        print("\n📋 步骤 4/4: 导入数据到数据库")
        if create_samples:
            import_data = input("是否将示例数据导入到数据库? (y/n): ").lower() == 'y'
            if import_data:
                self.import_datasets_to_database()
        
        print("\n🎉 快速开始向导完成！")
        print("现在您可以:")
        print("- 使用SQL代码管理功能编写和执行SQL")
        print("- 使用数据集生成器创建个性化数据")
        print("- 查看工作空间状态了解当前情况")
        
        # 播放30秒轻音乐提醒
        self.play_completion_music()
    
    def play_completion_music(self):
        """播放完成提醒音乐"""
        try:
            current_time = datetime.now()
            hour = current_time.hour
            
            # 根据时间选择不同的提醒方式
            if 22 <= hour or hour <= 8:
                # 深夜模式：轻柔提醒
                print("🌙 深夜模式：SQL工作空间设置完成")
                os.system("say '工作空间设置完成，请开始您的SQL开发之旅' --voice='Ting-Ting' --rate=120")
            else:
                # 日间模式：播放提醒音效
                print("🎵 SQL工作空间设置完成！")
                
                # 播放系统音效
                for i in range(3):
                    os.system("afplay /System/Library/Sounds/Glass.aiff")
                    if i < 2:
                        os.system("sleep 0.5")
                
                # 语音提醒
                os.system("say '恭喜！SQL工作空间设置完成，现在可以开始编写个性化的SQL代码和数据集了' --voice='Mei-Jia' --rate=180")
                
        except Exception as e:
            logger.error(f"播放提醒音乐失败: {str(e)}")


def main():
    """主函数"""
    print("🎯 欢迎使用SQL工作空间管理器")
    print("=" * 60)
    print("这是一个专为本地SQL开发和个性化数据集管理设计的工具")
    print("支持:")
    print("- 📝 本地SQL代码文件编写和管理")
    print("- 🗄️ MySQL数据库连接和操作")
    print("- 📊 个性化数据集生成和导入")
    print("- 🔧 完整的开发工作流程")
    
    # 创建工作空间管理器
    workspace_manager = SQLWorkspaceManager()
    
    # 尝试加载现有配置
    if workspace_manager.load_database_config():
        workspace_manager.setup_database_connection()
        workspace_manager.initialize_managers()
    
    # 运行交互式菜单
    workspace_manager.run_interactive_menu()


if __name__ == "__main__":
    main() 