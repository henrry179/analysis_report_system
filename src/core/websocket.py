#!/usr/bin/env python3
"""
WebSocket连接管理模块
"""

import json
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime

from fastapi import WebSocket, WebSocketDisconnect

from config.settings import settings
from utils.logger import websocket_logger, system_logger
from utils.exceptions import WebSocketError
from core.models import WebSocketMessage


class ConnectionManager:
    """WebSocket连接管理器"""
    
    def __init__(self):
        # 存储活跃连接：client_id -> WebSocket连接列表
        self.active_connections: Dict[str, List[WebSocket]] = {}
        # 存储用户连接：client_id -> WebSocket连接
        self.user_connections: Dict[str, WebSocket] = {}
        # 连接统计
        self.connection_stats = {
            "total_connections": 0,
            "active_count": 0,
            "messages_sent": 0,
            "messages_received": 0
        }
    
    async def connect(self, websocket: WebSocket, client_id: str):
        """接受WebSocket连接"""
        try:
            await websocket.accept()
            
            # 检查连接数限制
            if len(self.user_connections) >= settings.WEBSOCKET_MAX_CONNECTIONS:
                await websocket.send_json({
                    "type": "error",
                    "message": "连接数已达上限",
                    "error_code": "CONNECTION_LIMIT_EXCEEDED"
                })
                await websocket.close()
                return False
            
            # 添加到连接列表
            if client_id not in self.active_connections:
                self.active_connections[client_id] = []
            self.active_connections[client_id].append(websocket)
            self.user_connections[client_id] = websocket
            
            # 更新统计
            self.connection_stats["total_connections"] += 1
            self.connection_stats["active_count"] = len(self.user_connections)
            
            # 记录连接信息
            client_info = {
                "client_ip": getattr(websocket.client, 'host', 'unknown'),
                "user_agent": dict(websocket.headers).get('user-agent', 'unknown'),
                "connected_at": datetime.now().isoformat()
            }
            
            websocket_logger.connection_established(client_id, client_info)
            
            # 发送连接成功消息
            await self.send_json_to_user({
                "type": "connection",
                "status": "connected",
                "message": f"WebSocket连接成功，客户端ID: {client_id}",
                "client_id": client_id,
                "server_time": datetime.now().isoformat(),
                "connection_count": self.connection_stats["active_count"]
            }, client_id)
            
            return True
            
        except Exception as e:
            websocket_logger.error_occurred(client_id, e)
            system_logger.error("WebSocket连接建立失败", error=e, client_id=client_id)
            return False
    
    def disconnect(self, websocket: WebSocket, client_id: str):
        """断开WebSocket连接"""
        try:
            # 从连接列表中移除
            if client_id in self.active_connections:
                if websocket in self.active_connections[client_id]:
                    self.active_connections[client_id].remove(websocket)
                
                # 如果该客户端没有其他连接，清理记录
                if not self.active_connections[client_id]:
                    del self.active_connections[client_id]
            
            # 从用户连接中移除
            if client_id in self.user_connections and self.user_connections[client_id] == websocket:
                del self.user_connections[client_id]
            
            # 更新统计
            self.connection_stats["active_count"] = len(self.user_connections)
            
            websocket_logger.connection_closed(client_id)
            
        except Exception as e:
            websocket_logger.error_occurred(client_id, e)
            system_logger.error("WebSocket连接断开处理失败", error=e, client_id=client_id)
    
    async def send_personal_message(self, message: str, client_id: str) -> bool:
        """发送个人文本消息"""
        try:
            if client_id in self.user_connections:
                await self.user_connections[client_id].send_text(message)
                self.connection_stats["messages_sent"] += 1
                websocket_logger.message_sent(client_id, "text")
                return True
            return False
        except Exception as e:
            websocket_logger.error_occurred(client_id, e)
            return False
    
    async def send_json_to_user(self, data: dict, client_id: str) -> bool:
        """发送JSON数据给特定用户"""
        try:
            if client_id in self.user_connections:
                # 添加时间戳
                if "timestamp" not in data:
                    data["timestamp"] = datetime.now().isoformat()
                
                await self.user_connections[client_id].send_json(data)
                self.connection_stats["messages_sent"] += 1
                websocket_logger.message_sent(client_id, data.get("type", "json"))
                return True
            return False
        except Exception as e:
            websocket_logger.error_occurred(client_id, e)
            return False
    
    async def broadcast(self, message: str, exclude_client: Optional[str] = None) -> int:
        """广播文本消息给所有连接的客户端"""
        sent_count = 0
        for client_id, websocket in self.user_connections.items():
            if client_id != exclude_client:
                try:
                    await websocket.send_text(message)
                    sent_count += 1
                    self.connection_stats["messages_sent"] += 1
                except Exception as e:
                    websocket_logger.error_occurred(client_id, e)
        
        system_logger.info("广播消息完成", sent_count=sent_count, excluded=exclude_client)
        return sent_count
    
    async def broadcast_json(self, data: dict, exclude_client: Optional[str] = None) -> int:
        """广播JSON数据给所有连接的客户端"""
        sent_count = 0
        
        # 添加时间戳
        if "timestamp" not in data:
            data["timestamp"] = datetime.now().isoformat()
        
        for client_id, websocket in self.user_connections.items():
            if client_id != exclude_client:
                try:
                    await websocket.send_json(data)
                    sent_count += 1
                    self.connection_stats["messages_sent"] += 1
                except Exception as e:
                    websocket_logger.error_occurred(client_id, e)
        
        system_logger.info("广播JSON消息完成", sent_count=sent_count, excluded=exclude_client)
        return sent_count
    
    async def send_to_role(self, data: dict, role: str) -> int:
        """发送消息给特定角色的用户"""
        # 这里需要与用户管理系统集成
        # 暂时实现为发送给所有用户
        return await self.broadcast_json(data)
    
    async def ping_all_connections(self):
        """向所有连接发送ping消息"""
        ping_data = {
            "type": "ping",
            "server_time": datetime.now().isoformat(),
            "active_connections": len(self.user_connections)
        }
        
        return await self.broadcast_json(ping_data)
    
    def get_connection_info(self, client_id: str) -> Optional[dict]:
        """获取连接信息"""
        if client_id in self.user_connections:
            websocket = self.user_connections[client_id]
            return {
                "client_id": client_id,
                "state": websocket.client_state.name if hasattr(websocket, 'client_state') else "connected",
                "client_ip": getattr(websocket.client, 'host', 'unknown'),
                "headers": dict(websocket.headers)
            }
        return None
    
    def get_statistics(self) -> dict:
        """获取连接统计信息"""
        return {
            **self.connection_stats,
            "active_connections": list(self.user_connections.keys()),
            "connection_details": {
                client_id: self.get_connection_info(client_id) 
                for client_id in self.user_connections.keys()
            }
        }
    
    async def cleanup_stale_connections(self):
        """清理失效连接"""
        stale_connections = []
        
        for client_id, websocket in self.user_connections.items():
            try:
                # 尝试发送ping来检测连接状态
                await websocket.send_json({"type": "ping", "timestamp": datetime.now().isoformat()})
            except Exception:
                stale_connections.append(client_id)
        
        # 清理失效连接
        for client_id in stale_connections:
            websocket = self.user_connections.get(client_id)
            if websocket:
                self.disconnect(websocket, client_id)
        
        if stale_connections:
            system_logger.info("清理失效连接", count=len(stale_connections), clients=stale_connections)
        
        return len(stale_connections)


class WebSocketHandler:
    """WebSocket消息处理器"""
    
    def __init__(self, manager: ConnectionManager):
        self.manager = manager
    
    async def handle_message(self, websocket: WebSocket, client_id: str, message: str):
        """处理接收到的消息"""
        try:
            data = json.loads(message)
            message_type = data.get("type")
            
            # 更新接收统计
            self.manager.connection_stats["messages_received"] += 1
            
            # 根据消息类型分发处理
            if message_type == "ping":
                await self._handle_ping(client_id, data)
            elif message_type == "pong":
                await self._handle_pong(client_id, data)
            elif message_type == "subscribe":
                await self._handle_subscribe(client_id, data)
            elif message_type == "unsubscribe":
                await self._handle_unsubscribe(client_id, data)
            elif message_type == "echo":
                await self._handle_echo(client_id, data)
            else:
                await self._handle_unknown_message(client_id, data)
                
        except json.JSONDecodeError:
            await self.manager.send_json_to_user({
                "type": "error",
                "message": "无效的JSON格式",
                "error_code": "INVALID_JSON"
            }, client_id)
        except Exception as e:
            websocket_logger.error_occurred(client_id, e)
            await self.manager.send_json_to_user({
                "type": "error",
                "message": "消息处理失败",
                "error_code": "MESSAGE_PROCESSING_ERROR"
            }, client_id)
    
    async def _handle_ping(self, client_id: str, data: dict):
        """处理ping消息"""
        await self.manager.send_json_to_user({
            "type": "pong",
            "original_timestamp": data.get("timestamp"),
            "server_timestamp": datetime.now().isoformat()
        }, client_id)
    
    async def _handle_pong(self, client_id: str, data: dict):
        """处理pong消息"""
        # 记录延迟时间
        original_time = data.get("original_timestamp")
        if original_time:
            try:
                original_dt = datetime.fromisoformat(original_time.replace('Z', '+00:00'))
                latency = (datetime.now() - original_dt).total_seconds() * 1000
                websocket_logger.logger.info(f"客户端延迟", client_id=client_id, latency_ms=latency)
            except Exception:
                pass
    
    async def _handle_subscribe(self, client_id: str, data: dict):
        """处理订阅消息"""
        event_type = data.get("event_type")
        await self.manager.send_json_to_user({
            "type": "subscription",
            "event_type": event_type,
            "status": "subscribed",
            "message": f"已订阅 {event_type} 事件"
        }, client_id)
    
    async def _handle_unsubscribe(self, client_id: str, data: dict):
        """处理取消订阅消息"""
        event_type = data.get("event_type")
        await self.manager.send_json_to_user({
            "type": "subscription",
            "event_type": event_type,
            "status": "unsubscribed",
            "message": f"已取消订阅 {event_type} 事件"
        }, client_id)
    
    async def _handle_echo(self, client_id: str, data: dict):
        """处理回显消息"""
        await self.manager.send_json_to_user({
            "type": "echo",
            "original_message": data,
            "server_timestamp": datetime.now().isoformat()
        }, client_id)
    
    async def _handle_unknown_message(self, client_id: str, data: dict):
        """处理未知类型消息"""
        await self.manager.send_json_to_user({
            "type": "error",
            "message": f"未知的消息类型: {data.get('type')}",
            "error_code": "UNKNOWN_MESSAGE_TYPE",
            "received_data": data
        }, client_id)


# 全局连接管理器实例
manager = ConnectionManager()
handler = WebSocketHandler(manager)


async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """WebSocket端点处理函数"""
    connection_established = await manager.connect(websocket, client_id)
    if not connection_established:
        return
    
    try:
        while True:
            # 接收客户端消息
            data = await websocket.receive_text()
            await handler.handle_message(websocket, client_id, data)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, client_id)
        websocket_logger.connection_closed(client_id, "Normal disconnect")
        
        # 广播断开连接消息（可选）
        await manager.broadcast_json({
            "type": "connection",
            "status": "disconnected",
            "client_id": client_id,
            "message": f"客户端 {client_id} 已断开连接",
            "active_connections": manager.connection_stats["active_count"]
        }, exclude_client=client_id)
        
    except Exception as e:
        manager.disconnect(websocket, client_id)
        websocket_logger.error_occurred(client_id, e)
        system_logger.error("WebSocket连接异常", error=e, client_id=client_id)


async def start_websocket_maintenance():
    """启动WebSocket维护任务"""
    async def maintenance_task():
        while True:
            try:
                # 定期清理失效连接
                await manager.cleanup_stale_connections()
                
                # 定期发送ping
                if manager.user_connections:
                    await manager.ping_all_connections()
                
                # 等待下一次维护
                await asyncio.sleep(settings.WEBSOCKET_PING_INTERVAL)
                
            except Exception as e:
                system_logger.error("WebSocket维护任务失败", error=e)
                await asyncio.sleep(10)  # 出错时等待10秒再重试
    
    # 启动后台维护任务
    asyncio.create_task(maintenance_task())
    system_logger.info("WebSocket维护任务已启动", ping_interval=settings.WEBSOCKET_PING_INTERVAL) 