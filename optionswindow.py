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
    from optionswindow_base import OptionsWindowBase
    from optionswindow_statics import *

    from puzzle import find_best_ratio, print_in_square

except ImportError as eximp:
    print(eximp)
    sys.exit(-1)

class OptionsWindow(OptionsWindowBase):
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

    def draw_example(self, cr):
        samplechar = self.thedicts[self.current_dict_name][self.example_int]
        fname = self.fontfamily
        ratio = self.fontaspect
        size = self.drawingareaExample.get_allocated_height()

        square={}
        square['x'] = square['y'] = square['W'] = square['H'] = int(size/3)
        use_ratio = find_best_ratio(cr, square, ratio, fname, self.thedicts[self.current_dict_name])
        self.picker_size = int(size/3)
        for rowcounter in range(3):
            for colcounter in range(3):
                the_x = colcounter * (size / 3)
                the_y = rowcounter * (size / 3)
                square['W'] = square['H'] = int(size/3)
                square['x'] = the_x
                square['y'] = the_y
                cr.rectangle( square['x'] ,  square['y'], square['W'], square['H'])
                cr.stroke()
                samplechar = self.thedicts[self.current_dict_name][rowcounter * 3 + colcounter +1]
                print_in_square(cr, square, use_ratio, samplechar, fname, self.color)

    def hide_picker(self, *args, **kwargs):
        if self.is_picker_visible:
            self.is_picker_visible = False
        self.picker.hide()

    def on_any_custom_changed(self, widget, *args):
        index = widget.entry_tag
        char = widget.get_text()
        self.thedicts['custom'].pop(index)
        self.thedicts['custom'].insert(index,char)

    def response_from_picker(self, *args, **kwargs):
        self.is_picker_visible = False
        return True

    def select_fore_color(self):
        dlg = Gtk.ColorChooserDialog(_("a title"), self.OptionsWindow)
        response = dlg.run()
        #print(response,Gtk.ResponseType.OK, response == Gtk.ResponseType.OK)
        #print(dlg.get_rgba().to_string())
        if response == Gtk.ResponseType.OK:
            #thetuple = tuple(int(x) for x in dlg.get_rgba().to_string().split("(")[1].split(")")[0].split(","))
            dlgrgba = dlg.get_rgba()
            thetuple = (dlgrgba.red,dlgrgba.green,dlgrgba.blue)
            self.color = thetuple
            self.drawingareaExample.queue_draw()

        dlg.destroy()

    def show_dicts(self):
        """ Load and show the dictionaries.

        Load all from self.thedicts except 'standard' and 'custom'.
        A custom sort is used to sort localised names of dictionaries.
        """
        thegrid = self.gridDictionaries
        ycounter = 1
        self.radiobuttonDict1.tag = 'standard'
        for adict in sorted(self.thedicts, key=sorting):
            #print(adict)
            if adict != 'standard':
                theoption = Gtk.RadioButton(_(adict.title()))
                theoption.join_group(self.radiobuttonDict1)
                theoption.connect('toggled', self.on_radiobuttonDict1_toggled, theoption)
                theoption.tag = adict
                thegrid.attach(theoption,0,ycounter,1,1)
                xcounter = 1
                if adict == 'custom':
                    for x in range(9):
                        w = Gtk.Entry()
                        w.set_text(self.thedicts[adict][x+1])
                        w.set_width_chars(1)
                        w.set_max_width_chars(1)
                        w.entry_tag = x+1
                        w.connect('changed', self.on_any_custom_changed)
                        thegrid.attach(w,xcounter,ycounter,1,1)
                        xcounter += 1
                else:
                    for x in range(9):
                        label = Gtk.Label(self.thedicts[adict][x+1])
                        thegrid.attach(label,xcounter,ycounter,1,1)
                        xcounter += 1
                ycounter += 1
        thegrid.show_all()
