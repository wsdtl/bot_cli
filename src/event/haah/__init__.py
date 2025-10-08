from launch import OnEvent, logger


@OnEvent.disconnect()
async def _():
    logger.opt(colors=True).info("<y>执行断开任务</y>")
