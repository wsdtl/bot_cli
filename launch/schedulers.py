from typing import Callable, List
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler


class Scheduler:

    syncinstance = BackgroundScheduler()
    sync_list: List[dict] = []
    asyncinstance = AsyncIOScheduler()
    async_list: List[dict] = []

    def _sync(*args, **kwargs) -> Callable:
        """同步定时任务"""

        def wrapper(func: Callable):
            Scheduler.sync_list.append(
                {
                    "func": func,
                    "args": args,
                    "kwargs": kwargs,
                }
            )

        return wrapper

    def _async(*args, **kwargs) -> Callable:
        """异步定时任务"""

        def wrapper(func: Callable):
            Scheduler.async_list.append(
                {
                    "func": func,
                    "args": args,
                    "kwargs": kwargs,
                }
            )

        return wrapper
