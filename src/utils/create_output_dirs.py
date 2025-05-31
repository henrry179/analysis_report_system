import os
from pathlib import Path

def create_output_directories():
    """创建输出目录结构"""
    # 获取项目根目录
    root_dir = Path(__file__).parent
    
    # 创建输出目录
    output_dir = root_dir / 'output'
    charts_dir = output_dir / 'charts'
    reports_dir = output_dir / 'reports'
    
    # 创建目录
    output_dir.mkdir(exist_ok=True)
    charts_dir.mkdir(exist_ok=True)
    reports_dir.mkdir(exist_ok=True)
    
    print(f"Created output directory: {output_dir}")
    print(f"Created charts directory: {charts_dir}")
    print(f"Created reports directory: {reports_dir}")

if __name__ == '__main__':
    create_output_directories() 