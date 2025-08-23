import pytest
import os
import sys

def run_tests():
    """运行所有测试用例"""
    # 获取测试目录路径
    test_dir = os.path.join(os.path.dirname(__file__), 'tests')
    
    # 运行测试
    pytest.main([
        test_dir,
        '-v',  # 详细输出
        '--tb=short',  # 简化的错误回溯
        '--cov=src',  # 生成覆盖率报告
        '--cov-report=term-missing',  # 显示未覆盖的代码行
        '--cov-report=html'  # 生成HTML格式的覆盖率报告
    ])

if __name__ == '__main__':
    run_tests() 