# CMDB

架构
----------------
![图片](https://github.com/hequan2017/cmdb/blob/master/static/img/111.png)


DEMO
---------------

* 登录：`http://42.62.55.58:8002/`      ##请不要删除默认添加的服务器

* 默认用户名`admin` ,密码`1qaz.2wsx`

* 后台 登陆：  `http://42.62.55.58:8002//admin`

* 登录：`http://42.62.55.58:8002/`       ##做了特殊处理，主机密码错误也可以看见CPU和内存使用率。只限已经添加的 42.62.6.54

* 默认用户名`admin` ,密码`1qaz.2wsx`

* 后台 登陆：  `http://42.62.55.58:8002/admin`


* github链接：`https://github.com/hequan2017/cmdb`

* 博客： `http://hequan.blog.51cto.com/`

* 群 号：`620176501`   <a target="_blank" href="//shang.qq.com/wpa/qunwpa?idkey=bbe5716e8bd2075cb27029bd5dd97e22fc4d83c0f61291f47ed3ed6a4195b024"><img border="0" src="https://github.com/hequan2017/cmdb/blob/master/static/img/group.png"  alt="cmdb开发讨论群" title="cmdb开发讨论群"></a>


部署说明
-------------------

* 环境 python3.6.1  django1.11.4


* 服务器请yum 安装  `sshpass` ，不然无法获取资产信息。


* `git  clone  git@github.com:hequan2017/cmdb.git`

* `cd cmdb/`

* `pip install -r requirements.txt`     安装所需的模块

* `pip install https://github.com/darklow/django-suit/tarball/v2`  需要从这里下载  必须用这个版本，其他版本的suit不支持1.11版本django





##### 配置 celery 异步任务

* 执行 `install_redis.sh` 

##### 安装 `supervisor  `

* `supervisor` 只支持 `python2`,不影响启动`python3`
 
 
 `pip2 install    supervisor`      


* 生成配置文件，且放在`/etc`目录下


`echo_supervisord_conf > /etc/supervisord.conf  `
 

* 为了不将所有新增配置信息全写在一个配置文件里，这里新建一个文件夹，每个程序设置一个配置文件，相互隔离

`mkdir /etc/supervisord.d/  `
 

* 修改配置文件


`vim /etc/supervisord.conf`


* 加入以下配置信息


`[include]`

`files = /etc/supervisord.d/*.conf`


* 在supervisord.conf中设置通过web可以查看管理的进程，加入以下代码（默认即有，取消注释修改即可）	


`[inet_http_server] `


`port=0.0.0.0:9001 `


`username=user   `

   
`password=123`



* 将 `supervisor.conf` 拷贝到 `/etc/supervisord.d/`下面



* 执行`install_webssh.sh` 脚本， 安装`webconsole`模块。   需要修改的内容，可以看脚本。根据自己的情况修改。



*  `/usr/bin/python2.7 /usr/bin/supervisord -c /etc/supervisord.conf`

* 登陆 `0.0.0.0:9001` 账号 `user`  密码 `123`  就可以登陆进程管理界面

*  `python manage.py  runserver  0.0.0.0:8001`    ##启动服务



版本2.4
-------------
1. 进程管理 supervisor

![图片](https://github.com/hequan2017/cmdb/blob/master/static/img/10.png)


版本2.3
-------
1. celery 异步任务。  可进后台  点击 首页 › Djcelery ›    进行管理
![图片](https://github.com/hequan2017/cmdb/blob/master/static/img/9.png)



版本2.2
-------
1. web版本ssh，利用webconsole 。
![图片](https://github.com/hequan2017/cmdb/blob/master/static/img/8.png)



版本2.1
-------
1. 利用SSH  获取CPU和内存使用率

2. 利用django-crontab 做定时任务，每分钟获取一遍使用率，保存到monitor表里面，与host做关联。



版本2.0
-------
1. 第一版版本功能基本定型。
分为3块。 基础资源        主机（执行命令）     脚本（shell/python/yml）

2. 接下来主要开发 利用zabbix api 调取数据 出图（暂未实现）

![图片](https://github.com/hequan2017/cmdb/blob/master/static/img/1.png)
![图片](https://github.com/hequan2017/cmdb/blob/master/static/img/2.png)
![图片](https://github.com/hequan2017/cmdb/blob/master/static/img/3.png)
![图片](https://github.com/hequan2017/cmdb/blob/master/static/img/4.png)
![图片](https://github.com/hequan2017/cmdb/blob/master/static/img/5.png)
![图片](https://github.com/hequan2017/cmdb/blob/master/static/img/7.png)

后台

![图片](https://github.com/hequan2017/cmdb/blob/master/static/img/6.png)






历史
------------------------``

版本更新1.7.5

1 批量执行shell/yml


版本更新 1.7

1 版本小优化

2 更新后台admin模块 为suit v2版本



版本更新 1.6

1 批量执行命令


版本更新1.5.5

1 版本小优化


版本更新1.5

1 增加资产更新，分别为 添加 查看 修改 更新 删除。 可真实获取到服务器资产


版本更新1.4

1 增加命令行模式

2 增加历史命令记录


版本更新1.3

1 新增主机管理板块，采用模态对话框。

2 增加更新服务器时间板块，采用ansible-playbook ，需要安装 ansible模块。 操作的命令可以看hostinfo/ansible_api/cmd.yml文件


版本更新1.2

1 新增权限模块，采用admin自带的auth ，实现简单的权限管理。

无添加权限的，看不见 添加板块 ，同时对权限进行判断， 无权限 打不可，显示 error界面。
2 根据权限 判断 是否为 管理员。


版本更新1.1.2

1 修复了echarts 自适应更改大小。

2 更换了admin，采用django-suit 界面更好看，中文化。 需要安装 django-suit 模块。 admin的 帐号密码是 admin 1qaz.2wsx http://42.62.6.54:8001/admin


版本更新1.1.1

1 新增 图形化展示数据， 采用百度 echart 动态展示 数据。
