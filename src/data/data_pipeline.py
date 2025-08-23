#!/usr/bin/env python3
"""
数据管道管理模块
提供完整的数据处理流程
"""

import os
import pandas as pd
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from pathlib import Path
import logging

from src.config.settings import settings
from src.utils.logger import system_logger
from src.data.data_importer import DataImporter
from src.data.data_exporter import DataExporter

class DataPipeline:
    """数据管道管理器"""

    def __init__(self):
        self.importer = DataImporter()
        self.exporter = DataExporter()
        self.pipeline_steps = []

    def add_step(self, name: str, func: Callable, **kwargs):
        """
        添加处理步骤

        Args:
            name: 步骤名称
            func: 处理函数
            **kwargs: 函数参数
        """
        self.pipeline_steps.append({
            'name': name,
            'function': func,
            'kwargs': kwargs
        })

    def execute_pipeline(self, input_data: Any, **kwargs) -> Dict[str, Any]:
        """
        执行数据管道

        Args:
            input_data: 输入数据
            **kwargs: 其他参数

        Returns:
            Dict: 处理结果
        """
        result = {
            'success': True,
            'steps_executed': [],
            'errors': [],
            'data': input_data
        }

        system_logger.info("开始执行数据管道", steps_count=len(self.pipeline_steps))

        for i, step in enumerate(self.pipeline_steps):
            try:
                step_name = step['name']
                step_func = step['function']
                step_kwargs = step['kwargs']

                system_logger.info("执行管道步骤", step=i+1, name=step_name)

                # 执行步骤
                result['data'] = step_func(result['data'], **step_kwargs)

                result['steps_executed'].append({
                    'step': i + 1,
                    'name': step_name,
                    'status': 'success'
                })

            except Exception as e:
                error_msg = f"步骤 {step_name} 执行失败: {str(e)}"
                system_logger.error("管道步骤执行失败", step=step_name, error=e)

                result['success'] = False
                result['errors'].append(error_msg)
                result['steps_executed'].append({
                    'step': i + 1,
                    'name': step_name,
                    'status': 'failed',
                    'error': str(e)
                })

                # 根据配置决定是否继续执行
                if not kwargs.get('continue_on_error', False):
                    break

        system_logger.info("数据管道执行完成", success=result['success'], steps=len(result['steps_executed']))
        return result

    def import_and_process(self, file_path: str, pipeline_steps: List[Dict] = None,
                          output_path: str = None, output_format: str = 'csv') -> Dict[str, Any]:
        """
        导入并处理数据

        Args:
            file_path: 输入文件路径
            pipeline_steps: 处理步骤列表
            output_path: 输出文件路径
            output_format: 输出格式

        Returns:
            Dict: 处理结果
        """
        result = {
            'import_result': None,
            'processing_result': None,
            'export_result': None,
            'success': True
        }

        try:
            # 导入数据
            system_logger.info("开始导入数据", file_path=file_path)
            data, metadata = self.importer.import_data(file_path)
            result['import_result'] = {
                'success': True,
                'rows': len(data),
                'columns': len(data.columns),
                'metadata': metadata
            }

            # 设置处理步骤
            if pipeline_steps:
                for step in pipeline_steps:
                    self.add_step(**step)

            # 执行处理
            if self.pipeline_steps:
                processing_result = self.execute_pipeline(data)
                result['processing_result'] = processing_result
                data = processing_result['data']

                if not processing_result['success']:
                    result['success'] = False

            # 导出结果
            if output_path and result['success']:
                export_result = self.exporter.export_data(data, output_path, output_format)
                result['export_result'] = export_result

                if not export_result['success']:
                    result['success'] = False

            system_logger.info("数据导入处理完成", success=result['success'])

        except Exception as e:
            system_logger.error("数据导入处理失败", error=e)
            result['success'] = False
            result['error'] = str(e)

        return result

class DataPipelineManager:
    """数据管道管理器"""

    def __init__(self):
        self.pipelines = {}
        self.importer = DataImporter()
        self.exporter = DataExporter()

    def create_pipeline(self, name: str, steps: List[Dict]) -> DataPipeline:
        """
        创建数据管道

        Args:
            name: 管道名称
            steps: 处理步骤

        Returns:
            DataPipeline: 数据管道实例
        """
        pipeline = DataPipeline()

        for step in steps:
            pipeline.add_step(**step)

        self.pipelines[name] = pipeline
        system_logger.info("数据管道创建成功", name=name, steps_count=len(steps))

        return pipeline

    def get_pipeline(self, name: str) -> Optional[DataPipeline]:
        """获取数据管道"""
        return self.pipelines.get(name)

    def list_pipelines(self) -> List[str]:
        """列出所有管道"""
        return list(self.pipelines.keys())

    def delete_pipeline(self, name: str) -> bool:
        """
        删除数据管道

        Args:
            name: 管道名称

        Returns:
            bool: 是否删除成功
        """
        if name in self.pipelines:
            del self.pipelines[name]
            system_logger.info("数据管道删除成功", name=name)
            return True
        return False

    def execute_pipeline_by_name(self, name: str, input_data: Any, **kwargs) -> Dict[str, Any]:
        """
        按名称执行数据管道

        Args:
            name: 管道名称
            input_data: 输入数据
            **kwargs: 其他参数

        Returns:
            Dict: 执行结果
        """
        pipeline = self.get_pipeline(name)
        if not pipeline:
            return {
                'success': False,
                'error': f"管道 '{name}' 不存在"
            }

        system_logger.info("开始执行命名管道", name=name)
        return pipeline.execute_pipeline(input_data, **kwargs)

# 全局数据管道管理器实例
pipeline_manager = DataPipelineManager()

# 预定义的处理步骤函数
def clean_missing_values(data: pd.DataFrame, strategy: str = 'mean') -> pd.DataFrame:
    """清洗缺失值"""
    if strategy == 'mean':
        numeric_columns = data.select_dtypes(include=['number']).columns
        data[numeric_columns] = data[numeric_columns].fillna(data[numeric_columns].mean())
    elif strategy == 'median':
        numeric_columns = data.select_dtypes(include=['number']).columns
        data[numeric_columns] = data[numeric_columns].fillna(data[numeric_columns].median())
    elif strategy == 'drop':
        data = data.dropna()

    return data

def remove_duplicates(data: pd.DataFrame) -> pd.DataFrame:
    """删除重复行"""
    return data.drop_duplicates()

def normalize_numeric_columns(data: pd.DataFrame, columns: List[str] = None) -> pd.DataFrame:
    """标准化数值列"""
    if columns is None:
        columns = data.select_dtypes(include=['number']).columns.tolist()

    for col in columns:
        if col in data.columns:
            data[col] = (data[col] - data[col].mean()) / data[col].std()

    return data

def filter_by_date_range(data: pd.DataFrame, date_column: str, start_date: str, end_date: str) -> pd.DataFrame:
    """按日期范围过滤"""
    if date_column in data.columns:
        data[date_column] = pd.to_datetime(data[date_column])
        mask = (data[date_column] >= start_date) & (data[date_column] <= end_date)
        return data[mask]
    return data

def aggregate_by_group(data: pd.DataFrame, group_by: str, agg_columns: Dict[str, str]) -> pd.DataFrame:
    """按分组聚合"""
    if group_by in data.columns:
        return data.groupby(group_by).agg(agg_columns).reset_index()
    return data
