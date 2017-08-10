from django.contrib import admin
from hostinfo.models import Host,History,Business,Monitor

class HostAdmin(admin.ModelAdmin):
    search_fields = ('hostname','ip',) ## 定义搜索框以哪些字段可以搜索
    list_display = ('hostname','ip','osversion','disk','beizhu')#  每行的显示信息
    list_display_links = ('hostname',)
    list_filter = ('jifang',)
class Historyinfo(admin.ModelAdmin):
    search_fields = ('user','ip','cmd') ## 定义搜索框以哪些字段可以搜索
    list_display = ('user','ip','cmd','root')#  每行的显示信息
    list_display_links = ('user',)
    list_filter = ('user','ip')

admin.site.register(Host,HostAdmin)
admin.site.register(History,Historyinfo)
admin.site.register(Business)
admin.site.register(Monitor)