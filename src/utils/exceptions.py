#!/usr/bin/env python3
"""
统一异常处理模块
定义系统所有自定义异常类型
"""

from typing import Optional, Dict, Any
from enum import Enum


class ErrorCode(Enum):
    """错误代码枚举"""
    
    # 系统错误 1000-1999
    SYSTEM_ERROR = 1000
    CONFIG_ERROR = 1001
    STARTUP_ERROR = 1002
    
    # 认证错误 2000-2999
    AUTH_ERROR = 2000
    TOKEN_INVALID = 2001
    TOKEN_EXPIRED = 2002
    PERMISSION_DENIED = 2003
    
    # 数据错误 3000-3999
    DATA_ERROR = 3000
    DATA_NOT_FOUND = 3001
    DATA_INVALID = 3002
    DATA_DUPLICATE = 3003
    
    # 文件错误 4000-4999
    FILE_ERROR = 4000
    FILE_NOT_FOUND = 4001
    FILE_TOO_LARGE = 4002
    FILE_TYPE_INVALID = 4003
    
    # 网络错误 5000-5999
    NETWORK_ERROR = 5000
    WEBSOCKET_ERROR = 5001
    API_ERROR = 5002
    
    # 业务逻辑错误 6000-6999
    BUSINESS_ERROR = 6000
    REPORT_GENERATION_ERROR = 6001
    ANALYSIS_ERROR = 6002
    IMPORT_EXPORT_ERROR = 6003


class BaseSystemException(Exception):
    """系统基础异常类"""
    
    def __init__(
        self, 
        message: str, 
        error_code: ErrorCode = ErrorCode.SYSTEM_ERROR,
        details: Optional[Dict[str, Any]] = None,
        cause: Optional[Exception] = None
    ):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        self.cause = cause
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "error_code": self.error_code.value,
            "error_name": self.error_code.name,
            "message": self.message,
            "details": self.details,
            "cause": str(self.cause) if self.cause else None
        }
    
    def __str__(self) -> str:
        return f"[{self.error_code.name}] {self.message}"


class ConfigurationError(BaseSystemException):
    """配置错误"""
    
    def __init__(self, message: str, config_key: Optional[str] = None, **kwargs):
        details = {"config_key": config_key} if config_key else {}
        super().__init__(
            message=message,
            error_code=ErrorCode.CONFIG_ERROR,
            details=details,
            **kwargs
        )


class AuthenticationError(BaseSystemException):
    """认证错误"""
    
    def __init__(self, message: str = "认证失败", **kwargs):
        super().__init__(
            message=message,
            error_code=ErrorCode.AUTH_ERROR,
            **kwargs
        )


class TokenError(AuthenticationError):
    """Token错误"""
    
    def __init__(self, message: str = "Token无效", expired: bool = False, **kwargs):
        error_code = ErrorCode.TOKEN_EXPIRED if expired else ErrorCode.TOKEN_INVALID
        super().__init__(
            message=message,
            error_code=error_code,
            **kwargs
        )


class PermissionError(AuthenticationError):
    """权限错误"""
    
    def __init__(self, message: str = "权限不足", required_permission: Optional[str] = None, **kwargs):
        details = {"required_permission": required_permission} if required_permission else {}
        super().__init__(
            message=message,
            error_code=ErrorCode.PERMISSION_DENIED,
            details=details,
            **kwargs
        )


class DataError(BaseSystemException):
    """数据错误"""
    
    def __init__(self, message: str, data_type: Optional[str] = None, **kwargs):
        details = {"data_type": data_type} if data_type else {}
        super().__init__(
            message=message,
            error_code=ErrorCode.DATA_ERROR,
            details=details,
            **kwargs
        )


class DataNotFoundError(DataError):
    """数据未找到错误"""
    
    def __init__(self, message: str = "数据不存在", resource_id: Optional[str] = None, **kwargs):
        details = {"resource_id": resource_id} if resource_id else {}
        super().__init__(
            message=message,
            error_code=ErrorCode.DATA_NOT_FOUND,
            details=details,
            **kwargs
        )


class DataValidationError(DataError):
    """数据验证错误"""
    
    def __init__(self, message: str = "数据验证失败", validation_errors: Optional[list] = None, **kwargs):
        details = {"validation_errors": validation_errors} if validation_errors else {}
        super().__init__(
            message=message,
            error_code=ErrorCode.DATA_INVALID,
            details=details,
            **kwargs
        )


class FileError(BaseSystemException):
    """文件错误"""
    
    def __init__(self, message: str, file_path: Optional[str] = None, **kwargs):
        details = {"file_path": file_path} if file_path else {}
        super().__init__(
            message=message,
            error_code=ErrorCode.FILE_ERROR,
            details=details,
            **kwargs
        )


class FileNotFoundError(FileError):
    """文件未找到错误"""
    
    def __init__(self, message: str = "文件不存在", file_path: Optional[str] = None, **kwargs):
        super().__init__(
            message=message,
            error_code=ErrorCode.FILE_NOT_FOUND,
            file_path=file_path,
            **kwargs
        )


class FileSizeError(FileError):
    """文件大小错误"""
    
    def __init__(self, message: str = "文件过大", file_size: Optional[int] = None, max_size: Optional[int] = None, **kwargs):
        details = {}
        if file_size:
            details["file_size"] = file_size
        if max_size:
            details["max_size"] = max_size
        
        super().__init__(
            message=message,
            error_code=ErrorCode.FILE_TOO_LARGE,
            details=details,
            **kwargs
        )


class FileTypeError(FileError):
    """文件类型错误"""
    
    def __init__(self, message: str = "文件类型不支持", file_type: Optional[str] = None, allowed_types: Optional[list] = None, **kwargs):
        details = {}
        if file_type:
            details["file_type"] = file_type
        if allowed_types:
            details["allowed_types"] = allowed_types
        
        super().__init__(
            message=message,
            error_code=ErrorCode.FILE_TYPE_INVALID,
            details=details,
            **kwargs
        )


class NetworkError(BaseSystemException):
    """网络错误"""
    
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message=message,
            error_code=ErrorCode.NETWORK_ERROR,
            **kwargs
        )


class WebSocketError(NetworkError):
    """WebSocket错误"""
    
    def __init__(self, message: str = "WebSocket连接错误", client_id: Optional[str] = None, **kwargs):
        details = {"client_id": client_id} if client_id else {}
        super().__init__(
            message=message,
            error_code=ErrorCode.WEBSOCKET_ERROR,
            details=details,
            **kwargs
        )


class APIError(NetworkError):
    """API错误"""
    
    def __init__(self, message: str = "API请求失败", endpoint: Optional[str] = None, status_code: Optional[int] = None, **kwargs):
        details = {}
        if endpoint:
            details["endpoint"] = endpoint
        if status_code:
            details["status_code"] = status_code
        
        super().__init__(
            message=message,
            error_code=ErrorCode.API_ERROR,
            details=details,
            **kwargs
        )


class BusinessError(BaseSystemException):
    """业务逻辑错误"""
    
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message=message,
            error_code=ErrorCode.BUSINESS_ERROR,
            **kwargs
        )


class ReportGenerationError(BusinessError):
    """报告生成错误"""
    
    def __init__(self, message: str = "报告生成失败", report_type: Optional[str] = None, **kwargs):
        details = {"report_type": report_type} if report_type else {}
        super().__init__(
            message=message,
            error_code=ErrorCode.REPORT_GENERATION_ERROR,
            details=details,
            **kwargs
        )


class AnalysisError(BusinessError):
    """分析错误"""
    
    def __init__(self, message: str = "数据分析失败", analysis_type: Optional[str] = None, **kwargs):
        details = {"analysis_type": analysis_type} if analysis_type else {}
        super().__init__(
            message=message,
            error_code=ErrorCode.ANALYSIS_ERROR,
            details=details,
            **kwargs
        )


class ImportExportError(BusinessError):
    """导入导出错误"""
    
    def __init__(self, message: str = "数据导入导出失败", operation: Optional[str] = None, **kwargs):
        details = {"operation": operation} if operation else {}
        super().__init__(
            message=message,
            error_code=ErrorCode.IMPORT_EXPORT_ERROR,
            details=details,
            **kwargs
        )


# 用户相关异常类
class UserNotFoundError(DataNotFoundError):
    """用户不存在错误"""
    
    def __init__(self, message: str = "用户不存在", username: Optional[str] = None, **kwargs):
        details = {"username": username} if username else {}
        super().__init__(
            message=message,
            details=details,
            **kwargs
        )


class UserAlreadyExistsError(DataError):
    """用户已存在错误"""
    
    def __init__(self, message: str = "用户已存在", username: Optional[str] = None, **kwargs):
        details = {"username": username} if username else {}
        super().__init__(
            message=message,
            error_code=ErrorCode.DATA_DUPLICATE,
            details=details,
            **kwargs
        )


class InvalidCredentialsError(AuthenticationError):
    """无效凭据错误"""
    
    def __init__(self, message: str = "用户名或密码错误", **kwargs):
        super().__init__(
            message=message,
            **kwargs
        )


class PermissionDeniedError(PermissionError):
    """权限拒绝错误（别名）"""
    pass


class DataProcessingError(DataError):
    """数据处理错误"""
    
    def __init__(self, message: str = "数据处理失败", data_type: Optional[str] = None, **kwargs):
        super().__init__(
            message=message,
            data_type=data_type,
            **kwargs
        )


def handle_exception(func):
    """异常处理装饰器"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BaseSystemException:
            # 系统自定义异常，直接重新抛出
            raise
        except Exception as e:
            # 其他异常，包装成系统异常
            raise BaseSystemException(
                message=f"未预期的错误: {str(e)}",
                error_code=ErrorCode.SYSTEM_ERROR,
                cause=e
            )
    return wrapper


async def async_handle_exception(func):
    """异步异常处理装饰器"""
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except BaseSystemException:
            # 系统自定义异常，直接重新抛出
            raise
        except Exception as e:
            # 其他异常，包装成系统异常
            raise BaseSystemException(
                message=f"未预期的错误: {str(e)}",
                error_code=ErrorCode.SYSTEM_ERROR,
                cause=e
            )
    return wrapper 