"""
Prometheus指标收集模块
业务分析报告自动化系统监控指标
"""

import time
import logging
from typing import Dict, Any, Optional
from functools import wraps
from pathlib import Path
import sys

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# 尝试导入Prometheus客户端
try:
    from prometheus_client import (
        Counter, Histogram, Gauge, Summary, Info,
        generate_latest, CONTENT_TYPE_LATEST,
        CollectorRegistry, multiprocess, REGISTRY
    )
    HAS_PROMETHEUS = True
except ImportError:
    HAS_PROMETHEUS = False

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MetricsCollector:
    """
    Prometheus指标收集器
    收集应用程序的各种性能和业务指标
    """
    
    def __init__(self, registry=None):
        """
        初始化指标收集器
        
        Args:
            registry: Prometheus注册表，默认使用全局注册表
        """
        self.enabled = HAS_PROMETHEUS
        
        if not self.enabled:
            logger.warning("Prometheus客户端未安装，指标收集将被禁用")
            self.registry = None
            return
        
        self.registry = registry or REGISTRY
        
        # HTTP请求指标
        self.http_requests_total = Counter(
            'http_requests_total',
            'HTTP请求总数',
            ['method', 'endpoint', 'status'],
            registry=self.registry
        )
        
        self.http_request_duration_seconds = Histogram(
            'http_request_duration_seconds',
            'HTTP请求响应时间',
            ['method', 'endpoint'],
            registry=self.registry
        )
        
        # 应用程序指标
        self.app_info = Info(
            'app_info',
            '应用程序信息',
            registry=self.registry
        )
        
        # WebSocket指标
        self.websocket_connections_active = Gauge(
            'websocket_connections_active',
            '活跃WebSocket连接数',
            registry=self.registry
        )
        
        self.websocket_messages_sent_total = Counter(
            'websocket_messages_sent_total',
            '发送的WebSocket消息总数',
            ['message_type'],
            registry=self.registry
        )
        
        self.websocket_messages_received_total = Counter(
            'websocket_messages_received_total',
            '接收的WebSocket消息总数',
            ['message_type'],
            registry=self.registry
        )
        
        # 报告生成指标
        self.report_generation_total = Counter(
            'report_generation_total',
            '报告生成总数',
            ['report_type', 'industry'],
            registry=self.registry
        )
        
        self.report_generation_failed_total = Counter(
            'report_generation_failed_total',
            '报告生成失败总数',
            ['report_type', 'error_type'],
            registry=self.registry
        )
        
        self.report_generation_duration_seconds = Histogram(
            'report_generation_duration_seconds',
            '报告生成耗时',
            ['report_type'],
            registry=self.registry
        )
        
        # 数据分析指标
        self.analysis_tasks_total = Counter(
            'analysis_tasks_total',
            '分析任务总数',
            ['task_type'],
            registry=self.registry
        )
        
        self.analysis_tasks_pending = Gauge(
            'analysis_tasks_pending',
            '待处理的分析任务数',
            registry=self.registry
        )
        
        self.analysis_tasks_duration_seconds = Histogram(
            'analysis_tasks_duration_seconds',
            '分析任务执行时间',
            ['task_type'],
            registry=self.registry
        )
        
        # 用户认证指标
        self.login_attempts_total = Counter(
            'login_attempts_total',
            '登录尝试总数',
            ['result'],
            registry=self.registry
        )
        
        self.login_attempts_failed_total = Counter(
            'login_attempts_failed_total',
            '登录失败总数',
            ['reason'],
            registry=self.registry
        )
        
        self.active_users = Gauge(
            'active_users',
            '活跃用户数',
            registry=self.registry
        )
        
        # 文件操作指标
        self.file_uploads_total = Counter(
            'file_uploads_total',
            '文件上传总数',
            ['file_type'],
            registry=self.registry
        )
        
        self.file_upload_size_bytes = Histogram(
            'file_upload_size_bytes',
            '上传文件大小',
            ['file_type'],
            registry=self.registry
        )
        
        # 数据库指标（如果使用数据库）
        self.database_connections_active = Gauge(
            'database_connections_active',
            '活跃数据库连接数',
            registry=self.registry
        )
        
        self.database_query_duration_seconds = Histogram(
            'database_query_duration_seconds',
            '数据库查询耗时',
            ['operation'],
            registry=self.registry
        )
        
        # 缓存指标（如果使用Redis）
        self.cache_operations_total = Counter(
            'cache_operations_total',
            '缓存操作总数',
            ['operation', 'result'],
            registry=self.registry
        )
        
        self.cache_hit_ratio = Gauge(
            'cache_hit_ratio',
            '缓存命中率',
            registry=self.registry
        )
        
        # 设置应用信息
        self.set_app_info()
        
        logger.info("Prometheus指标收集器初始化完成")
    
    def set_app_info(self):
        """设置应用程序信息"""
        if not self.enabled:
            return
            
        self.app_info.info({
            'name': '业务分析报告自动化系统',
            'version': 'v4.0',
            'python_version': sys.version.split()[0],
        })
    
    def record_http_request(self, method: str, endpoint: str, status: int, duration: float):
        """
        记录HTTP请求指标
        
        Args:
            method: HTTP方法
            endpoint: 端点路径
            status: 状态码
            duration: 请求耗时（秒）
        """
        if not self.enabled:
            return
            
        self.http_requests_total.labels(
            method=method,
            endpoint=endpoint,
            status=str(status)
        ).inc()
        
        self.http_request_duration_seconds.labels(
            method=method,
            endpoint=endpoint
        ).observe(duration)
    
    def record_websocket_connection(self, action: str):
        """
        记录WebSocket连接变化
        
        Args:
            action: 'connect' 或 'disconnect'
        """
        if not self.enabled:
            return
            
        if action == 'connect':
            self.websocket_connections_active.inc()
        elif action == 'disconnect':
            self.websocket_connections_active.dec()
    
    def record_websocket_message(self, direction: str, message_type: str):
        """
        记录WebSocket消息
        
        Args:
            direction: 'sent' 或 'received'
            message_type: 消息类型
        """
        if not self.enabled:
            return
            
        if direction == 'sent':
            self.websocket_messages_sent_total.labels(
                message_type=message_type
            ).inc()
        elif direction == 'received':
            self.websocket_messages_received_total.labels(
                message_type=message_type
            ).inc()
    
    def record_report_generation(self, report_type: str, industry: str, 
                                duration: Optional[float] = None, 
                                success: bool = True, 
                                error_type: Optional[str] = None):
        """
        记录报告生成指标
        
        Args:
            report_type: 报告类型
            industry: 行业
            duration: 生成耗时
            success: 是否成功
            error_type: 错误类型（如果失败）
        """
        if not self.enabled:
            return
            
        if success:
            self.report_generation_total.labels(
                report_type=report_type,
                industry=industry
            ).inc()
            
            if duration is not None:
                self.report_generation_duration_seconds.labels(
                    report_type=report_type
                ).observe(duration)
        else:
            self.report_generation_failed_total.labels(
                report_type=report_type,
                error_type=error_type or 'unknown'
            ).inc()
    
    def record_analysis_task(self, task_type: str, duration: Optional[float] = None):
        """
        记录分析任务指标
        
        Args:
            task_type: 任务类型
            duration: 执行时间
        """
        if not self.enabled:
            return
            
        self.analysis_tasks_total.labels(task_type=task_type).inc()
        
        if duration is not None:
            self.analysis_tasks_duration_seconds.labels(
                task_type=task_type
            ).observe(duration)
    
    def update_pending_tasks(self, count: int):
        """
        更新待处理任务数
        
        Args:
            count: 待处理任务数量
        """
        if not self.enabled:
            return
            
        self.analysis_tasks_pending.set(count)
    
    def record_login_attempt(self, success: bool, reason: Optional[str] = None):
        """
        记录登录尝试
        
        Args:
            success: 是否成功
            reason: 失败原因
        """
        if not self.enabled:
            return
            
        result = 'success' if success else 'failed'
        self.login_attempts_total.labels(result=result).inc()
        
        if not success and reason:
            self.login_attempts_failed_total.labels(reason=reason).inc()
    
    def update_active_users(self, count: int):
        """
        更新活跃用户数
        
        Args:
            count: 活跃用户数量
        """
        if not self.enabled:
            return
            
        self.active_users.set(count)
    
    def record_file_upload(self, file_type: str, file_size: int):
        """
        记录文件上传
        
        Args:
            file_type: 文件类型
            file_size: 文件大小（字节）
        """
        if not self.enabled:
            return
            
        self.file_uploads_total.labels(file_type=file_type).inc()
        self.file_upload_size_bytes.labels(file_type=file_type).observe(file_size)
    
    def record_database_operation(self, operation: str, duration: float):
        """
        记录数据库操作
        
        Args:
            operation: 操作类型
            duration: 操作耗时
        """
        if not self.enabled:
            return
            
        self.database_query_duration_seconds.labels(
            operation=operation
        ).observe(duration)
    
    def update_database_connections(self, count: int):
        """
        更新数据库连接数
        
        Args:
            count: 连接数量
        """
        if not self.enabled:
            return
            
        self.database_connections_active.set(count)
    
    def record_cache_operation(self, operation: str, hit: bool):
        """
        记录缓存操作
        
        Args:
            operation: 操作类型 (get, set, delete)
            hit: 是否命中
        """
        if not self.enabled:
            return
            
        result = 'hit' if hit else 'miss'
        self.cache_operations_total.labels(
            operation=operation,
            result=result
        ).inc()
    
    def update_cache_hit_ratio(self, ratio: float):
        """
        更新缓存命中率
        
        Args:
            ratio: 命中率 (0.0-1.0)
        """
        if not self.enabled:
            return
            
        self.cache_hit_ratio.set(ratio)
    
    def get_metrics(self) -> str:
        """
        获取Prometheus格式的指标数据
        
        Returns:
            str: Prometheus格式的指标数据
        """
        if not self.enabled:
            return "# Prometheus metrics disabled\n"
            
        return generate_latest(self.registry)


# 全局指标收集器实例
metrics_collector = MetricsCollector()


def track_time(metric_name: str = None, labels: Dict[str, str] = None):
    """
    装饰器：跟踪函数执行时间
    
    Args:
        metric_name: 指标名称
        labels: 指标标签
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not metrics_collector.enabled:
                return func(*args, **kwargs)
                
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                
                # 记录成功的执行时间
                if hasattr(metrics_collector, metric_name):
                    metric = getattr(metrics_collector, metric_name)
                    if labels:
                        metric.labels(**labels).observe(duration)
                    else:
                        metric.observe(duration)
                
                return result
            except Exception as e:
                duration = time.time() - start_time
                # 可以在这里记录错误指标
                raise e
        return wrapper
    return decorator


def count_calls(metric_name: str = None, labels: Dict[str, str] = None):
    """
    装饰器：统计函数调用次数
    
    Args:
        metric_name: 指标名称
        labels: 指标标签
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if metrics_collector.enabled and hasattr(metrics_collector, metric_name):
                metric = getattr(metrics_collector, metric_name)
                if labels:
                    metric.labels(**labels).inc()
                else:
                    metric.inc()
            
            return func(*args, **kwargs)
        return wrapper
    return decorator


# 便捷函数
def record_http_request(method: str, endpoint: str, status: int, duration: float):
    """记录HTTP请求指标"""
    metrics_collector.record_http_request(method, endpoint, status, duration)


def record_websocket_connection(action: str):
    """记录WebSocket连接变化"""
    metrics_collector.record_websocket_connection(action)


def record_report_generation(report_type: str, industry: str, duration: float = None, 
                           success: bool = True, error_type: str = None):
    """记录报告生成指标"""
    metrics_collector.record_report_generation(
        report_type, industry, duration, success, error_type
    )


def get_metrics() -> str:
    """获取所有指标数据"""
    return metrics_collector.get_metrics()


if __name__ == "__main__":
    # 测试指标收集器
    print("🧪 测试Prometheus指标收集器")
    
    # 模拟一些指标
    record_http_request("GET", "/api/info", 200, 0.1)
    record_http_request("POST", "/api/reports", 201, 0.5)
    record_websocket_connection("connect")
    record_report_generation("monthly", "retail", 2.5, True)
    
    print("✅ 指标记录完成")
    print(f"🔍 指标数据预览:")
    print(get_metrics()[:500] + "...")