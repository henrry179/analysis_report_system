#!/usr/bin/env python3
"""
增强版图表生成器
支持更多图表类型和交互式可视化
"""

import os
import json
import math
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from pathlib import Path

# 条件导入
try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from matplotlib.patches import Rectangle, Circle
    import seaborn as sns
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    import plotly.offline as pyo
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

class EnhancedChartGenerator:
    """增强版图表生成器"""
    
    def __init__(self):
        self.chart_configs = {
            'style': 'modern',
            'color_palette': ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c'],
            'figure_size': (12, 8),
            'dpi': 300
        }
        self.generated_charts = []
        
    def create_advanced_dashboard(self, data: Dict[str, Any], output_dir: str = "output/charts") -> Dict[str, Any]:
        """创建高级仪表板"""
        dashboard_result = {
            'charts_created': [],
            'dashboard_file': '',
            'interactive_charts': [],
            'summary': {}
        }
        
        os.makedirs(output_dir, exist_ok=True)
        
        if PLOTLY_AVAILABLE:
            # 创建交互式仪表板
            dashboard_result = self._create_plotly_dashboard(data, output_dir)
        elif MATPLOTLIB_AVAILABLE:
            # 创建静态高级仪表板
            dashboard_result = self._create_matplotlib_dashboard(data, output_dir)
        else:
            # 创建ASCII艺术仪表板
            dashboard_result = self._create_ascii_dashboard(data, output_dir)
        
        return dashboard_result
    
    def _create_plotly_dashboard(self, data: Dict[str, Any], output_dir: str) -> Dict[str, Any]:
        """创建Plotly交互式仪表板"""
        # 创建子图布局
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=('GMV趋势分析', 'DAU变化图', '品类分布', '区域对比', '关键指标', '预测分析'),
            specs=[[{"secondary_y": True}, {"secondary_y": False}],
                   [{"type": "xy"}, {"type": "xy"}],
                   [{"type": "indicator"}, {"type": "xy"}]]
        )
        
        # 1. GMV趋势分析（左上）
        gmv_data = data.get('gmv_trend', {})
        if gmv_data:
            fig.add_trace(
                go.Scatter(
                    x=list(gmv_data.keys()),
                    y=list(gmv_data.values()),
                    mode='lines+markers',
                    name='GMV趋势',
                    line=dict(color='#3498db', width=3),
                    marker=dict(size=8)
                ),
                row=1, col=1
            )
        
        # 2. DAU变化图（右上）
        dau_data = data.get('dau_trend', {})
        if dau_data:
            fig.add_trace(
                go.Bar(
                    x=list(dau_data.keys()),
                    y=list(dau_data.values()),
                    name='DAU',
                    marker_color='#2ecc71'
                ),
                row=1, col=2
            )
        
        # 3. 品类分布（左中）
        category_data = data.get('category_analysis', {})
        if category_data:
            fig.add_trace(
                go.Pie(
                    labels=list(category_data.keys()),
                    values=list(category_data.values()),
                    name="品类分布",
                    hole=0.4
                ),
                row=2, col=1
            )
        
        # 4. 区域对比（右中）
        region_data = data.get('region_analysis', {})
        if region_data:
            fig.add_trace(
                go.Bar(
                    x=list(region_data.keys()),
                    y=list(region_data.values()),
                    name='区域GMV',
                    marker_color='#f39c12'
                ),
                row=2, col=2
            )
        
        # 5. 关键指标（左下）
        total_gmv = sum(gmv_data.values()) if gmv_data else 8500000
        fig.add_trace(
            go.Indicator(
                mode="gauge+number+delta",
                value=total_gmv,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "总GMV"},
                delta={'reference': 8000000},
                gauge={
                    'axis': {'range': [None, 10000000]},
                    'bar': {'color': "#3498db"},
                    'steps': [
                        {'range': [0, 5000000], 'color': "lightgray"},
                        {'range': [5000000, 8000000], 'color': "yellow"},
                        {'range': [8000000, 10000000], 'color': "green"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75, 'value': 9000000
                    }
                }
            ),
            row=3, col=1
        )
        
        # 6. 预测分析（右下）
        forecast_data = data.get('forecast', {})
        if forecast_data:
            dates = list(forecast_data.keys())
            actual = [forecast_data[d].get('actual', 0) for d in dates]
            predicted = [forecast_data[d].get('predicted', 0) for d in dates]
            
            fig.add_trace(
                go.Scatter(x=dates, y=actual, mode='lines', name='实际值', line=dict(color='#3498db')),
                row=3, col=2
            )
            fig.add_trace(
                go.Scatter(x=dates, y=predicted, mode='lines', name='预测值', 
                          line=dict(color='#e74c3c', dash='dash')),
                row=3, col=2
            )
        
        # 更新布局
        fig.update_layout(
            height=1200,
            title_text="业务分析综合仪表板",
            title_x=0.5,
            title_font_size=24,
            showlegend=True,
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        
        # 保存交互式HTML
        dashboard_file = os.path.join(output_dir, f"interactive_dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")
        pyo.plot(fig, filename=dashboard_file, auto_open=False)
        
        return {
            'charts_created': ['interactive_dashboard'],
            'dashboard_file': dashboard_file,
            'interactive_charts': [dashboard_file],
            'summary': {
                'chart_type': 'interactive_plotly',
                'total_charts': 6,
                'file_size': f"{os.path.getsize(dashboard_file) / 1024:.1f} KB" if os.path.exists(dashboard_file) else '0 KB'
            }
        }
    
    def _create_matplotlib_dashboard(self, data: Dict[str, Any], output_dir: str) -> Dict[str, Any]:
        """创建Matplotlib高级仪表板"""
        # 设置样式
        plt.style.use('seaborn-v0_8' if 'seaborn-v0_8' in plt.style.available else 'default')
        
        # 创建图形
        fig = plt.figure(figsize=(16, 12))
        fig.suptitle('业务分析综合仪表板', fontsize=24, fontweight='bold', y=0.95)
        
        # 1. GMV趋势分析 (2x3网格的左上)
        ax1 = plt.subplot(3, 3, (1, 2))
        gmv_data = data.get('gmv_trend', {'2024-01': 800000, '2024-02': 850000, '2024-03': 820000, '2024-04': 880000})
        dates = list(gmv_data.keys())
        values = list(gmv_data.values())
        
        ax1.plot(dates, values, marker='o', linewidth=3, markersize=8, color=self.chart_configs['color_palette'][0])
        ax1.set_title('GMV趋势分析', fontsize=16, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.tick_params(axis='x', rotation=45)
        
        # 添加趋势线
        if len(values) > 1:
            z = np.polyfit(range(len(values)), values, 1)
            p = np.poly1d(z)
            ax1.plot(dates, p(range(len(values))), "--", alpha=0.8, color=self.chart_configs['color_palette'][1])
        
        # 2. DAU分布 (右上)
        ax2 = plt.subplot(3, 3, 3)
        dau_data = data.get('dau_trend', {'北京': 1200, '上海': 1100, '广州': 950, '深圳': 1050})
        
        ax2.bar(dau_data.keys(), dau_data.values(), color=self.chart_configs['color_palette'][2], alpha=0.8)
        ax2.set_title('DAU区域分布', fontsize=16, fontweight='bold')
        ax2.tick_params(axis='x', rotation=45)
        
        # 3. 品类分析饼图 (中左)
        ax3 = plt.subplot(3, 3, 4)
        category_data = data.get('category_analysis', {'电子产品': 35, '服装': 25, '家居': 20, '其他': 20})
        
        wedges, texts, autotexts = ax3.pie(
            category_data.values(), 
            labels=category_data.keys(),
            autopct='%1.1f%%',
            colors=self.chart_configs['color_palette'][:len(category_data)],
            explode=[0.05 if max(category_data.values()) == v else 0 for v in category_data.values()]
        )
        ax3.set_title('品类分析', fontsize=16, fontweight='bold')
        
        # 4. 热力图 (中中)
        ax4 = plt.subplot(3, 3, 5)
        
        # 创建模拟热力图数据
        heatmap_data = [
            [0.8, 0.9, 0.7, 0.6],
            [0.9, 0.8, 0.8, 0.7],
            [0.7, 0.8, 0.9, 0.8],
            [0.6, 0.7, 0.8, 0.9]
        ]
        
        im = ax4.imshow(heatmap_data, cmap='YlOrRd', aspect='auto')
        ax4.set_title('区域-品类热力图', fontsize=16, fontweight='bold')
        ax4.set_xticks(range(4))
        ax4.set_yticks(range(4))
        ax4.set_xticklabels(['电子', '服装', '家居', '其他'])
        ax4.set_yticklabels(['北京', '上海', '广州', '深圳'])
        
        # 添加数值标注
        for i in range(4):
            for j in range(4):
                ax4.text(j, i, f'{heatmap_data[i][j]:.1f}', ha="center", va="center", color="black")
        
        # 5. 预测分析 (中右)
        ax5 = plt.subplot(3, 3, 6)
        
        forecast_dates = ['今天', '明天', '后天', '第4天', '第5天']
        actual_values = [880000, 870000, 890000, None, None]
        predicted_values = [880000, 870000, 890000, 895000, 902000]
        
        ax5.plot(forecast_dates[:3], actual_values[:3], marker='o', label='实际值', 
                linewidth=2, color=self.chart_configs['color_palette'][0])
        ax5.plot(forecast_dates, predicted_values, marker='s', label='预测值', 
                linewidth=2, linestyle='--', color=self.chart_configs['color_palette'][1])
        
        ax5.set_title('GMV预测分析', fontsize=16, fontweight='bold')
        ax5.legend()
        ax5.grid(True, alpha=0.3)
        ax5.tick_params(axis='x', rotation=45)
        
        # 6. 关键指标仪表 (下排)
        ax6 = plt.subplot(3, 3, (7, 9))
        
        # 创建关键指标卡片
        metrics = [
            {'name': '总GMV', 'value': '850万', 'change': '+12.5%', 'color': '#2ecc71'},
            {'name': '总DAU', 'value': '4,300', 'change': '+8.3%', 'color': '#3498db'},
            {'name': '转化率', 'value': '3.2%', 'change': '+0.5pp', 'color': '#f39c12'},
            {'name': '客单价', 'value': '1,977', 'change': '+15.2%', 'color': '#9b59b6'}
        ]
        
        ax6.axis('off')
        
        for i, metric in enumerate(metrics):
            x = i * 0.25
            y = 0.5
            
            # 创建指标卡片
            rect = Rectangle((x, y-0.3), 0.2, 0.6, linewidth=2, 
                           edgecolor=metric['color'], facecolor='white', alpha=0.9)
            ax6.add_patch(rect)
            
            # 添加文本
            ax6.text(x+0.1, y+0.15, metric['name'], ha='center', va='center', 
                    fontsize=12, fontweight='bold')
            ax6.text(x+0.1, y, metric['value'], ha='center', va='center', 
                    fontsize=16, fontweight='bold', color=metric['color'])
            ax6.text(x+0.1, y-0.15, metric['change'], ha='center', va='center', 
                    fontsize=10, color=metric['color'])
        
        ax6.set_xlim(-0.05, 1.05)
        ax6.set_ylim(0, 1)
        ax6.set_title('关键业务指标', fontsize=16, fontweight='bold', y=0.9)
        
        # 调整布局
        plt.tight_layout()
        plt.subplots_adjust(top=0.92, hspace=0.3, wspace=0.3)
        
        # 保存图片
        dashboard_file = os.path.join(output_dir, f"advanced_dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        plt.savefig(dashboard_file, dpi=self.chart_configs['dpi'], bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        plt.close()
        
        return {
            'charts_created': ['advanced_dashboard'],
            'dashboard_file': dashboard_file,
            'interactive_charts': [],
            'summary': {
                'chart_type': 'matplotlib_advanced',
                'total_charts': 6,
                'file_size': f"{os.path.getsize(dashboard_file) / 1024:.1f} KB" if os.path.exists(dashboard_file) else '0 KB'
            }
        }
    
    def _create_ascii_dashboard(self, data: Dict[str, Any], output_dir: str) -> Dict[str, Any]:
        """创建ASCII艺术仪表板"""
        dashboard_content = self._generate_advanced_ascii_dashboard(data)
        
        dashboard_file = os.path.join(output_dir, f"ascii_dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        
        with open(dashboard_file, 'w', encoding='utf-8') as f:
            f.write(dashboard_content)
        
        return {
            'charts_created': ['ascii_dashboard'],
            'dashboard_file': dashboard_file,
            'interactive_charts': [],
            'summary': {
                'chart_type': 'ascii_advanced',
                'total_charts': 6,
                'file_size': f"{os.path.getsize(dashboard_file) / 1024:.1f} KB"
            }
        }
    
    def _generate_advanced_ascii_dashboard(self, data: Dict[str, Any]) -> str:
        """生成高级ASCII仪表板"""
        content = []
        
        # 标题
        content.append("╔" + "═" * 98 + "╗")
        content.append("║" + " " * 30 + "🚀 业务分析综合仪表板 🚀" + " " * 30 + "║")
        content.append("║" + " " * 98 + "║")
        content.append("║" + f"📅 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}" + " " * 54 + "║")
        content.append("╚" + "═" * 98 + "╝")
        content.append("")
        
        # 关键指标概览
        content.append("┌─ 📊 关键业务指标概览 ─" + "─" * 65 + "┐")
        metrics = [
            ("📈 总GMV", "850万元", "+12.5%", "🟢"),
            ("👥 总DAU", "4,300人", "+8.3%", "🔵"),
            ("💰 转化率", "3.2%", "+0.5pp", "🟡"),
            ("🛒 客单价", "¥1,977", "+15.2%", "🟣")
        ]
        
        for i in range(0, len(metrics), 2):
            line = "│ "
            for j in range(2):
                if i + j < len(metrics):
                    metric = metrics[i + j]
                    line += f"{metric[3]} {metric[0]}: {metric[1]} ({metric[2]})"
                    line += " " * (45 - len(f"{metric[0]}: {metric[1]} ({metric[2]})"))
                else:
                    line += " " * 45
            line += " │"
            content.append(line)
        
        content.append("└" + "─" * 90 + "┘")
        content.append("")
        
        # GMV趋势图
        content.append("┌─ 📈 GMV趋势分析 ─" + "─" * 68 + "┐")
        
        gmv_data = data.get('gmv_trend', {'2024-01': 800000, '2024-02': 850000, '2024-03': 820000, '2024-04': 880000})
        max_val = max(gmv_data.values())
        min_val = min(gmv_data.values())
        
        for date, value in gmv_data.items():
            # 计算条形长度
            bar_length = int((value - min_val) / (max_val - min_val) * 50) if max_val != min_val else 25
            bar = "█" * bar_length + "░" * (50 - bar_length)
            content.append(f"│ {date}: │{bar}│ {value:,}元 │")
        
        content.append("└" + "─" * 90 + "┘")
        content.append("")
        
        # 品类分析饼图 (ASCII版本)
        content.append("┌─ 🏷️ 品类分析 ─" + "─" * 73 + "┐")
        
        category_data = data.get('category_analysis', {'电子产品': 35, '服装': 25, '家居': 20, '其他': 20})
        total = sum(category_data.values())
        
        for category, percentage in category_data.items():
            # 创建ASCII饼图段
            pie_length = int(percentage / total * 40) if total > 0 else 10
            pie_segment = "●" * pie_length + "○" * (40 - pie_length)
            content.append(f"│ {category:8s}: │{pie_segment}│ {percentage}% │")
        
        content.append("└" + "─" * 90 + "┘")
        content.append("")
        
        # 区域对比
        content.append("┌─ 🗺️ 区域业绩对比 ─" + "─" * 67 + "┐")
        
        region_data = data.get('region_analysis', {'北京': 1200, '上海': 1100, '广州': 950, '深圳': 1050})
        max_region_val = max(region_data.values())
        
        for region, value in region_data.items():
            bar_length = int(value / max_region_val * 40)
            bar = "▓" * bar_length + "░" * (40 - bar_length)
            content.append(f"│ {region:4s}: │{bar}│ {value:,}万元 │")
        
        content.append("└" + "─" * 90 + "┘")
        content.append("")
        
        # 预测分析
        content.append("┌─ 🔮 预测分析 ─" + "─" * 72 + "┐")
        
        forecast_data = [
            ("今天", 880000, "实际"),
            ("明天", 875000, "预测"),
            ("后天", 890000, "预测"),
            ("第4天", 895000, "预测"),
            ("第5天", 902000, "预测")
        ]
        
        for day, value, type_str in forecast_data:
            symbol = "📊" if type_str == "实际" else "🔮"
            content.append(f"│ {symbol} {day:6s}: {value:,}元 ({type_str}) " + " " * 30 + "│")
        
        content.append("└" + "─" * 90 + "┘")
        content.append("")
        
        # 异常检测
        content.append("┌─ 🚨 异常检测与警报 ─" + "─" * 64 + "┐")
        
        alerts = [
            ("⚠️", "GMV环比增长超预期", "需关注原因分析"),
            ("✅", "DAU增长稳定", "表现良好"),
            ("📢", "转化率有提升空间", "建议优化"),
            ("🎯", "客单价增长显著", "策略有效")
        ]
        
        for icon, alert, desc in alerts:
            content.append(f"│ {icon} {alert:20s} - {desc:30s} │")
        
        content.append("└" + "─" * 90 + "┘")
        content.append("")
        
        # 建议和行动项
        content.append("┌─ 💡 智能建议 ─" + "─" * 70 + "┐")
        
        recommendations = [
            "🎯 继续加强电子产品类目的推广力度",
            "📊 关注广州地区的业绩波动情况",
            "🔄 优化转化流程以提升整体转化率",
            "💰 研究客单价上升的成功因素并复制推广"
        ]
        
        for i, rec in enumerate(recommendations, 1):
            content.append(f"│ {i}. {rec:70s} │")
        
        content.append("└" + "─" * 90 + "┘")
        content.append("")
        
        # 页脚
        content.append("╔" + "═" * 98 + "╗")
        content.append("║" + " " * 25 + "📈 数据驱动决策，智能分析未来 📈" + " " * 25 + "║")
        content.append("╚" + "═" * 98 + "╝")
        
        return "\n".join(content)
    
    def create_specialized_charts(self, data: Dict[str, Any], chart_types: List[str], output_dir: str = "output/charts") -> Dict[str, Any]:
        """创建专业图表"""
        chart_results = {
            'charts_created': [],
            'files_generated': [],
            'chart_summaries': {}
        }
        
        os.makedirs(output_dir, exist_ok=True)
        
        for chart_type in chart_types:
            try:
                if chart_type == 'correlation_heatmap':
                    result = self._create_correlation_heatmap(data, output_dir)
                elif chart_type == 'cohort_heatmap':
                    result = self._create_cohort_heatmap(data, output_dir)
                elif chart_type == 'funnel_chart':
                    result = self._create_funnel_chart(data, output_dir)
                elif chart_type == 'sankey_diagram':
                    result = self._create_sankey_diagram(data, output_dir)
                elif chart_type == 'radar_chart':
                    result = self._create_radar_chart(data, output_dir)
                elif chart_type == 'waterfall_chart':
                    result = self._create_waterfall_chart(data, output_dir)
                else:
                    continue
                    
                chart_results['charts_created'].append(chart_type)
                chart_results['files_generated'].extend(result.get('files', []))
                chart_results['chart_summaries'][chart_type] = result.get('summary', {})
                
            except Exception as e:
                chart_results['chart_summaries'][chart_type] = {'error': str(e)}
        
        return chart_results
    
    def _create_correlation_heatmap(self, data: Dict[str, Any], output_dir: str) -> Dict[str, Any]:
        """创建相关性热力图"""
        if MATPLOTLIB_AVAILABLE:
            return self._matplotlib_correlation_heatmap(data, output_dir)
        else:
            return self._ascii_correlation_heatmap(data, output_dir)
    
    def _matplotlib_correlation_heatmap(self, data: Dict[str, Any], output_dir: str) -> Dict[str, Any]:
        """Matplotlib相关性热力图"""
        # 模拟相关性数据
        features = ['GMV', 'DAU', '转化率', '客单价', '频次']
        correlation_matrix = [
            [1.00, 0.85, 0.62, 0.45, 0.73],
            [0.85, 1.00, 0.58, 0.42, 0.68],
            [0.62, 0.58, 1.00, 0.35, 0.51],
            [0.45, 0.42, 0.35, 1.00, 0.28],
            [0.73, 0.68, 0.51, 0.28, 1.00]
        ]
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        im = ax.imshow(correlation_matrix, cmap='RdYlBu_r', aspect='auto', vmin=-1, vmax=1)
        
        # 设置标签
        ax.set_xticks(range(len(features)))
        ax.set_yticks(range(len(features)))
        ax.set_xticklabels(features)
        ax.set_yticklabels(features)
        
        # 添加数值标注
        for i in range(len(features)):
            for j in range(len(features)):
                text = ax.text(j, i, f'{correlation_matrix[i][j]:.2f}',
                             ha="center", va="center", color="black", fontweight='bold')
        
        ax.set_title('业务指标相关性分析', fontsize=16, fontweight='bold', pad=20)
        
        # 添加颜色条
        cbar = plt.colorbar(im, ax=ax, shrink=0.8)
        cbar.set_label('相关系数', rotation=270, labelpad=20)
        
        plt.tight_layout()
        
        filename = os.path.join(output_dir, f"correlation_heatmap_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        return {
            'files': [filename],
            'summary': {'type': 'correlation_heatmap', 'features_count': len(features)}
        }
    
    def _ascii_correlation_heatmap(self, data: Dict[str, Any], output_dir: str) -> Dict[str, Any]:
        """ASCII相关性热力图"""
        features = ['GMV', 'DAU', '转化率', '客单价', '频次']
        correlation_matrix = [
            [1.00, 0.85, 0.62, 0.45, 0.73],
            [0.85, 1.00, 0.58, 0.42, 0.68],
            [0.62, 0.58, 1.00, 0.35, 0.51],
            [0.45, 0.42, 0.35, 1.00, 0.28],
            [0.73, 0.68, 0.51, 0.28, 1.00]
        ]
        
        content = []
        content.append("┌─ 🔥 业务指标相关性热力图 ─" + "─" * 50 + "┐")
        content.append("│" + " " * 76 + "│")
        
        # 表头
        header = "│     "
        for feature in features:
            header += f"{feature:>8s}"
        header += "    │"
        content.append(header)
        
        content.append("│" + "─" * 76 + "│")
        
        # 数据行
        for i, row_feature in enumerate(features):
            line = f"│{row_feature:>5s}"
            for j, corr_val in enumerate(correlation_matrix[i]):
                # 使用不同符号表示相关性强度
                if corr_val >= 0.8:
                    symbol = "██"
                elif corr_val >= 0.6:
                    symbol = "▓▓"
                elif corr_val >= 0.4:
                    symbol = "▒▒"
                elif corr_val >= 0.2:
                    symbol = "░░"
                else:
                    symbol = "  "
                
                line += f"{symbol:>8s}"
            line += "    │"
            content.append(line)
        
        content.append("│" + " " * 76 + "│")
        content.append("│ 图例: ██ 强相关(≥0.8)  ▓▓ 中等(≥0.6)  ▒▒ 弱相关(≥0.4)  ░░ 微弱(≥0.2)" + " " * 8 + "│")
        content.append("└" + "─" * 76 + "┘")
        
        filename = os.path.join(output_dir, f"correlation_heatmap_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("\n".join(content))
        
        return {
            'files': [filename],
            'summary': {'type': 'ascii_correlation_heatmap', 'features_count': len(features)}
        }
    
    def _create_funnel_chart(self, data: Dict[str, Any], output_dir: str) -> Dict[str, Any]:
        """创建漏斗图"""
        if MATPLOTLIB_AVAILABLE:
            return self._matplotlib_funnel_chart(data, output_dir)
        else:
            return self._ascii_funnel_chart(data, output_dir)
    
    def _ascii_funnel_chart(self, data: Dict[str, Any], output_dir: str) -> Dict[str, Any]:
        """ASCII漏斗图"""
        funnel_data = data.get('funnel_data', {
            '访问': 10000,
            '浏览商品': 7500,
            '加入购物车': 3000,
            '下单': 1200,
            '支付完成': 950
        })
        
        max_value = max(funnel_data.values())
        content = []
        
        content.append("┌─ 🔽 用户转化漏斗分析 ─" + "─" * 55 + "┐")
        content.append("│" + " " * 76 + "│")
        
        for i, (stage, value) in enumerate(funnel_data.items()):
            # 计算漏斗宽度
            width = int((value / max_value) * 50)
            padding = (50 - width) // 2
            
            funnel_bar = " " * padding + "█" * width + " " * (50 - width - padding)
            percentage = (value / max_value) * 100
            
            content.append(f"│ {stage:10s} │{funnel_bar}│ {value:,} ({percentage:.1f}%) │")
            
            # 添加转化率
            if i > 0:
                prev_value = list(funnel_data.values())[i-1]
                conversion_rate = (value / prev_value) * 100
                content.append(f"│{' ':12s}└─ 转化率: {conversion_rate:.1f}%{' ':35s}│")
        
        content.append("│" + " " * 76 + "│")
        content.append("└" + "─" * 76 + "┘")
        
        filename = os.path.join(output_dir, f"funnel_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("\n".join(content))
        
        return {
            'files': [filename],
            'summary': {'type': 'ascii_funnel', 'stages_count': len(funnel_data)}
        } 