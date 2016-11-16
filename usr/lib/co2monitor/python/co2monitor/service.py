#!/usr/bin/env python
import dbus
import dbus.service
import dbus.mainloop.glib

import logging
import configparser 
import signal
import threading

from gi.repository import GLib

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
        # set up the quit signals
        self.setup_signals(
            signals = [signal.SIGINT, signal.SIGTERM, signal.SIGHUP],
            handler = self.please_stop_now
        )

        # use glib as default mailoop for dbus
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

        self.loop = GLib.MainLoop() # create mainloop

        systembus = dbus.SystemBus() # the system bus
        systembus.request_name(CO2MONITOR_BUSNAME) # request the bus name
        bus_name = dbus.service.BusName(CO2MONITOR_BUSNAME, systembus) # create bus name
        # register the object on the bus name
        dbus.service.Object.__init__(self, bus_name, CO2MONITOR_OBJECTPATH)

    def setup_signals(self, signals, handler):
        """
        This is a workaround to signal.signal(signal, handler)
        which does not work with a GLib.MainLoop() for some reason.
        Thanks to: http://stackoverflow.com/a/26457317/5433146
        args:
            signals (list of signal.SIG... signals): the signals to connect to
            handler (function): function to be executed on these signals
        """
        def install_glib_handler(sig): # add a unix signal handler
            GLib.unix_signal_add( GLib.PRIORITY_HIGH, 
                sig, # for the given signal
                handler, # on this signal, run this function
                sig # with this argument
                )

        for sig in signals: # loop over all signals
            GLib.idle_add( # 'execute'
                install_glib_handler, sig, # add a handler for this signal
                priority = GLib.PRIORITY_HIGH  )

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
        

