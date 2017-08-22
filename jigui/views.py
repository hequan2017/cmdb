from  django.shortcuts import render, redirect,HttpResponse
from jigui import models
from django.contrib.auth.decorators import permission_required,login_required

import json
@login_required(login_url="/login.html",)
def jigui(request):  ##首页
    jigui = models.JiguiInfo.objects.filter(id__gt=0).order_by('-id')
    return render(request, 'jigui/jigui.html', {"jigui_list": jigui,})


@login_required(login_url="/login.html")
@permission_required('jigui.add_jiguiinfo',login_url='/error.html')
def add(request):  #添加
    if request.method == "POST":
        name1 = request.POST.get('name', None)
        jq1 = request.POST.get('jq', None)
        zy1 = request.POST.get('zy', None)
        ziy1 = request.POST.get('ziy', None)
        zs1 = request.POST.get('zs', None)
        zb1 = request.POST.get('zb', None)
        sh1 = request.POST.get('sh', None)
        xz1 = request.POST.get('xz', None)
        dx1 = request.POST.getlist('dx')
        yong1 = request.POST.get('yong')
        obj = models.JiguiInfo.objects.create(name=name1, jq=jq1, zy=zy1, ziy=ziy1, zs=zs1, zb=zb1, sh=sh1,xz=xz1,yong=yong1)


        obj.dx.add(*dx1)

        msg = "添加成功"
        dx = models.Jiguidx.objects.all()
        return render(request, 'jigui/add.html', {'msg': msg ,"dx_list":dx})
    else:
        dx = models.Jiguidx.objects.all()
        return render(request, 'jigui/add.html', {"dx_list":dx})


@login_required(login_url="/login.html")
def xiangxi(request, nid):  #详细页面
    jigui = models.JiguiInfo.objects.filter(id=nid).first()
    obj = models.JiguiInfo.objects.get(id=nid)
    dx = obj.dx.all()
    return render(request, 'jigui/xiangxi.html', {"xiangxi_info": jigui, "dx": dx,})


@login_required(login_url="/login.html")
@permission_required('jigui.change_jiguiinfo',login_url='/error.html')
def jigui_del(request, nid):  #删除
    models.JiguiInfo.objects.filter(id=nid).delete()
    return redirect('/jigui/jigui.html')



@login_required(login_url="/login.html")
@permission_required('jigui.delete_jiguiinfo',login_url='/error.html')
def jigui_edit(request, nid):   #编辑
    if request.method == "GET":
        obj1 = models.JiguiInfo.objects.filter(id=nid).first()   ##基本信息
        obj = models.JiguiInfo.objects.get(id=nid)
        dx = obj.dx.all()
        dx1 = models.Jiguidx.objects.all()
        return render(request, 'jigui/jiguiedit.html', {'obj': obj1,"dx_list":dx,"dx_list1":dx1})

    elif request.method == "POST":
        name1 = request.POST.get('name', None)
        jq1 = request.POST.get('jq', None)
        zy1 = request.POST.get('zy', None)
        ziy1 = request.POST.get('ziy', None)
        zs1 = request.POST.get('zs', None)
        zb1 = request.POST.get('zb', None)
        sh1 = request.POST.get('sh', None)
        xz1 = request.POST.get('xz', None)
        dx1 = request.POST.getlist('dx')
        yong1 = request.POST.get('yong')

        obj = models.JiguiInfo.objects.filter(id=nid).first()
        obj.name=name1
        obj.jq=jq1
        obj.zy=zy1
        obj.ziy=ziy1
        obj.zs=zs1
        obj.zb=zb1
        obj.sh=sh1
        obj.xz=xz1
        obj.yong=yong1
        obj.save()
        obj1 = models.JiguiInfo.objects.get(id=nid)
        obj1.dx.set(dx1)

        return redirect('/jigui/jigui.html')
    else:
        return redirect('/index.html')


@login_required(login_url="/login.html")
def show(request):  ## 展示
    name_id = models.JiguiInfo.objects.filter(id__gt=0)
    name = []
    jq = []
    for i in name_id:
        name.append(i.name)
        jq.append(i.jq)
    
    ret = {'name': name, 'jq': jq}
    
    return render(request, 'jigui/show.html',{'name':name,'jq':jq})


@login_required(login_url="/login.html")
def showapi(request):  ## 展示
    name_id = models.JiguiInfo.objects.filter(id__gt=0)
    name = []
    jq = []
    for i in name_id:
        name.append(i.name)
        jq.append(i.jq)
    
    ret={'name':name,'jq':jq}
    return  HttpResponse(json.dumps(ret))


@login_required(login_url="/login.html")
@permission_required('jigui.delete_jiguiinfo',login_url='/error.html')
def delete_jigui(request):##批量删除
    ret = {'status': True, 'error': None, 'data': None}
    if  request.method == "POST":
             ids = request.POST.getlist('id')
             idstring = ','.join(ids)
             models.JiguiInfo.objects.extra(where=['id IN (' + idstring + ')']).delete()


    return HttpResponse(json.dumps(ret))



