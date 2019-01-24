#!/usr/bin/env python3
#FIXME:
# This is an example class generated using a bare glade file.
#
#FIXME:
"""
    Copyright (C) ilias iliadis, 2019-01-16; ilias iliadis <iliadis@kekbay.gr>

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

"""
        WARNING !!!

Since we are in python, any method here will override base class.
So do not declare here methods that exist also in the base class.
"""
#FIXME: correct the version
__version__ = '0.0.30'
VERSIONSTR = 'v. {}'.format(__version__)

try:
    import os
    import sys
    import subprocess
    import weakref
    import gc

    # Gtk and related
    from gi import require_version as gi_require_version
    gi_require_version('Gtk', '3.0')
    from gi.repository import Gtk
    from gi.repository import Gdk
    from gi.repository import GObject

    # Configuration and message boxes
    from auxiliary import SectionConfig, OptionConfig
    from auxiliary import MessageBox

    # Load base window class and static methods
    from startwindow_base import StartWindowBase
    from startwindow_statics import *
    from puzzlewindow import PuzzleWindow
    from optionswindow import OptionsWindow

    from numberpicker import NumberPicker

except ImportError as eximp:
    print(eximp)
    sys.exit(-1)

class StartWindow(StartWindowBase):
    #FIXME: fix the docstring.
    """ Main window with all components. """

    def __init__(self, application, *args, **kwargs):
        self.Application = application
        self.AppArgs = self.Application.MyArgs
        # define and bind settings, options to a class variable
        global settings
        global options
        settings = SectionConfig(self.Application.id, self.__class__.__name__)
        options = OptionConfig(self.Application.id)
        self.settings = settings
        self.options = options
        super().__init__(self,  *args, **kwargs)
        #print(dir(Gtk.IconSize))

    def get_a_puzzle(self):
        """ Read aboard from qqwing.

        Only difficulty easy (qqwing easy).
        """
        b = subprocess.run(['qqwing', "--generate", "--difficulty", "easy", "--compact"], stdout=subprocess.PIPE).stdout.decode('utf-8')
        return b.replace('\n','')

    def get_valid_history(self):
        """ Check history.

        Values in settings
        ------------------
        last_solved : a boolean
        last_board : a string
        last_time : a comma separated string
            holds minutes and seconds
        last_undos : an integer
        last_history : string
            comma separated list of 0000 moves.
            First two numbers are the number and second two are the cell.

        """
        self.AppArgs.history.is_valid = False
        if options.get('last_solved', False):
            return _('Last puzzle solved.\nStarting new game.')
        settings_history = options.get('last_history','')
        thehistory = []
        if len(settings_history.strip()):
            thehistory = [x.strip() for x in settings_history.split(',')]
        timepassed = options.get('last_time','')
        splitted_time_str = timepassed.split(",")
        if len(splitted_time_str) != 2:
            return _('No valid time saved.\nStarting new game.')
        if len(thehistory) < 1:
            return _('No moves in saved puzzle.\nStarting new game.')
        board_string = options.get('last_board', '').strip()
        board = [x for x in board_string]
        if len(board) != 81:
            return _('No valid board saved.\nStarting new game.')
        self.AppArgs.history.board = board
        self.AppArgs.history.days = int(splitted_time_str[0])
        self.AppArgs.history.seconds = int(splitted_time_str[1])
        self.AppArgs.history.undoes = options.get('last_undos',0)
        self.AppArgs.history.history = thehistory
        self.AppArgs.history.is_valid = True
        return ''

    def open_OptionsWindow(self):
        args_to_pass = {}
        args_to_pass['trigger_before_exit'] = self.return_from_OptionsWindow
        args_to_pass['is_modal'] = True
        self.OptionsWindow = OptionsWindow(application = self.Application,
                args_to_pass = args_to_pass)
        self.OptionsWindow.present()
        self.StartWindow.hide()

    def open_PuzzleWindow(self, tocontinue=False):
        self.AppArgs.current_board = self.get_a_puzzle()
        msg = self.get_valid_history()
        if tocontinue:
            if not self.AppArgs.history.is_valid:
                self.msg(msg)
                tocontinue = False
        args_to_pass = {}
        args_to_pass['trigger_before_exit'] = self.return_from_PuzzleWindow
        args_to_pass['show_history'] = False #TODO:get show_history
        args_to_pass['continue'] = tocontinue

        self.a_PuzzleWindow = PuzzleWindow(application = self.Application,
                args_to_pass = args_to_pass)
        #GObject.idle_add(self.run_check, ['a','b'])
        self.a_PuzzleWindow.present()
        self.StartWindow.hide()

    def run_check(self, *args, **kwars):
        print(kwars)
        self.a_PuzzleWindow.picker_resize()
        print(self.a_PuzzleWindow.drawingareaPuzzle.get_allocated_width(), self.AppArgs.picker.scaled_pixbuf_width)
        return False

    def reload_options(self):
        """ Reload all options in Application.Myars and display them. """
        self.Application.reload_options()
        self.show_info()

    def return_from_OptionsWindow(self, *args, **kwargs):
        """ Reload options and reset pickerc pixbuf. """
        self.StartWindow.show()
        self.reload_options()
        self.reset_picker()
        return self.__class__.__name__

    def return_from_PuzzleWindow(self, *args, **kwargs):
        self.StartWindow.show()
        return self.__class__.__name__

    def show_info(self):
        """ Show current options. """
        text = _("Font") + ':\t' + str(self.AppArgs.font) + '\n'
        text += _("Font aspect") + ':\t' + str(self.AppArgs.font_scale) + '\n'
        text += _("Show only board") + ':\t' + str(self.AppArgs.show_simple) + '\n'
        text += _("Show timer") + ':\t' + str(self.AppArgs.show_timer) + '\n'
        text += _("Show remaining pieces") + ':\t' + str(self.AppArgs.show_pieces) + '\n'
        text += _("Digits") + ':\t' + ','.join(self.AppArgs.strings_to_use[1:])
        self.labelInfo.set_label(text)

    def get_new_picker_pixbuf(self):
        """ Get a pixbuf to use in number picker window.

        TODO: convert surface to pixbuf directly
        """
        an_imagefile = get_imagename(self.StartWindow,
                self.AppArgs.strings_to_use,
                self.AppArgs.font_scale/100,
                self.AppArgs.font,
                self.AppArgs.fore_color
                )
        a_picker_pixbuf = GdkPixbuf.Pixbuf().new_from_file(an_imagefile)
        os.remove(an_imagefile)
        return a_picker_pixbuf

    def create_picker(self):
        """ Create a picker object. """
        if self.AppArgs.picker:
            self.reset_picker()
            return
        picker_pixbuf = self.get_new_picker_pixbuf()

        args_to_pass = {}
        args_to_pass['thelist'] = self.AppArgs.strings_to_use
        args_to_pass['parent'] = None #self.StartWindow #dummy parent. Should be reperented.
        args_to_pass['numbers_pixbuf'] = picker_pixbuf
        args_to_pass['response_from_picker'] = None

        self.AppArgs.picker = NumberPicker(args_to_pass=args_to_pass)
        self.is_picker_visible = False

    def reset_picker(self):
        """ Resize the pixbuf to fit in new squares. """
        if self.AppArgs.picker:
            self.AppArgs.picker.pixbuf = self.get_new_picker_pixbuf()

