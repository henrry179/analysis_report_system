import os
import sys
from pathlib import Path
import json
from datetime import datetime, timedelta
import psutil
import platform
import socket
import subprocess
from fastapi import FastAPI, HTTPException, Depends, status, Request, BackgroundTasks, UploadFile, Form, File, WebSocket, WebSocketDisconnect
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from passlib.hash import bcrypt
import uvicorn
import glob
from typing import Optional, List, Dict
import asyncio

# 添加项目根目录到Python路径
project_root = str(Path(__file__).parent.parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

# 条件导入，优雅处理缺失依赖
try:
    from main import AnalysisReportSystem
    MAIN_AVAILABLE = True
except ImportError:
    MAIN_AVAILABLE = False
    print("⚠️  警告: 主程序模块导入失败")

try:
    from pydantic import BaseModel
    PYDANTIC_AVAILABLE = True
except ImportError:
    PYDANTIC_AVAILABLE = False
    # 创建简单的BaseModel替代
    class BaseModel:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

try:
    from analysis.metrics_analyzer import MetricsAnalyzer
    from visualization.chart_generator import ChartGenerator
    ANALYSIS_MODULES_AVAILABLE = True
except ImportError:
    ANALYSIS_MODULES_AVAILABLE = False
    print("⚠️  警告: 分析或可视化模块导入失败")

try:
    from report.report_generator import ReportGenerator, ReportData
    REPORT_GENERATOR_AVAILABLE = True
except ImportError:
    REPORT_GENERATOR_AVAILABLE = False
    print("⚠️  警告: 报告生成器模块导入失败")

try:
    from analysis.professional_analytics import ProfessionalAnalytics, AnalysisConfig
    PROFESSIONAL_ANALYTICS_AVAILABLE = True
except ImportError:
    PROFESSIONAL_ANALYTICS_AVAILABLE = False
    print("⚠️  警告: 专业分析工具导入失败")

# 创建FastAPI应用
app = FastAPI(
    title="🚀 业务分析报告自动化系统",
    description="🏪 专业零售业务分析报告系统 - 智能分析 · 数据驱动 · 洞察未来",
    version="v3.2 Optimized",
    docs_url="/docs",  # 保留但设为开发者用途
    redoc_url=None,    # 隐藏ReDoc
    openapi_url="/openapi.json"
)

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="src/static"), name="static")

# 设置模板目录
templates = Jinja2Templates(directory="src/templates")

# 系统启动时间
SYSTEM_START_TIME = datetime.now()

# 示例图表数据
chart_data = {
    "pie": {
        "labels": ["类别A", "类别B", "类别C", "类别D"],
        "values": [30, 25, 20, 25],
        "title": "销售分布"
    },
    "bar": {
        "labels": ["1月", "2月", "3月", "4月", "5月"],
        "values": [100, 120, 90, 150, 130],
        "title": "月度销售趋势"
    },
    "line": {
        "labels": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"],
        "values": [65, 59, 80, 81, 56, 55, 40],
        "title": "一周访问量趋势"
    }
}

# 报告文件目录配置
REPORTS_DIR = os.path.join(project_root, "output", "reports")
PDF_REPORTS_DIR = os.path.join(project_root, "pdf_reports")
os.makedirs(PDF_REPORTS_DIR, exist_ok=True)

# 更新报告数据，添加实际文件路径
def get_actual_reports():
    """获取实际的报告文件列表"""
    actual_reports = []
    
    # 查找HTML报告文件
    html_files = glob.glob(os.path.join(REPORTS_DIR, "*.html"))
    md_files = glob.glob(os.path.join(REPORTS_DIR, "*.md"))
    
    for i, html_file in enumerate(html_files):
        filename = os.path.basename(html_file)
        name_without_ext = os.path.splitext(filename)[0]
        
        # 确定报告类型和标题
        if "retail_advanced_report" in filename:
            report_type = "零售深度分析"
            title_prefix = "🏪 零售行业深度分析报告"
            icon = "🏪"
        elif "retail_business_report" in filename:
            report_type = "零售月度报告"
            title_prefix = "🏪 零售业务分析报告"
            icon = "🏪"
        elif "community_group_buying_report" in filename:
            report_type = "社区团购分析"
            title_prefix = "🏘️ 社区团购行业分析报告"
            icon = "🏘️"
        elif "financial_trading_report" in filename:
            report_type = "金融交易分析"
            title_prefix = "💰 金融交易行业分析报告"
            icon = "💰"
        elif "ai_agent_industry_report" in filename:
            report_type = "智能体分析"
            title_prefix = "🤖 智能体行业分析报告"
            icon = "🤖"
        elif "cross_industry_analysis" in filename:
            report_type = "跨行业对比"
            title_prefix = "🔄 跨行业对比分析报告"
            icon = "🔄"
        elif "intelligent_report" in filename:
            report_type = "智能分析报告"
            title_prefix = "🧠 智能分析报告"
            icon = "🧠"
        else:
            report_type = "分析报告"
            title_prefix = "📊 分析报告"
            icon = "📊"
        
        # 从文件名提取日期
        try:
            if "_" in filename:
                parts = filename.split("_")
                if len(parts) >= 2:
                    date_str = parts[-2] + "_" + parts[-1].replace(".html", "")
                    create_date = datetime.strptime(date_str, "%Y%m%d_%H%M%S").strftime("%Y-%m-%d %H:%M")
                else:
                    create_date = datetime.now().strftime("%Y-%m-%d %H:%M")
            else:
                create_date = datetime.now().strftime("%Y-%m-%d %H:%M")
        except:
            create_date = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # 获取文件大小
        try:
            file_size = os.path.getsize(html_file)
            if file_size > 1024 * 1024:
                size_str = f"{file_size / (1024 * 1024):.1f}MB"
            else:
                size_str = f"{file_size / 1024:.1f}KB"
        except:
            size_str = "未知"
        
        # 检查是否有对应的Markdown文件
        md_file = html_file.replace(".html", ".md")
        has_md = os.path.exists(md_file)
        
        # 根据报告类型生成不同的描述
        if "retail" in filename:
            description = "基于零售业务数据生成的深度分析报告，包含销售趋势、区域分析、品类表现和运营指标"
            charts_count = 8 + (i * 2)
            pages = 25 + (i * 5)
        elif "community" in filename:
            description = "社区团购行业专业分析报告，涵盖订单分析、城市覆盖、团长表现和用户行为洞察"
            charts_count = 6 + (i * 2)
            pages = 20 + (i * 3)
        elif "financial" in filename:
            description = "金融交易行业全面分析报告，包含交易量分析、风险评估、产品表现和投资建议"
            charts_count = 10 + (i * 2)
            pages = 30 + (i * 5)
        elif "ai_agent" in filename:
            description = "智能体行业前沿分析报告，展示智能体类型分布、应用场景、技术能力和发展趋势"
            charts_count = 7 + (i * 2)
            pages = 22 + (i * 4)
        elif "cross_industry" in filename:
            description = "跨行业对比分析报告，多维度比较不同行业的发展状况、数字化水平和市场机会"
            charts_count = 12 + (i * 2)
            pages = 35 + (i * 5)
        else:
            description = f"基于数据分析生成的{report_type}，包含详细的业务指标和趋势分析"
            charts_count = 8 + (i * 2)
            pages = 25 + (i * 5)
        
        actual_reports.append({
            "id": i + 1,
            "title": f"{title_prefix}",
            "type": report_type,
            "create_date": create_date,
            "status": "已完成",
            "description": description,
            "file_size": size_str,
            "pages": pages,
            "charts_count": charts_count,
            "summary": f"本期报告显示各项关键指标表现{['优异', '良好', '稳定'][i % 3]}，为业务决策提供了重要参考。",
            "html_file": html_file,
            "md_file": md_file if has_md else None,
            "filename": name_without_ext,
            "icon": icon
        })
    
    # 按创建时间排序，最新的在前
    actual_reports.sort(key=lambda x: x['create_date'], reverse=True)
    
    return actual_reports

# 更新全局报告数据
reports_data = get_actual_reports()

# 用户相关模型和数据
fake_users_db = {
    "admin": {"username": "admin", "hashed_password": "simple_hash_adminpass", "role": "admin"},
    "analyst": {"username": "analyst", "hashed_password": "simple_hash_analyst123", "role": "analyst"},
    "viewer": {"username": "viewer", "hashed_password": "simple_hash_viewer123", "role": "viewer"}
}

class User(BaseModel):
    username: str
    role: str

class UserInDB(User):
    hashed_password: str

def create_user(username: str, password: str, role: str = "user"):
    """创建新用户"""
    if username in fake_users_db:
        return False
    
    hashed_password = f"simple_hash_{password}"
    fake_users_db[username] = {
        "username": username,
        "hashed_password": hashed_password,
        "role": role
    }
    return True

# OAuth2设置
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

def get_current_user(token: str = Depends(oauth2_scheme)):
    """获取当前用户"""
    if not token:
        return None
    user = fake_users_db.get(token)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return User(**user)

def get_system_stats():
    """获取系统统计信息"""
    try:
        # CPU使用率
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # 内存使用情况
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        memory_used = round(memory.used / 1024 / 1024 / 1024, 2)  # GB
        memory_total = round(memory.total / 1024 / 1024 / 1024, 2)  # GB
        
        # 磁盘使用情况
        disk = psutil.disk_usage('/')
        disk_percent = round((disk.used / disk.total) * 100, 1)
        disk_used = round(disk.used / 1024 / 1024 / 1024, 2)  # GB
        disk_total = round(disk.total / 1024 / 1024 / 1024, 2)  # GB
        
        # 系统运行时间
        uptime = datetime.now() - SYSTEM_START_TIME
        uptime_str = f"{uptime.days}天 {uptime.seconds//3600}小时 {(uptime.seconds//60)%60}分钟"
        
        return {
            "cpu_percent": cpu_percent,
            "memory_percent": memory_percent,
            "memory_used": memory_used,
            "memory_total": memory_total,
            "disk_percent": disk_percent,
            "disk_used": disk_used,
            "disk_total": disk_total,
            "uptime": uptime_str,
            "platform": platform.system(),
            "python_version": platform.python_version()
        }
    except:
        # 模拟数据作为后备
        return {
            "cpu_percent": 25.6,
            "memory_percent": 68.2,
            "memory_used": 5.5,
            "memory_total": 8.0,
            "disk_percent": 45.3,
            "disk_used": 45.3,
            "disk_total": 100.0,
            "uptime": "2天 15小时 30分钟",
            "platform": "模拟系统",
            "python_version": "3.12.0"
        }

# 在app创建后添加专业分析实例
if PROFESSIONAL_ANALYTICS_AVAILABLE:
    analytics_engine = ProfessionalAnalytics()
else:
    analytics_engine = None

# 新增系统设置相关的数据模型
class SystemSettings(BaseModel):
    """系统设置模型"""
    language: str = "zh"
    timezone: str = "Asia/Shanghai"
    theme: str = "light"
    report_format: str = "pdf"
    auto_generate: bool = True
    generation_frequency: str = "daily"
    email_notifications: bool = True
    report_notifications: bool = True
    system_error_notifications: bool = True

class UserPreferences(BaseModel):
    """用户偏好设置"""
    user_id: str
    settings: SystemSettings

# 系统设置存储（模拟数据库）
system_settings_db = {
    "default": SystemSettings(),
    "admin": SystemSettings()
}

# 新增批量报告生成相关的数据模型
class BatchReportRequest(BaseModel):
    """批量报告生成请求"""
    report_ids: List[str]
    output_format: str = "pdf"
    include_charts: bool = True
    async_generation: bool = True

class BatchReportStatus(BaseModel):
    """批量报告生成状态"""
    batch_id: str
    total_reports: int
    completed_reports: int
    failed_reports: int
    status: str  # pending, processing, completed, failed
    created_at: datetime
    completed_at: Optional[datetime] = None
    reports: List[dict]

# 批量报告状态存储
batch_report_status_db = {}

# 新增数据导入导出相关的数据模型
class DataImportRequest(BaseModel):
    """数据导入请求"""
    source_type: str  # csv, excel, json
    file_path: Optional[str] = None
    data_type: str  # sales, customer, product, etc.
    overwrite: bool = False

class DataExportRequest(BaseModel):
    """数据导出请求"""
    data_type: str  # report, analysis, raw_data
    format: str  # csv, excel, json, pdf
    date_range: Optional[dict] = None
    filters: Optional[dict] = None

class DataImportStatus(BaseModel):
    """数据导入状态"""
    import_id: str
    status: str  # pending, processing, completed, failed
    total_records: int = 0
    imported_records: int = 0
    failed_records: int = 0
    errors: List[str] = []
    created_at: datetime
    completed_at: Optional[datetime] = None

# 数据导入状态存储
data_import_status_db = {}

# 新增报告模板管理相关的数据模型
class ReportTemplate(BaseModel):
    """报告模板模型"""
    template_id: str
    name: str
    description: str
    template_type: str  # monthly, quarterly, annual, custom
    sections: List[str]
    created_at: datetime
    updated_at: datetime
    created_by: str
    is_active: bool = True
    settings: dict = {}

class CreateTemplateRequest(BaseModel):
    """创建模板请求"""
    name: str
    description: str
    template_type: str
    sections: List[str]
    settings: dict = {}

# 报告模板存储（模拟数据库）
report_templates_db = {
    "default_monthly": ReportTemplate(
        template_id="default_monthly",
        name="月度分析报告模板",
        description="标准月度业务分析报告模板",
        template_type="monthly",
        sections=["执行摘要", "核心指标", "趋势分析", "品类分析", "建议"],
        created_at=datetime.now(),
        updated_at=datetime.now(),
        created_by="system",
        is_active=True
    ),
    "default_quarterly": ReportTemplate(
        template_id="default_quarterly",
        name="季度总结报告模板",
        description="标准季度业务总结报告模板",
        template_type="quarterly",
        sections=["季度概览", "业绩回顾", "市场分析", "下季度计划"],
        created_at=datetime.now(),
        updated_at=datetime.now(),
        created_by="system",
        is_active=True
    )
}

# 批量报告处理函数
async def process_batch_reports(
    batch_id: str,
    report_ids: List[str],
    output_format: str,
    include_charts: bool,
    user_id: Optional[str] = None
):
    """处理批量报告生成（支持WebSocket进度推送）"""
    status = batch_report_status_db[batch_id]
    status.status = "processing"
    
    # 发送开始处理通知
    if user_id:
        await manager.send_json_to_user({
            "type": "batch_report_progress",
            "batch_id": batch_id,
            "status": "processing",
            "message": "开始处理批量报告生成任务",
            "progress": 0,
            "total": len(report_ids)
        }, user_id)
    
    try:
        for idx, report_id in enumerate(report_ids):
            try:
                # 发送单个报告处理进度
                if user_id:
                    await manager.send_json_to_user({
                        "type": "batch_report_progress",
                        "batch_id": batch_id,
                        "status": "processing",
                        "message": f"正在处理报告 {report_id} ({idx+1}/{len(report_ids)})",
                        "progress": idx,
                        "total": len(report_ids),
                        "current_report": report_id
                    }, user_id)
                
                # 查找报告
                report_path = None
                for file_path in glob.glob("output/reports/*.html"):
                    if report_id in file_path:
                        report_path = file_path
                        break
                
                if not report_path:
                    status.failed_reports += 1
                    status.reports.append({
                        "report_id": report_id,
                        "status": "failed",
                        "error": "报告不存在"
                    })
                    continue
                
                # 模拟处理时间
                await asyncio.sleep(0.5)
                
                # 根据格式生成报告
                if output_format == "pdf":
                    # 使用现有的PDF生成逻辑
                    pdf_path = report_path.replace('.html', '.pdf').replace('output/reports/', 'pdf_reports/')
                    # 这里可以调用实际的PDF生成函数
                    status.reports.append({
                        "report_id": report_id,
                        "status": "completed",
                        "output_path": pdf_path
                    })
                else:
                    status.reports.append({
                        "report_id": report_id,
                        "status": "completed",
                        "output_path": report_path
                    })
                
                status.completed_reports += 1
                
            except Exception as e:
                status.failed_reports += 1
                status.reports.append({
                    "report_id": report_id,
                    "status": "failed",
                    "error": str(e)
                })
        
        status.status = "completed"
        status.completed_at = datetime.now()
        
        # 发送完成通知
        if user_id:
            await manager.send_json_to_user({
                "type": "batch_report_progress",
                "batch_id": batch_id,
                "status": "completed",
                "message": "批量报告生成完成",
                "progress": len(report_ids),
                "total": len(report_ids),
                "completed": status.completed_reports,
                "failed": status.failed_reports
            }, user_id)
        
    except Exception as e:
        status.status = "failed"
        status.completed_at = datetime.now()
        print(f"批量报告生成失败: {str(e)}")
        
        # 发送失败通知
        if user_id:
            await manager.send_json_to_user({
                "type": "batch_report_progress",
                "batch_id": batch_id,
                "status": "failed",
                "message": f"批量报告生成失败: {str(e)}",
                "error": str(e)
            }, user_id)

# 路由定义
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """首页 - 显示系统信息和图表"""
    return templates.TemplateResponse("index.html", {"request": request})

# WebSocket端点 - 放在路由定义开始位置
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """WebSocket端点"""
    await manager.connect(websocket, client_id)
    try:
        # 发送连接成功消息
        await manager.send_json_to_user({
            "type": "connection",
            "status": "connected",
            "message": f"WebSocket连接成功，客户端ID: {client_id}",
            "timestamp": datetime.now().isoformat()
        }, client_id)
        
        while True:
            # 接收客户端消息
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # 处理不同类型的消息
            if message.get("type") == "ping":
                # 响应ping消息
                await manager.send_json_to_user({
                    "type": "pong",
                    "timestamp": datetime.now().isoformat()
                }, client_id)
            elif message.get("type") == "subscribe":
                # 订阅特定事件
                event_type = message.get("event_type")
                await manager.send_json_to_user({
                    "type": "subscription",
                    "event_type": event_type,
                    "status": "subscribed",
                    "message": f"已订阅 {event_type} 事件"
                }, client_id)
            else:
                # 回显其他消息
                await manager.send_json_to_user({
                    "type": "echo",
                    "original_message": message,
                    "timestamp": datetime.now().isoformat()
                }, client_id)
                
    except WebSocketDisconnect:
        manager.disconnect(websocket, client_id)
        # 广播断开连接消息（可选）
        await manager.broadcast_json({
            "type": "connection",
            "status": "disconnected",
            "client_id": client_id,
            "message": f"客户端 {client_id} 已断开连接",
            "timestamp": datetime.now().isoformat()
        }, exclude_client=client_id)

@app.get("/reports", response_class=HTMLResponse)
async def reports_list(request: Request):
    """报告列表页面"""
    return templates.TemplateResponse("reports.html", {
        "request": request, 
        "reports": reports_data,
        "total_reports": len(reports_data)
    })

@app.get("/reports/{report_id}", response_class=HTMLResponse)
async def report_detail(request: Request, report_id: int):
    """报告详情页面"""
    report = next((r for r in reports_data if r["id"] == report_id), None)
    if not report:
        raise HTTPException(status_code=404, detail="报告不存在")
    
    return templates.TemplateResponse("report_detail.html", {
        "request": request,
        "report": report
    })

@app.get("/analysis", response_class=HTMLResponse)
async def analysis_center(request: Request):
    """分析中心页面"""
    return templates.TemplateResponse("analysis.html", {"request": request})

@app.get("/settings", response_class=HTMLResponse)
async def settings_page(request: Request):
    """系统设置页面"""
    return templates.TemplateResponse("settings.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """系统仪表盘页面"""
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/users", response_class=HTMLResponse)
async def user_management(request: Request):
    """用户管理页面"""
    return templates.TemplateResponse("user_management.html", {"request": request})

@app.get("/api-docs", response_class=HTMLResponse)
async def api_documentation(request: Request):
    """API文档页面"""
    return templates.TemplateResponse("api_docs.html", {"request": request})

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """用户登录"""
    user_dict = fake_users_db.get(form_data.username)
    
    password_valid = False
    if user_dict:
        password_valid = user_dict["hashed_password"] == f"simple_hash_{form_data.password}"
    
    if not password_valid:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": form_data.username, "token_type": "bearer"}

@app.get("/api/info")
async def get_info():
    """获取系统信息"""
    return {
        "title": "业务分析报告自动化系统",
        "version": "v3.3 Enhanced",
        "status": "运行中",
        "features": [
            "智能数据分析",
            "自动报告生成",
            "多格式输出",
            "实时监控"
        ]
    }

@app.get("/api/system/stats")
async def get_system_statistics():
    """获取系统性能统计"""
    return JSONResponse(content=get_system_stats())

@app.get("/api/dashboard/overview")
async def get_dashboard_overview():
    """获取仪表盘概览数据"""
    stats = get_system_stats()
    
    # 报告统计
    total_reports = len(reports_data)
    completed_reports = len([r for r in reports_data if r["status"] == "已完成"])
    draft_reports = len([r for r in reports_data if r["status"] == "草稿"])
    
    # 用户统计
    total_users = len(fake_users_db)
    admin_users = len([u for u in fake_users_db.values() if u["role"] == "admin"])
    
    return {
        "system": stats,
        "reports": {
            "total": total_reports,
            "completed": completed_reports,
            "draft": draft_reports,
            "completion_rate": round((completed_reports / total_reports) * 100, 1) if total_reports > 0 else 0
        },
        "users": {
            "total": total_users,
            "admin": admin_users,
            "active": total_users  # 模拟所有用户都活跃
        },
        "performance": {
            "response_time": "125ms",
            "throughput": "1.2k req/min",
            "error_rate": "0.05%"
        }
    }

@app.get("/api/dashboard/charts")
async def get_dashboard_charts():
    """获取仪表盘图表数据"""
    return {
        "system_performance": {
            "labels": ["CPU", "内存", "磁盘", "网络"],
            "values": [25.6, 68.2, 45.3, 12.8],
            "title": "系统资源使用率"
        },
        "report_types": {
            "labels": ["月度报告", "周报", "专项报告", "预测报告"],
            "values": [1, 1, 1, 1],
            "title": "报告类型分布"
        },
        "user_activity": {
            "labels": ["今日", "昨日", "3天前", "4天前", "5天前", "6天前", "7天前"],
            "values": [45, 38, 52, 41, 35, 49, 43],
            "title": "用户活跃度趋势"
        }
    }

@app.post("/api/reports/batch/generate", response_model=BatchReportStatus)
async def generate_batch_reports(
    request: BatchReportRequest,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
):
    """批量生成报告"""
    import uuid
    
    batch_id = str(uuid.uuid4())
    status = BatchReportStatus(
        batch_id=batch_id,
        total_reports=len(request.report_ids),
        completed_reports=0,
        failed_reports=0,
        status="pending",
        created_at=datetime.now(),
        reports=[]
    )
    
    batch_report_status_db[batch_id] = status
    
    if request.async_generation:
        # 使用asyncio.create_task来处理异步函数
        asyncio.create_task(process_batch_reports(
            batch_id,
            request.report_ids,
            request.output_format,
            request.include_charts,
            current_user["username"]
        ))
        status.status = "processing"
    else:
        # 同步生成
        await process_batch_reports(
            batch_id,
            request.report_ids,
            request.output_format,
            request.include_charts,
            current_user["username"]
        )
    
    return status

@app.get("/api/reports/batch/{batch_id}/status", response_model=BatchReportStatus)
async def get_batch_report_status(
    batch_id: str,
    current_user: dict = Depends(get_current_user)
):
    """获取批量报告生成状态"""
    if batch_id not in batch_report_status_db:
        raise HTTPException(status_code=404, detail="批次不存在")
    
    return batch_report_status_db[batch_id]

@app.post("/api/reports/batch/{batch_id}/cancel")
async def cancel_batch_reports(
    batch_id: str,
    current_user: dict = Depends(get_current_user)
):
    """取消批量报告生成"""
    if batch_id not in batch_report_status_db:
        raise HTTPException(status_code=404, detail="批次不存在")
    
    status = batch_report_status_db[batch_id]
    if status.status in ["completed", "failed"]:
        raise HTTPException(status_code=400, detail="任务已经完成或失败，无法取消")
    
    status.status = "cancelled"
    status.completed_at = datetime.now()
    
    return {"message": "批量报告生成已取消"}

@app.get("/api/reports")
async def get_reports():
    """获取报告列表"""
    return JSONResponse(content={"reports": reports_data, "total": len(reports_data)})

@app.get("/api/reports/industry-types")
async def get_industry_types():
    """获取支持的行业类型"""
    return {
        "success": True,
        "industries": [
            {
                "code": "retail",
                "name": "零售行业",
                "icon": "🏪",
                "description": "零售业务深度分析，包含销售数据、区域分析、品类表现"
            },
            {
                "code": "community",
                "name": "社区团购",
                "icon": "🏘️",
                "description": "社区团购行业分析，涵盖订单数据、城市覆盖、团长运营"
            },
            {
                "code": "financial",
                "name": "金融交易",
                "icon": "💰",
                "description": "金融交易行业分析，包含交易量、风险评估、产品表现"
            },
            {
                "code": "ai_agent",
                "name": "智能体",
                "icon": "🤖",
                "description": "智能体行业分析，展示技术发展、应用场景、市场趋势"
            },
            {
                "code": "cross_industry",
                "name": "跨行业对比",
                "icon": "🔄",
                "description": "跨行业对比分析，多维度比较不同行业发展状况"
            }
        ]
    }

@app.get("/api/reports/{report_id}")
async def get_report_detail(report_id: int):
    """获取报告详情"""
    report = next((r for r in reports_data if r["id"] == report_id), None)
    if not report:
        raise HTTPException(status_code=404, detail="报告不存在")
    return JSONResponse(content=report)

@app.post("/api/reports/{report_id}/generate")
async def generate_report(report_id: int):
    """生成报告API"""
    report = next((r for r in reports_data if r["id"] == report_id), None)
    if not report:
        raise HTTPException(status_code=404, detail="报告不存在")
    
    # 模拟报告生成过程
    if report["status"] == "草稿":
        report["status"] = "生成中"
        # 这里可以添加实际的报告生成逻辑
        return JSONResponse(content={"message": "报告生成已启动", "status": "生成中"})
    else:
        return JSONResponse(content={"message": "报告已存在", "status": report["status"]})

@app.get("/api/users")
async def get_users(current_user: User = Depends(get_current_user)):
    """获取用户列表API（需要管理员权限）"""
    if not current_user or current_user.role != "admin":
        raise HTTPException(status_code=403, detail="需要管理员权限")
    
    users = [
        {"username": user["username"], "role": user["role"]} 
        for user in fake_users_db.values()
    ]
    return {"users": users, "total": len(users)}

@app.post("/api/users")
async def create_user_api(user_data: dict, current_user: User = Depends(get_current_user)):
    """创建用户API（需要管理员权限）"""
    if not current_user or current_user.role != "admin":
        raise HTTPException(status_code=403, detail="需要管理员权限")
    
    username = user_data.get("username")
    password = user_data.get("password")
    role = user_data.get("role", "viewer")
    
    if not username or not password:
        raise HTTPException(status_code=400, detail="用户名和密码不能为空")
    
    if create_user(username, password, role):
        return {"message": f"用户 {username} 创建成功"}
    else:
        raise HTTPException(status_code=400, detail="用户已存在")

@app.get("/charts")
async def get_charts():
    """获取所有图表数据"""
    return JSONResponse(content=chart_data)

@app.get("/charts/{chart_type}")
async def get_chart(chart_type: str):
    """获取指定类型的图表数据"""
    if chart_type not in chart_data:
        raise HTTPException(status_code=404, detail="图表类型不存在")
    return JSONResponse(content=chart_data[chart_type])

@app.get("/api/reports/{report_id}/download/{format}")
async def download_report(report_id: int, format: str):
    """下载报告文件"""
    report = next((r for r in reports_data if r["id"] == report_id), None)
    if not report:
        raise HTTPException(status_code=404, detail="报告不存在")
    
    if format == "html" and report.get("html_file"):
        file_path = report["html_file"]
        filename = f"{report['filename']}.html"
    elif format == "md" and report.get("md_file"):
        file_path = report["md_file"]
        filename = f"{report['filename']}.md"
    elif format == "pdf":
        # 生成PDF文件
        pdf_path = await generate_pdf_report(report)
        if not pdf_path:
            raise HTTPException(status_code=500, detail="PDF生成失败")
        file_path = pdf_path
        filename = f"{report['filename']}.pdf"
    else:
        raise HTTPException(status_code=404, detail="文件格式不支持或文件不存在")
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="文件不存在")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='application/octet-stream'
    )

@app.get("/api/reports/{report_id}/preview")
async def preview_report(report_id: int):
    """在线预览报告"""
    report = next((r for r in reports_data if r["id"] == report_id), None)
    if not report:
        raise HTTPException(status_code=404, detail="报告不存在")
    
    if not report.get("html_file") or not os.path.exists(report["html_file"]):
        raise HTTPException(status_code=404, detail="预览文件不存在")
    
    # 读取HTML文件内容
    try:
        with open(report["html_file"], 'r', encoding='utf-8') as f:
            content = f.read()
        return HTMLResponse(content=content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"读取文件失败: {str(e)}")

async def generate_pdf_report(report):
    """生成PDF报告"""
    try:
        if not REPORT_GENERATOR_AVAILABLE:
            print("⚠️  报告生成器不可用")
            return None
        
        # 创建报告生成器
        generator = ReportGenerator(
            template_dir=os.path.join(project_root, "src", "templates"),
            output_dir=PDF_REPORTS_DIR
        )
        
        # 创建报告数据（基于现有报告内容）
        report_data = ReportData(
            report_date=report['create_date'],
            gmv_change_rate=15.2,
            dau_change_rate=8.5,
            frequency_change_rate=12.1,
            order_price_change_rate=5.8,
            conversion_rate_change=3.2,
            order_price_contribution=35.6,
            conversion_rate_contribution=18.9,
            dau_contribution=42.5,
            frequency_contribution=28.3,
            category_gini=0.8421,
            region_gini=0.6789,
            category_price_contribution=22.1,
            current_gmv=1250000.0,
            previous_gmv=1086956.5,
            current_dau=85000,
            previous_dau=78341,
            current_frequency=2.85,
            previous_frequency=2.54,
            current_order_price=147.5,
            previous_order_price=139.2,
            current_conversion_rate=4.82,
            previous_conversion_rate=4.66,
            improvement_suggestions=[
                "优化高价值客户的服务体验",
                "加强新客户获取渠道建设",
                "提升产品推荐算法精准度",
                "优化移动端用户购买流程"
            ]
        )
        
        # 生成PDF
        pdf_path = generator.generate_report(report_data, format='pdf')
        return pdf_path
        
    except Exception as e:
        print(f"⚠️  PDF生成失败: {e}")
        return None

@app.post("/api/reports/{report_id}/generate-pdf")
async def generate_pdf_endpoint(report_id: int):
    """生成PDF报告API"""
    report = next((r for r in reports_data if r["id"] == report_id), None)
    if not report:
        raise HTTPException(status_code=404, detail="报告不存在")
    
    pdf_path = await generate_pdf_report(report)
    if pdf_path:
        return JSONResponse(content={
            "message": "PDF生成成功",
            "status": "completed",
            "download_url": f"/api/reports/{report_id}/download/pdf"
        })
    else:
        return JSONResponse(content={
            "message": "PDF生成失败，可能缺少必要依赖",
            "status": "failed",
            "suggestion": "请安装 wkhtmltopdf 和 pdfkit: pip install pdfkit"
        })

def check_port_available(host: str, port: int) -> bool:
    """检查端口是否可用"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            result = sock.connect_ex((host, port))
            return result != 0
    except Exception:
        return False

def find_available_port(start_port: int = 8000, max_attempts: int = 10) -> int:
    """查找可用端口"""
    for port in range(start_port, start_port + max_attempts):
        if check_port_available("127.0.0.1", port):
            return port
    return None

def kill_process_on_port(port: int) -> bool:
    """尝试终止占用端口的进程（跨平台支持）"""
    try:
        system = platform.system().lower()
        
        if system == "windows":
            # Windows系统使用netstat和taskkill
            result = subprocess.run(
                ['netstat', '-ano'], 
                capture_output=True, 
                text=True, 
                timeout=5
            )
            
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    if f':{port}' in line and 'LISTENING' in line:
                        parts = line.split()
                        if len(parts) >= 5:
                            pid = parts[-1]
                            try:
                                subprocess.run(['taskkill', '/PID', pid, '/F'], timeout=3, check=True)
                                print(f"✅ 已终止占用端口{port}的进程 (PID: {pid})")
                                return True
                            except subprocess.CalledProcessError:
                                continue
        else:
            # Unix/Linux系统使用lsof和kill
            result = subprocess.run(
                ['lsof', '-ti', f':{port}'], 
                capture_output=True, 
                text=True, 
                timeout=5
            )
            
            if result.returncode == 0 and result.stdout.strip():
                pids = result.stdout.strip().split('\n')
                for pid in pids:
                    try:
                        # 尝试优雅地终止进程
                        subprocess.run(['kill', '-TERM', pid], timeout=3, check=True)
                        print(f"✅ 已终止占用端口{port}的进程 (PID: {pid})")
                        return True
                    except subprocess.CalledProcessError:
                        # 如果优雅终止失败，强制终止
                        try:
                            subprocess.run(['kill', '-KILL', pid], timeout=3, check=True)
                            print(f"⚠️  强制终止占用端口{port}的进程 (PID: {pid})")
                            return True
                        except:
                            continue
        return False
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
        return False

def show_port_status(port: int):
    """显示端口状态信息（跨平台支持）"""
    try:
        system = platform.system().lower()
        
        if system == "windows":
            # Windows系统使用netstat
            result = subprocess.run(
                ['netstat', '-ano'], 
                capture_output=True, 
                text=True, 
                timeout=3
            )
            
            if result.returncode == 0:
                print(f"\n📊 端口 {port} 使用情况:")
                print("-" * 50)
                lines = result.stdout.split('\n')
                found = False
                for line in lines:
                    if f':{port}' in line and ('LISTENING' in line or 'ESTABLISHED' in line):
                        parts = line.split()
                        if len(parts) >= 5:
                            print(f"协议: {parts[0]}, 地址: {parts[1]}, 状态: {parts[3]}, PID: {parts[4]}")
                            found = True
                if not found:
                    print(f"未找到使用端口 {port} 的进程")
                print("-" * 50)
        else:
            # Unix/Linux系统使用lsof
            result = subprocess.run(
                ['lsof', '-i', f':{port}'], 
                capture_output=True, 
                text=True, 
                timeout=3
            )
            
            if result.returncode == 0 and result.stdout.strip():
                print(f"\n📊 端口 {port} 使用情况:")
                print("-" * 50)
                lines = result.stdout.strip().split('\n')
                for line in lines[1:]:  # 跳过标题行
                    parts = line.split()
                    if len(parts) >= 2:
                        print(f"进程: {parts[0]} (PID: {parts[1]})")
                print("-" * 50)
            else:
                print(f"\n📊 端口 {port} 当前未被使用")
    except:
        print(f"\n⚠️  无法检查端口 {port} 的使用情况")

def main():
    """主运行函数"""
    print("🚀 启动业务分析报告系统Web服务...")
    
    default_port = 8000
    host = "0.0.0.0"
    
    # 检查默认端口是否可用
    if check_port_available("127.0.0.1", default_port):
        port = default_port
        print(f"✅ 端口 {port} 可用")
    else:
        print(f"⚠️  端口 {default_port} 已被占用")
        show_port_status(default_port)
        
        # 检查是否在交互模式下运行
        is_interactive = hasattr(sys, 'ps1') or sys.stdin.isatty()
        
        if is_interactive:
            # 交互模式：询问用户是否要终止占用进程
            try:
                choice = input(f"\n是否尝试终止占用端口{default_port}的进程? (y/n): ").lower().strip()
                if choice in ['y', 'yes', '是']:
                    if kill_process_on_port(default_port):
                        import time
                        time.sleep(2)  # 等待进程完全终止
                        if check_port_available("127.0.0.1", default_port):
                            port = default_port
                            print(f"✅ 端口 {default_port} 现在可用")
                        else:
                            print(f"⚠️  端口 {default_port} 仍被占用，查找其他可用端口...")
                            port = find_available_port(default_port + 1)
                    else:
                        print("❌ 无法终止占用进程，查找其他可用端口...")
                        port = find_available_port(default_port + 1)
                else:
                    print("🔍 查找其他可用端口...")
                    port = find_available_port(default_port + 1)
            except KeyboardInterrupt:
                print("\n❌ 用户取消操作")
                return
            except EOFError:
                print("\n🔍 非交互模式，自动查找其他可用端口...")
                port = find_available_port(default_port + 1)
        else:
            # 非交互模式：自动处理
            print("🔍 自动查找其他可用端口...")
            port = find_available_port(default_port + 1)
    
    if port is None:
        print("❌ 无法找到可用端口 (8000-8009)")
        print("💡 建议:")
        print("   1. 手动终止占用端口的进程")
        print("   2. 检查防火墙设置")
        print("   3. 重启系统")
        return
    
    # 显示访问信息
    print(f"📊 访问地址: http://localhost:{port}")
    print(f"📝 API文档: http://localhost:{port}/docs")
    print("🔑 默认用户: admin / adminpass")
    
    if port != default_port:
        print(f"ℹ️  注意: 使用端口 {port} (默认端口 {default_port} 不可用)")
    
    print("\n" + "="*60)
    print("🎉 系统功能:")
    print("   📋 报告管理 - 查看和下载分析报告")
    print("   📊 在线预览 - 浏览器中查看报告内容")
    print("   📄 PDF下载 - 生成专业PDF格式报告")
    print("   🎛️ 系统仪表盘 - 实时监控系统状态")
    print("   👥 用户管理 - 用户权限管理")
    print("="*60)
    
    try:
        uvicorn.run(app, host=host, port=port, log_level="info")
    except KeyboardInterrupt:
        print("\n🛑 用户手动停止服务")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"\n❌ 端口 {port} 仍被占用")
            print("💡 解决方案:")
            print(f"   1. 手动终止进程: lsof -ti :{port} | xargs kill")
            print(f"   2. 或使用其他端口: python {sys.argv[0]} --port {port+1}")
        else:
            print(f"\n❌ 网络错误: {e}")
    except Exception as e:
        print(f"\n❌ Web服务启动失败: {e}")
        print("💡 故障排除:")
        print("   1. 检查是否有权限绑定端口")
        print("   2. 确认防火墙设置")
        print("   3. 检查系统资源使用情况")

# 新增：获取系统设置API
@app.get("/api/settings/{user_id}", response_model=SystemSettings)
async def get_settings(user_id: str, current_user: dict = Depends(get_current_user)):
    """获取用户系统设置"""
    if user_id not in system_settings_db:
        system_settings_db[user_id] = SystemSettings()
    return system_settings_db[user_id]

# 新增：更新系统设置API
@app.put("/api/settings/{user_id}", response_model=SystemSettings)
async def update_settings(
    user_id: str, 
    settings: SystemSettings,
    current_user: dict = Depends(get_current_user)
):
    """更新用户系统设置"""
    if current_user["username"] != user_id and current_user["username"] != "admin":
        raise HTTPException(status_code=403, detail="没有权限修改其他用户设置")
    
    system_settings_db[user_id] = settings
    return settings

# 新增：重置系统设置API
@app.post("/api/settings/{user_id}/reset", response_model=SystemSettings)
async def reset_settings(
    user_id: str,
    current_user: dict = Depends(get_current_user)
):
    """重置用户系统设置为默认值"""
    if current_user["username"] != user_id and current_user["username"] != "admin":
        raise HTTPException(status_code=403, detail="没有权限重置其他用户设置")
    
    system_settings_db[user_id] = SystemSettings()
    return system_settings_db[user_id]

# 新增：获取所有用户设置（管理员功能）
@app.get("/api/settings", response_model=Dict[str, SystemSettings])
async def get_all_settings(current_user: dict = Depends(get_current_user)):
    """获取所有用户的系统设置（需要管理员权限）"""
    if current_user["username"] != "admin":
        raise HTTPException(status_code=403, detail="需要管理员权限")
    
    return system_settings_db

# 在路由定义后添加分析API接口

@app.post("/api/analysis/data-profile")
async def analyze_data_profile(request: Request):
    """数据剖析API"""
    try:
        body = await request.json()
        
        if analytics_engine:
            # 这里应该处理实际数据，现在使用模拟数据
            result = analytics_engine.comprehensive_data_profile(
                data=body.get('data', {}),
                target_column=body.get('target_column')
            )
        else:
            # 简化版本
            result = {
                'basic_info': {'rows': 1000, 'columns': 10},
                'data_quality': {'overall_score': 0.85},
                'recommendations': ['数据质量良好', '可以进行进一步分析']
            }
        
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(
            content={'error': f"数据剖析失败: {str(e)}"}, 
            status_code=500
        )

@app.post("/api/analysis/customer-segmentation")
async def analyze_customer_segmentation(request: Request):
    """客户细分分析API"""
    try:
        body = await request.json()
        features = body.get('features', ['revenue', 'frequency', 'recency'])
        method = body.get('method', 'kmeans')
        
        if analytics_engine:
            result = analytics_engine.advanced_customer_segmentation(
                data=body.get('data', {}),
                features=features,
                method=method
            )
        else:
            # 简化版本
            result = {
                'segments': {'total_segments': 4, 'method_used': method},
                'segment_profiles': {
                    'high_value': {'size': 250, 'percentage': 25},
                    'medium_value': {'size': 500, 'percentage': 50},
                    'low_value': {'size': 200, 'percentage': 20},
                    'new_customers': {'size': 50, 'percentage': 5}
                },
                'recommendations': [
                    '高价值客户群体表现优异',
                    '中等价值客户有提升潜力',
                    '新客户需要特别关注'
                ]
            }
        
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(
            content={'error': f"客户细分分析失败: {str(e)}"}, 
            status_code=500
        )

@app.post("/api/analysis/predictive-modeling")
async def analyze_predictive_modeling(request: Request):
    """预测建模API"""
    try:
        body = await request.json()
        target_column = body.get('target_column', 'target')
        model_type = body.get('model_type', 'auto')
        
        if analytics_engine:
            result = analytics_engine.predictive_modeling(
                data=body.get('data', {}),
                target_column=target_column,
                model_type=model_type
            )
        else:
            # 简化版本
            result = {
                'model_type': model_type,
                'performance_metrics': {
                    'accuracy': 0.82,
                    'precision': 0.80,
                    'recall': 0.79
                },
                'feature_importance': {
                    'feature_1': 0.25,
                    'feature_2': 0.20,
                    'feature_3': 0.15
                },
                'model_insights': [
                    '模型性能良好，准确率达到82%',
                    '特征1对预测最重要'
                ]
            }
        
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(
            content={'error': f"预测建模失败: {str(e)}"}, 
            status_code=500
        )

@app.post("/api/analysis/ab-test")
async def analyze_ab_test(request: Request):
    """A/B测试分析API"""
    try:
        body = await request.json()
        control_data = body.get('control_data', [])
        treatment_data = body.get('treatment_data', [])
        metric = body.get('metric', 'conversion_rate')
        confidence_level = body.get('confidence_level', 0.95)
        
        if analytics_engine:
            result = analytics_engine.ab_test_analysis(
                control_data=control_data,
                treatment_data=treatment_data,
                metric=metric,
                confidence_level=confidence_level
            )
        else:
            # 简化版本
            result = {
                'test_summary': {
                    'control_size': len(control_data),
                    'treatment_size': len(treatment_data),
                    'control_mean': 2.5,
                    'treatment_mean': 2.8,
                    'relative_difference': 12.0
                },
                'statistical_significance': {
                    'p_value': 0.032,
                    'is_significant': True,
                    'confidence_level': confidence_level
                },
                'recommendations': [
                    '测试结果具有统计显著性',
                    '处理组表现更好，建议推广'
                ]
            }
        
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(
            content={'error': f"A/B测试分析失败: {str(e)}"}, 
            status_code=500
        )

@app.post("/api/analysis/time-series-forecast")
async def analyze_time_series_forecast(request: Request):
    """时间序列预测API"""
    try:
        body = await request.json()
        date_column = body.get('date_column', 'date')
        value_column = body.get('value_column', 'value')
        periods = body.get('periods', 12)
        
        if analytics_engine:
            result = analytics_engine.time_series_forecasting(
                data=body.get('data', {}),
                date_column=date_column,
                value_column=value_column,
                periods=periods
            )
        else:
            # 简化版本
            result = {
                'forecast_values': [
                    {'period': i+1, 'value': 850000 + i*20000} 
                    for i in range(periods)
                ],
                'trend_analysis': {
                    'direction': 'increasing',
                    'strength': 0.15
                },
                'insights': [
                    '预测显示持续增长趋势',
                    '建议准备应对需求增长'
                ]
            }
        
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(
            content={'error': f"时间序列预测失败: {str(e)}"}, 
            status_code=500
        )

@app.get("/api/analysis/tools")
async def get_analysis_tools():
    """获取可用分析工具列表"""
    tools = [
        {
            'id': 'data_profile',
            'name': '数据剖析',
            'description': '全面分析数据质量、分布和特征',
            'category': 'data_quality',
            'available': PROFESSIONAL_ANALYTICS_AVAILABLE
        },
        {
            'id': 'customer_segmentation',
            'name': '客户细分',
            'description': '使用机器学习进行高级客户细分',
            'category': 'customer_analysis',
            'available': PROFESSIONAL_ANALYTICS_AVAILABLE
        },
        {
            'id': 'predictive_modeling',
            'name': '预测建模',
            'description': '构建预测模型进行业务预测',
            'category': 'prediction',
            'available': PROFESSIONAL_ANALYTICS_AVAILABLE
        },
        {
            'id': 'ab_test',
            'name': 'A/B测试分析',
            'description': '统计学A/B测试结果分析',
            'category': 'testing',
            'available': PROFESSIONAL_ANALYTICS_AVAILABLE
        },
        {
            'id': 'time_series_forecast',
            'name': '时间序列预测',
            'description': '基于历史数据进行时间序列预测',
            'category': 'forecasting',
            'available': PROFESSIONAL_ANALYTICS_AVAILABLE
        },
        {
            'id': 'correlation_analysis',
            'name': '相关性分析',
            'description': '分析变量之间的相关关系',
            'category': 'statistical',
            'available': True
        },
        {
            'id': 'outlier_detection',
            'name': '异常检测',
            'description': '检测数据中的异常值和模式',
            'category': 'data_quality',
            'available': True
        }
    ]
    
    return JSONResponse(content={'tools': tools, 'total': len(tools)})

@app.post("/api/analysis/upload-data")
async def upload_data_for_analysis(request: Request):
    """上传数据进行分析"""
    try:
        # 这里应该处理文件上传，现在返回模拟结果
        return JSONResponse(content={
            'status': 'success',
            'message': '数据上传成功',
            'data_info': {
                'rows': 1000,
                'columns': 10,
                'file_size': '2.5MB',
                'data_types': {
                    'numeric': 7,
                    'categorical': 3
                }
            },
            'next_steps': [
                '选择分析类型',
                '配置分析参数',
                '开始分析'
            ]
        })
    except Exception as e:
        return JSONResponse(
            content={'error': f"数据上传失败: {str(e)}"}, 
            status_code=500
        )

# 新增：数据导入API
@app.post("/api/data/import", response_model=DataImportStatus)
async def import_data(
    request: DataImportRequest,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
):
    """导入数据"""
    import uuid
    
    import_id = str(uuid.uuid4())
    status = DataImportStatus(
        import_id=import_id,
        status="pending",
        created_at=datetime.now()
    )
    
    data_import_status_db[import_id] = status
    
    # 异步处理数据导入，支持WebSocket进度推送
    asyncio.create_task(process_data_import(
        import_id,
        request,
        current_user["username"]
    ))
    
    status.status = "processing"
    return status

# 数据导入处理函数
async def process_data_import(import_id: str, request: DataImportRequest, user_id: Optional[str] = None):
    """处理数据导入（支持WebSocket进度推送）"""
    status = data_import_status_db[import_id]
    
    # 发送开始处理通知
    if user_id:
        await manager.send_json_to_user({
            "type": "data_import_progress",
            "import_id": import_id,
            "status": "processing",
            "message": f"开始处理数据导入任务 ({request.source_type})",
            "progress": 0,
            "total": 100
        }, user_id)
    
    try:
        # 模拟数据导入过程
        if request.source_type == "csv":
            # 读取CSV文件
            try:
                import pandas as pd
                PANDAS_AVAILABLE = True
            except ImportError:
                PANDAS_AVAILABLE = False
            
            if PANDAS_AVAILABLE and request.file_path and os.path.exists(request.file_path):
                # 发送读取文件进度
                if user_id:
                    await manager.send_json_to_user({
                        "type": "data_import_progress",
                        "import_id": import_id,
                        "status": "processing",
                        "message": "正在读取CSV文件...",
                        "progress": 25,
                        "total": 100
                    }, user_id)
                
                await asyncio.sleep(0.5)  # 模拟处理时间
                
                df = pd.read_csv(request.file_path)
                status.total_records = len(df)
                
                # 发送数据验证进度
                if user_id:
                    await manager.send_json_to_user({
                        "type": "data_import_progress",
                        "import_id": import_id,
                        "status": "processing",
                        "message": f"验证数据格式 (共{len(df)}行)...",
                        "progress": 50,
                        "total": 100
                    }, user_id)
                
                await asyncio.sleep(0.5)
                
                # 保存到相应的数据目录
                output_path = f"data/imported/{request.data_type}_{import_id}.csv"
                os.makedirs("data/imported", exist_ok=True)
                
                # 发送保存文件进度
                if user_id:
                    await manager.send_json_to_user({
                        "type": "data_import_progress",
                        "import_id": import_id,
                        "status": "processing",
                        "message": "保存处理后的数据...",
                        "progress": 75,
                        "total": 100
                    }, user_id)
                
                await asyncio.sleep(0.3)
                df.to_csv(output_path, index=False)
                status.imported_records = len(df)
            else:
                raise ValueError("pandas不可用或文件路径无效")
                
        elif request.source_type == "json":
            # 处理JSON导入
            if user_id:
                await manager.send_json_to_user({
                    "type": "data_import_progress",
                    "import_id": import_id,
                    "status": "processing",
                    "message": "处理JSON数据...",
                    "progress": 50,
                    "total": 100
                }, user_id)
            
            await asyncio.sleep(1)
            status.total_records = 100  # 模拟
            status.imported_records = 100
            
        elif request.source_type == "excel":
            # 处理Excel导入
            if user_id:
                await manager.send_json_to_user({
                    "type": "data_import_progress",
                    "import_id": import_id,
                    "status": "processing",
                    "message": "处理Excel文件...",
                    "progress": 50,
                    "total": 100
                }, user_id)
            
            await asyncio.sleep(1.5)
            status.total_records = 200  # 模拟
            status.imported_records = 200
            
        status.status = "completed"
        status.completed_at = datetime.now()
        
        # 发送完成通知
        if user_id:
            await manager.send_json_to_user({
                "type": "data_import_progress",
                "import_id": import_id,
                "status": "completed",
                "message": f"数据导入完成，共处理 {status.imported_records} 条记录",
                "progress": 100,
                "total": 100,
                "imported_records": status.imported_records,
                "total_records": status.total_records
            }, user_id)
        
    except Exception as e:
        status.status = "failed"
        status.errors.append(str(e))
        status.completed_at = datetime.now()
        
        # 发送失败通知
        if user_id:
            await manager.send_json_to_user({
                "type": "data_import_progress",
                "import_id": import_id,
                "status": "failed",
                "message": f"数据导入失败: {str(e)}",
                "error": str(e)
            }, user_id)

# 新增：获取数据导入状态API
@app.get("/api/data/import/{import_id}/status", response_model=DataImportStatus)
async def get_import_status(
    import_id: str,
    current_user: dict = Depends(get_current_user)
):
    """获取数据导入状态"""
    if import_id not in data_import_status_db:
        raise HTTPException(status_code=404, detail="导入任务不存在")
    
    return data_import_status_db[import_id]

# 新增：数据导出API
@app.post("/api/data/export")
async def export_data(
    request: DataExportRequest,
    current_user: dict = Depends(get_current_user)
):
    """导出数据"""
    try:
        export_filename = f"{request.data_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{request.format}"
        export_path = f"output/exports/{export_filename}"
        os.makedirs("output/exports", exist_ok=True)
        
        # 模拟数据导出
        if request.data_type == "report":
            # 导出报告数据
            data = {
                "reports": [
                    {"id": "1", "title": "月度分析报告", "date": "2024-05"},
                    {"id": "2", "title": "季度总结报告", "date": "2024-Q2"}
                ]
            }
        elif request.data_type == "analysis":
            # 导出分析数据
            data = {
                "analysis_results": [
                    {"type": "trend", "value": 0.85},
                    {"type": "forecast", "value": 1000000}
                ]
            }
        else:
            # 导出原始数据
            data = {
                "raw_data": [
                    {"date": "2024-05-01", "sales": 10000},
                    {"date": "2024-05-02", "sales": 12000}
                ]
            }
        
        # 根据格式保存文件
        if request.format == "json":
            import json
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        elif request.format == "csv":
            import pandas as pd
            df = pd.DataFrame(data[list(data.keys())[0]])
            df.to_csv(export_path, index=False)
        
        # 返回文件下载
        return FileResponse(
            export_path,
            media_type=f'application/{request.format}',
            filename=export_filename
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"数据导出失败: {str(e)}")

# 新增：获取导入历史API
@app.get("/api/data/import/history")
async def get_import_history(
    limit: int = 10,
    current_user: dict = Depends(get_current_user)
):
    """获取数据导入历史"""
    # 按时间倒序排序，返回最近的导入记录
    import_list = sorted(
        data_import_status_db.values(),
        key=lambda x: x.created_at,
        reverse=True
    )[:limit]
    
    return {
        "total": len(data_import_status_db),
        "imports": import_list
    }

# 新增：数据上传API（用于Web界面上传文件）
@app.post("/api/data/upload")
async def upload_data_file(
    file: UploadFile = File(...),
    data_type: str = Form(...),
    current_user: dict = Depends(get_current_user)
):
    """上传数据文件"""
    try:
        # 检查文件类型
        allowed_extensions = ['.csv', '.json', '.xlsx', '.xls']
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"不支持的文件类型。支持的类型: {', '.join(allowed_extensions)}"
            )
        
        # 保存上传的文件
        upload_dir = "data/uploads"
        os.makedirs(upload_dir, exist_ok=True)
        
        file_path = os.path.join(upload_dir, f"{data_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}")
        
        # 发送文件上传开始通知
        await manager.send_json_to_user({
            "type": "file_upload_progress",
            "filename": file.filename,
            "status": "uploading",
            "message": f"正在上传文件 {file.filename}...",
            "progress": 0,
            "total": 100
        }, current_user["username"])
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # 发送文件上传完成通知
        await manager.send_json_to_user({
            "type": "file_upload_progress",
            "filename": file.filename,
            "status": "uploaded",
            "message": f"文件上传完成，正在创建导入任务...",
            "progress": 50,
            "total": 100
        }, current_user["username"])
        
        # 触发数据导入
        import_request = DataImportRequest(
            source_type=file_ext[1:],  # 去掉点号
            file_path=file_path,
            data_type=data_type,
            overwrite=False
        )
        
        # 创建导入任务
        import uuid
        import_id = str(uuid.uuid4())
        status = DataImportStatus(
            import_id=import_id,
            status="processing",
            created_at=datetime.now()
        )
        data_import_status_db[import_id] = status
        
        # 发送导入任务创建通知
        await manager.send_json_to_user({
            "type": "file_upload_progress",
            "filename": file.filename,
            "status": "processing",
            "message": f"导入任务已创建，任务ID: {import_id}",
            "progress": 100,
            "total": 100,
            "import_id": import_id
        }, current_user["username"])
        
        # 异步处理导入
        asyncio.create_task(process_data_import(import_id, import_request, current_user["username"]))
        
        return {
            "message": "文件上传成功",
            "import_id": import_id,
            "file_path": file_path
        }
        
    except Exception as e:
        # 发送失败通知
        await manager.send_json_to_user({
            "type": "file_upload_progress",
            "filename": file.filename if file else "unknown",
            "status": "failed",
            "message": f"文件上传失败: {str(e)}",
            "error": str(e)
        }, current_user["username"])
        
        raise HTTPException(status_code=500, detail=f"文件上传失败: {str(e)}")

# 新增：获取报告模板列表API
@app.get("/api/templates")
async def get_report_templates(
    template_type: Optional[str] = None,
    is_active: bool = True,
    current_user: dict = Depends(get_current_user)
):
    """获取报告模板列表"""
    templates = list(report_templates_db.values())
    
    # 过滤条件
    if template_type:
        templates = [t for t in templates if t.template_type == template_type]
    if is_active is not None:
        templates = [t for t in templates if t.is_active == is_active]
    
    return {
        "total": len(templates),
        "templates": templates
    }

# 新增：获取单个模板详情API
@app.get("/api/templates/{template_id}", response_model=ReportTemplate)
async def get_template_detail(
    template_id: str,
    current_user: dict = Depends(get_current_user)
):
    """获取报告模板详情"""
    if template_id not in report_templates_db:
        raise HTTPException(status_code=404, detail="模板不存在")
    
    return report_templates_db[template_id]

# 新增：创建报告模板API
@app.post("/api/templates", response_model=ReportTemplate)
async def create_report_template(
    request: CreateTemplateRequest,
    current_user: dict = Depends(get_current_user)
):
    """创建新的报告模板"""
    import uuid
    
    template_id = str(uuid.uuid4())
    template = ReportTemplate(
        template_id=template_id,
        name=request.name,
        description=request.description,
        template_type=request.template_type,
        sections=request.sections,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        created_by=current_user["username"],
        is_active=True,
        settings=request.settings
    )
    
    report_templates_db[template_id] = template
    return template

# 新增：更新报告模板API
@app.put("/api/templates/{template_id}", response_model=ReportTemplate)
async def update_report_template(
    template_id: str,
    request: CreateTemplateRequest,
    current_user: dict = Depends(get_current_user)
):
    """更新报告模板"""
    if template_id not in report_templates_db:
        raise HTTPException(status_code=404, detail="模板不存在")
    
    template = report_templates_db[template_id]
    
    # 检查权限
    if template.created_by != current_user["username"] and current_user["username"] != "admin":
        raise HTTPException(status_code=403, detail="没有权限修改此模板")
    
    # 更新模板
    template.name = request.name
    template.description = request.description
    template.template_type = request.template_type
    template.sections = request.sections
    template.settings = request.settings
    template.updated_at = datetime.now()
    
    return template

# 新增：删除报告模板API
@app.delete("/api/templates/{template_id}")
async def delete_report_template(
    template_id: str,
    current_user: dict = Depends(get_current_user)
):
    """删除报告模板（软删除）"""
    if template_id not in report_templates_db:
        raise HTTPException(status_code=404, detail="模板不存在")
    
    template = report_templates_db[template_id]
    
    # 检查权限
    if template.created_by != current_user["username"] and current_user["username"] != "admin":
        raise HTTPException(status_code=403, detail="没有权限删除此模板")
    
    # 软删除
    template.is_active = False
    template.updated_at = datetime.now()
    
    return {"message": "模板已删除"}

# 新增：复制报告模板API
@app.post("/api/templates/{template_id}/copy", response_model=ReportTemplate)
async def copy_report_template(
    template_id: str,
    new_name: str,
    current_user: dict = Depends(get_current_user)
):
    """复制报告模板"""
    if template_id not in report_templates_db:
        raise HTTPException(status_code=404, detail="模板不存在")
    
    import uuid
    
    source_template = report_templates_db[template_id]
    new_template_id = str(uuid.uuid4())
    
    new_template = ReportTemplate(
        template_id=new_template_id,
        name=new_name,
        description=f"{source_template.description} (复制)",
        template_type=source_template.template_type,
        sections=source_template.sections.copy(),
        created_at=datetime.now(),
        updated_at=datetime.now(),
        created_by=current_user["username"],
        is_active=True,
        settings=source_template.settings.copy()
    )
    
    report_templates_db[new_template_id] = new_template
    return new_template

# 新增：应用模板生成报告API
@app.post("/api/templates/{template_id}/generate-report")
async def generate_report_from_template(
    template_id: str,
    data_source: dict,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
):
    """使用模板生成报告"""
    if template_id not in report_templates_db:
        raise HTTPException(status_code=404, detail="模板不存在")
    
    template = report_templates_db[template_id]
    
    # 创建报告生成任务
    import uuid
    task_id = str(uuid.uuid4())
    
    # 异步生成报告
    background_tasks.add_task(
        generate_report_with_template,
        task_id,
        template,
        data_source
    )
    
    return {
        "message": "报告生成任务已创建",
        "task_id": task_id,
        "template_name": template.name
    }

# 报告生成处理函数
def generate_report_with_template(task_id: str, template: ReportTemplate, data_source: dict):
    """使用模板生成报告"""
    try:
        # 模拟报告生成过程
        print(f"开始使用模板 {template.name} 生成报告...")
        
        # 根据模板的sections生成对应内容
        report_content = {
            "title": f"{template.name} - {datetime.now().strftime('%Y-%m-%d')}",
            "sections": {}
        }
        
        for section in template.sections:
            report_content["sections"][section] = f"{section}内容（基于模板生成）"
        
        # 保存报告
        output_path = f"output/reports/template_report_{task_id}.json"
        os.makedirs("output/reports", exist_ok=True)
        
        import json
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report_content, f, ensure_ascii=False, indent=2)
        
        print(f"报告生成完成: {output_path}")
        
    except Exception as e:
        print(f"报告生成失败: {str(e)}")

# WebSocket连接管理器
class ConnectionManager:
    """WebSocket连接管理器"""
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
        self.user_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str):
        """接受WebSocket连接"""
        await websocket.accept()
        if client_id not in self.active_connections:
            self.active_connections[client_id] = []
        self.active_connections[client_id].append(websocket)
        self.user_connections[client_id] = websocket
        print(f"✅ WebSocket连接建立: {client_id}")
    
    def disconnect(self, websocket: WebSocket, client_id: str):
        """断开WebSocket连接"""
        if client_id in self.active_connections:
            self.active_connections[client_id].remove(websocket)
            if not self.active_connections[client_id]:
                del self.active_connections[client_id]
        if client_id in self.user_connections and self.user_connections[client_id] == websocket:
            del self.user_connections[client_id]
        print(f"❌ WebSocket连接断开: {client_id}")
    
    async def send_personal_message(self, message: str, client_id: str):
        """发送个人消息"""
        if client_id in self.user_connections:
            await self.user_connections[client_id].send_text(message)
    
    async def send_json_to_user(self, data: dict, client_id: str):
        """发送JSON数据给特定用户"""
        if client_id in self.user_connections:
            await self.user_connections[client_id].send_json(data)
    
    async def broadcast(self, message: str, exclude_client: Optional[str] = None):
        """广播消息给所有连接的客户端"""
        for client_id, connections in self.active_connections.items():
            if client_id != exclude_client:
                for connection in connections:
                    await connection.send_text(message)
    
    async def broadcast_json(self, data: dict, exclude_client: Optional[str] = None):
        """广播JSON数据给所有连接的客户端"""
        for client_id, connections in self.active_connections.items():
            if client_id != exclude_client:
                for connection in connections:
                    await connection.send_json(data)

# 创建WebSocket管理器实例
manager = ConnectionManager()

# 新增WebSocket测试页面
@app.get("/websocket-test", response_class=HTMLResponse)
async def websocket_test_page(request: Request):
    """WebSocket测试页面"""
    return templates.TemplateResponse("websocket_test.html", {"request": request})

@app.post("/api/reports/multi-industry/generate")
async def generate_multi_industry_reports(
    background_tasks: BackgroundTasks,
    industries: List[str] = ["retail", "community", "financial", "ai_agent", "cross_industry"],
    current_user: dict = Depends(get_current_user)
):
    """生成多行业分析报告"""
    try:
        # 导入多行业报告生成器
        from src.reports.multi_industry_report_generator import MultiIndustryReportGenerator
        
        # 创建生成器实例
        generator = MultiIndustryReportGenerator()
        
        # 在后台任务中生成报告
        background_tasks.add_task(generate_multi_industry_reports_task, generator, industries, current_user.get("username", "unknown"))
        
        return {
            "success": True,
            "message": "多行业报告生成任务已启动",
            "task_id": f"multi_industry_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "industries": industries,
            "estimated_time": "2-3分钟"
        }
        
    except Exception as e:
        print(f"生成多行业报告失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"生成报告失败: {str(e)}")

async def generate_multi_industry_reports_task(generator, industries, user_id):
    """后台任务：生成多行业报告"""
    try:
        # 发送开始通知
        await manager.send_json_to_user({
            "type": "multi_industry_progress",
            "status": "started",
            "message": "开始生成多行业分析报告...",
            "progress": 0,
            "total": len(industries)
        }, user_id)
        
        # 执行报告生成
        generated_reports = generator.generate_all_industry_reports()
        
        # 更新报告列表
        global reports_data
        reports_data = get_actual_reports()
        
        # 发送完成通知
        await manager.send_json_to_user({
            "type": "multi_industry_progress",
            "status": "completed",
            "message": f"成功生成 {len(generated_reports)} 个行业分析报告",
            "progress": len(industries),
            "total": len(industries),
            "reports": [os.path.basename(report) for report in generated_reports]
        }, user_id)
        
    except Exception as e:
        # 发送错误通知
        await manager.send_json_to_user({
            "type": "multi_industry_progress",
            "status": "error",
            "message": f"生成报告失败: {str(e)}",
            "error": str(e)
        }, user_id)

if __name__ == "__main__":
    main() 