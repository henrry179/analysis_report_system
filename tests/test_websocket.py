#!/usr/bin/env python3
"""
WebSocket实时进度推送功能测试脚本
"""

import asyncio
import websockets
import json
import requests
import sys
import time
from datetime import datetime

# 服务器配置
SERVER_URL = "localhost:8000"
WS_URL = f"ws://{SERVER_URL}/ws/admin"
API_BASE = f"http://{SERVER_URL}"

class WebSocketTester:
    def __init__(self):
        self.ws = None
        self.messages_received = []
        self.is_connected = False
        
    async def connect(self):
        """连接WebSocket"""
        try:
            print(f"🔗 正在连接WebSocket: {WS_URL}")
            self.ws = await websockets.connect(WS_URL)
            self.is_connected = True
            print("✅ WebSocket连接成功!")
            return True
        except Exception as e:
            print(f"❌ WebSocket连接失败: {e}")
            return False
    
    async def listen_for_messages(self):
        """监听WebSocket消息"""
        try:
            while self.is_connected:
                message = await self.ws.recv()
                data = json.loads(message)
                self.messages_received.append(data)
                
                timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                message_type = data.get("type", "unknown")
                status = data.get("status", "")
                
                print(f"📨 [{timestamp}] 收到消息: {message_type}")
                
                if message_type == "connection":
                    print(f"   🔗 连接状态: {status}")
                    print(f"   💬 消息: {data.get('message', '')}")
                    
                elif message_type == "batch_report_progress":
                    batch_id = data.get("batch_id", "")[:8]
                    progress = data.get("progress", 0)
                    total = data.get("total", 1)
                    message = data.get("message", "")
                    print(f"   📊 批量任务 {batch_id}: {progress}/{total} - {message}")
                    
                elif message_type == "data_import_progress":
                    import_id = data.get("import_id", "")[:8]
                    progress = data.get("progress", 0)
                    message = data.get("message", "")
                    print(f"   📥 数据导入 {import_id}: {progress}% - {message}")
                    
                elif message_type == "file_upload_progress":
                    filename = data.get("filename", "")
                    progress = data.get("progress", 0)
                    message = data.get("message", "")
                    print(f"   📁 文件上传 {filename}: {progress}% - {message}")
                    
                else:
                    print(f"   📄 内容: {json.dumps(data, indent=2, ensure_ascii=False)}")
                    
        except websockets.exceptions.ConnectionClosed:
            print("⚠️  WebSocket连接已关闭")
            self.is_connected = False
        except Exception as e:
            print(f"❌ 监听消息时出错: {e}")
            self.is_connected = False
    
    async def send_message(self, message):
        """发送WebSocket消息"""
        if self.ws and self.is_connected:
            await self.ws.send(json.dumps(message))
            print(f"📤 发送消息: {message}")
        else:
            print("❌ WebSocket未连接")
    
    async def close(self):
        """关闭WebSocket连接"""
        if self.ws:
            await self.ws.close()
            self.is_connected = False
            print("🔌 WebSocket连接已关闭")

def get_auth_token():
    """获取认证令牌"""
    try:
        response = requests.post(
            f"{API_BASE}/token",
            data={"username": "admin", "password": "adminpass"},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        if response.status_code == 200:
            token = response.json().get("access_token")
            print(f"✅ 获取认证令牌成功: {token}")
            return token
        else:
            print(f"❌ 获取认证令牌失败: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ 获取认证令牌出错: {e}")
        return None

def test_batch_report_api(token):
    """测试批量报告生成API"""
    try:
        print("\n🧪 测试批量报告生成API...")
        response = requests.post(
            f"{API_BASE}/api/reports/batch/generate",
            json={
                "report_ids": ["test_report_1", "test_report_2", "test_report_3"],
                "output_format": "pdf",
                "include_charts": True,
                "async_generation": True
            },
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            batch_id = result.get("batch_id")
            print(f"✅ 批量任务创建成功: {batch_id}")
            return batch_id
        else:
            print(f"❌ 批量任务创建失败: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ 测试批量报告API出错: {e}")
        return None

async def main():
    """主测试函数"""
    print("🚀 WebSocket实时进度推送功能测试")
    print("=" * 50)
    
    # 检查服务器状态
    try:
        response = requests.get(f"{API_BASE}/api/info", timeout=5)
        if response.status_code == 200:
            info = response.json()
            print(f"✅ 服务器状态正常: {info.get('title')} - {info.get('version')}")
        else:
            print(f"❌ 服务器状态异常: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ 无法连接到服务器: {e}")
        print("💡 请确保服务器正在运行: python scripts/start_server.py")
        return
    
    # 获取认证令牌
    token = get_auth_token()
    if not token:
        return
    
    # 创建WebSocket测试器
    tester = WebSocketTester()
    
    try:
        # 连接WebSocket
        if not await tester.connect():
            return
        
        # 启动消息监听任务
        listen_task = asyncio.create_task(tester.listen_for_messages())
        
        # 等待连接稳定
        await asyncio.sleep(1)
        
        # 测试ping/pong
        print("\n🏓 测试Ping/Pong...")
        await tester.send_message({"type": "ping"})
        await asyncio.sleep(1)
        
        # 测试订阅功能
        print("\n📡 测试事件订阅...")
        await tester.send_message({
            "type": "subscribe",
            "event_type": "batch_reports"
        })
        await asyncio.sleep(1)
        
        # 测试批量报告生成（会触发WebSocket进度推送）
        print("\n📊 测试批量报告生成...")
        batch_id = test_batch_report_api(token)
        if batch_id:
            print(f"⏱️  等待批量任务完成，batch_id: {batch_id}")
            # 等待足够的时间让任务完成
            await asyncio.sleep(5)
        
        # 等待一段时间观察消息
        print("\n⏳ 等待更多消息...")
        await asyncio.sleep(3)
        
        # 取消监听任务
        listen_task.cancel()
        
        # 总结
        print("\n📈 测试总结:")
        print(f"   📨 收到消息数量: {len(tester.messages_received)}")
        print(f"   🔗 连接状态: {'正常' if tester.is_connected else '已断开'}")
        
        # 显示消息类型统计
        message_types = {}
        for msg in tester.messages_received:
            msg_type = msg.get("type", "unknown")
            message_types[msg_type] = message_types.get(msg_type, 0) + 1
        
        print("   📊 消息类型统计:")
        for msg_type, count in message_types.items():
            print(f"      {msg_type}: {count}")
        
    except KeyboardInterrupt:
        print("\n🛑 用户中断测试")
    except Exception as e:
        print(f"\n❌ 测试过程中出错: {e}")
    finally:
        await tester.close()
        print("\n✅ WebSocket功能测试完成!")

if __name__ == "__main__":
    # 检查依赖
    try:
        import websockets
        import requests
    except ImportError as e:
        print(f"❌ 缺少必要依赖: {e}")
        print("💡 请安装: pip install websockets requests")
        sys.exit(1)
    
    # 运行测试
    asyncio.run(main()) 