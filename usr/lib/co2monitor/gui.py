#!/usr/bin/env python3
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
import logging


# logger
logger = logging.getLogger(__name__)

class Co2MonitorWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self) # initialize the window

        self.label = Gtk.Label("Co2monitor!")
        self.add(self.label)

        # basic signal connect
        self.connect("delete-event",Gtk.main_quit)

    def run(self):
        self.show_all() # show everything
        Gtk.main() # main loop


