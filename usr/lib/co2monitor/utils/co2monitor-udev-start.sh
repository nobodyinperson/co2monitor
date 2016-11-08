#!/bin/sh
# udev should set the environment variable DEVNAME to the current
# co2 device file
# echo "UDEV STARTED!" >> /var/log/co2monitor.log

# sleep one second
sleep 1

# get a list of already monitored device nodes
OPENDEVS=$(ps -ef | perl -ane 'print if(s/.*co2monitor-service\s+(\S+).*$/$1/g and not $F[1]==$$)')
# echo "DEVNAME: $DEVNAME">> /var/log/co2monitor.log
# echo "OPENDEVS: ">> /var/log/co2monitor.log
# echo "$OPENDEVS">> /var/log/co2monitor.log

# check if the current co2 device is already been monitored
export DEVICENAME=$(basename $DEVNAME)
echo $OPENDEVS | perl -e 'while(<>){ exit 0 if m#$ENV{DEVICENAME}$# };exit 1';
SYSTEMD=$?
# echo "SYSTEMD: $SYSTEMD">> /var/log/co2monitor.log

# if no, systemd obviously didn't manage to start co2monitor, so let's do it!
if ! $(exit $SYSTEMD);then
    # start co2monitor by hand and detach it
    # "at now" idea taken from http://unix.stackexchange.com/a/243648
    echo /usr/bin/co2monitor-service $DEVNAME udev | /usr/bin/at now
    exit 0 # exit quickly before udev kills us!!!
fi
