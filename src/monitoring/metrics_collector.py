#!/usr/bin/env python3
"""
高级监控指标收集系统
支持自定义指标、业务指标和系统指标的统一收集
"""

import time
import psutil
import asyncio
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from collections import defaultdict, deque
import threading
import json

try:
    from prometheus_client import Counter, Histogram, Gauge, Summary, CollectorRegistry, generate_latest
    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False

from src.utils.logger import system_logger


@dataclass
class MetricPoint:
    """指标数据点"""
    name: str
    value: float
    timestamp: datetime
    labels: Dict[str, str] = field(default_factory=dict)
    metric_type: str = "gauge"  # gauge, counter, histogram, summary


@dataclass
class MetricConfig:
    """指标配置"""
    name: str
    description: str
    metric_type: str = "gauge"
    labels: List[str] = field(default_factory=list)
    buckets: Optional[List[float]] = None  # for histogram
    enabled: bool = True


class CustomMetrics:
    """自定义指标管理器"""
    
    def __init__(self):
        self.registry = CollectorRegistry() if PROMETHEUS_AVAILABLE else None
        self.metrics: Dict[str, Any] = {}
        self.configs: Dict[str, MetricConfig] = {}
        self._setup_default_metrics()
    
    def _setup_default_metrics(self):
        """设置默认指标"""
        default_configs = [
            # 业务指标
            MetricConfig("reports_generated_total", "生成报告总数", "counter"),
            MetricConfig("active_users_count", "活跃用户数", "gauge"),
            MetricConfig("api_requests_total", "API请求总数", "counter", ["method", "endpoint"]),
            MetricConfig("websocket_connections", "WebSocket连接数", "gauge"),
            MetricConfig("data_processing_duration", "数据处理耗时", "histogram", 
                        buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0]),
            
            # 系统指标
            MetricConfig("system_cpu_usage", "系统CPU使用率", "gauge"),
            MetricConfig("system_memory_usage", "系统内存使用率", "gauge"),
            MetricConfig("system_disk_usage", "系统磁盘使用率", "gauge"),
            MetricConfig("database_connections", "数据库连接数", "gauge"),
            MetricConfig("cache_hit_ratio", "缓存命中率", "gauge"),
            
            # 应用指标
            MetricConfig("error_rate", "错误率", "gauge"),
            MetricConfig("response_time_95th", "响应时间95分位", "gauge"),
            MetricConfig("throughput_qps", "系统吞吐量QPS", "gauge"),
            MetricConfig("queue_size", "任务队列大小", "gauge"),
        ]
        
        for config in default_configs:
            self.register_metric(config)
    
    def register_metric(self, config: MetricConfig):
        """注册指标"""
        self.configs[config.name] = config
        
        if not PROMETHEUS_AVAILABLE or not config.enabled:
            return
        
        try:
            if config.metric_type == "counter":
                metric = Counter(
                    config.name, 
                    config.description,
                    labelnames=config.labels,
                    registry=self.registry
                )
            elif config.metric_type == "gauge":
                metric = Gauge(
                    config.name,
                    config.description,
                    labelnames=config.labels,
                    registry=self.registry
                )
            elif config.metric_type == "histogram":
                metric = Histogram(
                    config.name,
                    config.description,
                    labelnames=config.labels,
                    buckets=config.buckets or [0.1, 0.5, 1.0, 2.5, 5.0, 10.0],
                    registry=self.registry
                )
            elif config.metric_type == "summary":
                metric = Summary(
                    config.name,
                    config.description,
                    labelnames=config.labels,
                    registry=self.registry
                )
            else:
                system_logger.warning(f"Unknown metric type: {config.metric_type}")
                return
            
            self.metrics[config.name] = metric
            system_logger.info(f"Registered metric: {config.name}")
            
        except Exception as e:
            system_logger.error(f"Failed to register metric {config.name}: {e}")
    
    def increment_counter(self, name: str, labels: Dict[str, str] = None, value: float = 1):
        """增加计数器"""
        if name in self.metrics and PROMETHEUS_AVAILABLE:
            try:
                if labels:
                    self.metrics[name].labels(**labels).inc(value)
                else:
                    self.metrics[name].inc(value)
            except Exception as e:
                system_logger.error(f"Error incrementing counter {name}: {e}")
    
    def set_gauge(self, name: str, value: float, labels: Dict[str, str] = None):
        """设置仪表盘值"""
        if name in self.metrics and PROMETHEUS_AVAILABLE:
            try:
                if labels:
                    self.metrics[name].labels(**labels).set(value)
                else:
                    self.metrics[name].set(value)
            except Exception as e:
                system_logger.error(f"Error setting gauge {name}: {e}")
    
    def observe_histogram(self, name: str, value: float, labels: Dict[str, str] = None):
        """记录直方图观察值"""
        if name in self.metrics and PROMETHEUS_AVAILABLE:
            try:
                if labels:
                    self.metrics[name].labels(**labels).observe(value)
                else:
                    self.metrics[name].observe(value)
            except Exception as e:
                system_logger.error(f"Error observing histogram {name}: {e}")
    
    def get_prometheus_metrics(self) -> str:
        """获取Prometheus格式的指标"""
        if PROMETHEUS_AVAILABLE and self.registry:
            return generate_latest(self.registry).decode('utf-8')
        return ""


class MetricsCollector:
    """高级监控指标收集器"""
    
    def __init__(self, collection_interval: int = 30):
        self.collection_interval = collection_interval
        self.custom_metrics = CustomMetrics()
        self.data_points: deque = deque(maxlen=10000)  # 保留最近10000个数据点
        self.collectors: Dict[str, Callable] = {}
        self.running = False
        self._thread = None
        
        # 业务指标统计
        self.business_stats = {
            'reports_generated': 0,
            'api_requests': defaultdict(int),
            'websocket_connections': 0,
            'active_users': set(),
            'errors': defaultdict(int),
            'processing_times': deque(maxlen=1000)
        }
        
        self._setup_default_collectors()
    
    def _setup_default_collectors(self):
        """设置默认收集器"""
        self.collectors.update({
            'system_metrics': self._collect_system_metrics,
            'business_metrics': self._collect_business_metrics,
            'application_metrics': self._collect_application_metrics,
            'database_metrics': self._collect_database_metrics,
        })
    
    def register_collector(self, name: str, collector_func: Callable):
        """注册自定义收集器"""
        self.collectors[name] = collector_func
        system_logger.info(f"Registered collector: {name}")
    
    def start_collection(self):
        """启动指标收集"""
        if self.running:
            return
        
        self.running = True
        self._thread = threading.Thread(target=self._collection_loop, daemon=True)
        self._thread.start()
        system_logger.info("Metrics collection started")
    
    def stop_collection(self):
        """停止指标收集"""
        self.running = False
        if self._thread:
            self._thread.join(timeout=5)
        system_logger.info("Metrics collection stopped")
    
    def _collection_loop(self):
        """收集循环"""
        while self.running:
            try:
                self._collect_all_metrics()
                time.sleep(self.collection_interval)
            except Exception as e:
                system_logger.error(f"Error in metrics collection loop: {e}")
                time.sleep(5)  # 错误时短暂休息
    
    def _collect_all_metrics(self):
        """收集所有指标"""
        timestamp = datetime.now()
        
        for name, collector in self.collectors.items():
            try:
                metrics = collector()
                for metric in metrics:
                    metric.timestamp = timestamp
                    self.data_points.append(metric)
                    
                    # 更新Prometheus指标
                    self._update_prometheus_metric(metric)
                    
            except Exception as e:
                system_logger.error(f"Error collecting metrics from {name}: {e}")
    
    def _update_prometheus_metric(self, metric: MetricPoint):
        """更新Prometheus指标"""
        try:
            if metric.metric_type == "counter":
                self.custom_metrics.increment_counter(metric.name, metric.labels, metric.value)
            elif metric.metric_type == "gauge":
                self.custom_metrics.set_gauge(metric.name, metric.value, metric.labels)
            elif metric.metric_type == "histogram":
                self.custom_metrics.observe_histogram(metric.name, metric.value, metric.labels)
        except Exception as e:
            system_logger.error(f"Error updating Prometheus metric {metric.name}: {e}")
    
    def _collect_system_metrics(self) -> List[MetricPoint]:
        """收集系统指标"""
        metrics = []
        
        try:
            # CPU使用率
            cpu_percent = psutil.cpu_percent(interval=1)
            metrics.append(MetricPoint("system_cpu_usage", cpu_percent, datetime.now()))
            
            # 内存使用率
            memory = psutil.virtual_memory()
            metrics.append(MetricPoint("system_memory_usage", memory.percent, datetime.now()))
            
            # 磁盘使用率
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            metrics.append(MetricPoint("system_disk_usage", disk_percent, datetime.now()))
            
            # 网络IO
            network = psutil.net_io_counters()
            metrics.extend([
                MetricPoint("network_bytes_sent", network.bytes_sent, datetime.now()),
                MetricPoint("network_bytes_recv", network.bytes_recv, datetime.now()),
            ])
            
        except Exception as e:
            system_logger.error(f"Error collecting system metrics: {e}")
        
        return metrics
    
    def _collect_business_metrics(self) -> List[MetricPoint]:
        """收集业务指标"""
        metrics = []
        
        try:
            # 生成报告数量
            metrics.append(MetricPoint(
                "reports_generated_total", 
                self.business_stats['reports_generated'], 
                datetime.now()
            ))
            
            # 活跃用户数
            metrics.append(MetricPoint(
                "active_users_count", 
                len(self.business_stats['active_users']), 
                datetime.now()
            ))
            
            # WebSocket连接数
            metrics.append(MetricPoint(
                "websocket_connections", 
                self.business_stats['websocket_connections'], 
                datetime.now()
            ))
            
            # API请求统计
            for endpoint, count in self.business_stats['api_requests'].items():
                metrics.append(MetricPoint(
                    "api_requests_total", 
                    count, 
                    datetime.now(),
                    {"endpoint": endpoint}
                ))
            
            # 处理时间统计
            if self.business_stats['processing_times']:
                times = list(self.business_stats['processing_times'])
                avg_time = sum(times) / len(times)
                p95_time = sorted(times)[int(len(times) * 0.95)]
                
                metrics.extend([
                    MetricPoint("avg_processing_time", avg_time, datetime.now()),
                    MetricPoint("response_time_95th", p95_time, datetime.now()),
                ])
            
        except Exception as e:
            system_logger.error(f"Error collecting business metrics: {e}")
        
        return metrics
    
    def _collect_application_metrics(self) -> List[MetricPoint]:
        """收集应用指标"""
        metrics = []
        
        try:
            # 错误率计算
            total_requests = sum(self.business_stats['api_requests'].values())
            total_errors = sum(self.business_stats['errors'].values())
            error_rate = (total_errors / total_requests * 100) if total_requests > 0 else 0
            
            metrics.append(MetricPoint("error_rate", error_rate, datetime.now()))
            
            # 吞吐量计算 (简化版本)
            recent_requests = total_requests  # 这里应该是最近一分钟的请求数
            qps = recent_requests / 60
            metrics.append(MetricPoint("throughput_qps", qps, datetime.now()))
            
        except Exception as e:
            system_logger.error(f"Error collecting application metrics: {e}")
        
        return metrics
    
    def _collect_database_metrics(self) -> List[MetricPoint]:
        """收集数据库指标"""
        metrics = []
        
        try:
            # 这里可以添加数据库连接池、查询时间等指标
            # 暂时使用模拟数据
            metrics.append(MetricPoint("database_connections", 10, datetime.now()))
            metrics.append(MetricPoint("cache_hit_ratio", 85.5, datetime.now()))
            
        except Exception as e:
            system_logger.error(f"Error collecting database metrics: {e}")
        
        return metrics
    
    def record_report_generated(self):
        """记录报告生成"""
        self.business_stats['reports_generated'] += 1
    
    def record_api_request(self, endpoint: str):
        """记录API请求"""
        self.business_stats['api_requests'][endpoint] += 1
    
    def record_websocket_connection(self, delta: int = 1):
        """记录WebSocket连接变化"""
        self.business_stats['websocket_connections'] += delta
    
    def record_active_user(self, user_id: str):
        """记录活跃用户"""
        self.business_stats['active_users'].add(user_id)
    
    def record_error(self, error_type: str):
        """记录错误"""
        self.business_stats['errors'][error_type] += 1
    
    def record_processing_time(self, duration: float):
        """记录处理时间"""
        self.business_stats['processing_times'].append(duration)
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """获取指标摘要"""
        recent_points = list(self.data_points)[-100:]  # 最近100个数据点
        
        summary = {
            'total_metrics': len(recent_points),
            'collection_interval': self.collection_interval,
            'collectors_count': len(self.collectors),
            'business_stats': dict(self.business_stats),
            'last_collection': recent_points[-1].timestamp if recent_points else None,
        }
        
        # 转换set为list以便JSON序列化
        if 'active_users' in summary['business_stats']:
            summary['business_stats']['active_users'] = list(summary['business_stats']['active_users'])
        
        return summary
    
    def get_prometheus_metrics(self) -> str:
        """获取Prometheus格式指标"""
        return self.custom_metrics.get_prometheus_metrics()


# 全局指标收集器实例
metrics_collector = MetricsCollector()

def get_metrics_collector() -> MetricsCollector:
    """获取全局指标收集器"""
    return metrics_collector