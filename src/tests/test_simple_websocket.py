#!/usr/bin/env python3
"""
简化WebSocket功能验证脚本
"""

import asyncio
import websockets
import json
from datetime import datetime

async def simple_websocket_test():
    """简化的WebSocket测试"""
    print("🚀 简化WebSocket功能验证")
    print("=" * 40)
    
    try:
        # 连接WebSocket
        print("🔗 连接WebSocket服务器...")
        async with websockets.connect("ws://localhost:8000/ws/test_client") as websocket:
            print("✅ WebSocket连接成功!")
            
            # 监听连接确认消息
            message = await websocket.recv()
            data = json.loads(message)
            print(f"📨 收到连接确认: {data.get('message', '')}")
            
            # 测试ping/pong
            print("\n🏓 测试Ping/Pong...")
            await websocket.send(json.dumps({"type": "ping"}))
            
            # 接收pong响应
            pong_message = await websocket.recv()
            pong_data = json.loads(pong_message)
            print(f"📨 收到Pong响应: {pong_data.get('type', '')}")
            
            # 测试自定义消息
            print("\n💬 测试自定义消息...")
            custom_msg = {
                "type": "test_message",
                "content": "这是一个测试消息",
                "timestamp": datetime.now().isoformat()
            }
            await websocket.send(json.dumps(custom_msg))
            
            # 接收回显
            echo_message = await websocket.recv()
            echo_data = json.loads(echo_message)
            print(f"📨 收到回显: {echo_data.get('type', '')}")
            
            # 测试订阅功能
            print("\n📡 测试事件订阅...")
            subscribe_msg = {
                "type": "subscribe",
                "event_type": "test_events"
            }
            await websocket.send(json.dumps(subscribe_msg))
            
            # 接收订阅确认
            sub_message = await websocket.recv()
            sub_data = json.loads(sub_message)
            print(f"📨 收到订阅确认: {sub_data.get('message', '')}")
            
            print("\n✅ 所有基本功能测试成功!")
            
    except Exception as e:
        print(f"❌ WebSocket测试失败: {e}")
        return False
    
    return True

async def main():
    """主函数"""
    success = await simple_websocket_test()
    
    if success:
        print("\n🎉 WebSocket功能验证完成 - 所有测试通过!")
        print("💡 您现在可以:")
        print("   • 访问 http://localhost:8000/websocket-test 进行可视化测试")
        print("   • 在浏览器中测试实时进度推送功能")
        print("   • 使用批量报告生成功能测试进度显示")
    else:
        print("\n❌ WebSocket功能验证失败")
        print("💡 请检查:")
        print("   • 服务器是否正在运行")
        print("   • WebSocket端点是否正确注册")
        print("   • 防火墙设置")

if __name__ == "__main__":
    try:
        import websockets
    except ImportError:
        print("❌ 缺少websockets依赖")
        print("💡 请安装: pip install websockets")
        exit(1)
    
    asyncio.run(main()) 