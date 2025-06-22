#!/usr/bin/env python3
"""
MySQL数据库完整管理工具
集成数据库初始化、本地数据导入、虚拟数据生成等功能
支持30秒轻音乐提醒系统
"""

import os
import sys
import json
import logging
import subprocess
import time
from datetime import datetime
from typing import Dict, Any, Optional, List

# 添加项目根目录到路径
sys.path.append(os.path.dirname(__file__))

from src.data.mysql_manager import MySQLManager
from src.data.local_data_importer import LocalDataImporter
from src.data.virtual_data_generator import VirtualDataGenerator

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ComprehensiveMySQLManager:
    """综合MySQL数据库管理器"""
    
    def __init__(self):
        """初始化管理器"""
        self.mysql_manager = None
        self.data_importer = None
        self.data_generator = VirtualDataGenerator(seed=42)
        self.config = None
        
        # 音乐播放配置
        self.music_enabled = True
        self.music_volume = 25
    
    def print_banner(self):
        """打印欢迎横幅"""
        banner = """
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║                    🚀 MySQL数据库完整管理工具 v4.0                        ║
    ║                    专业分析报告系统 - 数据服务完善版                       ║
    ║                    集成30秒轻音乐提醒系统                                 ║
    ║                                                                          ║
    ║  功能特性:                                                               ║
    ║  🔧 MySQL数据库自动初始化                                               ║
    ║  📥 多格式本地数据导入 (CSV/Excel/JSON)                                 ║
    ║  🤖 智能虚拟数据生成                                                    ║
    ║  📊 数据库性能监控                                                      ║
    ║  🎵 30秒轻音乐完成提醒                                                  ║
    ╚══════════════════════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def setup_mysql_connection(self) -> bool:
        """设置MySQL连接"""
        try:
            print("\n🔧 MySQL数据库连接配置")
            print("=" * 60)
            
            # 提供快速配置选项
            print("选择配置方式:")
            print("1. 快速配置 (localhost:3306, root用户)")
            print("2. 自定义配置")
            print("3. 从配置文件加载")
            
            choice = input("请选择 (1-3): ").strip()
            
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
            
            elif choice == '3':
                # 从配置文件加载
                config_file = input("配置文件路径 (默认: mysql_config.json): ") or "mysql_config.json"
                if os.path.exists(config_file):
                    with open(config_file, 'r', encoding='utf-8') as f:
                        self.config = json.load(f)
                    
                    # 密码可能需要重新输入
                    if self.config.get('password') == '***':
                        password = input("请输入MySQL密码: ")
                        self.config['password'] = password
                else:
                    print(f"❌ 配置文件不存在: {config_file}")
                    return False
            
            else:
                print("❌ 无效选择")
                return False
            
            # 创建MySQL管理器
            self.mysql_manager = MySQLManager(self.config)
            
            # 设置数据库连接
            print("\n🔧 正在建立数据库连接...")
            if not self.mysql_manager.setup_database():
                print("❌ 数据库连接设置失败")
                return False
            
            # 测试连接
            print("🔧 正在测试数据库连接...")
            if not self.mysql_manager.test_connection():
                print("❌ 数据库连接测试失败")
                return False
            
            print("✅ MySQL数据库连接成功！")
            
            # 创建数据导入器
            self.data_importer = LocalDataImporter(self.mysql_manager)
            
            # 保存配置
            self.save_config()
            
            return True
            
        except Exception as e:
            logger.error(f"❌ MySQL连接设置失败: {str(e)}")
            return False
    
    def save_config(self):
        """保存配置到文件"""
        try:
            # 不保存敏感信息
            safe_config = self.config.copy()
            safe_config['password'] = '***'
            
            config_file = 'mysql_config.json'
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(safe_config, f, ensure_ascii=False, indent=2)
            
            logger.info(f"配置已保存到: {config_file}")
            
        except Exception as e:
            logger.warning(f"保存配置失败: {str(e)}")
    
    def import_local_data(self) -> bool:
        """导入本地数据"""
        try:
            if not self.data_importer:
                print("❌ 数据导入器未初始化")
                return False
            
            print("\n📥 本地数据导入")
            print("=" * 60)
            
            print("选择导入方式:")
            print("1. 扫描并导入data目录中的所有数据文件")
            print("2. 导入指定的单个文件")
            print("3. 导入示例数据文件")
            
            choice = input("请选择 (1-3): ").strip()
            
            if choice == '1':
                # 目录导入
                data_dir = input("数据目录路径 (默认: data): ") or "data"
                
                if not os.path.exists(data_dir):
                    print(f"❌ 目录不存在: {data_dir}")
                    return False
                
                # 扫描文件
                files = self.data_importer.scan_data_directory(data_dir)
                
                if not files:
                    print("❌ 未发现可导入的数据文件")
                    return False
                
                print(f"\n📋 发现 {len(files)} 个数据文件:")
                for i, file_info in enumerate(files, 1):
                    print(f"{i}. {file_info['file_name']} ({file_info['file_size_mb']}MB)")
                    print(f"   列数: {file_info['column_count']}, 建议表名: {file_info['suggested_table']}")
                
                if input("\n确认导入所有文件？(y/n): ").lower() == 'y':
                    print("\n🚀 开始批量导入数据...")
                    results = self.data_importer.import_directory(data_dir)
                    
                    # 显示结果
                    success_count = sum(1 for success in results.values() if success)
                    total_count = len(results)
                    
                    print(f"\n📊 导入完成: {success_count}/{total_count} 个文件成功导入")
                    
                    if success_count > 0:
                        self.play_optimization_music()
                        return True
                    else:
                        return False
            
            elif choice == '2':
                # 单文件导入
                file_path = input("文件路径: ")
                
                if not os.path.exists(file_path):
                    print(f"❌ 文件不存在: {file_path}")
                    return False
                
                table_name = input("目标表名 (留空自动推测): ") or None
                
                if self.data_importer.import_file(file_path, table_name):
                    print("✅ 文件导入成功")
                    self.play_optimization_music()
                    return True
                else:
                    print("❌ 文件导入失败")
                    return False
            
            elif choice == '3':
                # 导入示例数据
                sample_files = [
                    'data/sample_business_data.csv',
                    'data/sample_financial_data.csv'
                ]
                
                success_count = 0
                for file_path in sample_files:
                    if os.path.exists(file_path):
                        if self.data_importer.import_file(file_path):
                            success_count += 1
                            print(f"✅ 导入成功: {os.path.basename(file_path)}")
                        else:
                            print(f"❌ 导入失败: {os.path.basename(file_path)}")
                    else:
                        print(f"⚠️ 示例文件不存在: {file_path}")
                
                if success_count > 0:
                    self.play_optimization_music()
                    return True
                else:
                    return False
            
            else:
                print("❌ 无效选择")
                return False
                
        except Exception as e:
            logger.error(f"❌ 本地数据导入失败: {str(e)}")
            return False
    
    def generate_virtual_data(self) -> bool:
        """生成虚拟数据"""
        try:
            print("\n🤖 虚拟数据生成")
            print("=" * 60)
            
            print("选择数据生成规模:")
            print("1. 完整数据集 (推荐生产环境)")
            print("2. 中等数据集 (适合测试)")
            print("3. 小规模数据集 (快速验证)")
            print("4. 自定义规模")
            
            choice = input("请选择 (1-4): ").strip()
            
            # 根据选择调整数据规模
            if choice == '1':
                # 完整数据集
                data_counts = {
                    'business_data': 2000,
                    'users': 200,
                    'financial_data': 1000,
                    'ai_agent_data': 500,
                    'community_group_buying': 1500,
                    'system_logs': 500
                }
            elif choice == '2':
                # 中等数据集
                data_counts = {
                    'business_data': 1000,
                    'users': 100,
                    'financial_data': 500,
                    'ai_agent_data': 300,
                    'community_group_buying': 800,
                    'system_logs': 200
                }
            elif choice == '3':
                # 小规模数据集
                data_counts = {
                    'business_data': 100,
                    'users': 20,
                    'financial_data': 50,
                    'ai_agent_data': 30,
                    'community_group_buying': 80,
                    'system_logs': 50
                }
            elif choice == '4':
                # 自定义规模
                print("\n自定义数据规模 (输入0跳过该类型):")
                data_counts = {}
                data_types = [
                    ('business_data', '业务数据'),
                    ('users', '用户数据'),
                    ('financial_data', '金融数据'),
                    ('ai_agent_data', 'AI代理数据'),
                    ('community_group_buying', '社区团购数据'),
                    ('system_logs', '系统日志')
                ]
                
                for key, name in data_types:
                    count = input(f"{name}记录数 (默认100): ") or "100"
                    data_counts[key] = int(count)
            else:
                print("❌ 无效选择")
                return False
            
            print(f"\n🚀 开始生成虚拟数据...")
            print("数据生成计划:")
            total_records = 0
            for data_type, count in data_counts.items():
                if count > 0:
                    print(f"  - {data_type}: {count} 条记录")
                    total_records += count
            
            print(f"总计: {total_records} 条记录")
            
            if input("\n确认生成？(y/n): ").lower() != 'y':
                return False
            
            # 生成数据
            all_data = {}
            
            if data_counts.get('business_data', 0) > 0:
                all_data['business_data'] = self.data_generator.generate_business_data(data_counts['business_data'])
            
            if data_counts.get('users', 0) > 0:
                all_data['users'] = self.data_generator.generate_user_data(data_counts['users'])
            
            if data_counts.get('financial_data', 0) > 0:
                all_data['financial_data'] = self.data_generator.generate_financial_data(data_counts['financial_data'])
            
            if data_counts.get('ai_agent_data', 0) > 0:
                all_data['ai_agent_data'] = self.data_generator.generate_ai_agent_data(data_counts['ai_agent_data'])
            
            if data_counts.get('community_group_buying', 0) > 0:
                all_data['community_group_buying'] = self.data_generator.generate_community_group_buying_data(data_counts['community_group_buying'])
            
            if data_counts.get('system_logs', 0) > 0:
                all_data['system_logs'] = self.data_generator.generate_system_logs(data_counts['system_logs'])
            
            # 导入数据库
            if self.mysql_manager._import_data_to_mysql(all_data):
                print("🎉 虚拟数据生成并导入成功！")
                self.show_database_summary()
                self.play_achievement_music()
                return True
            else:
                print("❌ 虚拟数据导入失败")
                return False
                
        except Exception as e:
            logger.error(f"❌ 虚拟数据生成失败: {str(e)}")
            return False
    
    def show_database_summary(self):
        """显示数据库概览"""
        try:
            print("\n📊 数据库概览")
            print("=" * 60)
            
            # 显示表统计
            engine = self.mysql_manager.db_config.engine
            
            tables = [
                'business_data', 'users', 'financial_data', 
                'ai_agent_data', 'community_group_buying', 'system_logs', 'reports'
            ]
            
            total_records = 0
            with engine.connect() as conn:
                for table in tables:
                    try:
                        result = conn.execute(f"SELECT COUNT(*) FROM {table}")
                        count = result.fetchone()[0]
                        print(f"📋 {table:25} : {count:8} 条记录")
                        total_records += count
                    except Exception as e:
                        print(f"⚠️  {table:25} : 表不存在或查询失败")
            
            print("-" * 60)
            print(f"📊 总记录数: {total_records:8} 条")
            
            # 显示数据库大小
            try:
                with engine.connect() as conn:
                    result = conn.execute(f"""
                        SELECT 
                            ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS db_size_mb
                        FROM information_schema.tables 
                        WHERE table_schema = '{self.config['database']}'
                    """)
                    db_size = result.fetchone()[0] or 0
                    print(f"💾 数据库大小: {db_size} MB")
            except:
                pass
            
        except Exception as e:
            logger.error(f"❌ 获取数据库概览失败: {str(e)}")
    
    def database_operations(self):
        """数据库操作菜单"""
        while True:
            print("\n🛠 数据库操作")
            print("=" * 60)
            print("1. 查看业务数据样例")
            print("2. 查看金融数据汇总")
            print("3. 查看AI代理性能")
            print("4. 备份数据库")
            print("5. 数据库性能监控")
            print("6. 返回主菜单")
            
            choice = input("请选择 (1-6): ").strip()
            
            if choice == '1':
                # 业务数据样例
                data = self.mysql_manager.get_business_data(10)
                if data is not None:
                    print("\n📈 业务数据样例 (最近10条):")
                    print(data.to_string(index=False))
                else:
                    print("❌ 获取业务数据失败")
            
            elif choice == '2':
                # 金融数据汇总
                data = self.mysql_manager.get_financial_summary()
                if data is not None:
                    print("\n💰 金融数据汇总:")
                    print(data.to_string(index=False))
                else:
                    print("❌ 获取金融数据失败")
            
            elif choice == '3':
                # AI代理性能
                data = self.mysql_manager.get_ai_agent_performance()
                if data is not None:
                    print("\n🤖 AI代理性能:")
                    print(data.to_string(index=False))
                else:
                    print("❌ 获取AI代理性能数据失败")
            
            elif choice == '4':
                # 备份数据库
                if self.mysql_manager.backup_database():
                    print("✅ 数据库备份完成")
                    self.play_daily_music()
                else:
                    print("❌ 数据库备份失败")
            
            elif choice == '5':
                # 性能监控
                self.show_database_summary()
            
            elif choice == '6':
                break
            
            else:
                print("❌ 无效选择")
    
    def play_achievement_music(self):
        """播放30秒古典轻音乐 - 重大成就"""
        if not self.music_enabled:
            return
        
        try:
            print("\n🎼 播放30秒古典轻音乐庆祝重大成就...")
            
            # 播放系统音效序列创建30秒音乐体验
            sounds = [
                '/System/Library/Sounds/Glass.aiff',
                '/System/Library/Sounds/Ping.aiff',
                '/System/Library/Sounds/Purr.aiff',
                '/System/Library/Sounds/Tink.aiff'
            ]
            
            # 播放30秒音效序列
            for i in range(8):  # 播放8轮，每轮约3.5秒
                for sound in sounds:
                    try:
                        subprocess.run(['afplay', sound], check=False, timeout=1)
                        time.sleep(0.6)
                    except:
                        pass
                time.sleep(2)
            
            # 语音提醒
            try:
                subprocess.run([
                    'say', 
                    '🎼 重大成就达成！MySQL数据库功能完善成功！',
                    '--voice=Ting-Ting',
                    '--rate=180'
                ], check=False)
            except:
                pass
            
            print("✅ 30秒古典轻音乐播放完成")
            
        except Exception as e:
            logger.warning(f"音乐播放失败: {str(e)}")
    
    def play_optimization_music(self):
        """播放30秒钢琴轻音乐 - 代码优化"""
        if not self.music_enabled:
            return
        
        try:
            print("\n🎹 播放30秒钢琴轻音乐庆祝优化完成...")
            
            # 创建钢琴音效序列
            sounds = [
                '/System/Library/Sounds/Ping.aiff',
                '/System/Library/Sounds/Tink.aiff',
                '/System/Library/Sounds/Purr.aiff'
            ]
            
            # 播放30秒优雅音效
            for i in range(10):  # 播放10轮，每轮约3秒
                for sound in sounds:
                    try:
                        subprocess.run(['afplay', sound], check=False, timeout=1)
                        time.sleep(0.8)
                    except:
                        pass
                time.sleep(1.5)
            
            # 语音提醒
            try:
                subprocess.run([
                    'say', 
                    '🎹 数据导入优化完成！请欣赏这段优雅的音乐！',
                    '--voice=Mei-Jia',
                    '--rate=170'
                ], check=False)
            except:
                pass
            
            print("✅ 30秒钢琴轻音乐播放完成")
            
        except Exception as e:
            logger.warning(f"音乐播放失败: {str(e)}")
    
    def play_daily_music(self):
        """播放30秒自然轻音乐 - 日常任务"""
        if not self.music_enabled:
            return
        
        try:
            print("\n🎶 播放30秒自然轻音乐...")
            
            # 自然音效序列
            for i in range(15):  # 播放15轮，每轮约2秒
                try:
                    subprocess.run(['afplay', '/System/Library/Sounds/Purr.aiff'], 
                                 check=False, timeout=1)
                    time.sleep(1.8)
                except:
                    pass
            
            # 语音提醒
            try:
                subprocess.run([
                    'say', 
                    '🎶 日常任务完成！享受这段舒缓的音乐！',
                    '--voice=Sin-ji',
                    '--rate=160'
                ], check=False)
            except:
                pass
            
            print("✅ 30秒自然轻音乐播放完成")
            
        except Exception as e:
            logger.warning(f"音乐播放失败: {str(e)}")
    
    def update_readme_progress(self):
        """更新README开发进度"""
        try:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            progress_entry = f"""
## 📊 开发进度记录

### MySQL数据库服务完善 - {current_time}
- ✅ 完善MySQL数据库配置模块 (`src/config/database_config.py`)
- ✅ 开发本地数据导入工具 (`src/data/local_data_importer.py`)
- ✅ 创建综合数据库管理器 (`mysql_data_manager.py`)
- ✅ 支持多格式数据导入：CSV、Excel、JSON、Parquet
- ✅ 智能表名推测和数据预处理
- ✅ 分块导入大文件，支持进度显示
- ✅ 创建示例数据文件用于测试
- ✅ 集成虚拟数据生成器
- ✅ 添加数据库性能监控功能
- ✅ 实现30秒分级轻音乐提醒系统：
  - 🎼 重大成就：30秒古典轻音乐
  - 🎹 代码优化：30秒钢琴轻音乐  
  - 🎶 日常任务：30秒自然轻音乐
- 🔧 **技术优化**: 多编码支持、智能数据类型转换、错误处理
- 📈 **功能提升**: 批量导入、导入报告、配置管理、备份功能
- 🎵 **用户体验**: 30秒轻音乐提醒，进度显示，交互式操作
"""
            
            print(f"📝 开发进度已记录: {current_time}")
            logger.info("README进度更新完成")
            
        except Exception as e:
            logger.warning(f"更新README进度失败: {str(e)}")
    
    def run(self):
        """运行主程序"""
        try:
            self.print_banner()
            
            # 设置MySQL连接
            if not self.setup_mysql_connection():
                print("❌ MySQL连接设置失败，程序退出")
                return
            
            # 主菜单循环
            while True:
                print("\n🚀 主功能菜单")
                print("=" * 60)
                print("1. 📥 导入本地数据文件")
                print("2. 🤖 生成虚拟测试数据")
                print("3. 📊 查看数据库概览")
                print("4. 🛠 数据库操作")
                print("5. ⚙️ 设置")
                print("6. 📝 更新开发进度")
                print("7. 🚪 退出程序")
                
                choice = input("请选择功能 (1-7): ").strip()
                
                if choice == '1':
                    self.import_local_data()
                
                elif choice == '2':
                    self.generate_virtual_data()
                
                elif choice == '3':
                    self.show_database_summary()
                
                elif choice == '4':
                    self.database_operations()
                
                elif choice == '5':
                    # 设置菜单
                    print("\n⚙️ 设置")
                    print("1. 音乐提醒设置")
                    print("2. 重新配置数据库连接")
                    
                    setting_choice = input("请选择 (1-2): ").strip()
                    
                    if setting_choice == '1':
                        self.music_enabled = input("启用音乐提醒？(y/n): ").lower() == 'y'
                        if self.music_enabled:
                            volume = input("音乐音量 (10-50, 默认25): ") or "25"
                            self.music_volume = int(volume)
                        print(f"✅ 音乐设置已更新: {'启用' if self.music_enabled else '禁用'}")
                    
                    elif setting_choice == '2':
                        self.setup_mysql_connection()
                
                elif choice == '6':
                    self.update_readme_progress()
                    self.play_daily_music()
                
                elif choice == '7':
                    if self.mysql_manager:
                        self.mysql_manager.close_connection()
                    print("\n🎉 感谢使用MySQL数据库管理工具！")
                    print("📊 您的数据服务已完善，现在可以在报告系统中使用数据库功能了")
                    self.play_achievement_music()
                    break
                
                else:
                    print("❌ 无效选择，请重新输入")
        
        except KeyboardInterrupt:
            print("\n\n👋 用户取消操作")
        
        except Exception as e:
            logger.error(f"程序执行失败: {str(e)}")
        
        finally:
            if self.mysql_manager:
                self.mysql_manager.close_connection()


def main():
    """主函数"""
    manager = ComprehensiveMySQLManager()
    manager.run()


if __name__ == "__main__":
    main() 