# co2monitor
Automatic data logging for AirCO2ntrol mini USB co2 measurement devices.

**Hint**: This application is compatible with Raspbian Jessie.

**Note**: This application is in development state.

## Background

Hendryk Plötz reverse-engineered the usb protocol on [hackaday.io](https://hackaday.io/project/5301-reverse-engineering-a-low-cost-usb-co-monitor).
I wanted to have an easy-to-use plug'n'play data logging solution for Debian/Ubuntu systems.
That's what **co2monitor** is.

## Debian package

There are ready-to-use debian packages on the [releases page](https://github.com/nobodyinperson/co2monitor/releases), you may download the [latest release](https://github.com/nobodyinperson/co2monitor/releases/latest) there.

To build a debian package from the repository, run ```dpkg-buildpackage -us -uc``` (options mean without signing) from the repository root.
There will be a ```co2monitor_*.deb``` one folder layer above.

## Installation

Install the debian package via ```sudo dpkg -i co2monitor_*.deb```.
Older versions of **co2monitor** will automatically be removed.

Remove **co2monitor** from your system via ```sudo apt-get remove co2monitor```.

## Folder structure

The folder structure (```etc```,```lib```,```usr```,```var```) is based on the [FHS](https://en.wikipedia.org/wiki/Filesystem_Hierarchy_Standard) and will be installed as-is to the target system.

### important files
|           file                 |                  purpose              |
|--------------------------------|---------------------------------------|
| ```etc/co2monitor/co2monitor.conf``` | co2monitor service configuration file |
| ```usr/lib/co2monitor/co2monitor-service``` |  the co2monitor service executable |
| ```usr/bin/co2monitor-applet``` | the co2monitor applet executable (currently unfunctional) |
| ```var/lib/co2monitor/data/*``` | standard folder for logged co2 data |

## Special thanks

- Hendryk Plötz on [hackaday.io](https://hackaday.io/project/5301-reverse-engineering-a-low-cost-usb-co-monitor) for the device interaction
- Mike Kazantsev on his blog on [fraggod.net](http://blog.fraggod.net/2012/06/16/proper-ish-way-to-start-long-running-systemd-service-on-udev-event-device-hotplug.html) for the systemd integration
