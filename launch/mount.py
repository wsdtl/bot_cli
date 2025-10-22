from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.staticfiles import StaticFiles
from admin.app.wsgi import application as django_app

from .log import logger


def FastAPIMount(app: "FastAPI") -> None:
    """
    将模块、应用程序挂载到 FastAPI 实例上
    """

    # 提供 静态文件
    app.mount("/static", StaticFiles(directory="./static"), name="static")
    logger.opt(colors=True).success(f"<g> router already mount: </g> <y> /static </y>")

    # 提供 媒体文件
    app.mount("/media", StaticFiles(directory="./media"), name="media")
    logger.opt(colors=True).success(f"<g> router already mount: </g> <y> /media </y>")

    # 装载 Django 应用程序
    app.mount("/admin", WSGIMiddleware(django_app))
    logger.opt(colors=True).success(f"<g> router already mount: </g> <y> /admin </y> ")


def AdapterMount(app: "FastAPI") -> list:
    """
    挂载 Adapter
    """
    _adapter = []

    # # 挂载 ws 消息处理器
    # from .adapter import ws

    # app.include_router(ws.router)
    # logger.opt(colors=True).success(f"<g>Loaded hander:</g> <y> /ws/bot/ Adapter已加载</y>")
    # _adapter.append(ws.WsMessageHander)

    # 挂载 R485 消息处理
    import asyncio
    from .adapter import R485

    logger.opt(colors=True).success(f"<g>Loaded hander:</g> <y> R485 Adapter已加载</y>")
    
    # 运行 R485 服务器
    asyncio.create_task(R485.R485Message.run())
    _adapter.append(R485.R485MessageHander)

    return _adapter
