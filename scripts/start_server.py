#!/usr/bin/env python3
"""
分析报告系统服务器启动脚本 v4.0 Optimized
提供更好的错误处理和用户体验
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = str(Path(__file__).parent)
sys.path.insert(0, project_root)

def check_dependencies():
    """检查必要依赖"""
    missing_deps = []
    
    try:
        import fastapi
    except ImportError:
        missing_deps.append("fastapi")
    
    try:
        import uvicorn
    except ImportError:
        missing_deps.append("uvicorn")
    
    try:
        import pydantic
    except ImportError:
        missing_deps.append("pydantic")
    
    if missing_deps:
        print("❌ 缺少必要依赖包:")
        for dep in missing_deps:
            print(f"   - {dep}")
        print("\n💡 请运行以下命令安装依赖:")
        print("   pip install -r requirements.txt")
        return False
    
    return True


def main():
    """主启动函数"""
    print("🚀 分析报告系统启动器 v4.0 Optimized")
    print("=" * 60)
    
    # 检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    # 设置环境变量（如果需要）
    os.environ.setdefault("PYTHONPATH", project_root)
    
    try:
        # 导入并启动重构后的应用
        print("📦 正在加载应用模块...")
        from src.main import main as start_app
        
        print("✅ 模块加载完成")
        print("🌟 启动优化后的分析报告系统...")
        print("-" * 60)
        
        # 启动应用
        start_app()
        
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("💡 请确保您在正确的项目目录中运行此脚本")
        print("💡 请检查所有依赖是否正确安装")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 用户中断，正在关闭...")
        sys.exit(0)
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        print("💡 请检查系统配置和依赖安装")
        sys.exit(1)


if __name__ == "__main__":
    main() 