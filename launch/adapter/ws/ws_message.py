import json
import asyncio
from datetime import datetime
from fastapi import WebSocket, WebSocketDisconnect, APIRouter
from launch.log import logger

from .manager import manager
from .ws_hander import WsMessageHander
from .rule import RateLimiter

router = APIRouter()


@router.websocket("/ws/bot/{client_id}")
@RateLimiter.websocket()
async def websocket_endpoint(websocket: WebSocket, client_id: str) -> None:

    await manager.connect(websocket, client_id)

    try:
        # 发送连接成功消息
        await manager.send_personal_message(
            {
                "type": "system",
                "message": "Connection established",
                "client_id": client_id,
                "timestamp": datetime.now().isoformat(),
            },
            client_id,
        )

        while True:

            # 接收客户端消息
            data = await asyncio.wait_for(websocket.receive_text(), timeout=300.0)  # 5分钟超时

            # 解析 JSON 数据
            try:
                message_data = json.loads(data)
            except json.JSONDecodeError:
                error_msg = {
                    "type": "error",
                    "message": "Invalid JSON format",
                }

                await manager.send_personal_message(error_msg, client_id)
                continue

            # 处理不同类型的消息
            message_type = message_data.get("type", "other")
            if message_type == "chat":
                # 接入消息处理器进行消息处理
                await WsMessageHander.background_task(
                    client_id=client_id,
                    message_data=message_data,
                    manager=manager,
                )
                logger.opt(colors=True).success(
                    f"<g>收到消息 from </g> <y>{client_id}</y> <g>内容:</g> <y>{message_data}</y>"
                )

            elif message_type == "ping":
                # 响应心跳包
                pong_msg = {
                    "type": "pong",
                    "timestamp": datetime.now().isoformat(),
                }

                await manager.send_personal_message(pong_msg, client_id)

            else:
                # 处理其他类型的消息
                pass

    except WebSocketDisconnect:
        manager.disconnect(client_id)
