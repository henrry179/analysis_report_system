#!/usr/bin/env python3
"""
统一日志管理模块
提供标准化的日志记录功能
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime

from config.settings import settings


class Logger:
    """日志管理器"""
    
    _loggers = {}
    
    @classmethod
    def get_logger(cls, name: str, level: Optional[str] = None) -> logging.Logger:
        """获取日志记录器"""
        if name in cls._loggers:
            return cls._loggers[name]
        
        # 创建日志记录器
        logger = logging.getLogger(name)
        log_level = level or settings.LOG_LEVEL
        if callable(log_level):
            log_level = 'INFO'  # 默认级别
        logger.setLevel(getattr(logging, log_level.upper()))
        
        # 避免重复添加处理器
        if not logger.handlers:
            # 控制台处理器
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)
            console_formatter = ColoredFormatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)
            
            # 文件处理器
            log_file = settings.LOGS_DIR / f"{name}.log"
            file_handler = logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=settings.LOG_MAX_SIZE,
                backupCount=settings.LOG_BACKUP_COUNT,
                encoding='utf-8'
            )
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter(settings.LOG_FORMAT)
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
        
        cls._loggers[name] = logger
        return logger


class ColoredFormatter(logging.Formatter):
    """彩色日志格式化器"""
    
    # 颜色代码
    COLORS = {
        'DEBUG': '\033[36m',    # 青色
        'INFO': '\033[32m',     # 绿色
        'WARNING': '\033[33m',  # 黄色
        'ERROR': '\033[31m',    # 红色
        'CRITICAL': '\033[35m', # 紫色
        'RESET': '\033[0m'      # 重置
    }
    
    def format(self, record):
        # 添加颜色
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{self.COLORS['RESET']}"
        
        return super().format(record)


class SystemLogger:
    """系统级日志记录器"""
    
    def __init__(self):
        self.logger = Logger.get_logger('system')
    
    def info(self, message: str, **kwargs):
        """记录信息日志"""
        formatted_message = self._format_message(message, **kwargs)
        self.logger.info(formatted_message)
    
    def warning(self, message: str, **kwargs):
        """记录警告日志"""
        formatted_message = self._format_message(message, **kwargs)
        self.logger.warning(formatted_message)
    
    def error(self, message: str, error: Optional[Exception] = None, **kwargs):
        """记录错误日志"""
        formatted_message = self._format_message(message, **kwargs)
        if error:
            self.logger.error(f"{formatted_message} - {str(error)}", exc_info=True)
        else:
            self.logger.error(formatted_message)
    
    def debug(self, message: str, **kwargs):
        """记录调试日志"""
        formatted_message = self._format_message(message, **kwargs)
        self.logger.debug(formatted_message)
    
    def critical(self, message: str, **kwargs):
        """记录关键错误日志"""
        formatted_message = self._format_message(message, **kwargs)
        self.logger.critical(formatted_message)
    
    def _format_message(self, message: str, **kwargs) -> str:
        """格式化日志消息"""
        if kwargs:
            context = " | ".join([f"{k}={v}" for k, v in kwargs.items()])
            return f"{message} | {context}"
        return message


class PerformanceLogger:
    """性能监控日志记录器"""
    
    def __init__(self):
        self.logger = Logger.get_logger('performance')
    
    def log_request(self, method: str, path: str, duration: float, status_code: int):
        """记录请求性能"""
        message = f"Request completed - {method} {path} - {duration:.3f}s - {status_code}"
        self.logger.info(message)
    
    def log_operation(self, operation: str, duration: float, **kwargs):
        """记录操作性能"""
        context = " | ".join([f"{k}={v}" for k, v in kwargs.items()])
        message = f"Operation completed: {operation} - {duration:.3f}s"
        if context:
            message += f" | {context}"
        self.logger.info(message)


class WebSocketLogger:
    """WebSocket日志记录器"""
    
    def __init__(self):
        self.logger = Logger.get_logger('websocket')
    
    def connection_established(self, client_id: str, client_info: dict = None):
        """记录连接建立"""
        self.logger.info(f"WebSocket connection established", client_id=client_id, **(client_info or {}))
    
    def connection_closed(self, client_id: str, reason: str = None):
        """记录连接关闭"""
        self.logger.info(f"WebSocket connection closed", client_id=client_id, reason=reason or "Normal")
    
    def message_sent(self, client_id: str, message_type: str):
        """记录消息发送"""
        self.logger.debug(f"Message sent", client_id=client_id, type=message_type)
    
    def error_occurred(self, client_id: str, error: Exception):
        """记录WebSocket错误"""
        self.logger.error(f"WebSocket error", client_id=client_id, error=str(error))


# 全局日志记录器实例
system_logger = SystemLogger()
performance_logger = PerformanceLogger()
websocket_logger = WebSocketLogger()


def get_logger(name: str) -> logging.Logger:
    """便捷函数：获取日志记录器"""
    return Logger.get_logger(name)


def log_startup_info():
    """记录系统启动信息"""
    system_logger.info("="*60)
    system_logger.info(f"🚀 {settings.APP_NAME} 启动")
    system_logger.info(f"📊 版本: {settings.APP_VERSION}")
    system_logger.info(f"🌐 地址: http://{settings.HOST}:{settings.PORT}")
    system_logger.info(f"🐛 调试模式: {'开启' if settings.DEBUG else '关闭'}")
    system_logger.info(f"📁 报告目录: {settings.REPORTS_DIR}")
    system_logger.info(f"📝 日志目录: {settings.LOGS_DIR}")
    system_logger.info("="*60)


def log_shutdown_info():
    """记录系统关闭信息"""
    system_logger.info("="*60)
    system_logger.info("🛑 系统正在关闭...")
    system_logger.info(f"⏰ 关闭时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    system_logger.info("👋 再见！")
    system_logger.info("="*60) 