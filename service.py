#!/usr/bin/env python3

import dbus
import dbus.service
import dbus.mainloop.glib

import threading

import gi
from gi.repository import GObject

# define names
CO2MONITOR_BUSNAME    = "de.nobodyinperson.co2monitor"
CO2MONITOR_INTERFACE  = "de.nobodyinperson.co2monitor"
CO2MONITOR_OBJECTPATH = "/de/nobodyinperson/co2monitor"

# use glib as default mailoop for dbus
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

class LogThread(threading.Thread):
    def __init__(self, devicefile):
        self.devicefile = devicefile

    def run():
        pass
        

class Service(dbus.service.Object):
    def __init__(self):
        self.loop = GObject.MainLoop() # create mainloop

        sessionbus = dbus.SessionBus() # connect to sessionbus
        sessionbus.request_name(CO2MONITOR_BUSNAME) # request the bus name
        bus_name = dbus.service.BusName(CO2MONITOR_BUSNAME, sessionbus) # create bus name
        # register the object on the bus name
        dbus.service.Object.__init__(self, bus_name, CO2MONITOR_OBJECTPATH)


    def run(self):
        print("Service running...")
        self.loop.run()
        print("Service stopped")


    @dbus.service.method(CO2MONITOR_INTERFACE, in_signature='', out_signature='s')
    def status(self):
        if self.loop.is_running():
            return("running")
        else:
            return("stopped")
            

    @dbus.service.method(CO2MONITOR_INTERFACE, in_signature='', out_signature='')
    def quit(self):
        print("stopping co2monitor...")
        self.loop.quit()
        print("stopped co2monitor")


if __name__ == "__main__":
    service = Service()
    try:
        service.run()
    except KeyboardInterrupt:
        service.quit()
