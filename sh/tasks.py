import time
from celery import Celery, platforms
from hostinfo.models import Host,Monitor
from hostinfo.views import ssh
import threading,time


platforms.C_FORCE_ROOT = True

app= Celery('cmdb',)

@app.task
def add(x, y):
    print(x,y)
    return x + y


@app.task
def sendmail(mail):
    print('sending mail to %s...' % mail['to'])
    time.sleep(2.0)
    print('mail sent.')
    return mail['to']

@app.task
def job(id):  ##计划任务

    i = Host.objects.filter(id=id).first()
    cpu1 = ssh(ip=i.ip, port=i.port, username=i.username, password=i.password, cmd=" top -bn 1 -i -c | grep Cpu   ")
    cpu2 = cpu1['data'].split()
    cpu = cpu2[1].split('%')[0]


    total = ssh(ip=i.ip, port=i.port, username=i.username, password=i.password, cmd=" free | grep  Mem:  ")
    list = total['data'].split(" ")
    while '' in list:
        list.remove('')
    mem = float('%.2f' % (int(list[2]) / int(list[1]))) * 100

    in1 = ssh(ip=i.ip, port=i.port, username=i.username, password=i.password, cmd="cat /proc/net/dev  |  grep eth0  ")
    in2 = in1['data'].split()

    time.sleep(1)

    in3 = ssh(ip=i.ip, port=i.port, username=i.username, password=i.password,cmd="cat /proc/net/dev  |  grep eth0  ")
    in4 = in3['data'].split()

    in_network = int((int(in4[1]) - int(in2[1]))/1024/10*8)
    out_network = int((int(in4[9]) - int(in2[9]))/1024/10*8)
    Monitor.objects.create(server_id=i.id, cpu_use=cpu, mem_use=mem,in_use=in_network,out_use=out_network)



@app.task
def monitor_job():
    object = Host.objects.all()
    i_list = []
    for i in object:
        i_list.append(i.id)

    print(i_list)

    t_list = []
    for i in i_list:  ##循环调用
        t = threading.Thread(target=job, args=[i, ])
        t.start()
        t_list.append(t)
    for i in t_list:
        i.join()
    print("结束了")



