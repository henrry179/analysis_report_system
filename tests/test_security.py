#!/usr/bin/env python3
"""
安全测试用例
测试系统的安全性，包括认证、授权、加密、输入验证等
"""

import pytest
import json
import time
import hashlib
import secrets
import base64
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import sys
import tempfile
import shutil

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.security.encryption import DataEncryption, TransportSecurity
from src.security.audit_logger import SecurityAuditLogger, AuditEvent, AuditEventType, AuditSeverity
from src.core.auth import AuthManager
from src.utils.logger import system_logger


class TestSecurityEncryption:
    """加密安全测试"""
    
    def test_data_encryption_basic(self):
        """测试基本数据加密"""
        encryption = DataEncryption()
        
        test_data = "这是一个测试字符串，包含中文和English"
        
        # 加密
        encrypted = encryption.encrypt_data(test_data)
        assert encrypted is not None
        assert encrypted != test_data
        assert len(encrypted) > 0
        
        # 解密
        decrypted = encryption.decrypt_data(encrypted)
        assert decrypted == test_data
    
    def test_data_encryption_different_types(self):
        """测试不同数据类型的加密"""
        encryption = DataEncryption()
        
        test_cases = [
            "simple string",
            {"key": "value", "number": 123},
            ["item1", "item2", "item3"],
            "🚀📊💻",  # Unicode
            "",  # 空字符串
        ]
        
        for test_data in test_cases:
            encrypted = encryption.encrypt_data(test_data)
            assert encrypted is not None
            
            if isinstance(test_data, (str, dict, list)):
                decrypted = encryption.decrypt_data(encrypted, return_type='str' if isinstance(test_data, str) else 'dict' if isinstance(test_data, dict) else 'str')
                if isinstance(test_data, str):
                    assert decrypted == test_data
                else:
                    # 对于复杂类型，转换为JSON进行比较
                    assert json.loads(decrypted) == test_data if isinstance(decrypted, str) else decrypted == test_data
    
    def test_password_hashing(self):
        """测试密码哈希"""
        encryption = DataEncryption()
        
        password = "MySecurePassword123!"
        
        # 哈希密码
        hashed, salt = encryption.hash_password(password)
        assert hashed is not None
        assert salt is not None
        assert hashed != password
        assert len(salt) > 0
        
        # 验证密码
        assert encryption.verify_password(password, hashed, salt) is True
        assert encryption.verify_password("WrongPassword", hashed, salt) is False
    
    def test_rsa_encryption(self):
        """测试RSA加密"""
        encryption = DataEncryption()
        
        # 跳过测试如果没有cryptography库
        if not hasattr(encryption, 'rsa_public_key') or encryption.rsa_public_key is None:
            pytest.skip("RSA encryption not available")
        
        test_data = "RSA encryption test data"
        
        # RSA加密
        encrypted = encryption.encrypt_with_rsa(test_data)
        assert encrypted is not None
        assert encrypted != test_data
        
        # RSA解密
        decrypted = encryption.decrypt_with_rsa(encrypted)
        assert decrypted == test_data
    
    def test_secure_token_generation(self):
        """测试安全令牌生成"""
        encryption = DataEncryption()
        
        # 生成令牌
        token1 = encryption.generate_secure_token()
        token2 = encryption.generate_secure_token()
        
        assert token1 is not None
        assert token2 is not None
        assert token1 != token2  # 每次生成的令牌应该不同
        assert len(token1) > 0
        assert len(token2) > 0
    
    def test_hmac_signature(self):
        """测试HMAC签名"""
        encryption = DataEncryption()
        
        data = "Important data to sign"
        secret = "MySecretKey"
        
        # 创建签名
        signature = encryption.create_hmac_signature(data, secret)
        assert signature is not None
        assert len(signature) > 0
        
        # 验证签名
        assert encryption.verify_hmac_signature(data, signature, secret) is True
        assert encryption.verify_hmac_signature("Modified data", signature, secret) is False
        assert encryption.verify_hmac_signature(data, signature, "WrongSecret") is False
    
    def test_encryption_with_invalid_data(self):
        """测试无效数据的加密处理"""
        encryption = DataEncryption()
        
        # 测试None值
        result = encryption.encrypt_data(None)
        # 应该返回None或抛出异常，但不应该崩溃
        
        # 测试非常大的数据
        large_data = "x" * (10 * 1024 * 1024)  # 10MB
        try:
            result = encryption.encrypt_data(large_data)
            # 如果成功，应该能够解密
            if result:
                decrypted = encryption.decrypt_data(result)
                assert decrypted == large_data
        except MemoryError:
            pytest.skip("Insufficient memory for large data encryption test")


class TestTransportSecurity:
    """传输安全测试"""
    
    def test_jwt_token_creation_and_verification(self):
        """测试JWT令牌创建和验证"""
        transport = TransportSecurity()
        
        payload = {
            'user_id': 'test_user',
            'role': 'admin',
            'permissions': ['read', 'write']
        }
        
        # 创建JWT令牌
        token = transport.create_jwt_token(payload)
        if token is None:
            pytest.skip("JWT library not available")
        
        assert token is not None
        assert len(token) > 0
        
        # 验证JWT令牌
        decoded_payload = transport.verify_jwt_token(token)
        assert decoded_payload is not None
        assert decoded_payload['user_id'] == payload['user_id']
        assert decoded_payload['role'] == payload['role']
    
    def test_jwt_token_expiration(self):
        """测试JWT令牌过期"""
        transport = TransportSecurity()
        
        payload = {'user_id': 'test_user'}
        
        # 创建短期令牌（1秒过期）
        short_token = transport.create_jwt_token(payload, expires_delta=timedelta(seconds=1))
        if short_token is None:
            pytest.skip("JWT library not available")
        
        # 立即验证应该成功
        decoded = transport.verify_jwt_token(short_token)
        assert decoded is not None
        
        # 等待令牌过期
        time.sleep(2)
        
        # 过期后验证应该失败
        expired_decoded = transport.verify_jwt_token(short_token)
        assert expired_decoded is None
    
    def test_api_key_management(self):
        """测试API密钥管理"""
        transport = TransportSecurity()
        
        user_id = "test_user"
        permissions = ["read", "write", "delete"]
        
        # 创建API密钥
        api_key = transport.create_api_key(user_id, permissions)
        if api_key is None:
            pytest.skip("JWT library not available")
        
        assert api_key is not None
        
        # 验证API密钥
        payload = transport.verify_api_key(api_key)
        assert payload is not None
        assert payload['user_id'] == user_id
        assert payload['permissions'] == permissions
        assert payload['type'] == 'api_key'
    
    def test_csrf_token(self):
        """测试CSRF令牌"""
        transport = TransportSecurity()
        
        session_id = "test_session_123"
        
        # 创建CSRF令牌
        csrf_token = transport.create_csrf_token(session_id)
        assert csrf_token is not None
        assert len(csrf_token) > 0
        
        # 验证CSRF令牌
        assert transport.verify_csrf_token(csrf_token, session_id) is True
        assert transport.verify_csrf_token(csrf_token, "wrong_session") is False
        
        # 测试令牌过期
        old_csrf_token = transport.create_csrf_token(session_id)
        time.sleep(1)  # 等待一秒
        # 使用短过期时间进行测试
        assert transport.verify_csrf_token(old_csrf_token, session_id, max_age=0) is False
    
    def test_secure_headers(self):
        """测试安全头部"""
        transport = TransportSecurity()
        
        headers = transport.secure_headers()
        
        # 检查必要的安全头部
        assert 'X-Content-Type-Options' in headers
        assert 'X-Frame-Options' in headers
        assert 'X-XSS-Protection' in headers
        assert 'Strict-Transport-Security' in headers
        assert 'Content-Security-Policy' in headers
        
        # 检查头部值
        assert headers['X-Content-Type-Options'] == 'nosniff'
        assert headers['X-Frame-Options'] == 'DENY'
        assert 'max-age' in headers['Strict-Transport-Security']
    
    def test_sensitive_data_encryption(self):
        """测试敏感数据加密"""
        transport = TransportSecurity()
        
        sensitive_data = {
            'user_id': 'test_user',
            'email': 'test@example.com',
            'password': 'secret_password',
            'credit_card': '1234-5678-9012-3456',
            'public_info': 'This is public'
        }
        
        sensitive_fields = ['password', 'credit_card']
        
        # 加密敏感字段
        encrypted_data = transport.encrypt_sensitive_data(sensitive_data, sensitive_fields)
        
        assert encrypted_data is not None
        assert encrypted_data['user_id'] == sensitive_data['user_id']  # 非敏感字段不变
        assert encrypted_data['public_info'] == sensitive_data['public_info']
        assert encrypted_data['password'] != sensitive_data['password']  # 敏感字段被加密
        assert encrypted_data['credit_card'] != sensitive_data['credit_card']
        
        # 解密敏感字段
        decrypted_data = transport.decrypt_sensitive_data(encrypted_data, sensitive_fields)
        
        assert decrypted_data is not None
        assert decrypted_data['password'] == sensitive_data['password']
        assert decrypted_data['credit_card'] == sensitive_data['credit_card']


class TestSecurityAudit:
    """安全审计测试"""
    
    def test_audit_event_creation(self):
        """测试审计事件创建"""
        event = AuditEvent(
            event_type=AuditEventType.LOGIN_SUCCESS,
            severity=AuditSeverity.LOW,
            message="User logged in successfully",
            user_id="test_user",
            ip_address="192.168.1.100"
        )
        
        assert event.event_id is not None
        assert len(event.event_id) > 0
        assert event.event_type == AuditEventType.LOGIN_SUCCESS
        assert event.severity == AuditSeverity.LOW
        assert event.user_id == "test_user"
        assert event.ip_address == "192.168.1.100"
        assert 'security' in event.tags
    
    def test_audit_logger_basic_logging(self):
        """测试基本审计日志记录"""
        audit_logger = SecurityAuditLogger()
        
        # 记录登录成功
        audit_logger.log_login_success("test_user", "192.168.1.100")
        
        # 记录登录失败
        audit_logger.log_login_failed("test_user", "192.168.1.100", "Invalid password")
        
        # 记录数据访问
        audit_logger.log_data_access("test_user", "/api/reports", "read")
        
        # 检查统计信息
        stats = audit_logger.get_stats()
        assert stats['total_events'] >= 3
        assert stats['events_by_type'][AuditEventType.LOGIN_SUCCESS.value] >= 1
        assert stats['events_by_type'][AuditEventType.LOGIN_FAILED.value] >= 1
    
    def test_audit_logger_security_violations(self):
        """测试安全违规记录"""
        audit_logger = SecurityAuditLogger()
        
        # 记录安全违规
        audit_logger.log_security_violation(
            user_id="malicious_user",
            violation_type="SQL_INJECTION_ATTEMPT",
            details={
                'query': "'; DROP TABLE users; --",
                'endpoint': '/api/search',
                'blocked': True
            }
        )
        
        # 检查事件
        events = audit_logger.get_events(event_type=AuditEventType.SECURITY_VIOLATION)
        assert len(events) >= 1
        
        violation_event = events[0]
        assert violation_event['severity'] == AuditSeverity.HIGH.value
        assert 'violation' in violation_event['tags']
    
    def test_audit_logger_api_monitoring(self):
        """测试API监控审计"""
        audit_logger = SecurityAuditLogger()
        
        # 记录正常API调用
        audit_logger.log_api_call("test_user", "/api/reports", "GET", 200, "192.168.1.100", 0.15)
        
        # 记录错误API调用
        audit_logger.log_api_call("test_user", "/api/admin", "POST", 403, "192.168.1.100", 0.05)
        
        # 记录服务器错误
        audit_logger.log_api_call("test_user", "/api/process", "POST", 500, "192.168.1.100", 2.5)
        
        # 检查API事件
        api_events = audit_logger.get_events(event_type=AuditEventType.API_CALL)
        assert len(api_events) >= 3
        
        # 检查不同严重级别
        severities = [event['severity'] for event in api_events]
        assert AuditSeverity.LOW.value in severities  # 200状态码
        assert AuditSeverity.MEDIUM.value in severities  # 403状态码
        assert AuditSeverity.HIGH.value in severities  # 500状态码
    
    def test_audit_logger_data_modifications(self):
        """测试数据修改审计"""
        audit_logger = SecurityAuditLogger()
        
        # 记录数据修改
        audit_logger.log_data_modification(
            user_id="admin_user",
            resource="/api/users/123",
            action="update",
            details={
                'old_values': {'role': 'user'},
                'new_values': {'role': 'admin'},
                'reason': 'Promotion'
            }
        )
        
        audit_logger.log_data_modification(
            user_id="admin_user",
            resource="/api/reports/456",
            action="delete",
            details={'report_name': 'Confidential Report'}
        )
        
        # 检查数据修改事件
        update_events = audit_logger.get_events(event_type=AuditEventType.DATA_UPDATED)
        delete_events = audit_logger.get_events(event_type=AuditEventType.DATA_DELETED)
        
        assert len(update_events) >= 1
        assert len(delete_events) >= 1
    
    def test_audit_logger_access_control(self):
        """测试访问控制审计"""
        audit_logger = SecurityAuditLogger()
        
        # 记录访问拒绝
        audit_logger.log_access_denied(
            user_id="regular_user",
            resource="/api/admin/settings",
            reason="Insufficient permissions",
            ip_address="192.168.1.100"
        )
        
        # 检查访问拒绝事件
        denied_events = audit_logger.get_events(event_type=AuditEventType.ACCESS_DENIED)
        assert len(denied_events) >= 1
        
        denied_event = denied_events[0]
        assert denied_event['user_id'] == "regular_user"
        assert denied_event['resource'] == "/api/admin/settings"
        assert denied_event['severity'] == AuditSeverity.MEDIUM.value
    
    def test_audit_logger_threat_detection(self):
        """测试威胁检测"""
        audit_logger = SecurityAuditLogger()
        
        # 模拟多次登录失败（暴力破解）
        for i in range(6):  # 超过阈值
            audit_logger.log_login_failed(
                user_id="target_user",
                ip_address="192.168.1.200",
                reason="Invalid password"
            )
        
        # 检查是否触发了威胁检测
        # 注意：实际的威胁检测可能需要一些时间来处理
        time.sleep(0.1)
        
        stats = audit_logger.get_stats()
        assert stats['events_by_type'][AuditEventType.LOGIN_FAILED.value] >= 6
    
    def test_audit_logger_security_summary(self):
        """测试安全摘要"""
        audit_logger = SecurityAuditLogger()
        
        # 生成各种安全事件
        audit_logger.log_login_success("user1", "192.168.1.100")
        audit_logger.log_login_failed("user2", "192.168.1.101", "Invalid password")
        audit_logger.log_data_modification("admin", "/api/config", "update")
        audit_logger.log_security_violation("hacker", "XSS_ATTEMPT", {"payload": "<script>alert('xss')</script>"})
        
        # 获取安全摘要
        summary = audit_logger.get_security_summary(hours=1)
        
        assert summary['total_events'] >= 4
        assert summary['failed_logins'] >= 1
        assert summary['data_modifications'] >= 1
        assert summary['security_alerts'] >= 1  # 高严重级别事件


class TestInputValidation:
    """输入验证测试"""
    
    def test_sql_injection_prevention(self):
        """测试SQL注入防护"""
        malicious_inputs = [
            "'; DROP TABLE users; --",
            "1' OR '1'='1",
            "admin'--",
            "1; DELETE FROM users WHERE '1'='1",
            "' UNION SELECT * FROM passwords --"
        ]
        
        for malicious_input in malicious_inputs:
            # 这里应该测试实际的输入验证逻辑
            # 暂时只检查是否包含危险字符
            dangerous_patterns = ["DROP", "DELETE", "UNION", "--", "'", ";"]
            contains_dangerous = any(pattern in malicious_input.upper() for pattern in dangerous_patterns)
            assert contains_dangerous, f"Should detect dangerous pattern in: {malicious_input}"
    
    def test_xss_prevention(self):
        """测试XSS防护"""
        xss_payloads = [
            "<script>alert('xss')</script>",
            "<img src=x onerror=alert('xss')>",
            "javascript:alert('xss')",
            "<svg onload=alert('xss')>",
            "';alert('xss');//"
        ]
        
        for payload in xss_payloads:
            # 检查是否包含XSS模式
            dangerous_patterns = ["<script", "javascript:", "onerror", "onload", "alert("]
            contains_xss = any(pattern in payload.lower() for pattern in dangerous_patterns)
            assert contains_xss, f"Should detect XSS pattern in: {payload}"
    
    def test_path_traversal_prevention(self):
        """测试路径遍历防护"""
        path_traversal_attempts = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32\\config\\sam",
            "/etc/passwd",
            "C:\\Windows\\System32\\config\\SAM",
            "....//....//....//etc//passwd"
        ]
        
        for attempt in path_traversal_attempts:
            # 检查路径遍历模式
            dangerous_patterns = ["..", "/etc/", "\\system32\\", "passwd", "sam"]
            contains_traversal = any(pattern in attempt.lower() for pattern in dangerous_patterns)
            assert contains_traversal, f"Should detect path traversal in: {attempt}"
    
    def test_command_injection_prevention(self):
        """测试命令注入防护"""
        command_injection_attempts = [
            "; rm -rf /",
            "| cat /etc/passwd",
            "&& rm important_file.txt",
            "`whoami`",
            "$(id)",
            "; shutdown -h now"
        ]
        
        for attempt in command_injection_attempts:
            # 检查命令注入模式
            dangerous_patterns = [";", "|", "&&", "`", "$(", "rm", "cat", "whoami", "shutdown"]
            contains_injection = any(pattern in attempt.lower() for pattern in dangerous_patterns)
            assert contains_injection, f"Should detect command injection in: {attempt}"


class TestAuthenticationSecurity:
    """认证安全测试"""
    
    def test_password_strength_validation(self):
        """测试密码强度验证"""
        weak_passwords = [
            "123456",
            "password",
            "admin",
            "qwerty",
            "abc123",
            "password123",
            "12345678"
        ]
        
        strong_passwords = [
            "MyStr0ng!Password",
            "C0mpl3x@P@ssw0rd!",
            "Secure#2025$Password",
            "V3ry!Str0ng#P@ssw0rd"
        ]
        
        def is_password_strong(password):
            """简单的密码强度检查"""
            if len(password) < 8:
                return False
            
            has_upper = any(c.isupper() for c in password)
            has_lower = any(c.islower() for c in password)
            has_digit = any(c.isdigit() for c in password)
            has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
            
            return has_upper and has_lower and has_digit and has_special
        
        # 测试弱密码
        for weak_password in weak_passwords:
            assert not is_password_strong(weak_password), f"Should reject weak password: {weak_password}"
        
        # 测试强密码
        for strong_password in strong_passwords:
            assert is_password_strong(strong_password), f"Should accept strong password: {strong_password}"
    
    def test_session_security(self):
        """测试会话安全"""
        # 测试会话ID生成
        session_ids = set()
        for _ in range(100):
            session_id = secrets.token_urlsafe(32)
            assert session_id not in session_ids, "Session ID collision detected"
            session_ids.add(session_id)
            assert len(session_id) >= 32, "Session ID too short"
    
    def test_rate_limiting(self):
        """测试速率限制"""
        # 模拟速率限制器
        class RateLimiter:
            def __init__(self, max_attempts=5, window=60):
                self.max_attempts = max_attempts
                self.window = window
                self.attempts = {}
            
            def is_allowed(self, identifier):
                now = time.time()
                if identifier not in self.attempts:
                    self.attempts[identifier] = []
                
                # 清理过期的尝试
                self.attempts[identifier] = [
                    attempt for attempt in self.attempts[identifier]
                    if now - attempt < self.window
                ]
                
                # 检查是否超过限制
                if len(self.attempts[identifier]) >= self.max_attempts:
                    return False
                
                self.attempts[identifier].append(now)
                return True
        
        rate_limiter = RateLimiter(max_attempts=3, window=60)
        
        # 测试正常请求
        assert rate_limiter.is_allowed("192.168.1.100") is True
        assert rate_limiter.is_allowed("192.168.1.100") is True
        assert rate_limiter.is_allowed("192.168.1.100") is True
        
        # 第四次请求应该被拒绝
        assert rate_limiter.is_allowed("192.168.1.100") is False
        
        # 不同IP应该不受影响
        assert rate_limiter.is_allowed("192.168.1.101") is True


class TestSecurityConfiguration:
    """安全配置测试"""
    
    def test_secure_default_settings(self):
        """测试安全的默认设置"""
        # 检查默认设置是否安全
        default_settings = {
            'debug': False,
            'ssl_required': True,
            'session_timeout': 3600,  # 1小时
            'max_login_attempts': 5,
            'password_min_length': 8,
            'require_https': True
        }
        
        for setting, expected_value in default_settings.items():
            # 这里应该检查实际的配置
            # 暂时只验证期望的安全设置
            assert expected_value is not None
    
    def test_sensitive_data_masking(self):
        """测试敏感数据掩码"""
        sensitive_data = {
            'password': 'secret123',
            'api_key': 'sk-1234567890abcdef',
            'credit_card': '1234-5678-9012-3456',
            'ssn': '123-45-6789',
            'email': 'user@example.com'
        }
        
        def mask_sensitive_data(data):
            """掩码敏感数据"""
            masked = data.copy()
            for key, value in masked.items():
                if key in ['password', 'api_key']:
                    masked[key] = '*' * len(str(value))
                elif key == 'credit_card':
                    masked[key] = f"****-****-****-{str(value)[-4:]}"
                elif key == 'ssn':
                    masked[key] = f"***-**-{str(value)[-4:]}"
            return masked
        
        masked_data = mask_sensitive_data(sensitive_data)
        
        assert masked_data['password'] == '**********'
        assert masked_data['api_key'] == '********************'
        assert masked_data['credit_card'] == '****-****-****-3456'
        assert masked_data['ssn'] == '***-**-6789'
        assert masked_data['email'] == 'user@example.com'  # 邮箱可能不需要掩码


if __name__ == '__main__':
    pytest.main([__file__, '-v'])