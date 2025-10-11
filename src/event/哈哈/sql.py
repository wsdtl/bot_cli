from asgiref.sync import sync_to_async
from django.forms import model_to_dict

from admin.derun.lazy_import import DRCYYDL, DRCYYDL_TABLE_NAME


# 定义同步函数
@sync_to_async
def get_all():

    res = DRCYYDL.objects.raw("SELECT * FROM '德润产业园换热站地暖区' where id=5")

    return [{DRCYYDL_TABLE_NAME[k]: v for k, v in model_to_dict(item).items()} for item in res]
