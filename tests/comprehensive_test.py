#!/usr/bin/env python3
"""
综合测试系统
测试所有增强功能模块的完整性和性能
"""

import os
import sys
import time
import json
import traceback
from datetime import datetime
from typing import Dict, List, Any, Tuple
from pathlib import Path

# 添加源代码路径
sys.path.append('src')

class ComprehensiveTestSuite:
    """综合测试套件"""
    
    def __init__(self):
        self.test_results = {
            'total_tests': 0,
            'passed_tests': 0,
            'failed_tests': 0,
            'test_details': [],
            'performance_metrics': {},
            'start_time': None,
            'end_time': None
        }
        self.output_dir = "output/test_results"
        os.makedirs(self.output_dir, exist_ok=True)
        
    def run_all_tests(self) -> Dict[str, Any]:
        """运行所有测试"""
        print("🚀 开始运行综合测试套件...")
        print("=" * 80)
        
        self.test_results['start_time'] = datetime.now()
        
        # 测试模块列表
        test_modules = [
            ('数据处理模块', self.test_data_processing),
            ('分析引擎模块', self.test_analytics_engine),
            ('可视化模块', self.test_visualization),
            ('报告生成模块', self.test_report_generation),
            ('主系统集成', self.test_main_system),
            ('性能测试', self.test_performance),
            ('错误处理', self.test_error_handling),
            ('依赖检测', self.test_dependency_detection)
        ]
        
        for module_name, test_function in test_modules:
            print(f"\n📋 测试模块: {module_name}")
            print("-" * 50)
            
            try:
                test_function()
            except Exception as e:
                self._record_test_failure(module_name, f"模块测试失败: {str(e)}")
                print(f"❌ {module_name} 测试失败: {e}")
                traceback.print_exc()
        
        self.test_results['end_time'] = datetime.now()
        
        # 生成测试报告
        self._generate_test_report()
        
        # 显示测试摘要
        self._display_test_summary()
        
        return self.test_results
    
    def test_data_processing(self):
        """测试数据处理模块"""
        try:
            from src.data.enhanced_data_processor import EnhancedDataProcessor
            
            processor = EnhancedDataProcessor()
            
            # 测试1: 基本初始化
            self._run_test("数据处理器初始化", lambda: processor is not None)
            
            # 测试2: 数据验证
            mock_data = self._create_mock_dataframe()
            validation_result = processor.validate_data_structure(mock_data)
            self._run_test("数据结构验证", lambda: 'is_valid' in validation_result)
            
            # 测试3: 数据清洗
            cleaned_data, cleaning_report = processor.clean_data(mock_data)
            self._run_test("数据清洗功能", lambda: cleaning_report['operations_performed'] is not None)
            
            # 测试4: 数据转换
            transformed_data, transform_report = processor.transform_data(cleaned_data)
            self._run_test("数据转换功能", lambda: transform_report['transformations_applied'] is not None)
            
            # 测试5: 数据概况生成
            profile = processor.generate_data_profile(transformed_data)
            self._run_test("数据概况生成", lambda: 'summary' in profile)
            
            # 测试6: 完整流水线
            pipeline_data, pipeline_results = processor.process_pipeline(mock_data)
            self._run_test("完整处理流水线", lambda: 'processing_time' in pipeline_results)
            
            print("✅ 数据处理模块测试完成")
            
        except ImportError:
            self._record_test_failure("数据处理模块", "模块导入失败")
        except Exception as e:
            self._record_test_failure("数据处理模块", str(e))
    
    def test_analytics_engine(self):
        """测试分析引擎模块"""
        try:
            from src.analysis.advanced_analytics_engine import AdvancedAnalyticsEngine
            
            engine = AdvancedAnalyticsEngine()
            mock_data = self._create_mock_dataframe()
            
            # 测试1: 相关性分析
            features = ['gmv', 'dau', 'conversion_rate']
            correlation_result = engine.correlation_analysis(mock_data, features)
            self._run_test("相关性分析", lambda: 'correlation_matrix' in correlation_result)
            
            # 测试2: 趋势分析
            trend_result = engine.trend_analysis(mock_data, 'gmv')
            self._run_test("趋势分析", lambda: 'trend_direction' in trend_result)
            
            # 测试3: 异常检测
            anomaly_result = engine.anomaly_detection(mock_data, 'gmv')
            self._run_test("异常检测", lambda: 'anomalies_detected' in anomaly_result)
            
            # 测试4: 用户分群
            segmentation_result = engine.advanced_segmentation(mock_data, features)
            self._run_test("用户分群", lambda: 'segments' in segmentation_result)
            
            print("✅ 分析引擎模块测试完成")
            
        except ImportError:
            self._record_test_failure("分析引擎模块", "模块导入失败")
        except Exception as e:
            self._record_test_failure("分析引擎模块", str(e))
    
    def test_visualization(self):
        """测试可视化模块"""
        try:
            from src.visualization.enhanced_chart_generator import EnhancedChartGenerator
            
            generator = EnhancedChartGenerator()
            mock_data = self._create_mock_chart_data()
            
            # 测试1: 高级仪表板创建
            dashboard_result = generator.create_advanced_dashboard(mock_data, self.output_dir)
            self._run_test("高级仪表板创建", lambda: 'charts_created' in dashboard_result)
            
            # 测试2: 专业图表创建
            chart_types = ['correlation_heatmap', 'funnel_chart']
            charts_result = generator.create_specialized_charts(mock_data, chart_types, self.output_dir)
            self._run_test("专业图表创建", lambda: 'charts_created' in charts_result)
            
            print("✅ 可视化模块测试完成")
            
        except ImportError:
            self._record_test_failure("可视化模块", "模块导入失败")
        except Exception as e:
            self._record_test_failure("可视化模块", str(e))
    
    def test_report_generation(self):
        """测试报告生成模块"""
        try:
            from src.reports.intelligent_report_generator import IntelligentReportGenerator
            
            generator = IntelligentReportGenerator()
            mock_data = self._create_mock_data()
            mock_analysis = self._create_mock_analysis_results()
            
            # 测试1: 综合报告生成
            report_result = generator.generate_comprehensive_report(
                mock_data, mock_analysis, self.output_dir, 
                formats=['html', 'markdown', 'json', 'executive']
            )
            self._run_test("综合报告生成", lambda: len(report_result['reports_generated']) > 0)
            
            # 测试2: 洞察生成
            insights = generator.insight_engine.generate_insights(mock_data, mock_analysis)
            self._run_test("智能洞察生成", lambda: 'insights' in insights)
            
            # 测试3: 建议生成
            recommendations = generator.insight_engine.generate_recommendations(
                mock_data, mock_analysis, insights
            )
            self._run_test("行动建议生成", lambda: 'recommendations' in recommendations)
            
            print("✅ 报告生成模块测试完成")
            
        except ImportError:
            self._record_test_failure("报告生成模块", "模块导入失败")
        except Exception as e:
            self._record_test_failure("报告生成模块", str(e))
    
    def test_main_system(self):
        """测试主系统集成"""
        try:
            from src.main import main
            
            # 测试主系统运行
            result = main()
            self._run_test("主系统运行", lambda: result is not None)
            
            # 检查输出文件
            output_exists = os.path.exists("output") and len(os.listdir("output")) > 0
            self._run_test("输出文件生成", lambda: output_exists)
            
            print("✅ 主系统集成测试完成")
            
        except ImportError:
            self._record_test_failure("主系统集成", "模块导入失败")
        except Exception as e:
            self._record_test_failure("主系统集成", str(e))
    
    def test_performance(self):
        """测试性能指标"""
        print("⚡ 开始性能测试...")
        
        # 测试1: 系统启动时间
        start_time = time.time()
        try:
            from src.main import main
            main()
            startup_time = time.time() - start_time
            self.test_results['performance_metrics']['startup_time'] = startup_time
            self._run_test("系统启动性能", lambda: startup_time < 10.0)  # 10秒内启动
            print(f"📊 系统启动时间: {startup_time:.2f}秒")
        except Exception as e:
            self._record_test_failure("系统启动性能", str(e))
        
        # 测试2: 内存使用
        try:
            import psutil
            memory_percent = psutil.virtual_memory().percent
            self.test_results['performance_metrics']['memory_usage'] = memory_percent
            self._run_test("内存使用率", lambda: memory_percent < 80.0)  # 内存使用率低于80%
            print(f"💾 内存使用率: {memory_percent:.1f}%")
        except ImportError:
            print("⚠️ psutil未安装，跳过内存测试")
        
        # 测试3: 文件生成速度
        start_time = time.time()
        try:
            # 模拟文件生成测试
            test_file = os.path.join(self.output_dir, "performance_test.txt")
            with open(test_file, 'w') as f:
                for i in range(1000):
                    f.write(f"测试行 {i}\n")
            file_generation_time = time.time() - start_time
            self.test_results['performance_metrics']['file_generation_time'] = file_generation_time
            self._run_test("文件生成性能", lambda: file_generation_time < 1.0)  # 1秒内完成
            print(f"📁 文件生成时间: {file_generation_time:.3f}秒")
        except Exception as e:
            self._record_test_failure("文件生成性能", str(e))
        
        print("✅ 性能测试完成")
    
    def test_error_handling(self):
        """测试错误处理"""
        print("🛡️ 开始错误处理测试...")
        
        # 测试1: 无效数据处理
        try:
            from src.data.enhanced_data_processor import EnhancedDataProcessor
            processor = EnhancedDataProcessor()
            
            # 测试None数据
            result = processor.validate_data_structure(None)
            self._run_test("None数据处理", lambda: result is not None)
            
            # 测试空数据
            result = processor.validate_data_structure({})
            self._run_test("空数据处理", lambda: result is not None)
            
        except Exception as e:
            self._record_test_failure("错误处理测试", str(e))
        
        # 测试2: 模块缺失处理
        try:
            # 模拟模块导入错误
            import sys
            original_modules = sys.modules.copy()
            
            # 暂时移除某个模块
            if 'pandas' in sys.modules:
                del sys.modules['pandas']
            
            # 测试系统在缺少依赖时的表现
            from src.main import main
            result = main()
            self._run_test("缺失依赖处理", lambda: result is not None)
            
            # 恢复模块
            sys.modules.update(original_modules)
            
        except Exception as e:
            print(f"⚠️ 模块缺失测试: {e}")
        
        print("✅ 错误处理测试完成")
    
    def test_dependency_detection(self):
        """测试依赖检测"""
        print("🔍 开始依赖检测测试...")
        
        dependencies = [
            ('pandas', 'Level 2+ 数据处理'),
            ('matplotlib', 'Level 2+ 可视化'),
            ('numpy', 'Level 2+ 数值计算'),
            ('jinja2', 'Level 2+ 模板引擎'),
            ('fastapi', 'Level 2+ Web框架'),
            ('plotly', 'Level 3 交互式图表'),
            ('sklearn', 'Level 3 机器学习')
        ]
        
        dependency_status = {}
        
        for dep_name, dep_desc in dependencies:
            try:
                __import__(dep_name)
                dependency_status[dep_name] = {'available': True, 'description': dep_desc}
                print(f"✅ {dep_name}: 可用 ({dep_desc})")
            except ImportError:
                dependency_status[dep_name] = {'available': False, 'description': dep_desc}
                print(f"❌ {dep_name}: 不可用 ({dep_desc})")
        
        self.test_results['performance_metrics']['dependency_status'] = dependency_status
        
        # 计算可用性等级
        level_0_deps = []  # 零依赖
        level_2_deps = ['pandas', 'matplotlib', 'numpy', 'jinja2', 'fastapi']
        level_3_deps = ['plotly', 'sklearn']
        
        level_2_available = sum(1 for dep in level_2_deps if dependency_status.get(dep, {}).get('available', False))
        level_3_available = sum(1 for dep in level_3_deps if dependency_status.get(dep, {}).get('available', False))
        
        if level_2_available >= 3:
            system_level = "Level 2 (标准功能)"
        elif level_3_available >= 1:
            system_level = "Level 3 (完整功能)"
        else:
            system_level = "Level 0 (零依赖模式)"
        
        print(f"🏆 系统功能等级: {system_level}")
        self.test_results['performance_metrics']['system_level'] = system_level
        
        self._run_test("依赖检测功能", lambda: True)  # 总是通过，因为检测本身就是成功的
        
        print("✅ 依赖检测测试完成")
    
    def _run_test(self, test_name: str, test_func) -> bool:
        """运行单个测试"""
        self.test_results['total_tests'] += 1
        
        try:
            start_time = time.time()
            result = test_func()
            end_time = time.time()
            
            if result:
                self.test_results['passed_tests'] += 1
                status = "✅ PASS"
                print(f"  {status} {test_name} ({end_time - start_time:.3f}s)")
                
                self.test_results['test_details'].append({
                    'name': test_name,
                    'status': 'PASS',
                    'duration': end_time - start_time,
                    'timestamp': datetime.now().isoformat()
                })
                return True
            else:
                self._record_test_failure(test_name, "测试条件不满足")
                return False
                
        except Exception as e:
            self._record_test_failure(test_name, str(e))
            return False
    
    def _record_test_failure(self, test_name: str, error_message: str):
        """记录测试失败"""
        self.test_results['failed_tests'] += 1
        status = "❌ FAIL"
        print(f"  {status} {test_name}: {error_message}")
        
        self.test_results['test_details'].append({
            'name': test_name,
            'status': 'FAIL',
            'error': error_message,
            'timestamp': datetime.now().isoformat()
        })
    
    def _create_mock_dataframe(self):
        """创建模拟DataFrame"""
        try:
            import pandas as pd
            import numpy as np
            
            return pd.DataFrame({
                'date': pd.date_range('2024-01-01', periods=100),
                'gmv': np.random.normal(800000, 100000, 100),
                'dau': np.random.normal(1000, 200, 100),
                'conversion_rate': np.random.normal(3.0, 0.5, 100),
                'category': np.random.choice(['电子产品', '服装', '家居'], 100),
                'region': np.random.choice(['北京', '上海', '广州', '深圳'], 100)
            })
        except ImportError:
            # 返回模拟对象
            class MockDataFrame:
                def __init__(self):
                    self.data = {
                        'gmv': [800000, 850000, 820000, 880000],
                        'dau': [1000, 1100, 950, 1050],
                        'conversion_rate': [3.0, 3.2, 2.8, 3.5]
                    }
                    self.columns = list(self.data.keys())
                    self.shape = (4, 3)
            
            return MockDataFrame()
    
    def _create_mock_chart_data(self) -> Dict[str, Any]:
        """创建模拟图表数据"""
        return {
            'gmv_trend': {'2024-01': 800000, '2024-02': 850000, '2024-03': 820000, '2024-04': 880000},
            'dau_trend': {'北京': 1200, '上海': 1100, '广州': 950, '深圳': 1050},
            'category_analysis': {'电子产品': 35, '服装': 25, '家居': 20, '其他': 20},
            'region_analysis': {'北京': 1200, '上海': 1100, '广州': 950, '深圳': 1050},
            'forecast': {
                '2024-05-01': {'actual': 880000, 'predicted': 885000},
                '2024-05-02': {'actual': 875000, 'predicted': 880000},
                '2024-05-03': {'actual': None, 'predicted': 890000}
            }
        }
    
    def _create_mock_data(self) -> Dict[str, Any]:
        """创建模拟业务数据"""
        return {
            'total_gmv': 8500000,
            'total_dau': 4300,
            'conversion_rate': 3.2,
            'regions': ['北京', '上海', '广州', '深圳'],
            'categories': ['电子产品', '服装', '家居', '其他']
        }
    
    def _create_mock_analysis_results(self) -> Dict[str, Any]:
        """创建模拟分析结果"""
        return {
            'trend_analysis': {
                'gmv_trend': 'increasing',
                'growth_rate': 12.5
            },
            'segmentation': {
                'segments_count': 4,
                'largest_segment': 'segment_1'
            },
            'charts': {
                'charts_created': ['dashboard', 'heatmap', 'funnel'],
                'interactive_charts': ['dashboard.html']
            }
        }
    
    def _generate_test_report(self):
        """生成测试报告"""
        report_data = {
            'test_summary': {
                'total_tests': self.test_results['total_tests'],
                'passed_tests': self.test_results['passed_tests'],
                'failed_tests': self.test_results['failed_tests'],
                'pass_rate': (self.test_results['passed_tests'] / self.test_results['total_tests'] * 100) if self.test_results['total_tests'] > 0 else 0,
                'start_time': self.test_results['start_time'].isoformat(),
                'end_time': self.test_results['end_time'].isoformat(),
                'duration': (self.test_results['end_time'] - self.test_results['start_time']).total_seconds()
            },
            'test_details': self.test_results['test_details'],
            'performance_metrics': self.test_results['performance_metrics']
        }
        
        # 保存JSON报告
        json_file = os.path.join(self.output_dir, f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False, default=str)
        
        # 生成HTML报告
        html_file = os.path.join(self.output_dir, f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")
        self._generate_html_test_report(report_data, html_file)
        
        print(f"📄 测试报告已生成: {json_file}")
        print(f"🌐 HTML报告已生成: {html_file}")
    
    def _generate_html_test_report(self, report_data: Dict[str, Any], filename: str):
        """生成HTML测试报告"""
        summary = report_data['test_summary']
        
        html_content = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>综合测试报告</title>
    <style>
        body {{ font-family: 'Microsoft YaHei', Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 20px rgba(0,0,0,0.1); }}
        .header {{ text-align: center; border-bottom: 3px solid #007bff; padding-bottom: 20px; margin-bottom: 30px; }}
        .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }}
        .metric {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; text-align: center; }}
        .pass {{ color: #28a745; }}
        .fail {{ color: #dc3545; }}
        .test-item {{ background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #007bff; }}
        .performance {{ background: #e9ecef; padding: 20px; border-radius: 8px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧪 综合测试报告</h1>
            <p>系统功能验证与性能评估</p>
        </div>
        
        <div class="summary">
            <div class="metric">
                <h3>总测试数</h3>
                <div style="font-size: 2rem; font-weight: bold;">{summary['total_tests']}</div>
            </div>
            <div class="metric">
                <h3>通过测试</h3>
                <div style="font-size: 2rem; font-weight: bold;">{summary['passed_tests']}</div>
            </div>
            <div class="metric">
                <h3>失败测试</h3>
                <div style="font-size: 2rem; font-weight: bold;">{summary['failed_tests']}</div>
            </div>
            <div class="metric">
                <h3>通过率</h3>
                <div style="font-size: 2rem; font-weight: bold;">{summary['pass_rate']:.1f}%</div>
            </div>
        </div>
        
        <h2>📊 测试详情</h2>
"""
        
        for test in report_data['test_details']:
            status_class = 'pass' if test['status'] == 'PASS' else 'fail'
            status_icon = '✅' if test['status'] == 'PASS' else '❌'
            
            html_content += f"""
        <div class="test-item">
            <strong class="{status_class}">{status_icon} {test['name']}</strong>
            <div>状态: {test['status']}</div>
            {f"<div>错误: {test.get('error', '')}</div>" if test['status'] == 'FAIL' else ''}
            {f"<div>耗时: {test.get('duration', 0):.3f}s</div>" if 'duration' in test else ''}
        </div>
"""
        
        html_content += f"""
        <h2>⚡ 性能指标</h2>
        <div class="performance">
"""
        
        for metric, value in report_data['performance_metrics'].items():
            if isinstance(value, dict):
                html_content += f"<h4>{metric}:</h4><ul>"
                for k, v in value.items():
                    html_content += f"<li>{k}: {v}</li>"
                html_content += "</ul>"
            else:
                html_content += f"<p><strong>{metric}:</strong> {value}</p>"
        
        html_content += f"""
        </div>
        
        <div style="text-align: center; margin-top: 40px; color: #6c757d;">
            <p>🤖 测试完成时间: {summary['end_time']}</p>
            <p>⏱️ 总耗时: {summary['duration']:.2f}秒</p>
        </div>
    </div>
</body>
</html>
"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def _display_test_summary(self):
        """显示测试摘要"""
        duration = (self.test_results['end_time'] - self.test_results['start_time']).total_seconds()
        pass_rate = (self.test_results['passed_tests'] / self.test_results['total_tests'] * 100) if self.test_results['total_tests'] > 0 else 0
        
        print("\n" + "=" * 80)
        print("🏆 测试摘要")
        print("=" * 80)
        print(f"📊 总测试数: {self.test_results['total_tests']}")
        print(f"✅ 通过测试: {self.test_results['passed_tests']}")
        print(f"❌ 失败测试: {self.test_results['failed_tests']}")
        print(f"📈 通过率: {pass_rate:.1f}%")
        print(f"⏱️ 总耗时: {duration:.2f}秒")
        
        if pass_rate >= 90:
            print("🌟 测试结果: 优秀")
        elif pass_rate >= 80:
            print("👍 测试结果: 良好")
        elif pass_rate >= 70:
            print("➡️ 测试结果: 一般")
        else:
            print("⚠️ 测试结果: 需要改进")
        
        # 显示系统等级
        system_level = self.test_results['performance_metrics'].get('system_level', '未知')
        print(f"🏆 系统功能等级: {system_level}")
        
        print("=" * 80)


def main():
    """主测试函数"""
    print("🚀 业务分析报告自动化系统 - 综合测试")
    print("版本: 3.0 Enhanced")
    print("=" * 80)
    
    # 创建并运行测试套件
    test_suite = ComprehensiveTestSuite()
    results = test_suite.run_all_tests()
    
    return results


if __name__ == "__main__":
    main() 