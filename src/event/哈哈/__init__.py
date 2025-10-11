from launch import OnEvent, logger
from .sql import get_all



@OnEvent.connect()
async def _():
    logger.opt(colors=True).info("<y>执行启动任务</y>")
    res = await get_all()
    print(res)
