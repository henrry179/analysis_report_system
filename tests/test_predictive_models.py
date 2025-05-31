import pytest
import pandas as pd
import numpy as np
from src.main import AnalysisReportSystem

class TestPredictiveModels:
    """测试预测模型的所有边界条件"""

    def test_predictive_analysis_with_valid_data(self):
        """测试正常时间序列数据预测"""
        # 创建系统实例
        system = AnalysisReportSystem("dummy_input.csv", "dummy_output")
        
        # 模拟有效数据
        data = pd.DataFrame({
            'date': pd.date_range('2023-01-01', periods=100),
            'gmv': np.cumsum(np.random.rand(100) * 100)  # 模拟GMV增长曲线
        })
        
        result = system.perform_predictive_analysis(data)
        
        assert isinstance(result, dict)
        assert 'predictions' in result
        assert 'future_dates' in result
        assert len(result['predictions']) == 30
        assert len(result['future_dates']) == 30

    def test_predictive_analysis_with_insufficient_data(self):
        """测试数据不足（少于2条）"""
        system = AnalysisReportSystem("dummy_input.csv", "dummy_output")
        
        data = pd.DataFrame({
            'date': pd.date_range('2023-01-01', periods=1),
            'gmv': [100]
        })
        
        result = system.perform_predictive_analysis(data)
        
        # 数据不足时应返回空预测
        assert result['predictions'] == []
        assert result['future_dates'] == []

    def test_predictive_analysis_with_empty_data(self):
        """测试空数据输入"""
        system = AnalysisReportSystem("dummy_input.csv", "dummy_output")
        
        result = system.perform_predictive_analysis(pd.DataFrame())
        
        # 空数据应返回空预测
        assert result['predictions'] == []
        assert result['future_dates'] == []

    def test_send_alerts_functionality(self):
        """测试自动预警功能"""
        system = AnalysisReportSystem("dummy_input.csv", "dummy_output")
        
        # 模拟分析结果
        analysis_results = {
            'top_declining_categories': ['category1', 'category2'],
            'predictions': {
                'predictions': [-100, 50, 200],  # 包含负值
                'future_dates': ['2023-01-01', '2023-01-02', '2023-01-03']
            }
        }
        
        # 测试不会抛出异常
        try:
            system.send_alerts(analysis_results)
            assert True
        except Exception:
            pytest.fail("send_alerts() raised an unexpected exception")

    def test_send_alerts_with_no_issues(self):
        """测试无问题时的预警功能"""
        system = AnalysisReportSystem("dummy_input.csv", "dummy_output")
        
        # 模拟正常分析结果
        analysis_results = {
            'top_declining_categories': [],
            'predictions': {
                'predictions': [100, 150, 200],  # 全为正值
                'future_dates': ['2023-01-01', '2023-01-02', '2023-01-03']
            }
        }
        
        # 测试不会抛出异常
        try:
            system.send_alerts(analysis_results)
            assert True
        except Exception:
            pytest.fail("send_alerts() should not raise exception for normal data") 