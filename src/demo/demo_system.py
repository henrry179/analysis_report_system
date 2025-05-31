#!/usr/bin/env python3
"""
业务分析报告自动化系统 - 功能演示
无需完整依赖，展示系统的基本运行能力
"""

import sys
import os
from datetime import datetime

# 添加src到路径
sys.path.insert(0, 'src')

def demo_banner():
    """显示演示横幅"""
    print("=" * 60)
    print("🚀 业务分析报告自动化系统 - 功能演示")
    print("=" * 60)
    print(f"📅 运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🐍 Python版本: {sys.version.split()[0]}")
    print()

def demo_basic_import():
    """演示基本导入功能"""
    print("📦 1. 测试核心模块导入...")
    try:
        from main import AnalysisReportSystem
        print("  ✅ 主程序模块导入成功")
        
        import web_interface
        print("  ✅ Web接口模块导入成功")
        
        return True
    except Exception as e:
        print(f"  ❌ 导入失败: {e}")
        return False

def demo_system_init():
    """演示系统初始化"""
    print("\n🔧 2. 测试系统初始化...")
    try:
        from main import AnalysisReportSystem
        
        # 创建测试数据文件
        test_file = "demo_data.csv"
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("date,category,region,gmv,dau,frequency,order_price,conversion_rate\n")
            f.write("2023-01-01,Electronics,北京,50000,1000,2.5,50.0,12.5\n")
            f.write("2023-01-02,Clothing,上海,45000,950,2.3,47.4,11.8\n")
        
        # 初始化系统
        system = AnalysisReportSystem(test_file, "demo_output")
        print("  ✅ 系统初始化成功")
        
        return system, test_file
    except Exception as e:
        print(f"  ❌ 初始化失败: {e}")
        return None, None

def demo_data_loading(system):
    """演示数据加载功能"""
    print("\n📊 3. 测试数据加载...")
    try:
        current_data, previous_data = system.load_data()
        print("  ✅ 数据加载成功")
        print(f"  📈 当前期数据: {type(current_data).__name__}")
        print(f"  📉 上期数据: {type(previous_data).__name__}")
        return current_data, previous_data
    except Exception as e:
        print(f"  ❌ 数据加载失败: {e}")
        return None, None

def demo_predictive_analysis(system, data):
    """演示预测分析功能"""
    print("\n🔮 4. 测试预测分析...")
    try:
        if data is not None:
            predictions = system.perform_predictive_analysis(data)
            print("  ✅ 预测分析完成")
            print(f"  📊 预测结果: {len(predictions.get('predictions', []))} 个数据点")
            print(f"  📅 未来日期: {len(predictions.get('future_dates', []))} 个日期")
        else:
            print("  ⚠️  数据不可用，跳过预测分析")
    except Exception as e:
        print(f"  ❌ 预测分析失败: {e}")

def demo_web_interface():
    """演示Web接口功能"""
    print("\n🌐 5. 测试Web接口...")
    try:
        import web_interface
        
        if hasattr(web_interface, 'FASTAPI_AVAILABLE') and web_interface.FASTAPI_AVAILABLE:
            print("  ✅ FastAPI 可用")
            print("  🚀 可以启动Web服务：python src/web_interface.py")
        else:
            print("  ⚠️  FastAPI 不可用，Web功能受限")
            print("  💡 安装提示：pip install fastapi uvicorn")
        
        if hasattr(web_interface, 'create_user'):
            result = web_interface.create_user("demo", "password", "user")
            if result:
                print("  ✅ 用户创建功能正常")
            else:
                print("  ⚠️  用户创建功能受限")
                
    except Exception as e:
        print(f"  ❌ Web接口测试失败: {e}")

def demo_cleanup(test_file):
    """清理演示文件"""
    try:
        if os.path.exists(test_file):
            os.remove(test_file)
        if os.path.exists("demo_output"):
            os.rmdir("demo_output")
        print("\n🧹 演示文件清理完成")
    except:
        pass

def main():
    """主演示函数"""
    demo_banner()
    
    # 步骤1：基本导入测试
    if not demo_basic_import():
        print("❌ 基本功能不可用，演示终止")
        return
    
    # 步骤2：系统初始化
    system, test_file = demo_system_init()
    if not system:
        print("❌ 系统初始化失败，演示终止")
        return
    
    # 步骤3：数据加载
    current_data, previous_data = demo_data_loading(system)
    
    # 步骤4：预测分析
    demo_predictive_analysis(system, current_data)
    
    # 步骤5：Web接口测试
    demo_web_interface()
    
    # 清理
    demo_cleanup(test_file)
    
    print("\n" + "=" * 60)
    print("🎉 系统演示完成！")
    print("📋 详细状态请查看: PROJECT_STATUS.md")
    print("📖 使用指南请查看: README.md")
    print("🔧 项目完整性检查: python project_check.py")
    print("=" * 60)

if __name__ == "__main__":
    main() 