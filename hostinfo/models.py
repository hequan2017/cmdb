from django.db import models

# Create your models here.

class Host(models.Model):
    hostname = models.CharField(max_length=50, verbose_name='主机编号')
    ip = models.GenericIPAddressField(verbose_name='IP',null=True)
    port = models.CharField(max_length=50, verbose_name='端口',null=True)
    username = models.CharField(max_length=50, verbose_name='登陆用户',null=True)
    password = models.CharField(max_length=50, verbose_name='密码',null=True)
    jifang = models.ForeignKey(to="Business", to_field='id', null=True,verbose_name='机房')

    osversion = models.CharField(max_length=50,verbose_name='系统版本',null=True)
    memory = models.CharField(max_length=50,verbose_name='内存',null=True)
    disk = models.CharField(max_length=50,verbose_name='硬盘',null=True)
    sn = models.CharField(max_length=50, verbose_name='SN', null=True)
    model_name = models.CharField(max_length=50, verbose_name='型号', null=True)
    cpu_core = models.CharField(max_length=50, verbose_name='CPU', null=True)
    beizhu = models.CharField(max_length=1000, verbose_name='备注', null=True)


    class  Meta:
        db_table ="Host"
        verbose_name="服务器"
        verbose_name_plural = '服务器'


    def __str__(self):
        return self.hostname


class History(models.Model):
    root = models.CharField(max_length=50, verbose_name='用户', null=True)
    ip = models.GenericIPAddressField(verbose_name='IP',null=True)
    port = models.CharField(max_length=50,verbose_name='端口',null=True)
    cmd = models.CharField(max_length=50,verbose_name='命令',null=True)
    user = models.CharField(max_length=50,verbose_name='操作者',null=True)
    ctime = models.DateTimeField(auto_now_add=True, null=True, verbose_name='时间')

    class  Meta:
        db_table ="History"
        verbose_name="历史命令"
        verbose_name_plural = '历史命令'


    def __str__(self):
        return self.user

class Business(models.Model):
    caption = models.CharField(max_length=32, verbose_name='机房', null=True)
    # code = models.CharField(max_length=32, null=True, default="SA", verbose_name='产品线', )

    class Meta:
        db_table = "Business"
        verbose_name = "机房组"
        verbose_name_plural = '机房组'

    def __str__(self):
        return self.caption


# class Cpu(models.Model):
#     # host = models.OneToOneField('Host')   一条记录
#     server = models.ForeignKey('Host')
#     cpu_model = models.CharField(verbose_name='CPU型号', max_length=128,null=True)
#     cpu_count = models.SmallIntegerField(verbose_name='物理CPU个数',null=True)
#     cpu_core_count = models.SmallIntegerField(verbose_name='CPU核心数',null=True)
#     use = models.CharField(verbose_name='使用率',max_length=32,null=True)
#     memo = models.TextField(verbose_name='备注', null=True,)
#     create_date = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
#     update_date = models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')
#
#     class Meta:
#         db_table = 'Cpu'
#         verbose_name = 'CPU部件'
#         verbose_name_plural = verbose_name
#         # unique_together=("host","cpu_model")    联合唯一
#
#     def __str__(self):
#         return self.cpu_model


class Monitor(models.Model):
    server = models.ForeignKey('Host')
    cpu_use = models.CharField(verbose_name='CPU使用率',max_length=32,null=True)
    mem_use = models.CharField(verbose_name='内存使用率', max_length=32, null=True)
    # in_use = models.CharField(verbose_name='进流量', max_length=32, null=True)
    # out_use = models.CharField(verbose_name='出流量', max_length=32, null=True)

    create_date = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_date = models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')
    class Meta:
        db_table = 'Monitor'
        verbose_name = '监控状态'
        verbose_name_plural = verbose_name
        # unique_together=("host","cpu_model")    联合唯一

    def __str__(self):
        return self.cpu_use