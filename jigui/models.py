from django.db import models


class JiguiInfo(models.Model):
    #jifang_group = models.ForeignKey("index.JifangGroup", to_field='uid',default=1)  ##用户组表,默认id  user_group_id 数字
    name = models.CharField(max_length=64, verbose_name='名字')
    jq = models.CharField(max_length=64,verbose_name='总数')
    zy = models.CharField(max_length=64,verbose_name='自用',null=True)
    ziy = models.CharField(max_length=64,verbose_name='在用',null=True)
    zs = models.CharField(max_length=64,verbose_name='自用',null=True)
    zb = models.CharField(max_length=64,verbose_name='在售',null=True)
    sh = models.CharField(max_length=64,verbose_name='整包',null=True)
    xz = models.CharField(max_length=64,verbose_name='闲置',null=True)

    dx = models.ManyToManyField(to="Jiguidx",verbose_name='多选')
    yong = models.BooleanField(verbose_name='是否在用')

    ctime= models.DateTimeField(auto_now_add=True,null=True,verbose_name='创建时间')
    utime = models.DateTimeField(auto_now=True, null=True,verbose_name='更新时间')

    class  Meta:
        db_table ="JiguiInfo"
        verbose_name="机柜"
        verbose_name_plural = '机柜中心'


    def __str__(self):
        return self.name


class  Jiguidx(models.Model):
    xuan = models.CharField(max_length=64,verbose_name='多选选项')

    class  Meta:
        db_table ="Jiguidx"
        verbose_name="多选"
        verbose_name_plural = '多选'
    def __str__(self):
        return self.xuan





