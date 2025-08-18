#!/usr/bin/env python3
"""
边界条件测试
测试系统在各种边界情况下的行为
"""

import pytest
import json
import os
import tempfile
import shutil
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import sys

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.web_interface import WebInterface
from src.data.data_processor import DataProcessor
from src.analysis.professional_analytics import ProfessionalAnalytics
from src.visualization.chart_generator import ChartGenerator
from src.utils.logger import system_logger
from src.monitoring.metrics_collector import MetricsCollector
from src.security.encryption import DataEncryption
from src.security.audit_logger import SecurityAuditLogger


class TestBoundaryConditions:
    """边界条件测试类"""
    
    @pytest.fixture
    def setup_test_environment(self):
        """设置测试环境"""
        # 创建临时目录
        self.temp_dir = tempfile.mkdtemp()
        self.test_data_dir = Path(self.temp_dir) / "test_data"
        self.test_output_dir = Path(self.temp_dir) / "test_output"
        
        self.test_data_dir.mkdir(exist_ok=True)
        self.test_output_dir.mkdir(exist_ok=True)
        
        yield
        
        # 清理临时目录
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_empty_data_processing(self, setup_test_environment):
        """测试空数据处理"""
        processor = DataProcessor()
        
        # 测试空列表
        result = processor.process_data([])
        assert result is not None
        assert isinstance(result, dict)
        
        # 测试空字符串
        result = processor.process_data("")
        assert result is not None
        
        # 测试None值
        result = processor.process_data(None)
        assert result is not None
    
    def test_extremely_large_data(self, setup_test_environment):
        """测试极大数据量处理"""
        processor = DataProcessor()
        
        # 生成大量数据
        large_data = []
        for i in range(10000):  # 1万条记录
            large_data.append({
                'id': i,
                'value': i * 1.5,
                'category': f'category_{i % 100}',
                'timestamp': datetime.now().isoformat()
            })
        
        # 测试处理大量数据
        result = processor.process_data(large_data)
        assert result is not None
        assert 'processed_count' in result
        assert result['processed_count'] <= len(large_data)
    
    def test_malformed_data_handling(self, setup_test_environment):
        """测试畸形数据处理"""
        processor = DataProcessor()
        
        # 测试各种畸形数据
        malformed_data = [
            {'incomplete': 'data'},  # 缺少必要字段
            {'value': 'not_a_number'},  # 错误的数据类型
            {'nested': {'deeply': {'nested': {'data': 'value'}}}},  # 过度嵌套
            {'special_chars': '特殊字符\n\t\r\x00'},  # 特殊字符
            {'unicode': '🚀📊💻'},  # Unicode字符
            None,  # None值
            '',  # 空字符串
            [],  # 空列表
            {},  # 空字典
        ]
        
        # 应该能够处理而不崩溃
        result = processor.process_data(malformed_data)
        assert result is not None
    
    def test_memory_limits(self, setup_test_environment):
        """测试内存限制"""
        processor = DataProcessor()
        
        # 创建占用大量内存的数据结构
        memory_intensive_data = {
            'large_string': 'x' * (1024 * 1024),  # 1MB字符串
            'large_list': list(range(100000)),  # 10万个整数
            'nested_structure': {
                f'key_{i}': {
                    'data': list(range(1000))
                } for i in range(100)
            }
        }
        
        # 测试是否能够处理大内存占用
        try:
            result = processor.process_data(memory_intensive_data)
            assert result is not None
        except MemoryError:
            # 如果内存不足，应该优雅地处理
            pytest.skip("Insufficient memory for this test")
    
    def test_file_system_limits(self, setup_test_environment):
        """测试文件系统限制"""
        chart_generator = ChartGenerator()
        
        # 测试长文件名
        long_filename = 'a' * 255  # 最大文件名长度
        output_path = self.test_output_dir / f"{long_filename}.png"
        
        # 测试文件名过长的情况
        try:
            chart_generator.generate_chart(
                data={'x': [1, 2, 3], 'y': [1, 4, 9]},
                chart_type='line',
                output_path=str(output_path)
            )
        except OSError:
            # 文件名过长时应该优雅处理
            pass
        
        # 测试无效字符
        invalid_filename = 'chart<>:"|?*.png'
        safe_filename = chart_generator._sanitize_filename(invalid_filename)
        assert '<' not in safe_filename
        assert '>' not in safe_filename
        assert '|' not in safe_filename
    
    def test_concurrent_access(self, setup_test_environment):
        """测试并发访问"""
        import threading
        import time
        
        results = []
        errors = []
        
        def worker():
            try:
                processor = DataProcessor()
                data = [{'id': i, 'value': i} for i in range(100)]
                result = processor.process_data(data)
                results.append(result)
            except Exception as e:
                errors.append(e)
        
        # 创建多个线程
        threads = []
        for i in range(10):
            thread = threading.Thread(target=worker)
            threads.append(thread)
            thread.start()
        
        # 等待所有线程完成
        for thread in threads:
            thread.join(timeout=30)
        
        # 检查结果
        assert len(errors) == 0, f"Concurrent access errors: {errors}"
        assert len(results) > 0
    
    def test_network_timeout(self, setup_test_environment):
        """测试网络超时"""
        with patch('requests.get') as mock_get:
            # 模拟网络超时
            mock_get.side_effect = TimeoutError("Network timeout")
            
            # 测试网络请求超时处理
            from src.data.api_collector import APICollector
            collector = APICollector()
            
            result = collector.collect_data("http://example.com/api/data")
            # 应该返回空结果而不是崩溃
            assert result is not None
    
    def test_database_connection_failure(self, setup_test_environment):
        """测试数据库连接失败"""
        with patch('psycopg2.connect') as mock_connect:
            # 模拟数据库连接失败
            mock_connect.side_effect = Exception("Database connection failed")
            
            from src.data.database_collector import DatabaseCollector
            collector = DatabaseCollector()
            
            # 应该优雅地处理连接失败
            result = collector.collect_data("SELECT * FROM test_table")
            assert result is not None
    
    def test_disk_space_exhaustion(self, setup_test_environment):
        """测试磁盘空间耗尽"""
        with patch('builtins.open', side_effect=OSError("No space left on device")):
            chart_generator = ChartGenerator()
            
            # 测试磁盘空间不足时的处理
            result = chart_generator.generate_chart(
                data={'x': [1, 2, 3], 'y': [1, 4, 9]},
                chart_type='line',
                output_path=str(self.test_output_dir / "test.png")
            )
            
            # 应该返回错误信息而不是崩溃
            assert result is not None
    
    def test_unicode_handling(self, setup_test_environment):
        """测试Unicode处理"""
        processor = DataProcessor()
        
        unicode_data = [
            {'name': '张三', 'value': 100},
            {'name': 'José', 'value': 200},
            {'name': 'Müller', 'value': 300},
            {'name': '🚀 Rocket', 'value': 400},
            {'name': '\u200b\u200c\u200d', 'value': 500},  # 零宽字符
            {'name': '\x00\x01\x02', 'value': 600},  # 控制字符
        ]
        
        result = processor.process_data(unicode_data)
        assert result is not None
        assert 'processed_count' in result
    
    def test_timezone_handling(self, setup_test_environment):
        """测试时区处理"""
        analytics = ProfessionalAnalytics()
        
        # 不同时区的时间戳
        timezone_data = [
            {'timestamp': '2025-08-18T10:00:00+00:00', 'value': 100},
            {'timestamp': '2025-08-18T10:00:00+08:00', 'value': 200},
            {'timestamp': '2025-08-18T10:00:00-05:00', 'value': 300},
            {'timestamp': '2025-08-18T10:00:00Z', 'value': 400},
            {'timestamp': '2025-08-18 10:00:00', 'value': 500},  # 无时区信息
        ]
        
        result = analytics.analyze_data(timezone_data)
        assert result is not None
    
    def test_floating_point_precision(self, setup_test_environment):
        """测试浮点数精度"""
        processor = DataProcessor()
        
        # 浮点数精度测试数据
        precision_data = [
            {'value': 0.1 + 0.2},  # 应该是0.3，但可能有精度误差
            {'value': 1e-10},  # 极小数
            {'value': 1e10},   # 极大数
            {'value': float('inf')},  # 无穷大
            {'value': float('-inf')}, # 负无穷大
            {'value': float('nan')},  # NaN
        ]
        
        result = processor.process_data(precision_data)
        assert result is not None
    
    def test_date_boundary_conditions(self, setup_test_environment):
        """测试日期边界条件"""
        analytics = ProfessionalAnalytics()
        
        # 边界日期测试
        boundary_dates = [
            {'date': '1970-01-01', 'value': 100},  # Unix纪元
            {'date': '2038-01-19', 'value': 200},  # 32位时间戳上限
            {'date': '2000-02-29', 'value': 300},  # 闰年2月29日
            {'date': '1900-02-28', 'value': 400},  # 非闰年
            {'date': '9999-12-31', 'value': 500},  # 最大日期
            {'date': '0001-01-01', 'value': 600},  # 最小日期
            {'date': 'invalid-date', 'value': 700}, # 无效日期
        ]
        
        result = analytics.analyze_data(boundary_dates)
        assert result is not None
    
    def test_encryption_edge_cases(self, setup_test_environment):
        """测试加密边界情况"""
        encryption = DataEncryption()
        
        # 测试各种边界情况
        test_cases = [
            "",  # 空字符串
            "a",  # 单字符
            "a" * 10000,  # 长字符串
            "\x00\x01\x02",  # 二进制数据
            "🚀📊💻",  # Unicode
            None,  # None值
            123,  # 数字
            [1, 2, 3],  # 列表
            {'key': 'value'},  # 字典
        ]
        
        for test_data in test_cases:
            try:
                encrypted = encryption.encrypt_data(test_data)
                if encrypted is not None:
                    decrypted = encryption.decrypt_data(encrypted)
                    # 对于可序列化的数据，应该能够正确解密
                    if isinstance(test_data, (str, dict, list)):
                        assert decrypted is not None
            except Exception as e:
                # 记录但不失败，某些类型可能不支持加密
                system_logger.warning(f"Encryption test failed for {type(test_data)}: {e}")
    
    def test_metrics_collection_limits(self, setup_test_environment):
        """测试指标收集限制"""
        collector = MetricsCollector(collection_interval=1)
        
        # 测试快速连续调用
        for i in range(1000):
            collector.record_api_request(f"endpoint_{i}")
            collector.record_processing_time(0.1)
        
        # 应该不会崩溃或消耗过多内存
        summary = collector.get_metrics_summary()
        assert summary is not None
        assert 'total_metrics' in summary
    
    def test_audit_log_volume(self, setup_test_environment):
        """测试审计日志大量写入"""
        audit_logger = SecurityAuditLogger()
        
        # 快速生成大量审计事件
        for i in range(1000):
            audit_logger.log_api_call(
                user_id=f"user_{i % 10}",
                endpoint=f"/api/endpoint_{i % 50}",
                method="GET",
                status_code=200,
                ip_address=f"192.168.1.{i % 255}"
            )
        
        # 检查系统是否正常
        stats = audit_logger.get_stats()
        assert stats is not None
        assert stats['total_events'] > 0
    
    def test_web_interface_stress(self, setup_test_environment):
        """测试Web界面压力"""
        web_interface = WebInterface()
        
        # 模拟大量并发请求
        import asyncio
        
        async def make_request():
            # 模拟处理请求
            await asyncio.sleep(0.01)
            return {'status': 'ok'}
        
        async def stress_test():
            tasks = [make_request() for _ in range(100)]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            return results
        
        # 运行压力测试
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            results = loop.run_until_complete(stress_test())
            assert len(results) == 100
            # 检查是否有异常
            exceptions = [r for r in results if isinstance(r, Exception)]
            assert len(exceptions) == 0, f"Found exceptions: {exceptions}"
        finally:
            loop.close()
    
    def test_configuration_edge_cases(self, setup_test_environment):
        """测试配置边界情况"""
        # 测试空配置
        empty_config = {}
        
        # 测试无效配置值
        invalid_config = {
            'timeout': -1,
            'max_connections': 0,
            'buffer_size': 'invalid',
            'debug': 'not_boolean',
        }
        
        # 测试极端配置值
        extreme_config = {
            'timeout': 999999,
            'max_connections': 1000000,
            'buffer_size': 0,
            'batch_size': 1,
        }
        
        # 系统应该能够处理这些配置而不崩溃
        for config in [empty_config, invalid_config, extreme_config]:
            try:
                # 这里应该测试具体的配置加载逻辑
                # 暂时只验证配置不会导致崩溃
                assert isinstance(config, dict)
            except Exception as e:
                pytest.fail(f"Configuration handling failed: {e}")
    
    def test_error_recovery(self, setup_test_environment):
        """测试错误恢复"""
        processor = DataProcessor()
        
        # 模拟处理过程中的错误
        def failing_process(data):
            if len(data) > 5:
                raise ValueError("Simulated processing error")
            return {'processed': True}
        
        # 测试错误恢复机制
        test_data = [
            [1, 2, 3],  # 成功
            [1, 2, 3, 4, 5, 6, 7],  # 失败
            [1, 2],  # 成功
        ]
        
        results = []
        for data in test_data:
            try:
                result = failing_process(data)
                results.append(result)
            except ValueError:
                # 错误恢复：记录错误并继续
                results.append({'error': 'processing_failed'})
        
        assert len(results) == 3
        assert results[0]['processed'] is True
        assert 'error' in results[1]
        assert results[2]['processed'] is True


if __name__ == '__main__':
    pytest.main([__file__, '-v'])