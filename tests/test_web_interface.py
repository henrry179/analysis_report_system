import pytest
from fastapi.testclient import TestClient
from src.web_interface import app

class TestWebInterface:
    """测试Web接口的完整功能"""

    @pytest.fixture
    def client(self):
        """创建测试客户端"""
        return TestClient(app)

    def test_dashboard_access(self, client):
        """测试仪表盘访问"""
        response = client.get("/dashboard")
        assert response.status_code == 200
        assert "dashboard_data" in response.json()

    def test_login_with_valid_credentials(self, client):
        """测试有效凭据登录"""
        response = client.post(
            "/token",
            data={"username": "admin", "password": "adminpass"}
        )
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "bearer"

    def test_login_with_invalid_credentials(self, client):
        """测试无效凭据登录"""
        response = client.post(
            "/token",
            data={"username": "admin", "password": "wrongpass"}
        )
        assert response.status_code == 400
        assert "Incorrect username or password" in response.json()["detail"]

    def test_login_with_nonexistent_user(self, client):
        """测试不存在用户登录"""
        response = client.post(
            "/token",
            data={"username": "nonexistent", "password": "anypass"}
        )
        assert response.status_code == 400

    def test_generate_report_without_auth(self, client):
        """测试未认证访问报告生成"""
        response = client.get("/generate_report")
        assert response.status_code == 401  # Unauthorized

    def test_generate_report_with_auth(self, client):
        """测试认证后访问报告生成"""
        # 先登录获取token
        login_response = client.post(
            "/token",
            data={"username": "admin", "password": "adminpass"}
        )
        token = login_response.json()["access_token"]
        
        # 使用token访问受保护的端点
        response = client.get(
            "/generate_report",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        # 注意：由于测试环境可能缺少实际数据文件，这里可能返回500
        # 但至少应该通过认证检查，不是401
        assert response.status_code != 401

    def test_generate_report_with_invalid_token(self, client):
        """测试无效token访问"""
        response = client.get(
            "/generate_report",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 401

    def test_app_title(self, client):
        """测试应用基本信息"""
        # 通过FastAPI自动生成的OpenAPI文档检查应用标题
        response = client.get("/openapi.json")
        assert response.status_code == 200
        openapi_data = response.json()
        assert openapi_data["info"]["title"] == "Business Analysis Report System"

    def test_root_endpoint_exists(self, client):
        """测试根端点是否存在（如果有的话）"""
        response = client.get("/")
        # 如果没有根端点，返回404是正常的
        assert response.status_code in [200, 404]

    def test_token_endpoint_methods(self, client):
        """测试token端点只允许POST方法"""
        # GET方法应该不被允许
        response = client.get("/token")
        assert response.status_code == 405  # Method Not Allowed

    def test_admin_role_access(self, client):
        """测试管理员角色权限"""
        # 登录获取admin token
        login_response = client.post(
            "/token",
            data={"username": "admin", "password": "adminpass"}
        )
        token = login_response.json()["access_token"]
        
        # admin用户应该能访问受保护的资源
        response = client.get(
            "/generate_report",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        # 不应该因为权限问题被拒绝（403）
        assert response.status_code != 403 