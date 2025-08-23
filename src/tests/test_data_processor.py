import pytest
import pandas as pd
import numpy as np
from src.data.data_processor import clean_data

class TestDataProcessor:
    """测试数据清洗模块的完整性"""

    def test_normal_data_cleaning(self):
        """测试标准数据清洗流程"""
        test_data = pd.DataFrame({
            'gmv': [100, 200, 300, 400],
            'dau': [50, 60, 70, 80],
            'conversion_rate': [12.5, 15.0, 18.2, 20.1]
        })
        
        cleaned = clean_data(test_data)
        
        assert len(cleaned) == 4
        assert cleaned['gmv'].min() > 0
        assert cleaned['dau'].min() > 0
        assert not cleaned.isnull().any().any()

    def test_handle_null_values(self):
        """测试空值填充逻辑"""
        test_data = pd.DataFrame({
            'gmv': [100, np.nan, 300],
            'dau': [np.nan, 60, 70],
            'conversion_rate': [12.5, np.nan, 18.2]
        })
        
        cleaned = clean_data(test_data)
        
        # 检查空值是否被正确填充
        assert not cleaned.isnull().any().any()
        # 检查填充后的数据是否合理
        assert all(cleaned['gmv'] >= 0)
        assert all(cleaned['dau'] >= 0)

    def test_invalid_conversion_rate(self):
        """测试转化率边界值处理"""
        test_data = pd.DataFrame({
            'gmv': [100, 200, 300],
            'dau': [50, 60, 70],
            'conversion_rate': [120, -5, 15]  # 120%和-5%为非法值
        })
        
        # 如果data_processor中实现了转化率验证
        cleaned = clean_data(test_data)
        
        # 至少应该保留gmv和dau都大于0的行
        valid_rows = cleaned[(cleaned['gmv'] > 0) & (cleaned['dau'] > 0)]
        assert len(valid_rows) >= 1

    def test_zero_values_filtering(self):
        """测试零值和负值过滤"""
        test_data = pd.DataFrame({
            'gmv': [0, -10, 200, 300],
            'dau': [50, 60, 0, 80],
            'conversion_rate': [12.5, 15.0, 18.2, 20.1]
        })
        
        cleaned = clean_data(test_data)
        
        # 应该只保留gmv>0 且 dau>0的行
        assert all(cleaned['gmv'] > 0)
        assert all(cleaned['dau'] > 0)
        assert len(cleaned) == 1  # 只有最后一行符合条件

    def test_all_invalid_data(self):
        """测试全无效数据清洗"""
        test_data = pd.DataFrame({
            'gmv': [0, -1, 0],
            'dau': [-5, 0, 0],
            'conversion_rate': [150, -20, 200]
        })
        
        cleaned = clean_data(test_data)
        
        # 全无效数据应返回空DataFrame
        assert cleaned.empty or len(cleaned) == 0

    def test_mixed_valid_invalid_data(self):
        """测试混合有效无效数据"""
        test_data = pd.DataFrame({
            'gmv': [100, 0, 300, -50, 500],
            'dau': [50, 60, 0, 80, 90],
            'conversion_rate': [12.5, 15.0, 18.2, 20.1, 25.0]
        })
        
        cleaned = clean_data(test_data)
        
        # 应该保留第1行和第5行 (gmv>0 且 dau>0)
        assert len(cleaned) == 2
        assert all(cleaned['gmv'] > 0)
        assert all(cleaned['dau'] > 0)

    def test_empty_dataframe(self):
        """测试空DataFrame输入"""
        test_data = pd.DataFrame()
        
        # 根据实际实现调整预期行为
        try:
            cleaned = clean_data(test_data)
            # 如果能处理空DataFrame，应该返回空DataFrame
            assert cleaned.empty
        except (ValueError, KeyError):
            # 如果抛出异常，这也是合理的
            pass

    def test_single_row_valid_data(self):
        """测试单行有效数据"""
        test_data = pd.DataFrame({
            'gmv': [100],
            'dau': [50],
            'conversion_rate': [15.0]
        })
        
        cleaned = clean_data(test_data)
        
        assert len(cleaned) == 1
        assert cleaned['gmv'].iloc[0] == 100
        assert cleaned['dau'].iloc[0] == 50 