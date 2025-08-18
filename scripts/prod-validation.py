#!/usr/bin/env python3
"""
生产环境验证脚本
部署后运行关键功能验证测试
"""

import requests
import time
import sys
import json
from typing import Dict, List, Any
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ProductionValidator:
    """生产环境验证器"""
    
    def __init__(self, base_url: str = "https://analysis-system.example.com"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.timeout = 30
        self.results = []
    
    def run_validation(self) -> bool:
        """运行所有验证测试"""
        logger.info("🚀 开始生产环境验证...")
        
        tests = [
            ("健康检查", self.test_health_check),
            ("API信息", self.test_api_info),
            ("用户认证", self.test_authentication),
            ("报告生成", self.test_report_generation),
            ("数据处理", self.test_data_processing),
            ("WebSocket连接", self.test_websocket_connection),
            ("系统指标", self.test_system_metrics),
            ("安全头部", self.test_security_headers),
            ("响应时间", self.test_response_times),
            ("错误处理", self.test_error_handling),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            try:
                logger.info(f"🧪 运行测试: {test_name}")
                result = test_func()
                if result:
                    logger.info(f"✅ {test_name} - 通过")
                    passed += 1
                else:
                    logger.error(f"❌ {test_name} - 失败")
                self.results.append({"test": test_name, "passed": result})
            except Exception as e:
                logger.error(f"❌ {test_name} - 异常: {e}")
                self.results.append({"test": test_name, "passed": False, "error": str(e)})
        
        success_rate = (passed / total) * 100
        logger.info(f"📊 验证结果: {passed}/{total} 通过 ({success_rate:.1f}%)")
        
        # 生成报告
        self.generate_report()
        
        return success_rate >= 90  # 90%通过率认为验证成功
    
    def test_health_check(self) -> bool:
        """测试健康检查端点"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            return response.status_code == 200
        except Exception:
            return False
    
    def test_api_info(self) -> bool:
        """测试API信息端点"""
        try:
            response = self.session.get(f"{self.base_url}/api/info")
            if response.status_code != 200:
                return False
            
            data = response.json()
            required_fields = ['name', 'version', 'status']
            return all(field in data for field in required_fields)
        except Exception:
            return False
    
    def test_authentication(self) -> bool:
        """测试用户认证"""
        try:
            # 测试登录端点
            login_data = {
                "username": "admin",
                "password": "adminpass"
            }
            response = self.session.post(f"{self.base_url}/api/login", json=login_data)
            
            if response.status_code != 200:
                return False
            
            # 检查返回的token
            data = response.json()
            return 'token' in data or 'access_token' in data
        except Exception:
            return False
    
    def test_report_generation(self) -> bool:
        """测试报告生成"""
        try:
            # 获取报告列表
            response = self.session.get(f"{self.base_url}/api/reports")
            if response.status_code != 200:
                return False
            
            # 测试报告详情
            reports = response.json()
            if isinstance(reports, list) and len(reports) > 0:
                report_id = reports[0].get('id', 1)
                detail_response = self.session.get(f"{self.base_url}/api/reports/{report_id}")
                return detail_response.status_code in [200, 404]  # 存在或不存在都是正常的
            
            return True
        except Exception:
            return False
    
    def test_data_processing(self) -> bool:
        """测试数据处理功能"""
        try:
            # 测试数据上传端点
            test_data = {"test": "data", "items": [1, 2, 3]}
            response = self.session.post(f"{self.base_url}/api/data/process", json=test_data)
            
            # 接受200或其他合理的状态码
            return response.status_code in [200, 201, 202]
        except Exception:
            return False
    
    def test_websocket_connection(self) -> bool:
        """测试WebSocket连接"""
        try:
            # 简单的WebSocket连接测试
            # 这里只测试WebSocket端点是否可访问
            response = self.session.get(f"{self.base_url}/websocket-test")
            return response.status_code == 200
        except Exception:
            return False
    
    def test_system_metrics(self) -> bool:
        """测试系统指标端点"""
        try:
            response = self.session.get(f"{self.base_url}/metrics")
            # Prometheus格式或JSON格式都可以
            return response.status_code == 200
        except Exception:
            return False
    
    def test_security_headers(self) -> bool:
        """测试安全头部"""
        try:
            response = self.session.get(f"{self.base_url}/")
            headers = response.headers
            
            security_headers = [
                'X-Content-Type-Options',
                'X-Frame-Options', 
                'X-XSS-Protection',
                'Strict-Transport-Security'
            ]
            
            present_headers = sum(1 for header in security_headers if header in headers)
            return present_headers >= 2  # 至少要有2个安全头部
        except Exception:
            return False
    
    def test_response_times(self) -> bool:
        """测试响应时间"""
        try:
            start_time = time.time()
            response = self.session.get(f"{self.base_url}/api/info")
            response_time = time.time() - start_time
            
            return response.status_code == 200 and response_time < 5.0  # 5秒内响应
        except Exception:
            return False
    
    def test_error_handling(self) -> bool:
        """测试错误处理"""
        try:
            # 测试404错误
            response = self.session.get(f"{self.base_url}/api/nonexistent")
            if response.status_code != 404:
                return False
            
            # 测试错误响应格式
            try:
                error_data = response.json()
                return 'error' in error_data or 'message' in error_data
            except:
                return True  # 非JSON响应也是可以的
        except Exception:
            return False
    
    def generate_report(self):
        """生成验证报告"""
        report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "base_url": self.base_url,
            "total_tests": len(self.results),
            "passed_tests": sum(1 for r in self.results if r['passed']),
            "failed_tests": sum(1 for r in self.results if not r['passed']),
            "success_rate": (sum(1 for r in self.results if r['passed']) / len(self.results)) * 100,
            "results": self.results
        }
        
        # 保存报告到文件
        with open('production-validation-report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info("📋 验证报告已保存到 production-validation-report.json")


def main():
    """主函数"""
    import os
    
    base_url = os.getenv('PROD_BASE_URL', 'https://analysis-system.example.com')
    validator = ProductionValidator(base_url)
    
    success = validator.run_validation()
    
    if success:
        logger.info("🎉 生产环境验证通过!")
        sys.exit(0)
    else:
        logger.error("❌ 生产环境验证失败!")
        sys.exit(1)


if __name__ == "__main__":
    main()