import asyncio
from datetime import datetime
from launch.adapter.ws import WsMessageHander, ConnectionManager


@WsMessageHander.hander(cmd="你好")
async def write_notification(client_id: str, message: str, manager: "ConnectionManager") -> None:
    """
    Ws 消息处理器 示例命令函数

    参数：
        client_id (str): 触发消息的客户端 ID
        message (str): 触发消息内容
        manager (ConnectionManager): Ws对话管理器
    """
    response = f"你好！你发送的消息是: {message}"

    await manager.send_personal_message(
        {
            "type": "response",
            "message": response,
            "client_id": client_id,
            "timestamp": datetime.now().isoformat(),
        },
        client_id,
    )
    await asyncio.sleep(3)  # 模拟处理时间
    
