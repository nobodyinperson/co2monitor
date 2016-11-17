% co2monitor-service(1) | co2monitor-service manpage

NAME
====

**co2monitor-service** - a program to log co2 data from appropriate USB devices.


SYNOPSIS
========

**co2monitor-service**


SYSTEMD
=======

There is also a **systemd** unit, called **co2monitor.service**.
You may as well start **co2monitor-service** via

sudo systemctl start co2monitor


FILES
=====

| File                         | purpose                                   |
|------------------------------|-------------------------------------------|
| /etc/co2monitor/service.conf | **co2monitor-service** configuration file |


AUTHOR
======

Yann Büchau <yann.buechau@web.de>


SEE ALSO
========

the invoker **co2monitor-invoker(1)**, the gui **co2monitor(1)**


