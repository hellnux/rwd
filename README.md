# rwd - Restart When Down

## Introduction

Project focused on keeping web hosting services operative, prolonging online time, even in unfavorable situations. Made, tested and used only on WHM/cPanel servers.

By identifying that Apache or MySQL is not running, or that the server has a high load average or high swap memory usage, rwd will restart Apache and/or MySQL to keep them online. The actions are recorded on log file and it possible enable e-mail notifications.

Initially developed to cover the WHM/cPanel monitor deficiency. Started in April 2011 in shell script, being rewritten in python 2 in 2012, gained new features and improvements until December 2014, and has been receiving maintenance to be compatible with recent operating systems.

## How rwd acts

Each cycle of 20 seconds (default) is performed 3 types of checks:

1. Swap - By default, upon reaching 50% swap usage, Apache and MySQL will be restarted.
2. MySQL - If MySQL is not running, MySQL will be restarted.
3. Apache - If Apache is not online or the server is overloaded, Apache will restart.

There are mechanisms that prevent multiple restarts in a short time, in cases of such as high swap usage or overloaded system.

## Prerequisites

- WHM/cPanel
- CentOS 6/7
- AlmaLinux 8/9
- RockyLinux 8/9 (not tested, but it is very likely that it will run)
- Uncheck Apache and Mysql from the "Monitor" column in "Service Manager" of WHM, to avoid conflict.

## Installation

As root:

```
mkdir -p /root/scripts/ 2> /dev/null
cd /root/scripts/
git clone https://github.com/hellnux/rwd.git
cd rwd
chmod 700 rwd.py rwd.conf
mv -f rwd /etc/rc.d/init.d/
cd /etc/rc.d/init.d/
chmod 755 rwd
chkconfig --add rwd
chkconfig --level 3 rwd on
service rwd start
```

## Use

rwd is ready for use, but you can edit the configuration file in /root/scripts/rwd/rwd.conf by simply restarting rwd to take effect.

Monitor the log:
```
tail -f /root/scripts/rwd/rwd.log
```

Start rwd:
```
service rwd start
```

Stop rwd:
```
service rwd stop
```

Restart rwd:
```
service rwd restart
```

## Uninstallation

As root:

```
service rwd stop;
chkconfig --del rwd
rm -f /etc/init.d/rwd
systemctl daemon-reload 2> /dev/null
rm -Rf /root/scripts/rwd/
```

## Authors

* **Danillo Costa** - [hellnux](https://github.com/hellnux)

See also the list of [contributors](https://github.com/hellnux/rwd/contributors) and [here](CONTRIBUTING.md) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
