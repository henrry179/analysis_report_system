#!/usr/bin/env python3
"""
统一配置管理模块
集中管理所有系统配置
"""

import os
from pathlib import Path
from typing import Dict, Any

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent.parent
SRC_ROOT = PROJECT_ROOT / "src"

class Settings:
    """系统设置类"""
    
    # 应用基础设置
    APP_NAME = "业务分析报告自动化系统"
    APP_VERSION = "v4.0 Optimized"
    APP_DESCRIPTION = "🏪 专业业务分析报告系统 - 智能分析 · 数据驱动 · 洞察未来"
    
    # 服务器配置
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    RELOAD = os.getenv("RELOAD", "false").lower() == "true"
    
    # 目录配置
    STATIC_DIR = SRC_ROOT / "static"
    TEMPLATES_DIR = SRC_ROOT / "templates"
    REPORTS_DIR = PROJECT_ROOT / "output" / "reports"
    PDF_REPORTS_DIR = PROJECT_ROOT / "pdf_reports"
    DATA_DIR = SRC_ROOT / "data"
    LOGS_DIR = PROJECT_ROOT / "logs"
    
    # 上传配置
    UPLOAD_DIR = DATA_DIR / "uploads"
    MAX_UPLOAD_SIZE = 100 * 1024 * 1024  # 100MB
    ALLOWED_EXTENSIONS = {'.csv', '.json', '.xlsx', '.xls', '.txt'}
    
    # 数据库配置（如果需要）
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///analysis_system.db")
    
    # WebSocket配置
    WEBSOCKET_MAX_CONNECTIONS = int(os.getenv("WEBSOCKET_MAX_CONNECTIONS", 100))
    WEBSOCKET_PING_INTERVAL = int(os.getenv("WEBSOCKET_PING_INTERVAL", 30))
    
    # 安全配置
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    TOKEN_EXPIRE_MINUTES = int(os.getenv("TOKEN_EXPIRE_MINUTES", 60))
    
    # 日志配置
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_MAX_SIZE = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT = 5
    
    # 报告生成配置
    REPORT_CACHE_TTL = int(os.getenv("REPORT_CACHE_TTL", 3600))  # 1小时
    MAX_BATCH_REPORTS = int(os.getenv("MAX_BATCH_REPORTS", 50))
    
    # 性能配置
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 30))
    
    @classmethod
    def get_all_settings(cls) -> Dict[str, Any]:
        """获取所有配置"""
        return {
            key: value for key, value in cls.__dict__.items()
            if not key.startswith('_') and not callable(value)
        }
    
    @classmethod
    def ensure_directories(cls):
        """确保必要的目录存在"""
        directories = [
            cls.REPORTS_DIR,
            cls.PDF_REPORTS_DIR,
            cls.UPLOAD_DIR,
            cls.LOGS_DIR,
            cls.DATA_DIR / "imported",
            cls.DATA_DIR / "exports"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            
    @classmethod
    def validate_settings(cls):
        """验证配置的有效性"""
        errors = []
        
        # 检查必要的目录
        if not cls.STATIC_DIR.exists():
            errors.append(f"静态文件目录不存在: {cls.STATIC_DIR}")
        
        if not cls.TEMPLATES_DIR.exists():
            errors.append(f"模板目录不存在: {cls.TEMPLATES_DIR}")
        
        # 检查端口范围
        if not (1000 <= cls.PORT <= 65535):
            errors.append(f"端口号无效: {cls.PORT}")
        
        if errors:
            raise ValueError(f"配置验证失败:\n" + "\n".join(errors))
        
        return True

# 全局设置实例
settings = Settings()

# 在导入时确保目录存在
settings.ensure_directories() 