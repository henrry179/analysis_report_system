import pytest
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from src.visualization.chart_generator import ChartGenerator
from statsmodels.tsa.arima.model import ARIMA
from analysis.predictive_models import arima_forecast

@pytest.fixture
def output_dir(tmp_path):
    """创建临时输出目录"""
    return str(tmp_path / 'charts')

@pytest.fixture
def chart_generator(output_dir):
    """创建图表生成器实例"""
    return ChartGenerator(output_dir)

@pytest.fixture
def sample_metrics():
    """创建测试指标数据"""
    return {
        'gmv': {
            'current': 10000,
            'previous': 9000,
            'change_rate': 11.11,
            'contribution': 100.0
        },
        'dau': {
            'current': 1000,
            'previous': 900,
            'change_rate': 11.11,
            'contribution': 50.0
        },
        'frequency': {
            'current': 2.5,
            'previous': 2.3,
            'change_rate': 8.7,
            'contribution': 30.0
        },
        'order_price': {
            'current': 100,
            'previous': 95,
            'change_rate': 5.26,
            'contribution': 15.0
        },
        'conversion_rate': {
            'current': 0.03,
            'previous': 0.028,
            'change_rate': 7.14,
            'contribution': 20.0
        }
    }

@pytest.fixture
def sample_category_metrics():
    """创建测试品类指标数据"""
    return [
        {
            'name': '品类A',
            'current_price': 100,
            'previous_price': 95,
            'change_rate': 5.26,
            'current_share': 40,
            'previous_share': 35,
            'structure_change': 14.29,
            'contribution': 2.1
        },
        {
            'name': '品类B',
            'current_price': 80,
            'previous_price': 85,
            'change_rate': -5.88,
            'current_share': 35,
            'previous_share': 40,
            'structure_change': -12.5,
            'contribution': -2.06
        },
        {
            'name': '品类C',
            'current_price': 120,
            'previous_price': 115,
            'change_rate': 4.35,
            'current_share': 25,
            'previous_share': 25,
            'structure_change': 0,
            'contribution': 1.09
        }
    ]

@pytest.fixture
def sample_region_metrics():
    """创建测试区域指标数据"""
    return [
        {
            'name': '区域1',
            'current_price': 100,
            'previous_price': 95,
            'change_value': 5,
            'change_rate': 5.26,
            'current_rate': 0.03,
            'previous_rate': 0.028
        },
        {
            'name': '区域2',
            'current_price': 90,
            'previous_price': 95,
            'change_value': -5,
            'change_rate': -5.26,
            'current_rate': 0.028,
            'previous_rate': 0.03
        },
        {
            'name': '区域3',
            'current_price': 110,
            'previous_price': 105,
            'change_value': 5,
            'change_rate': 4.76,
            'current_rate': 0.032,
            'previous_rate': 0.03
        }
    ]

@pytest.fixture
def sample_data():
    """创建测试数据"""
    dates = pd.date_range(start='2024-01-01', end='2024-01-10', freq='D')
    data = pd.DataFrame({
        'date': dates,
        'value': np.random.normal(100, 10, len(dates))
    })
    return data

def test_generate_gmv_contribution_chart(chart_generator, sample_metrics):
    """测试GMV贡献度分析图表生成"""
    output_path = chart_generator.generate_gmv_contribution_chart(sample_metrics)
    
    # 验证文件是否生成
    assert os.path.exists(output_path)
    assert output_path.endswith('gmv_contribution.png')

def test_generate_category_analysis_chart(chart_generator, sample_category_metrics):
    """测试品类分析图表生成"""
    output_path = chart_generator.generate_category_analysis_chart(sample_category_metrics)
    
    # 验证文件是否生成
    assert os.path.exists(output_path)
    assert output_path.endswith('category_analysis.png')

def test_generate_region_analysis_chart(chart_generator, sample_region_metrics):
    """测试区域分析图表生成"""
    output_path = chart_generator.generate_region_analysis_chart(sample_region_metrics)
    
    # 验证文件是否生成
    assert os.path.exists(output_path)
    assert output_path.endswith('region_analysis.png')

def test_generate_heatmap(chart_generator, sample_data):
    """测试热力图生成"""
    # 创建透视数据
    pivot_data = pd.DataFrame({
        'x': ['A', 'B', 'C'] * 3,
        'y': ['X', 'Y', 'Z'] * 3,
        'value': np.random.uniform(0, 100, 9)
    })
    
    output_path = chart_generator.generate_heatmap(
        pivot_data,
        x_col='x',
        y_col='y',
        value_col='value'
    )
    
    # 验证文件是否生成
    assert os.path.exists(output_path)
    assert output_path.endswith('heatmap_x_y_value.png')

def test_generate_trend_chart(chart_generator, sample_data):
    """测试趋势图生成"""
    output_path = chart_generator.generate_trend_chart(
        sample_data,
        date_col='date',
        value_col='value'
    )
    
    # 验证文件是否生成
    assert os.path.exists(output_path)
    assert output_path.endswith('trend_value.png')

def test_generate_all_charts(chart_generator, sample_metrics, sample_category_metrics, sample_region_metrics):
    """测试所有图表生成"""
    analysis_results = {
        'gmv_metrics': sample_metrics,
        'category_metrics': sample_category_metrics,
        'region_metrics': sample_region_metrics
    }
    
    chart_paths = chart_generator.generate_all_charts(analysis_results)
    
    # 验证返回的图表路径
    assert isinstance(chart_paths, dict)
    assert 'gmv_contribution' in chart_paths
    assert 'category_analysis' in chart_paths
    assert 'region_analysis' in chart_paths
    
    # 验证所有文件是否生成
    for path in chart_paths.values():
        assert os.path.exists(path)

def arima_forecast(data: pd.DataFrame, target_column: str = "gmv", steps: int = 30) -> dict:
    data = data.set_index('date').sort_index()
    model = ARIMA(data[target_column], order=(5,1,0))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=steps)
    future_dates = pd.date_range(
        start=data.index[-1] + pd.Timedelta(days=1),
        periods=steps
    )
    return {
        "predictions": forecast.tolist(),
        "future_dates": future_dates.strftime('%Y-%m-%d').tolist()
    } 