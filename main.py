#!/usr/bin/env python3
#FIXME:
"""
    Copyright (C) ilias iliadis, 2019; ilias iliadis <iliadis@kekbay.gr>

    This file is part of Sudoku Puzzle.

    Sudoku Puzzle is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Sudoku Puzzle is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Sudoku Puzzle.  If not, see <http://www.gnu.org/licenses/>.
"""

#FIXME: correct the version
APPID = "gr.kekbay.sudokupuzzle"
__version__ = '0.0.30'

#RETURN ERROR CODES
ERROR_IMPORT_LIBRARIES_FAIL = -1

try:
    import os
    import sys

    # Gtk and related
    from gi import require_version as gi_require_version
    gi_require_version('Gtk', '3.0')
    from gi.repository import Gtk
    from gi.repository import Gdk, GdkPixbuf, GObject, Gio, GLib

    # Localization
    import locale
    import gettext

    #from locale import gettext

    # Configuration and message boxes
    from auxiliary import SectionConfig, OptionConfig
    from auxiliary import MessageBox

    #At least a starting window must exist
    from startwindow import StartWindow
    from main_statics import *

except ImportError as eximp:
    print(eximp)
    sys.exit(ERROR_IMPORT_LIBRARIES_FAIL)

WHERE_AM_I = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
LOCALE_DIR = os.path.join(WHERE_AM_I, 'locale')

locale.setlocale(locale.LC_ALL, '')
locale.bindtextdomain(APPID, LOCALE_DIR)
#bind locale application wide
gettext.install(APPID, LOCALE_DIR)

settings = None # Will keep window related options
options = None # Will keep application wide options in a 'General Options' section

class CustomAppArgs:
    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        pass
    def __init__(self, *args, **kwargs):
        self.THEDICTS = THEDICTS
        self.custom_dict = [' ','1','2','3','4','5','6','7','8','9']

class History():
    def __init__(self, *args, **kwargs):
        self.board = ''
        self.days = 0
        self.seconds = 0
        self.undoes = 0
        self.history = []

class MyApplication(Gtk.Application):
    #FIXME: fix the docstring.
    """ Main entry of the application. """

    def __init__(self, *args, **kwargs):
        args2 = tuple()
        kwargs2 = {}

        self.id = APPID
        Gtk.Application.__init__(self, application_id=self.id , flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE)

        self.MyArgs = CustomAppArgs()
        #ensure name is the same with included in self.localizedname below
        self.MyArgs.name = 'Sudoku Puzzle'

        self.MyArgs.START_DIR = kwargs['START_DIR']
        self.MyArgs.APP_DIR = kwargs['APP_DIR']
        self.MyArgs.version = "v." + __version__

        self.MyArgs.history = History()

        self.MyArgs.localizedname = _("Sudoku Puzzle")#after binding text domain

        # Init the modules for settings (globally).
        self.set_config_file()

        self.MyArgs.picker = None
        self.MyArgs.current_board = None
        self.reload_options()

        # Load the icon file.
        theiconfile = os.path.join(self.MyArgs.APP_DIR, 'icons', 'logo.png')
        try:
            self.icon = GdkPixbuf.Pixbuf.new_from_file(theiconfile)
        except Exception:
            self.icon = None

        self.MyArgs.startwindow = None
        # Set any command line options here.
        self.add_main_option("test", ord("t"), GLib.OptionFlags.NONE,
                             GLib.OptionArg.NONE, _("Command line test"), None)

        self.connect("activate", self.my_activate)

    def set_config_file(self):
        global settings
        settings = SectionConfig(self.id, self.__class__.__name__)
        global options
        options = OptionConfig(self.id)

    def do_startup(self):
        Gtk.Application.do_startup(self)

    def my_activate(self, *args, **kwargs):

        # We only allow a single window and raise any existing ones
        if not self.MyArgs.startwindow:
            # Windows are associated with the «application ID»
            # when the last one is closed the application shuts down
            #FIXME: remove custom args if not needed
            some_custom_args = {}
            some_custom_args['haha'] = 'ena'
            # we can provide anything, even a local function
            some_custom_args['trigger_before_exit'] = self.custom_return_function
            self.MyArgs.startwindow = StartWindow(application = self,
                custom_args = some_custom_args)
        else:
            print('activated------------------------')
        self.MyArgs.startwindow.present()

    #FIXME: remove if not needed
    def custom_return_function(self, *args, **kwargs):
        """ Custom function to be triggered before opened window exit.

        Opened "startwindow" can use it to:
        - Return to this class a value.
        - Get from this class a processed value before exit.

        Notes
        -----
        This function will run BEFORE the opened window is destroyed.
        If you want to do something AFTER the window is destroyed,
        you should find other way or trigger.
        """
        # dummy printout of passed dict (kwargs)
        #print('== kwargs from child ==')
        #print(kwargs)
        #print('custom_return_function in main.py. kwargs form mainwindow:', kwargs)
        # dummy return of my class name
        return self.__class__.__name__

    def do_command_line(self, command_line):
        """ Parse command line and activate the application. """
        start_options = command_line.get_options_dict()
        if start_options.contains("test"):
            # This is printed on the main instance
            print("Test argument recieved")
        self.activate()
        return 0

    def reload_options(self):
        """ Reload all options.

        Sets various self.Application.MyArgs.
        strings_to_use : list of strings
        font : string
            a font name as shown in a font button
        font_scale : float 0-1
            a scale to use when drawing
        show_simple : boolean
            if user wants only the board
        show_timer : boolean
            shown only not show_simple is set
        show_pieces : boolean
            shown only not show_simple is set
        """
        tmpcustomdict = options.get('custom_dict', '').split(',')
        if len(tmpcustomdict) == 10 and tmpcustomdict[0].strip() == '':
            tmpcustomstrings = [x.strip() for x in tmpcustomdict]
        dict_to_use = options.get('dict_to_use', 'standard')
        with self.MyArgs as myargs:
            if dict_to_use in myargs.THEDICTS:
                myargs.strings_to_use = myargs.THEDICTS[dict_to_use]
            elif dict_to_use == 'custom':
                myargs.strings_to_use = tmpcustomstrings
            else:
                myargs.strings_to_use = myargs.THEDICTS['standard']
            myargs.font_scale = options.get('font_scale', 80)
            fname = options.get('font', 'Monospace 10')
            rstring = fname.split(' ')
            if rstring[-1].isnumeric():
                myargs.font = ' '.join(rstring[:-1])
            else:
                myargs.font = fname
            if myargs.font_scale > 90 or myargs.font_scale < 40:
                myargs.font_scale = 70
            myargs.show_simple = options.get_bool('show_simple', False)
            myargs.show_timer = options.get_bool('show_timer', True) and not myargs.show_simple #and myargs.show_simple
            myargs.show_pieces = options.get_bool('show_pieces', True) and not myargs.show_simple #and myargs.show_simple
            myargs.lasthistory = options.get('lasthistory', '')
            myargs.back_color = options.get('back_color', '')
            fore_color = (0,0,0)
            loaded_fore_color = options.get('fore_color', '0,0,0').split(',')
            if len(loaded_fore_color) == 3:
                 fore_color = tuple(float(x) for x in loaded_fore_color)
            myargs.fore_color = fore_color

if __name__ == '__main__':
    #Main entry point if running the program from command line
    START_DIR = os.path.dirname(os.path.abspath('.'))
    APP_DIR = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
    myapp = MyApplication(START_DIR=START_DIR, APP_DIR=APP_DIR)
    myapp.run(sys.argv)

