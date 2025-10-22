import json
import asyncio
from launch.log import logger

from .R485_message_hander import R485MessageHander
from .rule import TaskLimiter


class R485Message:
    """R485 消息处理类"""

    # 当前所有连接的 R485 客户端
    CONNECT = set()

    # 保持每个tasks的引用，防止被垃圾回收
    BACKGROUNDTASKS = set()

    # 创建任务并发限制器实例
    TASKLIMITER = TaskLimiter()

    @staticmethod
    async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        """
        R485 TCP接口回调函数

        参数:
            reader (asyncio.StreamReader): 提供从 IO 流读取数据的 API 的读取器
            writer (asyncio.StreamWriter): 提供api以便于写数据至IO流中
        注意：
            json_string = data.decode("utf-8").strip()
            json_data = json.loads(json_string)
            将二进制转为 json 字符串
        """
        addr, port = writer.get_extra_info("peername")
        logger.opt(colors=True).success(f"<g>R485 客户端建立连接:</g> <y>{addr}:{port}</y>")
        R485Message.CONNECT.add(writer)

        try:
            while True:
                data = await reader.read(1024)
                if not data:
                    break

                # 将字节流转为字符串并解析为 JSON
                try:
                    # 反序列化数据
                    json_string = data.decode("utf-8").strip()
                    json_data = json.loads(json_string)

                    ts = json_data.get("ts", None)
                    for k, v in json_data.items():
                        if k == "ts":
                            continue

                        # 将时间戳添加到每个消息中
                        v.append({"ts": ts})
                        logger.opt(colors=True).info(f"<g>收到R485消息</g> from <y>{k}:</y> <g>{v}</g>")

                        # 创建后台任务，并限制并发数
                        task = asyncio.create_task(
                            R485Message.TASKLIMITER.bounded_task(
                                R485MessageHander.background_task(
                                    cmd=k,
                                    message={_k: _v for d in v for _k, _v in d.items()},
                                    writer=writer,
                                    send=R485Message.send_data,
                                )
                            )
                        )

                        # 将 task 添加到集合中，以保持强引用：
                        R485Message.BACKGROUNDTASKS.add(task)

                        # 为了防止 task 被永远保持强引用，而无法被垃圾回收
                        # 让每个 task 在结束后将自己从集合中移除：
                        task.add_done_callback(R485Message.BACKGROUNDTASKS.discard)

                except (json.JSONDecodeError, UnicodeDecodeError) as e:
                    # 如果解析失败，回退到十六进制显示
                    message = " ".join(f"{byte:02x}" for byte in data)
                    logger.opt(colors=True).error(f"<r>收到非 R485 消息</r> from <y>{addr}:{port}</y>: {message}")

        except Exception as e:
            logger.opt(colors=True).success(f"<g>R485客户端 {addr} 主动断开连接:</g> <y>{e}</y>")
        finally:
            R485Message.CONNECT.remove(writer)
            writer.close()
            try:
                # 等待关闭完成，释放资源
                await writer.wait_closed()
            except Exception as e:
                pass

    @staticmethod
    async def send_data(writer: asyncio.StreamWriter, data: dict) -> None:
        """
        R485 发送数据接口函数

        参数:
            writer (asyncio.StreamWriter): 提供api以便于写数据至IO流中
            data (dict): 需要发送的数据字典
        """
        try:
            json_string = json.dumps(data)
            writer.write(json_string.encode("utf-8"))

            # 确保数据发送完成
            await writer.drain()

        except Exception as e:
            logger.opt(colors=True).error(f"<r>R485 发送数据失败:</r> <y>{e}</y>")

    async def run() -> None:
        """
        R485 TCP连接启动接口函数
        """
        HOST = "0.0.0.0"
        PORT = 1234
        server = await asyncio.start_server(R485Message.handle_client, host=HOST, port=PORT)
        logger.opt(colors=True).success(f"<g>R485 服务器启动在</g> <y>http://{HOST}:{PORT}</y>")
        async with server:
            await server.serve_forever()
