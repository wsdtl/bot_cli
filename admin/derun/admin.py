from django.contrib import admin
from django.db.models import Model
from importlib import import_module

from admin.plugins.my_import_export import ImportExportModelAdmin


drcyydl = import_module("admin.derun.德润产业园换热站地暖区")
DRCYYDL: Model = getattr(drcyydl, "DRCYYDL")
DRCYYDLResource = getattr(drcyydl, "DRCYYDLResource")
DRCYYDL_TABLE_NAME: dict = getattr(DRCYYDLResource, "my_verbose_name_dict")


@admin.register(DRCYYDL)
class DRCYYDLAdmin(ImportExportModelAdmin):
    """
    Args:
        resource_class: 绑定对于批量导入导出模型
        list_per_page: 列表查询分页
        search_fields: 列表页上方的搜索框
        list_display: 列表页展示的字段
    """

    resource_class = DRCYYDLResource
    list_per_page = 10
    search_fields = DRCYYDL.search_fields()
    list_display = DRCYYDL.list_display()
    list_filter = DRCYYDL.list_filter()
