import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Union
import pandas as pd
import jinja2
from weasyprint import HTML
import markdown
import plotly.graph_objects as go
import plotly.express as px

class ReportGenerator:
    """报告生成器核心类，负责生成和导出报告"""
    
    def __init__(self, template_dir: str = 'src/templates/reports'):
        self.logger = logging.getLogger(__name__)
        self.template_dir = template_dir
        self.template_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(template_dir)
        )
        
    def generate_report(self, 
                       report_data: Dict,
                       template_name: str,
                       output_format: str = 'html',
                       output_path: Optional[str] = None) -> str:
        """
        生成报告
        
        Args:
            report_data: 报告数据
            template_name: 模板名称
            output_format: 输出格式 (html/pdf/md/json)
            output_path: 输出路径
            
        Returns:
            str: 报告文件路径
        """
        try:
            # 加载模板
            template = self.template_env.get_template(f"{template_name}.html")
            
            # 渲染模板
            html_content = template.render(**report_data)
            
            # 生成输出文件名
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            if not output_path:
                output_path = os.path.join('output', 'reports')
            os.makedirs(output_path, exist_ok=True)
            
            output_file = os.path.join(
                output_path,
                f"report_{timestamp}.{output_format}"
            )
            
            # 根据格式导出
            if output_format == 'html':
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(html_content)
            elif output_format == 'pdf':
                HTML(string=html_content).write_pdf(output_file)
            elif output_format == 'md':
                self._export_to_markdown(html_content, output_file)
            elif output_format == 'json':
                self._export_to_json(report_data, output_file)
            else:
                raise ValueError(f"不支持的输出格式: {output_format}")
                
            self.logger.info(f"报告生成成功: {output_file}")
            return output_file
            
        except Exception as e:
            self.logger.error(f"报告生成失败: {str(e)}")
            raise
            
    def create_executive_summary(self, report_data: Dict) -> Dict:
        """
        创建执行摘要
        
        Args:
            report_data: 报告数据
            
        Returns:
            Dict: 执行摘要数据
        """
        try:
            summary = {
                'title': report_data.get('title', '报告摘要'),
                'generated_at': datetime.now().isoformat(),
                'key_metrics': {},
                'findings': [],
                'recommendations': []
            }
            
            # 提取关键指标
            if 'analysis_results' in report_data:
                results = report_data['analysis_results']
                
                # 描述性统计摘要
                if 'descriptive' in results:
                    desc_stats = results['descriptive']
                    for col, stats in desc_stats.get('numeric_stats', {}).items():
                        summary['key_metrics'][col] = {
                            'mean': stats['mean'],
                            'trend': stats.get('trend', 'stable')
                        }
                        
                # 相关性分析摘要
                if 'correlation' in results:
                    corr = results['correlation']
                    strong_corr = corr.get('strong_correlations', [])
                    if strong_corr:
                        summary['findings'].append({
                            'type': 'correlation',
                            'description': f"发现{len(strong_corr)}个强相关性关系"
                        })
                        
                # 趋势分析摘要
                if 'trend' in results:
                    trend = results['trend']
                    for col, stats in trend.get('trend_analysis', {}).items():
                        if stats['trend_direction'] != 'stable':
                            summary['findings'].append({
                                'type': 'trend',
                                'description': f"{col}呈现{stats['trend_direction']}趋势"
                            })
                            
                # 预测分析摘要
                if 'forecast' in results:
                    forecast = results['forecast']
                    for col, stats in forecast.get('forecast_analysis', {}).items():
                        if stats['model_metrics']['r2_score'] > 0.7:
                            summary['findings'].append({
                                'type': 'forecast',
                                'description': f"{col}的预测模型表现良好"
                            })
                            
            # 生成建议
            for finding in summary['findings']:
                if finding['type'] == 'correlation':
                    summary['recommendations'].append(
                        "建议进一步分析强相关性变量之间的关系"
                    )
                elif finding['type'] == 'trend':
                    summary['recommendations'].append(
                        "建议制定相应的应对策略"
                    )
                elif finding['type'] == 'forecast':
                    summary['recommendations'].append(
                        "建议将预测结果纳入决策考虑"
                    )
                    
            return summary
            
        except Exception as e:
            self.logger.error(f"创建执行摘要失败: {str(e)}")
            raise
            
    def create_visualization_report(self, 
                                  data: pd.DataFrame,
                                  template_name: str = 'visualization',
                                  output_format: str = 'html') -> str:
        """
        创建可视化报告
        
        Args:
            data: 数据框
            template_name: 模板名称
            output_format: 输出格式
            
        Returns:
            str: 报告文件路径
        """
        try:
            # 创建图表
            charts = {}
            
            # 数值型列的分布图
            numeric_cols = data.select_dtypes(include=['number']).columns
            for col in numeric_cols:
                fig = px.histogram(data, x=col, title=f"{col}分布")
                charts[f"{col}_distribution"] = fig.to_html(full_html=False)
                
            # 相关性热力图
            if len(numeric_cols) > 1:
                corr_matrix = data[numeric_cols].corr()
                fig = go.Figure(data=go.Heatmap(
                    z=corr_matrix,
                    x=corr_matrix.columns,
                    y=corr_matrix.columns
                ))
                charts['correlation_heatmap'] = fig.to_html(full_html=False)
                
            # 时间序列图
            time_cols = [col for col in data.columns if 'date' in col.lower() or 'time' in col.lower()]
            if time_cols:
                time_col = time_cols[0]
                for col in numeric_cols:
                    fig = px.line(data, x=time_col, y=col, title=f"{col}时间序列")
                    charts[f"{col}_time_series"] = fig.to_html(full_html=False)
                    
            # 生成报告
            report_data = {
                'title': '数据可视化报告',
                'generated_at': datetime.now().isoformat(),
                'charts': charts,
                'data_summary': {
                    'total_rows': len(data),
                    'total_columns': len(data.columns),
                    'numeric_columns': len(numeric_cols),
                    'categorical_columns': len(data.select_dtypes(include=['object']).columns)
                }
            }
            
            return self.generate_report(
                report_data,
                template_name,
                output_format
            )
            
        except Exception as e:
            self.logger.error(f"创建可视化报告失败: {str(e)}")
            raise
            
    def create_analysis_report(self,
                             analysis_results: Dict,
                             template_name: str = 'analysis',
                             output_format: str = 'html') -> str:
        """
        创建分析报告
        
        Args:
            analysis_results: 分析结果
            template_name: 模板名称
            output_format: 输出格式
            
        Returns:
            str: 报告文件路径
        """
        try:
            # 创建执行摘要
            summary = self.create_executive_summary({
                'analysis_results': analysis_results
            })
            
            # 准备报告数据
            report_data = {
                'title': '数据分析报告',
                'generated_at': datetime.now().isoformat(),
                'summary': summary,
                'analysis_results': analysis_results
            }
            
            # 生成报告
            return self.generate_report(
                report_data,
                template_name,
                output_format
            )
            
        except Exception as e:
            self.logger.error(f"创建分析报告失败: {str(e)}")
            raise
            
    def _export_to_markdown(self, html_content: str, output_file: str) -> None:
        """导出为Markdown格式"""
        try:
            # 将HTML转换为Markdown
            md_content = markdown.markdown(html_content)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(md_content)
                
        except Exception as e:
            self.logger.error(f"导出Markdown失败: {str(e)}")
            raise
            
    def _export_to_json(self, data: Dict, output_file: str) -> None:
        """导出为JSON格式"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            self.logger.error(f"导出JSON失败: {str(e)}")
            raise 