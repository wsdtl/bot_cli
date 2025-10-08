from typing import Callable, List


class OnEvent:

    connect_list: List[Callable] = []
    disconnect_list: List[Callable] = []

    def connect() -> Callable:
        """
        服务器启动时运行的函数
        """

        def wrapper(func: Callable):
            OnEvent.connect_list.append(func)

        return wrapper

    def disconnect() -> Callable:
        """
        服务器关闭时运行的函数
        """

        def wrapper(func: Callable):
            OnEvent.disconnect_list.append(func)

        return wrapper
