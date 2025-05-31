import unittest
import pandas as pd
import numpy as np
import os
import json
from datetime import datetime
from src.core.report_generator import ReportGenerator

class TestReportGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = ReportGenerator()
        self.sample_data = pd.DataFrame({
            'numeric_col1': [1, 2, 3, 4, 5],
            'numeric_col2': [2, 4, 6, 8, 10],
            'categorical_col': ['A', 'B', 'A', 'C', 'B'],
            'date_col': pd.date_range(start='2023-01-01', periods=5)
        })
        self.analysis_results = {
            'descriptive': {
                'numeric_stats': {
                    'numeric_col1': {
                        'mean': 3.0,
                        'median': 3.0,
                        'std': 1.58
                    }
                }
            },
            'correlation': {
                'correlation_matrix': pd.DataFrame({
                    'numeric_col1': [1.0, 0.9],
                    'numeric_col2': [0.9, 1.0]
                })
            }
        }
        
    def test_generate_report(self):
        # 测试报告生成
        report_data = {
            'title': '测试报告',
            'generated_at': datetime.now().isoformat(),
            'data': self.sample_data.to_dict()
        }
        
        # 测试HTML格式
        output_path = self.generator.generate_report(
            report_data,
            'visualization',
            'html'
        )
        self.assertTrue(os.path.exists(output_path))
        self.assertTrue(output_path.endswith('.html'))
        
        # 测试PDF格式
        output_path = self.generator.generate_report(
            report_data,
            'visualization',
            'pdf'
        )
        self.assertTrue(os.path.exists(output_path))
        self.assertTrue(output_path.endswith('.pdf'))
        
        # 测试Markdown格式
        output_path = self.generator.generate_report(
            report_data,
            'visualization',
            'md'
        )
        self.assertTrue(os.path.exists(output_path))
        self.assertTrue(output_path.endswith('.md'))
        
        # 测试JSON格式
        output_path = self.generator.generate_report(
            report_data,
            'visualization',
            'json'
        )
        self.assertTrue(os.path.exists(output_path))
        self.assertTrue(output_path.endswith('.json'))
        
    def test_create_executive_summary(self):
        # 测试执行摘要生成
        summary = self.generator.create_executive_summary({
            'analysis_results': self.analysis_results
        })
        
        # 检查摘要结构
        self.assertIn('title', summary)
        self.assertIn('generated_at', summary)
        self.assertIn('key_metrics', summary)
        self.assertIn('findings', summary)
        self.assertIn('recommendations', summary)
        
        # 验证关键指标
        self.assertIn('numeric_col1', summary['key_metrics'])
        self.assertEqual(summary['key_metrics']['numeric_col1']['mean'], 3.0)
        
    def test_create_visualization_report(self):
        # 测试可视化报告生成
        output_path = self.generator.create_visualization_report(
            self.sample_data,
            output_format='html'
        )
        
        # 验证输出文件
        self.assertTrue(os.path.exists(output_path))
        self.assertTrue(output_path.endswith('.html'))
        
        # 验证报告内容
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn('数据可视化报告', content)
            self.assertIn('数据概览', content)
            
    def test_create_analysis_report(self):
        # 测试分析报告生成
        output_path = self.generator.create_analysis_report(
            self.analysis_results,
            output_format='html'
        )
        
        # 验证输出文件
        self.assertTrue(os.path.exists(output_path))
        self.assertTrue(output_path.endswith('.html'))
        
        # 验证报告内容
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn('数据分析报告', content)
            self.assertIn('执行摘要', content)
            
    def test_export_to_markdown(self):
        # 测试Markdown导出
        html_content = '<h1>测试</h1><p>内容</p>'
        output_path = 'tests/output/test.md'
        
        self.generator._export_to_markdown(html_content, output_path)
        
        # 验证输出文件
        self.assertTrue(os.path.exists(output_path))
        self.assertTrue(output_path.endswith('.md'))
        
        # 验证内容
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn('# 测试', content)
            self.assertIn('内容', content)
            
    def test_export_to_json(self):
        # 测试JSON导出
        data = {'test': 'data'}
        output_path = 'tests/output/test.json'
        
        self.generator._export_to_json(data, output_path)
        
        # 验证输出文件
        self.assertTrue(os.path.exists(output_path))
        self.assertTrue(output_path.endswith('.json'))
        
        # 验证内容
        with open(output_path, 'r', encoding='utf-8') as f:
            content = json.load(f)
            self.assertEqual(content, data)
            
    def test_invalid_output_format(self):
        # 测试无效输出格式
        report_data = {
            'title': '测试报告',
            'generated_at': datetime.now().isoformat()
        }
        
        with self.assertRaises(ValueError):
            self.generator.generate_report(
                report_data,
                'visualization',
                'invalid_format'
            )
            
    def test_missing_template(self):
        # 测试缺失模板
        report_data = {
            'title': '测试报告',
            'generated_at': datetime.now().isoformat()
        }
        
        with self.assertRaises(Exception):
            self.generator.generate_report(
                report_data,
                'non_existent_template',
                'html'
            )
            
    def test_empty_data(self):
        # 测试空数据
        empty_df = pd.DataFrame()
        
        with self.assertRaises(ValueError):
            self.generator.create_visualization_report(empty_df)
            
    def tearDown(self):
        # 清理测试文件
        test_files = [
            'tests/output/test.md',
            'tests/output/test.json',
            'tests/output/report_*.html',
            'tests/output/report_*.pdf',
            'tests/output/report_*.md',
            'tests/output/report_*.json'
        ]
        
        for pattern in test_files:
            for file in os.listdir('tests/output'):
                if file.startswith('report_') or file in ['test.md', 'test.json']:
                    os.remove(os.path.join('tests/output', file))
                    
if __name__ == '__main__':
    unittest.main() 