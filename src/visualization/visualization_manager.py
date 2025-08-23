#!/usr/bin/env python3
"""
可视化管理器
统一管理所有图表生成和可视化功能
"""

import os
import json
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
from pathlib import Path
import logging

from src.config.settings import settings
from src.utils.logger import system_logger
from .chart_generator import ChartGenerator, TextChartGenerator
from .enhanced_chart_generator import EnhancedChartGenerator

class VisualizationManager:
    """可视化管理器"""

    def __init__(self, output_dir: str = None):
        """
        初始化可视化管理器

        Args:
            output_dir: 输出目录，默认使用配置中的目录
        """
        self.output_dir = Path(output_dir or settings.CHARTS_DIR)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.chart_generator = ChartGenerator(str(self.output_dir))
        self.enhanced_generator = EnhancedChartGenerator()
        self.text_generator = TextChartGenerator()

        self.generated_charts = []
        self.visualization_configs = {
            'theme': 'modern',
            'color_palette': 'viridis',
            'interactive': True,
            'export_formats': ['html', 'png', 'svg', 'pdf']
        }

    def create_comprehensive_dashboard(self, data: Any, dashboard_type: str = 'comprehensive',
                                    **kwargs) -> Dict[str, Any]:
        """
        创建综合仪表板

        Args:
            data: 数据
            dashboard_type: 仪表板类型
            **kwargs: 其他参数

        Returns:
            Dict: 仪表板创建结果
        """
        try:
            system_logger.info("开始创建综合仪表板", dashboard_type=dashboard_type)

            result = {
                'success': True,
                'dashboard_type': dashboard_type,
                'charts_generated': [],
                'files_created': [],
                'interactive_components': [],
                'data_summary': {}
            }

            # 数据预处理
            processed_data = self._preprocess_data(data)

            # 根据类型创建不同仪表板
            if dashboard_type == 'comprehensive':
                dashboard_result = self._create_comprehensive_dashboard(processed_data, **kwargs)
            elif dashboard_type == 'business':
                dashboard_result = self._create_business_dashboard(processed_data, **kwargs)
            elif dashboard_type == 'technical':
                dashboard_result = self._create_technical_dashboard(processed_data, **kwargs)
            elif dashboard_type == 'retail':
                dashboard_result = self._create_retail_dashboard(processed_data, **kwargs)
            else:
                dashboard_result = self._create_custom_dashboard(processed_data, dashboard_type, **kwargs)

            result.update(dashboard_result)

            # 生成数据摘要
            result['data_summary'] = self._generate_data_summary(processed_data)

            system_logger.info("综合仪表板创建完成", charts_count=len(result['charts_generated']))
            return result

        except Exception as e:
            system_logger.error("综合仪表板创建失败", error=e, dashboard_type=dashboard_type)
            return {
                'success': False,
                'error': str(e),
                'dashboard_type': dashboard_type
            }

    def _create_comprehensive_dashboard(self, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """创建综合仪表板"""
        charts = []

        # 1. 核心指标卡片
        if 'metrics' in data:
            metrics_chart = self._create_metrics_cards(data['metrics'])
            charts.append(metrics_chart)

        # 2. 趋势分析图表
        if 'trends' in data:
            trend_chart = self._create_trend_chart(data['trends'])
            charts.append(trend_chart)

        # 3. 分布分析图表
        if 'distributions' in data:
            dist_chart = self._create_distribution_chart(data['distributions'])
            charts.append(dist_chart)

        # 4. 相关性热力图
        if 'correlations' in data:
            corr_chart = self._create_correlation_heatmap(data['correlations'])
            charts.append(corr_chart)

        # 5. 异常检测图表
        if 'outliers' in data:
            outlier_chart = self._create_outlier_chart(data['outliers'])
            charts.append(outlier_chart)

        return {
            'charts_generated': charts,
            'files_created': [chart['file_path'] for chart in charts if 'file_path' in chart],
            'interactive_components': self._create_interactive_components(charts)
        }

    def _create_business_dashboard(self, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """创建业务仪表板"""
        charts = []

        # 业务关键指标
        business_metrics = ['gmv', 'revenue', 'orders', 'customers', 'conversion_rate']
        for metric in business_metrics:
            if metric in data:
                chart = self._create_metric_chart(data[metric], metric)
                charts.append(chart)

        # 销售漏斗分析
        if 'sales_funnel' in data:
            funnel_chart = self._create_funnel_chart(data['sales_funnel'])
            charts.append(funnel_chart)

        # 客户细分分析
        if 'customer_segments' in data:
            segment_chart = self._create_segment_chart(data['customer_segments'])
            charts.append(segment_chart)

        return {
            'charts_generated': charts,
            'files_created': [chart['file_path'] for chart in charts if 'file_path' in chart],
            'interactive_components': self._create_interactive_components(charts)
        }

    def _create_retail_dashboard(self, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """创建零售行业仪表板"""
        charts = []

        # 零售核心指标
        retail_metrics = ['gmv', 'dau', 'conversion_rate', 'order_price', 'category_performance']
        for metric in retail_metrics:
            if metric in data:
                chart = self._create_retail_metric_chart(data[metric], metric)
                charts.append(chart)

        # 区域分析
        if 'region_analysis' in data:
            region_chart = self._create_region_chart(data['region_analysis'])
            charts.append(region_chart)

        # 品类贡献分析
        if 'category_contribution' in data:
            category_chart = self._create_category_chart(data['category_contribution'])
            charts.append(category_chart)

        return {
            'charts_generated': charts,
            'files_created': [chart['file_path'] for chart in charts if 'file_path' in chart],
            'interactive_components': self._create_interactive_components(charts)
        }

    def _create_technical_dashboard(self, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """创建技术仪表板"""
        charts = []

        # 数据质量指标
        if 'data_quality' in data:
            quality_chart = self._create_quality_chart(data['data_quality'])
            charts.append(quality_chart)

        # 系统性能指标
        if 'system_performance' in data:
            perf_chart = self._create_performance_chart(data['system_performance'])
            charts.append(perf_chart)

        # 错误分析
        if 'error_analysis' in data:
            error_chart = self._create_error_chart(data['error_analysis'])
            charts.append(error_chart)

        return {
            'charts_generated': charts,
            'files_created': [chart['file_path'] for chart in charts if 'file_path' in chart],
            'interactive_components': self._create_interactive_components(charts)
        }

    def _create_custom_dashboard(self, data: Dict[str, Any], dashboard_type: str, **kwargs) -> Dict[str, Any]:
        """创建自定义仪表板"""
        # 基于配置创建自定义图表
        custom_config = kwargs.get('config', {})

        charts = []
        for chart_config in custom_config.get('charts', []):
            chart = self._create_custom_chart(data, chart_config)
            if chart:
                charts.append(chart)

        return {
            'charts_generated': charts,
            'files_created': [chart['file_path'] for chart in charts if 'file_path' in chart],
            'interactive_components': self._create_interactive_components(charts)
        }

    def _create_metrics_cards(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """创建指标卡片"""
        try:
            # 使用增强图表生成器创建指标卡片
            cards_config = {
                'type': 'metric_cards',
                'data': metrics,
                'title': '核心指标概览'
            }

            # 生成HTML格式的指标卡片
            cards_html = self._generate_metric_cards_html(metrics)

            filename = f"metric_cards_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            file_path = self.output_dir / filename

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(cards_html)

            return {
                'type': 'metric_cards',
                'title': '核心指标概览',
                'file_path': str(file_path),
                'file_url': f"/charts/{filename}",
                'format': 'html',
                'metrics_count': len(metrics)
            }

        except Exception as e:
            system_logger.error("指标卡片创建失败", error=e)
            return {
                'type': 'metric_cards',
                'title': '核心指标概览',
                'error': str(e)
            }

    def _create_trend_chart(self, trend_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建趋势图表"""
        try:
            # 使用图表生成器创建趋势图
            if hasattr(self.chart_generator, 'generate_trend_chart'):
                result = self.chart_generator.generate_trend_chart(trend_data)
                return result
            else:
                # 备选方案：生成文本趋势图
                text_chart = self.text_generator.generate_text_bar_chart(
                    trend_data.get('values', {}),
                    trend_data.get('title', '趋势分析')
                )

                filename = f"trend_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                file_path = self.output_dir / filename

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(text_chart)

                return {
                    'type': 'trend_chart',
                    'title': trend_data.get('title', '趋势分析'),
                    'file_path': str(file_path),
                    'file_url': f"/charts/{filename}",
                    'format': 'txt'
                }

        except Exception as e:
            system_logger.error("趋势图表创建失败", error=e)
            return {
                'type': 'trend_chart',
                'title': '趋势分析',
                'error': str(e)
            }

    def _create_distribution_chart(self, dist_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建分布图表"""
        try:
            # 使用图表生成器创建分布图
            if hasattr(self.chart_generator, 'generate_distribution_chart'):
                result = self.chart_generator.generate_distribution_chart(dist_data)
                return result
            else:
                return {
                    'type': 'distribution_chart',
                    'title': dist_data.get('title', '分布分析'),
                    'message': '分布图表功能待实现'
                }

        except Exception as e:
            system_logger.error("分布图表创建失败", error=e)
            return {
                'type': 'distribution_chart',
                'title': '分布分析',
                'error': str(e)
            }

    def _create_correlation_heatmap(self, corr_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建相关性热力图"""
        try:
            # 使用图表生成器创建热力图
            if hasattr(self.chart_generator, 'generate_correlation_heatmap'):
                result = self.chart_generator.generate_correlation_heatmap(corr_data)
                return result
            else:
                return {
                    'type': 'correlation_heatmap',
                    'title': corr_data.get('title', '相关性分析'),
                    'message': '相关性热力图功能待实现'
                }

        except Exception as e:
            system_logger.error("相关性热力图创建失败", error=e)
            return {
                'type': 'correlation_heatmap',
                'title': '相关性分析',
                'error': str(e)
            }

    def _create_outlier_chart(self, outlier_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建异常值图表"""
        try:
            return {
                'type': 'outlier_chart',
                'title': outlier_data.get('title', '异常值检测'),
                'message': '异常值图表功能待实现'
            }

        except Exception as e:
            system_logger.error("异常值图表创建失败", error=e)
            return {
                'type': 'outlier_chart',
                'title': '异常值检测',
                'error': str(e)
            }

    def _generate_metric_cards_html(self, metrics: Dict[str, Any]) -> str:
        """生成指标卡片的HTML"""
        html = f"""<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>核心指标概览</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .metric-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 15px;
            padding: 2rem;
            margin-bottom: 1rem;
            box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
            transition: transform 0.3s ease;
        }}
        .metric-card:hover {{
            transform: translateY(-5px);
        }}
        .metric-value {{
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }}
        .metric-label {{
            font-size: 1.1rem;
            opacity: 0.9;
        }}
        .metric-change {{
            font-size: 0.9rem;
            margin-top: 0.5rem;
        }}
        .positive {{ color: #2ecc71; }}
        .negative {{ color: #e74c3c; }}
    </style>
</head>
<body>
    <div class="container-fluid py-4">
        <div class="row mb-4">
            <div class="col-12">
                <h1 class="text-center">📊 核心指标概览</h1>
                <p class="text-center text-muted">生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
        </div>

        <div class="row">
"""

        # 添加指标卡片
        for key, value in metrics.items():
            if isinstance(value, dict) and 'current' in value:
                current = value['current']
                change_rate = value.get('change_rate', 0)

                # 格式化数值
                if isinstance(current, (int, float)):
                    if current > 1000000:
                        formatted_value = ".1f"{current/1000000}M"
                    elif current > 1000:
                        formatted_value = ".1f"{current/1000}K"
                    else:
                        formatted_value = str(current)
                else:
                    formatted_value = str(current)

                # 变化指示器
                change_class = 'positive' if change_rate > 0 else 'negative'
                change_icon = '↗️' if change_rate > 0 else '↘️'

                html += f'''
            <div class="col-md-3">
                <div class="metric-card text-center">
                    <div class="metric-value">{formatted_value}</div>
                    <div class="metric-label">{key.upper()}</div>
                    <div class="metric-change {change_class}">
                        {change_icon} {abs(change_rate):.1f}%
                    </div>
                </div>
            </div>'''

        html += """
        </div>
    </div>
</body>
</html>"""

        return html

    def _create_interactive_components(self, charts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """创建交互式组件"""
        components = []

        try:
            # 为每个图表创建交互式版本
            for chart in charts:
                if chart.get('format') == 'html':
                    interactive_chart = {
                        'type': 'interactive_chart',
                        'title': chart.get('title', '交互式图表'),
                        'source_file': chart.get('file_path'),
                        'interactive_url': chart.get('file_url'),
                        'features': ['hover', 'click', 'zoom', 'filter']
                    }
                    components.append(interactive_chart)

        except Exception as e:
            system_logger.error("交互式组件创建失败", error=e)

        return components

    def _preprocess_data(self, data: Any) -> Dict[str, Any]:
        """预处理数据"""
        try:
            import pandas as pd

            if hasattr(data, 'to_dict'):
                return data.to_dict()
            elif isinstance(data, dict):
                return data
            elif isinstance(data, (list, tuple)):
                return {'data': data}
            else:
                return {'value': str(data)}

        except Exception as e:
            system_logger.error("数据预处理失败", error=e)
            return {'error': str(e)}

    def _generate_data_summary(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """生成数据摘要"""
        summary = {
            'total_items': 0,
            'data_types': set(),
            'has_metrics': False,
            'has_trends': False,
            'has_distributions': False
        }

        try:
            if isinstance(data, dict):
                summary['total_items'] = len(data)

                for key, value in data.items():
                    if isinstance(value, dict):
                        if 'current' in value and 'change_rate' in value:
                            summary['has_metrics'] = True
                        elif key.lower() in ['trend', 'trends']:
                            summary['has_trends'] = True
                        elif key.lower() in ['distribution', 'distributions']:
                            summary['has_distributions'] = True

        except Exception as e:
            system_logger.error("数据摘要生成失败", error=e)

        return summary

    def cleanup_old_charts(self, days: int = 30):
        """
        清理旧的图表文件

        Args:
            days: 保留天数
        """
        try:
            cutoff_date = datetime.now().timestamp() - (days * 24 * 60 * 60)

            for file_path in self.output_dir.glob("*"):
                if file_path.is_file():
                    if file_path.stat().st_mtime < cutoff_date:
                        file_path.unlink()
                        system_logger.info("清理旧图表文件", file_path=str(file_path))

        except Exception as e:
            system_logger.error("清理旧图表文件失败", error=e)

    def get_visualization_stats(self) -> Dict[str, Any]:
        """获取可视化统计信息"""
        stats = {
            'total_charts': len(self.generated_charts),
            'output_directory': str(self.output_dir),
            'available_themes': ['modern', 'classic', 'dark', 'light'],
            'supported_formats': ['html', 'png', 'svg', 'pdf', 'txt'],
            'charts_by_type': {}
        }

        # 统计图表类型
        for chart in self.generated_charts:
            chart_type = chart.get('type', 'unknown')
            stats['charts_by_type'][chart_type] = stats['charts_by_type'].get(chart_type, 0) + 1

        return stats
