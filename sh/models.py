from django.db import models



TOOL_RUN_TYPE = (
    (0, 'shell'),
    (1, 'python'),
    (2, 'yml'),
)

# class ToolsTypes(models.Model):
#     name = models.CharField(max_length=255, verbose_name='类型名称')
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = "工具类型"
#         verbose_name_plural = verbose_name


class ToolsScript(models.Model):
    name = models.CharField(max_length=255, verbose_name='工具名称')
    tool_script = models.TextField(verbose_name='脚本')
    # tools_type = models.ForeignKey(ToolsTypes, verbose_name='工具类型')
    # tool_run_type = models.CharField(max_length=255, verbose_name='脚本类型')
    tool_run_type = models.IntegerField(choices=TOOL_RUN_TYPE,verbose_name='脚本类型',default=0)
    comment = models.TextField(verbose_name='工具说明', null=True, blank=True)
    ctime = models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')
    utime = models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')
    
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = "ToolsScript"
        verbose_name = "工具"
        verbose_name_plural = verbose_name
        




