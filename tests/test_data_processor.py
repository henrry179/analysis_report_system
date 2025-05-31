import unittest
import pandas as pd
import numpy as np
from src.core.data_processor import DataProcessor

class TestDataProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = DataProcessor()
        self.sample_data = pd.DataFrame({
            'numeric_col': [1, 2, 3, np.nan, 5],
            'categorical_col': ['A', 'B', 'A', 'C', 'B'],
            'date_col': pd.date_range(start='2023-01-01', periods=5)
        })
        
    def test_import_data(self):
        # 测试CSV导入
        df = self.processor.import_data('tests/data/sample.csv', 'csv')
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)
        
        # 测试Excel导入
        df = self.processor.import_data('tests/data/sample.xlsx', 'xlsx')
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)
        
        # 测试JSON导入
        df = self.processor.import_data('tests/data/sample.json', 'json')
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)
        
    def test_preprocess_data(self):
        # 测试预处理
        processed_df = self.processor.preprocess_data(self.sample_data)
        
        # 检查缺失值处理
        self.assertFalse(processed_df.isnull().any().any())
        
        # 检查数据类型转换
        self.assertTrue(pd.api.types.is_numeric_dtype(processed_df['numeric_col']))
        self.assertTrue(pd.api.types.is_categorical_dtype(processed_df['categorical_col']))
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(processed_df['date_col']))
        
    def test_validate_data(self):
        # 测试数据验证
        validation_results = self.processor.validate_data(self.sample_data)
        
        # 检查验证结果
        self.assertIn('total_rows', validation_results)
        self.assertIn('total_columns', validation_results)
        self.assertIn('missing_values', validation_results)
        self.assertIn('data_types', validation_results)
        self.assertIn('duplicates', validation_results)
        
        # 验证具体值
        self.assertEqual(validation_results['total_rows'], 5)
        self.assertEqual(validation_results['total_columns'], 3)
        self.assertEqual(validation_results['missing_values']['numeric_col'], 1)
        
    def test_export_data(self):
        # 测试数据导出
        output_path = 'tests/output/test_export.csv'
        self.processor.export_data(self.sample_data, output_path, 'csv')
        
        # 验证导出文件
        exported_df = pd.read_csv(output_path)
        self.assertTrue(exported_df.equals(self.sample_data))
        
    def test_handle_missing_values(self):
        # 测试缺失值处理
        df_with_missing = self.sample_data.copy()
        df_with_missing.loc[0, 'numeric_col'] = np.nan
        
        processed_df = self.processor._handle_missing_values(df_with_missing)
        self.assertFalse(processed_df.isnull().any().any())
        
    def test_handle_outliers(self):
        # 测试异常值处理
        df_with_outliers = self.sample_data.copy()
        df_with_outliers.loc[0, 'numeric_col'] = 1000  # 添加异常值
        
        processed_df = self.processor._handle_outliers(df_with_outliers)
        self.assertTrue(processed_df['numeric_col'].max() < 1000)
        
    def test_convert_data_types(self):
        # 测试数据类型转换
        df = self.sample_data.copy()
        df['numeric_col'] = df['numeric_col'].astype(str)
        
        processed_df = self.processor._convert_data_types(df)
        self.assertTrue(pd.api.types.is_numeric_dtype(processed_df['numeric_col']))
        
    def test_normalize_data(self):
        # 测试数据标准化
        df = self.sample_data.copy()
        processed_df = self.processor._normalize_data(df)
        
        # 检查标准化后的数据
        self.assertTrue(processed_df['numeric_col'].mean() < 1)
        self.assertTrue(processed_df['numeric_col'].std() < 1)
        
if __name__ == '__main__':
    unittest.main() 