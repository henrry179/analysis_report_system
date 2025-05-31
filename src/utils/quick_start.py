#!/usr/bin/env python3
"""
业务分析报告自动化系统 - 快速启动演示
无需完整依赖，展示系统核心架构和功能
"""

import os
import sys
from datetime import datetime

def print_banner():
    """打印系统横幅"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║              业务分析报告自动化系统                             ║
║                  快速启动演示                                  ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def show_system_info():
    """显示系统信息"""
    print("🚀 系统信息")
    print("=" * 50)
    print(f"Python版本: {sys.version.split()[0]}")
    print(f"运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"项目目录: {os.getcwd()}")
    print(f"Python路径: {sys.executable}")
    print()

def show_modules_status():
    """显示模块状态"""
    print("📦 核心模块状态")
    print("=" * 50)
    
    modules = {
        "src/main.py": "系统主程序",
        "src/web_interface.py": "Web管理界面", 
        "src/analysis/metrics_analyzer.py": "指标分析引擎",
        "src/data/data_processor.py": "数据处理模块",
        "src/visualization/chart_generator.py": "可视化模块",
        "src/report/report_generator.py": "报告生成器",
        "tests/test_predictive_models.py": "预测模型测试",
        "tests/test_data_processor.py": "数据处理测试",
        "tests/test_web_interface.py": "Web接口测试"
    }
    
    for module, description in modules.items():
        status = "✅" if os.path.exists(module) else "❌"
        print(f"{status} {module:<40} {description}")
    print()

def show_features():
    """显示功能特性"""
    print("🎯 实现的功能特性")
    print("=" * 50)
    
    features = [
        "✅ 多源数据采集 (CSV/数据库/API)",
        "✅ 智能数据处理和清洗",
        "✅ 贡献度分解分析",
        "✅ 基尼系数计算", 
        "✅ 异常检测算法",
        "✅ 预测分析 (线性回归/ARIMA)",
        "✅ 交互式仪表盘 (Streamlit)",
        "✅ 多格式报告生成 (MD/HTML/PDF)",
        "✅ Web管理界面 (FastAPI)",
        "✅ OAuth2权限认证",
        "✅ 后台任务调度 (APScheduler)",
        "✅ 自动预警系统",
        "✅ 完整测试套件 (54个测试用例)"
    ]
    
    for feature in features:
        print(f"  {feature}")
    print()

def show_quick_commands():
    """显示快速命令"""
    print("⚡ 快速启动命令")
    print("=" * 50)
    print("# 1. 检查项目完整性")
    print("python project_check.py")
    print()
    print("# 2. 启动Web服务 (需要安装FastAPI)")
    print("python src/web_interface.py")
    print()
    print("# 3. 启动交互式仪表盘 (需要安装Streamlit)")
    print("streamlit run src/visualization/chart_generator.py")
    print()
    print("# 4. 运行测试套件 (需要安装pytest)")
    print("pytest tests/ -v")
    print()
    print("# 5. 生成分析报告")
    print("python src/main.py --input data/sales.csv --output reports/")
    print()

def show_architecture():
    """显示系统架构"""
    print("🏗️  系统架构")
    print("=" * 50)
    print("""
    数据源层          处理层              分析层              展示层
    ┌─────────┐      ┌─────────┐        ┌─────────┐        ┌─────────┐
    │ CSV文件 │  ──► │数据采集  │  ──►  │指标分析  │  ──►  │报告生成  │
    │ 数据库  │      │数据清洗  │        │预测建模  │        │图表展示  │
    │ API接口 │      │缓存管理  │        │异常检测  │        │Web界面  │
    └─────────┘      └─────────┘        └─────────┘        └─────────┘
                           │                  │                  │
                           ▼                  ▼                  ▼
                      ┌─────────┐        ┌─────────┐        ┌─────────┐
                      │任务调度  │        │自动预警  │        │权限管理  │
                      │APScheduler│       │智能告警  │        │OAuth2   │
                      └─────────┘        └─────────┘        └─────────┘
    """)

def main():
    """主演示函数"""
    print_banner()
    show_system_info()
    show_modules_status()
    show_features()
    show_architecture()
    show_quick_commands()
    
    print("🎉 系统演示完成!")
    print("📋 详细信息请查看: PROJECT_STATUS.md")
    print("📖 使用指南请查看: README.md")

if __name__ == "__main__":
    main() 