#!/usr/bin/env python3
"""
数据模型定义
包含系统所有的数据模型
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, EmailStr, Field


class UserRole(str, Enum):
    """用户角色枚举"""
    ADMIN = "admin"
    ANALYST = "analyst"
    VIEWER = "viewer"


class User(BaseModel):
    """用户模型"""
    username: str = Field(..., description="用户名")
    role: UserRole = Field(default=UserRole.VIEWER, description="用户角色")
    email: Optional[str] = Field(None, description="邮箱地址")
    is_active: bool = Field(default=True, description="是否激活")
    created_at: Optional[datetime] = Field(default_factory=datetime.now, description="创建时间")
    updated_at: Optional[datetime] = Field(None, description="更新时间")


class UserInDB(User):
    """数据库中的用户模型"""
    hashed_password: str = Field(..., description="密码哈希")


class UserCreate(BaseModel):
    """创建用户请求模型"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    password: str = Field(..., min_length=6, description="密码")
    role: UserRole = Field(default=UserRole.VIEWER, description="用户角色")
    email: Optional[str] = Field(None, description="邮箱地址")


class UserUpdate(BaseModel):
    """更新用户请求模型"""
    role: Optional[UserRole] = Field(None, description="用户角色")
    email: Optional[str] = Field(None, description="邮箱地址")
    is_active: Optional[bool] = Field(None, description="是否激活")


class LoginRequest(BaseModel):
    """登录请求模型"""
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")


class LoginResponse(BaseModel):
    """登录响应模型"""
    access_token: str = Field(..., description="访问令牌")
    token_type: str = Field(default="bearer", description="令牌类型")
    user_info: Dict[str, Any] = Field(..., description="用户信息")


class ReportStatus(str, Enum):
    """报告状态枚举"""
    DRAFT = "草稿"
    GENERATING = "生成中"
    COMPLETED = "已完成"
    FAILED = "失败"


class ReportType(str, Enum):
    """报告类型枚举"""
    MONTHLY = "月度报告"
    WEEKLY = "周报"
    SPECIAL = "专项报告"
    FORECAST = "预测报告"
    INDUSTRY = "行业报告"


class Report(BaseModel):
    """报告模型"""
    id: int = Field(..., description="报告ID")
    title: str = Field(..., description="报告标题")
    type: ReportType = Field(..., description="报告类型")
    status: ReportStatus = Field(default=ReportStatus.DRAFT, description="报告状态")
    description: str = Field("", description="报告描述")
    create_date: datetime = Field(default_factory=datetime.now, description="创建时间")
    file_size: Optional[str] = Field(None, description="文件大小")
    pages: Optional[int] = Field(None, description="页数")
    charts_count: Optional[int] = Field(None, description="图表数量")
    html_file: Optional[str] = Field(None, description="HTML文件路径")
    md_file: Optional[str] = Field(None, description="Markdown文件路径")
    filename: Optional[str] = Field(None, description="文件名")
    icon: Optional[str] = Field(None, description="图标")


class BatchReportRequest(BaseModel):
    """批量报告生成请求"""
    report_ids: List[str] = Field(..., description="报告ID列表")
    output_format: str = Field(default="html", description="输出格式")
    include_charts: bool = Field(default=True, description="是否包含图表")
    async_generation: bool = Field(default=True, description="是否异步生成")


class BatchReportStatus(BaseModel):
    """批量报告生成状态"""
    batch_id: str = Field(..., description="批次ID")
    total_reports: int = Field(..., description="总报告数")
    completed_reports: int = Field(default=0, description="已完成报告数")
    failed_reports: int = Field(default=0, description="失败报告数")
    status: str = Field(..., description="状态")
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    completed_at: Optional[datetime] = Field(None, description="完成时间")
    reports: List[Dict[str, Any]] = Field(default=[], description="报告列表")


class IndustryType(BaseModel):
    """行业类型模型"""
    code: str = Field(..., description="行业代码")
    name: str = Field(..., description="行业名称")
    icon: str = Field(..., description="行业图标")
    description: str = Field(..., description="行业描述")


class MultiIndustryRequest(BaseModel):
    """多行业报告生成请求"""
    industries: List[str] = Field(..., description="行业代码列表")


class SystemSettings(BaseModel):
    """系统设置模型"""
    language: str = Field(default="zh", description="语言")
    timezone: str = Field(default="Asia/Shanghai", description="时区")
    theme: str = Field(default="light", description="主题")
    report_format: str = Field(default="html", description="报告格式")
    auto_generate: bool = Field(default=True, description="自动生成")
    generation_frequency: str = Field(default="daily", description="生成频率")
    email_notifications: bool = Field(default=True, description="邮件通知")
    report_notifications: bool = Field(default=True, description="报告通知")
    system_error_notifications: bool = Field(default=True, description="系统错误通知")


class UserPreferences(BaseModel):
    """用户偏好设置"""
    user_id: str = Field(..., description="用户ID")
    settings: SystemSettings = Field(..., description="设置")


class DataImportRequest(BaseModel):
    """数据导入请求"""
    source_type: str = Field(..., description="数据源类型")
    file_path: Optional[str] = Field(None, description="文件路径")
    data_type: str = Field(..., description="数据类型")
    overwrite: bool = Field(default=False, description="是否覆盖")


class DataExportRequest(BaseModel):
    """数据导出请求"""
    data_type: str = Field(..., description="数据类型")
    format: str = Field(..., description="导出格式")
    date_range: Optional[Dict[str, Any]] = Field(None, description="日期范围")
    filters: Optional[Dict[str, Any]] = Field(None, description="过滤条件")


class DataImportStatus(BaseModel):
    """数据导入状态"""
    import_id: str = Field(..., description="导入ID")
    status: str = Field(..., description="状态")
    total_records: int = Field(default=0, description="总记录数")
    imported_records: int = Field(default=0, description="已导入记录数")
    failed_records: int = Field(default=0, description="失败记录数")
    errors: List[str] = Field(default=[], description="错误列表")
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    completed_at: Optional[datetime] = Field(None, description="完成时间")


class ReportTemplate(BaseModel):
    """报告模板模型"""
    template_id: str = Field(..., description="模板ID")
    name: str = Field(..., description="模板名称")
    description: str = Field(..., description="模板描述")
    template_type: str = Field(..., description="模板类型")
    sections: List[str] = Field(..., description="章节列表")
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.now, description="更新时间")
    created_by: str = Field(..., description="创建者")
    is_active: bool = Field(default=True, description="是否激活")
    settings: Dict[str, Any] = Field(default={}, description="设置")


class CreateTemplateRequest(BaseModel):
    """创建模板请求"""
    name: str = Field(..., description="模板名称")
    description: str = Field(..., description="模板描述")
    template_type: str = Field(..., description="模板类型")
    sections: List[str] = Field(..., description="章节列表")
    settings: Dict[str, Any] = Field(default={}, description="设置")


class AnalysisRequest(BaseModel):
    """分析请求模型"""
    data_source: str = Field(..., description="数据源")
    analysis_type: str = Field(..., description="分析类型")
    parameters: Dict[str, Any] = Field(default={}, description="参数")


class AnalysisResult(BaseModel):
    """分析结果模型"""
    analysis_id: str = Field(..., description="分析ID")
    analysis_type: str = Field(..., description="分析类型")
    status: str = Field(..., description="状态")
    results: Dict[str, Any] = Field(..., description="结果")
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    completed_at: Optional[datetime] = Field(None, description="完成时间")


class WebSocketMessage(BaseModel):
    """WebSocket消息模型"""
    type: str = Field(..., description="消息类型")
    data: Dict[str, Any] = Field(default={}, description="消息数据")
    timestamp: datetime = Field(default_factory=datetime.now, description="时间戳")


class SystemStatus(BaseModel):
    """系统状态模型"""
    status: str = Field(..., description="系统状态")
    uptime: str = Field(..., description="运行时间")
    version: str = Field(..., description="版本")
    cpu_usage: float = Field(..., description="CPU使用率")
    memory_usage: float = Field(..., description="内存使用率")
    disk_usage: float = Field(..., description="磁盘使用率")
    active_connections: int = Field(default=0, description="活跃连接数")


class APIResponse(BaseModel):
    """API响应模型"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="消息")
    data: Optional[Dict[str, Any]] = Field(None, description="数据")
    error_code: Optional[int] = Field(None, description="错误代码")
    timestamp: datetime = Field(default_factory=datetime.now, description="时间戳")


class PaginatedResponse(BaseModel):
    """分页响应模型"""
    items: List[Any] = Field(..., description="数据项")
    total: int = Field(..., description="总数")
    page: int = Field(..., description="当前页")
    size: int = Field(..., description="页大小")
    pages: int = Field(..., description="总页数")


class SearchRequest(BaseModel):
    """搜索请求模型"""
    query: str = Field(..., description="搜索关键词")
    filters: Optional[Dict[str, Any]] = Field(None, description="过滤条件")
    page: int = Field(default=1, ge=1, description="页码")
    size: int = Field(default=20, ge=1, le=100, description="页大小")
    sort_by: Optional[str] = Field(None, description="排序字段")
    sort_order: Optional[str] = Field(default="desc", description="排序顺序")


class FileUploadResponse(BaseModel):
    """文件上传响应模型"""
    filename: str = Field(..., description="文件名")
    file_path: str = Field(..., description="文件路径")
    file_size: int = Field(..., description="文件大小")
    upload_time: datetime = Field(default_factory=datetime.now, description="上传时间")
    file_type: str = Field(..., description="文件类型")


# 类型别名
UserList = List[User]
ReportList = List[Report]
IndustryList = List[IndustryType] 