#!/usr/bin/env python
import dbus
import dbus.service
import dbus.mainloop.glib

import logging
import configparser 
import signal
import threading
import os
import csv
import time

from gi.repository import GLib

from . import device
from . import utils

# define names
CO2MONITOR_BUSNAME    = "de.nobodyinperson.co2monitor"
CO2MONITOR_INTERFACE  = "de.nobodyinperson.co2monitor"
CO2MONITOR_OBJECTPATH = "/de/nobodyinperson/co2monitor"

###############
### Service ###
###############
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
        dbus.mainloop.glib.threads_init()
        GLib.threads_init()

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

    @dbus.service.method(CO2MONITOR_INTERFACE, in_signature='s', out_signature='')
    def start_device_logging(self, devicefile):
        self.logger.info(_("received request to start logging on device {}").format(
            devicefile))
        thread = LogThread(devicefile = devicefile) # logger object
        self.logger.info(_("starting logging thread for device {}").format(
            devicefile))
        # same logger as service
        thread.set_logger(self.logger)
        # same config as service
        thread.set_config(self.config)
        thread.daemon = True # let this thread be a daemon thread
        thread.start()


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


#################
### LogThread ###
#################
class LogThread(threading.Thread, dbus.service.Object):
    def __init__(self, devicefile):
        # by default, log!
        self.do_data_logging = True
        # initially set the standard logger
        self.set_logger(logging.getLogger(__name__))
        # initially set an empty configuration
        self.set_config(configparser.ConfigParser())

        # use glib as default mailoop for dbus
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        dbus.mainloop.glib.threads_init()
        GLib.threads_init()

        systembus = dbus.SystemBus() # the system bus
        systembus.request_name(CO2MONITOR_BUSNAME) # request the bus name
        bus_name = dbus.service.BusName(CO2MONITOR_BUSNAME, systembus) # create bus name

        self.devicefile = devicefile

        # set up the device
        self.device = device.co2device(self.devicefile)

        # register the object on the bus name
        objectpath = "/".join([CO2MONITOR_OBJECTPATH,
            os.path.basename(self.devicefile)])
        dbus.service.Object.__init__(self, bus_name, objectpath)
        self.update_status(_("idle"))
        threading.Thread.__init__(self)


    # set the config
    def set_config(self, config):
        self.config = config

    # set the logger
    def set_logger(self, logger):
        self.logger = logger

    @dbus.service.method(CO2MONITOR_INTERFACE, in_signature='', out_signature='s')
    def status(self):
        return self.current_status

    def update_temperature(self, temperature):
        self.current_temperature = temperature

    @dbus.service.method(CO2MONITOR_INTERFACE, in_signature='', out_signature='d')
    def temperature(self):
        try:    temperature = float(self.current_temperature) # try to convert to float
        except: temperature =           -99999                # fake measurement
        return temperature

    def update_co2(self, co2):
        self.current_co2 = co2

    @dbus.service.method(CO2MONITOR_INTERFACE, in_signature='', out_signature='i')
    def co2(self):
        try:    co2 = int(self.current_co2) # try to convert to int
        except: co2 = -99999                # fake measurement
        return co2

    # kindly stop logging
    @dbus.service.method(CO2MONITOR_INTERFACE, in_signature='', out_signature='')
    def please_stop_now(self):
        self.logger.debug(_("Request to stop logging on device {} - will terminate soon...").format(self.devicefile))
        self.do_data_logging = False

    # update the current status
    def update_status(self, status):
        self.current_status = status

    # shut this thread down
    def quit(self):
        self.logger.debug(_("Shutting down logging thread of device {}").format(
            self.devicefile))
        self.remove_from_connection()
        sys.exit()

    # logloop
    def run(self):
        self.logger.info(_("Starting data logging on device {}").format(
            self.devicefile))
        datafolder = self.config.get('data-logging','datafolder')

        self.update_status(_("creating data directory"))
        if not os.path.isdir(datafolder): # check if data folder does not exist
            os.makedirs(datafolder,0o755) # create data folder
        self.update_status(_("created data directory"))
        
        fieldnames = ['time','temperature','co2']

        datafile   = "{folder}/co2monitor-{device}-{time}.csv".format(
            time = time.strftime("%Y%m%d%H%M%S",time.localtime()),
            device = os.path.basename(self.devicefile),
            folder = datafolder
            )

        # warmup
        warmuptime = self.config.getint('data-logging','warmuptime')
        waittime = round(max(0,warmuptime - self.device.uptime()))
        if waittime > 0:
            self.update_status(_("device warmup"))
            self.logger.info(
                _("giving the device another {} seconds of warmup time...").format(
                waittime))
            for i in range(waittime): 
                if not self.do_data_logging: break # stop if asked to stop
                time.sleep(1) # sleep one second

        self.update_status(_("opening data file"))
        with open(datafile, 'w') as csvfile: # open file
            self.update_status(_("opened data file"))
            self.logger.info(_("opened {} for data logging.").format(datafile))

            writer = csv.DictWriter(csvfile, fieldnames = fieldnames)

            self.update_status(_("writing header to file"))
            writer.writeheader()
            measold = {}
            while self.do_data_logging: # read as long as you are allowed
                # self.logger.debug(_("reading from device {}...").format(self.devicefile))
                self.update_status(_("reading from device"))
                meas = self.device.read() # read from device
                # self.logger.debug(_("read {} from device {}").format(meas,self.devicefile))

                self.update_status(_("postprocessing raw data"))
                if isinstance(meas, dict): # measurement worked
                    # set time
                    meas['time'] = time.strftime("%Y-%m-%d %H:%M:%S",
                                                 time.localtime())
    
                    anything_new = False

                    temperature     =    meas.get('temperature',None)
                    temperature_old = measold.get('temperature',None)
                    co2     =    meas.get('co2',None)
                    co2_old = measold.get('co2',None)

                    if temperature != temperature_old:
                        self.update_temperature(temperature)
                        anything_new = True
                    if co2 != co2_old:
                        self.update_co2(co2)
                        anything_new = True
                    # check if this measurement introduces something new
                    if anything_new:
                        # measurement is not only None
                        if not temperature is None or not co2 is None:
                            self.update_status(_("writing data to file"))
                            writer.writerow(meas) # write
                            csvfile.flush() # writeout
    
                    
                    # update old measurements
                    measold.update(meas)
                else: # measurement didn't work
                    break # exit logloop

            # logging ended
            self.logger.info(_("stopped logging."))
        self.logger.debug(_("closed data logging file '{}'").format(datafile))

        self.logger.info(_("Stopped data logging on device {}").format(
            self.devicefile))
        # quit
        self.quit() 
            

