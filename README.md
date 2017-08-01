> # This project has moved to [Gitlab.com](https://gitlab.com/nobodyinperson/co2monitor)
> 
> The GitHub repository here is not up-to date.
> Please refer to [the repository on Gitlab.com](https://gitlab.com/nobodyinperson/co2monitor) for 
> Issues, Releases and the up-to-date repository code.

# co2monitor

Automatic data logging for AirCO2ntrol mini USB co2 measurement devices.

**Hint**: This application is compatible with Raspbian.

**Note**: This application is in development state.

![co2monitor svg](https://cloud.githubusercontent.com/assets/19148271/20570532/44d42ab0-b1a4-11e6-97aa-cef5713e21cc.png)

## Background

Hendryk Plötz reverse-engineered the usb protocol on [hackaday.io](https://hackaday.io/project/5301-reverse-engineering-a-low-cost-usb-co-monitor).
I wanted to have an easy-to-use plug'n'play data logging solution for Debian/Ubuntu systems.
That's what **co2monitor** is.

## Debian package

There are ready-to-use debian packages on the [releases page](https://github.com/nobodyinperson/co2monitor/releases), you may download the [latest release](https://github.com/nobodyinperson/co2monitor/releases/latest) there.

For automatic updates, you may use my [apt repository](http://apt.nobodyinperson.de).

To build a debian package from the repository, run ```dpkg-buildpackage -us -uc``` (options mean without signing) from the repository root.
There will be a ```co2monitor_*.deb``` one folder layer above.

## Installation

Install the debian package via ```sudo dpkg -i co2monitor_*.deb```.
Older versions of **co2monitor** will automatically be removed.

If you use my [apt repository](http://apt.nobodyinperson.de), install **co2monitor** like any other package via ```sudo apt-get update && sudo apt-get install co2monitor```

Remove **co2monitor** from your system via ```sudo apt-get remove co2monitor```.

## Folder structure

The folder structure (```etc```,```lib```,```usr```,```var```) is based on the [FHS](https://en.wikipedia.org/wiki/Filesystem_Hierarchy_Standard) and will be installed as-is to the target system.

### important files
|           file                 |                  purpose              |
|--------------------------------|---------------------------------------|
| ```etc/co2monitor/service.conf``` | co2monitor service configuration file |
| ```usr/bin/co2monitor-service``` |  the co2monitor service executable |
| ```usr/bin/co2monitor``` | the co2monitor application executable |
| ```var/lib/co2monitor/data/*``` | standard folder for logged co2 data |

## Special thanks

- Hendryk Plötz on [hackaday.io](https://hackaday.io/project/5301-reverse-engineering-a-low-cost-usb-co-monitor) for the device interaction
- Mike Kazantsev on his blog on [fraggod.net](http://blog.fraggod.net/2012/06/16/proper-ish-way-to-start-long-running-systemd-service-on-udev-event-device-hotplug.html) for the systemd integration
- Ascot on [StackOverflow.com](http://stackoverflow.com/a/26457317/5433146) for a workaround on ```signal.signal(signal, handler)``` when using a ```GLib.MainLoop```
- don_crissti on [StackOveflow.com](http://unix.stackexchange.com/a/203678) for
  getting a list of dbus objects
