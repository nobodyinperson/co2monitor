#!/usr/bin/env python3
import logging
import configparser
import sys, os, glob
import csv
import time
import signal

from . import device

# logger
logger = logging.getLogger(__name__)

##########################
### monitoring service ###
##########################
class co2monitorService(object):
    def __init__(self):
        # handle SIGINT and SIGTERM
        self.kill_now = False
        signal.signal(signal.SIGINT, self.please_stop_now)
        signal.signal(signal.SIGTERM, self.please_stop_now)

        # set up config
        self.config_setup()

        # set up logging
        self.logging_setup()

    # kindly stop logging
    def please_stop_now(self, signum=None, frame=None):
        logger.info(" ".join(["received stop signal {},",
            "will terminate soon..."]).format(signum))
        self.kill_now = True

    # set up config
    def config_setup(self):
        # read config
        configfiles = glob.glob("/etc/co2monitor/*")
        self.config = configparser.ConfigParser()
        self.config.read(configfiles)

    # set up logging according to config
    def logging_setup(self):
        # initialize logging
        # set loglevel possiblities
        loglevels = {
            'debug'   :logging.DEBUG,
            'info'    :logging.INFO,
            'warning' :logging.WARNING,
            'error'   :logging.ERROR,
            'critical':logging.CRITICAL
            }

        # set up logging with loglevel from config
        loglevel = loglevels.get(self.config.get('service-logging','loglevel'),
                                 logging.WARNING)
        logfile = self.config.get('service-logging','logfile')
        if logfile is None: # if no logfile was specified
            logfile = "/var/log/co2monitor.log"

        logging.basicConfig(
            filename=logfile, level=loglevel,
            format="%(asctime)s [%(levelname)s] %(module)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
            )

        # no logging wanted
        if not self.config.getboolean('service-logging','logging'): 
            logger.propagate = False # switch off logging
            
    # set up the device
    def setup_device(self, devicefile):
        self.device = device.co2device(devicefile)

    # loop 
    def logloop(self):
        datafolder = self.config.get('data-logging','datafolder')

        if not os.path.isdir(datafolder): # check if data folder does not exist
            os.makedirs(datafolder,0o755) # create data folder
        
        fieldnames = ['time','temperature','co2']
        datafile   = "{folder}/co2monitor-{time}.csv".format(
            time = time.strftime("%Y%m%d%H%M%S",time.localtime()),
            folder = datafolder
            )

        # warmup
        warmuptime = self.config.getint('data-logging','warmuptime')
        logger.info("giving the device {} seconds of warmup time...".format(
            warmuptime))
        for i in range(warmuptime): # Loop over each sleep second
            if self.kill_now: break # stop if asked to stop
            time.sleep(1) # sleep one second

        with open(datafile, 'w') as csvfile: # open file
            logger.info("opened {} for data logging.".format(datafile))
            writer = csv.DictWriter(csvfile, fieldnames = fieldnames)

            writer.writeheader()
            measold = {}
            while not self.kill_now: # read as long as you are allowed
                meas = self.device.read() # read from device

                if isinstance(meas, dict): # measurement worked
                    # set time
                    meas['time'] = time.strftime("%Y-%m-%d %H:%M:%S",
                                                 time.localtime())
    
                    # check if this measurement introduces something new
                    if meas.get('temperature',None)    != \
                       measold.get('temperature',None) or \
                       meas.get('co2',None) != measold.get('co2',None):
                        # measurement is not only None
                        if not meas.get('temperature',None) is None or \
                           not meas.get('co2',None) is None:
                            writer.writerow(meas) # write
                            csvfile.flush() # writeout
    
                    
                    # update old measurements
                    measold.update(meas)
                else: # measurement didn't work
                    break # exit logloop
                    #sys.exit(2) # stop!

            # logging ended
            logger.info("stopped logging.")
        logger.debug("closed data logging file '{}'".format(datafile))
