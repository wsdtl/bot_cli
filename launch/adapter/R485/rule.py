import asyncio
from typing import Optional


class TaskLimiter:
    """异步任务并发限制器"""

    def __init__(self, max_concurrent: Optional[int] = 100):
        """初始化信号量以限制并发任务数"""

        self.semaphore = asyncio.Semaphore(max_concurrent)

    async def bounded_task(self, coro):
        """限制并发执行的协程任务"""

        async with self.semaphore:
            return await coro
