#!/usr/bin/env python3
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
from gi.repository import GLib
import logging
import os
import configparser
import signal


class Co2MonitorGui():
    def __init__(self):
        # initially set the standard logger
        self.set_logger(logging.getLogger(__name__))
        # initially set an empty configuration
        self.set_config(configparser.ConfigParser())

    # build the gui
    def load_builder(self):
        # get a GTK builder
        self.builder = Gtk.Builder()
        # load the gladefile
        self.builder.add_from_file(self.config.get('gui-general','gladefile'))

    # set the config
    def set_config(self, config):
        self.config = config

    # set the logger
    def set_logger(self, logger):
        self.logger = logger

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
        # can't use Gtk.main() because of a bug that prevents proper SIGINT
        # handling. use Glib.MainLoop() directly instead.
        self.mainloop = GLib.MainLoop() # main loop
        # signal.signal(signal.SIGINT, signal.SIG_DFL)
        self.logger.debug(_("Starting GLib main loop..."))
        try:
            self.mainloop.run()
        except KeyboardInterrupt:
            self.quit()
        self.logger.debug(_("GLib main loop ended."))

    # quit the gui
    def quit(self, *args):
        self.logger.debug(_("Received quitting signal."))
        self.mainloop.quit()

