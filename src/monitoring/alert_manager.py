#!/usr/bin/env python3
"""
告警管理系统
支持规则配置、阈值监控、多渠道通知
"""

import asyncio
import json
import smtplib
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading
from collections import defaultdict, deque

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

from src.utils.logger import system_logger
from src.config.settings import settings


class AlertSeverity(Enum):
    """告警严重级别"""
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"


class AlertStatus(Enum):
    """告警状态"""
    ACTIVE = "active"
    RESOLVED = "resolved"
    SILENCED = "silenced"


@dataclass
class AlertRule:
    """告警规则"""
    name: str
    description: str
    metric_name: str
    condition: str  # >, <, >=, <=, ==, !=
    threshold: float
    severity: AlertSeverity = AlertSeverity.WARNING
    duration: int = 300  # 持续时间(秒)，超过此时间才触发告警
    enabled: bool = True
    labels: Dict[str, str] = field(default_factory=dict)
    annotations: Dict[str, str] = field(default_factory=dict)
    
    def evaluate(self, value: float) -> bool:
        """评估规则是否满足"""
        if not self.enabled:
            return False
        
        try:
            if self.condition == '>':
                return value > self.threshold
            elif self.condition == '<':
                return value < self.threshold
            elif self.condition == '>=':
                return value >= self.threshold
            elif self.condition == '<=':
                return value <= self.threshold
            elif self.condition == '==':
                return abs(value - self.threshold) < 1e-6
            elif self.condition == '!=':
                return abs(value - self.threshold) >= 1e-6
            else:
                system_logger.error(f"Unknown condition: {self.condition}")
                return False
        except Exception as e:
            system_logger.error(f"Error evaluating rule {self.name}: {e}")
            return False


@dataclass
class Alert:
    """告警实例"""
    rule_name: str
    message: str
    severity: AlertSeverity
    status: AlertStatus = AlertStatus.ACTIVE
    created_at: datetime = field(default_factory=datetime.now)
    resolved_at: Optional[datetime] = None
    labels: Dict[str, str] = field(default_factory=dict)
    annotations: Dict[str, str] = field(default_factory=dict)
    value: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'rule_name': self.rule_name,
            'message': self.message,
            'severity': self.severity.value,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None,
            'labels': self.labels,
            'annotations': self.annotations,
            'value': self.value
        }


class NotificationChannel:
    """通知渠道基类"""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config
        self.enabled = config.get('enabled', True)
    
    async def send(self, alert: Alert) -> bool:
        """发送通知"""
        raise NotImplementedError


class EmailNotification(NotificationChannel):
    """邮件通知"""
    
    async def send(self, alert: Alert) -> bool:
        """发送邮件通知"""
        if not self.enabled:
            return False
        
        try:
            smtp_server = self.config.get('smtp_server', 'localhost')
            smtp_port = self.config.get('smtp_port', 587)
            username = self.config.get('username')
            password = self.config.get('password')
            to_emails = self.config.get('to_emails', [])
            
            if not to_emails:
                system_logger.warning("No email recipients configured")
                return False
            
            # 创建邮件内容
            msg = MIMEMultipart()
            msg['From'] = username
            msg['To'] = ', '.join(to_emails)
            msg['Subject'] = f"[{alert.severity.value.upper()}] {alert.rule_name}"
            
            body = self._format_email_body(alert)
            msg.attach(MIMEText(body, 'html'))
            
            # 发送邮件
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(username, password)
            server.send_message(msg)
            server.quit()
            
            system_logger.info(f"Email alert sent for {alert.rule_name}")
            return True
            
        except Exception as e:
            system_logger.error(f"Failed to send email alert: {e}")
            return False
    
    def _format_email_body(self, alert: Alert) -> str:
        """格式化邮件内容"""
        return f"""
        <html>
        <body>
            <h2>告警通知</h2>
            <table border="1" style="border-collapse: collapse;">
                <tr><td><b>规则名称</b></td><td>{alert.rule_name}</td></tr>
                <tr><td><b>告警消息</b></td><td>{alert.message}</td></tr>
                <tr><td><b>严重级别</b></td><td>{alert.severity.value}</td></tr>
                <tr><td><b>当前值</b></td><td>{alert.value}</td></tr>
                <tr><td><b>触发时间</b></td><td>{alert.created_at}</td></tr>
                <tr><td><b>状态</b></td><td>{alert.status.value}</td></tr>
            </table>
            
            <h3>标签</h3>
            <ul>
                {''.join(f'<li>{k}: {v}</li>' for k, v in alert.labels.items())}
            </ul>
            
            <h3>注释</h3>
            <ul>
                {''.join(f'<li>{k}: {v}</li>' for k, v in alert.annotations.items())}
            </ul>
        </body>
        </html>
        """


class WebhookNotification(NotificationChannel):
    """Webhook通知"""
    
    async def send(self, alert: Alert) -> bool:
        """发送Webhook通知"""
        if not self.enabled or not REQUESTS_AVAILABLE:
            return False
        
        try:
            url = self.config.get('url')
            if not url:
                system_logger.warning("No webhook URL configured")
                return False
            
            payload = {
                'alert': alert.to_dict(),
                'timestamp': datetime.now().isoformat(),
                'source': 'analysis-report-system'
            }
            
            headers = {
                'Content-Type': 'application/json',
                'User-Agent': 'AnalysisReportSystem/1.0'
            }
            
            # 添加自定义头部
            custom_headers = self.config.get('headers', {})
            headers.update(custom_headers)
            
            response = requests.post(
                url, 
                json=payload, 
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            
            system_logger.info(f"Webhook alert sent for {alert.rule_name}")
            return True
            
        except Exception as e:
            system_logger.error(f"Failed to send webhook alert: {e}")
            return False


class SlackNotification(NotificationChannel):
    """Slack通知"""
    
    async def send(self, alert: Alert) -> bool:
        """发送Slack通知"""
        if not self.enabled or not REQUESTS_AVAILABLE:
            return False
        
        try:
            webhook_url = self.config.get('webhook_url')
            if not webhook_url:
                system_logger.warning("No Slack webhook URL configured")
                return False
            
            # 根据严重级别选择颜色
            color_map = {
                AlertSeverity.CRITICAL: 'danger',
                AlertSeverity.WARNING: 'warning',
                AlertSeverity.INFO: 'good'
            }
            
            payload = {
                'text': f'告警: {alert.rule_name}',
                'attachments': [{
                    'color': color_map.get(alert.severity, 'warning'),
                    'fields': [
                        {'title': '规则名称', 'value': alert.rule_name, 'short': True},
                        {'title': '严重级别', 'value': alert.severity.value, 'short': True},
                        {'title': '当前值', 'value': str(alert.value), 'short': True},
                        {'title': '状态', 'value': alert.status.value, 'short': True},
                        {'title': '消息', 'value': alert.message, 'short': False},
                        {'title': '时间', 'value': alert.created_at.strftime('%Y-%m-%d %H:%M:%S'), 'short': False}
                    ]
                }]
            }
            
            response = requests.post(webhook_url, json=payload, timeout=10)
            response.raise_for_status()
            
            system_logger.info(f"Slack alert sent for {alert.rule_name}")
            return True
            
        except Exception as e:
            system_logger.error(f"Failed to send Slack alert: {e}")
            return False


class AlertManager:
    """告警管理器"""
    
    def __init__(self):
        self.rules: Dict[str, AlertRule] = {}
        self.active_alerts: Dict[str, Alert] = {}
        self.alert_history: deque = deque(maxlen=1000)
        self.notification_channels: Dict[str, NotificationChannel] = {}
        
        # 规则状态跟踪
        self.rule_states: Dict[str, Dict] = defaultdict(lambda: {
            'first_breach': None,
            'last_breach': None,
            'breach_count': 0,
            'consecutive_breaches': 0
        })
        
        self.running = False
        self._thread = None
        
        self._setup_default_rules()
        self._setup_notification_channels()
    
    def _setup_default_rules(self):
        """设置默认告警规则"""
        default_rules = [
            # 系统资源告警
            AlertRule(
                name="high_cpu_usage",
                description="CPU使用率过高",
                metric_name="system_cpu_usage",
                condition=">",
                threshold=80.0,
                severity=AlertSeverity.WARNING,
                duration=300,
                annotations={
                    "summary": "CPU使用率超过80%",
                    "description": "系统CPU使用率持续5分钟超过80%，请检查系统负载"
                }
            ),
            AlertRule(
                name="high_memory_usage", 
                description="内存使用率过高",
                metric_name="system_memory_usage",
                condition=">",
                threshold=85.0,
                severity=AlertSeverity.WARNING,
                duration=300
            ),
            AlertRule(
                name="high_disk_usage",
                description="磁盘使用率过高", 
                metric_name="system_disk_usage",
                condition=">",
                threshold=90.0,
                severity=AlertSeverity.CRITICAL,
                duration=60
            ),
            
            # 应用性能告警
            AlertRule(
                name="high_error_rate",
                description="错误率过高",
                metric_name="error_rate", 
                condition=">",
                threshold=5.0,
                severity=AlertSeverity.WARNING,
                duration=180
            ),
            AlertRule(
                name="slow_response_time",
                description="响应时间过慢",
                metric_name="response_time_95th",
                condition=">", 
                threshold=5.0,
                severity=AlertSeverity.WARNING,
                duration=300
            ),
            AlertRule(
                name="low_throughput",
                description="系统吞吐量过低",
                metric_name="throughput_qps",
                condition="<",
                threshold=1.0,
                severity=AlertSeverity.INFO,
                duration=600
            ),
            
            # 业务指标告警
            AlertRule(
                name="too_many_websocket_connections",
                description="WebSocket连接数过多",
                metric_name="websocket_connections",
                condition=">",
                threshold=100.0,
                severity=AlertSeverity.WARNING,
                duration=60
            )
        ]
        
        for rule in default_rules:
            self.add_rule(rule)
    
    def _setup_notification_channels(self):
        """设置通知渠道"""
        # 邮件通知
        email_config = getattr(settings, 'EMAIL_CONFIG', {})
        if email_config.get('enabled', False):
            self.notification_channels['email'] = EmailNotification('email', email_config)
        
        # Webhook通知
        webhook_config = getattr(settings, 'WEBHOOK_CONFIG', {})
        if webhook_config.get('enabled', False):
            self.notification_channels['webhook'] = WebhookNotification('webhook', webhook_config)
        
        # Slack通知
        slack_config = getattr(settings, 'SLACK_CONFIG', {})
        if slack_config.get('enabled', False):
            self.notification_channels['slack'] = SlackNotification('slack', slack_config)
    
    def add_rule(self, rule: AlertRule):
        """添加告警规则"""
        self.rules[rule.name] = rule
        system_logger.info(f"Added alert rule: {rule.name}")
    
    def remove_rule(self, rule_name: str):
        """移除告警规则"""
        if rule_name in self.rules:
            del self.rules[rule_name]
            # 清理相关状态
            if rule_name in self.rule_states:
                del self.rule_states[rule_name]
            system_logger.info(f"Removed alert rule: {rule_name}")
    
    def add_notification_channel(self, channel: NotificationChannel):
        """添加通知渠道"""
        self.notification_channels[channel.name] = channel
        system_logger.info(f"Added notification channel: {channel.name}")
    
    async def evaluate_metrics(self, metrics: Dict[str, float]):
        """评估指标并触发告警"""
        current_time = datetime.now()
        
        for rule_name, rule in self.rules.items():
            if not rule.enabled:
                continue
            
            metric_value = metrics.get(rule.metric_name)
            if metric_value is None:
                continue
            
            try:
                # 评估规则
                is_breach = rule.evaluate(metric_value)
                rule_state = self.rule_states[rule_name]
                
                if is_breach:
                    # 记录违规
                    if rule_state['first_breach'] is None:
                        rule_state['first_breach'] = current_time
                    
                    rule_state['last_breach'] = current_time
                    rule_state['breach_count'] += 1
                    rule_state['consecutive_breaches'] += 1
                    
                    # 检查是否需要触发告警
                    breach_duration = (current_time - rule_state['first_breach']).total_seconds()
                    
                    if (breach_duration >= rule.duration and 
                        rule_name not in self.active_alerts):
                        # 触发新告警
                        await self._trigger_alert(rule, metric_value)
                
                else:
                    # 规则不再违规
                    rule_state['consecutive_breaches'] = 0
                    
                    # 如果有活跃告警，解决它
                    if rule_name in self.active_alerts:
                        await self._resolve_alert(rule_name)
                    
                    # 重置首次违规时间
                    if rule_state['first_breach']:
                        rule_state['first_breach'] = None
                        
            except Exception as e:
                system_logger.error(f"Error evaluating rule {rule_name}: {e}")
    
    async def _trigger_alert(self, rule: AlertRule, value: float):
        """触发告警"""
        alert = Alert(
            rule_name=rule.name,
            message=f"{rule.description}: 当前值 {value}, 阈值 {rule.threshold}",
            severity=rule.severity,
            labels=rule.labels.copy(),
            annotations=rule.annotations.copy(),
            value=value
        )
        
        self.active_alerts[rule.name] = alert
        self.alert_history.append(alert)
        
        system_logger.warning(f"Alert triggered: {rule.name} - {alert.message}")
        
        # 发送通知
        await self._send_notifications(alert)
    
    async def _resolve_alert(self, rule_name: str):
        """解决告警"""
        if rule_name in self.active_alerts:
            alert = self.active_alerts[rule_name]
            alert.status = AlertStatus.RESOLVED
            alert.resolved_at = datetime.now()
            
            del self.active_alerts[rule_name]
            
            system_logger.info(f"Alert resolved: {rule_name}")
            
            # 发送解决通知
            await self._send_notifications(alert)
    
    async def _send_notifications(self, alert: Alert):
        """发送通知"""
        for channel_name, channel in self.notification_channels.items():
            try:
                success = await channel.send(alert)
                if success:
                    system_logger.info(f"Notification sent via {channel_name}")
                else:
                    system_logger.warning(f"Failed to send notification via {channel_name}")
            except Exception as e:
                system_logger.error(f"Error sending notification via {channel_name}: {e}")
    
    def silence_alert(self, rule_name: str, duration: int = 3600):
        """静默告警"""
        if rule_name in self.active_alerts:
            alert = self.active_alerts[rule_name]
            alert.status = AlertStatus.SILENCED
            
            # 设置定时器自动取消静默
            def unsilence():
                if rule_name in self.active_alerts:
                    self.active_alerts[rule_name].status = AlertStatus.ACTIVE
            
            timer = threading.Timer(duration, unsilence)
            timer.start()
            
            system_logger.info(f"Alert silenced for {duration}s: {rule_name}")
    
    def get_active_alerts(self) -> List[Dict[str, Any]]:
        """获取活跃告警"""
        return [alert.to_dict() for alert in self.active_alerts.values()]
    
    def get_alert_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """获取告警历史"""
        history = list(self.alert_history)[-limit:]
        return [alert.to_dict() for alert in history]
    
    def get_rules_status(self) -> Dict[str, Any]:
        """获取规则状态"""
        return {
            'total_rules': len(self.rules),
            'enabled_rules': len([r for r in self.rules.values() if r.enabled]),
            'active_alerts': len(self.active_alerts),
            'notification_channels': len(self.notification_channels),
            'rules': {name: {
                'enabled': rule.enabled,
                'severity': rule.severity.value,
                'threshold': rule.threshold,
                'state': self.rule_states.get(name, {})
            } for name, rule in self.rules.items()}
        }


# 全局告警管理器实例
alert_manager = AlertManager()

def get_alert_manager() -> AlertManager:
    """获取全局告警管理器"""
    return alert_manager