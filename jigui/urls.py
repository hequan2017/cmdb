#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""hequan URL Configuration

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

from django.conf.urls import url,include


from jigui.views import jigui, xiangxi, add, jigui_del,jigui_edit,show,delete_jigui,showapi


urlpatterns = [
    url(r'^$',jigui,name='jigui'),
    url(r'^jigui.html$', jigui,name='jigui'),
    url(r'^show.html$',  show,name='show'),
    url(r'^showapi$', showapi ,name='showapi'),
    url(r'^xiangxi-(?P<nid>\d+).html$', xiangxi,name='xiangxi'),
    url(r'^add.html$', add, name='addx'),
    url(r'^jigui-del.html$', delete_jigui),
    url(r'^jiguidel-(?P<nid>\d+).html$', jigui_del),
    url(r'^jiguiedit-(?P<nid>\d+).html$', jigui_edit),
    ## url(r'^home',Home.as_view())   调用类里面的，如果是get调用get,post调用post

]

