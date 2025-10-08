from typing import List, Dict
from django.db.models import Model
from django.db.models.fields import Field
from import_export.fields import Field as IField
from import_export import resources
from .models import DRCYYDL


class DRCYYDLResource(resources.ModelResource):
    """
    Args:
        for en_name, zh_name in my_verbose_name_dict.items(): 重写对应表头
    """

    class Meta:
        """
        Args:
            model: 准备批量导入导出模型
        """

        model: Model = DRCYYDL

    my_fields_list: List["Field"] = Meta.model._meta.fields
    my_verbose_name_dict: Dict[str, str] = {
        i.name: i.verbose_name for i in my_fields_list
    }

    for en_name, zh_name in my_verbose_name_dict.items():
        locals()[en_name] = IField(attribute=en_name, column_name=zh_name)
