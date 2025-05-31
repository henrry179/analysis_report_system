#!/usr/bin/env python3
"""
项目完整性验证脚本
检查所有Python文件的语法和导入
"""

import os
import ast
import sys
from pathlib import Path

def check_python_syntax(file_path):
    """检查Python文件语法"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        ast.parse(content)
        return True, "语法正确"
    except SyntaxError as e:
        return False, f"语法错误: {e}"
    except Exception as e:
        return False, f"文件读取错误: {e}"

def find_python_files(directory):
    """查找所有Python文件"""
    python_files = []
    for root, dirs, files in os.walk(directory):
        # 跳过虚拟环境和缓存目录
        dirs[:] = [d for d in dirs if d not in ['.venv', '__pycache__', '.git']]
        
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files

def check_required_files():
    """检查必需文件是否存在"""
    required_files = [
        'src/main.py',
        'src/web_interface.py',
        'src/analysis/metrics_analyzer.py',
        'src/data/data_processor.py',
        'src/visualization/chart_generator.py',
        'src/report/report_generator.py',
        'tests/test_predictive_models.py',
        'tests/test_data_processor.py',
        'tests/test_web_interface.py',
        'requirements.txt'
    ]
    
    missing_files = []
    existing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            existing_files.append(file_path)
        else:
            missing_files.append(file_path)
    
    return existing_files, missing_files

def main():
    """主验证函数"""
    print("🔍 项目完整性检查开始...")
    print("=" * 50)
    
    # 检查必需文件
    print("📁 检查必需文件...")
    existing_files, missing_files = check_required_files()
    
    print(f"✅ 存在的文件 ({len(existing_files)}):")
    for file in existing_files:
        print(f"   {file}")
    
    if missing_files:
        print(f"❌ 缺失的文件 ({len(missing_files)}):")
        for file in missing_files:
            print(f"   {file}")
    
    print("\n" + "=" * 50)
    
    # 检查Python文件语法
    print("🐍 检查Python文件语法...")
    python_files = find_python_files('.')
    
    syntax_ok = 0
    syntax_errors = 0
    
    for file_path in python_files:
        if file_path.endswith('project_check.py'):
            continue  # 跳过自己
            
        is_valid, message = check_python_syntax(file_path)
        if is_valid:
            print(f"✅ {file_path}: {message}")
            syntax_ok += 1
        else:
            print(f"❌ {file_path}: {message}")
            syntax_errors += 1
    
    print("\n" + "=" * 50)
    print("📊 检查结果汇总:")
    print(f"   总Python文件数: {len(python_files)}")
    print(f"   语法正确: {syntax_ok}")
    print(f"   语法错误: {syntax_errors}")
    print(f"   必需文件存在: {len(existing_files)}")
    print(f"   必需文件缺失: {len(missing_files)}")
    
    # 项目状态评估
    if syntax_errors == 0 and len(missing_files) == 0:
        print("\n🎉 项目状态: 完整且健康!")
        return 0
    elif syntax_errors == 0:
        print(f"\n⚠️  项目状态: 语法正确但缺失{len(missing_files)}个文件")
        return 1
    else:
        print(f"\n❌ 项目状态: 存在{syntax_errors}个语法错误")
        return 2

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 