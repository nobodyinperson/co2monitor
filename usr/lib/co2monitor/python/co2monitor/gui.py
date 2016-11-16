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
        # set up the quit signals
        self.setup_signals(
            signals = [signal.SIGINT, signal.SIGTERM, signal.SIGHUP],
            handler = self.quit
        )


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
        self.mainloop.run()
        self.logger.debug(_("GLib main loop ended."))

    # quit the gui
    def quit(self, *args):
        self.logger.debug(_("Received quitting signal."))
        self.mainloop.quit()

