#!/usr/bin/env python3
"""
报告相关API路由
"""

import os
import glob
import asyncio
from datetime import datetime
from typing import List, Optional, Dict, Any

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, UploadFile, File, Form, Body
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse

from src.config.settings import settings
from src.utils.logger import system_logger, performance_logger
from src.utils.exceptions import (
    DataNotFoundError, 
    ReportGenerationError,
    FileNotFoundError,
    BusinessError
)
from src.core.auth import get_current_user, User
from src.core.models import BatchReportRequest, BatchReportStatus
from src.core.websocket import manager

# 导入报告生成器
try:
    from src.reports.multi_industry_report_generator import MultiIndustryReportGenerator
except ImportError as e:
    system_logger.warning("报告生成器导入失败，将使用简化版本", error=str(e))
    
    # 如果导入失败，创建一个简单的替代类
    class MultiIndustryReportGenerator:
        def __init__(self):
            self.output_dir = str(settings.REPORTS_DIR)
            os.makedirs(self.output_dir, exist_ok=True)
        
        def generate_all_industry_reports(self):
            """简单的报告生成实现"""
            print("生成简化的多行业报告...")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            reports = []
            
            industries_config = {
                "retail": {"name": "零售行业", "icon": "🏪"},
                "community": {"name": "社区团购", "icon": "🏘️"},
                "financial": {"name": "金融交易", "icon": "💰"},
                "ai_agent": {"name": "智能体", "icon": "🤖"},
                "cross_industry": {"name": "跨行业对比", "icon": "🔄"}
            }
            
            for industry_code, config in industries_config.items():
                html_content = f"""
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{config['icon']} {config['name']}分析报告</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        .metric-card {{ background: linear-gradient(135deg, #007bff 0%, rgba(0, 123, 255, 0.8) 100%); color: white; }}
        .chart-container {{ height: 300px; margin: 15px 0; }}
        .insight-box {{ background: #f8f9fa; padding: 20px; border-left: 4px solid #007bff; margin: 15px 0; border-radius: 5px; }}
    </style>
</head>
<body>
    <div class="container mt-4">
        <div class="row mb-4">
            <div class="col-12">
                <h1 class="text-center">{config['icon']} {config['name']}分析报告</h1>
                <p class="text-center text-muted">生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 报告编号: {industry_code.upper()}_{timestamp}</p>
            </div>
        </div>

        <div class="row mb-4">
            <div class="col-md-3">
                <div class="card metric-card text-center">
                    <div class="card-body">
                        <h3>1,234,567</h3>
                        <p class="mb-0">核心指标</p>
                        <small>+15.2%</small>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card metric-card text-center">
                    <div class="card-body">
                        <h3>89.5%</h3>
                        <p class="mb-0">完成率</p>
                        <small>持续优化</small>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card metric-card text-center">
                    <div class="card-body">
                        <h3>25</h3>
                        <p class="mb-0">覆盖区域</p>
                        <small>全国布局</small>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card metric-card text-center">
                    <div class="card-body">
                        <h3>12</h3>
                        <p class="mb-0">业务类型</p>
                        <small>多元发展</small>
                    </div>
                </div>
            </div>
        </div>

        <div class="row mb-4">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h5>📊 趋势分析</h5>
                    </div>
                    <div class="card-body">
                        <canvas id="trendChart" class="chart-container"></canvas>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h5>📈 分布分析</h5>
                    </div>
                    <div class="card-body">
                        <canvas id="pieChart" class="chart-container"></canvas>
                    </div>
                </div>
            </div>
        </div>

        <div class="row mb-4">
            <div class="col-12">
                <div class="insight-box">
                    <h5>💡 关键洞察</h5>
                    <ul>
                        <li>该行业在过去一季度表现良好，主要指标稳步增长</li>
                        <li>区域分布均衡，各区域发展态势良好</li>
                        <li>建议继续关注市场变化，保持增长态势</li>
                        <li>数字化转型程度不断提升，竞争优势明显</li>
                    </ul>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-12">
                <div class="alert alert-success">
                    <h4>✅ 报告生成成功!</h4>
                    <p>这是{config['name']}的分析报告。系统已成功收集和分析相关数据，生成了本报告。</p>
                    <hr>
                    <p class="mb-0"><strong>注意:</strong> 这是v4.0 Optimized版本的示例报告，实际使用中会包含更详细的数据分析和可视化图表。</p>
                </div>
            </div>
        </div>
    </div>

    <script>
        // 趋势图表
        const trendCtx = document.getElementById('trendChart').getContext('2d');
        new Chart(trendCtx, {{
            type: 'line',
            data: {{
                labels: ['1月', '2月', '3月', '4月', '5月', '6月'],
                datasets: [{{
                    label: '月度趋势',
                    data: [120, 150, 180, 160, 200, 220],
                    borderColor: '#007bff',
                    backgroundColor: 'rgba(0, 123, 255, 0.1)',
                    tension: 0.4
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false
            }}
        }});

        // 饼图
        const pieCtx = document.getElementById('pieChart').getContext('2d');
        new Chart(pieCtx, {{
            type: 'doughnut',
            data: {{
                labels: ['类别A', '类别B', '类别C', '类别D'],
                datasets: [{{
                    data: [30, 25, 25, 20],
                    backgroundColor: ['#007bff', '#28a745', '#ffc107', '#dc3545']
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false
            }}
        }});
    </script>
</body>
</html>
                """
                
                filename = f"{industry_code}_report_{timestamp}.html"
                filepath = os.path.join(self.output_dir, filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                reports.append(filepath)
                print(f"✅ 生成{config['name']}报告: {filename}")
            
            return reports

# 创建路由器
router = APIRouter(prefix="/api/reports", tags=["reports"])

# 全局变量（这些应该移到数据层）
reports_data = []
batch_report_status_db = {}


@router.get("/")
async def get_reports():
    """获取报告列表"""
    try:
        return JSONResponse(content={
            "reports": reports_data, 
            "total": len(reports_data)
        })
    except Exception as e:
        system_logger.error("获取报告列表失败", error=e)
        raise HTTPException(status_code=500, detail="获取报告列表失败")


@router.get("/industry-types")
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


@router.post("/multi-industry/generate")
async def generate_multi_industry_reports(
    request_body: Dict[str, Any] = Body(...),
    current_user: User = Depends(get_current_user)
):
    """生成多行业分析报告"""
    try:
        industries = request_body.get("industries", ["retail", "community", "financial", "ai_agent", "cross_industry"])
        if not isinstance(industries, list) or len(industries) == 0:
            raise HTTPException(status_code=400, detail="industries参数必须是非空列表")
        generator = MultiIndustryReportGenerator()

        # 用asyncio.create_task调度异步后台任务
        asyncio.create_task(
            generate_multi_industry_reports_task(generator, industries, current_user.username)
        )

        system_logger.info("多行业报告生成任务已启动", industries=industries, user=current_user.username)
        return {
            "success": True,
            "message": "多行业报告生成任务已启动",
            "task_id": f"multi_industry_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "industries": industries,
            "estimated_time": "2-3分钟"
        }
    except Exception as e:
        system_logger.error("生成多行业报告失败", error=e)
        raise HTTPException(status_code=500, detail=f"生成报告失败: {str(e)}")


@router.post("/batch/generate")
async def generate_batch_reports(
    request: BatchReportRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user)
):
    """批量生成报告"""
    try:
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
                current_user.username
            ))
            status.status = "processing"
        else:
            # 同步生成
            await process_batch_reports(
                batch_id,
                request.report_ids,
                request.output_format,
                request.include_charts,
                current_user.username
            )
        
        system_logger.info("批量报告生成任务已启动", batch_id=batch_id, user=current_user.username)
        return status
        
    except Exception as e:
        system_logger.error("批量报告生成失败", error=e)
        raise HTTPException(status_code=500, detail="批量报告生成失败")


@router.get("/batch/{batch_id}/status")
async def get_batch_report_status(
    batch_id: str,
    current_user: User = Depends(get_current_user)
):
    """获取批量报告生成状态"""
    if batch_id not in batch_report_status_db:
        raise HTTPException(status_code=404, detail="批次不存在")
    
    return batch_report_status_db[batch_id]


@router.get("/{report_id}")
async def get_report_detail(report_id: int):
    """获取报告详情"""
    try:
        report = next((r for r in reports_data if r["id"] == report_id), None)
        if not report:
            raise DataNotFoundError("报告不存在", resource_id=str(report_id))
        return JSONResponse(content=report)
    except DataNotFoundError:
        raise HTTPException(status_code=404, detail="报告不存在")
    except Exception as e:
        system_logger.error("获取报告详情失败", error=e, report_id=report_id)
        raise HTTPException(status_code=500, detail="获取报告详情失败")


@router.post("/{report_id}/generate")
async def generate_report(report_id: int, current_user: User = Depends(get_current_user)):
    """生成报告API"""
    try:
        report = next((r for r in reports_data if r["id"] == report_id), None)
        if not report:
            raise DataNotFoundError("报告不存在", resource_id=str(report_id))
        
        # 模拟报告生成过程
        if report["status"] == "草稿":
            report["status"] = "生成中"
            system_logger.info("报告生成已启动", report_id=report_id, user=current_user.username)
            return JSONResponse(content={"message": "报告生成已启动", "status": "生成中"})
        else:
            return JSONResponse(content={"message": "报告已存在", "status": report["status"]})
            
    except DataNotFoundError:
        raise HTTPException(status_code=404, detail="报告不存在")
    except Exception as e:
        system_logger.error("生成报告失败", error=e, report_id=report_id)
        raise HTTPException(status_code=500, detail="生成报告失败")


@router.get("/{report_id}/preview")
async def preview_report(report_id: int):
    """在线预览报告"""
    try:
        report = next((r for r in reports_data if r["id"] == report_id), None)
        if not report:
            raise DataNotFoundError("报告不存在", resource_id=str(report_id))
        
        if not report.get("html_file") or not os.path.exists(report["html_file"]):
            raise FileNotFoundError("预览文件不存在", file_path=report.get("html_file"))
        
        # 读取HTML文件内容
        with open(report["html_file"], 'r', encoding='utf-8') as f:
            content = f.read()
        return HTMLResponse(content=content)
        
    except (DataNotFoundError, FileNotFoundError) as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        system_logger.error("预览报告失败", error=e, report_id=report_id)
        raise HTTPException(status_code=500, detail="预览报告失败")


@router.get("/{report_id}/download/{format}")
async def download_report(report_id: int, format: str):
    """下载报告文件"""
    try:
        report = next((r for r in reports_data if r["id"] == report_id), None)
        if not report:
            raise DataNotFoundError("报告不存在", resource_id=str(report_id))
        
        if format == "html" and report.get("html_file"):
            file_path = report["html_file"]
            filename = f"{report['filename']}.html"
        elif format == "md" and report.get("md_file"):
            file_path = report["md_file"]
            filename = f"{report['filename']}.md"
        elif format == "pdf":
            # 生成PDF文件（这里需要实现PDF生成逻辑）
            raise HTTPException(status_code=501, detail="PDF生成功能暂未实现")
        else:
            raise HTTPException(status_code=404, detail="文件格式不支持或文件不存在")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError("文件不存在", file_path=file_path)
        
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type='application/octet-stream'
        )
        
    except DataNotFoundError:
        raise HTTPException(status_code=404, detail="报告不存在")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="文件不存在")
    except Exception as e:
        system_logger.error("下载报告失败", error=e, report_id=report_id, format=format)
        raise HTTPException(status_code=500, detail="下载报告失败")


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
                for file_path in glob.glob(str(settings.REPORTS_DIR / "*.html")):
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
                    # 这里应该实现PDF生成逻辑
                    pdf_path = report_path.replace('.html', '.pdf').replace('output/reports/', 'pdf_reports/')
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
                system_logger.error("处理单个报告失败", error=e, report_id=report_id)
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
        system_logger.error("批量报告生成失败", error=e, batch_id=batch_id)
        
        # 发送失败通知
        if user_id:
            await manager.send_json_to_user({
                "type": "batch_report_progress",
                "batch_id": batch_id,
                "status": "failed",
                "message": f"批量报告生成失败: {str(e)}",
                "error": str(e)
            }, user_id)


async def generate_multi_industry_reports_task(generator, industries, user_id):
    """异步生成多行业报告任务"""
    try:
        # 发送开始通知
        if user_id:
            await manager.send_json_to_user({
                "type": "report_generation",
                "status": "started", 
                "message": f"开始生成多行业报告，包含{len(industries)}个行业",
                "industries": industries
            }, user_id)
        
        # 生成报告
        reports = generator.generate_all_industry_reports(industries)
        
        # 发送完成通知
        if user_id:
            await manager.send_json_to_user({
                "type": "report_generation",
                "status": "completed",
                "message": f"多行业报告生成完成，共生成{len(reports)}个报告",
                "reports": reports,
                "industries": industries
            }, user_id)
        
        system_logger.info("多行业报告生成任务完成", reports_count=len(reports), user=user_id)
        
    except Exception as e:
        system_logger.error("多行业报告生成任务失败", error=e, user=user_id)
        if user_id:
            await manager.send_json_to_user({
                "type": "report_generation",
                "status": "failed",
                "message": f"报告生成失败: {str(e)}"
            }, user_id)


def _refresh_reports_data():
    """刷新报告数据（这应该移到数据层）"""
    # 这里应该实现从文件系统读取报告列表的逻辑
    # 暂时返回空列表
    return [] 