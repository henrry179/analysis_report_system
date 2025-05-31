#!/usr/bin/env python3
"""
重构后的主应用文件
整合所有模块，提供干净的启动点
"""

import asyncio
import sys
from pathlib import Path
from contextlib import asynccontextmanager

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
import uvicorn

# 导入配置和工具
from src.config.settings import settings
from src.utils.logger import (
    system_logger, 
    log_startup_info, 
    log_shutdown_info,
    performance_logger
)
from src.utils.exceptions import BaseSystemException

# 导入核心模块
from src.core.auth import login_user, init_default_users
from src.core.websocket import websocket_endpoint, start_websocket_maintenance, manager
from src.core.models import LoginRequest

# 导入API路由
from src.api.reports import router as reports_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时执行
    system_logger.info("🚀 应用启动中...")
    
    try:
        # 验证配置
        settings.validate_settings()
        system_logger.info("✅ 配置验证通过")
        
        # 初始化默认用户
        init_default_users()
        
        # 启动WebSocket维护任务
        await start_websocket_maintenance()
        
        # 记录启动信息
        log_startup_info()
        
        system_logger.info("🎉 应用启动完成")
        
        yield  # 应用运行期间
        
    except Exception as e:
        system_logger.error("应用启动失败", error=e)
        raise
    finally:
        # 关闭时执行
        system_logger.info("🛑 应用正在关闭...")
        log_shutdown_info()


# 创建FastAPI应用
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url=None,
    openapi_url="/openapi.json" if settings.DEBUG else None,
    lifespan=lifespan
)

# 添加中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

# 挂载静态文件
app.mount("/static", StaticFiles(directory=str(settings.STATIC_DIR)), name="static")

# 设置模板
templates = Jinja2Templates(directory=str(settings.TEMPLATES_DIR))

# 注册API路由
app.include_router(reports_router)


# 异常处理器
@app.exception_handler(BaseSystemException)
async def system_exception_handler(request: Request, exc: BaseSystemException):
    """系统异常处理器"""
    system_logger.error("系统异常", error=exc, path=request.url.path)
    return JSONResponse(
        status_code=500,
        content=exc.to_dict()
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """HTTP异常处理器"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error_code": exc.status_code,
            "message": exc.detail,
            "path": str(request.url.path)
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """通用异常处理器"""
    system_logger.error("未处理的异常", error=exc, path=request.url.path)
    return JSONResponse(
        status_code=500,
        content={
            "error_code": 500,
            "message": "内部服务器错误",
            "detail": str(exc) if settings.DEBUG else "服务器内部错误"
        }
    )


# 中间件：请求日志
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """请求日志中间件"""
    import time
    
    start_time = time.time()
    
    # 处理请求
    response = await call_next(request)
    
    # 计算耗时
    process_time = time.time() - start_time
    
    # 记录性能日志
    performance_logger.log_request(
        method=request.method,
        path=str(request.url.path),
        duration=process_time,
        status_code=response.status_code
    )
    
    # 添加响应头
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-API-Version"] = settings.APP_VERSION
    
    return response


# WebSocket端点
@app.websocket("/ws/{client_id}")
async def websocket_route(websocket, client_id: str):
    """WebSocket路由"""
    await websocket_endpoint(websocket, client_id)


# 页面路由
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """首页"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "app_name": settings.APP_NAME,
        "app_version": settings.APP_VERSION
    })


@app.get("/reports", response_class=HTMLResponse)
async def reports_page(request: Request):
    """报告管理页面"""
    # 这里应该从数据层获取报告列表
    reports = []  # 暂时为空
    return templates.TemplateResponse("reports.html", {
        "request": request,
        "reports": reports,
        "total_reports": len(reports)
    })


@app.get("/reports/{report_id}", response_class=HTMLResponse)
async def report_detail_page(request: Request, report_id: int):
    """报告详情页面"""
    # 这里应该从数据层获取报告详情
    report = {"id": report_id, "title": f"报告 {report_id}", "status": "已完成"}
    return templates.TemplateResponse("report_detail.html", {
        "request": request,
        "report": report
    })


@app.get("/analysis", response_class=HTMLResponse)
async def analysis_page(request: Request):
    """分析中心页面"""
    return templates.TemplateResponse("analysis.html", {
        "request": request
    })


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    """仪表盘页面"""
    return templates.TemplateResponse("dashboard.html", {
        "request": request
    })


@app.get("/settings", response_class=HTMLResponse)
async def settings_page(request: Request):
    """设置页面"""
    return templates.TemplateResponse("settings.html", {
        "request": request
    })


@app.get("/users", response_class=HTMLResponse)
async def users_page(request: Request):
    """用户管理页面"""
    return templates.TemplateResponse("user_management.html", {
        "request": request
    })


@app.get("/test", response_class=HTMLResponse)
async def test_page(request: Request):
    """测试页面"""
    return templates.TemplateResponse("test_report_generation.html", {
        "request": request
    })


@app.get("/status", response_class=HTMLResponse)
async def status_page(request: Request):
    """系统状态页面"""
    status_html = """
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>系统状态 - 业务分析报告系统 v4.0</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .status-card { margin-bottom: 1rem; }
        .endpoint-list { background: #f8f9fa; border-radius: 8px; padding: 1rem; }
        .endpoint-item { margin-bottom: 0.5rem; }
        .method-get { color: #28a745; font-weight: bold; }
        .method-post { color: #007bff; font-weight: bold; }
        .live-status { animation: pulse 2s infinite; }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
    </style>
</head>
<body>
    <div class="container mt-4">
        <div class="row">
            <div class="col-12">
                <div class="alert alert-success">
                    <h2 class="alert-heading">🚀 业务分析报告系统 v4.0 Optimized</h2>
                    <p class="mb-0">
                        <span class="badge bg-success live-status">● 运行中</span>
                        服务器正常运行在 <strong>localhost:8000</strong>
                    </p>
                </div>
            </div>
        </div>
        
        <div class="row">
            <div class="col-md-6">
                <div class="card status-card">
                    <div class="card-header bg-primary text-white">
                        <h5 class="mb-0">📄 页面端点</h5>
                    </div>
                    <div class="card-body endpoint-list">
                        <div class="endpoint-item">
                            <span class="method-get">GET</span> 
                            <a href="/" target="_blank">/</a> - 主页
                        </div>
                        <div class="endpoint-item">
                            <span class="method-get">GET</span> 
                            <a href="/test" target="_blank">/test</a> - 报告生成测试页面
                        </div>
                        <div class="endpoint-item">
                            <span class="method-get">GET</span> 
                            <a href="/reports" target="_blank">/reports</a> - 报告管理
                        </div>
                        <div class="endpoint-item">
                            <span class="method-get">GET</span> 
                            <a href="/dashboard" target="_blank">/dashboard</a> - 仪表盘
                        </div>
                        <div class="endpoint-item">
                            <span class="method-get">GET</span> 
                            <a href="/analysis" target="_blank">/analysis</a> - 分析中心
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="col-md-6">
                <div class="card status-card">
                    <div class="card-header bg-success text-white">
                        <h5 class="mb-0">🔌 API端点</h5>
                    </div>
                    <div class="card-body endpoint-list">
                        <div class="endpoint-item">
                            <span class="method-get">GET</span> 
                            <a href="/health" target="_blank">/health</a> - 健康检查
                        </div>
                        <div class="endpoint-item">
                            <span class="method-get">GET</span> 
                            <a href="/api/info" target="_blank">/api/info</a> - 系统信息
                        </div>
                        <div class="endpoint-item">
                            <span class="method-get">GET</span> 
                            <a href="/api/system/status" target="_blank">/api/system/status</a> - 系统状态
                        </div>
                        <div class="endpoint-item">
                            <span class="method-get">GET</span> 
                            <a href="/api/reports/industry-types" target="_blank">/api/reports/industry-types</a> - 行业类型
                        </div>
                        <div class="endpoint-item">
                            <span class="method-post">POST</span> 
                            /api/reports/multi-industry/generate - 生成多行业报告
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="row mt-4">
            <div class="col-12">
                <div class="card">
                    <div class="card-header bg-info text-white">
                        <h5 class="mb-0">⚡ 快速测试</h5>
                    </div>
                    <div class="card-body">
                        <p>点击下方按钮快速测试报告生成功能：</p>
                        <div class="text-center">
                            <a href="/test" class="btn btn-primary btn-lg">
                                🎯 测试报告生成
                            </a>
                            <button onclick="testAPI()" class="btn btn-success btn-lg ms-2">
                                🔧 测试API
                            </button>
                        </div>
                        <div id="apiResult" class="mt-3"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        async function testAPI() {
            const resultDiv = document.getElementById('apiResult');
            resultDiv.innerHTML = '<div class="alert alert-info">正在测试API...</div>';
            
            try {
                const response = await fetch('/api/reports/multi-industry/generate', {
                    method: 'POST',
                    headers: {
                        'Authorization': 'Bearer admin',
                        'Content-Type': 'application/json'
                    }
                });
                
                const data = await response.json();
                
                if (data.success) {
                    resultDiv.innerHTML = `
                        <div class="alert alert-success">
                            <h6>✅ API测试成功！</h6>
                            <p><strong>任务ID:</strong> ${data.task_id}</p>
                            <p><strong>包含行业:</strong> ${data.industries.join(', ')}</p>
                        </div>
                    `;
                } else {
                    throw new Error(data.message || 'API调用失败');
                }
            } catch (error) {
                resultDiv.innerHTML = `
                    <div class="alert alert-danger">
                        <h6>❌ API测试失败</h6>
                        <p>错误: ${error.message}</p>
                    </div>
                `;
            }
        }
        
        // 实时更新状态
        setInterval(async () => {
            try {
                const response = await fetch('/api/system/status');
                const data = await response.json();
                console.log('系统状态:', data);
            } catch (error) {
                console.log('状态检查失败:', error);
            }
        }, 30000); // 每30秒检查一次
    </script>
</body>
</html>
    """
    return HTMLResponse(content=status_html)


# 认证API
@app.post("/token")
async def login_endpoint(form_data: OAuth2PasswordRequestForm = Depends()):
    """用户登录"""
    try:
        result = await login_user(form_data)
        system_logger.info("用户登录", username=form_data.username)
        return result
    except Exception as e:
        system_logger.error("登录失败", error=e, username=form_data.username)
        raise HTTPException(status_code=400, detail="登录失败")


# 系统信息API
@app.get("/api/info")
async def get_system_info():
    """获取系统信息"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": settings.APP_DESCRIPTION,
        "status": "running",
        "debug": settings.DEBUG,
        "features": [
            "智能数据分析",
            "自动报告生成", 
            "多行业支持",
            "实时WebSocket通信",
            "用户权限管理",
            "批量报告处理"
        ]
    }


@app.get("/api/system/status")
async def get_system_status():
    """获取系统状态"""
    try:
        import psutil
        
        # 获取系统信息
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # 获取WebSocket统计
        ws_stats = manager.get_statistics()
        
        return {
            "status": "healthy",
            "uptime": "运行中",
            "version": settings.APP_VERSION,
            "cpu_usage": cpu_percent,
            "memory_usage": memory.percent,
            "disk_usage": (disk.used / disk.total) * 100,
            "active_connections": ws_stats["active_count"],
            "total_messages": ws_stats["messages_sent"] + ws_stats["messages_received"]
        }
    except Exception as e:
        system_logger.error("获取系统状态失败", error=e)
        return {
            "status": "error",
            "message": "无法获取系统状态",
            "version": settings.APP_VERSION
        }


@app.get("/api/websocket/stats")
async def get_websocket_stats():
    """获取WebSocket统计信息"""
    return manager.get_statistics()


# 健康检查端点
@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "timestamp": "2024-05-26T00:00:00Z",
        "version": settings.APP_VERSION,
        "service": "analysis_report_system"
    }


# 图表数据API（兼容性）
@app.get("/charts")
async def get_charts():
    """获取图表数据"""
    return {
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


def main():
    """主函数：启动应用"""
    try:
        # 验证配置
        settings.validate_settings()
        
        # 启动服务器
        uvicorn.run(
            "src.main:app",
            host=settings.HOST,
            port=settings.PORT,
            reload=settings.RELOAD,
            log_level=settings.LOG_LEVEL.lower(),
            access_log=settings.DEBUG,
            reload_dirs=["src"] if settings.RELOAD else None
        )
        
    except KeyboardInterrupt:
        system_logger.info("用户中断，正在关闭服务器...")
    except Exception as e:
        system_logger.error("服务器启动失败", error=e)
        sys.exit(1)


if __name__ == "__main__":
    main() 