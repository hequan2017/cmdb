from  django.shortcuts import render, redirect, HttpResponse
from sh.models import ToolsScript
from hostinfo.models import Host,History
import json,os
from django.contrib.auth.decorators import permission_required, login_required


from  hostinfo.ansible_runner.runner import AdHocRunner,CommandResultCallback,PlayBookRunner

@login_required(login_url="/login.html", )
def sh(request):  ##首页
    sh = ToolsScript.objects.filter(id__gt=0).order_by('-id')
    return render(request, 'sh/sh.html', {"sh_list":sh, })

@login_required(login_url="/login.html")
@permission_required('sh.add_ToolsScript',login_url='/error.html')
def shadd(request):  #添加
    if request.method == "POST":
        name = request.POST.get('name', None)
        tool_script = request.POST.get('tool_script', None)
        tool_run_type = request.POST.get('tool_run_type', None)
        comment = request.POST.get('comment', None)
        obj = ToolsScript.objects.create(name=name,tool_script=tool_script,tool_run_type=tool_run_type,comment=comment)
        msg = "添加成功"
        return render(request, 'sh/shadd.html', {'msg': msg ,})
    else:
        return render(request, 'sh/shadd.html',)
    
    
    
@login_required(login_url="/login.html")
@permission_required('sh.change_ToolsScript',login_url='/error.html')
def shedit(request, nid):   #编辑
    if request.method == "GET":
        obj1 = ToolsScript.objects.filter(id=nid)
        return render(request, 'sh/shedit.html',{'obj':obj1})

    elif request.method == "POST":
        
        name = request.POST.get('name', None)
        tool_script = request.POST.get('tool_script', None)
        tool_run_type = request.POST.get('tool_run_type', None)
        comment = request.POST.get('comment', None)

        obj1 = ToolsScript.objects.filter(id=nid).first()
        obj1.name=name
        obj1.tool_script=tool_script
        obj1.tool_run_type=tool_run_type
        obj1.comment = comment
        obj1.save()
        
        return redirect('/sh/sh.html')


@login_required(login_url="/login.html")
def shinfo(request, nid):  # 查看
    if request.method == "GET":
        obj1 = ToolsScript.objects.filter(id=nid)

        return render(request, 'sh/shinfo.html', {'obj': obj1})


@login_required(login_url="/login.html")
@permission_required('sh.delete_ToolsScript',login_url='/error.html')
def shdel(request):  # 删除
    ret = {'status': True, 'error': None, 'data': None}
    if request.method == "POST":
        id = request.POST.get('id',None)
        obj1 = ToolsScript.objects.filter(id=id).delete()
        return HttpResponse(json.dumps(ret))

@login_required(login_url="/login.html")
@permission_required('sh.delete_ToolsScript',login_url='/error.html')
def shdelall(request):##批量删除
    ret = {'status': True, 'error': None, 'data': None}
    if  request.method == "POST":
             ids = request.POST.getlist('id')
             idstring = ','.join(ids)
             ToolsScript.objects.extra(where=['id IN (' + idstring + ')']).delete()
             return HttpResponse(json.dumps(ret))




@login_required(login_url="/login.html")
def shell(request,nid):  ##执行脚本页面
    if  request.method=="GET":
        obj = Host.objects.filter(id__gt=0)
        sh = ToolsScript.objects.filter(id=nid)
      
        return  render(request,'sh/shell.html',{"host_list": obj,"sh":sh })


@login_required(login_url="/login.html")
def shell_sh(request):  ##执行脚本-执行
    ret = {'status': True, 'data': None}
    
    if request.method == 'POST':
        try:
            host_ids = request.POST.getlist('id', None)
            sh_id = request.POST.get('shid', None)
            user = request.user

            if not host_ids:
                error1 = "请选择主机"
                ret = {"error": error1, "status": False}
                return HttpResponse(json.dumps(ret))
                
            idstring = ','.join(host_ids)
            
            host = Host.objects.extra(where=['id IN (' + idstring + ')'])
            sh = ToolsScript.objects.filter(id=sh_id)
            
            for s in sh:
                if s.tool_run_type == 0:
                    with  open('sh/shell/test.sh'.format(s.id), 'w+') as f:
                        f.write(s.tool_script)
                        a = 'sh/shell/{}.sh'.format(s.id)
                    os.system("sed 's/\r//'  sh/shell/test.sh >  {}".format(a))
                    
                elif s.tool_run_type == 1:
                    with  open('sh/shell/test.py'.format(s.id), 'w+') as f:
                        f.write(s.tool_script)
                        p = 'sh/shell/{}.py'.format(s.id)
                    os.system("sed 's/\r//'  sh/shell/test.py >  {}".format(p))
                elif s.tool_run_type ==  2:
                    with  open('sh/shell/test.yml'.format(s.id), 'w+') as f:
                        f.write(s.tool_script)
                        y = 'sh/shell/{}.yml'.format(s.id)
                    os.system("sed 's/\r//'  sh/shell/test.yml >  {}".format(y))
                else:
                        ret['status'] = False
                        ret['error'] = '脚本类型错误,只能是shell、yml、python'
                        return HttpResponse(json.dumps(ret))
        

                data1 = []
                for h in host:
                    try:
                        data2={}
                        assets = [
                            {
                                "hostname": h.hostname,
                                "ip": h.ip,
                                "port": h.port,
                                "username": h.username,
                                "password": h.password,
                            },
                        ]

                        history = History.objects.create(ip=h.ip, root=h.username, port=h.port, cmd=s.name, user=user)
                        if s.tool_run_type == 0 :
                            task_tuple = (('script', a),)
                            hoc = AdHocRunner(hosts=assets)
                            hoc.results_callback = CommandResultCallback()
                            r = hoc.run(task_tuple)
                            data2['ip']=h.ip
                            data2['data']=r['contacted'][h.hostname]['stdout']
                            data1.append(data2)
                        elif s.tool_run_type == 1 :
                            task_tuple = (('script', p),)
                            hoc = AdHocRunner(hosts=assets)
                            hoc.results_callback = CommandResultCallback()
                            r = hoc.run(task_tuple)
                            data2['ip'] = h.ip
                            data2['data'] = r['contacted'][h.hostname]['stdout']
                            data1.append(data2)
                        elif s.tool_run_type ==  2 :
                            play = PlayBookRunner(assets, playbook_path=y)
                            b = play.run()
                            print(b)
                            data2['ip'] = h.ip
                            data2['data'] = b['plays'][0]['tasks'][1]['hosts'][h.hostname]['stdout'] + b['plays'][0]['tasks'][1]['hosts'][h.hostname]['stderr']
                            print(data2['data'])
                            
                            
                            print(data2)
                            data1.append(data2)
                        else:
                            data2['ip'] = "脚本类型错误"
                            data2['data'] = "脚本类型错误"
                    except  Exception as  e:
                        data2['ip'] = h.ip
                        data2['data'] ="账号密码不对，请修改 {}".format(e)
                        data1.append(data2)
                        
                ret['data'] = data1
                print(ret)
                return HttpResponse(json.dumps(ret))
        except Exception as e:
               ret['status'] = False
               ret['error'] = '未知错误 {}'.format(e)
               return HttpResponse(json.dumps(ret))

        