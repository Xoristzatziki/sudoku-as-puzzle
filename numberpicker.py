#!/usr/bin/env python3
"""
    Copyright (C) Ηλίας Ηλιάδης, 2018-04-11; ilias iliadis <iliadis@kekbay.gr>

    This file is part of Sudoku-Gtk.

    Sudoku-Gtk is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Sudoku-Gtk is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Sudoku-Gtk.  If not, see <http://www.gnu.org/licenses/>.
"""

#FIXME: correct the version
__version__ = '0.0.30'
VERSIONSTR = 'v. {}'.format(__version__)

# No need to check imports.
#They are already imported by main window class.
import os
import sys
# Gtk and related
from gi import require_version as gi_require_version
gi_require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GdkPixbuf
BILINEAR = GdkPixbuf.InterpType.BILINEAR

KEYVALUES = ['0','1','2','3','4','5','6','7','8','9','Escape','BackSpace','Delete']
KEYSTRINGS = ['0','1','2','3','4','5','6','7','8','9','-1','0','0']

class NumberPicker(object):
    def __init__(self, *args, **kwargs):
        self.passed_args = kwargs['args_to_pass']
        self.thelist = self.passed_args['thelist']
        self.myparent = self.passed_args['parent']
        #self.pixbuf = self.passed_args['numbers_pixbuf']
        self.pixbuf = self.passed_args['numbers_pixbuf'].copy()
        self.scaled_pixbuf = self.pixbuf.copy()
        self.scaled_pixbuf_width = self.scaled_pixbuf.get_width()
        self.response_from_picker = self.passed_args['response_from_picker']

        self.PickerWindow = Gtk.Window()

        aBox = Gtk.Box()

        self.main_Image = Gtk.Image()
        self.main_Image.set_from_pixbuf(self.scaled_pixbuf)
        aBox.pack_start(self.main_Image,True, True, 0 )
        self.PickerWindow.add(aBox)

        self.PickerWindow.set_transient_for(self.myparent)
        self.PickerWindow.set_modal(False)
        self.PickerWindow.set_decorated(False)
        self.PickerWindow.set_size_request(1,1)

        self.PickerWindow.connect('destroy', self.on_PickerWindow_destroy)
        self.PickerWindow.connect('key-release-event', self.on_PickerWindow_key_release_event)
        self.PickerWindow.connect('button-release-event', self.on_PickerWindow_button_release_event)
        self.PickerWindow.connect('focus-out-event', self.on_PickerWindow_focus_out_event)

        self.subpixbufs = {}
        self.create_digit_pibufs(self.pixbuf.get_width())

    def on_PickerWindow_focus_out_event(self, widget, event, *args):
        #print('I_lost_focus')
        #self.I_lost_focus()
        self.return_the_str('-1')

    def on_PickerWindow_button_release_event(self, widget, event, *args):
        if event.button == 3:
            return self.return_the_str('0')
        elif event.button == 1:
            #print('self.get_9cell_number(event)',self.get_9cell_number(event))
            return self.return_the_str(str(self.get_9cell_number(event)))
        return False # means not handled

    def on_PickerWindow_destroy(self, widget, *args):
        """ Handler for PickerWindow.destroy. """
        print('destroyed')
        return False

    def on_PickerWindow_key_release_event(self, widget, event, *args):
        """ Handler for PickerWindow.key-release-event. """
        txt = Gdk.keyval_name(event.keyval)
        if type(txt) == type(None):
            return
        txt = txt.replace('KP_', '')
        if txt in KEYVALUES:
            return self.return_the_str(KEYSTRINGS[KEYVALUES.index(txt)])
        try:
            aunichar = chr(Gdk.keyval_to_unicode(event.keyval))
            if aunichar and aunichar in self.thelist[1:]:
                return self.return_the_str(self.thelist.index(aunichar))
        except:
            pass
        return False # means not handled

    def image_resize(self, newsize):
        self.scaled_pixbuf = self.pixbuf.scale_simple(newsize, newsize, BILINEAR)
        self.main_Image.set_from_pixbuf(self.scaled_pixbuf)
        self.PickerWindow.resize(newsize, newsize)
        self.create_digit_pibufs(newsize)
        self.scaled_pixbuf_width = newsize
        #print('image resized')

    def exit_requested(self, *args):
        self.destroy()

    def present(self):
        """ Show the window. """
        pass

    def return_the_str(self, astring):
        #print(astring)
        self.PickerWindow.hide()
        self.response_from_picker(number_as_str = astring)
        return True

    def get_9cell_number(self, event):
        width, height = self.PickerWindow.get_size()
        return int(3*(event.y // (height // 3)) + event.x // (width // 3) + 1)

    def create_digit_pibufs(self, newsize):
        w_origin = h_origin = self.pixbuf.get_width()
        w = h = self.scaled_pixbuf.get_width()
        #w = h = newsize
        w3 = h3 = int(w_origin/3)
        w4 = h4 = int(w/2)
        if w4 < 32:
            w4 = h4 = 32
        #print(w, w3, w4)
        for xcounter in range(3):
            for ycounter in range(3):
                cell_number = 1 + ycounter * 3 + xcounter
                self.subpixbufs[cell_number] = self.pixbuf.new_subpixbuf(xcounter*w3, ycounter*h3, w3, h3)
                self.subpixbufs[cell_number] = self.subpixbufs[cell_number].scale_simple(w4, h4, BILINEAR)
                #print('new_sub_pixbuf', self.subpixbufs[cell_number].get_width())
                #self.subpixbufs[cell_number].savev("/home/ilias/Λήψεις/Προγραμματισμός1/testing/dragndrop/screenshot" + str(cell_number)+".png", "png", ["quality"], ["100"])
                #self.subpixbufs[cell_number] = self.subpixbufs[cell_number] .scale_simple(w4, h4, BILINEAR)
                #print('self.subpixbuf', self.subpixbufs[cell_number].get_width())

                #new_sub_pixbuf = self.pixbuf.new_subpixbuf(xcounter*w3,ycounter*h3,w3,h3)
                #self.subpixbufs[1 + ycounter * 3 + xcounter] = self.pixbuf.new_subpixbuf(xcounter*(w/3),ycounter*(w/3),w/3,h/3).scale_simple(newsize * 0.7, newsize * 0.7, GdkPixbuf.InterpType.BILINEAR)
                #self.subpixbufs[1 + ycounter * 3 + xcounter] = new_sub_pixbuf.scale_simple(int(newsize * 0.3),int(newsize * 0.3), BILINEAR)
                #del new_sub_pixbuf
