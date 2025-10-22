import inspect
import asyncio
from typing import Dict, Callable, List, Union, TYPE_CHECKING

from ..base_hander import BaseMessageHander

if TYPE_CHECKING:
    from .R485_message import R485Message


class R485MessageHander(BaseMessageHander):
    """R485 消息处理器

    参数:
        func_dict: Dict[str, Callable]: 触发命令及其函数
    """

    func_dict: Dict[str, Callable] = {}
    func_cmd: List[str] = []

    @staticmethod
    async def run() -> None:
        """
        启动 R485 消息处理器 分类处理函数
        """

        R485MessageHander.func_cmd = R485MessageHander.func_dict.keys()

    @staticmethod
    async def background_task(cmd: str, message: List[dict], writer: asyncio.StreamWriter, send: "R485Message.send_data") -> None:
        """
        R485 消息处理器 处理后台任务

        参数：
            cmd (str): 触发消息的 cmd
            message (List[dict]): 触发消息数据 json 字符串
            writer (asyncio.StreamWriter): 提供api以便于写数据至IO流中
        """

        if cmd in R485MessageHander.func_cmd and cmd:

            if inspect.iscoroutinefunction(func := R485MessageHander.func_dict[cmd]):
                await func(cmd=cmd, message=message, writer=writer, send=send)
            else:
                func(cmd=cmd, message=message, writer=writer, send=send)

    @staticmethod
    def hander(cmd: Union[str, list]) -> Callable:
        """收集任务函数

        参数:
            cmd (str): 函数触发命令
        """

        def wrapper(func: Callable):

            if isinstance(cmd, list):
                for c in cmd:
                    if c in R485MessageHander.func_dict:
                        raise ValueError(f"命令 {c} 已存在，不能重复注册 from {c.__module__}.{func.__name__}")
                    R485MessageHander.func_dict[c] = func
            else:
                if cmd in R485MessageHander.func_dict:
                    raise ValueError(f"命令 {cmd} 已存在，不能重复注册 from {func.__module__}.{func.__name__}")
                R485MessageHander.func_dict[cmd] = func

        return wrapper
