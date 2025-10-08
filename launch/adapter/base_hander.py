from abc import abstractmethod
from typing import Callable


class BaseMessageHander:
    """消息处理器基类"""

    @abstractmethod
    async def run() -> None:
        """
        启动 消息处理器 分类处理函数
        """
        pass

    @abstractmethod
    async def background_task(*args, **kwargs) -> None:
        """
        消息处理器 处理后台任务
        """
        pass

    @abstractmethod
    def hander(*args, **kwargs) -> Callable:
        """消息处理器 收集任务函数"""
        pass
