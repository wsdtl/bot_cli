from pathlib import Path
from django.apps import AppConfig


class DerunConfig(AppConfig):
    """
    Args:
        default_auto_field: 默认自动创建主键
        name: 项目名字,与父目录同名
        verbose_name: Admin 一级管理菜单名字
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = ".".join(["admin", Path(__file__).resolve().parent.name])
    verbose_name = "德润热网数据库"
