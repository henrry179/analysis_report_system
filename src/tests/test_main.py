import pytest
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from src.main import AnalysisReportSystem

@pytest.fixture
def sample_data(tmp_path):
    """创建测试数据文件"""
    # 创建日期
    dates = [
        (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),  # 上周
        datetime.now().strftime('%Y-%m-%d')  # 当前
    ]
    
    # 创建品类
    categories = ['品类A', '品类B', '品类C']
    
    # 创建区域
    regions = ['区域1', '区域2', '区域3']
    
    # 创建数据
    data = []
    for date in dates:
        for category in categories:
            for region in regions:
                data.append({
                    'date': date,
                    'category': category,
                    'region': region,
                    'gmv': np.random.uniform(1000, 5000),
                    'dau': np.random.randint(100, 1000),
                    'frequency': np.random.uniform(1.5, 3.0),
                    'order_price': np.random.uniform(100, 500),
                    'conversion_rate': np.random.uniform(0.01, 0.05)
                })
    
    # 创建数据文件
    input_file = tmp_path / 'input.csv'
    pd.DataFrame(data).to_csv(input_file, index=False)
    
    return str(input_file)

@pytest.fixture
def output_dir(tmp_path):
    """创建输出目录"""
    return str(tmp_path / 'output')

@pytest.fixture
def system(sample_data, output_dir):
    """创建系统实例"""
    return AnalysisReportSystem(sample_data, output_dir)

def test_load_data(system):
    """测试数据加载"""
    current_data, previous_data = system.load_data()
    
    # 验证数据类型
    assert isinstance(current_data, pd.DataFrame)
    assert isinstance(previous_data, pd.DataFrame)
    
    # 验证数据列
    required_columns = ['date', 'category', 'region', 'gmv', 'dau', 'frequency', 
                       'order_price', 'conversion_rate']
    assert all(col in current_data.columns for col in required_columns)
    assert all(col in previous_data.columns for col in required_columns)
    
    # 验证数据不为空
    assert not current_data.empty
    assert not previous_data.empty

def test_generate_report(system):
    """测试报告生成"""
    report_date = datetime.now().strftime('%Y-%m-%d')
    output_paths = system.generate_report(report_date)
    
    # 验证返回结果
    assert isinstance(output_paths, dict)
    assert 'charts' in output_paths
    assert 'reports' in output_paths
    
    # 验证图表文件
    charts = output_paths['charts']
    assert isinstance(charts, dict)
    assert 'gmv_contribution' in charts
    assert 'category_analysis' in charts
    assert 'region_analysis' in charts
    
    # 验证报告文件
    reports = output_paths['reports']
    assert isinstance(reports, dict)
    assert 'markdown' in reports
    assert 'html' in reports
    assert 'pdf' in reports
    
    # 验证文件是否生成
    for path in charts.values():
        assert os.path.exists(path)
    for path in reports.values():
        assert os.path.exists(path)

def test_generate_report_without_date(system):
    """测试无日期参数的报告生成"""
    output_paths = system.generate_report()
    
    # 验证返回结果
    assert isinstance(output_paths, dict)
    assert 'charts' in output_paths
    assert 'reports' in output_paths
    
    # 验证文件是否生成
    for path in output_paths['charts'].values():
        assert os.path.exists(path)
    for path in output_paths['reports'].values():
        assert os.path.exists(path)

def test_invalid_input_file():
    """测试无效输入文件"""
    with pytest.raises(FileNotFoundError):
        AnalysisReportSystem('nonexistent.csv', 'output')

def test_invalid_output_dir():
    """测试无效输出目录"""
    with pytest.raises(OSError):
        AnalysisReportSystem('input.csv', '/nonexistent/dir')

def test_empty_data_file(tmp_path):
    """测试空数据文件"""
    # 创建空文件
    input_file = tmp_path / 'empty.csv'
    input_file.touch()
    
    system = AnalysisReportSystem(str(input_file), str(tmp_path / 'output'))
    
    with pytest.raises(ValueError):
        system.load_data()

def test_invalid_data_format(tmp_path):
    """测试无效数据格式"""
    # 创建格式错误的文件
    input_file = tmp_path / 'invalid.csv'
    with open(input_file, 'w') as f:
        f.write('invalid,data,format\n')
    
    system = AnalysisReportSystem(str(input_file), str(tmp_path / 'output'))
    
    with pytest.raises(pd.errors.EmptyDataError):
        system.load_data() 