"""cmdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from sh.views import sh,shadd,shedit,shinfo,shdel,shdelall,shell,shell_sh


urlpatterns = [
    url(r'^sh.html$', sh,name="sh"),
    url(r'^shadd.html$', shadd,name="sh_add"),
    url(r'^shedit-(?P<nid>\d+).html$', shedit,name="sh_edit"),
    url(r'^shinfo-(?P<nid>\d+).html$', shinfo, name="sh_info"),
    url(r'^shdel.html$', shdel, name="sh_del"),
    url(r'^shalldel.html$', shdelall, name="sh_delall"),
    url(r'^shell-(?P<nid>\d+).html$', shell, name="shell"),
    url(r'^shell.html$', shell_sh, name="shell_sh"),
    # url(r'^shdel$', host_del,name='host_del'),
    # url(r'^shupdate$', hostupdate,name="hostupdate"),
    # url(r'^sh-del.html$', hostall_del),
    # url(r'^sh-(?P<nid>\d+).html$', host_show, name='sh_info'),

]
