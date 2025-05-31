import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union
import logging
from datetime import datetime
import json
import os

class DataProcessor:
    """数据处理核心类，负责数据的导入、预处理和验证"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.supported_formats = ['csv', 'excel', 'json']
        self.data_cache = {}
        
    def import_data(self, file_path: str, file_type: str) -> pd.DataFrame:
        """
        导入数据文件
        
        Args:
            file_path: 文件路径
            file_type: 文件类型 (csv/excel/json)
            
        Returns:
            pd.DataFrame: 导入的数据
        """
        try:
            if file_type not in self.supported_formats:
                raise ValueError(f"不支持的文件类型: {file_type}")
                
            if file_type == 'csv':
                df = pd.read_csv(file_path)
            elif file_type == 'excel':
                df = pd.read_excel(file_path)
            elif file_type == 'json':
                df = pd.read_json(file_path)
                
            self.logger.info(f"成功导入数据文件: {file_path}")
            return df
            
        except Exception as e:
            self.logger.error(f"导入数据文件失败: {str(e)}")
            raise
            
    def preprocess_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        数据预处理
        
        Args:
            df: 输入数据框
            
        Returns:
            pd.DataFrame: 预处理后的数据
        """
        try:
            # 1. 处理缺失值
            df = self._handle_missing_values(df)
            
            # 2. 处理异常值
            df = self._handle_outliers(df)
            
            # 3. 数据类型转换
            df = self._convert_data_types(df)
            
            # 4. 数据标准化
            df = self._normalize_data(df)
            
            self.logger.info("数据预处理完成")
            return df
            
        except Exception as e:
            self.logger.error(f"数据预处理失败: {str(e)}")
            raise
            
    def validate_data(self, df: pd.DataFrame) -> Dict:
        """
        数据验证
        
        Args:
            df: 输入数据框
            
        Returns:
            Dict: 验证结果
        """
        try:
            validation_results = {
                'total_rows': len(df),
                'total_columns': len(df.columns),
                'missing_values': df.isnull().sum().to_dict(),
                'data_types': df.dtypes.to_dict(),
                'duplicates': df.duplicated().sum(),
                'validation_time': datetime.now().isoformat()
            }
            
            self.logger.info("数据验证完成")
            return validation_results
            
        except Exception as e:
            self.logger.error(f"数据验证失败: {str(e)}")
            raise
            
    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """处理缺失值"""
        # 数值型列用中位数填充
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
        
        # 分类型列用众数填充
        categorical_cols = df.select_dtypes(include=['object']).columns
        df[categorical_cols] = df[categorical_cols].fillna(df[categorical_cols].mode().iloc[0])
        
        return df
        
    def _handle_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        """处理异常值"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            df[col] = df[col].clip(lower_bound, upper_bound)
            
        return df
        
    def _convert_data_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """数据类型转换"""
        # 日期列转换
        date_columns = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
        for col in date_columns:
            try:
                df[col] = pd.to_datetime(df[col])
            except:
                pass
                
        return df
        
    def _normalize_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """数据标准化"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            mean = df[col].mean()
            std = df[col].std()
            if std != 0:
                df[col] = (df[col] - mean) / std
                
        return df
        
    def export_data(self, df: pd.DataFrame, file_path: str, file_type: str) -> None:
        """
        导出数据
        
        Args:
            df: 数据框
            file_path: 导出文件路径
            file_type: 文件类型
        """
        try:
            if file_type == 'csv':
                df.to_csv(file_path, index=False)
            elif file_type == 'excel':
                df.to_excel(file_path, index=False)
            elif file_type == 'json':
                df.to_json(file_path, orient='records')
                
            self.logger.info(f"数据导出成功: {file_path}")
            
        except Exception as e:
            self.logger.error(f"数据导出失败: {str(e)}")
            raise 