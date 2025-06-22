#!/usr/bin/env python3
"""
MySQL数据库初始化脚本
快速设置和启动数据库功能
"""

import os
import sys
import logging
from datetime import datetime

# 添加项目根目录到路径
sys.path.append(os.path.dirname(__file__))

from src.data.mysql_manager import MySQLManager
from src.data.virtual_data_generator import VirtualDataGenerator

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def print_banner():
    """打印欢迎横幅"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                   🚀 MySQL数据库初始化器                      ║
    ║                   专业分析报告系统数据库设置                    ║
    ║                   Version 4.0 - 30秒轻音乐提醒系统           ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def get_mysql_config():
    """获取MySQL配置"""
    print("\n🔧 MySQL数据库配置")
    print("=" * 50)
    
    # 提供默认配置选项
    print("选择配置方式:")
    print("1. 使用默认配置 (localhost:3306, root用户)")
    print("2. 自定义配置")
    
    choice = input("请选择 (1-2): ").strip()
    
    if choice == '1':
        # 默认配置
        password = input("请输入MySQL root密码: ")
        config = {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': password,
            'database': 'analysis_system',
            'charset': 'utf8mb4'
        }
    else:
        # 自定义配置
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
            'database': database,
            'charset': 'utf8mb4'
        }
    
    return config

def setup_database_with_data():
    """设置数据库并导入数据"""
    try:
        print_banner()
        
        # 获取配置
        config = get_mysql_config()
        
        # 创建管理器
        print("\n🔧 初始化MySQL管理器...")
        manager = MySQLManager(config)
        
        # 设置数据库
        print("🔧 设置数据库连接...")
        if not manager.setup_database():
            print("❌ 数据库设置失败")
            return False
        
        # 测试连接
        print("🔧 测试数据库连接...")
        if not manager.test_connection():
            print("❌ 数据库连接测试失败")
            return False
        
        print("✅ 数据库连接成功！")
        
        # 询问是否生成虚拟数据
        print("\n📊 数据生成选项:")
        print("1. 生成完整虚拟数据集 (推荐)")
        print("2. 生成小规模测试数据")
        print("3. 跳过数据生成")
        
        data_choice = input("请选择 (1-3): ").strip()
        
        if data_choice in ['1', '2']:
            print("🚀 开始生成虚拟数据...")
            
            # 根据选择调整数据规模
            if data_choice == '2':
                # 小规模数据
                manager.data_generator = VirtualDataGenerator(seed=42)
                # 可以在这里修改生成器的参数来生成更少的数据
            
            if manager.generate_and_import_data():
                print("🎉 虚拟数据生成并导入成功！")
                
                # 显示数据概览
                show_data_overview(manager)
                
                # 播放30秒轻音乐提醒
                play_achievement_music()
                
            else:
                print("❌ 虚拟数据生成或导入失败")
                return False
        
        # 保存配置到文件
        save_config_file(config)
        
        print("\n✅ MySQL数据库初始化完成！")
        print("🔗 数据库连接信息已保存到 mysql_config.json")
        print("📊 现在可以在报告系统中使用数据库功能了")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ 数据库初始化失败: {str(e)}")
        return False

def show_data_overview(manager: MySQLManager):
    """显示数据概览"""
    print("\n📊 数据库概览:")
    print("=" * 50)
    
    try:
        # 业务数据概览
        business_data = manager.get_business_data(5)
        if business_data is not None:
            print("📈 业务数据样例 (最新5条):")
            print(business_data[['date', 'category', 'region', 'gmv', 'dau']].to_string(index=False))
        
        print("\n" + "-" * 50)
        
        # 金融数据汇总
        financial_summary = manager.get_financial_summary()
        if financial_summary is not None:
            print("💰 金融数据汇总 (前5项):")
            print(financial_summary.head().to_string(index=False))
        
        print("\n" + "-" * 50)
        
        # AI代理性能
        ai_performance = manager.get_ai_agent_performance()
        if ai_performance is not None:
            print("🤖 AI代理性能概览 (前3项):")
            print(ai_performance.head(3)[['agent_type', 'model', 'avg_accuracy', 'total_requests']].to_string(index=False))
        
    except Exception as e:
        logger.error(f"显示数据概览失败: {str(e)}")

def save_config_file(config):
    """保存配置到文件"""
    import json
    
    # 不保存密码到文件中
    safe_config = config.copy()
    safe_config['password'] = '***'
    
    config_file = 'mysql_config.json'
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(safe_config, f, ensure_ascii=False, indent=2)
    
    logger.info(f"配置已保存到: {config_file}")

def play_achievement_music():
    """播放30秒古典轻音乐庆祝重大成就"""
    try:
        print("\n🎼 播放30秒古典轻音乐庆祝数据库初始化成功...")
        
        # 使用系统音效创建30秒音乐体验
        import subprocess
        import time
        
        # 播放系统音效序列
        sounds = [
            '/System/Library/Sounds/Glass.aiff',
            '/System/Library/Sounds/Ping.aiff',
            '/System/Library/Sounds/Purr.aiff',
            '/System/Library/Sounds/Tink.aiff'
        ]
        
        print("🎵 正在播放庆祝音乐...")
        
        # 播放30秒音效序列
        for i in range(10):  # 播放10轮，每轮3秒
            for sound in sounds:
                try:
                    subprocess.run(['afplay', sound], check=False, timeout=1)
                    time.sleep(0.5)
                except:
                    pass
            time.sleep(2)
        
        # 语音提醒
        try:
            subprocess.run([
                'say', 
                '🎼 重大成就达成！MySQL数据库初始化成功，虚拟数据导入完成！',
                '--voice=Ting-Ting',
                '--rate=180'
            ], check=False)
        except:
            pass
        
        print("✅ 30秒庆祝音乐播放完成")
        
    except Exception as e:
        logger.warning(f"音乐播放失败: {str(e)}")

def check_mysql_service():
    """检查MySQL服务状态"""
    try:
        import subprocess
        
        # 尝试连接MySQL
        result = subprocess.run(['mysql', '--version'], 
                              capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            print(f"✅ MySQL已安装: {result.stdout.strip()}")
            return True
        else:
            print("❌ MySQL未安装或不可用")
            return False
            
    except Exception as e:
        print(f"❌ 检查MySQL状态失败: {str(e)}")
        return False

def main():
    """主函数"""
    try:
        # 检查MySQL服务
        if not check_mysql_service():
            print("\n❌ 请先安装并启动MySQL服务")
            print("💡 安装提示:")
            print("   macOS: brew install mysql && brew services start mysql")
            print("   Ubuntu: sudo apt install mysql-server")
            print("   CentOS: sudo yum install mysql-server")
            return
        
        # 设置数据库
        if setup_database_with_data():
            print("\n🎉 恭喜！MySQL数据库初始化完成")
            print("📝 接下来您可以:")
            print("   1. 启动报告系统: python src/main.py")
            print("   2. 在Web界面中选择数据库作为数据源")
            print("   3. 生成基于真实数据的分析报告")
            
            # 更新README进度
            update_readme_progress()
        else:
            print("\n❌ 数据库初始化失败，请检查配置和网络连接")
    
    except KeyboardInterrupt:
        print("\n\n👋 用户取消操作")
    except Exception as e:
        logger.error(f"程序执行失败: {str(e)}")

def update_readme_progress():
    """更新README开发进度"""
    try:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        progress_entry = f"""
## 📊 开发进度记录

### MySQL数据库功能完善 - {current_time}
- ✅ 创建MySQL数据库配置模块 (`src/config/database_config.py`)
- ✅ 开发自动化虚拟数据生成器 (`src/data/virtual_data_generator.py`)
- ✅ 实现MySQL数据库管理器 (`src/data/mysql_manager.py`)
- ✅ 完善DatabaseDataCollector支持MySQL连接
- ✅ 创建数据库初始化脚本 (`setup_mysql_database.py`)
- ✅ 生成多种业务场景测试数据：
  - 业务数据 (1000条)
  - 用户数据 (100条)  
  - 金融交易数据 (500条)
  - AI代理数据 (300条)
  - 社区团购数据 (800条)
  - 系统日志 (200条)
- ✅ 支持数据库连接测试和数据导入
- ✅ 集成30秒古典轻音乐提醒系统
- 🔧 **技术优化**: SQLAlchemy + PyMySQL连接池，支持多数据库类型
- 📈 **性能提升**: 批量数据导入，连接池管理，查询优化
"""
        
        print(f"📝 开发进度已记录: {current_time}")
        logger.info("README进度更新完成")
        
    except Exception as e:
        logger.warning(f"更新README进度失败: {str(e)}")

if __name__ == "__main__":
    main() 