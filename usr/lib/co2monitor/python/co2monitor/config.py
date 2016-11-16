#!/usr/bin/env python3

import os, glob
import gettext
import logging
import configparser

# install the user language globally
def install_language_globally():
    # get user system language
    user_language = os.environ.get('LANGUAGE','##')
    # init translation
    lang = gettext.translation(
        domain    = 'co2monitor',                  # domain
        localedir = '/usr/share/co2monitor/lang',  # language folder
        languages = [user_language.split("_")[0]], # user language
        fallback  = True
        )
    lang.install() # install the language

def get_configuration():
    # a ConfigParser
    config = configparser.ConfigParser()
    # all configuration files
    configfiles = glob.glob("/etc/co2monitor/*.conf")
    # read all configuration files
    config.read(configfiles)
    # return the ConfigParser
    return config

# setup logging from configuration file section
def setup_logger_from_config(logger,section,config=None):
    if not isinstance(config, configparser.ConfigParser):
        # get the configuration
        config = get_configuration()

    # no logging wanted
    if not config.getboolean(section,'logging'): 
        logger.propagate = False # switch off logging
        return logger

    # initialize logging
    # set loglevel possiblities
    loglevels = {
    'debug'   :logging.DEBUG,
    'info'    :logging.INFO,
    'warning' :logging.WARNING,
    'error'   :logging.ERROR,
    'critical':logging.CRITICAL
    }

    # get loglevel from config
    loglevel = loglevels.get(config.get(section,'loglevel').lower(),
                         logging.WARNING)
    # get file from config
    logfile = config.get(section,'logfile')

    # create a handler
    if os.path.exists(logfile):
        # create a file handler and log to that file
        handler = logging.FileHandler(filename = logfile)
    else:
        # create a stream handler and log to stderr
        handler = logging.StreamHandler()
    # set the loglevel for the handler and the logger
    handler.setLevel(loglevel)
    logger.setLevel(loglevel)

    # create a formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(module)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
        )

    # add the formatter to the handler
    handler.setFormatter(formatter)

    # add the handler to the logger
    logger.addHandler(handler)

    # return the logger
    return logger

    

