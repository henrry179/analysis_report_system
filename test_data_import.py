#!/usr/bin/env python3
"""
数据导入WebSocket进度推送测试脚本
"""

import asyncio
import websockets
import json
import requests
import tempfile
import csv
from datetime import datetime

# 服务器配置
SERVER_URL = "localhost:8000"
WS_URL = f"ws://{SERVER_URL}/ws/admin"
API_BASE = f"http://{SERVER_URL}"

async def test_data_import_with_websocket():
    """测试数据导入的WebSocket进度推送"""
    print("🚀 数据导入WebSocket进度推送测试")
    print("=" * 50)
    
    # 获取认证令牌
    try:
        response = requests.post(
            f"{API_BASE}/token",
            data={"username": "admin", "password": "adminpass"},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        if response.status_code == 200:
            token = response.json().get("access_token")
            print(f"✅ 获取认证令牌成功: {token}")
        else:
            print(f"❌ 获取认证令牌失败: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ 获取认证令牌出错: {e}")
        return
    
    # 创建测试CSV文件
    test_data = [
        ["date", "category", "region", "gmv", "dau", "order_price", "conversion_rate"],
        ["2024-05-01", "肉禽蛋类", "华东一区", 100000, 5000, 150.5, 3.2],
        ["2024-05-02", "水产类", "华东二区", 120000, 5500, 160.2, 3.5],
        ["2024-05-03", "猪肉类", "华东三区", 95000, 4800, 145.8, 3.1],
        ["2024-05-04", "冷藏加工", "华东一区", 110000, 5200, 155.3, 3.4],
        ["2024-05-05", "蔬菜类", "华东二区", 85000, 4500, 140.1, 2.9]
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        writer = csv.writer(f)
        writer.writerows(test_data)
        csv_file_path = f.name
    
    print(f"📄 创建测试CSV文件: {csv_file_path}")
    
    # 连接WebSocket
    try:
        print(f"🔗 连接WebSocket: {WS_URL}")
        async with websockets.connect(WS_URL) as websocket:
            # 启动消息监听
            async def listen_for_messages():
                while True:
                    try:
                        message = await websocket.recv()
                        data = json.loads(message)
                        
                        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                        message_type = data.get("type", "unknown")
                        
                        print(f"📨 [{timestamp}] {message_type}")
                        
                        if message_type == "data_import_progress":
                            import_id = data.get("import_id", "")[:8]
                            progress = data.get("progress", 0)
                            message = data.get("message", "")
                            status = data.get("status", "")
                            print(f"   📥 导入任务 {import_id}: {progress}% - {status} - {message}")
                            
                        elif message_type == "file_upload_progress":
                            filename = data.get("filename", "")
                            progress = data.get("progress", 0)
                            message = data.get("message", "")
                            status = data.get("status", "")
                            print(f"   📁 文件上传 {filename}: {progress}% - {status} - {message}")
                            
                        else:
                            print(f"   💬 {data.get('message', '')}")
                            
                    except websockets.exceptions.ConnectionClosed:
                        break
                    except Exception as e:
                        print(f"❌ 监听消息错误: {e}")
                        break
            
            # 启动监听任务
            listen_task = asyncio.create_task(listen_for_messages())
            
            # 等待连接稳定
            await asyncio.sleep(1)
            
            print("\n📤 测试数据导入API...")
            
            # 使用API导入数据
            try:
                with open(csv_file_path, 'rb') as f:
                    files = {'file': ('test_data.csv', f, 'text/csv')}
                    data = {'data_type': 'sales'}
                    headers = {'Authorization': f'Bearer {token}'}
                    
                    response = requests.post(
                        f"{API_BASE}/api/data/upload",
                        files=files,
                        data=data,
                        headers=headers
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        import_id = result.get("import_id")
                        print(f"✅ 数据导入请求成功: {import_id}")
                    else:
                        print(f"❌ 数据导入请求失败: {response.status_code} - {response.text}")
                        
            except Exception as e:
                print(f"❌ 数据导入API调用失败: {e}")
            
            # 等待导入完成
            print("\n⏳ 等待导入进度推送...")
            await asyncio.sleep(8)
            
            # 取消监听任务
            listen_task.cancel()
            
    except Exception as e:
        print(f"❌ WebSocket连接失败: {e}")
    
    # 清理临时文件
    import os
    try:
        os.unlink(csv_file_path)
        print(f"🗑️  清理临时文件: {csv_file_path}")
    except:
        pass
    
    print("\n✅ 数据导入WebSocket测试完成!")

if __name__ == "__main__":
    try:
        import websockets
        import requests
    except ImportError as e:
        print(f"❌ 缺少必要依赖: {e}")
        print("💡 请安装: pip install websockets requests")
        exit(1)
    
    asyncio.run(test_data_import_with_websocket()) 