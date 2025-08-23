#!/usr/bin/env python3
"""
数据导入模块
支持多种数据格式的导入功能
"""

import os
import pandas as pd
import json
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from pathlib import Path
import logging

from src.config.settings import settings
from src.utils.logger import system_logger

class DataImporter:
    """数据导入器"""

    def __init__(self):
        self.supported_formats = {
            '.csv': self._import_csv,
            '.json': self._import_json,
            '.xlsx': self._import_excel,
            '.xls': self._import_excel,
            '.txt': self._import_txt
        }

    def import_data(self, file_path: str, **kwargs) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        导入数据文件

        Args:
            file_path: 文件路径
            **kwargs: 其他参数

        Returns:
            Tuple[DataFrame, Dict]: (数据, 元数据)
        """
        try:
            file_path_obj = Path(file_path)
            if not file_path_obj.exists():
                raise FileNotFoundError(f"文件不存在: {file_path}")

            file_extension = file_path_obj.suffix.lower()
            if file_extension not in self.supported_formats:
                raise ValueError(f"不支持的文件格式: {file_extension}")

            # 记录导入开始
            system_logger.info("开始导入数据文件", file_path=file_path, format=file_extension)

            # 调用对应的导入方法
            data = self.supported_formats[file_extension](file_path, **kwargs)

            # 生成元数据
            metadata = self._generate_metadata(data, file_path, file_extension)

            system_logger.info("数据文件导入完成", rows=len(data), columns=len(data.columns))

            return data, metadata

        except Exception as e:
            system_logger.error("数据导入失败", error=e, file_path=file_path)
            raise

    def _import_csv(self, file_path: str, **kwargs) -> pd.DataFrame:
        """导入CSV文件"""
        encoding = kwargs.get('encoding', 'utf-8')
        delimiter = kwargs.get('delimiter', ',')
        header = kwargs.get('header', 0)

        return pd.read_csv(file_path, encoding=encoding, delimiter=delimiter, header=header)

    def _import_excel(self, file_path: str, **kwargs) -> pd.DataFrame:
        """导入Excel文件"""
        sheet_name = kwargs.get('sheet_name', 0)
        header = kwargs.get('header', 0)

        return pd.read_excel(file_path, sheet_name=sheet_name, header=header)

    def _import_json(self, file_path: str, **kwargs) -> pd.DataFrame:
        """导入JSON文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if isinstance(data, list):
            return pd.DataFrame(data)
        elif isinstance(data, dict):
            if 'data' in data:
                return pd.DataFrame(data['data'])
            else:
                return pd.DataFrame([data])
        else:
            raise ValueError("不支持的JSON格式")

    def _import_txt(self, file_path: str, **kwargs) -> pd.DataFrame:
        """导入文本文件"""
        encoding = kwargs.get('encoding', 'utf-8')
        delimiter = kwargs.get('delimiter', '\t')

        return pd.read_csv(file_path, encoding=encoding, delimiter=delimiter)

    def _generate_metadata(self, data: pd.DataFrame, file_path: str, format_type: str) -> Dict[str, Any]:
        """生成导入元数据"""
        file_path_obj = Path(file_path)

        return {
            'file_info': {
                'name': file_path_obj.name,
                'size': file_path_obj.stat().st_size,
                'format': format_type,
                'path': str(file_path)
            },
            'data_info': {
                'rows': len(data),
                'columns': len(data.columns),
                'column_names': data.columns.tolist(),
                'dtypes': data.dtypes.to_dict()
            },
            'import_info': {
                'timestamp': datetime.now().isoformat(),
                'missing_values': data.isnull().sum().to_dict(),
                'memory_usage': data.memory_usage(deep=True).sum()
            }
        }

    def validate_data(self, data: pd.DataFrame, validation_rules: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证数据质量

        Args:
            data: 待验证的数据
            validation_rules: 验证规则

        Returns:
            Dict: 验证结果
        """
        results = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'statistics': {}
        }

        # 检查必需列
        required_columns = validation_rules.get('required_columns', [])
        missing_columns = [col for col in required_columns if col not in data.columns]
        if missing_columns:
            results['valid'] = False
            results['errors'].append(f"缺少必需列: {missing_columns}")

        # 检查数据类型
        expected_types = validation_rules.get('expected_types', {})
        for col, expected_type in expected_types.items():
            if col in data.columns:
                actual_type = str(data[col].dtype)
                if expected_type not in actual_type:
                    results['warnings'].append(f"列 {col} 类型不匹配，期望: {expected_type}, 实际: {actual_type}")

        # 检查数据范围
        range_rules = validation_rules.get('range_rules', {})
        for col, ranges in range_rules.items():
            if col in data.columns:
                min_val = data[col].min()
                max_val = data[col].max()
                expected_min = ranges.get('min')
                expected_max = ranges.get('max')

                if expected_min is not None and min_val < expected_min:
                    results['warnings'].append(f"列 {col} 最小值 {min_val} 低于期望值 {expected_min}")
                if expected_max is not None and max_val > expected_max:
                    results['warnings'].append(f"列 {col} 最大值 {max_val} 高于期望值 {expected_max}")

        # 计算基本统计信息
        results['statistics'] = {
            'total_cells': data.size,
            'missing_cells': data.isnull().sum().sum(),
            'missing_percentage': (data.isnull().sum().sum() / data.size * 100) if data.size > 0 else 0
        }

        return results
