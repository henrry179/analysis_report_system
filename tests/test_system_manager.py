import unittest
import os
import json
import jwt
from datetime import datetime, timedelta
from src.core.system_manager import SystemManager

class TestSystemManager(unittest.TestCase):
    def setUp(self):
        self.manager = SystemManager()
        self.test_user = {
            'username': 'testuser',
            'password': 'testpass',
            'role': 'user'
        }
        self.admin_user = {
            'username': 'admin',
            'password': 'adminpass',
            'role': 'admin'
        }
        
    def test_authenticate_user(self):
        # 测试用户认证
        # 创建测试用户
        self.manager.create_user(
            self.test_user['username'],
            self.test_user['password'],
            self.test_user['role']
        )
        
        # 测试有效认证
        token = self.manager.authenticate_user(
            self.test_user['username'],
            self.test_user['password']
        )
        self.assertIsNotNone(token)
        
        # 测试无效密码
        token = self.manager.authenticate_user(
            self.test_user['username'],
            'wrongpass'
        )
        self.assertIsNone(token)
        
        # 测试不存在的用户
        token = self.manager.authenticate_user(
            'nonexistent',
            'password'
        )
        self.assertIsNone(token)
        
    def test_verify_token(self):
        # 测试令牌验证
        # 创建测试用户
        self.manager.create_user(
            self.test_user['username'],
            self.test_user['password'],
            self.test_user['role']
        )
        
        # 获取有效令牌
        token = self.manager.authenticate_user(
            self.test_user['username'],
            self.test_user['password']
        )
        
        # 测试有效令牌
        user_info = self.manager.verify_token(token)
        self.assertIsNotNone(user_info)
        self.assertEqual(user_info['username'], self.test_user['username'])
        self.assertEqual(user_info['role'], self.test_user['role'])
        
        # 测试无效令牌
        user_info = self.manager.verify_token('invalid_token')
        self.assertIsNone(user_info)
        
        # 测试过期令牌
        expired_token = jwt.encode(
            {
                'username': self.test_user['username'],
                'role': self.test_user['role'],
                'exp': datetime.utcnow() - timedelta(hours=1)
            },
            self.manager.secret_key,
            algorithm='HS256'
        )
        user_info = self.manager.verify_token(expired_token)
        self.assertIsNone(user_info)
        
    def test_create_user(self):
        # 测试用户创建
        # 创建新用户
        success = self.manager.create_user(
            self.test_user['username'],
            self.test_user['password'],
            self.test_user['role']
        )
        self.assertTrue(success)
        
        # 验证用户数据
        with open(self.manager.users_file, 'r') as f:
            users = json.load(f)
            self.assertIn(self.test_user['username'], users)
            self.assertEqual(users[self.test_user['username']]['role'], self.test_user['role'])
            
        # 测试重复用户名
        success = self.manager.create_user(
            self.test_user['username'],
            'newpass',
            'user'
        )
        self.assertFalse(success)
        
    def test_delete_user(self):
        # 测试用户删除
        # 创建测试用户
        self.manager.create_user(
            self.test_user['username'],
            self.test_user['password'],
            self.test_user['role']
        )
        
        # 测试删除用户
        success = self.manager.delete_user(self.test_user['username'])
        self.assertTrue(success)
        
        # 验证用户已删除
        with open(self.manager.users_file, 'r') as f:
            users = json.load(f)
            self.assertNotIn(self.test_user['username'], users)
            
        # 测试删除不存在的用户
        success = self.manager.delete_user('nonexistent')
        self.assertFalse(success)
        
    def test_check_permission(self):
        # 测试权限检查
        # 创建测试用户和管理员
        self.manager.create_user(
            self.test_user['username'],
            self.test_user['password'],
            self.test_user['role']
        )
        self.manager.create_user(
            self.admin_user['username'],
            self.admin_user['password'],
            self.admin_user['role']
        )
        
        # 获取令牌
        user_token = self.manager.authenticate_user(
            self.test_user['username'],
            self.test_user['password']
        )
        admin_token = self.manager.authenticate_user(
            self.admin_user['username'],
            self.admin_user['password']
        )
        
        # 测试用户权限
        self.assertTrue(self.manager.check_permission(user_token, 'read'))
        self.assertFalse(self.manager.check_permission(user_token, 'admin'))
        
        # 测试管理员权限
        self.assertTrue(self.manager.check_permission(admin_token, 'read'))
        self.assertTrue(self.manager.check_permission(admin_token, 'admin'))
        
        # 测试无效令牌
        self.assertFalse(self.manager.check_permission('invalid_token', 'read'))
        
    def test_get_system_logs(self):
        # 测试获取系统日志
        logs = self.manager.get_system_logs()
        self.assertIsInstance(logs, list)
        
    def test_clear_system_logs(self):
        # 测试清理系统日志
        success = self.manager.clear_system_logs()
        self.assertTrue(success)
        
        # 验证日志已清理
        logs = self.manager.get_system_logs()
        self.assertEqual(len(logs), 0)
        
    def test_backup_system(self):
        # 测试系统备份
        backup_path = self.manager.backup_system()
        
        # 验证备份文件
        self.assertTrue(os.path.exists(backup_path))
        self.assertTrue(backup_path.endswith('.zip'))
        
    def test_restore_system(self):
        # 测试系统恢复
        # 创建备份
        backup_path = self.manager.backup_system()
        
        # 修改一些数据
        self.manager.create_user(
            self.test_user['username'],
            self.test_user['password'],
            self.test_user['role']
        )
        
        # 恢复系统
        success = self.manager.restore_system(backup_path)
        self.assertTrue(success)
        
        # 验证数据已恢复
        with open(self.manager.users_file, 'r') as f:
            users = json.load(f)
            self.assertNotIn(self.test_user['username'], users)
            
    def tearDown(self):
        # 清理测试文件
        if os.path.exists(self.manager.users_file):
            os.remove(self.manager.users_file)
        if os.path.exists(self.manager.log_file):
            os.remove(self.manager.log_file)
            
if __name__ == '__main__':
    unittest.main() 