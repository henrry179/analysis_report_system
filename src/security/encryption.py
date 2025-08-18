#!/usr/bin/env python3
"""
数据加密和传输安全模块
提供数据加密、解密、签名验证等安全功能
"""

import os
import base64
import hashlib
import hmac
import secrets
from typing import Dict, Any, Optional, Union, Tuple
from datetime import datetime, timedelta
import json

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa, padding
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    CRYPTOGRAPHY_AVAILABLE = True
except ImportError:
    CRYPTOGRAPHY_AVAILABLE = False

try:
    import jwt
    JWT_AVAILABLE = True
except ImportError:
    JWT_AVAILABLE = False

from src.utils.logger import system_logger
from src.config.settings import settings


class DataEncryption:
    """数据加密类"""
    
    def __init__(self, master_key: Optional[str] = None):
        self.master_key = master_key or self._get_master_key()
        self.fernet = None
        self.rsa_private_key = None
        self.rsa_public_key = None
        
        if CRYPTOGRAPHY_AVAILABLE:
            self._setup_symmetric_encryption()
            self._setup_asymmetric_encryption()
    
    def _get_master_key(self) -> str:
        """获取主密钥"""
        # 从环境变量或配置文件获取
        master_key = getattr(settings, 'ENCRYPTION_MASTER_KEY', None)
        if not master_key:
            master_key = os.environ.get('ENCRYPTION_MASTER_KEY')
        
        if not master_key:
            # 生成新的主密钥（开发环境）
            master_key = base64.urlsafe_b64encode(os.urandom(32)).decode()
            system_logger.warning("Generated new master key for development. Set ENCRYPTION_MASTER_KEY in production!")
        
        return master_key
    
    def _setup_symmetric_encryption(self):
        """设置对称加密"""
        if not CRYPTOGRAPHY_AVAILABLE:
            return
        
        try:
            # 使用主密钥派生Fernet密钥
            key_bytes = self.master_key.encode()
            if len(key_bytes) != 44:  # Fernet需要44字节的base64编码密钥
                # 使用PBKDF2派生密钥
                kdf = PBKDF2HMAC(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=b'analysis_report_system_salt',
                    iterations=100000,
                )
                key = base64.urlsafe_b64encode(kdf.derive(key_bytes))
            else:
                key = key_bytes
            
            self.fernet = Fernet(key)
            system_logger.info("Symmetric encryption initialized")
            
        except Exception as e:
            system_logger.error(f"Failed to setup symmetric encryption: {e}")
    
    def _setup_asymmetric_encryption(self):
        """设置非对称加密"""
        if not CRYPTOGRAPHY_AVAILABLE:
            return
        
        try:
            # 检查是否已有密钥文件
            private_key_path = getattr(settings, 'RSA_PRIVATE_KEY_PATH', 'keys/private_key.pem')
            public_key_path = getattr(settings, 'RSA_PUBLIC_KEY_PATH', 'keys/public_key.pem')
            
            if os.path.exists(private_key_path) and os.path.exists(public_key_path):
                # 加载现有密钥
                with open(private_key_path, 'rb') as f:
                    self.rsa_private_key = serialization.load_pem_private_key(
                        f.read(),
                        password=None
                    )
                
                with open(public_key_path, 'rb') as f:
                    self.rsa_public_key = serialization.load_pem_public_key(f.read())
                
                system_logger.info("Loaded existing RSA keys")
            else:
                # 生成新密钥对
                self._generate_rsa_keys(private_key_path, public_key_path)
                
        except Exception as e:
            system_logger.error(f"Failed to setup asymmetric encryption: {e}")
    
    def _generate_rsa_keys(self, private_key_path: str, public_key_path: str):
        """生成RSA密钥对"""
        try:
            # 创建目录
            os.makedirs(os.path.dirname(private_key_path), exist_ok=True)
            
            # 生成私钥
            self.rsa_private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048
            )
            
            # 获取公钥
            self.rsa_public_key = self.rsa_private_key.public_key()
            
            # 保存私钥
            private_pem = self.rsa_private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
            
            with open(private_key_path, 'wb') as f:
                f.write(private_pem)
            
            # 保存公钥
            public_pem = self.rsa_public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            
            with open(public_key_path, 'wb') as f:
                f.write(public_pem)
            
            system_logger.info("Generated new RSA key pair")
            
        except Exception as e:
            system_logger.error(f"Failed to generate RSA keys: {e}")
    
    def encrypt_data(self, data: Union[str, bytes, Dict[str, Any]]) -> Optional[str]:
        """加密数据"""
        if not self.fernet:
            system_logger.error("Symmetric encryption not available")
            return None
        
        try:
            # 转换数据为字节
            if isinstance(data, dict):
                data_bytes = json.dumps(data, ensure_ascii=False).encode('utf-8')
            elif isinstance(data, str):
                data_bytes = data.encode('utf-8')
            else:
                data_bytes = data
            
            # 加密
            encrypted_data = self.fernet.encrypt(data_bytes)
            return base64.urlsafe_b64encode(encrypted_data).decode('utf-8')
            
        except Exception as e:
            system_logger.error(f"Failed to encrypt data: {e}")
            return None
    
    def decrypt_data(self, encrypted_data: str, return_type: str = 'str') -> Optional[Union[str, bytes, Dict[str, Any]]]:
        """解密数据"""
        if not self.fernet:
            system_logger.error("Symmetric encryption not available")
            return None
        
        try:
            # 解码base64
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode('utf-8'))
            
            # 解密
            decrypted_bytes = self.fernet.decrypt(encrypted_bytes)
            
            # 根据返回类型转换
            if return_type == 'bytes':
                return decrypted_bytes
            elif return_type == 'dict':
                return json.loads(decrypted_bytes.decode('utf-8'))
            else:
                return decrypted_bytes.decode('utf-8')
                
        except Exception as e:
            system_logger.error(f"Failed to decrypt data: {e}")
            return None
    
    def encrypt_with_rsa(self, data: Union[str, bytes]) -> Optional[str]:
        """使用RSA加密数据"""
        if not self.rsa_public_key:
            system_logger.error("RSA public key not available")
            return None
        
        try:
            if isinstance(data, str):
                data = data.encode('utf-8')
            
            # RSA加密
            encrypted_data = self.rsa_public_key.encrypt(
                data,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            
            return base64.urlsafe_b64encode(encrypted_data).decode('utf-8')
            
        except Exception as e:
            system_logger.error(f"Failed to encrypt with RSA: {e}")
            return None
    
    def decrypt_with_rsa(self, encrypted_data: str) -> Optional[str]:
        """使用RSA解密数据"""
        if not self.rsa_private_key:
            system_logger.error("RSA private key not available")
            return None
        
        try:
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode('utf-8'))
            
            # RSA解密
            decrypted_data = self.rsa_private_key.decrypt(
                encrypted_bytes,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            
            return decrypted_data.decode('utf-8')
            
        except Exception as e:
            system_logger.error(f"Failed to decrypt with RSA: {e}")
            return None
    
    def hash_password(self, password: str, salt: Optional[str] = None) -> Tuple[str, str]:
        """哈希密码"""
        if not salt:
            salt = secrets.token_urlsafe(32)
        
        # 使用PBKDF2
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt.encode('utf-8'),
            iterations=100000,
        )
        
        key = kdf.derive(password.encode('utf-8'))
        hashed = base64.urlsafe_b64encode(key).decode('utf-8')
        
        return hashed, salt
    
    def verify_password(self, password: str, hashed: str, salt: str) -> bool:
        """验证密码"""
        try:
            new_hashed, _ = self.hash_password(password, salt)
            return hmac.compare_digest(hashed, new_hashed)
        except Exception as e:
            system_logger.error(f"Failed to verify password: {e}")
            return False
    
    def generate_secure_token(self, length: int = 32) -> str:
        """生成安全令牌"""
        return secrets.token_urlsafe(length)
    
    def create_hmac_signature(self, data: str, secret: str) -> str:
        """创建HMAC签名"""
        signature = hmac.new(
            secret.encode('utf-8'),
            data.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def verify_hmac_signature(self, data: str, signature: str, secret: str) -> bool:
        """验证HMAC签名"""
        expected_signature = self.create_hmac_signature(data, secret)
        return hmac.compare_digest(signature, expected_signature)


class TransportSecurity:
    """传输安全类"""
    
    def __init__(self, secret_key: Optional[str] = None):
        self.secret_key = secret_key or self._get_secret_key()
        self.jwt_algorithm = 'HS256'
        self.token_expiry = timedelta(hours=24)
    
    def _get_secret_key(self) -> str:
        """获取密钥"""
        secret_key = getattr(settings, 'JWT_SECRET_KEY', None)
        if not secret_key:
            secret_key = os.environ.get('JWT_SECRET_KEY')
        
        if not secret_key:
            secret_key = secrets.token_urlsafe(64)
            system_logger.warning("Generated new JWT secret key for development. Set JWT_SECRET_KEY in production!")
        
        return secret_key
    
    def create_jwt_token(self, payload: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> Optional[str]:
        """创建JWT令牌"""
        if not JWT_AVAILABLE:
            system_logger.error("JWT library not available")
            return None
        
        try:
            # 设置过期时间
            expire = datetime.utcnow() + (expires_delta or self.token_expiry)
            
            # 添加标准字段
            payload.update({
                'exp': expire,
                'iat': datetime.utcnow(),
                'iss': 'analysis-report-system'
            })
            
            # 生成令牌
            token = jwt.encode(payload, self.secret_key, algorithm=self.jwt_algorithm)
            return token
            
        except Exception as e:
            system_logger.error(f"Failed to create JWT token: {e}")
            return None
    
    def verify_jwt_token(self, token: str) -> Optional[Dict[str, Any]]:
        """验证JWT令牌"""
        if not JWT_AVAILABLE:
            system_logger.error("JWT library not available")
            return None
        
        try:
            payload = jwt.decode(
                token, 
                self.secret_key, 
                algorithms=[self.jwt_algorithm],
                options={'verify_exp': True}
            )
            return payload
            
        except jwt.ExpiredSignatureError:
            system_logger.warning("JWT token has expired")
            return None
        except jwt.InvalidTokenError as e:
            system_logger.warning(f"Invalid JWT token: {e}")
            return None
        except Exception as e:
            system_logger.error(f"Failed to verify JWT token: {e}")
            return None
    
    def create_api_key(self, user_id: str, permissions: List[str]) -> str:
        """创建API密钥"""
        payload = {
            'user_id': user_id,
            'permissions': permissions,
            'type': 'api_key'
        }
        
        # API密钥不设置过期时间
        token = self.create_jwt_token(payload, expires_delta=timedelta(days=365))
        return token
    
    def verify_api_key(self, api_key: str) -> Optional[Dict[str, Any]]:
        """验证API密钥"""
        payload = self.verify_jwt_token(api_key)
        
        if payload and payload.get('type') == 'api_key':
            return payload
        
        return None
    
    def encrypt_sensitive_data(self, data: Dict[str, Any], fields: List[str]) -> Dict[str, Any]:
        """加密敏感数据字段"""
        encryption = DataEncryption()
        encrypted_data = data.copy()
        
        for field in fields:
            if field in encrypted_data:
                original_value = encrypted_data[field]
                encrypted_value = encryption.encrypt_data(str(original_value))
                if encrypted_value:
                    encrypted_data[field] = encrypted_value
                    encrypted_data[f'{field}_encrypted'] = True
        
        return encrypted_data
    
    def decrypt_sensitive_data(self, data: Dict[str, Any], fields: List[str]) -> Dict[str, Any]:
        """解密敏感数据字段"""
        encryption = DataEncryption()
        decrypted_data = data.copy()
        
        for field in fields:
            if field in decrypted_data and decrypted_data.get(f'{field}_encrypted'):
                encrypted_value = decrypted_data[field]
                decrypted_value = encryption.decrypt_data(encrypted_value)
                if decrypted_value:
                    decrypted_data[field] = decrypted_value
                    decrypted_data.pop(f'{field}_encrypted', None)
        
        return decrypted_data
    
    def create_csrf_token(self, session_id: str) -> str:
        """创建CSRF令牌"""
        timestamp = str(int(datetime.utcnow().timestamp()))
        data = f"{session_id}:{timestamp}"
        
        signature = hmac.new(
            self.secret_key.encode('utf-8'),
            data.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return f"{timestamp}.{signature}"
    
    def verify_csrf_token(self, token: str, session_id: str, max_age: int = 3600) -> bool:
        """验证CSRF令牌"""
        try:
            timestamp_str, signature = token.split('.', 1)
            timestamp = int(timestamp_str)
            
            # 检查时间戳
            current_time = int(datetime.utcnow().timestamp())
            if current_time - timestamp > max_age:
                return False
            
            # 验证签名
            data = f"{session_id}:{timestamp_str}"
            expected_signature = hmac.new(
                self.secret_key.encode('utf-8'),
                data.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            return hmac.compare_digest(signature, expected_signature)
            
        except Exception as e:
            system_logger.error(f"Failed to verify CSRF token: {e}")
            return False
    
    def secure_headers(self) -> Dict[str, str]:
        """生成安全头部"""
        return {
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'X-XSS-Protection': '1; mode=block',
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
            'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'",
            'Referrer-Policy': 'strict-origin-when-cross-origin',
            'Permissions-Policy': 'geolocation=(), microphone=(), camera=()'
        }


# 全局加密实例
data_encryption = DataEncryption()
transport_security = TransportSecurity()

def get_data_encryption() -> DataEncryption:
    """获取数据加密实例"""
    return data_encryption

def get_transport_security() -> TransportSecurity:
    """获取传输安全实例"""
    return transport_security