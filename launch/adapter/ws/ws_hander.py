import inspect
from typing import Dict, Callable, List, Union

from ..base_hander import BaseMessageHander
from .manager import ConnectionManager


class WsMessageHander(BaseMessageHander):
    """Ws 消息处理器

    参数:
        func_dict: Dict[str, Callable]: 触发命令及其函数
    """

    func_dict: Dict[str, Callable] = {}
    func_cmd: List[str] = []

    @staticmethod
    async def run() -> None:
        """
        启动 Ws 消息处理器 分类处理函数
        """

        WsMessageHander.func_cmd = WsMessageHander.func_dict.keys()

    @staticmethod
    async def background_task(client_id: str, message_data: str, manager: "ConnectionManager") -> None:
        """
        Ws 消息处理器 处理后台任务

        参数：
            client_id (str): 触发消息的客户端 ID
            message_data (str): 触发消息数据 json 字符串
            manager (ConnectionManager): Ws对话管理器
        """

        _s = message_data.get("message", "").split()
        cmd = _s[0]
        message = _s[1:] if len(_s) > 1 else ""

        if cmd in WsMessageHander.func_cmd and cmd:

            if inspect.iscoroutinefunction(func := WsMessageHander.func_dict[cmd]):
                await func(client_id=client_id, message=message, manager=manager)
            else:
                func(client_id=client_id, message=message, manager=manager)

    @staticmethod
    def hander(cmd: Union[str, list]) -> Callable:
        """收集任务函数

        参数:
            cmd (str): 函数触发命令
        """

        def wrapper(func: Callable):

            if isinstance(cmd, list):
                for c in cmd:
                    if c in WsMessageHander.func_dict:
                        raise ValueError(f"命令 {c} 已存在，不能重复注册 from {c.__module__}.{func.__name__}")
                    WsMessageHander.func_dict[c] = func
            else:
                if cmd in WsMessageHander.func_dict:
                    raise ValueError(f"命令 {cmd} 已存在，不能重复注册 from {func.__module__}.{func.__name__}")
                WsMessageHander.func_dict[cmd] = func

        return wrapper
