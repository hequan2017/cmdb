from  django.shortcuts import render, redirect, HttpResponse
from hostinfo.models import Host, History,Business,Monitor
import json
from datetime import datetime
import paramiko
from django.contrib.auth.decorators import permission_required, login_required


from  hostinfo.ansible_runner.runner import AdHocRunner


@login_required(login_url="/login.html")
def host(request):  ##首页
    host = Host.objects.filter(id__gt=0)
    jifang_list = Business.objects.all()
    return render(request, 'host/host.html', {"host_list": host, "jifang_list": jifang_list})


@login_required(login_url="/login.html")
@permission_required('hostinfo.add_host', login_url='/error.html')
def host_add(request):  ##添加
    ret = {'status': True, 'error': None, 'data': None}
    if request.method == 'POST':
        try:
            ip = request.POST.get('ip', None)
            port = request.POST.get('port', None)
            username = request.POST.get('username', None)
            password = request.POST.get('password', None)
            jifang = request.POST.get('jifang_id', None)

            if ip and len(ip) > 8:
                assets = [
                    {
                        "hostname": 'host',
                        "ip": ip,
                        "port": port,
                        "username": username,
                        "password": password,
                    },
                ]
                task_tuple = (('setup', ''),)
                runner = AdHocRunner(assets)
                result = runner.run(task_tuple=task_tuple, pattern='all', task_name='Ansible Ad-hoc')
                data = result['contacted']['host'][0]['ansible_facts']
                hostname = data['ansible_fqdn']
                osversion = data['ansible_distribution'] + data['ansible_distribution_version']
                disk = str(sum([int(data["ansible_devices"][i]["sectors"]) * \
                                int(data["ansible_devices"][i]["sectorsize"]) / 1024 / 1024 / 1024 \
                                for i in data["ansible_devices"] if i[0:2] in ("vd", "ss", "sd")])) + str(" GB")
                
                memory = '{}MB'.format(data['ansible_memtotal_mb'])
                sn = data['ansible_product_serial']
                model_name = data['ansible_product_name']
                cpu_core = data['ansible_processor'][1] + "{}核".format(data['ansible_processor_count'])
                obj = Host.objects.create(hostname=hostname, ip=ip, port=port, username=username, password=password,
                                          jifang_id=jifang,
                                          osversion=osversion, memory=memory, disk=disk, sn=sn, model_name=model_name,
                                          cpu_core=cpu_core)
            else:
                ret['status'] = False
                ret['error'] = 'IP太短了,不能为空'
        except Exception as e:
            ret['status'] = False
            ret['error'] = '添加请求错误'
    return HttpResponse(json.dumps(ret))


@login_required(login_url="/login.html")
@permission_required('hostinfo.change_host', login_url='/error.html')
def host_change(request):  ##编辑
    ret = {'status': True, 'error': None, 'data': None}
    if request.method == 'POST':
        try:
            id = request.POST.get('id', None)
            hostname = request.POST.get('hostname', None)
            ip = request.POST.get('ip', None)
            osversion = request.POST.get('osversion', None)
            memory = request.POST.get('memory', None)
            disk = request.POST.get('disk', None)
            jifang = request.POST.get('jifang_id', None)
            sn = request.POST.get('sn', None)
            cpu_core = request.POST.get('cpu_core', None)
            model_name = request.POST.get('model_name', None)
            username = request.POST.get('username', None)
            password = request.POST.get('password', None)
            port = request.POST.get('port', None)
            beizhu = request.POST.get('beizhu', None)

            if ip and len(ip) > 4:
                obj = Host.objects.filter(id=id).update(hostname=hostname, ip=ip, osversion=osversion, memory=memory,
                                                        disk=disk, jifang_id=jifang, username=username,
                                                        password=password, sn=sn, cpu_core=cpu_core,
                                                        model_name=model_name,
                                                        port=port, beizhu=beizhu)
            else:
                ret['status'] = False
                ret['error'] = 'IP太短了,不能为空......'

        except Exception as e:
            ret['status'] = False
            ret['error'] = '添加请求错误'
        return HttpResponse(json.dumps(ret))


@login_required(login_url="/login.html")
@permission_required('hostinfo.change_host', login_url='/error.html')
def host_change_password(request):  ##修改密码
    if request.method == 'POST':
        id = request.POST.get('id', None)
        obj = Host.objects.filter(id=id).first()
        password = obj.password
        return HttpResponse(password)


@login_required(login_url="/login.html")
@permission_required('hostinfo.delete_host', login_url='/error.html')
def host_del(request):  ##删除
    ret = {'status': True, 'error': None, 'data': None}
    if request.method == 'POST':
        try:
            id = request.POST.get('id', None)
            obj = Host.objects.filter(id=id).delete()
        except Exception as e:
            ret['status'] = False
            ret['error'] = '删除请求错误'
    return HttpResponse(json.dumps(ret))


def ssh(ip,port,username,password,cmd):
    try:
        ssh = paramiko.SSHClient()  # 创建ssh对象
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ip, port=int(port), username=username, password=password, )
        stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
        result = stdout.read()
        result1 = result.decode()
        error = stderr.read().decode('utf-8')
        
        if not error:
            ret = {"ip":ip,"data":result1}
            ssh.close()
            return ret
    except Exception as e:
        error = "账号或密码错误,请修改保存再执行命令"
        ret = {"ip": ip, "data": error}
        return   ret
        
        

@login_required(login_url="/login.html")
def cmd(request):  ##命令行
    if request.method == "GET":
        obj = Host.objects.filter(id__gt=0)
        return render(request, 'host/cmd.html', {"host_list": obj, })
    if request.method == 'POST':
    
        ids = request.POST.getlist('id')
        cmd = request.POST.get('cmd', None)
        idstring = ','.join(ids)
        
        
        if not ids:
            error1 = "请选择主机"
            ret = {"error": error1, "status": False}
            return HttpResponse(json.dumps(ret))
        elif not cmd:
            error1 = "请输入命令"
            ret = {"error": error1, "status": False}
            return HttpResponse(json.dumps(ret))
        
        obj1 = Host.objects.extra(where=['id IN (' + idstring + ')'])

        x = {}
        x['status'] = True
        x['data'] = []
        for  i in obj1:
            a = ssh(ip=i.ip,port=i.port,username=i.username,password=i.password,cmd=cmd)
            history = History.objects.create(ip=i.ip, root=i.username, port=i.port, cmd=cmd, user=i.username)
            x['data'].append(a)
        return HttpResponse(json.dumps(x))


@login_required(login_url="/login.html")
def history(request):  ##历史命令
    history = History.objects.filter(id__gt=0)
    return render(request, 'host/history.html', {"history": history, })




@login_required(login_url="/login.html")
@permission_required('hostinfo.change_host', login_url='/error.html')
def hostupdate(request):  ## 更新

    ret = {'status': True, 'error': None, 'data': None}
    if request.method == 'POST':
        try:
            id = request.POST.get('id', None)
            obj = Host.objects.filter(id=id).first()
            ip = obj.ip
            port = obj.port
            username = obj.username
            password = obj.password
            beizhu = obj.beizhu
            jifang = obj.jifang_id
            assets = [
                {
                    "hostname": 'host',
                    "ip": ip,
                    "port": port,
                    "username": username,
                    "password": password,
                },
            ]
            task_tuple = (('setup', ''),)
            runner = AdHocRunner(assets)
            result = runner.run(task_tuple=task_tuple, pattern='all', task_name='Ansible Ad-hoc')
            data = result['contacted']['host'][0]['ansible_facts']
            hostname = data['ansible_fqdn']
            osversion = data['ansible_distribution'] + data['ansible_distribution_version']
            disk = str(sum([int(data["ansible_devices"][i]["sectors"]) * \
                        int(data["ansible_devices"][i]["sectorsize"]) / 1024 / 1024 / 1024 \
                        for i in data["ansible_devices"] if i[0:2] in ("vd", "ss", "sd")]))+str(" GB")
            
            
            memory = '{}MB'.format(data['ansible_memtotal_mb'])
            sn = data['ansible_product_serial']
            model_name = data['ansible_product_name']
            cpu_core = data['ansible_processor'][1] + "{}核".format(data['ansible_processor_count'])
            obj = Host.objects.filter(id=id).update(hostname=hostname, ip=ip, port=port,
                                      username=username, password=password,
                                      jifang_id=jifang,
                                      osversion=osversion, memory=memory,
                                      disk=disk, sn=sn, model_name=model_name,
                                      cpu_core=cpu_core, beizhu=beizhu)


            ret['status'] = False
            ret['error'] = '更新成功'

        except Exception as e:
            ret['status'] = False
            ret['error'] = '账号或密码错误'
        return HttpResponse(json.dumps(ret))
    
    
    
@login_required(login_url="/login.html")
@permission_required('hostinfo.delete_host', login_url='/error.html')
def hostall_del(request): ##批量删除
    ret = {'status': True, 'error': None, 'data': None}
    if  request.method == "POST":
             ids = request.POST.getlist('id')
             idstring = ','.join(ids)
             Host.objects.extra(where=['id IN (' + idstring + ')']).delete()

    return HttpResponse(json.dumps(ret))

@login_required(login_url="/login.html")
def host_show(request,nid):#性能展示
    try:
        i = Host.objects.filter(id=nid).first()
        cpu1 = ssh(ip=i.ip, port=i.port, username=i.username, password=i.password, cmd=" top -bn 1 -i -c | grep Cpu   ")
        cpu = float(cpu1['data'][8:14])
    
        total = ssh(ip=i.ip, port=i.port, username=i.username, password=i.password, cmd=" free | grep  Mem:  ")
        list = total['data'].split(" ")
        while ''  in list:
            list.remove('')
        mem = float('%.2f' %(int(list[2])/int(list[1])))
        

        all = Monitor.objects.all()
        date = []
        cpu_use = []
        mem_use = []
        for i in all:
            if i.server_id == int(nid):
                date.append(i.create_date.strftime("%m-%d %H:%M"))
                cpu_use.append(i.cpu_use)
                mem_use.append(i.mem_use)
                
        return render(request, 'host/show.html',{'cpu':cpu,'mem':mem,"hostid":nid, 'date':date ,'cpu_use':cpu_use, 'mem_use':mem_use })
    
    except Exception as e:
        host = Host.objects.filter(id__gt=0)
        jifang_list = Business.objects.all()
        msg = "账号密码错误，请修改"
        return render(request, 'host/host.html', {"host_list": host, "jifang_list": jifang_list,'msg':msg,})

@login_required(login_url="/login.html")
def host_show_api(request):#性能展示api
    if request.method == 'GET':
        id = request.GET.get('id',None)
        all = Monitor.objects.all()
        date=[]
        cpu_use=[]
        mem_use=[]
        for i in all:
            if  i.server_id == int(id):
                date.append(i.create_date.strftime("%m-%d %H:%M"))
                cpu_use.append(i.cpu_use)
                mem_use.append(i.mem_use)
                
        ret = {'date':date ,'cpu_use':cpu_use,'mem_use':mem_use}
        
        return HttpResponse(json.dumps(ret))
    
    
    
    
    