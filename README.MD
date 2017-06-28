# ServerAutoConnect

解决非固定IP下，服务器的自动联网以及DNS更新的方案。目前实现了在ip发生变动时，通过邮件来通知变动信息。



### Before you start

补充`auth/config/account.yaml`和`ip_update/config/emails.yaml`中的设置信息



### 使用`cron`来周期性调度脚本的方法

首先让`run.py`文件转变为可执行

```shell
chmod -x /path/to/run.py
```

随后编辑cron设置

```shell
crontab -e
```

在文件末尾加上

```shell
*/5 * * * * /usr/bin/python /path/to/run.py
```

（注意，如果你使用了virtualenv，那么上面的`/usr/bin/python`应当使用虚拟环境中的python）

通过下面的命令来更新cron

```shell
sudo service cron reload
```

cron的日志文件位于`/var/log/syslog`中，你可以通过下面的命令筛选出相cron相关的条目

```shell
bash sudo grep CRON /var/log/syslog
```

