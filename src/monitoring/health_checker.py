#!/usr/bin/env python3
"""
健康检查系统
提供应用程序和依赖服务的健康状态监控
"""

import asyncio
import time
import psutil
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import threading
import json

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

try:
    import psycopg2
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

from src.utils.logger import system_logger
from src.config.settings import settings


class HealthStatus(Enum):
    """健康状态"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


@dataclass
class HealthCheck:
    """健康检查项"""
    name: str
    description: str
    check_func: Callable
    timeout: int = 10
    interval: int = 30
    enabled: bool = True
    critical: bool = False  # 是否为关键检查项
    tags: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        self.last_check: Optional[datetime] = None
        self.last_status: HealthStatus = HealthStatus.UNKNOWN
        self.last_error: Optional[str] = None
        self.check_count: int = 0
        self.failure_count: int = 0


@dataclass
class HealthResult:
    """健康检查结果"""
    name: str
    status: HealthStatus
    message: str
    timestamp: datetime = field(default_factory=datetime.now)
    duration: float = 0.0
    details: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'name': self.name,
            'status': self.status.value,
            'message': self.message,
            'timestamp': self.timestamp.isoformat(),
            'duration': self.duration,
            'details': self.details
        }


class HealthChecker:
    """健康检查器"""
    
    def __init__(self, check_interval: int = 30):
        self.check_interval = check_interval
        self.checks: Dict[str, HealthCheck] = {}
        self.results: Dict[str, HealthResult] = {}
        self.running = False
        self._thread = None
        
        self._setup_default_checks()
    
    def _setup_default_checks(self):
        """设置默认健康检查"""
        # 系统资源检查
        self.register_check(HealthCheck(
            name="system_resources",
            description="系统资源检查",
            check_func=self._check_system_resources,
            critical=True,
            tags=["system", "resources"]
        ))
        
        # 磁盘空间检查
        self.register_check(HealthCheck(
            name="disk_space",
            description="磁盘空间检查",
            check_func=self._check_disk_space,
            critical=True,
            tags=["system", "disk"]
        ))
        
        # 数据库连接检查
        if POSTGRES_AVAILABLE:
            self.register_check(HealthCheck(
                name="database_connection",
                description="数据库连接检查",
                check_func=self._check_database_connection,
                critical=True,
                tags=["database", "postgres"]
            ))
        
        # Redis连接检查
        if REDIS_AVAILABLE:
            self.register_check(HealthCheck(
                name="redis_connection", 
                description="Redis连接检查",
                check_func=self._check_redis_connection,
                critical=False,
                tags=["cache", "redis"]
            ))
        
        # Web服务检查
        self.register_check(HealthCheck(
            name="web_service",
            description="Web服务健康检查",
            check_func=self._check_web_service,
            critical=True,
            tags=["web", "api"]
        ))
        
        # 内存泄漏检查
        self.register_check(HealthCheck(
            name="memory_leak",
            description="内存泄漏检查",
            check_func=self._check_memory_leak,
            interval=300,  # 5分钟检查一次
            tags=["system", "memory"]
        ))
    
    def register_check(self, check: HealthCheck):
        """注册健康检查"""
        self.checks[check.name] = check
        system_logger.info(f"Registered health check: {check.name}")
    
    def remove_check(self, name: str):
        """移除健康检查"""
        if name in self.checks:
            del self.checks[name]
            if name in self.results:
                del self.results[name]
            system_logger.info(f"Removed health check: {name}")
    
    def start_monitoring(self):
        """启动健康监控"""
        if self.running:
            return
        
        self.running = True
        self._thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self._thread.start()
        system_logger.info("Health monitoring started")
    
    def stop_monitoring(self):
        """停止健康监控"""
        self.running = False
        if self._thread:
            self._thread.join(timeout=5)
        system_logger.info("Health monitoring stopped")
    
    def _monitoring_loop(self):
        """监控循环"""
        while self.running:
            try:
                asyncio.run(self._run_all_checks())
                time.sleep(self.check_interval)
            except Exception as e:
                system_logger.error(f"Error in health monitoring loop: {e}")
                time.sleep(5)
    
    async def _run_all_checks(self):
        """运行所有健康检查"""
        tasks = []
        current_time = datetime.now()
        
        for check in self.checks.values():
            if not check.enabled:
                continue
            
            # 检查是否需要运行
            if (check.last_check is None or 
                (current_time - check.last_check).total_seconds() >= check.interval):
                tasks.append(self._run_single_check(check))
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _run_single_check(self, check: HealthCheck):
        """运行单个健康检查"""
        start_time = time.time()
        
        try:
            # 运行检查函数
            result = await asyncio.wait_for(
                asyncio.create_task(self._execute_check(check)),
                timeout=check.timeout
            )
            
            duration = time.time() - start_time
            
            # 更新检查状态
            check.last_check = datetime.now()
            check.check_count += 1
            check.last_status = result.status
            check.last_error = None if result.status == HealthStatus.HEALTHY else result.message
            
            if result.status != HealthStatus.HEALTHY:
                check.failure_count += 1
            
            result.duration = duration
            self.results[check.name] = result
            
            if result.status == HealthStatus.UNHEALTHY:
                system_logger.warning(f"Health check failed: {check.name} - {result.message}")
            
        except asyncio.TimeoutError:
            duration = time.time() - start_time
            result = HealthResult(
                name=check.name,
                status=HealthStatus.UNHEALTHY,
                message=f"Health check timeout after {check.timeout}s",
                duration=duration
            )
            
            check.last_check = datetime.now()
            check.check_count += 1
            check.failure_count += 1
            check.last_status = HealthStatus.UNHEALTHY
            check.last_error = result.message
            
            self.results[check.name] = result
            system_logger.error(f"Health check timeout: {check.name}")
            
        except Exception as e:
            duration = time.time() - start_time
            result = HealthResult(
                name=check.name,
                status=HealthStatus.UNHEALTHY,
                message=f"Health check error: {str(e)}",
                duration=duration
            )
            
            check.last_check = datetime.now()
            check.check_count += 1
            check.failure_count += 1
            check.last_status = HealthStatus.UNHEALTHY
            check.last_error = str(e)
            
            self.results[check.name] = result
            system_logger.error(f"Health check error: {check.name} - {e}")
    
    async def _execute_check(self, check: HealthCheck) -> HealthResult:
        """执行检查函数"""
        if asyncio.iscoroutinefunction(check.check_func):
            return await check.check_func()
        else:
            # 在线程池中运行同步函数
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, check.check_func)
    
    # 默认检查函数
    def _check_system_resources(self) -> HealthResult:
        """检查系统资源"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory_percent = psutil.virtual_memory().percent
            
            details = {
                'cpu_usage': cpu_percent,
                'memory_usage': memory_percent
            }
            
            if cpu_percent > 90:
                return HealthResult(
                    name="system_resources",
                    status=HealthStatus.UNHEALTHY,
                    message=f"CPU usage too high: {cpu_percent}%",
                    details=details
                )
            elif cpu_percent > 80 or memory_percent > 85:
                return HealthResult(
                    name="system_resources",
                    status=HealthStatus.DEGRADED,
                    message=f"High resource usage - CPU: {cpu_percent}%, Memory: {memory_percent}%",
                    details=details
                )
            else:
                return HealthResult(
                    name="system_resources",
                    status=HealthStatus.HEALTHY,
                    message=f"System resources normal - CPU: {cpu_percent}%, Memory: {memory_percent}%",
                    details=details
                )
                
        except Exception as e:
            return HealthResult(
                name="system_resources",
                status=HealthStatus.UNHEALTHY,
                message=f"Failed to check system resources: {e}"
            )
    
    def _check_disk_space(self) -> HealthResult:
        """检查磁盘空间"""
        try:
            disk_usage = psutil.disk_usage('/')
            used_percent = (disk_usage.used / disk_usage.total) * 100
            free_gb = disk_usage.free / (1024**3)
            
            details = {
                'used_percent': used_percent,
                'free_gb': round(free_gb, 2),
                'total_gb': round(disk_usage.total / (1024**3), 2)
            }
            
            if used_percent > 95:
                return HealthResult(
                    name="disk_space",
                    status=HealthStatus.UNHEALTHY,
                    message=f"Disk space critically low: {used_percent:.1f}% used",
                    details=details
                )
            elif used_percent > 90:
                return HealthResult(
                    name="disk_space",
                    status=HealthStatus.DEGRADED,
                    message=f"Disk space low: {used_percent:.1f}% used",
                    details=details
                )
            else:
                return HealthResult(
                    name="disk_space",
                    status=HealthStatus.HEALTHY,
                    message=f"Disk space normal: {used_percent:.1f}% used, {free_gb:.1f}GB free",
                    details=details
                )
                
        except Exception as e:
            return HealthResult(
                name="disk_space",
                status=HealthStatus.UNHEALTHY,
                message=f"Failed to check disk space: {e}"
            )
    
    def _check_database_connection(self) -> HealthResult:
        """检查数据库连接"""
        try:
            if not POSTGRES_AVAILABLE:
                return HealthResult(
                    name="database_connection",
                    status=HealthStatus.UNKNOWN,
                    message="PostgreSQL client not available"
                )
            
            # 从设置中获取数据库配置
            db_config = getattr(settings, 'DATABASE_URL', None)
            if not db_config:
                return HealthResult(
                    name="database_connection",
                    status=HealthStatus.DEGRADED,
                    message="Database configuration not found"
                )
            
            # 尝试连接数据库
            conn = psycopg2.connect(db_config)
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            cursor.close()
            conn.close()
            
            return HealthResult(
                name="database_connection",
                status=HealthStatus.HEALTHY,
                message="Database connection successful"
            )
            
        except Exception as e:
            return HealthResult(
                name="database_connection",
                status=HealthStatus.UNHEALTHY,
                message=f"Database connection failed: {e}"
            )
    
    def _check_redis_connection(self) -> HealthResult:
        """检查Redis连接"""
        try:
            if not REDIS_AVAILABLE:
                return HealthResult(
                    name="redis_connection",
                    status=HealthStatus.UNKNOWN,
                    message="Redis client not available"
                )
            
            # 从设置中获取Redis配置
            redis_url = getattr(settings, 'REDIS_URL', 'redis://localhost:6379/0')
            
            # 尝试连接Redis
            r = redis.from_url(redis_url)
            r.ping()
            
            # 获取Redis信息
            info = r.info()
            details = {
                'version': info.get('redis_version'),
                'connected_clients': info.get('connected_clients'),
                'used_memory_human': info.get('used_memory_human')
            }
            
            return HealthResult(
                name="redis_connection",
                status=HealthStatus.HEALTHY,
                message="Redis connection successful",
                details=details
            )
            
        except Exception as e:
            return HealthResult(
                name="redis_connection",
                status=HealthStatus.UNHEALTHY,
                message=f"Redis connection failed: {e}"
            )
    
    def _check_web_service(self) -> HealthResult:
        """检查Web服务"""
        try:
            if not REQUESTS_AVAILABLE:
                return HealthResult(
                    name="web_service",
                    status=HealthStatus.UNKNOWN,
                    message="Requests library not available"
                )
            
            # 检查本地Web服务
            response = requests.get('http://localhost:8000/api/info', timeout=5)
            
            if response.status_code == 200:
                return HealthResult(
                    name="web_service",
                    status=HealthStatus.HEALTHY,
                    message="Web service responding normally",
                    details={'status_code': response.status_code}
                )
            else:
                return HealthResult(
                    name="web_service",
                    status=HealthStatus.DEGRADED,
                    message=f"Web service returned status {response.status_code}",
                    details={'status_code': response.status_code}
                )
                
        except Exception as e:
            return HealthResult(
                name="web_service",
                status=HealthStatus.UNHEALTHY,
                message=f"Web service check failed: {e}"
            )
    
    def _check_memory_leak(self) -> HealthResult:
        """检查内存泄漏"""
        try:
            process = psutil.Process()
            memory_info = process.memory_info()
            memory_percent = process.memory_percent()
            
            details = {
                'rss_mb': round(memory_info.rss / (1024*1024), 2),
                'vms_mb': round(memory_info.vms / (1024*1024), 2),
                'memory_percent': round(memory_percent, 2)
            }
            
            # 简单的内存泄漏检测（实际应用中需要更复杂的逻辑）
            if memory_percent > 50:
                return HealthResult(
                    name="memory_leak",
                    status=HealthStatus.DEGRADED,
                    message=f"High memory usage: {memory_percent:.1f}%",
                    details=details
                )
            else:
                return HealthResult(
                    name="memory_leak",
                    status=HealthStatus.HEALTHY,
                    message=f"Memory usage normal: {memory_percent:.1f}%",
                    details=details
                )
                
        except Exception as e:
            return HealthResult(
                name="memory_leak",
                status=HealthStatus.UNHEALTHY,
                message=f"Memory leak check failed: {e}"
            )
    
    async def run_check(self, name: str) -> Optional[HealthResult]:
        """运行指定的健康检查"""
        if name not in self.checks:
            return None
        
        check = self.checks[name]
        await self._run_single_check(check)
        return self.results.get(name)
    
    def get_overall_health(self) -> Dict[str, Any]:
        """获取整体健康状态"""
        if not self.results:
            return {
                'status': HealthStatus.UNKNOWN.value,
                'message': 'No health checks have been run',
                'checks': {}
            }
        
        # 计算整体状态
        critical_unhealthy = any(
            result.status == HealthStatus.UNHEALTHY and self.checks[name].critical
            for name, result in self.results.items()
            if name in self.checks
        )
        
        any_unhealthy = any(
            result.status == HealthStatus.UNHEALTHY
            for result in self.results.values()
        )
        
        any_degraded = any(
            result.status == HealthStatus.DEGRADED
            for result in self.results.values()
        )
        
        if critical_unhealthy:
            overall_status = HealthStatus.UNHEALTHY
            message = "Critical health checks failing"
        elif any_unhealthy:
            overall_status = HealthStatus.DEGRADED
            message = "Some health checks failing"
        elif any_degraded:
            overall_status = HealthStatus.DEGRADED
            message = "Some health checks degraded"
        else:
            overall_status = HealthStatus.HEALTHY
            message = "All health checks passing"
        
        return {
            'status': overall_status.value,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'checks': {name: result.to_dict() for name, result in self.results.items()},
            'summary': {
                'total_checks': len(self.results),
                'healthy': len([r for r in self.results.values() if r.status == HealthStatus.HEALTHY]),
                'degraded': len([r for r in self.results.values() if r.status == HealthStatus.DEGRADED]),
                'unhealthy': len([r for r in self.results.values() if r.status == HealthStatus.UNHEALTHY]),
                'unknown': len([r for r in self.results.values() if r.status == HealthStatus.UNKNOWN])
            }
        }
    
    def get_check_status(self, name: str) -> Optional[Dict[str, Any]]:
        """获取指定检查的状态"""
        if name not in self.checks:
            return None
        
        check = self.checks[name]
        result = self.results.get(name)
        
        return {
            'check': {
                'name': check.name,
                'description': check.description,
                'enabled': check.enabled,
                'critical': check.critical,
                'interval': check.interval,
                'timeout': check.timeout,
                'tags': check.tags,
                'stats': {
                    'check_count': check.check_count,
                    'failure_count': check.failure_count,
                    'success_rate': (check.check_count - check.failure_count) / check.check_count * 100 if check.check_count > 0 else 0,
                    'last_check': check.last_check.isoformat() if check.last_check else None
                }
            },
            'result': result.to_dict() if result else None
        }


# 全局健康检查器实例
health_checker = HealthChecker()

def get_health_checker() -> HealthChecker:
    """获取全局健康检查器"""
    return health_checker