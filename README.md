[简体中文](README.md) | [English](README.en.md)

# CMDB

![Python](https://img.shields.io/badge/Python-3.6-blue.svg)
![Django](https://img.shields.io/badge/Django-1.11-green.svg)
![Celery](https://img.shields.io/badge/Celery-3.1-brightgreen.svg)
![Maintained](https://img.shields.io/badge/Maintenance-%E5%B7%B2%E5%81%9C%E6%AD%A2-red.svg)

> **⚠️ 本项目已停止开发！** 因长时间未对代码进行维护，可能会造成项目在不同环境上无法部署、运行 BUG 等问题，请知晓！**项目仅供参考！**

## 📖 项目介绍

CMDB 是一个基于 Django 1.11 开发的轻量级运维资产管理系统，涵盖资产管理、主机管理、批量执行命令/脚本、性能图形化展示和 WebSSH 登录。

它适合中小规模的服务器运维场景，也适合作为 Django + Ansible + Celery 运维开发的入门学习项目：通过 SSH/Ansible 真实采集服务器资产信息，用 Celery 处理异步与定时任务，用 ECharts 展示 CPU/内存/网络数据，并用 Supervisor 统一托管各进程。

## ✨ 功能特性

- **服务器资产管理**：主机增删改查、批量删除，记录 IP、端口、登录账号、机房（Business）、系统版本、内存、硬盘、SN、型号、CPU 核数、备注等
- **资产信息自动采集**：通过 Ansible Ad-hoc（`setup` 模块）真实获取主机名、系统版本、硬盘、内存、CPU 等信息回填资产表
- **性能监控采集**：通过 SSH 获取 CPU、内存使用率和 eth0 网卡进出流量（读 `/proc/net/dev`），由 Celery 定时任务定时采集（原版每分钟一次），保存到 Monitor 表并与主机关联
- **图形化展示**：基于 ECharts 动态展示主机的 CPU、内存、网络性能数据
- **批量执行命令**：paramiko SSH 批量下发命令，支持命令行模式
- **批量执行脚本**：支持 shell / python / yml 三类脚本，基于 Ansible Runner（AdHocRunner / PlayBookRunner）对所选主机批量执行
- **历史命令记录**：History 表记录操作者、IP、端口、命令与时间
- **WebSSH**：集成 webconsole（Go 语言项目），实现浏览器 SSH 登录
- **机柜管理**：jigui 模块维护机柜资源（总数、自用、在用、在售、整包等）
- **权限管理**：基于 Django admin 自带 auth 实现简单权限控制，无权限时隐藏添加入口并返回 error 页面
- **后台美化**：django-suit v2 中文化后台
- **异步任务**：Celery 3 异步任务，可在后台「首页 › Djcelery」中管理；Flower 监控（端口 9008）
- **进程管理**：Supervisor 托管 redis、celery worker/beat/celerycam/flower，并提供 Web 管理界面（端口 9001）

## 🛠 技术栈

| 层次 | 技术 |
| --- | --- |
| 后端 | Python 3.6、Django 1.11.20（requirements.txt 锁定版本）、Celery 3.1.25 + django-celery、Ansible、Paramiko、Flower、Supervisor |
| 前端 | Bootstrap 模板、ECharts |
| 后台 | django-suit v2（必须使用该版本，其他版本的 suit 不支持 Django 1.11） |
| 依赖服务 | Redis（install_redis.sh 编译安装 4.0.1）、webconsole（Go） |

## 🚀 快速开始

环境要求：Python 3.6，服务器需用 yum 安装 `sshpass`（否则无法获取资产信息）。

### 1. 拉取代码并安装依赖

```bash
git clone git@github.com:hequan2017/cmdb.git
cd cmdb/
pip install -r requirements.txt
pip install https://github.com/darklow/django-suit/tarball/v2
```

> django-suit 必须用上面 tarball v2 版本，其他版本的 suit 不支持 Django 1.11。

### 2. 配置 Celery 异步任务

执行 `install_redis.sh`（编译安装 Redis）。

### 3. 安装配置 Supervisor

`supervisor` 只支持 `python2`，不影响启动 `python3` 程序。

```bash
pip2 install supervisor

# 生成配置文件，放到 /etc 目录下
echo_supervisord_conf > /etc/supervisord.conf

# 新建配置目录，每个程序一个配置文件，相互隔离
mkdir /etc/supervisord.d/
```

修改 `/etc/supervisord.conf`，加入：

```ini
[include]
files = /etc/supervisord.d/*.conf
```

开启 Web 管理界面（默认已有，取消注释修改即可）：

```ini
[inet_http_server]
port=0.0.0.0:9001
username=user
password=123
```

将仓库中的 `supervisor.conf` 拷贝到 `/etc/supervisord.d/` 下（托管 redis、celery worker/beat/celerycam/flower）。

### 4. 安装 WebSSH（webconsole）

执行 `install_webssh.sh` 安装 `webconsole` 模块，按脚本内说明修改：

- `vim /opt/webconsole/conf/conf.json`：`"addr": ":9000"` 修改端口（如改成其他端口需同步修改 `templates/host/host.html`）；`"enable_jsonp": true` 开启跨域；`cors_white_list` 填写 web 主机地址
- 启动/停止：`/opt/webconsole/bin/apibox start | stop`

### 5. 启动

```bash
/usr/bin/python2.7 /usr/bin/supervisord -c /etc/supervisord.conf
# 登录 http://0.0.0.0:9001 （账号 user 密码 123）管理进程

python manage.py runserver 0.0.0.0:8001    ##启动服务
```

## 📁 目录结构

```text
├── cmdb               主配置（settings / urls）
├── hostinfo           服务器资产、命令执行、性能数据（内含 ansible_runner）
├── index              登录 / 首页 / 错误页
├── jigui              机柜管理
├── sh                 脚本工具库与批量执行（Celery 任务在 sh/tasks.py）
├── static             css | js | img
├── templates          模板（host / jigui / sh）
├── install_redis.sh   编译安装 Redis 4.0.1
├── install_webssh.sh  编译安装 webconsole（WebSSH）
└── supervisor.conf    Supervisor 进程托管配置
```

## 📸 截图

架构：

![架构](https://github.com/hequan2017/cmdb/blob/master/static/img/111.png)

版本 2.4 — 进程管理 supervisor：

![supervisor](https://github.com/hequan2017/cmdb/blob/master/static/img/10.png)

版本 2.3 — celery 异步任务（后台「首页 › Djcelery」管理）：

![celery](https://github.com/hequan2017/cmdb/blob/master/static/img/9.png)

版本 2.2 — web 版 ssh（webconsole）：

![webssh](https://github.com/hequan2017/cmdb/blob/master/static/img/8.png)

版本 2.0 — 基础资源、主机（执行命令）、脚本（shell/python/yml）：

![1](https://github.com/hequan2017/cmdb/blob/master/static/img/1.png)
![2](https://github.com/hequan2017/cmdb/blob/master/static/img/2.png)
![3](https://github.com/hequan2017/cmdb/blob/master/static/img/3.png)
![4](https://github.com/hequan2017/cmdb/blob/master/static/img/4.png)
![5](https://github.com/hequan2017/cmdb/blob/master/static/img/5.png)
![7](https://github.com/hequan2017/cmdb/blob/master/static/img/7.png)

后台：

![6](https://github.com/hequan2017/cmdb/blob/master/static/img/6.png)

## 🗓 版本历史

- **2.4**：进程管理 supervisor
- **2.3**：celery 异步任务，可在后台「首页 › Djcelery」管理
- **2.2**：web 版 ssh，利用 webconsole
- **2.1**：SSH 获取 CPU 和内存使用率；django-crontab 定时任务每分钟采集，保存到 monitor 表与 host 关联
- **2.0**：功能基本定型，分为三块：基础资源、主机（执行命令）、脚本（shell/python/yml）；计划用 zabbix api 调数据出图（暂未实现）
- **1.7.5**：批量执行 shell/yml
- **1.7**：小优化；后台 admin 更新为 suit v2
- **1.6**：批量执行命令
- **1.5.5**：小优化
- **1.5**：资产管理增、查、改、更新、删除，可真实获取服务器资产
- **1.4**：命令行模式；历史命令记录
- **1.3**：主机管理（模态对话框）；更新服务器时间（ansible-playbook，命令见 `hostinfo/ansible_api/cmd.yml`）
- **1.2**：权限模块（admin 自带 auth）：无添加权限看不到添加入口，无权限访问显示 error 页；根据权限判断是否管理员
- **1.1.2**：echarts 自适应；更换 admin 为 django-suit（界面更美观、中文化），demo 帐号密码 admin / 1qaz.2wsx（http://42.62.6.54:8001/admin）
- **1.1.1**：百度 echarts 图形化动态展示数据

## 🔗 相关项目

同作者（hequan2017）的其他运维项目：

- [autoops](https://github.com/hequan2017/autoops)：Linux 资产管理（CMDB）、WebSSH、自动化运维平台
- [chain](https://github.com/hequan2017/chain)：链喵 CMDB —— Linux 云主机管理系统（资产管理、WebSSH、命令/脚本执行、定时任务）
- [husky](https://github.com/hequan2017/husky)：Django 之入门 CMDB 系统（教程项目）

## 📄 License

仓库未附带 LICENSE 文件，代码仅供学习参考。

## 💬 联系方式

* 博客：`http://hequan.blog.51cto.com/`
* 群号：`620176501`  <a target="_blank" href="//shang.qq.com/wpa/qunwpa?idkey=bbe5716e8bd2075cb27029bd5dd97e22fc4d83c0f61291f47ed3ed6a4195b024"><img border="0" src="https://github.com/hequan2017/cmdb/blob/master/static/img/group.png"  alt="cmdb开发讨论群" title="cmdb开发讨论群"></a>
