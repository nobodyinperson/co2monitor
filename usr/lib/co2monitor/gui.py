#!/usr/bin/env python3
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
import logging
import os
import configparser

# logger
logger = logging.getLogger(__name__)

class Co2MonitorGui():
    def __init__(self):
        pass

    # build the gui
    def load_builder(self):
        # get a GTK builder
        self.builder = Gtk.Builder()
        # load the gladefile
        self.builder.add_from_file(self.config.get('gui-general','gladefile'))

    # set up config
    def config_setup(self, configfiles):
        # read config
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
        loglevel = loglevels.get(self.config.get('gui-logging','loglevel'),
                                 logging.WARNING)

        logging.basicConfig(
            level=loglevel,
            format="%(asctime)s [%(levelname)s] %(module)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
            )

        # no logging wanted
        if not self.config.getboolean('gui-logging','logging'): 
            logger.propagate = False # switch off logging

    # set up the gui
    def setup_gui(self):
        # load the builder
        self.load_builder()
        
        # define handlers
        self.handlers = {
            "CloseWindow": self.quit,
            }

        self.builder.connect_signals(self.handlers)

        window = self.builder.get_object("window1")
        window.show_all()
        label = self.builder.get_object("label1")
        label.set_text(_("Welcome to Co2monitor!"))

    # run the gui
    def run(self):
        logger.debug(_("Starting GTK main loop..."))
        Gtk.main() # main loop
        logger.debug(_("GTK main loop ended."))

    # quit the gui
    def quit(self, *args):
        logger.debug(_("Received quitting signal."))
        Gtk.main_quit()

