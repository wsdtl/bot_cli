"""本模块定义了日志记录 Logger。

使用 [`loguru`][loguru] 来记录日志信息。

自定义 logger 请参考 [自定义日志](https://nonebot.dev/docs/appendices/log)
以及 [`loguru`][loguru] 文档。

[loguru]: https://github.com/Delgan/loguru

"""

import inspect
import logging
import sys
from typing import TYPE_CHECKING

import loguru

if TYPE_CHECKING:
    # avoid sphinx autodoc resolve annotation failed
    # because loguru module do not have `Logger` class actually
    from loguru import Logger

logger: "Logger" = loguru.logger
"""NoneBot 日志记录器对象。

默认信息:

- 格式: `[%(asctime)s %(name)s] %(levelname)s: %(message)s`
- 等级: `INFO` ，根据 `config.log_level` 配置改变
- 输出: 输出至 stdout

用法:
    ```python
    from nonebot.log import logger
    ```
"""

# default_handler = logging.StreamHandler(sys.stdout)
# default_handler.setFormatter(
#     logging.Formatter("[%(asctime)s %(name)s] %(levelname)s: %(message)s"))
# logger.addHandler(default_handler)


# https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging
class LoguruHandler(logging.Handler):  # pragma: no cover
    """logging 与 loguru 之间的桥梁，将 logging 的日志转发到 loguru。"""

    def emit(self, record: logging.LogRecord):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = inspect.currentframe(), 0
        while frame and (
            depth == 0 or frame.f_code.co_filename == logging.__file__
        ):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )

    @staticmethod
    def my_filter(record):
        """这里可以根据需求对日志进行筛选"""

        if "uvicorn" in record["name"]:
            record["name"] = "uvicorn"
        return True


"""默认日志格式"""
default_format: str = (
    "<g>{time:MM-DD HH:mm:ss}</g> "
    "[<lvl>{level}</lvl>] "
    "<c><u>{name}</u></c> | "
    # "<c>{function}:{line}</c>| "
    "{message}"
)


logger.remove()

"""默认日志处理器"""
local_logger_id = logger.add(
    "launch/log/runserver.log",
    rotation="12:00",
    level="INFO",
    format=default_format,
)

logger_id = logger.add(
    sys.stdout,
    level="INFO",
    format=default_format,
    filter=LoguruHandler.my_filter,
)


__autodoc__ = {
    "logger_id": False,
    "local_logger_id": False,
}


"""uvicorn 处理器日志配置 """
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "launch.log.LoguruHandler",
        },
    },
    "loggers": {
        "uvicorn.error": {"handlers": ["console"], "level": "INFO"},
        "uvicorn.access": {
            "handlers": ["console"],
            "level": "INFO",
        },
    },
}
