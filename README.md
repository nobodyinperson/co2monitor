# co2monitor
Python access to the TFA-Dostmann AirCO2ntrol USB co2 measurement device

**Note**: This application is in development state.

## Debian package

To build a debian package, run ```dpkg-buildpackage -us -uc``` (options mean without signing) from the repository root.
There will be a ```co2monitor_*.deb``` one folder layer above.

You may then install it via ```sudo dpkg -i co2monitor_*.deb```.
Older versions will automatically be removed.

## folder structure

The folder structure (```etc```,```lib```,```usr```,```var```) is based on the [FHS](https://en.wikipedia.org/wiki/Filesystem_Hierarchy_Standard) and will be installed as-is to the target system.

### important files
|           file                 |                  purpose              |
|--------------------------------|---------------------------------------|
| ```etc/co2monitor/co2monitor.conf``` | co2monitor service configuration file |
| ```usr/lib/co2monitor/co2monitor-service``` |  the co2monitor service executable |
| ```usr/bin/co2monitor-applet``` | the co2monitor applet executable |
| ```var/cache/co2monitor/data/*``` | logged co2 data |

