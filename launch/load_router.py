import os
from typing import List
from fastapi import APIRouter
from abc import abstractmethod


class Routers:

    router_list: List[str] = []
    module_list: List[str] = []

    @staticmethod
    def run() -> None:

        Routers.router_list = list(set(Routers.router_list))
        Routers.router_list.sort()
        Routers.module_list = list(set(Routers.module_list))
        Routers.module_list.sort()

    class Router:

        @abstractmethod
        def router(self) -> "APIRouter":
            """
            各模块必须实现
            router = APIRouter(prefix="", tags=[""])
            且将其置于 模块 __init__.py 文件中
            """
            ...


class LoadRouter:

    @staticmethod
    def module_to_path(folder: str) -> str:

        if "." in folder:
            folder = os.path.join(*folder.split("."))

        return folder

    @staticmethod
    def load_router_folders(folder: str) -> None:
        """
        导入文件夹下所有文件夹下路由\n
        📦 src\n
        ├── 📂 router\n
        │   └── 📂 __init__.py include router\n
        ├── 📂 router\n
        │   └── 📂 __init__.py include router
        """

        folders = [
            f
            for f in os.listdir(LoadRouter.module_to_path(folder))
            if os.path.isdir(os.path.join(LoadRouter.module_to_path(folder), f))
        ]

        for module in folders:
            if "__init__.py" in os.listdir(os.path.join(LoadRouter.module_to_path(folder), module)):
                Routers.router_list.append(f"{folder}.{module}")
                Routers.module_list.append(f"{folder}.{module}")

    @staticmethod
    def load_router_folder(folder: str) -> None:
        """
        导入文件夹下所有路由\n
        📂 router\n
        └── 📂 __init__.py include router\n
        """

        if "__init__.py" in os.listdir(LoadRouter.module_to_path(folder)):
            Routers.router_list.append(folder)
            Routers.module_list.append(folder)

    @staticmethod
    def load_router_group(folder: str) -> None:
        """
        导入一个标准的路由模块\n
        APIRouter 在包 __init__.py 里面\n
        功能函数在各个小分包里面\n
        📦 src\n
        ├── __init__.py include router\n
        ├── 📂 module 需有 __init__.py not include router\n
        ├── 📂 module 需有 __init__.py not include router\n
        """

        LoadRouter.load_router_folder(folder)
        folders = [
            f
            for f in os.listdir(LoadRouter.module_to_path(folder))
            if os.path.isdir(os.path.join(LoadRouter.module_to_path(folder), f))
        ]
        for module in folders:
            if "__init__.py" in os.listdir(os.path.join(LoadRouter.module_to_path(folder), module)):
                Routers.module_list.append(f"{folder}.{module}")

    @staticmethod
    def load_module(folder: str) -> None:
        """
        导入一个标准的模型\n
        📂 module _init__.py not include router\n
        """

        Routers.module_list.append(folder)

    @staticmethod
    def load_module_group(folder: str) -> None:
        """
        导入一个标准的模型组\n
        功能函数在各个小分包里面\n
        📦 src\n
        ├── 📂 module _init__.py not include router\n
        ├── 📂 module _init__.py not include router\n
        """

        folders = [
            f
            for f in os.listdir(LoadRouter.module_to_path(folder))
            if os.path.isdir(os.path.join(LoadRouter.module_to_path(folder), f))
        ]
        for module in folders:
            if "__init__.py" in os.listdir(os.path.join(LoadRouter.module_to_path(folder), module)):
                Routers.module_list.append(f"{folder}.{module}")


def FastAPILoadRouter() -> None:
    """
    导入 FastAPI 项目各种路由
    """

    LoadRouter.load_module_group("src.event")
    LoadRouter.load_module("src.ws_cs")
