import os
from pathlib import Path

def setup_directories():
    """创建必要的目录结构"""
    directories = [
        'data',
        'output/charts',
        'output/reports',
        'templates',
        'src/analysis',
        'src/visualization',
        'src/report'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"创建目录: {directory}")
        
    # 创建必要的__init__.py文件
    init_files = [
        'src/__init__.py',
        'src/analysis/__init__.py',
        'src/visualization/__init__.py',
        'src/report/__init__.py'
    ]
    
    for init_file in init_files:
        Path(init_file).touch()
        print(f"创建文件: {init_file}")

if __name__ == '__main__':
    setup_directories() 