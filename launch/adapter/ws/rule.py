import asyncio
from functools import wraps
from typing import Optional
from datetime import datetime, timedelta
from collections import defaultdict
from fastapi import WebSocket, status


class TaskLimiter:
    """异步任务并发限制器"""

    def __init__(self, max_concurrent: Optional[int] = 100):
        """初始化信号量以限制并发任务数"""

        self.semaphore = asyncio.Semaphore(max_concurrent)

    async def bounded_task(self, coro):
        """限制并发执行的协程任务"""

        async with self.semaphore:
            return await coro


class RateLimiter:
    """WebSocket连接频率限制装饰器类"""

    # 存储客户端连接时间记录
    websocket_connected = defaultdict(list)

    @staticmethod
    def websocket(limit: int = 5, window: int = 60):
        """
        WebSocket连接频率限制装饰器

        Args:
            limit: 时间窗口内最大连接次数
            window: 时间窗口（秒）
        """

        def decorator(func):
            @wraps(func)
            async def wrapper(websocket: WebSocket, client_id: str, *args, **kwargs):
                current_time = datetime.now()

                # 清理过期的连接记录
                RateLimiter.websocket_connected[client_id] = [
                    connected_time for connected_time in RateLimiter.websocket_connected[client_id] if current_time - connected_time < timedelta(seconds=window)
                ]

                # 检查是否超过频率限制
                if len(RateLimiter.websocket_connected[client_id]) >= limit:
                    await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
                    return

                # 记录本次连接尝试
                RateLimiter.websocket_connected[client_id].append(current_time)

                # 调用原始函数
                return await func(websocket, client_id, *args, **kwargs)

            return wrapper

        return decorator
