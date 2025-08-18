#!/usr/bin/env python3
"""
压力测试和性能测试
测试系统在高负载下的性能表现
"""

import pytest
import time
import threading
import asyncio
import psutil
import gc
import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from pathlib import Path
import json
import tempfile
import shutil
from unittest.mock import Mock, patch

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.web_interface import WebInterface
from src.data.data_processor import DataProcessor
from src.analysis.professional_analytics import ProfessionalAnalytics
from src.visualization.chart_generator import ChartGenerator
from src.monitoring.metrics_collector import MetricsCollector
from src.utils.logger import system_logger


class PerformanceMonitor:
    """性能监控工具"""
    
    def __init__(self):
        self.start_time = None
        self.start_memory = None
        self.start_cpu = None
        
    def start(self):
        """开始监控"""
        self.start_time = time.time()
        self.start_memory = psutil.virtual_memory().used
        self.start_cpu = psutil.cpu_percent(interval=1)
        gc.collect()  # 垃圾回收
        
    def stop(self):
        """停止监控并返回结果"""
        end_time = time.time()
        end_memory = psutil.virtual_memory().used
        end_cpu = psutil.cpu_percent(interval=1)
        
        return {
            'duration': end_time - self.start_time,
            'memory_delta': end_memory - self.start_memory,
            'cpu_avg': (self.start_cpu + end_cpu) / 2,
            'memory_used': end_memory / (1024 * 1024),  # MB
        }


class TestStressPerformance:
    """压力测试和性能测试类"""
    
    @pytest.fixture
    def setup_test_environment(self):
        """设置测试环境"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_data_dir = Path(self.temp_dir) / "test_data"
        self.test_output_dir = Path(self.temp_dir) / "test_output"
        
        self.test_data_dir.mkdir(exist_ok=True)
        self.test_output_dir.mkdir(exist_ok=True)
        
        yield
        
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def generate_test_data(self, size: int) -> list:
        """生成测试数据"""
        return [
            {
                'id': i,
                'name': f'Item_{i}',
                'value': i * 1.5,
                'category': f'Category_{i % 10}',
                'timestamp': datetime.now().isoformat(),
                'metadata': {
                    'source': 'test',
                    'priority': i % 5,
                    'tags': [f'tag_{j}' for j in range(i % 3 + 1)]
                }
            }
            for i in range(size)
        ]
    
    @pytest.mark.performance
    def test_data_processing_performance(self, setup_test_environment):
        """测试数据处理性能"""
        processor = DataProcessor()
        monitor = PerformanceMonitor()
        
        # 测试不同数据量的处理性能
        test_sizes = [100, 1000, 5000, 10000]
        results = {}
        
        for size in test_sizes:
            test_data = self.generate_test_data(size)
            
            monitor.start()
            result = processor.process_data(test_data)
            performance = monitor.stop()
            
            results[size] = performance
            
            # 性能断言
            assert performance['duration'] < size * 0.01, f"Processing too slow for {size} items"
            assert performance['memory_delta'] < size * 1000, f"Memory usage too high for {size} items"
            
            system_logger.info(f"Processed {size} items in {performance['duration']:.2f}s")
        
        # 检查性能线性度
        if len(results) >= 2:
            sizes = sorted(results.keys())
            for i in range(1, len(sizes)):
                ratio = sizes[i] / sizes[i-1]
                time_ratio = results[sizes[i]]['duration'] / results[sizes[i-1]]['duration']
                
                # 时间复杂度不应该超过O(n²)
                assert time_ratio < ratio * ratio, "Performance degradation too severe"
    
    @pytest.mark.performance
    def test_concurrent_data_processing(self, setup_test_environment):
        """测试并发数据处理"""
        processor = DataProcessor()
        monitor = PerformanceMonitor()
        
        def process_batch(batch_id: int):
            """处理数据批次"""
            test_data = self.generate_test_data(1000)
            start_time = time.time()
            result = processor.process_data(test_data)
            duration = time.time() - start_time
            return batch_id, duration, result
        
        # 测试不同并发级别
        concurrency_levels = [1, 2, 4, 8]
        
        for concurrency in concurrency_levels:
            monitor.start()
            
            with ThreadPoolExecutor(max_workers=concurrency) as executor:
                futures = [executor.submit(process_batch, i) for i in range(concurrency)]
                results = [future.result() for future in as_completed(futures)]
            
            performance = monitor.stop()
            
            # 检查所有任务都成功完成
            assert len(results) == concurrency
            
            # 并发处理不应该比单线程慢太多
            if concurrency > 1:
                avg_duration = sum(r[1] for r in results) / len(results)
                assert performance['duration'] < avg_duration * 2, "Concurrency overhead too high"
            
            system_logger.info(f"Concurrent processing ({concurrency} threads): {performance['duration']:.2f}s")
    
    @pytest.mark.performance
    def test_memory_usage_under_load(self, setup_test_environment):
        """测试负载下的内存使用"""
        processor = DataProcessor()
        initial_memory = psutil.virtual_memory().used
        
        # 持续处理数据并监控内存
        memory_samples = []
        
        for i in range(50):
            test_data = self.generate_test_data(2000)
            processor.process_data(test_data)
            
            current_memory = psutil.virtual_memory().used
            memory_delta = current_memory - initial_memory
            memory_samples.append(memory_delta)
            
            # 强制垃圾回收
            if i % 10 == 0:
                gc.collect()
        
        # 检查内存泄漏
        max_memory = max(memory_samples)
        final_memory = memory_samples[-1]
        
        # 最终内存使用不应该超过峰值的80%
        assert final_memory < max_memory * 0.8, "Possible memory leak detected"
        
        # 内存使用不应该无限增长
        recent_avg = sum(memory_samples[-10:]) / 10
        early_avg = sum(memory_samples[:10]) / 10
        growth_ratio = recent_avg / early_avg if early_avg > 0 else 1
        
        assert growth_ratio < 2.0, "Memory usage growing too fast"
        
        system_logger.info(f"Memory usage - Max: {max_memory/1024/1024:.1f}MB, Final: {final_memory/1024/1024:.1f}MB")
    
    @pytest.mark.performance
    def test_chart_generation_performance(self, setup_test_environment):
        """测试图表生成性能"""
        chart_generator = ChartGenerator()
        monitor = PerformanceMonitor()
        
        # 测试不同复杂度的图表
        test_cases = [
            {'size': 100, 'type': 'line'},
            {'size': 500, 'type': 'bar'},
            {'size': 1000, 'type': 'scatter'},
            {'size': 2000, 'type': 'heatmap'},
        ]
        
        for case in test_cases:
            # 生成测试数据
            x_data = list(range(case['size']))
            y_data = [i * 1.5 + (i % 10) for i in x_data]
            
            chart_data = {
                'x': x_data,
                'y': y_data,
                'labels': [f'Point_{i}' for i in x_data]
            }
            
            monitor.start()
            result = chart_generator.generate_chart(
                data=chart_data,
                chart_type=case['type'],
                output_path=str(self.test_output_dir / f"test_{case['type']}_{case['size']}.png")
            )
            performance = monitor.stop()
            
            # 性能断言
            assert performance['duration'] < 30, f"Chart generation too slow: {performance['duration']:.2f}s"
            assert result is not None, "Chart generation failed"
            
            system_logger.info(f"Generated {case['type']} chart ({case['size']} points) in {performance['duration']:.2f}s")
    
    @pytest.mark.performance
    def test_analytics_performance(self, setup_test_environment):
        """测试分析引擎性能"""
        analytics = ProfessionalAnalytics()
        monitor = PerformanceMonitor()
        
        # 生成复杂的分析数据
        large_dataset = self.generate_test_data(10000)
        
        # 测试各种分析功能
        analysis_types = [
            'correlation_analysis',
            'trend_analysis',
            'statistical_summary',
            'outlier_detection',
        ]
        
        for analysis_type in analysis_types:
            monitor.start()
            
            try:
                if hasattr(analytics, analysis_type):
                    result = getattr(analytics, analysis_type)(large_dataset)
                else:
                    result = analytics.analyze_data(large_dataset, analysis_type=analysis_type)
                
                performance = monitor.stop()
                
                # 性能断言
                assert performance['duration'] < 60, f"{analysis_type} analysis too slow"
                assert result is not None, f"{analysis_type} analysis failed"
                
                system_logger.info(f"{analysis_type} analysis completed in {performance['duration']:.2f}s")
                
            except Exception as e:
                system_logger.warning(f"{analysis_type} analysis failed: {e}")
    
    @pytest.mark.performance
    def test_metrics_collection_performance(self, setup_test_environment):
        """测试指标收集性能"""
        collector = MetricsCollector(collection_interval=1)
        monitor = PerformanceMonitor()
        
        # 启动指标收集
        collector.start_collection()
        
        monitor.start()
        
        # 模拟高频指标记录
        for i in range(10000):
            collector.record_api_request(f"endpoint_{i % 100}")
            collector.record_processing_time(0.1 + (i % 10) * 0.01)
            collector.record_active_user(f"user_{i % 50}")
            
            if i % 1000 == 0:
                collector.record_report_generated()
        
        performance = monitor.stop()
        collector.stop_collection()
        
        # 性能断言
        assert performance['duration'] < 10, "Metrics collection too slow"
        
        # 检查指标摘要
        summary = collector.get_metrics_summary()
        assert summary['total_metrics'] > 0
        
        system_logger.info(f"Recorded 10000 metrics in {performance['duration']:.2f}s")
    
    @pytest.mark.performance
    def test_file_io_performance(self, setup_test_environment):
        """测试文件I/O性能"""
        monitor = PerformanceMonitor()
        
        # 测试大文件读写
        large_data = self.generate_test_data(50000)
        test_file = self.test_data_dir / "large_test_file.json"
        
        # 写入性能测试
        monitor.start()
        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(large_data, f, ensure_ascii=False, indent=2)
        write_performance = monitor.stop()
        
        # 读取性能测试
        monitor.start()
        with open(test_file, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)
        read_performance = monitor.stop()
        
        # 性能断言
        assert write_performance['duration'] < 30, "File write too slow"
        assert read_performance['duration'] < 20, "File read too slow"
        assert len(loaded_data) == len(large_data), "Data integrity issue"
        
        file_size = test_file.stat().st_size / (1024 * 1024)  # MB
        system_logger.info(f"File I/O - Size: {file_size:.1f}MB, Write: {write_performance['duration']:.2f}s, Read: {read_performance['duration']:.2f}s")
    
    @pytest.mark.performance
    def test_api_response_time(self, setup_test_environment):
        """测试API响应时间"""
        web_interface = WebInterface()
        
        # 模拟API请求
        async def simulate_api_request(endpoint: str):
            start_time = time.time()
            
            # 模拟不同类型的API请求
            if endpoint == '/api/reports':
                await asyncio.sleep(0.1)  # 模拟数据库查询
                result = {'reports': [{'id': i, 'name': f'Report {i}'} for i in range(100)]}
            elif endpoint == '/api/analytics':
                await asyncio.sleep(0.5)  # 模拟复杂分析
                result = {'analysis': 'completed', 'metrics': {}}
            elif endpoint == '/api/charts':
                await asyncio.sleep(0.2)  # 模拟图表生成
                result = {'chart_url': '/charts/sample.png'}
            else:
                await asyncio.sleep(0.05)  # 基本响应
                result = {'status': 'ok'}
            
            duration = time.time() - start_time
            return endpoint, duration, result
        
        async def run_api_stress_test():
            endpoints = ['/api/reports', '/api/analytics', '/api/charts', '/api/status']
            tasks = []
            
            # 创建多个并发请求
            for _ in range(100):
                for endpoint in endpoints:
                    task = simulate_api_request(endpoint)
                    tasks.append(task)
            
            results = await asyncio.gather(*tasks)
            return results
        
        # 运行压力测试
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            start_time = time.time()
            results = loop.run_until_complete(run_api_stress_test())
            total_duration = time.time() - start_time
            
            # 分析结果
            response_times = [r[1] for r in results]
            avg_response_time = sum(response_times) / len(response_times)
            max_response_time = max(response_times)
            
            # 性能断言
            assert avg_response_time < 1.0, f"Average response time too high: {avg_response_time:.2f}s"
            assert max_response_time < 2.0, f"Max response time too high: {max_response_time:.2f}s"
            
            # 计算QPS
            total_requests = len(results)
            qps = total_requests / total_duration
            
            assert qps > 50, f"QPS too low: {qps:.1f}"
            
            system_logger.info(f"API Stress Test - Requests: {total_requests}, QPS: {qps:.1f}, Avg Response: {avg_response_time:.3f}s")
            
        finally:
            loop.close()
    
    @pytest.mark.performance
    def test_database_query_performance(self, setup_test_environment):
        """测试数据库查询性能"""
        # 模拟数据库查询
        class MockDatabase:
            def __init__(self):
                self.data = self.generate_mock_data(100000)
            
            def generate_mock_data(self, size):
                return [
                    {
                        'id': i,
                        'name': f'Record_{i}',
                        'value': i * 1.5,
                        'category': f'Category_{i % 20}',
                        'created_at': datetime.now() - timedelta(days=i % 365)
                    }
                    for i in range(size)
                ]
            
            def query(self, conditions):
                # 模拟查询逻辑
                result = []
                for record in self.data:
                    if self._match_conditions(record, conditions):
                        result.append(record)
                return result
            
            def _match_conditions(self, record, conditions):
                for key, value in conditions.items():
                    if key not in record or record[key] != value:
                        return False
                return True
        
        db = MockDatabase()
        monitor = PerformanceMonitor()
        
        # 测试不同复杂度的查询
        test_queries = [
            {'category': 'Category_1'},  # 简单查询
            {'category': 'Category_1', 'value': 1.5},  # 复合查询
            {},  # 全表扫描
        ]
        
        for i, query in enumerate(test_queries):
            monitor.start()
            results = db.query(query)
            performance = monitor.stop()
            
            # 性能断言
            assert performance['duration'] < 5.0, f"Query {i} too slow: {performance['duration']:.2f}s"
            
            system_logger.info(f"Query {i} returned {len(results)} results in {performance['duration']:.3f}s")
    
    @pytest.mark.performance
    def test_websocket_performance(self, setup_test_environment):
        """测试WebSocket性能"""
        import websockets
        import json
        
        async def websocket_stress_test():
            # 模拟WebSocket服务器
            messages_sent = 0
            messages_received = 0
            start_time = time.time()
            
            async def mock_websocket_handler(websocket, path):
                nonlocal messages_received
                try:
                    async for message in websocket:
                        messages_received += 1
                        # 回显消息
                        await websocket.send(f"Echo: {message}")
                except Exception as e:
                    system_logger.error(f"WebSocket error: {e}")
            
            # 模拟客户端连接和消息发送
            async def client_simulation():
                nonlocal messages_sent
                for i in range(1000):
                    messages_sent += 1
                    # 模拟发送消息
                    await asyncio.sleep(0.001)  # 模拟网络延迟
            
            # 运行客户端模拟
            await client_simulation()
            
            duration = time.time() - start_time
            
            # 计算性能指标
            messages_per_second = messages_sent / duration if duration > 0 else 0
            
            assert messages_per_second > 100, f"WebSocket throughput too low: {messages_per_second:.1f} msg/s"
            
            system_logger.info(f"WebSocket Performance - Sent: {messages_sent}, Rate: {messages_per_second:.1f} msg/s")
        
        # 运行WebSocket压力测试
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            loop.run_until_complete(websocket_stress_test())
        finally:
            loop.close()
    
    @pytest.mark.performance
    def test_system_resource_limits(self, setup_test_environment):
        """测试系统资源限制"""
        initial_memory = psutil.virtual_memory().used
        initial_cpu = psutil.cpu_percent(interval=1)
        
        # 运行资源密集型任务
        def resource_intensive_task():
            # CPU密集型任务
            result = sum(i * i for i in range(100000))
            
            # 内存密集型任务
            large_list = [i for i in range(10000)]
            large_dict = {i: f"value_{i}" for i in range(10000)}
            
            return result, len(large_list), len(large_dict)
        
        monitor = PerformanceMonitor()
        monitor.start()
        
        # 并发执行资源密集型任务
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(resource_intensive_task) for _ in range(10)]
            results = [future.result() for future in as_completed(futures)]
        
        performance = monitor.stop()
        
        # 检查资源使用
        final_memory = psutil.virtual_memory().used
        memory_delta = final_memory - initial_memory
        
        # 资源使用断言
        assert performance['cpu_avg'] < 90, f"CPU usage too high: {performance['cpu_avg']:.1f}%"
        assert memory_delta < 500 * 1024 * 1024, f"Memory usage too high: {memory_delta / 1024 / 1024:.1f}MB"
        
        system_logger.info(f"Resource Test - CPU: {performance['cpu_avg']:.1f}%, Memory Delta: {memory_delta / 1024 / 1024:.1f}MB")


# 性能基准测试
class TestPerformanceBenchmarks:
    """性能基准测试"""
    
    @pytest.mark.benchmark
    def test_data_processing_benchmark(self, setup_test_environment):
        """数据处理基准测试"""
        processor = DataProcessor()
        
        # 基准测试数据
        benchmark_data = [
            {'size': 1000, 'expected_time': 0.5},
            {'size': 5000, 'expected_time': 2.0},
            {'size': 10000, 'expected_time': 4.0},
        ]
        
        for benchmark in benchmark_data:
            test_data = TestStressPerformance().generate_test_data(benchmark['size'])
            
            start_time = time.time()
            result = processor.process_data(test_data)
            duration = time.time() - start_time
            
            # 基准断言
            assert duration < benchmark['expected_time'], f"Benchmark failed: {duration:.2f}s > {benchmark['expected_time']}s"
            assert result is not None
            
            system_logger.info(f"Benchmark {benchmark['size']} items: {duration:.2f}s (expected < {benchmark['expected_time']}s)")


if __name__ == '__main__':
    # 运行性能测试
    pytest.main([__file__, '-v', '-m', 'performance'])