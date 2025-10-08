from import_export.admin import ImportExportModelAdmin
from import_export.formats import base_formats


class ImportExportModelAdmin(ImportExportModelAdmin):

    def get_import_formats(self) -> list:
        """
        重写get_import_formats方法,返回导入格式选项
        """
        formats = (
            base_formats.CSV,
            base_formats.XLS,
            base_formats.XLSX,
            base_formats.JSON,
        )
        return [f for f in formats if f().can_export()]

    def get_export_formats(self) -> list:
        """
        重写get_export_formats方法,返回导出格式选项
        """
        formats = (
            base_formats.CSV,
            base_formats.XLS,
            base_formats.XLSX,
            base_formats.TSV,
            base_formats.ODS,
            base_formats.JSON,
            base_formats.YAML,
            base_formats.HTML,
        )
        return [f for f in formats if f().can_export()]
