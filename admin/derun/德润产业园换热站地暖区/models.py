from django.db import models


# 德润产业园换热站地暖区纵向运行报表
class DRCYYDL(models.Model):
    """
    数据库参数:
        verbose_name: 后台菜单展示名字
        db_column: 创建数据库时表头名字
        db_table: 通过db_table自定义数据表名

    函数功能：
        __str__: 每项数据简略展示数据
    """

    class Meta:
        """
        Args:
            verbose_name: Admin 二级管理菜单名字
            verbose_name_plural: 如果不设置这条表名后会带有's'符号
            db_table: 通过db_table自定义数据表名
        """

        verbose_name = "德润产业园换热站地暖区"
        verbose_name_plural = verbose_name
        db_table = "德润产业园换热站地暖区"

    time = models.DateTimeField(unique=True, null=True, verbose_name="时间", db_column="时间")
    comm = models.CharField(max_length=8, verbose_name="通讯状态", db_column="通讯状态")
    yzgw = models.FloatField(blank=True, null=True, verbose_name="一总供温", db_column="一总供温")
    yzhw = models.FloatField(blank=True, null=True, verbose_name="一总回温", db_column="一总回温")
    ywwc = models.FloatField(blank=True, null=True, verbose_name="一网温差", db_column="一网温差")
    ygyl = models.FloatField(blank=True, null=True, verbose_name="一供压力", db_column="一供压力")
    ygyllh = models.FloatField(blank=True, null=True, verbose_name="一供压(滤后)", db_column="一供压(滤后)")
    yhyl = models.FloatField(blank=True, null=True, verbose_name="一回压力", db_column="一回压力")
    ywyc = models.FloatField(blank=True, null=True, verbose_name="一网压差", db_column="一网压差")
    swwd = models.FloatField(blank=True, null=True, verbose_name="室外温度", db_column="室外温度")
    ygdn = models.FloatField(blank=True, null=True, verbose_name="有功电能", db_column="有功电能")
    ywssll = models.FloatField(blank=True, null=True, verbose_name="一网瞬时流量", db_column="一网瞬时流量")
    ywljll = models.FloatField(blank=True, null=True, verbose_name="一网累计流量", db_column="一网累计流量")
    bsljll = models.FloatField(blank=True, null=True, verbose_name="补水累积流量", db_column="补水累积流量")
    ywssrl = models.FloatField(blank=True, null=True, verbose_name="一网瞬时热量", db_column="一网瞬时热量")
    ywljrl = models.FloatField(blank=True, null=True, verbose_name="一网累计热量", db_column="一网累计热量")
    ewgw = models.FloatField(blank=True, null=True, verbose_name="二网供温", db_column="二网供温")
    ewhw = models.FloatField(blank=True, null=True, verbose_name="二网回温", db_column="二网回温")
    ewwc = models.FloatField(blank=True, null=True, verbose_name="二网温差", db_column="二网温差")
    egyl = models.FloatField(blank=True, null=True, verbose_name="二供压力", db_column="二供压力")
    ehyl = models.FloatField(blank=True, null=True, verbose_name="二回压力", db_column="二回压力")
    ewyc = models.FloatField(blank=True, null=True, verbose_name="二网压差", db_column="二网压差")
    sxyw = models.FloatField(blank=True, null=True, verbose_name="水箱液位", db_column="水箱液位")
    yhxhbpl = models.FloatField(blank=True, null=True, verbose_name="一号循环泵频率", db_column="一号循环泵频率")
    yhxhbsdpl = models.FloatField(blank=True, null=True, verbose_name="一号循环泵设定频率", db_column="一号循环泵设定频率")
    ehxhbpl = models.FloatField(blank=True, null=True, verbose_name="二号循环泵频率", db_column="二号循环泵频率")
    ehxhbsdpl = models.FloatField(blank=True, null=True, verbose_name="二号循环泵设定频率", db_column="二号循环泵设定频率")
    shxhbpl = models.FloatField(blank=True, null=True, verbose_name="三号循环泵频率", db_column="三号循环泵频率")
    shxhbsdpl = models.FloatField(blank=True, null=True, verbose_name="三号循环泵设定频率", db_column="三号循环泵设定频率")
    ehbsbpl = models.FloatField(blank=True, null=True, verbose_name="二号补水泵频率", db_column="二号补水泵频率")
    ehbsbsdpl = models.FloatField(blank=True, null=True, verbose_name="二号补水泵设定频率", db_column="二号补水泵设定频率")
    ewssll = models.FloatField(blank=True, null=True, verbose_name="二网瞬时流量", db_column="二网瞬时流量")
    ewljll = models.FloatField(blank=True, null=True, verbose_name="二网累计流量", db_column="二网累计流量")
    ewssrl = models.FloatField(blank=True, null=True, verbose_name="二网瞬时热量", db_column="二网瞬时热量")
    ewljrl = models.FloatField(blank=True, null=True, verbose_name="二网累计热量", db_column="二网累计热量")
    bsssll = models.FloatField(blank=True, null=True, verbose_name="补水瞬时流量", db_column="补水瞬时流量")
    zqmgwd = models.FloatField(blank=True, null=True, verbose_name="蒸汽母管温度", db_column="蒸汽母管温度")
    ljsljll = models.FloatField(blank=True, null=True, verbose_name="凝结水累计流量", db_column="凝结水累计流量")
    ljsssll = models.FloatField(blank=True, null=True, verbose_name="凝结水瞬时流量", db_column="凝结水瞬时流量")
    ljsgwd = models.FloatField(blank=True, null=True, verbose_name="凝结水管温度", db_column="凝结水管温度")
    ljsgyl = models.FloatField(blank=True, null=True, verbose_name="凝结水管压力", db_column="凝结水管压力")
    zqmgyl = models.FloatField(blank=True, null=True, verbose_name="蒸汽母管压力", db_column="蒸汽母管压力")
    shxhbpl = models.FloatField(blank=True, null=True, verbose_name="四号循环泵频率", db_column="四号循环泵频率")

    def __str__(self):
        return f"{self.time} {self.comm}"

    @staticmethod
    def search_fields():
        "搜索所用表头"
        return ["id", "time", "comm"]

    @staticmethod
    def list_display():
        "预览所用表头"
        return ["id", "time", "comm"]

    @staticmethod
    def list_filter():
        "聚合分类所用表头"
        return ["comm"]
