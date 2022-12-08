---
layout: post
category: [Linux]
tag: [Linux, 系统服务, service, systemctl, init系统, systemd]
title: Linux服务管理命令：service和systemctl
---

Linux 系统服务==守护程序：Linux启动时自动加载并在Linux退出时自动停止的系统任务。

早期Linux使用service来管理服务，现在用systemctl。

> 早期中，init是系统启动的第一个守护进程，也是其他所有进程的直接/间接祖先，pid为1。init进程后来进一步成为init系统，其工作：挂载/卸载文件系统、进程监控、启动其他守护进程等。
> 后来有了systemd，pid为1，负责启动其他程序。
> init系统是一系列简单精小服务构成的集合，配置起来很复杂，但是配置过程透明。而systemd则是一个包含很多功能的庞大系统，配置简单。

## 1. init系统

service是init系统下进行服务管理的命令，实质是一个shell脚本，在/etc/init.d/目录查找指定的服务脚本，然后调用该服务脚本来完成任务。

![](/assets/images/linux-system-command-service-and-systemctl/ShotScreen_20221208231044.png)

```shell
service acpid start
service cron stop
service kmod restart
service procps status
service --status-all # +运行中，-关闭，?无状态
ps aux | grep cups # 查看进程情况
```

**用户可以添加自定义服务，将相应脚本放置于/etc/init.d/文件夹下。**

## 2. systemd系统

[systemctl](https://man.archlinux.org/man/systemctl.1)是systemd系统下的服务管理命令。

```shell
systemctl status
systemctl start [单元]
systemctl stop [单元] 
systemctl restart [单元]
systemctl enable [单元]  #开机自动激活单元
systemctl disable [单元] #取消开机自动激活单元
systemctl daemon-reload  #重新载入systemd，扫描新的或有变动的单元
systemctl list-units --type=target # 列出了当前加载的和激活的目标
```

systemd管理所有系统资源，系统资源分为12类，每个系统资源对应一个[单元（Unit）](http://www.jinbuguo.com/systemd/systemd.unit.html)。12类单元包括service、target、device等，其中.service是最常见的单元文件。单元文件封装了对象的信息： 服务(service)、套接字(socket)、设备(device)、挂载点(mount)等。单元文件通常位于ubuntu `/etc/systemd/system`下：
![](/assets/images/linux-system-command-service-and-systemctl/ShotScreen_20221208232425.png)

**更改相关服务配置文件后，重启服务：**
```shell
sudo systemctl daemon-reload && sudo systemctl restart <service_name>
```

.target单元文件可以同时启动多个.service。

systemd提供日志功能：
```shell
journalctl # 输出所有的日志
journalctl -n [num] # 显示最后num行，默认10行
journalctl -f # 实时滚动最新日志
journalctl -u [unit] #显示指定unit的日志
```