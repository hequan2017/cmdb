from django.contrib import admin


from jigui.models import JiguiInfo,Jiguidx

class  jigui(admin.ModelAdmin):
    search_fields = ('name','dx','yong','dx') ## 定义搜索框以哪些字段可以搜索
    list_display = ('name','jq','zy','ziy','xz',)#  每行的显示信息
    list_display_links = ('name',)
    list_filter = ('yong','dx')
admin.site.register(JiguiInfo,jigui)
admin.site.register(Jiguidx)