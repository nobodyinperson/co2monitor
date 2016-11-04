#!/usr/bin/env python3
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
import logging
import os


# logger
logger = logging.getLogger(__name__)

# get user system language
user_language = os.environ.get('LANGUAGE')
try: # try to use gettext for translations
    import gettext # translations
    # init translation
    lang = gettext.translation(
        'co2monitor', # domain
        localedir='/usr/share/co2monitor/lang', # language folder
        languages=[user_language.split("_")[0]]
        )
    lang.install() # install the language
except: # use the strings from here
    _ = lambda s:s


class Co2MonitorWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self) # initialize the window

        self.label = Gtk.Label(_("Welcome to Co2monitor!"))
        self.add(self.label)

        # basic signal connect
        self.connect("delete-event",Gtk.main_quit)

    def run(self):
        self.show_all() # show everything
        Gtk.main() # main loop


