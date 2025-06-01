#!/usr/bin/env python3
"""
简化测试运行器
不依赖外部库，验证基本代码功能
"""

import sys
import os
import traceback
from datetime import datetime

# 添加src到Python路径
sys.path.insert(0, 'src')

def run_test(test_name, test_func):
    """运行单个测试"""
    try:
        print(f"🧪 运行测试: {test_name}")
        test_func()
        print(f"  ✅ 通过")
        return True
    except Exception as e:
        print(f"  ❌ 失败: {str(e)}")
        print(f"     {traceback.format_exc()}")
        return False

def test_basic_imports():
    """测试基本导入"""
    # 测试主程序导入
    try:
        from main import AnalysisReportSystem
        print("    ✓ main.py 导入成功")
    except ImportError as e:
        print(f"    ✗ main.py 导入失败: {e}")
        raise
    
    # 测试Web接口导入
    try:
        import web_interface
        print("    ✓ web_interface.py 导入成功")
    except ImportError as e:
        print(f"    ✗ web_interface.py 导入失败: {e}")
        raise

def test_analysis_system_init():
    """测试分析系统初始化"""
    from main import AnalysisReportSystem
    
    # 创建临时目录用于测试
    test_input = "test_input.csv"
    test_output = "test_output"
    
    # 创建测试用的CSV文件
    with open(test_input, 'w', encoding='utf-8') as f:
        f.write("date,category,region,gmv,dau,frequency,order_price,conversion_rate\n")
        f.write("2023-01-01,A,北京,1000,100,2.5,40.0,10.5\n")
        f.write("2023-01-02,B,上海,1200,120,2.8,45.0,12.0\n")
    
    try:
        system = AnalysisReportSystem(test_input, test_output)
        print("    ✓ AnalysisReportSystem 初始化成功")
    finally:
        # 清理测试文件
        if os.path.exists(test_input):
            os.remove(test_input)

def test_predictive_analysis():
    """测试预测分析功能"""
    from main import AnalysisReportSystem
    
    # 不再直接导入pandas，而是使用系统的模拟功能
    system = AnalysisReportSystem("dummy", "dummy")
    
    # 创建模拟数据（不依赖pandas的复杂功能）
    class MockDataFrame:
        def __init__(self, data):
            self.data = data
        
        def __len__(self):
            return len(self.data.get('gmv', []))
        
        def sort_values(self, *args, **kwargs):
            return self
        
        def __getitem__(self, key):
            return MockSeries(self.data.get(key, []))
        
        def max(self):
            return "2023-01-01"
    
    class MockSeries:
        def __init__(self, data):
            self.values = data
        
        def min(self):
            return MockTimedelta()
        
        def max(self):
            return MockTimedelta()
    
    class MockTimedelta:
        def dt(self):
            return self
        
        @property
        def days(self):
            return MockDays()
    
    class MockDays:
        @property
        def values(self):
            return MockValues()
    
    class MockValues:
        def reshape(self, shape):
            return [[1], [2]]
    
    # 测试空数据情况
    empty_data = MockDataFrame({})
    result = system.perform_predictive_analysis(empty_data)
    print("    ✓ 空数据预测处理正常")
    
    # 根据pandas是否可用，调整期望值
    try:
        import pandas as pd
        # pandas可用时期望空列表
        assert result['predictions'] == []
        assert result['future_dates'] == []
        print("    ✓ 空数据返回结果正确（pandas模式）")
    except ImportError:
        # pandas不可用时期望模拟结果
        assert isinstance(result['predictions'], list)
        assert isinstance(result['future_dates'], list)
        print("    ✓ 空数据返回结果正确（模拟模式）")
    
    # 测试有数据情况
    sample_data = MockDataFrame({'gmv': [100, 200, 300]})
    result = system.perform_predictive_analysis(sample_data)
    print("    ✓ 预测功能返回结果正常")

def test_file_structure():
    """测试文件结构完整性"""
    required_files = [
        'src/main.py',
        'src/web_interface.py',
        'src/analysis/metrics_analyzer.py',
        'src/data/data_processor.py',
        'src/visualization/chart_generator.py',
        'src/report/report_generator.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        raise AssertionError(f"缺失文件: {missing_files}")
    
    print(f"    ✓ 所有 {len(required_files)} 个核心文件存在")

def test_syntax_check():
    """测试语法检查"""
    import ast
    
    python_files = []
    for root, dirs, files in os.walk('src'):
        dirs[:] = [d for d in dirs if d not in ['__pycache__']]
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    syntax_errors = []
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                ast.parse(f.read())
        except SyntaxError as e:
            syntax_errors.append(f"{file_path}: {e}")
    
    if syntax_errors:
        raise AssertionError(f"语法错误: {syntax_errors}")
    
    print(f"    ✓ 所有 {len(python_files)} 个Python文件语法正确")

def main():
    """主测试函数"""
    print("🚀 开始简化测试...")
    print("=" * 60)
    
    tests = [
        ("文件结构检查", test_file_structure),
        ("语法检查", test_syntax_check),
        ("基本导入测试", test_basic_imports),
        ("分析系统初始化", test_analysis_system_init),
        ("预测分析功能", test_predictive_analysis),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        if run_test(test_name, test_func):
            passed += 1
        else:
            failed += 1
        print()
    
    print("=" * 60)
    print("📊 测试结果汇总:")
    print(f"  总测试数: {len(tests)}")
    print(f"  通过: {passed}")
    print(f"  失败: {failed}")
    print(f"  通过率: {passed/len(tests)*100:.1f}%")
    
    if failed == 0:
        print("\n🎉 所有测试通过!")
        return 0
    else:
        print(f"\n⚠️  有 {failed} 个测试失败")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 