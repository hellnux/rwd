## Under construction

# rwd - Restart When Down

## Introduction

Project focused on keeping web hosting services operative, or prolonging online time, even in unfavorable situations. Made, tested, and used only on WHM/cPanel servers.

By identifying that Apache or MySQL is not running, or that the machine has a high load average, or high swap memory usage, rwd will restart Apache and MySQL to keep them online. Actions are logged, and you can enable e-mail notifications.

Initially developed to cover the WHM/cPanel Monitor deficiency. Started in April 2011 in shell script, being rewritten in python 2 in 2012, gained new features and improvements until December 2014, when it received no further modification due to my lack of availability, which is why I am opening the code.

## Prerequisites

- WHM/cPanel
- CentOS 6/7
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

Rwd is ready for use, but you can edit the configuration file in /root/scripts/rwd/rwd.conf by simply restarting rwd to take effect.

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

## How rwd acts

Each cycle is performed 3 checks:

1. Swap - By default, upon reaching 50% swap usage, Apache and MySQL will be restarted.
2. MySQL - If MySQL is not operating, MySQL will be restarted.
3. Apache - If Apache is not online or the server is overloaded, Apache will restart.

## Authors

* **Danillo Costa** - [hellnux](https://github.com/hellnux)

See also the list of [contributors](https://github.com/hellnux/rwd/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details