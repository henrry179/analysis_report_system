#!/usr/bin/env python3
"""
增强版数据处理器
提供更强大的数据清洗、验证和转换功能
"""

import os
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from pathlib import Path

# 条件导入
try:
    import pandas as pd
    import numpy as np
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

class EnhancedDataProcessor:
    """增强版数据处理器"""
    
    def __init__(self):
        self.processing_log = []
        self.data_quality_metrics = {}
        
    def log_operation(self, operation: str, details: str):
        """记录处理操作"""
        self.processing_log.append({
            'timestamp': datetime.now().isoformat(),
            'operation': operation,
            'details': details
        })
    
    def validate_data_structure(self, data: Any) -> Dict[str, Any]:
        """验证数据结构"""
        validation_result = {
            'is_valid': True,
            'issues': [],
            'suggestions': [],
            'data_info': {}
        }
        
        if PANDAS_AVAILABLE and hasattr(data, 'shape'):
            # pandas DataFrame 验证
            validation_result['data_info'] = {
                'rows': data.shape[0],
                'columns': data.shape[1],
                'column_names': list(data.columns),
                'dtypes': {col: str(dtype) for col, dtype in data.dtypes.items()},
                'null_counts': data.isnull().sum().to_dict(),
                'memory_usage': f"{data.memory_usage(deep=True).sum() / 1024:.2f} KB"
            }
            
            # 检查必需字段
            required_fields = ['date', 'category', 'region', 'gmv', 'dau']
            missing_fields = [field for field in required_fields if field not in data.columns]
            
            if missing_fields:
                validation_result['is_valid'] = False
                validation_result['issues'].append(f"缺少必需字段: {missing_fields}")
                validation_result['suggestions'].append("请确保数据包含所有必需字段")
            
            # 检查数据质量
            if data.empty:
                validation_result['is_valid'] = False
                validation_result['issues'].append("数据为空")
            
            # 检查空值比例
            null_percentages = (data.isnull().sum() / len(data) * 100)
            high_null_cols = null_percentages[null_percentages > 50].index.tolist()
            
            if high_null_cols:
                validation_result['issues'].append(f"高空值比例字段: {high_null_cols}")
                validation_result['suggestions'].append("考虑清理或填充高空值比例的字段")
        
        else:
            # 简化模式验证
            if hasattr(data, 'data'):
                validation_result['data_info'] = {
                    'type': 'MockDataFrame',
                    'data_keys': list(data.data.keys()) if hasattr(data, 'data') else []
                }
            else:
                validation_result['data_info'] = {
                    'type': type(data).__name__,
                    'length': len(data) if hasattr(data, '__len__') else 'unknown'
                }
        
        self.log_operation('数据验证', f"验证结果: {'通过' if validation_result['is_valid'] else '失败'}")
        return validation_result
    
    def clean_data(self, data: Any, cleaning_config: Optional[Dict] = None) -> Tuple[Any, Dict]:
        """增强数据清洗"""
        if cleaning_config is None:
            cleaning_config = {
                'remove_duplicates': True,
                'fill_numeric_nulls': 'mean',  # 'mean', 'median', 'zero', 'forward_fill'
                'fill_categorical_nulls': 'mode',  # 'mode', 'unknown', 'forward_fill'
                'outlier_method': 'iqr',  # 'iqr', 'zscore', 'none'
                'date_format': '%Y-%m-%d'
            }
        
        cleaning_report = {
            'operations_performed': [],
            'rows_before': 0,
            'rows_after': 0,
            'columns_processed': 0,
            'issues_fixed': []
        }
        
        if PANDAS_AVAILABLE and hasattr(data, 'shape'):
            cleaning_report['rows_before'] = len(data)
            cleaned_data = data.copy()
            
            # 1. 移除重复行
            if cleaning_config.get('remove_duplicates', True):
                before_dedup = len(cleaned_data)
                cleaned_data = cleaned_data.drop_duplicates()
                duplicates_removed = before_dedup - len(cleaned_data)
                if duplicates_removed > 0:
                    cleaning_report['operations_performed'].append(f"移除重复行: {duplicates_removed}")
                    cleaning_report['issues_fixed'].append('重复数据')
            
            # 2. 处理数值型空值
            numeric_columns = cleaned_data.select_dtypes(include=[np.number]).columns
            for col in numeric_columns:
                null_count = cleaned_data[col].isnull().sum()
                if null_count > 0:
                    fill_method = cleaning_config.get('fill_numeric_nulls', 'mean')
                    if fill_method == 'mean':
                        fill_value = cleaned_data[col].mean()
                    elif fill_method == 'median':
                        fill_value = cleaned_data[col].median()
                    elif fill_method == 'zero':
                        fill_value = 0
                    else:
                        fill_value = cleaned_data[col].fillna(method='ffill')
                        continue
                    
                    cleaned_data[col] = cleaned_data[col].fillna(fill_value)
                    cleaning_report['operations_performed'].append(f"填充 {col} 空值: {null_count} 个")
            
            # 3. 处理分类型空值
            categorical_columns = cleaned_data.select_dtypes(include=['object']).columns
            for col in categorical_columns:
                null_count = cleaned_data[col].isnull().sum()
                if null_count > 0:
                    fill_method = cleaning_config.get('fill_categorical_nulls', 'mode')
                    if fill_method == 'mode':
                        mode_value = cleaned_data[col].mode().iloc[0] if not cleaned_data[col].mode().empty else 'Unknown'
                        cleaned_data[col] = cleaned_data[col].fillna(mode_value)
                    elif fill_method == 'unknown':
                        cleaned_data[col] = cleaned_data[col].fillna('Unknown')
                    
                    cleaning_report['operations_performed'].append(f"填充 {col} 空值: {null_count} 个")
            
            # 4. 异常值检测和处理
            outlier_method = cleaning_config.get('outlier_method', 'iqr')
            if outlier_method != 'none':
                for col in numeric_columns:
                    if outlier_method == 'iqr':
                        Q1 = cleaned_data[col].quantile(0.25)
                        Q3 = cleaned_data[col].quantile(0.75)
                        IQR = Q3 - Q1
                        lower_bound = Q1 - 1.5 * IQR
                        upper_bound = Q3 + 1.5 * IQR
                        
                        outliers = ((cleaned_data[col] < lower_bound) | (cleaned_data[col] > upper_bound)).sum()
                        if outliers > 0:
                            # 用边界值替换异常值
                            cleaned_data[col] = cleaned_data[col].clip(lower=lower_bound, upper=upper_bound)
                            cleaning_report['operations_performed'].append(f"处理 {col} 异常值: {outliers} 个")
                            cleaning_report['issues_fixed'].append(f'{col}异常值')
            
            # 5. 日期格式标准化
            if 'date' in cleaned_data.columns:
                try:
                    cleaned_data['date'] = pd.to_datetime(cleaned_data['date'], format=cleaning_config.get('date_format'))
                    cleaning_report['operations_performed'].append("标准化日期格式")
                except:
                    cleaning_report['operations_performed'].append("日期格式标准化失败")
            
            cleaning_report['rows_after'] = len(cleaned_data)
            cleaning_report['columns_processed'] = len(cleaned_data.columns)
            
        else:
            # 简化模式清洗
            cleaned_data = data
            cleaning_report['operations_performed'].append("简化模式清洗 - 基本验证")
            
        self.log_operation('数据清洗', f"处理了 {len(cleaning_report['operations_performed'])} 个操作")
        return cleaned_data, cleaning_report
    
    def transform_data(self, data: Any, transformations: Optional[Dict] = None) -> Tuple[Any, Dict]:
        """数据转换"""
        if transformations is None:
            transformations = {
                'create_derived_metrics': True,
                'normalize_values': False,
                'create_time_features': True,
                'aggregate_by_period': None  # 'daily', 'weekly', 'monthly'
            }
        
        transform_report = {
            'transformations_applied': [],
            'new_columns_created': [],
            'metrics_computed': []
        }
        
        if PANDAS_AVAILABLE and hasattr(data, 'columns'):
            transformed_data = data.copy()
            
            # 1. 创建衍生指标
            if transformations.get('create_derived_metrics', True):
                if all(col in transformed_data.columns for col in ['gmv', 'dau']):
                    transformed_data['arpu'] = transformed_data['gmv'] / transformed_data['dau']
                    transform_report['new_columns_created'].append('arpu')
                    transform_report['metrics_computed'].append('平均每用户收入')
                
                if all(col in transformed_data.columns for col in ['gmv', 'frequency', 'dau']):
                    transformed_data['avg_order_value'] = transformed_data['gmv'] / (transformed_data['frequency'] * transformed_data['dau'])
                    transform_report['new_columns_created'].append('avg_order_value')
                    transform_report['metrics_computed'].append('平均订单价值')
                
                if 'conversion_rate' in transformed_data.columns:
                    transformed_data['conversion_efficiency'] = transformed_data['conversion_rate'] * transformed_data.get('dau', 1)
                    transform_report['new_columns_created'].append('conversion_efficiency')
                    transform_report['metrics_computed'].append('转化效率')
            
            # 2. 创建时间特征
            if transformations.get('create_time_features', True) and 'date' in transformed_data.columns:
                try:
                    date_col = pd.to_datetime(transformed_data['date'])
                    transformed_data['year'] = date_col.dt.year
                    transformed_data['month'] = date_col.dt.month
                    transformed_data['day'] = date_col.dt.day
                    transformed_data['weekday'] = date_col.dt.dayofweek
                    transformed_data['is_weekend'] = date_col.dt.dayofweek.isin([5, 6])
                    
                    time_features = ['year', 'month', 'day', 'weekday', 'is_weekend']
                    transform_report['new_columns_created'].extend(time_features)
                    transform_report['transformations_applied'].append('时间特征提取')
                except:
                    transform_report['transformations_applied'].append('时间特征提取失败')
            
            # 3. 数值标准化
            if transformations.get('normalize_values', False):
                numeric_columns = transformed_data.select_dtypes(include=[np.number]).columns
                for col in numeric_columns:
                    if col not in ['year', 'month', 'day', 'weekday']:  # 跳过时间特征
                        col_mean = transformed_data[col].mean()
                        col_std = transformed_data[col].std()
                        if col_std > 0:
                            transformed_data[f'{col}_normalized'] = (transformed_data[col] - col_mean) / col_std
                            transform_report['new_columns_created'].append(f'{col}_normalized')
                
                if any('_normalized' in col for col in transform_report['new_columns_created']):
                    transform_report['transformations_applied'].append('数值标准化')
            
            # 4. 聚合数据
            agg_period = transformations.get('aggregate_by_period')
            if agg_period and 'date' in transformed_data.columns:
                try:
                    date_col = pd.to_datetime(transformed_data['date'])
                    if agg_period == 'weekly':
                        transformed_data['period'] = date_col.dt.to_period('W')
                    elif agg_period == 'monthly':
                        transformed_data['period'] = date_col.dt.to_period('M')
                    
                    if 'period' in transformed_data.columns:
                        transform_report['transformations_applied'].append(f'{agg_period}聚合')
                except:
                    transform_report['transformations_applied'].append(f'{agg_period}聚合失败')
                    
        else:
            # 简化模式转换
            transformed_data = data
            transform_report['transformations_applied'].append('简化模式转换')
        
        self.log_operation('数据转换', f"应用了 {len(transform_report['transformations_applied'])} 个转换")
        return transformed_data, transform_report
    
    def generate_data_profile(self, data: Any) -> Dict[str, Any]:
        """生成数据概况"""
        profile = {
            'summary': {},
            'quality_metrics': {},
            'recommendations': []
        }
        
        if PANDAS_AVAILABLE and hasattr(data, 'describe'):
            # 基础统计信息
            profile['summary'] = {
                'total_rows': len(data),
                'total_columns': len(data.columns),
                'numeric_columns': len(data.select_dtypes(include=[np.number]).columns),
                'categorical_columns': len(data.select_dtypes(include=['object']).columns),
                'datetime_columns': len(data.select_dtypes(include=['datetime64']).columns)
            }
            
            # 数据质量指标
            total_cells = len(data) * len(data.columns)
            null_cells = data.isnull().sum().sum()
            
            profile['quality_metrics'] = {
                'completeness': (1 - null_cells / total_cells) * 100,
                'null_percentage': (null_cells / total_cells) * 100,
                'duplicate_rows': data.duplicated().sum(),
                'unique_values_per_column': {col: data[col].nunique() for col in data.columns}
            }
            
            # 推荐
            if profile['quality_metrics']['null_percentage'] > 10:
                profile['recommendations'].append("空值比例较高，建议进行数据清洗")
            
            if profile['quality_metrics']['duplicate_rows'] > 0:
                profile['recommendations'].append("发现重复行，建议去重处理")
            
            # 检查数据分布
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                skewness = data[col].skew()
                if abs(skewness) > 2:
                    profile['recommendations'].append(f"{col} 数据分布偏斜，考虑变换处理")
        
        else:
            # 简化模式概况
            profile['summary'] = {
                'mode': 'simplified',
                'data_type': type(data).__name__
            }
            profile['quality_metrics'] = {
                'mode': 'basic_validation_only'
            }
        
        return profile
    
    def export_processing_log(self, filepath: str) -> bool:
        """导出处理日志"""
        try:
            log_data = {
                'processing_log': self.processing_log,
                'data_quality_metrics': self.data_quality_metrics,
                'export_time': datetime.now().isoformat()
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"导出处理日志失败: {e}")
            return False
    
    def process_pipeline(self, data: Any, config: Optional[Dict] = None) -> Tuple[Any, Dict]:
        """完整的数据处理流水线"""
        if config is None:
            config = {
                'validate': True,
                'clean': True,
                'transform': True,
                'profile': True
            }
        
        pipeline_results = {
            'validation_result': None,
            'cleaning_report': None,
            'transform_report': None,
            'data_profile': None,
            'processing_time': 0
        }
        
        start_time = datetime.now()
        processed_data = data
        
        try:
            # 1. 数据验证
            if config.get('validate', True):
                pipeline_results['validation_result'] = self.validate_data_structure(processed_data)
            
            # 2. 数据清洗
            if config.get('clean', True):
                processed_data, pipeline_results['cleaning_report'] = self.clean_data(processed_data)
            
            # 3. 数据转换
            if config.get('transform', True):
                processed_data, pipeline_results['transform_report'] = self.transform_data(processed_data)
            
            # 4. 数据概况
            if config.get('profile', True):
                pipeline_results['data_profile'] = self.generate_data_profile(processed_data)
            
            # 记录处理时间
            end_time = datetime.now()
            pipeline_results['processing_time'] = (end_time - start_time).total_seconds()
            
            self.log_operation('完整流水线', f"处理完成，耗时 {pipeline_results['processing_time']:.2f} 秒")
            
        except Exception as e:
            self.log_operation('流水线错误', f"处理失败: {str(e)}")
            raise
        
        return processed_data, pipeline_results 