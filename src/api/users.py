#!/usr/bin/env python3
"""
用户管理API路由
提供用户注册、登录、权限管理等功能
"""

from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Depends, Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr

from src.config.settings import settings
from src.utils.logger import system_logger
from src.core.auth import get_current_user, create_access_token, verify_password, get_password_hash
from src.core.models import User, UserCreate, UserUpdate, UserRole
from src.utils.exceptions import (
    UserNotFoundError,
    UserAlreadyExistsError,
    InvalidCredentialsError,
    PermissionDeniedError
)

# 创建路由器
router = APIRouter(prefix="/api/users", tags=["users"])

# 模拟用户数据库（实际项目中应该使用真实数据库）
users_db = {
    "admin": {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "full_name": "系统管理员",
        "hashed_password": get_password_hash("adminpass"),
        "role": UserRole.ADMIN,
        "is_active": True,
        "created_at": datetime.now(),
        "last_login": None,
        "login_count": 0
    },
    "analyst": {
        "id": 2,
        "username": "analyst",
        "email": "analyst@example.com",
        "full_name": "数据分析师",
        "hashed_password": get_password_hash("analyst123"),
        "role": UserRole.ANALYST,
        "is_active": True,
        "created_at": datetime.now(),
        "last_login": None,
        "login_count": 0
    },
    "viewer": {
        "id": 3,
        "username": "viewer",
        "email": "viewer@example.com",
        "full_name": "报告查看者",
        "hashed_password": get_password_hash("viewer123"),
        "role": UserRole.VIEWER,
        "is_active": True,
        "created_at": datetime.now(),
        "last_login": None,
        "login_count": 0
    }
}


class UserListResponse(BaseModel):
    """用户列表响应模型"""
    users: List[Dict[str, Any]]
    total: int
    page: int
    size: int


class PasswordChangeRequest(BaseModel):
    """密码修改请求"""
    current_password: str
    new_password: str


class UserStatsResponse(BaseModel):
    """用户统计响应"""
    total_users: int
    active_users: int
    admin_count: int
    analyst_count: int
    viewer_count: int
    recent_logins: int


@router.get("/", response_model=UserListResponse)
async def get_users(
    page: int = 1,
    size: int = 10,
    search: Optional[str] = None,
    role: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """获取用户列表"""
    # 检查权限
    if current_user.role not in [UserRole.ADMIN, UserRole.ANALYST]:
        raise HTTPException(status_code=403, detail="权限不足")
    
    try:
        # 过滤用户
        filtered_users = []
        for user_data in users_db.values():
            if search and search.lower() not in user_data["username"].lower() and search.lower() not in user_data["full_name"].lower():
                continue
            if role and user_data["role"] != role:
                continue
            
            # 隐藏敏感信息
            safe_user = {
                "id": user_data["id"],
                "username": user_data["username"],
                "email": user_data["email"],
                "full_name": user_data["full_name"],
                "role": user_data["role"],
                "is_active": user_data["is_active"],
                "created_at": user_data["created_at"].isoformat(),
                "last_login": user_data["last_login"].isoformat() if user_data["last_login"] else None,
                "login_count": user_data["login_count"]
            }
            filtered_users.append(safe_user)
        
        # 分页
        start = (page - 1) * size
        end = start + size
        paginated_users = filtered_users[start:end]
        
        system_logger.info("获取用户列表", user=current_user.username, total=len(filtered_users))
        
        return UserListResponse(
            users=paginated_users,
            total=len(filtered_users),
            page=page,
            size=size
        )
        
    except Exception as e:
        system_logger.error("获取用户列表失败", error=e, user=current_user.username)
        raise HTTPException(status_code=500, detail="获取用户列表失败")


@router.get("/stats", response_model=UserStatsResponse)
async def get_user_stats(current_user: User = Depends(get_current_user)):
    """获取用户统计信息"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="权限不足")
    
    try:
        total_users = len(users_db)
        active_users = sum(1 for u in users_db.values() if u["is_active"])
        admin_count = sum(1 for u in users_db.values() if u["role"] == UserRole.ADMIN)
        analyst_count = sum(1 for u in users_db.values() if u["role"] == UserRole.ANALYST)
        viewer_count = sum(1 for u in users_db.values() if u["role"] == UserRole.VIEWER)
        
        # 计算最近7天登录的用户数
        recent_threshold = datetime.now() - timedelta(days=7)
        recent_logins = sum(1 for u in users_db.values() 
                          if u["last_login"] and u["last_login"] > recent_threshold)
        
        return UserStatsResponse(
            total_users=total_users,
            active_users=active_users,
            admin_count=admin_count,
            analyst_count=analyst_count,
            viewer_count=viewer_count,
            recent_logins=recent_logins
        )
        
    except Exception as e:
        system_logger.error("获取用户统计失败", error=e, user=current_user.username)
        raise HTTPException(status_code=500, detail="获取用户统计失败")


@router.get("/profile")
async def get_user_profile(current_user: User = Depends(get_current_user)):
    """获取当前用户信息"""
    try:
        user_data = users_db.get(current_user.username)
        if not user_data:
            raise UserNotFoundError("用户不存在")
        
        profile = {
            "id": user_data["id"],
            "username": user_data["username"],
            "email": user_data["email"],
            "full_name": user_data["full_name"],
            "role": user_data["role"],
            "is_active": user_data["is_active"],
            "created_at": user_data["created_at"].isoformat(),
            "last_login": user_data["last_login"].isoformat() if user_data["last_login"] else None,
            "login_count": user_data["login_count"]
        }
        
        return JSONResponse(content={"success": True, "profile": profile})
        
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="用户不存在")
    except Exception as e:
        system_logger.error("获取用户信息失败", error=e, user=current_user.username)
        raise HTTPException(status_code=500, detail="获取用户信息失败")


@router.put("/profile")
async def update_user_profile(
    user_update: Dict[str, Any] = Body(...),
    current_user: User = Depends(get_current_user)
):
    """更新当前用户信息"""
    try:
        user_data = users_db.get(current_user.username)
        if not user_data:
            raise UserNotFoundError("用户不存在")
        
        # 允许更新的字段
        allowed_fields = ["email", "full_name"]
        updated_fields = []
        
        for field in allowed_fields:
            if field in user_update:
                user_data[field] = user_update[field]
                updated_fields.append(field)
        
        if updated_fields:
            system_logger.info("用户信息已更新", user=current_user.username, fields=updated_fields)
        
        return JSONResponse(content={
            "success": True,
            "message": "用户信息更新成功",
            "updated_fields": updated_fields
        })
        
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="用户不存在")
    except Exception as e:
        system_logger.error("更新用户信息失败", error=e, user=current_user.username)
        raise HTTPException(status_code=500, detail="更新用户信息失败")


@router.post("/change-password")
async def change_password(
    password_data: PasswordChangeRequest,
    current_user: User = Depends(get_current_user)
):
    """修改密码"""
    try:
        user_data = users_db.get(current_user.username)
        if not user_data:
            raise UserNotFoundError("用户不存在")
        
        # 验证当前密码
        if not verify_password(password_data.current_password, user_data["hashed_password"]):
            raise InvalidCredentialsError("当前密码错误")
        
        # 更新密码
        user_data["hashed_password"] = get_password_hash(password_data.new_password)
        
        system_logger.info("用户密码已修改", user=current_user.username)
        
        return JSONResponse(content={
            "success": True,
            "message": "密码修改成功"
        })
        
    except (UserNotFoundError, InvalidCredentialsError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        system_logger.error("修改密码失败", error=e, user=current_user.username)
        raise HTTPException(status_code=500, detail="修改密码失败")


@router.post("/create")
async def create_user(
    user_data: Dict[str, Any] = Body(...),
    current_user: User = Depends(get_current_user)
):
    """创建新用户"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="权限不足")
    
    try:
        username = user_data.get("username")
        if not username:
            raise HTTPException(status_code=400, detail="用户名不能为空")
        
        if username in users_db:
            raise UserAlreadyExistsError("用户名已存在")
        
        # 创建新用户
        new_user = {
            "id": len(users_db) + 1,
            "username": username,
            "email": user_data.get("email", ""),
            "full_name": user_data.get("full_name", ""),
            "hashed_password": get_password_hash(user_data.get("password", "123456")),
            "role": user_data.get("role", UserRole.VIEWER),
            "is_active": True,
            "created_at": datetime.now(),
            "last_login": None,
            "login_count": 0
        }
        
        users_db[username] = new_user
        
        system_logger.info("新用户已创建", user=current_user.username, new_user=username)
        
        return JSONResponse(content={
            "success": True,
            "message": "用户创建成功",
            "user_id": new_user["id"]
        })
        
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        system_logger.error("创建用户失败", error=e, user=current_user.username)
        raise HTTPException(status_code=500, detail="创建用户失败")


@router.put("/{user_id}")
async def update_user(
    user_id: int,
    user_update: Dict[str, Any] = Body(...),
    current_user: User = Depends(get_current_user)
):
    """更新用户信息"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="权限不足")
    
    try:
        # 查找用户
        target_user = None
        target_username = None
        for username, user_data in users_db.items():
            if user_data["id"] == user_id:
                target_user = user_data
                target_username = username
                break
        
        if not target_user:
            raise UserNotFoundError("用户不存在")
        
        # 更新用户信息
        updated_fields = []
        allowed_fields = ["email", "full_name", "role", "is_active"]
        
        for field in allowed_fields:
            if field in user_update:
                target_user[field] = user_update[field]
                updated_fields.append(field)
        
        system_logger.info("用户信息已更新", admin=current_user.username, 
                          target_user=target_username, fields=updated_fields)
        
        return JSONResponse(content={
            "success": True,
            "message": "用户信息更新成功",
            "updated_fields": updated_fields
        })
        
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="用户不存在")
    except Exception as e:
        system_logger.error("更新用户失败", error=e, user=current_user.username)
        raise HTTPException(status_code=500, detail="更新用户失败")


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user)
):
    """删除用户"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="权限不足")
    
    try:
        # 查找并删除用户
        target_username = None
        for username, user_data in users_db.items():
            if user_data["id"] == user_id:
                target_username = username
                break
        
        if not target_username:
            raise UserNotFoundError("用户不存在")
        
        if target_username == current_user.username:
            raise HTTPException(status_code=400, detail="不能删除自己的账户")
        
        del users_db[target_username]
        
        system_logger.info("用户已删除", admin=current_user.username, deleted_user=target_username)
        
        return JSONResponse(content={
            "success": True,
            "message": "用户删除成功"
        })
        
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="用户不存在")
    except Exception as e:
        system_logger.error("删除用户失败", error=e, user=current_user.username)
        raise HTTPException(status_code=500, detail="删除用户失败")


def update_user_login(username: str):
    """更新用户登录信息"""
    if username in users_db:
        users_db[username]["last_login"] = datetime.now()
        users_db[username]["login_count"] += 1 