#!/usr/bin/env python3
"""
日志聚合和分析系统
提供统一的日志收集、分析和查询功能
"""

import json
import time
import gzip
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union, Callable
from dataclasses import dataclass, field
from collections import defaultdict, deque
from pathlib import Path
import re
import logging
from enum import Enum

try:
    import elasticsearch
    ELASTICSEARCH_AVAILABLE = True
except ImportError:
    ELASTICSEARCH_AVAILABLE = False

from src.utils.logger import system_logger
from src.config.settings import settings


class LogLevel(Enum):
    """日志级别"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogSource(Enum):
    """日志来源"""
    APPLICATION = "application"
    SYSTEM = "system"
    WEB = "web"
    DATABASE = "database"
    SECURITY = "security"
    PERFORMANCE = "performance"


@dataclass
class LogEntry:
    """日志条目"""
    timestamp: datetime
    level: LogLevel
    source: LogSource
    message: str
    logger_name: str = ""
    module: str = ""
    function: str = ""
    line_number: Optional[int] = None
    thread_id: Optional[int] = None
    process_id: Optional[int] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    request_id: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    extra_data: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'timestamp': self.timestamp.isoformat(),
            'level': self.level.value,
            'source': self.source.value,
            'message': self.message,
            'logger_name': self.logger_name,
            'module': self.module,
            'function': self.function,
            'line_number': self.line_number,
            'thread_id': self.thread_id,
            'process_id': self.process_id,
            'user_id': self.user_id,
            'session_id': self.session_id,
            'request_id': self.request_id,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'extra_data': self.extra_data
        }


@dataclass
class LogQuery:
    """日志查询条件"""
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    levels: Optional[List[LogLevel]] = None
    sources: Optional[List[LogSource]] = None
    keywords: Optional[List[str]] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    request_id: Optional[str] = None
    limit: int = 100
    offset: int = 0
    sort_order: str = "desc"  # desc or asc


@dataclass
class LogStats:
    """日志统计"""
    total_count: int = 0
    level_counts: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    source_counts: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    error_rate: float = 0.0
    top_errors: List[Dict[str, Any]] = field(default_factory=list)
    hourly_counts: List[Dict[str, Any]] = field(default_factory=list)


class LogAggregator:
    """日志聚合器"""
    
    def __init__(self, max_memory_entries: int = 10000):
        self.max_memory_entries = max_memory_entries
        self.memory_logs: deque = deque(maxlen=max_memory_entries)
        self.log_files: Dict[str, Path] = {}
        self.elasticsearch_client = None
        
        # 统计信息
        self.stats = {
            'total_processed': 0,
            'errors_count': 0,
            'last_cleanup': datetime.now(),
            'storage_backends': []
        }
        
        # 日志轮转配置
        self.rotation_config = {
            'max_file_size': 100 * 1024 * 1024,  # 100MB
            'max_files': 10,
            'compress_old': True
        }
        
        self._setup_storage_backends()
        self._setup_log_rotation()
    
    def _setup_storage_backends(self):
        """设置存储后端"""
        # 文件存储
        log_dir = Path(getattr(settings, 'LOG_DIR', 'logs'))
        log_dir.mkdir(exist_ok=True)
        
        self.log_files = {
            'application': log_dir / 'application.log',
            'system': log_dir / 'system.log',
            'web': log_dir / 'web.log',
            'database': log_dir / 'database.log',
            'security': log_dir / 'security.log',
            'performance': log_dir / 'performance.log',
            'all': log_dir / 'all.log'
        }
        
        self.stats['storage_backends'].append('file')
        
        # Elasticsearch存储（如果可用）
        if ELASTICSEARCH_AVAILABLE:
            es_config = getattr(settings, 'ELASTICSEARCH_CONFIG', {})
            if es_config.get('enabled', False):
                try:
                    self.elasticsearch_client = elasticsearch.Elasticsearch(
                        es_config.get('hosts', ['localhost:9200']),
                        **es_config.get('client_options', {})
                    )
                    self.stats['storage_backends'].append('elasticsearch')
                    system_logger.info("Elasticsearch backend enabled")
                except Exception as e:
                    system_logger.error(f"Failed to setup Elasticsearch: {e}")
    
    def _setup_log_rotation(self):
        """设置日志轮转"""
        def rotation_worker():
            while True:
                try:
                    self._rotate_logs()
                    time.sleep(3600)  # 每小时检查一次
                except Exception as e:
                    system_logger.error(f"Log rotation error: {e}")
                    time.sleep(300)  # 错误时5分钟后重试
        
        rotation_thread = threading.Thread(target=rotation_worker, daemon=True)
        rotation_thread.start()
    
    def add_log_entry(self, entry: LogEntry):
        """添加日志条目"""
        try:
            # 添加到内存缓存
            self.memory_logs.append(entry)
            
            # 写入文件
            self._write_to_file(entry)
            
            # 写入Elasticsearch（如果可用）
            if self.elasticsearch_client:
                self._write_to_elasticsearch(entry)
            
            # 更新统计
            self.stats['total_processed'] += 1
            if entry.level in [LogLevel.ERROR, LogLevel.CRITICAL]:
                self.stats['errors_count'] += 1
                
        except Exception as e:
            system_logger.error(f"Failed to add log entry: {e}")
    
    def _write_to_file(self, entry: LogEntry):
        """写入日志文件"""
        try:
            # 格式化日志条目
            log_line = self._format_log_entry(entry)
            
            # 写入对应源的日志文件
            source_file = self.log_files.get(entry.source.value)
            if source_file:
                with open(source_file, 'a', encoding='utf-8') as f:
                    f.write(log_line + '\n')
            
            # 写入总日志文件
            with open(self.log_files['all'], 'a', encoding='utf-8') as f:
                f.write(log_line + '\n')
                
        except Exception as e:
            system_logger.error(f"Failed to write log to file: {e}")
    
    def _write_to_elasticsearch(self, entry: LogEntry):
        """写入Elasticsearch"""
        try:
            index_name = f"logs-{datetime.now().strftime('%Y-%m')}"
            doc = entry.to_dict()
            
            self.elasticsearch_client.index(
                index=index_name,
                body=doc
            )
            
        except Exception as e:
            system_logger.error(f"Failed to write log to Elasticsearch: {e}")
    
    def _format_log_entry(self, entry: LogEntry) -> str:
        """格式化日志条目"""
        base_format = (
            f"{entry.timestamp.isoformat()} "
            f"[{entry.level.value}] "
            f"[{entry.source.value}] "
            f"{entry.message}"
        )
        
        # 添加额外信息
        extras = []
        if entry.logger_name:
            extras.append(f"logger={entry.logger_name}")
        if entry.module:
            extras.append(f"module={entry.module}")
        if entry.function:
            extras.append(f"func={entry.function}")
        if entry.line_number:
            extras.append(f"line={entry.line_number}")
        if entry.user_id:
            extras.append(f"user={entry.user_id}")
        if entry.request_id:
            extras.append(f"req_id={entry.request_id}")
        if entry.ip_address:
            extras.append(f"ip={entry.ip_address}")
        
        if extras:
            base_format += f" [{', '.join(extras)}]"
        
        # 添加额外数据
        if entry.extra_data:
            base_format += f" extra={json.dumps(entry.extra_data, ensure_ascii=False)}"
        
        return base_format
    
    def _rotate_logs(self):
        """轮转日志文件"""
        for log_type, log_file in self.log_files.items():
            if not log_file.exists():
                continue
            
            try:
                file_size = log_file.stat().st_size
                if file_size > self.rotation_config['max_file_size']:
                    self._rotate_single_log(log_file)
                    
            except Exception as e:
                system_logger.error(f"Failed to rotate log {log_file}: {e}")
        
        self.stats['last_cleanup'] = datetime.now()
    
    def _rotate_single_log(self, log_file: Path):
        """轮转单个日志文件"""
        base_name = log_file.stem
        suffix = log_file.suffix
        log_dir = log_file.parent
        
        # 移动现有的编号文件
        for i in range(self.rotation_config['max_files'] - 1, 0, -1):
            old_file = log_dir / f"{base_name}.{i}{suffix}"
            new_file = log_dir / f"{base_name}.{i + 1}{suffix}"
            
            if old_file.exists():
                if i == self.rotation_config['max_files'] - 1:
                    # 删除最老的文件
                    old_file.unlink()
                else:
                    old_file.rename(new_file)
                    
                    # 压缩旧文件
                    if self.rotation_config['compress_old'] and i > 1:
                        self._compress_log_file(new_file)
        
        # 重命名当前文件
        rotated_file = log_dir / f"{base_name}.1{suffix}"
        log_file.rename(rotated_file)
        
        # 压缩轮转的文件
        if self.rotation_config['compress_old']:
            self._compress_log_file(rotated_file)
        
        system_logger.info(f"Rotated log file: {log_file}")
    
    def _compress_log_file(self, log_file: Path):
        """压缩日志文件"""
        try:
            compressed_file = log_file.with_suffix(log_file.suffix + '.gz')
            
            with open(log_file, 'rb') as f_in:
                with gzip.open(compressed_file, 'wb') as f_out:
                    f_out.writelines(f_in)
            
            log_file.unlink()  # 删除原文件
            
        except Exception as e:
            system_logger.error(f"Failed to compress log file {log_file}: {e}")
    
    def query_logs(self, query: LogQuery) -> List[LogEntry]:
        """查询日志"""
        results = []
        
        # 从内存中查询
        memory_results = self._query_memory_logs(query)
        results.extend(memory_results)
        
        # 从Elasticsearch查询（如果可用且内存结果不足）
        if (self.elasticsearch_client and 
            len(results) < query.limit):
            es_results = self._query_elasticsearch_logs(query)
            results.extend(es_results)
        
        # 从文件查询（如果其他方式结果不足）
        if len(results) < query.limit:
            file_results = self._query_file_logs(query)
            results.extend(file_results)
        
        # 排序和限制结果
        results = sorted(
            results, 
            key=lambda x: x.timestamp, 
            reverse=(query.sort_order == "desc")
        )
        
        return results[query.offset:query.offset + query.limit]
    
    def _query_memory_logs(self, query: LogQuery) -> List[LogEntry]:
        """从内存查询日志"""
        results = []
        
        for entry in self.memory_logs:
            if self._matches_query(entry, query):
                results.append(entry)
        
        return results
    
    def _query_elasticsearch_logs(self, query: LogQuery) -> List[LogEntry]:
        """从Elasticsearch查询日志"""
        if not self.elasticsearch_client:
            return []
        
        try:
            # 构建ES查询
            es_query = {
                "query": {"bool": {"must": []}},
                "sort": [{"timestamp": {"order": query.sort_order}}],
                "size": query.limit,
                "from": query.offset
            }
            
            # 时间范围
            if query.start_time or query.end_time:
                time_range = {}
                if query.start_time:
                    time_range["gte"] = query.start_time.isoformat()
                if query.end_time:
                    time_range["lte"] = query.end_time.isoformat()
                
                es_query["query"]["bool"]["must"].append({
                    "range": {"timestamp": time_range}
                })
            
            # 日志级别
            if query.levels:
                es_query["query"]["bool"]["must"].append({
                    "terms": {"level": [level.value for level in query.levels]}
                })
            
            # 日志来源
            if query.sources:
                es_query["query"]["bool"]["must"].append({
                    "terms": {"source": [source.value for source in query.sources]}
                })
            
            # 关键词搜索
            if query.keywords:
                for keyword in query.keywords:
                    es_query["query"]["bool"]["must"].append({
                        "match": {"message": keyword}
                    })
            
            # 用户ID
            if query.user_id:
                es_query["query"]["bool"]["must"].append({
                    "term": {"user_id": query.user_id}
                })
            
            # 执行搜索
            index_pattern = "logs-*"
            response = self.elasticsearch_client.search(
                index=index_pattern,
                body=es_query
            )
            
            # 转换结果
            results = []
            for hit in response["hits"]["hits"]:
                entry = self._dict_to_log_entry(hit["_source"])
                results.append(entry)
            
            return results
            
        except Exception as e:
            system_logger.error(f"Elasticsearch query failed: {e}")
            return []
    
    def _query_file_logs(self, query: LogQuery) -> List[LogEntry]:
        """从文件查询日志"""
        results = []
        
        try:
            # 读取相关日志文件
            files_to_search = [self.log_files['all']]
            if query.sources:
                for source in query.sources:
                    source_file = self.log_files.get(source.value)
                    if source_file and source_file not in files_to_search:
                        files_to_search.append(source_file)
            
            for log_file in files_to_search:
                if not log_file.exists():
                    continue
                
                with open(log_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        entry = self._parse_log_line(line.strip())
                        if entry and self._matches_query(entry, query):
                            results.append(entry)
                            
                            # 限制结果数量以避免内存问题
                            if len(results) >= query.limit * 2:
                                break
        
        except Exception as e:
            system_logger.error(f"File query failed: {e}")
        
        return results
    
    def _matches_query(self, entry: LogEntry, query: LogQuery) -> bool:
        """检查日志条目是否匹配查询条件"""
        # 时间范围
        if query.start_time and entry.timestamp < query.start_time:
            return False
        if query.end_time and entry.timestamp > query.end_time:
            return False
        
        # 日志级别
        if query.levels and entry.level not in query.levels:
            return False
        
        # 日志来源
        if query.sources and entry.source not in query.sources:
            return False
        
        # 关键词
        if query.keywords:
            message_lower = entry.message.lower()
            for keyword in query.keywords:
                if keyword.lower() not in message_lower:
                    return False
        
        # 用户ID
        if query.user_id and entry.user_id != query.user_id:
            return False
        
        # 会话ID
        if query.session_id and entry.session_id != query.session_id:
            return False
        
        # 请求ID
        if query.request_id and entry.request_id != query.request_id:
            return False
        
        return True
    
    def _parse_log_line(self, line: str) -> Optional[LogEntry]:
        """解析日志行"""
        try:
            # 简化的日志解析（实际应用中需要更复杂的解析逻辑）
            pattern = r'^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+) \[(\w+)\] \[(\w+)\] (.+)$'
            match = re.match(pattern, line)
            
            if match:
                timestamp_str, level_str, source_str, message = match.groups()
                
                return LogEntry(
                    timestamp=datetime.fromisoformat(timestamp_str.replace('Z', '+00:00')),
                    level=LogLevel(level_str),
                    source=LogSource(source_str),
                    message=message
                )
        except Exception as e:
            system_logger.error(f"Failed to parse log line: {e}")
        
        return None
    
    def _dict_to_log_entry(self, data: Dict[str, Any]) -> LogEntry:
        """将字典转换为LogEntry"""
        return LogEntry(
            timestamp=datetime.fromisoformat(data['timestamp'].replace('Z', '+00:00')),
            level=LogLevel(data['level']),
            source=LogSource(data['source']),
            message=data['message'],
            logger_name=data.get('logger_name', ''),
            module=data.get('module', ''),
            function=data.get('function', ''),
            line_number=data.get('line_number'),
            thread_id=data.get('thread_id'),
            process_id=data.get('process_id'),
            user_id=data.get('user_id'),
            session_id=data.get('session_id'),
            request_id=data.get('request_id'),
            ip_address=data.get('ip_address'),
            user_agent=data.get('user_agent'),
            extra_data=data.get('extra_data', {})
        )
    
    def get_log_stats(self, hours: int = 24) -> LogStats:
        """获取日志统计信息"""
        start_time = datetime.now() - timedelta(hours=hours)
        
        query = LogQuery(
            start_time=start_time,
            limit=10000  # 获取更多数据用于统计
        )
        
        logs = self.query_logs(query)
        
        stats = LogStats()
        stats.total_count = len(logs)
        
        # 按级别统计
        for entry in logs:
            stats.level_counts[entry.level.value] += 1
            stats.source_counts[entry.source.value] += 1
        
        # 计算错误率
        error_count = (stats.level_counts.get('ERROR', 0) + 
                      stats.level_counts.get('CRITICAL', 0))
        stats.error_rate = (error_count / stats.total_count * 100) if stats.total_count > 0 else 0
        
        # 统计最常见错误
        error_messages = defaultdict(int)
        for entry in logs:
            if entry.level in [LogLevel.ERROR, LogLevel.CRITICAL]:
                # 简化错误消息用于分组
                simplified_msg = entry.message[:100]
                error_messages[simplified_msg] += 1
        
        stats.top_errors = [
            {'message': msg, 'count': count}
            for msg, count in sorted(error_messages.items(), key=lambda x: x[1], reverse=True)[:10]
        ]
        
        # 按小时统计
        hourly_counts = defaultdict(int)
        for entry in logs:
            hour_key = entry.timestamp.strftime('%Y-%m-%d %H:00')
            hourly_counts[hour_key] += 1
        
        stats.hourly_counts = [
            {'hour': hour, 'count': count}
            for hour, count in sorted(hourly_counts.items())
        ]
        
        return stats
    
    def cleanup_old_logs(self, days: int = 30):
        """清理旧日志"""
        cutoff_time = datetime.now() - timedelta(days=days)
        
        # 清理文件日志
        for log_file in self.log_files.values():
            if log_file.exists():
                try:
                    # 这里应该实现更智能的清理逻辑
                    # 暂时只记录日志
                    system_logger.info(f"Would clean logs older than {cutoff_time} from {log_file}")
                except Exception as e:
                    system_logger.error(f"Failed to clean log file {log_file}: {e}")
        
        # 清理Elasticsearch索引
        if self.elasticsearch_client:
            try:
                # 删除旧索引
                cutoff_month = cutoff_time.strftime('%Y-%m')
                index_pattern = f"logs-{cutoff_month}"
                
                if self.elasticsearch_client.indices.exists(index_pattern):
                    self.elasticsearch_client.indices.delete(index_pattern)
                    system_logger.info(f"Deleted old Elasticsearch index: {index_pattern}")
                    
            except Exception as e:
                system_logger.error(f"Failed to clean Elasticsearch indices: {e}")
    
    def get_aggregator_stats(self) -> Dict[str, Any]:
        """获取聚合器统计信息"""
        return {
            'total_processed': self.stats['total_processed'],
            'errors_count': self.stats['errors_count'],
            'memory_entries': len(self.memory_logs),
            'max_memory_entries': self.max_memory_entries,
            'storage_backends': self.stats['storage_backends'],
            'last_cleanup': self.stats['last_cleanup'].isoformat(),
            'log_files': {name: str(path) for name, path in self.log_files.items()}
        }


# 自定义日志处理器，将日志发送到聚合器
class AggregatorHandler(logging.Handler):
    """日志聚合器处理器"""
    
    def __init__(self, aggregator: LogAggregator, source: LogSource = LogSource.APPLICATION):
        super().__init__()
        self.aggregator = aggregator
        self.source = source
    
    def emit(self, record: logging.LogRecord):
        """发送日志记录"""
        try:
            # 转换日志级别
            level_map = {
                logging.DEBUG: LogLevel.DEBUG,
                logging.INFO: LogLevel.INFO,
                logging.WARNING: LogLevel.WARNING,
                logging.ERROR: LogLevel.ERROR,
                logging.CRITICAL: LogLevel.CRITICAL
            }
            
            level = level_map.get(record.levelno, LogLevel.INFO)
            
            # 创建日志条目
            entry = LogEntry(
                timestamp=datetime.fromtimestamp(record.created),
                level=level,
                source=self.source,
                message=self.format(record),
                logger_name=record.name,
                module=record.module if hasattr(record, 'module') else '',
                function=record.funcName,
                line_number=record.lineno,
                thread_id=record.thread,
                process_id=record.process,
                extra_data=getattr(record, 'extra_data', {})
            )
            
            self.aggregator.add_log_entry(entry)
            
        except Exception:
            self.handleError(record)


# 全局日志聚合器实例
log_aggregator = LogAggregator()

def get_log_aggregator() -> LogAggregator:
    """获取全局日志聚合器"""
    return log_aggregator

def setup_log_aggregation():
    """设置日志聚合"""
    # 为系统日志器添加聚合器处理器
    handler = AggregatorHandler(log_aggregator, LogSource.SYSTEM)
    handler.setLevel(logging.INFO)
    
    # 添加到根日志器
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    
    system_logger.info("Log aggregation setup completed")