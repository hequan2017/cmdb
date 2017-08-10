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
from hostinfo.views import host, cmd, host_add, host_change, host_del,history,hostupdate,host_change_password,hostall_del,host_show,host_show_api
urlpatterns = [
    url(r'^host.html$', host,name="host"),
    url(r'^cmd.html$', cmd,name="cmd"),
    url(r'^hostadd$', host_add,name="host_add"),
    url(r'^history.html$', history,name="history"),
    url(r'^hostpassword$', host_change_password,name="host_change_password"),
    url(r'^hostchange$', host_change,name="host_change"),
    url(r'^hostdel$', host_del,name='host_del'),
    url(r'^hostupdate$', hostupdate,name="hostupdate"),
    url(r'^hostapi$', host_show_api,name="hostshowapi"),
    url(r'^hostall-del.html$', hostall_del),
    url(r'^show-(?P<nid>\d+).html$', host_show, name='xiangxi'),
]