#!/usr/bin/env python3
"""
认证和授权模块
"""

from typing import Optional, Dict, Any
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from passlib.hash import bcrypt
from jose import JWTError, jwt

from config.settings import settings
from utils.logger import system_logger
from utils.exceptions import AuthenticationError, TokenError, PermissionError
from core.models import User, UserInDB

# OAuth2设置
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 模拟用户数据库（实际项目中应使用真实数据库）
fake_users_db: Dict[str, UserInDB] = {
    "admin": UserInDB(
        username="admin",
        hashed_password=pwd_context.hash("adminpass"),
        role="admin",
        email="admin@example.com",
        is_active=True,
        created_at=datetime.now()
    ),
    "analyst": UserInDB(
        username="analyst",
        hashed_password=pwd_context.hash("analyst123"),
        role="analyst",
        email="analyst@example.com",
        is_active=True,
        created_at=datetime.now()
    ),
    "viewer": UserInDB(
        username="viewer",
        hashed_password=pwd_context.hash("viewer123"),
        role="viewer",
        email="viewer@example.com",
        is_active=True,
        created_at=datetime.now()
    )
}


class AuthService:
    """认证服务类"""

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """验证密码"""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """获取密码哈希值"""
        return pwd_context.hash(password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        """创建访问令牌"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
        return encoded_jwt

    @staticmethod
    def verify_token(token: str) -> Optional[str]:
        """验证JWT令牌"""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            username: str = payload.get("sub")
            if username is None:
                return None
            return username
        except JWTError:
            return None
    
    @staticmethod
    def get_user(username: str) -> Optional[UserInDB]:
        """获取用户信息"""
        return fake_users_db.get(username)
    
    @staticmethod
    def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
        """验证用户身份"""
        user = AuthService.get_user(username)
        if not user:
            return None
        if not AuthService.verify_password(password, user.hashed_password):
            return None
        if not user.is_active:
            return None
        return user
    
    @staticmethod
    def create_user(
        username: str, 
        password: str, 
        role: str = "viewer",
        email: Optional[str] = None
    ) -> bool:
        """创建新用户"""
        if username in fake_users_db:
            return False
        
        hashed_password = AuthService.get_password_hash(password)
        user = UserInDB(
            username=username,
            hashed_password=hashed_password,
            role=role,
            email=email or f"{username}@example.com",
            is_active=True,
            created_at=datetime.now()
        )
        
        fake_users_db[username] = user
        system_logger.info("新用户创建成功", username=username, role=role)
        return True
    
    @staticmethod
    def update_user(username: str, **kwargs) -> bool:
        """更新用户信息"""
        if username not in fake_users_db:
            return False
        
        user = fake_users_db[username]
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        user.updated_at = datetime.now()
        system_logger.info("用户信息更新成功", username=username)
        return True
    
    @staticmethod
    def delete_user(username: str) -> bool:
        """删除用户（软删除）"""
        if username not in fake_users_db:
            return False
        
        fake_users_db[username].is_active = False
        fake_users_db[username].updated_at = datetime.now()
        system_logger.info("用户已停用", username=username)
        return True
    
    @staticmethod
    def get_all_users() -> list[User]:
        """获取所有用户列表"""
        return [
            User(
                username=user.username,
                role=user.role,
                email=user.email,
                is_active=user.is_active,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
            for user in fake_users_db.values()
        ]


class PermissionManager:
    """权限管理器"""
    
    # 角色权限映射
    ROLE_PERMISSIONS = {
        "admin": [
            "user_management",
            "system_settings",
            "all_reports",
            "report_generation", 
            "data_import_export",
            "analysis_tools",
            "websocket_access"
        ],
        "analyst": [
            "all_reports",
            "report_generation",
            "data_import_export", 
            "analysis_tools",
            "websocket_access"
        ],
        "viewer": [
            "view_reports",
            "download_reports"
        ]
    }
    
    @staticmethod
    def has_permission(user: User, permission: str) -> bool:
        """检查用户是否有特定权限"""
        user_permissions = PermissionManager.ROLE_PERMISSIONS.get(user.role, [])
        return permission in user_permissions
    
    @staticmethod
    def require_permission(permission: str):
        """权限装饰器"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                # 这里需要从请求中获取当前用户
                # 实际实现时需要配合依赖注入
                return func(*args, **kwargs)
            return wrapper
        return decorator
    
    @staticmethod
    def get_user_permissions(user: User) -> list[str]:
        """获取用户所有权限"""
        return PermissionManager.ROLE_PERMISSIONS.get(user.role, [])


def get_current_user(token: str = Depends(oauth2_scheme)) -> Optional[User]:
    """获取当前用户依赖"""
    if not token:
        return None

    try:
        # 验证JWT token
        username = AuthService.verify_token(token)
        if not username:
            raise TokenError("Token无效或已过期")

        user_data = fake_users_db.get(username)
        if not user_data:
            raise TokenError("用户不存在")

        if not user_data.is_active:
            raise AuthenticationError("用户已禁用")

        return User(
            username=user_data.username,
            role=user_data.role,
            email=user_data.email,
            is_active=user_data.is_active,
            created_at=user_data.created_at,
            updated_at=user_data.updated_at
        )

    except JWTError:
        raise TokenError("Token无效或已过期")
    except Exception as e:
        system_logger.error("获取当前用户失败", error=e, token=token)
        raise AuthenticationError("认证失败")


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """获取当前活跃用户依赖"""
    if not current_user:
        raise AuthenticationError("需要登录")
    
    if not current_user.is_active:
        raise AuthenticationError("用户账号已禁用")
    
    return current_user


def require_admin(current_user: User = Depends(get_current_active_user)) -> User:
    """要求管理员权限依赖"""
    if current_user.role != "admin":
        raise PermissionError("需要管理员权限")
    
    return current_user


def require_analyst_or_admin(current_user: User = Depends(get_current_active_user)) -> User:
    """要求分析师或管理员权限依赖"""
    if current_user.role not in ["analyst", "admin"]:
        raise PermissionError("需要分析师或管理员权限")
    
    return current_user


def check_permission(permission: str):
    """检查权限装饰器工厂"""
    def permission_dependency(current_user: User = Depends(get_current_active_user)) -> User:
        if not PermissionManager.has_permission(current_user, permission):
            raise PermissionError(f"需要权限: {permission}", required_permission=permission)
        return current_user
    
    return permission_dependency


async def login_user(form_data: OAuth2PasswordRequestForm) -> dict:
    """用户登录"""
    try:
        user = AuthService.authenticate_user(form_data.username, form_data.password)
        if not user:
            system_logger.warning("登录失败", username=form_data.username, reason="用户名或密码错误")
            raise AuthenticationError("用户名或密码错误")

        # 创建JWT访问令牌
        access_token_expires = timedelta(minutes=settings.TOKEN_EXPIRE_MINUTES)
        access_token = AuthService.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )

        system_logger.info("用户登录成功", username=user.username, role=user.role)

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": int(access_token_expires.total_seconds()),
            "user_info": {
                "username": user.username,
                "role": user.role,
                "email": user.email,
                "permissions": PermissionManager.get_user_permissions(
                    User(username=user.username, role=user.role, email=user.email, is_active=user.is_active)
                )
            }
        }

    except AuthenticationError:
        raise
    except Exception as e:
        system_logger.error("登录过程发生错误", error=e, username=form_data.username)
        raise AuthenticationError("登录失败")


async def logout_user(current_user: User = Depends(get_current_active_user)) -> dict:
    """用户登出"""
    try:
        system_logger.info("用户登出", username=current_user.username)
        return {"message": "登出成功"}
        
    except Exception as e:
        system_logger.error("登出过程发生错误", error=e, username=current_user.username)
        return {"message": "登出过程出现问题，但已清除本地状态"}


def init_default_users():
    """初始化默认用户"""
    system_logger.info("初始化默认用户账户")
    system_logger.info("默认管理员账户: admin / adminpass")
    system_logger.info("默认分析师账户: analyst / analyst123") 
    system_logger.info("默认查看者账户: viewer / viewer123") 