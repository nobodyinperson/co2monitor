#!/usr/bin/env python3

import os, glob
import gettext
import logging
import configparser

# install the user language globally
def install_language_globally():
    # get user system language
    user_language = os.environ.get('LANG',     # first, try LANG 
                    os.environ.get('LANGUAGE', # then try LANGUAGE
                                   '##'))      # bogus value
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

    # if this section is not in the config, leave the logger as is
    try:    configsection = config[section]
    except: return logger

    # no logging wanted
    if not configsection.getboolean('logging'): 
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
    loglevel = loglevels.get(configsection.get('loglevel','debug').lower(),
                         logging.WARNING)
    # get file from config
    logfile = configsection.get('logfile', None)

    # create a handler
    if logfile:
        try:
            # create a file handler and log to that file
            handler = logging.FileHandler(filename = logfile, encoding="UTF-8")
        except: # e.g. file permissions don't work
            # create a stream handler and log to stderr
            handler = logging.StreamHandler()
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

    

