from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List, Optional
import pandas as pd
import json
import os
from datetime import datetime

from src.core.data_processor import DataProcessor
from src.core.analysis_engine import AnalysisEngine
from src.core.report_generator import ReportGenerator
from src.core.system_manager import SystemManager

# 导入数据库路由
try:
    from src.api.database import router as database_router
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False

app = FastAPI(title="分析报告系统API")

# 包含数据库路由（如果可用）
if DATABASE_AVAILABLE:
    app.include_router(database_router)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化核心组件
data_processor = DataProcessor()
analysis_engine = AnalysisEngine()
report_generator = ReportGenerator()
system_manager = SystemManager()

# OAuth2认证
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 依赖项
async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = system_manager.verify_token(token)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="无效的认证凭据",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

# 认证路由
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    token = system_manager.authenticate_user(form_data.username, form_data.password)
    if not token:
        raise HTTPException(
            status_code=401,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": token, "token_type": "bearer"}

# 数据处理路由
@app.post("/api/data/import")
async def import_data(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    try:
        # 保存上传的文件
        file_path = f"temp/{file.filename}"
        os.makedirs("temp", exist_ok=True)
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
            
        # 根据文件扩展名确定文件类型
        file_type = file.filename.split(".")[-1].lower()
        if file_type not in ["csv", "xlsx", "json"]:
            raise HTTPException(status_code=400, detail="不支持的文件类型")
            
        # 导入数据
        df = data_processor.import_data(file_path, file_type)
        
        # 预处理数据
        df = data_processor.preprocess_data(df)
        
        # 验证数据
        validation_results = data_processor.validate_data(df)
        
        return {
            "message": "数据导入成功",
            "validation_results": validation_results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    finally:
        # 清理临时文件
        if os.path.exists(file_path):
            os.remove(file_path)

# 数据分析路由
@app.post("/api/analysis")
async def analyze_data(
    analysis_type: str,
    data: dict,
    current_user: dict = Depends(get_current_user)
):
    try:
        # 将数据转换为DataFrame
        df = pd.DataFrame(data)
        
        # 执行分析
        results = analysis_engine.analyze_data(df, analysis_type)
        
        return {
            "message": "分析完成",
            "results": results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 报告生成路由
@app.post("/api/reports/generate")
async def generate_report(
    report_type: str,
    data: dict,
    output_format: str = "html",
    current_user: dict = Depends(get_current_user)
):
    try:
        if report_type == "visualization":
            # 将数据转换为DataFrame
            df = pd.DataFrame(data)
            report_path = report_generator.create_visualization_report(
                df,
                output_format=output_format
            )
        elif report_type == "analysis":
            report_path = report_generator.create_analysis_report(
                data,
                output_format=output_format
            )
        else:
            raise HTTPException(status_code=400, detail="不支持的报告类型")
            
        return {
            "message": "报告生成成功",
            "report_path": report_path
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 系统管理路由
@app.post("/api/users")
async def create_user(
    username: str,
    password: str,
    role: str = "user",
    current_user: dict = Depends(get_current_user)
):
    try:
        if not system_manager.check_permission(current_user["username"], "manage_users"):
            raise HTTPException(status_code=403, detail="没有权限创建用户")
            
        success = system_manager.create_user(
            username,
            password,
            role,
            current_user["username"]
        )
        
        if not success:
            raise HTTPException(status_code=400, detail="用户名已存在")
            
        return {"message": "用户创建成功"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/users/{username}")
async def delete_user(
    username: str,
    current_user: dict = Depends(get_current_user)
):
    try:
        if not system_manager.check_permission(current_user["username"], "manage_users"):
            raise HTTPException(status_code=403, detail="没有权限删除用户")
            
        success = system_manager.delete_user(username, current_user["username"])
        
        if not success:
            raise HTTPException(status_code=404, detail="用户不存在")
            
        return {"message": "用户删除成功"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/logs")
async def get_logs(
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    level: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    try:
        if not system_manager.check_permission(current_user["username"], "read"):
            raise HTTPException(status_code=403, detail="没有权限查看日志")
            
        logs = system_manager.get_system_logs(start_time, end_time, level)
        return {"logs": logs}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/system/backup")
async def backup_system(
    backup_path: str,
    current_user: dict = Depends(get_current_user)
):
    try:
        if not system_manager.check_permission(current_user["username"], "manage_system"):
            raise HTTPException(status_code=403, detail="没有权限备份系统")
            
        backup_file = system_manager.backup_system(backup_path)
        return {
            "message": "系统备份成功",
            "backup_file": backup_file
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/system/restore")
async def restore_system(
    backup_file: str,
    current_user: dict = Depends(get_current_user)
):
    try:
        if not system_manager.check_permission(current_user["username"], "manage_system"):
            raise HTTPException(status_code=403, detail="没有权限恢复系统")
            
        system_manager.restore_system(backup_file)
        return {"message": "系统恢复成功"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 