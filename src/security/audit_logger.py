#!/usr/bin/env python3
"""
安全审计日志系统
记录和分析安全相关事件
"""

import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, deque
import threading
import hashlib

from src.utils.logger import system_logger
from src.utils.log_aggregator import LogEntry, LogLevel, LogSource, get_log_aggregator


class AuditEventType(Enum):
    """审计事件类型"""
    # 认证事件
    LOGIN_SUCCESS = "login_success"
    LOGIN_FAILED = "login_failed"
    LOGOUT = "logout"
    PASSWORD_CHANGED = "password_changed"
    ACCOUNT_LOCKED = "account_locked"
    
    # 授权事件
    ACCESS_GRANTED = "access_granted"
    ACCESS_DENIED = "access_denied"
    PERMISSION_CHANGED = "permission_changed"
    ROLE_ASSIGNED = "role_assigned"
    ROLE_REMOVED = "role_removed"
    
    # 数据操作事件
    DATA_ACCESS = "data_access"
    DATA_CREATED = "data_created"
    DATA_UPDATED = "data_updated"
    DATA_DELETED = "data_deleted"
    DATA_EXPORTED = "data_exported"
    DATA_IMPORTED = "data_imported"
    
    # 系统事件
    SYSTEM_START = "system_start"
    SYSTEM_STOP = "system_stop"
    CONFIG_CHANGED = "config_changed"
    BACKUP_CREATED = "backup_created"
    BACKUP_RESTORED = "backup_restored"
    
    # 安全事件
    SUSPICIOUS_ACTIVITY = "suspicious_activity"
    BRUTE_FORCE_ATTEMPT = "brute_force_attempt"
    SECURITY_VIOLATION = "security_violation"
    ENCRYPTION_ERROR = "encryption_error"
    CERTIFICATE_EXPIRED = "certificate_expired"
    
    # API事件
    API_CALL = "api_call"
    API_RATE_LIMIT = "api_rate_limit"
    API_ERROR = "api_error"
    
    # 文件操作事件
    FILE_UPLOADED = "file_uploaded"
    FILE_DOWNLOADED = "file_downloaded"
    FILE_DELETED = "file_deleted"
    FILE_MODIFIED = "file_modified"


class AuditSeverity(Enum):
    """审计严重级别"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class AuditEvent:
    """审计事件"""
    event_type: AuditEventType
    severity: AuditSeverity
    message: str
    timestamp: datetime = field(default_factory=datetime.now)
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    resource: Optional[str] = None
    action: Optional[str] = None
    result: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """初始化后处理"""
        # 生成事件ID
        self.event_id = self._generate_event_id()
        
        # 添加默认标签
        if 'security' not in self.tags:
            self.tags.append('security')
        
        if self.severity in [AuditSeverity.HIGH, AuditSeverity.CRITICAL]:
            self.tags.append('alert')
    
    def _generate_event_id(self) -> str:
        """生成事件ID"""
        data = f"{self.event_type.value}:{self.timestamp.isoformat()}:{self.user_id or 'anonymous'}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'event_id': self.event_id,
            'event_type': self.event_type.value,
            'severity': self.severity.value,
            'message': self.message,
            'timestamp': self.timestamp.isoformat(),
            'user_id': self.user_id,
            'session_id': self.session_id,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'resource': self.resource,
            'action': self.action,
            'result': self.result,
            'details': self.details,
            'tags': self.tags
        }


class SecurityAuditLogger:
    """安全审计日志器"""
    
    def __init__(self):
        self.log_aggregator = get_log_aggregator()
        self.events_cache: deque = deque(maxlen=1000)
        self.threat_detection = ThreatDetection()
        
        # 统计信息
        self.stats = {
            'total_events': 0,
            'events_by_type': defaultdict(int),
            'events_by_severity': defaultdict(int),
            'events_by_user': defaultdict(int),
            'last_event_time': None
        }
        
        self._setup_event_handlers()
    
    def _setup_event_handlers(self):
        """设置事件处理器"""
        # 可以在这里添加特定事件类型的处理逻辑
        pass
    
    def log_event(self, event: AuditEvent):
        """记录审计事件"""
        try:
            # 添加到缓存
            self.events_cache.append(event)
            
            # 更新统计
            self.stats['total_events'] += 1
            self.stats['events_by_type'][event.event_type.value] += 1
            self.stats['events_by_severity'][event.severity.value] += 1
            if event.user_id:
                self.stats['events_by_user'][event.user_id] += 1
            self.stats['last_event_time'] = event.timestamp
            
            # 威胁检测
            self.threat_detection.analyze_event(event)
            
            # 转换为日志条目并记录
            log_entry = self._convert_to_log_entry(event)
            self.log_aggregator.add_log_entry(log_entry)
            
            # 特殊事件处理
            self._handle_special_events(event)
            
            system_logger.info(f"Audit event logged: {event.event_type.value} - {event.message}")
            
        except Exception as e:
            system_logger.error(f"Failed to log audit event: {e}")
    
    def _convert_to_log_entry(self, event: AuditEvent) -> LogEntry:
        """转换审计事件为日志条目"""
        # 映射严重级别到日志级别
        severity_map = {
            AuditSeverity.LOW: LogLevel.INFO,
            AuditSeverity.MEDIUM: LogLevel.WARNING,
            AuditSeverity.HIGH: LogLevel.ERROR,
            AuditSeverity.CRITICAL: LogLevel.CRITICAL
        }
        
        return LogEntry(
            timestamp=event.timestamp,
            level=severity_map[event.severity],
            source=LogSource.SECURITY,
            message=f"[{event.event_type.value}] {event.message}",
            logger_name="security_audit",
            user_id=event.user_id,
            session_id=event.session_id,
            ip_address=event.ip_address,
            user_agent=event.user_agent,
            extra_data={
                'event_id': event.event_id,
                'event_type': event.event_type.value,
                'severity': event.severity.value,
                'resource': event.resource,
                'action': event.action,
                'result': event.result,
                'details': event.details,
                'tags': event.tags
            }
        )
    
    def _handle_special_events(self, event: AuditEvent):
        """处理特殊事件"""
        # 高严重级别事件立即告警
        if event.severity in [AuditSeverity.HIGH, AuditSeverity.CRITICAL]:
            self._send_security_alert(event)
        
        # 特定事件类型的处理
        if event.event_type == AuditEventType.LOGIN_FAILED:
            self._handle_failed_login(event)
        elif event.event_type == AuditEventType.BRUTE_FORCE_ATTEMPT:
            self._handle_brute_force(event)
        elif event.event_type == AuditEventType.SUSPICIOUS_ACTIVITY:
            self._handle_suspicious_activity(event)
    
    def _send_security_alert(self, event: AuditEvent):
        """发送安全告警"""
        # 这里可以集成告警系统
        system_logger.critical(f"SECURITY ALERT: {event.message}")
    
    def _handle_failed_login(self, event: AuditEvent):
        """处理登录失败事件"""
        # 可以实现账户锁定逻辑
        pass
    
    def _handle_brute_force(self, event: AuditEvent):
        """处理暴力破解事件"""
        # 可以实现IP封禁逻辑
        pass
    
    def _handle_suspicious_activity(self, event: AuditEvent):
        """处理可疑活动事件"""
        # 可以实现额外的监控逻辑
        pass
    
    # 便捷方法用于记录常见事件
    def log_login_success(self, user_id: str, ip_address: str, user_agent: str = None):
        """记录登录成功"""
        event = AuditEvent(
            event_type=AuditEventType.LOGIN_SUCCESS,
            severity=AuditSeverity.LOW,
            message=f"User {user_id} logged in successfully",
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
            action="login",
            result="success"
        )
        self.log_event(event)
    
    def log_login_failed(self, user_id: str, ip_address: str, reason: str, user_agent: str = None):
        """记录登录失败"""
        event = AuditEvent(
            event_type=AuditEventType.LOGIN_FAILED,
            severity=AuditSeverity.MEDIUM,
            message=f"Login failed for user {user_id}: {reason}",
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
            action="login",
            result="failed",
            details={'reason': reason}
        )
        self.log_event(event)
    
    def log_data_access(self, user_id: str, resource: str, action: str, ip_address: str = None):
        """记录数据访问"""
        event = AuditEvent(
            event_type=AuditEventType.DATA_ACCESS,
            severity=AuditSeverity.LOW,
            message=f"User {user_id} accessed {resource}",
            user_id=user_id,
            ip_address=ip_address,
            resource=resource,
            action=action,
            result="success"
        )
        self.log_event(event)
    
    def log_data_modification(self, user_id: str, resource: str, action: str, details: Dict[str, Any] = None):
        """记录数据修改"""
        event_type_map = {
            'create': AuditEventType.DATA_CREATED,
            'update': AuditEventType.DATA_UPDATED,
            'delete': AuditEventType.DATA_DELETED
        }
        
        event = AuditEvent(
            event_type=event_type_map.get(action, AuditEventType.DATA_UPDATED),
            severity=AuditSeverity.MEDIUM,
            message=f"User {user_id} {action}d {resource}",
            user_id=user_id,
            resource=resource,
            action=action,
            result="success",
            details=details or {}
        )
        self.log_event(event)
    
    def log_access_denied(self, user_id: str, resource: str, reason: str, ip_address: str = None):
        """记录访问拒绝"""
        event = AuditEvent(
            event_type=AuditEventType.ACCESS_DENIED,
            severity=AuditSeverity.MEDIUM,
            message=f"Access denied for user {user_id} to {resource}: {reason}",
            user_id=user_id,
            ip_address=ip_address,
            resource=resource,
            action="access",
            result="denied",
            details={'reason': reason}
        )
        self.log_event(event)
    
    def log_api_call(self, user_id: str, endpoint: str, method: str, status_code: int, 
                     ip_address: str = None, response_time: float = None):
        """记录API调用"""
        severity = AuditSeverity.LOW
        if status_code >= 400:
            severity = AuditSeverity.MEDIUM
        if status_code >= 500:
            severity = AuditSeverity.HIGH
        
        event = AuditEvent(
            event_type=AuditEventType.API_CALL,
            severity=severity,
            message=f"API call: {method} {endpoint} -> {status_code}",
            user_id=user_id,
            ip_address=ip_address,
            resource=endpoint,
            action=method.lower(),
            result="success" if status_code < 400 else "error",
            details={
                'status_code': status_code,
                'response_time': response_time
            }
        )
        self.log_event(event)
    
    def log_security_violation(self, user_id: str, violation_type: str, details: Dict[str, Any]):
        """记录安全违规"""
        event = AuditEvent(
            event_type=AuditEventType.SECURITY_VIOLATION,
            severity=AuditSeverity.HIGH,
            message=f"Security violation: {violation_type}",
            user_id=user_id,
            details=details,
            tags=['security', 'violation', 'alert']
        )
        self.log_event(event)
    
    def get_events(self, limit: int = 100, event_type: Optional[AuditEventType] = None,
                   severity: Optional[AuditSeverity] = None, 
                   user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """获取审计事件"""
        events = list(self.events_cache)
        
        # 过滤
        if event_type:
            events = [e for e in events if e.event_type == event_type]
        if severity:
            events = [e for e in events if e.severity == severity]
        if user_id:
            events = [e for e in events if e.user_id == user_id]
        
        # 排序和限制
        events = sorted(events, key=lambda x: x.timestamp, reverse=True)
        return [event.to_dict() for event in events[:limit]]
    
    def get_security_summary(self, hours: int = 24) -> Dict[str, Any]:
        """获取安全摘要"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_events = [e for e in self.events_cache if e.timestamp > cutoff_time]
        
        summary = {
            'total_events': len(recent_events),
            'time_range': f"Last {hours} hours",
            'events_by_type': defaultdict(int),
            'events_by_severity': defaultdict(int),
            'top_users': defaultdict(int),
            'security_alerts': 0,
            'failed_logins': 0,
            'data_modifications': 0
        }
        
        for event in recent_events:
            summary['events_by_type'][event.event_type.value] += 1
            summary['events_by_severity'][event.severity.value] += 1
            
            if event.user_id:
                summary['top_users'][event.user_id] += 1
            
            if event.severity in [AuditSeverity.HIGH, AuditSeverity.CRITICAL]:
                summary['security_alerts'] += 1
            
            if event.event_type == AuditEventType.LOGIN_FAILED:
                summary['failed_logins'] += 1
            
            if event.event_type in [AuditEventType.DATA_CREATED, 
                                  AuditEventType.DATA_UPDATED, 
                                  AuditEventType.DATA_DELETED]:
                summary['data_modifications'] += 1
        
        # 转换为普通字典
        summary['events_by_type'] = dict(summary['events_by_type'])
        summary['events_by_severity'] = dict(summary['events_by_severity'])
        summary['top_users'] = dict(sorted(summary['top_users'].items(), 
                                         key=lambda x: x[1], reverse=True)[:10])
        
        return summary
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            'total_events': self.stats['total_events'],
            'events_by_type': dict(self.stats['events_by_type']),
            'events_by_severity': dict(self.stats['events_by_severity']),
            'top_users': dict(sorted(self.stats['events_by_user'].items(), 
                                   key=lambda x: x[1], reverse=True)[:10]),
            'last_event_time': self.stats['last_event_time'].isoformat() if self.stats['last_event_time'] else None,
            'cache_size': len(self.events_cache)
        }


class ThreatDetection:
    """威胁检测系统"""
    
    def __init__(self):
        self.login_attempts: defaultdict = defaultdict(list)
        self.api_requests: defaultdict = defaultdict(list)
        self.data_access_patterns: defaultdict = defaultdict(list)
        
        # 检测阈值
        self.thresholds = {
            'max_login_attempts': 5,
            'login_attempt_window': 300,  # 5分钟
            'max_api_requests': 100,
            'api_request_window': 60,  # 1分钟
            'suspicious_data_access': 20
        }
    
    def analyze_event(self, event: AuditEvent):
        """分析事件以检测威胁"""
        try:
            if event.event_type == AuditEventType.LOGIN_FAILED:
                self._check_brute_force_login(event)
            elif event.event_type == AuditEventType.API_CALL:
                self._check_api_rate_limit(event)
            elif event.event_type == AuditEventType.DATA_ACCESS:
                self._check_suspicious_data_access(event)
                
        except Exception as e:
            system_logger.error(f"Threat detection error: {e}")
    
    def _check_brute_force_login(self, event: AuditEvent):
        """检查暴力破解登录"""
        ip_key = event.ip_address or 'unknown'
        current_time = time.time()
        
        # 清理旧记录
        cutoff_time = current_time - self.thresholds['login_attempt_window']
        self.login_attempts[ip_key] = [
            t for t in self.login_attempts[ip_key] if t > cutoff_time
        ]
        
        # 添加当前尝试
        self.login_attempts[ip_key].append(current_time)
        
        # 检查是否超过阈值
        if len(self.login_attempts[ip_key]) >= self.thresholds['max_login_attempts']:
            # 创建暴力破解事件
            brute_force_event = AuditEvent(
                event_type=AuditEventType.BRUTE_FORCE_ATTEMPT,
                severity=AuditSeverity.HIGH,
                message=f"Brute force login attempt detected from IP {ip_key}",
                ip_address=event.ip_address,
                details={
                    'attempt_count': len(self.login_attempts[ip_key]),
                    'time_window': self.thresholds['login_attempt_window']
                },
                tags=['security', 'brute_force', 'alert']
            )
            
            # 这里应该记录到审计日志，但要避免循环调用
            system_logger.critical(f"BRUTE FORCE DETECTED: {brute_force_event.message}")
    
    def _check_api_rate_limit(self, event: AuditEvent):
        """检查API速率限制"""
        user_key = event.user_id or event.ip_address or 'anonymous'
        current_time = time.time()
        
        # 清理旧记录
        cutoff_time = current_time - self.thresholds['api_request_window']
        self.api_requests[user_key] = [
            t for t in self.api_requests[user_key] if t > cutoff_time
        ]
        
        # 添加当前请求
        self.api_requests[user_key].append(current_time)
        
        # 检查是否超过阈值
        if len(self.api_requests[user_key]) >= self.thresholds['max_api_requests']:
            system_logger.warning(f"API rate limit exceeded for {user_key}")
    
    def _check_suspicious_data_access(self, event: AuditEvent):
        """检查可疑数据访问"""
        user_key = event.user_id or 'anonymous'
        current_time = time.time()
        
        # 记录数据访问
        self.data_access_patterns[user_key].append({
            'time': current_time,
            'resource': event.resource,
            'action': event.action
        })
        
        # 保留最近的访问记录
        cutoff_time = current_time - 3600  # 1小时
        self.data_access_patterns[user_key] = [
            access for access in self.data_access_patterns[user_key]
            if access['time'] > cutoff_time
        ]
        
        # 检查访问模式
        recent_accesses = len(self.data_access_patterns[user_key])
        if recent_accesses >= self.thresholds['suspicious_data_access']:
            system_logger.warning(f"Suspicious data access pattern for user {user_key}: {recent_accesses} accesses in 1 hour")


# 全局安全审计日志器实例
security_audit_logger = SecurityAuditLogger()

def get_security_audit_logger() -> SecurityAuditLogger:
    """获取全局安全审计日志器"""
    return security_audit_logger