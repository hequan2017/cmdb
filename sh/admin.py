from django.contrib import admin
from sh.models import ToolsScript


class ToolAdmin(admin.ModelAdmin):
   search_fields = ('name','tool_run_type') ## 定义搜索框以哪些字段可以搜索
   list_display = ('name','tool_run_type','comment','ctime','utime')#  每行的显示信息
   list_display_links = ('name',)
   list_filter = ('name',)


admin.site.register(ToolsScript,ToolAdmin)
