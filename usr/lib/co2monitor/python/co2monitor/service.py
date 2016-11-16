#!/usr/bin/env python
import dbus
import dbus.service
import dbus.mainloop.glib

import logging
import configparser 
import signal
import threading

from gi.repository import GObject

# define names
CO2MONITOR_BUSNAME    = "de.nobodyinperson.co2monitor"
CO2MONITOR_INTERFACE  = "de.nobodyinperson.co2monitor"
CO2MONITOR_OBJECTPATH = "/de/nobodyinperson/co2monitor"

class Co2MonitorService(dbus.service.Object):
    def __init__(self):
        # initially set the standard logger
        self.set_logger(logging.getLogger(__name__))
        # initially set an empty configuration
        self.set_config(configparser.ConfigParser())

        # handle SIGINT and SIGTERM
        signal.signal(signal.SIGINT, self.please_stop_now)
        # signal.signal(signal.SIGTERM, self.please_stop_now)

        # use glib as default mailoop for dbus
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

        self.loop = GObject.MainLoop() # create mainloop

        systembus = dbus.SystemBus() # the system bus
        systembus.request_name(CO2MONITOR_BUSNAME) # request the bus name
        bus_name = dbus.service.BusName(CO2MONITOR_BUSNAME, systembus) # create bus name
        # register the object on the bus name
        dbus.service.Object.__init__(self, bus_name, CO2MONITOR_OBJECTPATH)

    # set the config
    def set_config(self, config):
        self.config = config

    # set the logger
    def set_logger(self, logger):
        self.logger = logger

    # kindly stop logging
    def please_stop_now(self, signum=None, frame=None):
        self.logger.info(" ".join([_("received stop signal {},"),
            _("will terminate soon...")]).format(signum))
        self.quit()

    def run(self):
        self.logger.info(_("Service running..."))
        self.loop.run()
        self.logger.info(_("Service stopped"))


    @dbus.service.method(CO2MONITOR_INTERFACE, in_signature='', out_signature='s')
    def status(self):
        if self.loop.is_running():
            return(_("running"))
        else:
            return(_("stopped"))
            

    @dbus.service.method(CO2MONITOR_INTERFACE, in_signature='', out_signature='')
    def quit(self):
        self.logger.info(_("stopping co2monitor..."))
        self.loop.quit()
        self.logger.info(_("stopped co2monitor"))


class LogThread(threading.Thread):
    def __init__(self, devicefile):
        self.devicefile = devicefile

    def run():
        pass
        

