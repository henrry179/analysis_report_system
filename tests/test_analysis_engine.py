import unittest
import pandas as pd
import numpy as np
from src.core.analysis_engine import AnalysisEngine

class TestAnalysisEngine(unittest.TestCase):
    def setUp(self):
        self.engine = AnalysisEngine()
        self.sample_data = pd.DataFrame({
            'numeric_col1': [1, 2, 3, 4, 5],
            'numeric_col2': [2, 4, 6, 8, 10],
            'categorical_col': ['A', 'B', 'A', 'C', 'B'],
            'date_col': pd.date_range(start='2023-01-01', periods=5)
        })
        
    def test_descriptive_analysis(self):
        # 测试描述性统计
        results = self.engine._descriptive_analysis(self.sample_data)
        
        # 检查结果结构
        self.assertIn('numeric_stats', results)
        self.assertIn('categorical_stats', results)
        
        # 检查数值型统计
        numeric_stats = results['numeric_stats']
        self.assertIn('numeric_col1', numeric_stats)
        self.assertIn('numeric_col2', numeric_stats)
        
        # 验证具体统计值
        col1_stats = numeric_stats['numeric_col1']
        self.assertEqual(col1_stats['mean'], 3.0)
        self.assertEqual(col1_stats['median'], 3.0)
        self.assertEqual(col1_stats['std'], 1.5811388300841898)
        
    def test_correlation_analysis(self):
        # 测试相关性分析
        results = self.engine._correlation_analysis(self.sample_data)
        
        # 检查结果结构
        self.assertIn('correlation_matrix', results)
        self.assertIn('strong_correlations', results)
        
        # 验证相关性矩阵
        corr_matrix = results['correlation_matrix']
        self.assertEqual(corr_matrix.shape, (2, 2))  # 只有两个数值列
        
        # 验证强相关性
        strong_corr = results['strong_correlations']
        self.assertTrue(len(strong_corr) > 0)  # 应该有强相关性
        
    def test_trend_analysis(self):
        # 测试趋势分析
        results = self.engine._trend_analysis(self.sample_data)
        
        # 检查结果结构
        self.assertIn('trend_analysis', results)
        self.assertIn('moving_averages', results)
        self.assertIn('growth_rates', results)
        
        # 验证趋势分析
        trend_analysis = results['trend_analysis']
        self.assertIn('numeric_col1', trend_analysis)
        self.assertIn('numeric_col2', trend_analysis)
        
        # 验证移动平均
        moving_avgs = results['moving_averages']
        self.assertIn('numeric_col1', moving_avgs)
        
    def test_forecast_analysis(self):
        # 测试预测分析
        results = self.engine._forecast_analysis(self.sample_data)
        
        # 检查结果结构
        self.assertIn('forecast_analysis', results)
        self.assertIn('model_metrics', results)
        
        # 验证预测结果
        forecast_analysis = results['forecast_analysis']
        self.assertIn('numeric_col1', forecast_analysis)
        self.assertIn('numeric_col2', forecast_analysis)
        
        # 验证模型指标
        model_metrics = results['model_metrics']
        self.assertIn('r2_score', model_metrics)
        self.assertIn('rmse', model_metrics)
        
    def test_segment_customers(self):
        # 测试客户分群
        results = self.engine.segment_customers(self.sample_data, n_clusters=2)
        
        # 检查结果结构
        self.assertIn('cluster_assignments', results)
        self.assertIn('cluster_stats', results)
        
        # 验证分群结果
        cluster_assignments = results['cluster_assignments']
        self.assertEqual(len(cluster_assignments), len(self.sample_data))
        
        # 验证分群统计
        cluster_stats = results['cluster_stats']
        self.assertEqual(len(cluster_stats), 2)  # 两个群组
        
    def test_analyze_data(self):
        # 测试主分析函数
        results = self.engine.analyze_data(self.sample_data, 'descriptive')
        
        # 检查结果结构
        self.assertIn('descriptive', results)
        
        # 测试不同类型分析
        results = self.engine.analyze_data(self.sample_data, 'correlation')
        self.assertIn('correlation', results)
        
        results = self.engine.analyze_data(self.sample_data, 'trend')
        self.assertIn('trend', results)
        
        results = self.engine.analyze_data(self.sample_data, 'forecast')
        self.assertIn('forecast', results)
        
    def test_invalid_analysis_type(self):
        # 测试无效分析类型
        with self.assertRaises(ValueError):
            self.engine.analyze_data(self.sample_data, 'invalid_type')
            
    def test_empty_dataframe(self):
        # 测试空数据框
        empty_df = pd.DataFrame()
        with self.assertRaises(ValueError):
            self.engine.analyze_data(empty_df, 'descriptive')
            
    def test_single_column_dataframe(self):
        # 测试单列数据框
        single_col_df = pd.DataFrame({'col': [1, 2, 3]})
        results = self.engine.analyze_data(single_col_df, 'descriptive')
        self.assertIn('descriptive', results)
        
if __name__ == '__main__':
    unittest.main() 