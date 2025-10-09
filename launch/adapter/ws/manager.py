import json
from fastapi import WebSocket
from typing import Dict, Optional

from launch.log import logger


class ConnectionManager:
    """ws 对话管理器"""

    def __init__(self):

        # 存储活跃连接的字典
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: str) -> None:
        """接受 websocket 连接

        Args:
            websocket (WebSocket): websocket 对象
            client_id (str): client_id 唯一标识
        """

        await websocket.accept()

        # 将连接存储在字典中
        self.active_connections[client_id] = websocket

    def disconnect(self, client_id: str) -> None:
        """disconnect 断开连接

        Args:
            client_id (str): client_id 唯一标识
        """

        # 从字典中移除连接
        if client_id in self.active_connections:
            del self.active_connections[client_id]

    async def send_personal_message(self, message: dict, client_id: str, is_log: Optional[bool] = True) -> None:
        """发送个人消息

        Args:
            message (dict): 发送消息内容
            client_id (str): client_id 唯一标识
        """

        try:
            # 发送个人消息 序列化为 JSON 格式
            if client_id in self.active_connections:
                data = json.dumps(message, ensure_ascii=False)
                await self.active_connections[client_id].send_text(data)
                if is_log:
                    logger.opt(colors=True).success(f"<g>发送消息 to </g> <y>{client_id}</y> <g>内容:</g> <y>{data}</y>")

        except Exception:
            self.disconnect(client_id)

    async def broadcast(self, message: dict, exclude_client: str = None) -> None:
        """广播消息

        Args:
            message (dict): 发送消息内容
            exclude_client (str): 排除广播的 client_id 唯一标识 不填写则广播所有
        """

        # 广播消息 序列化为 JSON 格式
        disconnected_clients = []
        for client_id, connection in self.active_connections.items():
            if client_id == exclude_client:
                continue
            try:
                await connection.send_text(json.dumps(message, ensure_ascii=False))
            except Exception:
                disconnected_clients.append(client_id)

        # 清理断开连接的客户端
        for client_id in disconnected_clients:
            self.disconnect(client_id)


manager = ConnectionManager()
