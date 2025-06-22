#!/usr/bin/env python3
"""
数据库API端点
支持数据库连接、查询和数据管理
"""

import os
import sys
import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
import pandas as pd

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.data.mysql_manager import MySQLManager
from src.data.virtual_data_generator import VirtualDataGenerator
from src.config.database_config import DatabaseConfig

# 配置日志
logger = logging.getLogger(__name__)

# 创建路由器
router = APIRouter(prefix="/api/database", tags=["database"])

# 全局数据库管理器
db_manager: Optional[MySQLManager] = None

class DatabaseConnectionRequest(BaseModel):
    """数据库连接请求模型"""
    host: str = "localhost"
    port: int = 3306
    user: str = "root"
    password: str
    database: str = "analysis_system"
    db_type: str = "mysql"

class DatabaseQueryRequest(BaseModel):
    """数据库查询请求模型"""
    sql: str
    limit: Optional[int] = 1000

class DatabaseResponse(BaseModel):
    """数据库响应模型"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

@router.post("/connect", response_model=DatabaseResponse)
async def connect_database(request: DatabaseConnectionRequest):
    """
    连接数据库
    
    Args:
        request: 数据库连接请求
        
    Returns:
        DatabaseResponse: 连接结果
    """
    global db_manager
    
    try:
        logger.info(f"尝试连接数据库: {request.host}:{request.port}")
        
        # 创建数据库配置
        config = {
            'host': request.host,
            'port': request.port,
            'user': request.user,
            'password': request.password,
            'database': request.database,
            'db_type': request.db_type
        }
        
        # 创建管理器
        db_manager = MySQLManager(config)
        
        # 设置数据库连接
        if not db_manager.setup_database():
            raise Exception("数据库连接设置失败")
        
        # 测试连接
        if not db_manager.test_connection():
            raise Exception("数据库连接测试失败")
        
        logger.info("数据库连接成功")
        
        return DatabaseResponse(
            success=True,
            message="数据库连接成功",
            data={
                "host": request.host,
                "port": request.port,
                "database": request.database,
                "connected_at": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        logger.error(f"数据库连接失败: {str(e)}")
        return DatabaseResponse(
            success=False,
            message="数据库连接失败",
            error=str(e)
        )

@router.get("/test", response_model=DatabaseResponse)
async def test_database_connection():
    """
    测试数据库连接
    
    Returns:
        DatabaseResponse: 测试结果
    """
    global db_manager
    
    try:
        if not db_manager:
            raise Exception("数据库未连接，请先连接数据库")
        
        if db_manager.test_connection():
            return DatabaseResponse(
                success=True,
                message="数据库连接正常",
                data={"status": "connected", "tested_at": datetime.now().isoformat()}
            )
        else:
            raise Exception("数据库连接测试失败")
            
    except Exception as e:
        logger.error(f"数据库连接测试失败: {str(e)}")
        return DatabaseResponse(
            success=False,
            message="数据库连接测试失败",
            error=str(e)
        )

@router.post("/query", response_model=DatabaseResponse)
async def query_database(request: DatabaseQueryRequest):
    """
    执行数据库查询
    
    Args:
        request: 查询请求
        
    Returns:
        DatabaseResponse: 查询结果
    """
    global db_manager
    
    try:
        if not db_manager:
            raise Exception("数据库未连接，请先连接数据库")
        
        logger.info(f"执行SQL查询: {request.sql[:100]}...")
        
        # 执行查询
        df = db_manager.query_data(request.sql)
        
        if df is None:
            raise Exception("查询执行失败")
        
        # 限制返回记录数
        if request.limit and len(df) > request.limit:
            df = df.head(request.limit)
        
        # 转换为字典格式
        result_data = {
            "columns": df.columns.tolist(),
            "data": df.to_dict('records'),
            "total_rows": len(df),
            "query_time": datetime.now().isoformat()
        }
        
        return DatabaseResponse(
            success=True,
            message=f"查询成功，返回 {len(df)} 条记录",
            data=result_data
        )
        
    except Exception as e:
        logger.error(f"数据库查询失败: {str(e)}")
        return DatabaseResponse(
            success=False,
            message="数据库查询失败",
            error=str(e)
        )

@router.get("/business-data", response_model=DatabaseResponse)
async def get_business_data(limit: int = Query(100, description="限制返回记录数")):
    """
    获取业务数据
    
    Args:
        limit: 限制返回记录数
        
    Returns:
        DatabaseResponse: 业务数据
    """
    global db_manager
    
    try:
        if not db_manager:
            raise Exception("数据库未连接，请先连接数据库")
        
        df = db_manager.get_business_data(limit)
        
        if df is None:
            raise Exception("获取业务数据失败")
        
        result_data = {
            "columns": df.columns.tolist(),
            "data": df.to_dict('records'),
            "total_rows": len(df)
        }
        
        return DatabaseResponse(
            success=True,
            message=f"获取业务数据成功，返回 {len(df)} 条记录",
            data=result_data
        )
        
    except Exception as e:
        logger.error(f"获取业务数据失败: {str(e)}")
        return DatabaseResponse(
            success=False,
            message="获取业务数据失败",
            error=str(e)
        )

@router.get("/financial-summary", response_model=DatabaseResponse)
async def get_financial_summary():
    """
    获取金融数据汇总
    
    Returns:
        DatabaseResponse: 金融汇总数据
    """
    global db_manager
    
    try:
        if not db_manager:
            raise Exception("数据库未连接，请先连接数据库")
        
        df = db_manager.get_financial_summary()
        
        if df is None:
            raise Exception("获取金融汇总数据失败")
        
        result_data = {
            "columns": df.columns.tolist(),
            "data": df.to_dict('records'),
            "total_rows": len(df)
        }
        
        return DatabaseResponse(
            success=True,
            message=f"获取金融汇总数据成功，返回 {len(df)} 条记录",
            data=result_data
        )
        
    except Exception as e:
        logger.error(f"获取金融汇总数据失败: {str(e)}")
        return DatabaseResponse(
            success=False,
            message="获取金融汇总数据失败",
            error=str(e)
        )

@router.get("/ai-agent-performance", response_model=DatabaseResponse)
async def get_ai_agent_performance():
    """
    获取AI代理性能数据
    
    Returns:
        DatabaseResponse: AI代理性能数据
    """
    global db_manager
    
    try:
        if not db_manager:
            raise Exception("数据库未连接，请先连接数据库")
        
        df = db_manager.get_ai_agent_performance()
        
        if df is None:
            raise Exception("获取AI代理性能数据失败")
        
        result_data = {
            "columns": df.columns.tolist(),
            "data": df.to_dict('records'),
            "total_rows": len(df)
        }
        
        return DatabaseResponse(
            success=True,
            message=f"获取AI代理性能数据成功，返回 {len(df)} 条记录",
            data=result_data
        )
        
    except Exception as e:
        logger.error(f"获取AI代理性能数据失败: {str(e)}")
        return DatabaseResponse(
            success=False,
            message="获取AI代理性能数据失败",
            error=str(e)
        )

@router.post("/generate-data", response_model=DatabaseResponse)
async def generate_virtual_data():
    """
    生成并导入虚拟数据
    
    Returns:
        DatabaseResponse: 生成结果
    """
    global db_manager
    
    try:
        if not db_manager:
            raise Exception("数据库未连接，请先连接数据库")
        
        logger.info("开始生成虚拟数据...")
        
        if db_manager.generate_and_import_data():
            return DatabaseResponse(
                success=True,
                message="虚拟数据生成并导入成功",
                data={
                    "generated_at": datetime.now().isoformat(),
                    "tables": ["business_data", "users", "financial_data", "ai_agent_data", "community_group_buying", "system_logs"]
                }
            )
        else:
            raise Exception("虚拟数据生成或导入失败")
            
    except Exception as e:
        logger.error(f"虚拟数据生成失败: {str(e)}")
        return DatabaseResponse(
            success=False,
            message="虚拟数据生成失败",
            error=str(e)
        )

@router.get("/tables", response_model=DatabaseResponse)
async def get_database_tables():
    """
    获取数据库表列表
    
    Returns:
        DatabaseResponse: 表列表
    """
    global db_manager
    
    try:
        if not db_manager:
            raise Exception("数据库未连接，请先连接数据库")
        
        # 查询所有表
        sql = "SHOW TABLES"
        df = db_manager.query_data(sql)
        
        if df is None:
            raise Exception("获取表列表失败")
        
        tables = df.iloc[:, 0].tolist()
        
        return DatabaseResponse(
            success=True,
            message=f"获取表列表成功，共 {len(tables)} 个表",
            data={
                "tables": tables,
                "total_count": len(tables)
            }
        )
        
    except Exception as e:
        logger.error(f"获取表列表失败: {str(e)}")
        return DatabaseResponse(
            success=False,
            message="获取表列表失败",
            error=str(e)
        )

@router.get("/status", response_model=DatabaseResponse)
async def get_database_status():
    """
    获取数据库状态
    
    Returns:
        DatabaseResponse: 数据库状态
    """
    global db_manager
    
    try:
        if not db_manager:
            return DatabaseResponse(
                success=True,
                message="数据库未连接",
                data={
                    "connected": False,
                    "status": "disconnected"
                }
            )
        
        # 测试连接
        is_connected = db_manager.test_connection()
        
        status_data = {
            "connected": is_connected,
            "status": "connected" if is_connected else "disconnected",
            "config": {
                "host": db_manager.default_config.get('host'),
                "port": db_manager.default_config.get('port'),
                "database": db_manager.default_config.get('database')
            } if db_manager.db_config else None,
            "checked_at": datetime.now().isoformat()
        }
        
        return DatabaseResponse(
            success=True,
            message="数据库状态获取成功",
            data=status_data
        )
        
    except Exception as e:
        logger.error(f"获取数据库状态失败: {str(e)}")
        return DatabaseResponse(
            success=False,
            message="获取数据库状态失败",
            error=str(e)
        )

@router.post("/disconnect", response_model=DatabaseResponse)
async def disconnect_database():
    """
    断开数据库连接
    
    Returns:
        DatabaseResponse: 断开结果
    """
    global db_manager
    
    try:
        if db_manager:
            db_manager.close_connection()
            db_manager = None
        
        return DatabaseResponse(
            success=True,
            message="数据库连接已断开",
            data={"disconnected_at": datetime.now().isoformat()}
        )
        
    except Exception as e:
        logger.error(f"断开数据库连接失败: {str(e)}")
        return DatabaseResponse(
            success=False,
            message="断开数据库连接失败",
            error=str(e)
        ) 