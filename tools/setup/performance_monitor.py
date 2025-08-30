#!/usr/bin/env python3
"""
业务分析报告自动化系统 - 性能监控工具
评估系统性能，提供优化建议
"""

import sys
import os
import time
from datetime import datetime

# 条件导入psutil
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("⚠️  警告: psutil 未安装，部分系统信息将不可用")

# 添加src到路径
sys.path.insert(0, 'src')

class PerformanceMonitor:
    """性能监控器（支持简化模式）"""
    
    def __init__(self):
        self.start_time = None
        self.initial_memory = None
        self.results = {}
    
    def start_monitoring(self):
        """开始监控"""
        self.start_time = time.time()
        if PSUTIL_AVAILABLE:
            self.initial_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        else:
            self.initial_memory = 0
    
    def end_monitoring(self, test_name: str):
        """结束监控并记录结果"""
        if self.start_time is None:
            return
        
        end_time = time.time()
        
        if PSUTIL_AVAILABLE:
            final_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
            memory_used = final_memory - self.initial_memory
        else:
            final_memory = 0
            memory_used = 0
        
        self.results[test_name] = {
            'duration': end_time - self.start_time,
            'memory_used': memory_used,
            'final_memory': final_memory
        }
        
        self.start_time = None
        self.initial_memory = None
    
    def get_system_info(self):
        """获取系统信息"""
        if PSUTIL_AVAILABLE:
            try:
                return {
                    'python_version': sys.version.split()[0],
                    'cpu_count': psutil.cpu_count(),
                    'total_memory': psutil.virtual_memory().total / 1024 / 1024 / 1024,  # GB
                    'available_memory': psutil.virtual_memory().available / 1024 / 1024 / 1024,  # GB
                    'cpu_percent': psutil.cpu_percent(interval=1)
                }
            except:
                pass
        
        # 简化模式
        return {
            'python_version': sys.version.split()[0],
            'cpu_count': 'N/A',
            'total_memory': 'N/A',
            'available_memory': 'N/A',
            'cpu_percent': 'N/A'
        }

def check_dependencies():
    """检查依赖可用性"""
    dependencies = {
        'pandas': False,
        'numpy': False,
        'matplotlib': False,
        'seaborn': False,
        'fastapi': False,
        'streamlit': False,
        'jinja2': False,
        'markdown': False,
        'pdfkit': False,
        'sklearn': False
    }
    
    for dep in dependencies:
        try:
            __import__(dep)
            dependencies[dep] = True
        except ImportError:
            pass
    
    return dependencies

def performance_test_basic_import():
    """测试基本导入性能"""
    monitor = PerformanceMonitor()
    monitor.start_monitoring()
    
    try:
        from main import AnalysisReportSystem
        import web_interface
        success = True
    except Exception as e:
        success = False
        print(f"导入失败: {e}")
    
    monitor.end_monitoring('basic_import')
    return monitor.results['basic_import'], success

def performance_test_system_init():
    """测试系统初始化性能"""
    monitor = PerformanceMonitor()
    monitor.start_monitoring()
    
    try:
        from main import AnalysisReportSystem
        system = AnalysisReportSystem("dummy", "dummy_output")
        success = True
    except Exception as e:
        success = False
        print(f"初始化失败: {e}")
    
    monitor.end_monitoring('system_init')
    return monitor.results['system_init'], success

def performance_test_analysis():
    """测试分析性能"""
    monitor = PerformanceMonitor()
    monitor.start_monitoring()
    
    try:
        from main import AnalysisReportSystem
        from analysis.metrics_analyzer import MetricsAnalyzer
        
        system = AnalysisReportSystem("dummy", "dummy_output")
        current_data, previous_data = system.load_data()
        
        analyzer = MetricsAnalyzer(current_data, previous_data)
        results = analyzer.analyze()
        success = True
    except Exception as e:
        success = False
        print(f"分析失败: {e}")
    
    monitor.end_monitoring('analysis')
    return monitor.results['analysis'], success

def performance_test_visualization():
    """测试可视化性能"""
    monitor = PerformanceMonitor()
    monitor.start_monitoring()
    
    try:
        from visualization.chart_generator import ChartGenerator
        
        chart_gen = ChartGenerator("temp_charts")
        
        # 模拟分析结果
        mock_results = {
            'gmv_metrics': {
                'dau': type('MockMetric', (), {'change_rate': 5.2, 'contribution': 25.0})(),
                'frequency': type('MockMetric', (), {'change_rate': -2.1, 'contribution': -10.0})(),
                'order_price': type('MockMetric', (), {'change_rate': 3.8, 'contribution': 15.0})(),
                'conversion_rate': type('MockMetric', (), {'change_rate': -1.5, 'contribution': -5.0})()
            }
        }
        
        chart_paths = chart_gen.generate_all_charts(mock_results)
        success = True
        
        # 清理临时文件
        if os.path.exists("temp_charts"):
            import shutil
            shutil.rmtree("temp_charts")
    
    except Exception as e:
        success = False
        print(f"可视化失败: {e}")
    
    monitor.end_monitoring('visualization')
    return monitor.results['visualization'], success

def generate_performance_report():
    """生成性能报告"""
    print("=" * 70)
    print("🔍 业务分析报告自动化系统 - 性能监控报告")
    print("=" * 70)
    print(f"📅 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 系统信息
    monitor = PerformanceMonitor()
    sys_info = monitor.get_system_info()
    
    print("💻 系统环境:")
    print(f"  Python版本: {sys_info['python_version']}")
    print(f"  CPU核心数: {sys_info['cpu_count']}")
    print(f"  总内存: {sys_info['total_memory'] if isinstance(sys_info['total_memory'], str) else f'{sys_info['total_memory']:.1f} GB'}")
    print(f"  可用内存: {sys_info['available_memory'] if isinstance(sys_info['available_memory'], str) else f'{sys_info['available_memory']:.1f} GB'}")
    print(f"  CPU使用率: {sys_info['cpu_percent'] if isinstance(sys_info['cpu_percent'], str) else f'{sys_info['cpu_percent']:.1f}%'}")
    
    if not PSUTIL_AVAILABLE:
        print("  💡 安装psutil可获取详细系统信息: pip install psutil")
    print()
    
    # 依赖检查
    deps = check_dependencies()
    available_deps = sum(1 for v in deps.values() if v)
    total_deps = len(deps)
    
    print("📦 依赖可用性:")
    print(f"  可用依赖: {available_deps}/{total_deps} ({available_deps/total_deps*100:.1f}%)")
    
    dep_levels = {
        'Level 0 (零依赖)': True,  # 总是可用
        'Level 1 (最小)': deps['pandas'] and deps['jinja2'],
        'Level 2 (标准)': deps['pandas'] and deps['matplotlib'] and deps['fastapi'],
        'Level 3 (完整)': all([deps['pandas'], deps['matplotlib'], deps['fastapi'], 
                              deps['streamlit'], deps['sklearn']])
    }
    
    for level, available in dep_levels.items():
        status = "✅" if available else "❌"
        print(f"  {status} {level}")
    print()
    
    # 性能测试
    print("⚡ 性能基准测试:")
    
    tests = [
        ("基本导入", performance_test_basic_import),
        ("系统初始化", performance_test_system_init),
        ("数据分析", performance_test_analysis),
        ("图表生成", performance_test_visualization)
    ]
    
    total_time = 0
    total_memory = 0
    successful_tests = 0
    
    for test_name, test_func in tests:
        print(f"\n  🧪 {test_name}:")
        try:
            result, success = test_func()
            if success:
                print(f"    ✅ 成功")
                print(f"    ⏱️  耗时: {result['duration']:.3f} 秒")
                if PSUTIL_AVAILABLE and result['memory_used'] > 0:
                    print(f"    🧠 内存: {result['memory_used']:.1f} MB")
                else:
                    print(f"    🧠 内存: 监控不可用")
                total_time += result['duration']
                if PSUTIL_AVAILABLE:
                    total_memory += result['memory_used']
                successful_tests += 1
            else:
                print(f"    ❌ 失败")
        except Exception as e:
            print(f"    ❌ 异常: {e}")
    
    print("\n📊 总体性能:")
    print(f"  成功率: {successful_tests}/{len(tests)} ({successful_tests/len(tests)*100:.1f}%)")
    print(f"  总耗时: {total_time:.3f} 秒")
    if PSUTIL_AVAILABLE:
        print(f"  总内存: {total_memory:.1f} MB")
    else:
        print(f"  总内存: 监控不可用")
    
    # 性能等级
    if total_time < 1.0:
        perf_level = "🚀 优秀"
    elif total_time < 3.0:
        perf_level = "⚡ 良好"
    elif total_time < 5.0:
        perf_level = "👍 一般"
    else:
        perf_level = "🐌 需优化"
    
    print(f"  性能等级: {perf_level}")
    print()
    
    # 优化建议
    print("💡 优化建议:")
    
    if PSUTIL_AVAILABLE and isinstance(sys_info['available_memory'], (int, float)):
        if sys_info['available_memory'] < 1.0:
            print("  ⚠️  可用内存不足1GB，建议使用Level 0-1功能")
        
        if isinstance(sys_info['cpu_percent'], (int, float)) and sys_info['cpu_percent'] > 80:
            print("  ⚠️  CPU使用率过高，建议减少并发任务")
    
    if not deps['pandas']:
        print("  📈 安装pandas可显著提升数据处理性能")
    
    if not deps['matplotlib']:
        print("  📊 安装matplotlib可启用图表可视化功能")
    
    if total_time > 3.0:
        print("  🔧 系统响应较慢，建议检查网络和磁盘性能")
    
    if successful_tests < len(tests):
        print("  🚨 部分功能不可用，建议检查依赖安装")
    
    if not PSUTIL_AVAILABLE:
        print("  🔍 安装psutil可获取详细性能监控: pip install psutil")
    
    print("\n🎯 推荐配置:")
    
    memory_ok = not PSUTIL_AVAILABLE or (isinstance(sys_info['available_memory'], (int, float)) and sys_info['available_memory'] >= 2.0)
    
    if memory_ok and available_deps >= 8:
        print("  🌟 推荐使用Level 3完整功能")
    elif (not PSUTIL_AVAILABLE or (isinstance(sys_info['available_memory'], (int, float)) and sys_info['available_memory'] >= 1.0)) and available_deps >= 5:
        print("  📊 推荐使用Level 2标准功能")
    elif available_deps >= 2:
        print("  🔧 推荐使用Level 1最小功能")
    else:
        print("  ⚡ 推荐使用Level 0零依赖模式")
    
    print("\n" + "=" * 70)

def main():
    """主函数"""
    try:
        generate_performance_report()
    except Exception as e:
        print(f"❌ 性能监控失败: {e}")
        print("💡 建议运行: python test_runner.py 进行基础测试")

if __name__ == "__main__":
    main() 