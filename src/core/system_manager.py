import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Union
import hashlib
import jwt
from pathlib import Path
import shutil

class SystemManager:
    """系统管理核心类，负责用户认证、权限管理和系统日志"""
    
    def __init__(self, config_path: str = 'src/config'):
        self.logger = logging.getLogger(__name__)
        self.config_path = config_path
        self.users_file = os.path.join(config_path, 'users.json')
        self.roles_file = os.path.join(config_path, 'roles.json')
        self.log_file = os.path.join(config_path, 'system.log')
        self.secret_key = os.getenv('SECRET_KEY', 'your-secret-key')
        
        # 初始化日志
        self._setup_logging()
        
        # 初始化用户和角色
        self._init_users_and_roles()
        
    def _setup_logging(self) -> None:
        """设置日志系统"""
        try:
            logging.basicConfig(
                filename=self.log_file,
                level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
        except Exception as e:
            print(f"日志系统初始化失败: {str(e)}")
            raise
            
    def _init_users_and_roles(self) -> None:
        """初始化用户和角色数据"""
        try:
            # 确保配置文件目录存在
            os.makedirs(self.config_path, exist_ok=True)
            
            # 初始化用户文件
            if not os.path.exists(self.users_file):
                with open(self.users_file, 'w', encoding='utf-8') as f:
                    json.dump({
                        'admin': {
                            'password': self._hash_password('admin'),
                            'role': 'admin',
                            'created_at': datetime.now().isoformat()
                        }
                    }, f, ensure_ascii=False, indent=2)
                    
            # 初始化角色文件
            if not os.path.exists(self.roles_file):
                with open(self.roles_file, 'w', encoding='utf-8') as f:
                    json.dump({
                        'admin': {
                            'permissions': ['read', 'write', 'delete', 'manage_users'],
                            'description': '系统管理员'
                        },
                        'user': {
                            'permissions': ['read', 'write'],
                            'description': '普通用户'
                        }
                    }, f, ensure_ascii=False, indent=2)
                    
        except Exception as e:
            self.logger.error(f"用户和角色初始化失败: {str(e)}")
            raise
            
    def _hash_password(self, password: str) -> str:
        """密码哈希"""
        return hashlib.sha256(password.encode()).hexdigest()
        
    def authenticate_user(self, username: str, password: str) -> Optional[str]:
        """
        用户认证
        
        Args:
            username: 用户名
            password: 密码
            
        Returns:
            Optional[str]: JWT令牌
        """
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                users = json.load(f)
                
            if username not in users:
                return None
                
            if users[username]['password'] != self._hash_password(password):
                return None
                
            # 生成JWT令牌
            token = jwt.encode({
                'username': username,
                'role': users[username]['role'],
                'exp': datetime.utcnow().timestamp() + 3600  # 1小时过期
            }, self.secret_key, algorithm='HS256')
            
            self.logger.info(f"用户 {username} 登录成功")
            return token
            
        except Exception as e:
            self.logger.error(f"用户认证失败: {str(e)}")
            raise
            
    def verify_token(self, token: str) -> Optional[Dict]:
        """
        验证JWT令牌
        
        Args:
            token: JWT令牌
            
        Returns:
            Optional[Dict]: 用户信息
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            self.logger.warning("令牌已过期")
            return None
        except jwt.InvalidTokenError:
            self.logger.warning("无效的令牌")
            return None
            
    def create_user(self, 
                   username: str,
                   password: str,
                   role: str = 'user',
                   created_by: str = 'admin') -> bool:
        """
        创建用户
        
        Args:
            username: 用户名
            password: 密码
            role: 角色
            created_by: 创建者
            
        Returns:
            bool: 是否创建成功
        """
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                users = json.load(f)
                
            if username in users:
                return False
                
            users[username] = {
                'password': self._hash_password(password),
                'role': role,
                'created_at': datetime.now().isoformat(),
                'created_by': created_by
            }
            
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(users, f, ensure_ascii=False, indent=2)
                
            self.logger.info(f"用户 {username} 创建成功")
            return True
            
        except Exception as e:
            self.logger.error(f"用户创建失败: {str(e)}")
            raise
            
    def delete_user(self, username: str, deleted_by: str) -> bool:
        """
        删除用户
        
        Args:
            username: 用户名
            deleted_by: 删除者
            
        Returns:
            bool: 是否删除成功
        """
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                users = json.load(f)
                
            if username not in users:
                return False
                
            del users[username]
            
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(users, f, ensure_ascii=False, indent=2)
                
            self.logger.info(f"用户 {username} 被 {deleted_by} 删除")
            return True
            
        except Exception as e:
            self.logger.error(f"用户删除失败: {str(e)}")
            raise
            
    def check_permission(self, username: str, permission: str) -> bool:
        """
        检查用户权限
        
        Args:
            username: 用户名
            permission: 权限
            
        Returns:
            bool: 是否有权限
        """
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                users = json.load(f)
                
            if username not in users:
                return False
                
            role = users[username]['role']
            
            with open(self.roles_file, 'r', encoding='utf-8') as f:
                roles = json.load(f)
                
            if role not in roles:
                return False
                
            return permission in roles[role]['permissions']
            
        except Exception as e:
            self.logger.error(f"权限检查失败: {str(e)}")
            raise
            
    def get_system_logs(self, 
                       start_time: Optional[str] = None,
                       end_time: Optional[str] = None,
                       level: Optional[str] = None) -> List[Dict]:
        """
        获取系统日志
        
        Args:
            start_time: 开始时间
            end_time: 结束时间
            level: 日志级别
            
        Returns:
            List[Dict]: 日志列表
        """
        try:
            logs = []
            with open(self.log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        # 解析日志行
                        parts = line.split(' - ')
                        if len(parts) >= 4:
                            timestamp = parts[0]
                            name = parts[1]
                            log_level = parts[2]
                            message = ' - '.join(parts[3:]).strip()
                            
                            # 过滤条件
                            if start_time and timestamp < start_time:
                                continue
                            if end_time and timestamp > end_time:
                                continue
                            if level and log_level != level:
                                continue
                                
                            logs.append({
                                'timestamp': timestamp,
                                'name': name,
                                'level': log_level,
                                'message': message
                            })
                    except:
                        continue
                        
            return logs
            
        except Exception as e:
            self.logger.error(f"获取系统日志失败: {str(e)}")
            raise
            
    def clear_system_logs(self) -> None:
        """清理系统日志"""
        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                f.write('')
            self.logger.info("系统日志已清理")
        except Exception as e:
            self.logger.error(f"清理系统日志失败: {str(e)}")
            raise
            
    def backup_system(self, backup_path: str) -> str:
        """
        备份系统
        
        Args:
            backup_path: 备份路径
            
        Returns:
            str: 备份文件路径
        """
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = os.path.join(backup_path, f'system_backup_{timestamp}.zip')
            
            # 确保备份目录存在
            os.makedirs(backup_path, exist_ok=True)
            
            # 创建备份
            shutil.make_archive(
                backup_file[:-4],  # 移除.zip后缀
                'zip',
                self.config_path
            )
            
            self.logger.info(f"系统备份成功: {backup_file}")
            return backup_file
            
        except Exception as e:
            self.logger.error(f"系统备份失败: {str(e)}")
            raise
            
    def restore_system(self, backup_file: str) -> None:
        """
        恢复系统
        
        Args:
            backup_file: 备份文件路径
        """
        try:
            # 解压备份文件
            shutil.unpack_archive(backup_file, self.config_path, 'zip')
            
            self.logger.info(f"系统恢复成功: {backup_file}")
            
        except Exception as e:
            self.logger.error(f"系统恢复失败: {str(e)}")
            raise 