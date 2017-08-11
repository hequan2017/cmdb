# ~*~ coding: utf-8 ~*~

from hostinfo.models import Host,Monitor
from hostinfo.views import ssh

def   monitor_job():  ##计划任务
	
	object =  Host.objects.all()
	for i in object:
		cpu1 = ssh(ip=i.ip, port=i.port, username=i.username, password=i.password, cmd=" top -bn 1 -i -c | grep Cpu   ")
		cpu = float(cpu1['data'][8:14])
	
		total = ssh(ip=i.ip, port=i.port, username=i.username, password=i.password, cmd=" free | grep  Mem:  ")
		list = total['data'].split(" ")
		while '' in list:
			list.remove('')
		mem = float('%.2f' % (int(list[2]) / int(list[1])))
		Monitor.objects.create(server_id=i.id,cpu_use=cpu,mem_use=mem,)
		
