[简体中文](README.md) | [English](README.en.md)

# CMDB

![Python](https://img.shields.io/badge/Python-3.6-blue.svg)
![Django](https://img.shields.io/badge/Django-1.11-green.svg)
![Celery](https://img.shields.io/badge/Celery-3.1-brightgreen.svg)
![Maintained](https://img.shields.io/badge/Maintenance-Discontinued-red.svg)

> **⚠️ This project has been discontinued!** Since the code has not been maintained for a long time, it may fail to deploy or contain bugs on different environments — please be aware. **For reference only!**

## 📖 Introduction

CMDB is a lightweight ops asset management system built with Django 1.11, covering asset management, host management, batch command/script execution, graphical performance display and WebSSH login.

It suits small and medium-sized server ops scenarios, and also works as a beginner project for Django + Ansible + Celery ops development: it collects real server asset info over SSH/Ansible, handles async and scheduled jobs with Celery, visualizes CPU/memory/network data with ECharts, and manages all processes with Supervisor.

## ✨ Features

- **Server asset management**: host CRUD and batch deletion, recording IP, port, login account, data center (Business), OS version, memory, disk, SN, model, CPU cores, notes, etc.
- **Automatic asset collection**: fetches hostname, OS version, disk, memory, CPU and more via Ansible Ad-hoc (the `setup` module) and fills them into the asset table
- **Performance monitoring**: collects CPU and memory usage plus eth0 network traffic in/out (reading `/proc/net/dev`) over SSH, by a Celery scheduled task (once a minute in the original version), saved into the Monitor table and linked to the host
- **Graphical display**: dynamic ECharts dashboards for CPU, memory and network performance of each host
- **Batch command execution**: runs commands on multiple hosts in parallel over paramiko SSH, with a command-line mode
- **Batch script execution**: shell / python / yml scripts, executed on selected hosts via the Ansible Runner (AdHocRunner / PlayBookRunner)
- **Command history**: the History table records operator, IP, port, command and time
- **WebSSH**: integrates webconsole (a Go project) for browser SSH login
- **Cabinet management**: the jigui module tracks cabinet resources (total, self-use, in-use, for-sale, full-package, etc.)
- **Permissions**: simple permission control based on Django admin's built-in auth — the add entry is hidden without permission and unauthorized access shows an error page
- **Admin theme**: django-suit v2 with a localized (Chinese) backend
- **Async tasks**: Celery 3 async tasks, manageable in the admin under "Home › Djcelery"; Flower monitoring on port 9008
- **Process management**: Supervisor manages redis, celery worker/beat/celerycam/flower and provides a web UI (port 9001)

## 🛠 Tech Stack

| Layer | Technology |
| --- | --- |
| Backend | Python 3.6, Django 1.11.20 (pinned in requirements.txt), Celery 3.1.25 + django-celery, Ansible, Paramiko, Flower, Supervisor |
| Frontend | Bootstrap template, ECharts |
| Admin | django-suit v2 (this exact version is required; other suit versions do not support Django 1.11) |
| Services | Redis (built from source by install_redis.sh, 4.0.1), webconsole (Go) |

## 🚀 Quick Start

Requirements: Python 3.6; install `sshpass` on the server with yum (otherwise asset info cannot be collected).

### 1. Clone and install dependencies

```bash
git clone git@github.com:hequan2017/cmdb.git
cd cmdb/
pip install -r requirements.txt
pip install https://github.com/darklow/django-suit/tarball/v2
```

> django-suit must be the tarball v2 version above; other suit versions do not support Django 1.11.

### 2. Configure Celery async tasks

Run `install_redis.sh` (builds and installs Redis).

### 3. Install and configure Supervisor

`supervisor` only supports `python2`, which does not affect running `python3` programs.

```bash
pip2 install supervisor

# Generate the config file and put it under /etc
echo_supervisord_conf > /etc/supervisord.conf

# Create a config directory, one file per program, isolated from each other
mkdir /etc/supervisord.d/
```

Edit `/etc/supervisord.conf` and add:

```ini
[include]
files = /etc/supervisord.d/*.conf
```

Enable the web management UI (already present by default, just uncomment and adjust):

```ini
[inet_http_server]
port=0.0.0.0:9001
username=user
password=123
```

Copy `supervisor.conf` from the repo into `/etc/supervisord.d/` (it manages redis, celery worker/beat/celerycam/flower).

### 4. Install WebSSH (webconsole)

Run `install_webssh.sh` to install the `webconsole` module, then adjust as explained in the script:

- `vim /opt/webconsole/conf/conf.json`: `"addr": ":9000"` sets the port (if you change it, update `templates/host/host.html` accordingly); `"enable_jsonp": true` enables cross-origin requests; put the web host address in `cors_white_list`
- Start/stop: `/opt/webconsole/bin/apibox start | stop`

### 5. Start

```bash
/usr/bin/python2.7 /usr/bin/supervisord -c /etc/supervisord.conf
# Manage processes at http://0.0.0.0:9001 (user: user, password: 123)

python manage.py runserver 0.0.0.0:8001    ##start the service
```

## 📁 Directory Structure

```text
├── cmdb               main configuration (settings / urls)
├── hostinfo           server assets, command execution, performance data (includes ansible_runner)
├── index              login / home / error pages
├── jigui              cabinet management
├── sh                 script tool library and batch execution (Celery tasks in sh/tasks.py)
├── static             css | js | img
├── templates          templates (host / jigui / sh)
├── install_redis.sh   build and install Redis 4.0.1
├── install_webssh.sh  build and install webconsole (WebSSH)
└── supervisor.conf    Supervisor process management config
```

## 📸 Screenshots

Architecture:

![Architecture](https://github.com/hequan2017/cmdb/blob/master/static/img/111.png)

Version 2.4 — process management with supervisor:

![supervisor](https://github.com/hequan2017/cmdb/blob/master/static/img/10.png)

Version 2.3 — celery async tasks (managed in the admin under "Home › Djcelery"):

![celery](https://github.com/hequan2017/cmdb/blob/master/static/img/9.png)

Version 2.2 — web SSH (webconsole):

![webssh](https://github.com/hequan2017/cmdb/blob/master/static/img/8.png)

Version 2.0 — basic resources, hosts (command execution), scripts (shell/python/yml):

![1](https://github.com/hequan2017/cmdb/blob/master/static/img/1.png)
![2](https://github.com/hequan2017/cmdb/blob/master/static/img/2.png)
![3](https://github.com/hequan2017/cmdb/blob/master/static/img/3.png)
![4](https://github.com/hequan2017/cmdb/blob/master/static/img/4.png)
![5](https://github.com/hequan2017/cmdb/blob/master/static/img/5.png)
![7](https://github.com/hequan2017/cmdb/blob/master/static/img/7.png)

Admin backend:

![6](https://github.com/hequan2017/cmdb/blob/master/static/img/6.png)

## 🗓 Version History

- **2.4**: process management with supervisor
- **2.3**: celery async tasks, manageable in the admin under "Home › Djcelery"
- **2.2**: web SSH via webconsole
- **2.1**: CPU and memory usage over SSH; django-crontab scheduled job collects data every minute and saves it to the monitor table, linked to the host
- **2.0**: feature set basically finalized in three parts: basic resources, hosts (command execution), scripts (shell/python/yml); planned to fetch data for graphs via the zabbix api (not implemented)
- **1.7.5**: batch execution of shell/yml
- **1.7**: minor improvements; admin backend updated to suit v2
- **1.6**: batch command execution
- **1.5.5**: minor improvements
- **1.5**: asset add, view, edit, update, delete — with real server asset collection
- **1.4**: command-line mode; command history
- **1.3**: host management (modal dialogs); server time update (ansible-playbook, see `hostinfo/ansible_api/cmd.yml`)
- **1.2**: permission module (admin's built-in auth): no add entry without permission, error page on unauthorized access; admin status derived from permissions
- **1.1.2**: echarts auto-resize; switched admin to django-suit (nicer UI, localized), demo account admin / 1qaz.2wsx (http://42.62.6.54:8001/admin)
- **1.1.1**: dynamic data visualization with Baidu ECharts

## 🔗 Related Projects

Other ops projects by the same author (hequan2017):

- [autoops](https://github.com/hequan2017/autoops): Linux asset management (CMDB), WebSSH and an ops automation platform
- [chain](https://github.com/hequan2017/chain): Lianmiao CMDB — Linux cloud host management system (assets, WebSSH, command/script execution, scheduled tasks)
- [husky](https://github.com/hequan2017/husky): a beginner-friendly Django CMDB tutorial project

## 📄 License

The repository ships without a LICENSE file; the code is for learning and reference only.

## 💬 Contact

* Blog: `http://hequan.blog.51cto.com/`
* Group: `620176501`  <a target="_blank" href="//shang.qq.com/wpa/qunwpa?idkey=bbe5716e8bd2075cb27029bd5dd97e22fc4d83c0f61291f47ed3ed6a4195b024"><img border="0" src="https://github.com/hequan2017/cmdb/blob/master/static/img/group.png"  alt="cmdb开发讨论群" title="cmdb开发讨论群"></a>
