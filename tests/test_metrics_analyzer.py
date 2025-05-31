import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from src.analysis.metrics_analyzer import MetricsAnalyzer, GMVMetrics, CategoryMetrics, RegionMetrics

@pytest.fixture
def sample_data():
    """创建测试数据"""
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
    
    return pd.DataFrame(data)

@pytest.fixture
def analyzer(sample_data):
    """创建分析器实例"""
    latest_date = sample_data['date'].max()
    previous_date = sample_data[sample_data['date'] < latest_date]['date'].max()
    
    current_data = sample_data[sample_data['date'] == latest_date]
    previous_data = sample_data[sample_data['date'] == previous_date]
    
    return MetricsAnalyzer(current_data, previous_data)

def test_calculate_gmv_metrics(analyzer):
    """测试GMV指标计算"""
    metrics = analyzer.calculate_gmv_metrics()
    
    # 验证返回的指标类型
    assert isinstance(metrics, dict)
    assert all(isinstance(v, GMVMetrics) for v in metrics.values())
    
    # 验证GMV指标
    assert metrics['gmv'].contribution == 100.0
    assert metrics['gmv'].current > 0
    assert metrics['gmv'].previous > 0
    
    # 验证其他指标
    for metric in ['dau', 'frequency', 'order_price', 'conversion_rate']:
        assert metrics[metric].current > 0
        assert metrics[metric].previous > 0

def test_calculate_category_metrics(analyzer):
    """测试品类指标计算"""
    metrics = analyzer.calculate_category_metrics()
    
    # 验证返回的指标类型
    assert isinstance(metrics, list)
    assert all(isinstance(m, CategoryMetrics) for m in metrics)
    
    # 验证每个品类的指标
    for metric in metrics:
        assert metric.current_price > 0
        assert metric.previous_price > 0
        assert 0 <= metric.current_share <= 100
        assert 0 <= metric.previous_share <= 100

def test_calculate_region_metrics(analyzer):
    """测试区域指标计算"""
    metrics = analyzer.calculate_region_metrics()
    
    # 验证返回的指标类型
    assert isinstance(metrics, list)
    assert all(isinstance(m, RegionMetrics) for m in metrics)
    
    # 验证每个区域的指标
    for metric in metrics:
        assert metric.current_price > 0
        assert metric.previous_price > 0
        assert metric.current_rate > 0
        assert metric.previous_rate > 0

def test_calculate_gini_coefficient(analyzer):
    """测试基尼系数计算"""
    # 创建测试数据
    data = pd.Series([1, 2, 3, 4, 5])
    gini = analyzer.calculate_gini_coefficient(data)
    
    # 验证基尼系数
    assert 0 <= gini <= 1
    assert gini > 0  # 对于非均匀分布的数据，基尼系数应该大于0

def test_identify_top_declining_categories(analyzer):
    """测试下降品类识别"""
    metrics = analyzer.calculate_category_metrics()
    declining = analyzer.identify_top_declining_categories(metrics)
    
    # 验证返回结果
    assert isinstance(declining, list)
    assert len(declining) <= 3  # 默认返回前3个
    assert all(isinstance(d, dict) for d in declining)
    assert all('name' in d and 'decline_rate' in d for d in declining)

def test_identify_top_declining_regions(analyzer):
    """测试下降区域识别"""
    metrics = analyzer.calculate_region_metrics()
    declining = analyzer.identify_top_declining_regions(metrics)
    
    # 验证返回结果
    assert isinstance(declining, list)
    assert len(declining) <= 3  # 默认返回前3个
    assert all(isinstance(d, dict) for d in declining)
    assert all('name' in d and 'decline_rate' in d for d in declining)

def test_generate_improvement_suggestions(analyzer):
    """测试改进建议生成"""
    metrics = analyzer.calculate_gmv_metrics()
    suggestions = analyzer.generate_improvement_suggestions(metrics)
    
    # 验证返回结果
    assert isinstance(suggestions, list)
    assert all(isinstance(s, str) for s in suggestions)

def test_analyze(analyzer):
    """测试完整分析流程"""
    results = analyzer.analyze()
    
    # 验证返回结果
    assert isinstance(results, dict)
    assert 'gmv_metrics' in results
    assert 'category_metrics' in results
    assert 'region_metrics' in results
    assert 'category_gini' in results
    assert 'region_gini' in results
    assert 'top_declining_categories' in results
    assert 'top_declining_regions' in results
    assert 'improvement_suggestions' in results 