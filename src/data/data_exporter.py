#!/usr/bin/env python3
"""
数据导出模块
支持多种数据格式的导出功能
"""

import os
import pandas as pd
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path
import logging

from src.config.settings import settings
from src.utils.logger import system_logger

class DataExporter:
    """数据导出器"""

    def __init__(self):
        self.supported_formats = {
            'csv': self._export_csv,
            'json': self._export_json,
            'xlsx': self._export_excel,
            'html': self._export_html,
            'txt': self._export_txt
        }

    def export_data(self, data: pd.DataFrame, file_path: str, format_type: str = 'csv',
                   include_metadata: bool = True, **kwargs) -> Dict[str, Any]:
        """
        导出数据到文件

        Args:
            data: 要导出的数据
            file_path: 导出文件路径
            format_type: 导出格式
            include_metadata: 是否包含元数据
            **kwargs: 其他参数

        Returns:
            Dict: 导出结果信息
        """
        try:
            if format_type not in self.supported_formats:
                raise ValueError(f"不支持的导出格式: {format_type}")

            file_path_obj = Path(file_path)
            file_path_obj.parent.mkdir(parents=True, exist_ok=True)

            # 记录导出开始
            system_logger.info("开始导出数据文件", file_path=file_path, format=format_type, rows=len(data))

            # 调用对应的导出方法
            self.supported_formats[format_type](data, file_path, **kwargs)

            # 生成元数据
            metadata = None
            if include_metadata:
                metadata = self._generate_export_metadata(data, file_path, format_type)

            # 获取文件信息
            file_size = file_path_obj.stat().st_size

            system_logger.info("数据文件导出完成", file_size=file_size, format=format_type)

            return {
                'success': True,
                'file_path': str(file_path),
                'format': format_type,
                'rows': len(data),
                'columns': len(data.columns),
                'file_size': file_size,
                'export_time': datetime.now().isoformat(),
                'metadata': metadata
            }

        except Exception as e:
            system_logger.error("数据导出失败", error=e, file_path=file_path)
            return {
                'success': False,
                'error': str(e),
                'file_path': file_path,
                'format': format_type
            }

    def _export_csv(self, data: pd.DataFrame, file_path: str, **kwargs):
        """导出为CSV文件"""
        encoding = kwargs.get('encoding', 'utf-8')
        index = kwargs.get('index', False)
        sep = kwargs.get('sep', ',')

        data.to_csv(file_path, encoding=encoding, index=index, sep=sep)

    def _export_excel(self, data: pd.DataFrame, file_path: str, **kwargs):
        """导出为Excel文件"""
        sheet_name = kwargs.get('sheet_name', 'Sheet1')
        index = kwargs.get('index', False)

        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            data.to_excel(writer, sheet_name=sheet_name, index=index)

    def _export_json(self, data: pd.DataFrame, file_path: str, **kwargs):
        """导出为JSON文件"""
        orient = kwargs.get('orient', 'records')
        indent = kwargs.get('indent', 2)

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data.to_dict(orient=orient), f, indent=indent, ensure_ascii=False)

    def _export_html(self, data: pd.DataFrame, file_path: str, **kwargs):
        """导出为HTML文件"""
        title = kwargs.get('title', '数据导出报告')
        index = kwargs.get('index', False)

        html_content = f"""
        <!DOCTYPE html>
        <html lang="zh">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title}</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            <div class="container mt-4">
                <h2 class="mb-4">{title}</h2>
                <p class="text-muted">导出时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p class="text-muted">数据行数: {len(data)}, 列数: {len(data.columns)}</p>
                <div class="table-responsive">
                    {data.to_html(index=index, classes='table table-striped table-hover')}
                </div>
            </div>
        </body>
        </html>
        """

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

    def _export_txt(self, data: pd.DataFrame, file_path: str, **kwargs):
        """导出为文本文件"""
        sep = kwargs.get('sep', '\t')
        index = kwargs.get('index', False)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"# 数据导出报告\n")
            f.write(f"# 导出时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# 数据行数: {len(data)}, 列数: {len(data.columns)}\n")
            f.write("#" * 50 + "\n")

        data.to_csv(file_path, mode='a', sep=sep, index=index, encoding='utf-8')

    def _generate_export_metadata(self, data: pd.DataFrame, file_path: str, format_type: str) -> Dict[str, Any]:
        """生成导出元数据"""
        return {
            'export_info': {
                'timestamp': datetime.now().isoformat(),
                'format': format_type,
                'file_path': file_path
            },
            'data_summary': {
                'rows': len(data),
                'columns': len(data.columns),
                'column_names': data.columns.tolist(),
                'dtypes': data.dtypes.to_dict(),
                'memory_usage': data.memory_usage(deep=True).sum()
            },
            'data_quality': {
                'missing_values': data.isnull().sum().to_dict(),
                'missing_percentage': (data.isnull().sum() / len(data) * 100).to_dict(),
                'duplicate_rows': data.duplicated().sum()
            }
        }

    def export_multiple_formats(self, data: pd.DataFrame, base_path: str,
                              formats: List[str] = None) -> List[Dict[str, Any]]:
        """
        同时导出多种格式

        Args:
            data: 要导出的数据
            base_path: 基础文件路径（不含扩展名）
            formats: 要导出的格式列表

        Returns:
            List[Dict]: 导出结果列表
        """
        if formats is None:
            formats = ['csv', 'xlsx', 'json']

        results = []
        for fmt in formats:
            file_path = f"{base_path}.{fmt}"
            result = self.export_data(data, file_path, fmt)
            results.append(result)

        return results
