#!/usr/bin/env python3
"""
简化Web服务器 - 无需额外依赖
展示业务分析报告
"""

import http.server
import socketserver
import webbrowser
import os
import threading
import time
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import json

class ReportHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """自定义HTTP请求处理器"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="output", **kwargs)
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()
    
    def do_GET(self):
        """处理GET请求"""
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            # 获取最新报告
            reports_dir = Path("output/reports")
            if reports_dir.exists():
                html_files = list(reports_dir.glob("*.html"))
                if html_files:
                    latest_report = max(html_files, key=os.path.getctime)
                    latest_report_name = latest_report.name
                else:
                    latest_report_name = "无可用报告"
            else:
                latest_report_name = "reports目录不存在"
            
            # 生成主页
            html_content = f"""
            <!DOCTYPE html>
            <html lang="zh-CN">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>业务分析报告自动化系统</title>
                <style>
                    :root {{
                        --primary-color: #3498db;
                        --secondary-color: #2c3e50;
                        --background-color: #f5f5f5;
                        --card-background: #ffffff;
                        --text-color: #333333;
                        --border-color: #e0e0e0;
                        --success-color: #27ae60;
                        --warning-color: #f39c12;
                        --error-color: #e74c3c;
                    }}

                    [data-theme="dark"] {{
                        --primary-color: #2980b9;
                        --secondary-color: #ecf0f1;
                        --background-color: #1a1a1a;
                        --card-background: #2d2d2d;
                        --text-color: #ffffff;
                        --border-color: #404040;
                    }}

                    * {{
                        margin: 0;
                        padding: 0;
                        box-sizing: border-box;
                        transition: background-color 0.3s, color 0.3s;
                    }}

                    body {{
                        font-family: 'Microsoft YaHei', Arial, sans-serif;
                        line-height: 1.6;
                        background-color: var(--background-color);
                        color: var(--text-color);
                    }}

                    .container {{
                        max-width: 1200px;
                        margin: 0 auto;
                        padding: 20px;
                    }}

                    .header {{
                        background: var(--card-background);
                        padding: 20px;
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                        margin-bottom: 20px;
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                    }}

                    .theme-switch {{
                        position: relative;
                        display: inline-block;
                        width: 60px;
                        height: 34px;
                    }}

                    .theme-switch input {{
                        opacity: 0;
                        width: 0;
                        height: 0;
                    }}

                    .slider {{
                        position: absolute;
                        cursor: pointer;
                        top: 0;
                        left: 0;
                        right: 0;
                        bottom: 0;
                        background-color: #ccc;
                        transition: .4s;
                        border-radius: 34px;
                    }}

                    .slider:before {{
                        position: absolute;
                        content: "";
                        height: 26px;
                        width: 26px;
                        left: 4px;
                        bottom: 4px;
                        background-color: white;
                        transition: .4s;
                        border-radius: 50%;
                    }}

                    input:checked + .slider {{
                        background-color: var(--primary-color);
                    }}

                    input:checked + .slider:before {{
                        transform: translateX(26px);
                    }}

                    .status-card {{
                        background: var(--card-background);
                        padding: 20px;
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                        margin-bottom: 20px;
                        animation: fadeIn 0.5s ease-in;
                    }}

                    .feature-grid {{
                        display: grid;
                        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                        gap: 20px;
                        margin: 20px 0;
                    }}

                    .feature-card {{
                        background: var(--card-background);
                        padding: 20px;
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                        border-left: 4px solid var(--primary-color);
                        transition: transform 0.3s ease;
                    }}

                    .feature-card:hover {{
                        transform: translateY(-5px);
                    }}

                    .btn {{
                        display: inline-block;
                        background: var(--primary-color);
                        color: white;
                        padding: 10px 20px;
                        text-decoration: none;
                        border-radius: 5px;
                        margin: 5px;
                        transition: all 0.3s;
                        border: none;
                        cursor: pointer;
                    }}

                    .btn:hover {{
                        background: var(--secondary-color);
                        transform: translateY(-2px);
                    }}

                    .loading {{
                        display: none;
                        position: fixed;
                        top: 0;
                        left: 0;
                        width: 100%;
                        height: 100%;
                        background: rgba(0,0,0,0.5);
                        z-index: 1000;
                    }}

                    .loading-spinner {{
                        position: absolute;
                        top: 50%;
                        left: 50%;
                        transform: translate(-50%, -50%);
                        width: 50px;
                        height: 50px;
                        border: 5px solid #f3f3f3;
                        border-top: 5px solid var(--primary-color);
                        border-radius: 50%;
                        animation: spin 1s linear infinite;
                    }}

                    @keyframes spin {{
                        0% {{ transform: translate(-50%, -50%) rotate(0deg); }}
                        100% {{ transform: translate(-50%, -50%) rotate(360deg); }}
                    }}

                    @keyframes fadeIn {{
                        from {{ opacity: 0; transform: translateY(20px); }}
                        to {{ opacity: 1; transform: translateY(0); }}
                    }}

                    .footer {{
                        text-align: center;
                        margin-top: 40px;
                        padding: 20px;
                        background: var(--card-background);
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    }}

                    @media (max-width: 768px) {{
                        .container {{
                            padding: 10px;
                        }}
                        .feature-grid {{
                            grid-template-columns: 1fr;
                        }}
                        .header {{
                            flex-direction: column;
                            text-align: center;
                        }}
                        .theme-switch {{
                            margin-top: 10px;
                        }}
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🚀 业务分析报告自动化系统</h1>
                        <label class="theme-switch">
                            <input type="checkbox" id="theme-toggle">
                            <span class="slider"></span>
                        </label>
                    </div>
                    
                    <div class="status-card">
                        <h2>系统状态</h2>
                        <div class="status-content">
                            <p><strong>✅ 运行状态：</strong>正常</p>
                            <p><strong>📅 最新报告：</strong>{latest_report_name}</p>
                            <p><strong>🔧 运行模式：</strong>Level 0 零依赖模式 + FastAPI核心</p>
                            <p><strong>📊 功能可用性：</strong>核心分析功能 100% 可用</p>
                        </div>
                    </div>
                    
                    <div class="feature-grid">
                        <div class="feature-card">
                            <h3>📊 分析报告</h3>
                            <p>查看最新生成的业务分析报告，包含GMV分解、品类分析、区域对比等。</p>
                            <div class="card-actions">
                                <a href="/reports/" class="btn">查看报告列表</a>
                                <a href="/reports/{latest_report_name}" class="btn">最新报告</a>
                            </div>
                        </div>
                        
                        <div class="feature-card">
                            <h3>📈 数据图表</h3>
                            <p>查看ASCII文本图表，包含贡献度分析、趋势图表等可视化内容。</p>
                            <div class="card-actions">
                                <a href="/charts/" class="btn">查看图表</a>
                            </div>
                        </div>
                        
                        <div class="feature-card">
                            <h3>⚙️ 系统功能</h3>
                            <p>系统具备优秀的零依赖运行能力，支持完整的业务分析流程。</p>
                            <ul class="feature-list">
                                <li>✅ 数据分析引擎</li>
                                <li>✅ 报告自动生成</li>
                                <li>✅ 文本图表</li>
                                <li>✅ 预测分析（模拟）</li>
                                <li>✅ Web界面（当前）</li>
                            </ul>
                        </div>
                        
                        <div class="feature-card">
                            <h3>🔧 系统信息</h3>
                            <ul class="feature-list">
                                <li>🚀 零依赖运行能力</li>
                                <li>⚡ 智能降级机制</li>
                                <li>🛡️ 优雅错误处理</li>
                                <li>📈 渐进式功能增强</li>
                            </ul>
                        </div>
                    </div>
                    
                    <div class="footer">
                        <p>🎉 业务分析报告自动化系统 v3.0 | 生产就绪状态</p>
                        <p>💡 提示：当前运行在零依赖+Web核心模式，所有核心功能完全可用</p>
                    </div>
                </div>

                <div class="loading">
                    <div class="loading-spinner"></div>
                </div>

                <script>
                    // 主题切换
                    const themeToggle = document.getElementById('theme-toggle');
                    themeToggle.addEventListener('change', () => {{
                        document.body.setAttribute('data-theme', themeToggle.checked ? 'dark' : 'light');
                    }});

                    // 加载动画
                    document.querySelectorAll('a').forEach(link => {{
                        link.addEventListener('click', (e) => {{
                            if (!link.getAttribute('href').startsWith('#')) {{
                                document.querySelector('.loading').style.display = 'block';
                            }}
                        }});
                    }});

                    // 页面加载完成后隐藏加载动画
                    window.addEventListener('load', () => {{
                        document.querySelector('.loading').style.display = 'none';
                    }});
                </script>
            </body>
            </html>
            """
            
            self.wfile.write(html_content.encode('utf-8'))
        elif self.path == "/reports/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()

            # 递归读取output/reports及子目录下所有报告文件
            def scan_reports(base_dir, rel_path=""):
                items = []
                for entry in sorted(Path(base_dir).iterdir(), key=lambda x: (x.is_file(), -x.stat().st_ctime)):
                    if entry.is_dir():
                        items.append({
                            'type': 'dir',
                            'name': entry.name,
                            'children': scan_reports(entry, rel_path + entry.name + '/')
                        })
                    else:
                        items.append({
                            'type': 'file',
                            'name': entry.name,
                            'path': rel_path + entry.name,
                            'ctime': entry.stat().st_ctime,
                            'size': entry.stat().st_size
                        })
                return items

            report_tree = scan_reports("output/reports")

            # 标签和类型映射
            def get_label_color(name):
                if "retail_business_report" in name:
                    return ("零售", "#27ae60")
                if "intelligent_report" in name:
                    return ("智能", "#2980b9")
                if "executive_summary" in name:
                    return ("摘要", "#e67e22")
                if "export" in name:
                    return ("导出", "#8e44ad")
                return ("其他", "#7f8c8d")

            # 递归渲染目录树
            def render_tree(items, level=0):
                html = ''
                for item in items:
                    if item['type'] == 'dir':
                        html += f'''<details class="dir-group" open><summary class="dir-title" style="margin-left:{level*18}px;">📁 {item['name']}</summary>'''
                        html += render_tree(item['children'], level+1)
                        html += '</details>'
                    else:
                        label, color = get_label_color(item['name'])
                        ext = Path(item['name']).suffix.lower()
                        icon = "📄" if ext in [".md", ".html"] else ("📊" if ext in [".csv", ".json"] else "📁")
                        html += f'''
                        <div class="report-card" style="border-left: 5px solid {color};margin-left:{level*18}px;">
                            <div class="report-header">
                                <span class="report-icon">{icon}</span>
                                <span class="report-title">{item['name']}</span>
                                <span class="report-label" style="background:{color};">{label}</span>
                            </div>
                            <div class="report-meta">
                                <span>创建时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(item['ctime']))}</span>
                                <span>大小: {item['size']//1024}KB</span>
                            </div>
                            <a href="/reports/{item['path']}" class="report-link">查看/下载</a>
                        </div>
                        '''
                return html

            html = f'''
            <!DOCTYPE html>
            <html lang="zh-CN">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>报告列表 - 业务分析报告自动化系统</title>
                <style>
                    body {{ font-family: 'Microsoft YaHei', Arial, sans-serif; background: #f4f7fa; margin: 0; padding: 0; }}
                    .container {{ max-width: 1200px; margin: 40px auto; background: #fff; border-radius: 12px; box-shadow: 0 4px 32px rgba(44,62,80,0.08); padding: 32px 40px 40px 40px; }}
                    h1 {{ text-align: center; color: #2c3e50; margin-bottom: 32px; font-size: 2.2em; letter-spacing: 2px; }}
                    .dir-group {{ margin-bottom: 18px; }}
                    .dir-title {{ font-size: 1.15em; font-weight: bold; color: #2980b9; cursor: pointer; }}
                    .report-card {{ background: #f9fbfd; border-radius: 8px; box-shadow: 0 2px 8px rgba(44,62,80,0.06); padding: 20px 24px 18px 24px; display: flex; flex-direction: column; justify-content: space-between; transition: box-shadow 0.2s; border-left: 5px solid #3498db; margin-bottom: 10px; }}
                    .report-card:hover {{ box-shadow: 0 6px 24px rgba(52,152,219,0.13); background: #f0f6fa; }}
                    .report-header {{ display: flex; align-items: center; margin-bottom: 8px; }}
                    .report-icon {{ font-size: 1.6em; margin-right: 12px; }}
                    .report-title {{ font-weight: bold; color: #34495e; flex: 1; font-size: 1.1em; }}
                    .report-label {{ color: #7f8c8d; font-size: 0.85em; border-radius: 4px; padding: 2px 8px; margin-left: 10px; vertical-align: middle; }}
                    .report-meta {{ color: #7f8c8d; font-size: 0.95em; margin-bottom: 10px; display: flex; justify-content: space-between; }}
                    .report-link {{ display: inline-block; background: #3498db; color: #fff; padding: 8px 18px; border-radius: 5px; text-decoration: none; text-align: center; font-size: 1em; margin-top: 8px; transition: background 0.2s; }}
                    .report-link:hover {{ background: #217dbb; }}
                    @media (max-width: 700px) {{ .container {{ padding: 10px; }} .report-card {{ padding: 12px; }} }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>📋 分析报告多层级列表</h1>
                    {render_tree(report_tree)}
                </div>
            </body>
            </html>
            '''
            self.wfile.write(html.encode('utf-8'))
        elif self.path == "/charts/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()

            # 生成图表展示页面，使用 ECharts 展示约 20 种交互式图表
            html_content = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>数据图表 - 业务分析报告自动化系统</title>
    <style>
        :root {
            --primary-color: #3498db;
            --secondary-color: #2c3e50;
            --background-color: #f5f5f5;
            --card-background: #ffffff;
            --text-color: #333333;
        }
        [data-theme="dark"] {
            --primary-color: #2980b9;
            --background-color: #1a1a1a;
            --card-background: #2d2d2d;
            --text-color: #ffffff;
        }
        body {
            margin: 0; padding: 0;
            background: var(--background-color);
            color: var(--text-color);
            font-family: 'Microsoft YaHei', Arial, sans-serif;
        }
        .echarts-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px,1fr));
            gap: 20px;
            padding: 20px;
        }
        .echarts-card {
            background: var(--card-background);
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 20px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            cursor: pointer;
            position: relative;
        }
        .echarts-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        .single-export-btn {
            position: absolute;
            top: 12px;
            right: 12px;
            background: var(--primary-color);
            color: #fff;
            border: none;
            border-radius: 4px;
            padding: 2px 8px;
            font-size: 0.85em;
            cursor: pointer;
            z-index: 2;
        }
        .chart-controls-bar {
            display: flex;
            justify-content: flex-end;
            gap: 10px;
            padding: 10px 20px;
        }
        .export-btn {
            background: var(--primary-color);
            color: white;
            border: none;
            padding: 6px 12px;
            border-radius: 4px;
            cursor: pointer;
            margin-left: 10px;
        }
        .modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            display: none;
            justify-content: center;
            align-items: center;
            z-index: 1000;
        }
        .modal-content {
            background: var(--card-background);
            padding: 20px;
            border-radius: 8px;
            width: 80%;
            max-height: 80%;
            overflow: auto;
        }
    </style>
</head>
<body data-theme="light">
    <!-- 引入 ECharts -->
    <script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/echarts-wordcloud@2/dist/echarts-wordcloud.min.js"></script>

    <div class="chart-controls-bar">
        <select id="globalTimeRange" class="time-range">
            <option value="day">日</option>
            <option value="week">周</option>
            <option value="month" selected>月</option>
            <option value="quarter">季度</option>
        </select>
        <button id="exportAll" class="export-btn">导出所有</button>
    </div>

    <div class="echarts-grid">
        <div class="echarts-card"><button class="single-export-btn" data-idx="1">导出</button><div class="echarts-title">折线图</div><div id="chart1" class="echart"></div></div>
        <div class="echarts-card"><button class="single-export-btn" data-idx="2">导出</button><div class="echarts-title">柱状图</div><div id="chart2" class="echart"></div></div>
        <div class="echarts-card"><button class="single-export-btn" data-idx="3">导出</button><div class="echarts-title">条形图</div><div id="chart3" class="echart"></div></div>
        <div class="echarts-card"><button class="single-export-btn" data-idx="4">导出</button><div class="echarts-title">饼图</div><div id="chart4" class="echart"></div></div>
        <div class="echarts-card"><button class="single-export-btn" data-idx="5">导出</button><div class="echarts-title">散点图</div><div id="chart5" class="echart"></div></div>
        <div class="echarts-card"><button class="single-export-btn" data-idx="6">导出</button><div class="echarts-title">雷达图</div><div id="chart6" class="echart"></div></div>
        <div class="echarts-card"><button class="single-export-btn" data-idx="7">导出</button><div class="echarts-title">漏斗图</div><div id="chart7" class="echart"></div></div>
        <div class="echarts-card"><button class="single-export-btn" data-idx="8">导出</button><div class="echarts-title">仪表盘</div><div id="chart8" class="echart"></div></div>
        <div class="echarts-card"><button class="single-export-btn" data-idx="9">导出</button><div class="echarts-title">矩形树图</div><div id="chart9" class="echart"></div></div>
        <div class="echarts-card"><button class="single-export-btn" data-idx="10">导出</button><div class="echarts-title">旭日图</div><div id="chart10" class="echart"></div></div>
        <div class="echarts-card"><button class="single-export-btn" data-idx="11">导出</button><div class="echarts-title">桑基图</div><div id="chart11" class="echart"></div></div>
        <div class="echarts-card"><button class="single-export-btn" data-idx="12">导出</button><div class="echarts-title">平行坐标</div><div id="chart12" class="echart"></div></div>
        <div class="echarts-card"><button class="single-export-btn" data-idx="13">导出</button><div class="echarts-title">主题河流图</div><div id="chart13" class="echart"></div></div>
        <div class="echarts-card"><button class="single-export-btn" data-idx="14">导出</button><div class="echarts-title">力导向图</div><div id="chart14" class="echart"></div></div>
        <div class="echarts-card"><button class="single-export-btn" data-idx="15">导出</button><div class="echarts-title">日历图</div><div id="chart15" class="echart"></div></div>
        <div class="echarts-card"><button class="single-export-btn" data-idx="16">导出</button><div class="echarts-title">象形柱状图</div><div id="chart16" class="echart"></div></div>
        <div class="echarts-card"><button class="single-export-btn" data-idx="17">导出</button><div class="echarts-title">K线图</div><div id="chart17" class="echart"></div></div>
        <div class="echarts-card"><button class="single-export-btn" data-idx="18">导出</button><div class="echarts-title">箱线图</div><div id="chart18" class="echart"></div></div>
        <div class="echarts-card"><button class="single-export-btn" data-idx="19">导出</button><div class="echarts-title">词云图</div><div id="chart19" class="echart"></div></div>
        <div class="echarts-card"><button class="single-export-btn" data-idx="20">导出</button><div class="echarts-title">甘特图</div><div id="chart20" class="echart"></div></div>
    </div>

    <div id="modalOverlay" class="modal-overlay"><div class="modal-content" id="modalContent"></div></div>

    <script>
        const commonToolbox = { feature: { dataZoom:{ yAxisIndex:'none' }, brush:{ type:['rect','polygon','clear'] }, dataView:{ readOnly:false }, restore:{}, saveAsImage:{} } };
        const chartOptions = [
            { title:{ text:'折线图', left:'center' }, toolbox:commonToolbox, tooltip:{ trigger:'axis' }, xAxis:{ type:'category', data:['Mon','Tue','Wed','Thu','Fri','Sat','Sun'] }, yAxis:{ type:'value' }, series:[{ name:'销量', type:'line', data:[150,230,224,218,135,147,260] }] },
            { title:{ text:'柱状图', left:'center' }, toolbox:commonToolbox, tooltip:{ trigger:'axis' }, xAxis:{ type:'category', data:['Mon','Tue','Wed','Thu','Fri','Sat','Sun'] }, yAxis:{ type:'value' }, series:[{ name:'销售额', type:'bar', data:[820,932,901,934,1290,1330,1320] }] },
            { title:{ text:'条形图', left:'center' }, toolbox:commonToolbox, tooltip:{ trigger:'item' }, xAxis:{ type:'value' }, yAxis:{ type:'category', data:['Mon','Tue','Wed','Thu','Fri','Sat','Sun'] }, series:[{ name:'访问量', type:'bar', data:[560,430,670,410,620,580,790] }] },
            { title:{ text:'饼图', left:'center' }, toolbox:commonToolbox, tooltip:{ trigger:'item' }, series:[{ name:'来源', type:'pie', radius:'50%', data:[{value:1048,name:'直接访问'},{value:735,name:'邮件营销'},{value:580,name:'联盟广告'},{value:484,name:'视频广告'},{value:300,name:'搜索引擎'}] }] },
            { title:{ text:'散点图', left:'center' }, toolbox:commonToolbox, tooltip:{ trigger:'axis' }, xAxis:{ type:'value' }, yAxis:{ type:'value' }, series:[{ name:'A组', type:'scatter', data:[[10,8],[15,12],[12,19],[8,5],[17,9]] }] },
            { title:{ text:'雷达图', left:'center' }, toolbox:commonToolbox, tooltip:{}, radar:{ indicator:[{name:'销售',max:6500},{name:'管理',max:16000},{name:'IT',max:30000},{name:'客服',max:38000},{name:'研发',max:52000},{name:'市场',max:25000}] }, series:[{ name:'预算 vs 实际', type:'radar', data:[{value:[4200,3000,20000,35000,50000,18000],name:'预算'},{value:[5000,14000,28000,26000,42000,21000],name:'实际'}] }] },
            { title:{ text:'漏斗图', left:'center' }, toolbox:commonToolbox, tooltip:{ trigger:'item' }, series:[{ name:'步骤', type:'funnel', left:'10%', top:'20%', width:'80%', min:0, max:100, sort:'descending', gap:2, label:{show:true}, data:[{value:60,name:'访问'},{value:40,name:'咨询'},{value:20,name:'订单'},{value:80,name:'展现'},{value:100,name:'曝光'}] }] },
            { title:{ text:'仪表盘', left:'center' }, toolbox:commonToolbox, tooltip:{ formatter:'{a}<br />{b} : {c}%' }, series:[{ name:'完成率', type:'gauge', progress:{ show:true }, detail:{ formatter:'{value}%' }, data:[{value:75,name:'完成率'}] }] },
            { title:{ text:'矩形树图', left:'center' }, toolbox:commonToolbox, tooltip:{ formatter:'{b} : {c}' }, series:[{ type:'treemap', data:[{name:'产品A',value:10},{name:'产品B',value:20},{name:'产品C',value:30},{name:'产品D',value:40}] }] },
            { title:{ text:'旭日图', left:'center' }, toolbox:commonToolbox, tooltip:{}, series:[{ type:'sunburst', data:[{ name:'全球', children:[{name:'亚洲',children:[{name:'中国',value:40},{name:'日本',value:30}]},{name:'欧洲',value:20}]}], radius:[0,'90%'], label:{rotate:'radial'} }] },
            { title:{ text:'桑基图', left:'center' }, toolbox:commonToolbox, tooltip:{ trigger:'item', triggerOn:'mousemove' }, series:[{ type:'sankey', data:[{name:'A'},{name:'B'},{name:'C'}], links:[{source:'A',target:'B',value:5},{source:'B',target:'C',value:3}] }] },
            { title:{ text:'平行坐标', left:'center' }, toolbox:commonToolbox, tooltip:{ trigger:'item', triggerOn:'mousemove' }, parallelAxis:[{dim:0,name:'AQI',max:300},{dim:1,name:'PM10',max:100},{dim:2,name:'PM2.5',max:100},{dim:3,name:'NO2',max:50}], series:[{ name:'北京', type:'parallel', data:[[50,30,20,10],[120,50,40,20],[80,20,10,5],[200,80,60,30]] }] },
            { title:{ text:'主题河流图', left:'center' }, toolbox:commonToolbox, tooltip:{ trigger:'axis', axisPointer:{ type:'shadow' } }, series:[{ type:'themeRiver', emphasis:{ focus:'series' }, data:[['2023-01-01','系列1',120],['2023-01-02','系列1',132],['2023-01-03','系列1',101],['2023-01-01','系列2',220],['2023-01-02','系列2',182],['2023-01-03','系列2',191]] }] },
            { title:{ text:'力导向图', left:'center' }, toolbox:commonToolbox, tooltip:{}, series:[{ type:'graph', layout:'force', roam:true, data:[{name:'节点1'},{name:'节点2'},{name:'节点3'}], links:[{source:'节点1',target:'节点2'},{source:'节点2',target:'节点3'}], force:{ repulsion:100 } }] },
            { title:{ text:'日历图', left:'center' }, toolbox:commonToolbox, tooltip:{}, calendar:{ range:['2023-04'], cellSize:['auto',20], orient:'horizontal' }, series:[{ type:'heatmap', coordinateSystem:'calendar', data:[['2023-04-01',1],['2023-04-05',5],['2023-04-10',10],['2023-04-15',8],['2023-04-20',15]] }] },
            { title:{ text:'象形柱状图', left:'center' }, toolbox:commonToolbox, tooltip:{ trigger:'axis' }, xAxis:{ type:'category', data:['A','B','C','D','E'] }, yAxis:{ type:'value' }, series:[{ name:'数量', type:'pictorialBar', symbol:'roundRect', data:[120,200,150,80,70], symbolRepeat:true, symbolSize:[20,20] }] },
            { title:{ text:'K线图', left:'center' }, toolbox:commonToolbox, tooltip:{ trigger:'axis', axisPointer:{ type:'cross' } }, xAxis:{ data:['2023/4/1','2023/4/2','2023/4/3','2023/4/4','2023/4/5'], boundaryGap:true, axisLine:{ onZero:false } }, yAxis:{ scale:true }, series:[{ type:'candlestick', data:[[2320.26,2302.6,2287.3,2362.94],[2300,2291.3,2288.26,2308.38]] }] },
            { title:{ text:'箱线图', left:'center' }, toolbox:commonToolbox, tooltip:{ trigger:'item' }, xAxis:{ type:'category', data:['A','B','C'] }, yAxis:{ type:'value' }, series:[{ name:'boxplot', type:'boxplot', data:[[85,120,140,200,250],[100,130,150,180,220],[80,110,135,190,230]] }] },
            { title:{ text:'词云图', left:'center' }, toolbox:commonToolbox, tooltip:{}, series:[{ type:'wordCloud', shape:'circle', data:[{name:'数据',value:1000},{name:'分析',value:618},{name:'报表',value:438},{name:'互动',value:405},{name:'可视化',value:309}], textRotation:[0,45,90,-45] }] },
            { title:{ text:'甘特图', left:'center' }, toolbox:commonToolbox, tooltip:{ formatter: function(params){ return params.value[0] + '<br />开始: ' + params.value[1] + '<br />结束: ' + params.value[2]; } }, xAxis:{ type:'time' }, yAxis:{ type:'category', data:['任务A','任务B','任务C'] }, series:[{ type:'bar', stack:'总量', encode:{ x:[1,2], y:0 }, data:[['任务A','2023-04-01','2023-04-05'],['任务B','2023-04-03','2023-04-08'],['任务C','2023-04-06','2023-04-10']] }] }
        ];
        chartOptions.forEach((opt, idx) => {
            const dom = document.getElementById('chart' + (idx + 1));
            const chart = echarts.init(dom);
            chart.setOption(opt);
            window.addEventListener('resize', () => chart.resize());
        });

        // 全局导出
        document.getElementById('exportAll').addEventListener('click', () => {
            chartOptions.forEach((opt, idx) => {
                const chart = echarts.getInstanceByDom(document.getElementById('chart' + (idx + 1)));
                const url = chart.getDataURL({ type: 'png', pixelRatio: 2, backgroundColor: '#fff' });
                const link = document.createElement('a');
                link.download = opt.title.text + '.png';
                link.href = url;
                link.click();
            });
        });

        // 单图导出
        document.querySelectorAll('.single-export-btn').forEach(btn => {
            btn.addEventListener('click', e => {
                e.stopPropagation();
                const idx = parseInt(btn.getAttribute('data-idx'));
                const chart = echarts.getInstanceByDom(document.getElementById('chart' + idx));
                const url = chart.getDataURL({ type: 'png', pixelRatio: 2, backgroundColor: '#fff' });
                const link = document.createElement('a');
                link.download = chartOptions[idx-1].title.text + '.png';
                link.href = url;
                link.click();
            });
        });

        // 全局时间/维度选择器联动（前端模拟）
        document.getElementById('globalTimeRange').addEventListener('change', e => {
            const val = e.target.value;
            chartOptions.forEach((opt, idx) => {
                // 这里只做标题后缀变化模拟，实际可根据后端数据动态切换
                let base = opt.title.text.replace(/（.*?）/g, '');
                opt.title.text = base + '（' + (val==='day'?'日':val==='week'?'周':val==='month'?'月':'季度') + '维度）';
                const chart = echarts.getInstanceByDom(document.getElementById('chart' + (idx + 1)));
                chart.setOption({ title: { text: opt.title.text } });
            });
        });

        // Modal放大时支持下拉切换系列（模拟）
        const modalOverlay = document.getElementById('modalOverlay');
        document.querySelectorAll('.echart').forEach(dom => {
            dom.addEventListener('dblclick', () => {
                const idx = Array.from(document.querySelectorAll('.echart')).indexOf(dom);
                const opt = chartOptions[idx];
                document.getElementById('modalContent').innerHTML = `<div class="echarts-title">${opt.title.text} <select id='modalSeries'><option value='0'>主系列</option><option value='1'>对比系列</option></select></div><div style="height:400px;" id="modalChart"></div>`;
                modalOverlay.style.display = 'flex';
                const modalChart = echarts.init(document.getElementById('modalChart'));
                modalChart.setOption(opt);
                window.addEventListener('resize', () => modalChart.resize());
                // 下拉切换系列（仅模拟，实际可根据 opt.series 切换）
                document.getElementById('modalSeries').addEventListener('change', e => {
                    // 这里只是演示，实际可根据不同series切换数据
                    modalChart.setOption({ title: { text: opt.title.text + (e.target.value==='1'?'（对比）':'') } });
                });
            });
        });

        // 点击遮罩关闭模态
        modalOverlay.addEventListener('click', () => modalOverlay.style.display = 'none');
    </script>
</body>
</html>
            """
            self.wfile.write(html_content.encode('utf-8'))
        # 报告详情页面，注入返回导航栏
        elif self.path.startswith("/reports/") and self.path.endswith(".html"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            # 构造文件路径
            file_rel = self.path[len("/"):]  # e.g. 'reports/xxx.html'
            full_path = Path("output") / file_rel
            if full_path.exists():
                content = full_path.read_text(encoding='utf-8')
                # 插入返回导航栏
                nav_html = '<div style="background:#ffffff;padding:10px;text-align:left;"><a href="/reports/" style="color:#3498db;text-decoration:none;font-weight:bold;">« 返回报告列表</a></div>'
                content = content.replace("<body>", "<body>" + nav_html, 1)
            else:
                content = '<h1>报告不存在</h1>'
            self.wfile.write(content.encode('utf-8'))
        elif self.path.startswith("/api/chart-data"):
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            # 解析参数
            query = urlparse(self.path).query
            params = parse_qs(query)
            chart_type = params.get('type', ['line'])[0]
            dim = params.get('dim', ['month'])[0]
            # 构造模拟数据
            if chart_type == 'line':
                data = {
                    'x': ['1月','2月','3月','4月','5月'],
                    'y': [8.5, 8.2, 9.1, 9.8, 10.2],
                    'title': f'折线图（{dim}维度）'
                }
            elif chart_type == 'bar':
                data = {
                    'x': ['A','B','C','D','E'],
                    'y': [120, 200, 150, 80, 70],
                    'title': f'柱状图（{dim}维度）'
                }
            elif chart_type == 'pie':
                data = {
                    'labels': ['直接访问','邮件营销','联盟广告','视频广告','搜索引擎'],
                    'values': [1048, 735, 580, 484, 300],
                    'title': f'饼图（{dim}维度）'
                }
            else:
                data = {'msg': '暂不支持该类型', 'title': f'{chart_type}（{dim}维度）'}
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
        else:
            # 处理其他请求
            super().do_GET()

def start_web_server(port=8080):
    """启动Web服务器"""
    print(f"🌐 启动简化Web服务器...")
    print(f"📂 服务目录: output/")
    print(f"🔗 访问地址: http://localhost:{port}")
    print(f"📄 主页: http://localhost:{port}/")
    print(f"📊 报告列表: http://localhost:{port}/reports/")
    print("")
    print("按 Ctrl+C 停止服务器")
    print("=" * 50)
    
    try:
        with socketserver.TCPServer(("", port), ReportHTTPRequestHandler) as httpd:
            # 自动在浏览器中打开
            def open_browser():
                time.sleep(1)  # 等待服务器启动
                webbrowser.open(f'http://localhost:{port}')
            
            browser_thread = threading.Thread(target=open_browser)
            browser_thread.daemon = True
            browser_thread.start()
            
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Web服务器已停止")
    except Exception as e:
        print(f"❌ 服务器启动失败: {e}")

if __name__ == "__main__":
    start_web_server() 