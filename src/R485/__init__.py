import asyncio
from launch.adapter.R485 import R485MessageHander, R485Message

from launch.log import logger


@R485MessageHander.hander(cmd="温湿度传感器")
async def _(cmd: str, message: dict, writer: asyncio.StreamWriter, send: R485Message.send_data) -> None:
    """
    处理 温湿度传感器 消息
    参数:
        cmd (str): 命令字
        message (dict): 消息内容
        writer (asyncio.StreamWriter): 提供api以便于写数据至IO流中
        send (Callable): 发送数据接口函数
    """

    temperature = message.get("温度", None)
    humidity = message.get("湿度", None)
    ts = message.get("ts", None)

    # 显示接收到的数据
    logger.opt(colors=True).info(
        f"<g>收到温湿度传感器数据:</g> 温度: <y>{temperature}°C</y>, 湿度: <y>{humidity}%</y>, 更新时间: <y>{ts}</y>",
    )
