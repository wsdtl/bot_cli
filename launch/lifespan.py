import inspect
from fastapi import FastAPI
from typing import AsyncGenerator
from importlib import import_module
from contextlib import asynccontextmanager

from .log import logger
from .on_event import OnEvent
from .load_router import Routers, FastAPILoadRouter
from .schedulers import Scheduler
from .mount import FastAPIMount, AdapterMount


@asynccontextmanager
async def lifespan(app: "FastAPI") -> AsyncGenerator:
    """
    创建并启动后台线程来运行任务
    """
    
    # 挂载相应文件和服务
    FastAPIMount(app)
    
    # 导入模块设置
    FastAPILoadRouter()



    # 挂载 Adapter
    AdapterList = AdapterMount(app)

    # 启动同步定时任务调度器
    Scheduler.syncinstance.start()

    # 启动异步定时任务调度器
    Scheduler.asyncinstance.start()

    # 导入各级模块
    Routers.run()
    for module_name in Routers.module_list:
        try:
            module: Routers.Router = import_module(module_name)
            if module_name in Routers.router_list and hasattr(module, "router"):
                app.include_router(module.router)
                logger.opt(colors=True).success(f"<g>Loaded module include router:</g> <y>{module_name}</y>")
            else:
                logger.opt(colors=True).success(f"<g>Loaded module not include router:</g> <y>{module_name}</y>")
        except Exception as e:
            logger.opt(colors=True, exception=e).error(f"Loaded module error: {module_name}")

    # 运行 Adapter 收集器
    for Adapter in AdapterList:
        await Adapter.run()

    # 在同步定时任务调度器中添加任务
    for _sync in Scheduler.sync_list:
        Scheduler.syncinstance.add_job(
            _sync.get("func", None),
            *_sync.get("args", None),
            **_sync.get("kwargs", None),
        )

    # 在异步定时任务调度器中添加任务
    for _async in Scheduler.async_list:
        Scheduler.asyncinstance.add_job(
            _async.get("func", None),
            *_async.get("args", None),
            **_async.get("kwargs", None),
        )

    # 运行连接任务
    for connect in OnEvent.connect_list:
        if inspect.iscoroutinefunction(connect):
            await connect()
        else:
            connect()

    logger.opt(colors=True).success("<g>FastAPI 服务启动成功！</g>")

    yield

    # 运行断开任务
    for disconnect in OnEvent.disconnect_list:
        if inspect.iscoroutinefunction(disconnect):
            await disconnect()
        else:
            disconnect()
