#!/usr/bin/env python3
"""
多行业报告生成器
智能分析多个行业的业务数据并生成综合报告
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

from src.config.settings import settings
from src.utils.logger import system_logger


class MultiIndustryReportGenerator:
    """多行业报告生成器"""
    
    def __init__(self):
        """初始化报告生成器"""
        self.output_dir = str(settings.REPORTS_DIR)
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 行业配置
        self.industries_config = {
            "retail": {
                "name": "零售行业", 
                "icon": "🏪",
                "color": "#e74c3c",
                "description": "零售业务深度分析，包含销售数据、区域分析、品类表现"
            },
            "community": {
                "name": "社区团购", 
                "icon": "🏘️",
                "color": "#3498db",
                "description": "社区团购行业分析，涵盖订单数据、城市覆盖、团长运营"
            },
            "financial": {
                "name": "金融交易", 
                "icon": "💰",
                "color": "#f39c12",
                "description": "金融交易行业分析，包含交易量、风险评估、产品表现"
            },
            "ai_agent": {
                "name": "智能体", 
                "icon": "🤖",
                "color": "#9b59b6",
                "description": "智能体行业分析，展示技术发展、应用场景、市场趋势"
            },
            "cross_industry": {
                "name": "跨行业对比", 
                "icon": "🔄",
                "color": "#2ecc71",
                "description": "跨行业对比分析，多维度比较不同行业发展状况"
            }
        }
    
    def generate_all_industry_reports(self, industries: Optional[List[str]] = None) -> List[str]:
        """生成所有行业报告"""
        if industries is None:
            industries = list(self.industries_config.keys())
        
        system_logger.info("开始生成多行业报告", industries=industries)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        generated_reports = []
        
        for industry_code in industries:
            if industry_code not in self.industries_config:
                system_logger.warning("未知行业类型", industry=industry_code)
                continue
                
            try:
                report_path = self._generate_single_industry_report(industry_code, timestamp)
                generated_reports.append(report_path)
                system_logger.info("行业报告生成成功", industry=industry_code, path=report_path)
            except Exception as e:
                system_logger.error("行业报告生成失败", industry=industry_code, error=e)
        
        # 生成汇总报告
        if len(generated_reports) > 1:
            summary_report = self._generate_summary_report(industries, timestamp)
            generated_reports.append(summary_report)
        
        system_logger.info("多行业报告生成完成", total_reports=len(generated_reports))
        return generated_reports
    
    def _generate_single_industry_report(self, industry_code: str, timestamp: str) -> str:
        """生成单个行业报告"""
        config = self.industries_config[industry_code]
        
        # 模拟数据生成
        mock_data = self._generate_mock_data(industry_code)
        
        html_content = self._create_html_report(industry_code, config, mock_data, timestamp)
        
        filename = f"{industry_code}_report_{timestamp}.html"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return filepath
    
    def _generate_mock_data(self, industry_code: str) -> Dict[str, Any]:
        """生成模拟数据"""
        import random
        
        base_data = {
            "metrics": {
                "core_value": random.randint(1000000, 5000000),
                "growth_rate": round(random.uniform(5.0, 25.0), 1),
                "completion_rate": round(random.uniform(75.0, 95.0), 1),
                "coverage_areas": random.randint(15, 35),
                "business_types": random.randint(8, 15)
            },
            "trend_data": {
                "labels": ["1月", "2月", "3月", "4月", "5月", "6月"],
                "values": [random.randint(100, 300) for _ in range(6)]
            },
            "distribution_data": {
                "labels": ["类别A", "类别B", "类别C", "类别D"],
                "values": [random.randint(20, 40) for _ in range(4)]
            },
            "insights": [
                f"该行业在过去一季度表现{'良好' if random.choice([True, False]) else '稳定'}，主要指标{'稳步增长' if random.choice([True, False]) else '保持稳定'}",
                f"区域分布{'均衡' if random.choice([True, False]) else '集中'}，各区域发展态势{'良好' if random.choice([True, False]) else '有待提升'}",
                f"建议{'继续关注' if random.choice([True, False]) else '重点关注'}市场变化，保持{'增长' if random.choice([True, False]) else '稳定'}态势",
                f"数字化转型程度{'不断提升' if random.choice([True, False]) else '有所进展'}，竞争优势{'明显' if random.choice([True, False]) else '逐步显现'}"
            ]
        }
        
        # 根据行业特点调整数据
        if industry_code == "financial":
            base_data["metrics"]["risk_level"] = round(random.uniform(2.0, 8.0), 1)
        elif industry_code == "ai_agent":
            base_data["metrics"]["ai_adoption"] = round(random.uniform(60.0, 90.0), 1)
        
        return base_data
    
    def _create_html_report(self, industry_code: str, config: Dict, data: Dict, timestamp: str) -> str:
        """创建HTML报告"""
        return f"""<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{config['icon']} {config['name']}分析报告</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        .metric-card {{ 
            background: linear-gradient(135deg, {config['color']} 0%, rgba({self._hex_to_rgb(config['color'])}, 0.8) 100%); 
            color: white; 
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .chart-container {{ height: 300px; margin: 15px 0; }}
        .insight-box {{ 
            background: #f8f9fa; 
            padding: 20px; 
            border-left: 4px solid {config['color']}; 
            margin: 15px 0; 
            border-radius: 5px; 
        }}
        .header-section {{
            background: linear-gradient(135deg, {config['color']} 0%, rgba({self._hex_to_rgb(config['color'])}, 0.7) 100%);
            color: white;
            padding: 2rem;
            border-radius: 10px;
            margin-bottom: 2rem;
        }}
    </style>
</head>
<body>
    <div class="container mt-4">
        <div class="header-section">
            <div class="row">
                <div class="col-12 text-center">
                    <h1>{config['icon']} {config['name']}分析报告</h1>
                    <p class="mb-0">{config['description']}</p>
                    <small>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 报告编号: {industry_code.upper()}_{timestamp}</small>
                </div>
            </div>
        </div>

        <div class="row mb-4">
            <div class="col-md-3">
                <div class="card metric-card text-center">
                    <div class="card-body">
                        <h3>{data['metrics']['core_value']:,}</h3>
                        <p class="mb-0">核心指标</p>
                        <small>+{data['metrics']['growth_rate']}%</small>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card metric-card text-center">
                    <div class="card-body">
                        <h3>{data['metrics']['completion_rate']}%</h3>
                        <p class="mb-0">完成率</p>
                        <small>持续优化</small>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card metric-card text-center">
                    <div class="card-body">
                        <h3>{data['metrics']['coverage_areas']}</h3>
                        <p class="mb-0">覆盖区域</p>
                        <small>全国布局</small>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card metric-card text-center">
                    <div class="card-body">
                        <h3>{data['metrics']['business_types']}</h3>
                        <p class="mb-0">业务类型</p>
                        <small>多元发展</small>
                    </div>
                </div>
            </div>
        </div>

        <div class="row mb-4">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h5>📊 趋势分析</h5>
                    </div>
                    <div class="card-body">
                        <canvas id="trendChart" class="chart-container"></canvas>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h5>📈 分布分析</h5>
                    </div>
                    <div class="card-body">
                        <canvas id="pieChart" class="chart-container"></canvas>
                    </div>
                </div>
            </div>
        </div>

        <div class="row mb-4">
            <div class="col-12">
                <div class="insight-box">
                    <h5>💡 关键洞察</h5>
                    <ul>
                        {''.join([f'<li>{insight}</li>' for insight in data['insights']])}
                    </ul>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-12">
                <div class="alert alert-success">
                    <h4>✅ 报告生成成功!</h4>
                    <p>这是{config['name']}的分析报告。系统已成功收集和分析相关数据，生成了本报告。</p>
                    <hr>
                    <p class="mb-0"><strong>注意:</strong> 这是{settings.APP_VERSION}版本的报告，包含详细的数据分析和可视化图表。</p>
                </div>
            </div>
        </div>
    </div>

    <script>
        // 趋势图表
        const trendCtx = document.getElementById('trendChart').getContext('2d');
        new Chart(trendCtx, {{
            type: 'line',
            data: {{
                labels: {json.dumps(data['trend_data']['labels'])},
                datasets: [{{
                    label: '月度趋势',
                    data: {json.dumps(data['trend_data']['values'])},
                    borderColor: '{config['color']}',
                    backgroundColor: 'rgba({self._hex_to_rgb(config['color'])}, 0.1)',
                    tension: 0.4,
                    fill: true
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    y: {{
                        beginAtZero: true
                    }}
                }}
            }}
        }});

        // 饼图
        const pieCtx = document.getElementById('pieChart').getContext('2d');
        new Chart(pieCtx, {{
            type: 'doughnut',
            data: {{
                labels: {json.dumps(data['distribution_data']['labels'])},
                datasets: [{{
                    data: {json.dumps(data['distribution_data']['values'])},
                    backgroundColor: ['{config['color']}', 'rgba({self._hex_to_rgb(config['color'])}, 0.8)', 'rgba({self._hex_to_rgb(config['color'])}, 0.6)', 'rgba({self._hex_to_rgb(config['color'])}, 0.4)']
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false
            }}
        }});
    </script>
</body>
</html>"""

    def _generate_summary_report(self, industries: List[str], timestamp: str) -> str:
        """生成汇总报告"""
        filename = f"multi_industry_summary_{timestamp}.html"
        filepath = os.path.join(self.output_dir, filename)
        
        html_content = f"""<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔄 多行业综合分析报告</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-4">
        <div class="row mb-4">
            <div class="col-12">
                <div class="alert alert-info">
                    <h2 class="alert-heading">🔄 多行业综合分析报告</h2>
                    <p>本报告汇总了以下行业的分析结果：{', '.join([self.industries_config[ind]['name'] for ind in industries if ind in self.industries_config])}</p>
                    <p class="mb-0">生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 报告编号: SUMMARY_{timestamp}</p>
                </div>
            </div>
        </div>
        
        <div class="row">
            {''.join([f"""
            <div class="col-md-6 mb-3">
                <div class="card">
                    <div class="card-header" style="background-color: {self.industries_config[ind]['color']}; color: white;">
                        <h5 class="mb-0">{self.industries_config[ind]['icon']} {self.industries_config[ind]['name']}</h5>
                    </div>
                    <div class="card-body">
                        <p>{self.industries_config[ind]['description']}</p>
                        <a href="{ind}_report_{timestamp}.html" class="btn btn-primary">查看详细报告</a>
                    </div>
                </div>
            </div>
            """ for ind in industries if ind in self.industries_config])}
        </div>
    </div>
</body>
</html>"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return filepath
    
    def _hex_to_rgb(self, hex_color: str) -> str:
        """将十六进制颜色转换为RGB"""
        hex_color = hex_color.lstrip('#')
        return f"{int(hex_color[0:2], 16)}, {int(hex_color[2:4], 16)}, {int(hex_color[4:6], 16)}" 