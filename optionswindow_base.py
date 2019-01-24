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

Since we are in python, any subclass of this class
will take over any method with the same name.
So do not declare here methods that exist also in the subclass.
(subclass is the class that uses the class here as Base.
Imagine the subclass as a super-duper class,
although in computing superclass is the base class)
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
    from gi.repository import GdkPixbuf

    # Configuration and message boxes
    from auxiliary import SectionConfig, OptionConfig
    from auxiliary import MessageBox

    # Load base window class and static methods
    from optionswindow_statics import *
    from numberpicker import NumberPicker

except ImportError as eximp:
    print(eximp)
    sys.exit(-1)

class OptionsWindowBase(object):
    #FIXME: fix the docstring.
    """ Main window with all components. """

    def __init__(self, application, *args, **kwargs):
        # Set the app
        self.myparent = None
        self.passed_args = kwargs['args_to_pass']

        # bind settings,options to a class variable
        global settings
        settings = self.settings
        global options
        options = self.options

        # Before builder.
        self._run_before_builder()

        # Read GUI from file and retrieve objects from Gtk.Builder
        thebuilder = Gtk.Builder()
        thebuilder.set_translation_domain(self.Application.id)
        try:
            thebuilder.add_from_file(os.path.join(self.Application.MyArgs.APP_DIR,
                'ui',
                'optionswindow.glade')
                )
            thebuilder.connect_signals(self)
        except GObject.GError:
            print("Error reading GUI file")
            raise

        # Fire up the main window
        self.OptionsWindow = thebuilder.get_object("OptionsWindow")
        self.OptionsWindow.set_application(self.Application)
        self._get_from_builder(thebuilder)
        self._post_initialisations()

        self.OptionsWindow.show()

#********* Auto created "class defs" START ************************************************************
    def _run_before_builder(self):
        self.fontaspect = 0.85
        self.example_int = 9
        self.example_char = '9'
        self.fontfamily = 'Sans'
        self.canceled = True
        self.squares = {}

        self.thedicts = THEDICTS

        self.color = (0,0,0)

    def _get_from_builder(self, builder):
        """ Create self names for easy access. """
        self.MainBox = builder.get_object('MainBox')
        self.adjustment1 = builder.get_object('adjustment1')
        self.box3 = builder.get_object('box3')
        self.boxForDisplay = builder.get_object('boxForDisplay')
        self.boxForFooter = builder.get_object('boxForFooter')
        self.buttonBackColorSelect = builder.get_object('buttonBackColorSelect')
        self.buttonCancel = builder.get_object('buttonCancel')
        self.buttonForeColorSelect = builder.get_object('buttonForeColorSelect')
        self.buttonSave = builder.get_object('buttonSave')
        self.checkbuttonShowOnlyBoard = builder.get_object('checkbuttonShowOnlyBoard')
        self.checkbuttonShowPieces = builder.get_object('checkbuttonShowPieces')
        self.checkbuttonShowTimer = builder.get_object('checkbuttonShowTimer')
        self.drawingareaExample = builder.get_object('drawingareaExample')
        self.eventbox1 = builder.get_object('eventbox1')
        self.eventbox2 = builder.get_object('eventbox2')
        self.eventbox3 = builder.get_object('eventbox3')
        self.eventbox4 = builder.get_object('eventbox4')
        self.eventbox5 = builder.get_object('eventbox5')
        self.eventbox6 = builder.get_object('eventbox6')
        self.eventbox7 = builder.get_object('eventbox7')
        self.eventbox8 = builder.get_object('eventbox8')
        self.eventbox9 = builder.get_object('eventbox9')
        self.eventboxForDrawingSample = builder.get_object('eventboxForDrawingSample')
        self.fontbutton1 = builder.get_object('fontbutton1')
        self.gridDictionaries = builder.get_object('gridDictionaries')
        self.image1 = builder.get_object('image1')
        self.label1 = builder.get_object('label1')
        self.label10 = builder.get_object('label10')
        self.label11 = builder.get_object('label11')
        self.label2 = builder.get_object('label2')
        self.label3 = builder.get_object('label3')
        self.label4 = builder.get_object('label4')
        self.label5 = builder.get_object('label5')
        self.label6 = builder.get_object('label6')
        self.label7 = builder.get_object('label7')
        self.label8 = builder.get_object('label8')
        self.label9 = builder.get_object('label9')
        self.labelVersion = builder.get_object('labelVersion')
        self.radiobuttonDict1 = builder.get_object('radiobuttonDict1')
        self.scale1 = builder.get_object('scale1')
        self.viewportSample = builder.get_object('viewportSample')

        # Connect signals existing in the Glade file.
        builder.connect_signals(self)

        # Connect generated by OCPgenerator signals:
        # to builder's main window
        self.OptionsWindow.connect('delete-event', self.on_OptionsWindow_delete_event)
        self.OptionsWindow.connect('destroy', self.on_OptionsWindow_destroy)
        self.OptionsWindow.connect('size-allocate', self.on_OptionsWindow_size_allocate)
        self.OptionsWindow.connect('window-state-event', self.on_OptionsWindow_window_state_event)
        self.buttonBackColorSelect.connect('clicked', self.on_buttonBackColorSelect_clicked)
        self.buttonCancel.connect('clicked', self.on_buttonCancel_clicked)
        self.buttonForeColorSelect.connect('clicked', self.on_buttonForeColorSelect_clicked)
        self.buttonSave.connect('clicked', self.on_buttonSave_clicked)
        self.checkbuttonShowPieces.connect('clicked', self.on_checkbuttonShowPieces_toggled)
        self.checkbuttonShowTimer.connect('clicked', self.on_checkbuttonShowTimer_toggled)

    def _post_initialisations(self):
        """ Do some extra initializations.

        Display the version if a labelVersion is found.
        Set defaults (try to load them from a configuration file):
            - Window size and state (width, height and if maximized)
        Load any custom settings from a configuration file.
        """
        if 'trigger_before_exit' in self.passed_args:
            # must be a function on calling class
            self.trigger_before_exit = self.passed_args['trigger_before_exit']
            self.return_parameters = None

        # Bind message boxes.
        self.MessageBox = MessageBox(self.OptionsWindow, self.Application)
        self.msg = self.MessageBox.Message
        self.are_you_sure = self.MessageBox.are_you_sure

        # Reset MainWindow to a default or previous size and state.
        width = settings.get('width', 350)
        height = settings.get('height', 350)
        self.OptionsWindow.set_title(self.Application.MyArgs.localizedname + " - " + _('Options'))
        self.OptionsWindow.resize(width, height)
        self.OptionsWindow.set_icon(self.Application.icon)
        if settings.get_bool('maximized', False):
            self.OptionsWindow.maximize()

        # Set the label for labelVersion
        self.labelVersion.set_label(self.Application.MyArgs.version)
        self.labelVersion.set_tooltip_text(_("Version of this window:") + "\n" + VERSIONSTR)

        # Load any other settings here.
        self.current_dict_name = 'standard'
        self.thedicts['custom'] = self.thedicts['standard'].copy()
        tmpcustomdict = options.get('custom_dict', '').split(',')
        if len(tmpcustomdict) == 10 and tmpcustomdict[0].strip() == '':
            self.thedicts['custom'] = ['']
            for x in range (1, 10):
                self.thedicts['custom'].append(tmpcustomdict[x].strip())
        self.show_dicts()
        self.OptionsWindow.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("#228b22"))#forest green

        simple = options.get('show_simple', False )
        self.checkbuttonShowPieces.set_active(not simple and options.get('show_pieces', False))
        self.checkbuttonShowTimer.set_active(not simple and options.get('show_timer', True))
        self.checkbuttonShowOnlyBoard.set_active(simple)
        scale = options.get('font_scale', 100)
        self.adjustment1.set_value(scale / 100)
        self.fontaspect = self.adjustment1.get_value()
        self.fontfamily = options.get('font', self.fontbutton1.get_font_name())
        self.fontbutton1.set_font_name(self.fontfamily)
        #print('self.fontbutton1.get_font_name()', self.fontbutton1.get_font_name())

        digits_dict = options.get('dict_to_use', 'standard')
        for b in self.gridDictionaries.get_children():
            if hasattr(b, 'tag') and b.tag == digits_dict:
                b.set_active(True)
                break

        self.picker = self.AppArgs.picker
        #self.image1.set_from_pixbuf(pixbuf)

#********* Auto created handlers START *********************************
    def on_NUM_button_press_event(self, widget, event, *args):
        """ Handler for eventbox1.button-press-event. """
        self.example_int = int(widget.get_child().get_label())
        self.drawingareaExample.queue_draw()

    def on_adjustment1_changed(self, widget, *args):
        """ Handler for adjustment1.changed. """
        pass

    def on_buttonBackColorSelect_clicked(self, widget, *args):
        """ Handler for buttonBackColorSelect.clicked. """
        self.msg_not_yet()

    def on_buttonCancel_clicked(self, widget, *args):
        """ Handler for buttonCancel.clicked. """
        self.exit_requested()

    def on_buttonForeColorSelect_clicked(self, widget, *args):
        """ Handler for buttonForeColorSelect.clicked. """
        self.select_fore_color()

    def on_buttonSave_clicked(self, widget, *args):
        """ Handler for buttonSave.clicked. """
        self.canceled = False
        self.exit_requested()

    def on_checkbuttonShowOnlyBoard_toggled(self, widget, *args):
        """ Handler for checkbuttonShowOnlyBoard.toggled. """
        boolval = self.checkbuttonShowOnlyBoard.get_active()
        self.checkbuttonShowPieces.set_sensitive(not boolval)
        self.checkbuttonShowTimer.set_sensitive(not boolval)

    def on_checkbuttonShowPieces_toggled(self, widget, *args):
        """ Handler for checkbuttonShowPieces.clicked. """
        pass

    def on_checkbuttonShowTimer_toggled(self, widget, *args):
        """ Handler for checkbuttonShowTimer.clicked. """
        pass

    def on_drawingareaExample_draw(self, widget, cr, *args):
        """ Handler for drawingareaExample.draw. """
        sizes = self.eventboxForDrawingSample.get_allocation()
        min_size = min(sizes.width, sizes.height)
        self.working_restangle = Gdk.Rectangle()
        self.working_restangle.x = int((sizes.width - min_size) / 2)
        self.working_restangle.y = int((sizes.height - min_size) / 2)
        self.working_restangle.width = int(min_size)
        self.working_restangle.height = int(min_size)
        self.draw_example(cr)
        #print('on_drawingareaExample_draw', self.fontfamily)

    def on_eventboxForDrawingSample_button_press_event(self, widget, event, *args):
        """ Handler for eventboxForDrawingSample.button-press-event. """
        pass

    def on_fontbutton1_font_set(self, widget, *args):
        """ Handler for fontbutton1.font-set. """
        self.fontfamily = self.fontbutton1.get_font_name()
        self.drawingareaExample.queue_draw()

    def on_radiobuttonDict1_toggled(self, widget, *args):
        """ Handler for radiobuttonDict1.toggled. """
        if widget.get_active():
            self.current_dict_name = widget.tag
            self.drawingareaExample.queue_draw()

    def on_scale1_change_value(self, widget, scroll, new_value, *args):
        """ Handler for scale1.change-value. """
        if new_value <= self.adjustment1.get_upper():
            self.fontaspect = new_value
            self.drawingareaExample.queue_draw()

#********* Auto created handlers END ***********************************

#********* Standard handlers START *************************************
    def msg_not_yet(self):
        self.msg(_('Not yet implemented'))

    def on_buttonAbout_clicked(self, widget, *args):
        """ Handler for buttonAbout.clicked. """
        #TODO: Check if used.
        self.MessageBox.AboutBox()

    def on_buttonExit_clicked(self, widget, *args):
        """ Handler for buttonExit.clicked. """
        #TODO: Check if used.
        self.exit_requested()

    def on_OptionsWindow_delete_event(self, widget, event, *args):
        """ Handler for our main window: delete-event. """
        return (self.exit_requested())

    def on_OptionsWindow_destroy(self, widget, *args):
        """ Handler for our main window: destroy. """
        return (self.exit_requested('from_destroy'))

    def on_OptionsWindow_size_allocate(self, widget, allocation, *args):
        """ Handler for our main window: size-allocate. """
        self.save_my_size()

    def on_OptionsWindow_window_state_event(self, widget, event, *args):
        """ Handler for our main window: window-state-event. """
        settings.set('maximized',
            ((int(event.new_window_state) & Gdk.WindowState.ICONIFIED) != Gdk.WindowState.ICONIFIED) and
            ((int(event.new_window_state) & Gdk.WindowState.MAXIMIZED) == Gdk.WindowState.MAXIMIZED)
            )
        self.save_my_size()

#********* Standard handlers END ***************************************
#********* Standard exit defs START *********************************************************
    def exit_requested(self, *args, **kwargs):
        """ Final work before exit. """
        self.OptionsWindow.set_transient_for()
        self.OptionsWindow.set_modal(False)
        self.set_unhandled_settings()# also saves all settings
        if 'from_destroy' in args:
            return True
        else:
            # Check if we should provide info to caller
            if 'trigger_before_exit' in self.passed_args:
                self.trigger_before_exit(exiting = True,
                    return_parameters = self.return_parameters)
            self.OptionsWindow.destroy()

    def present(self):
        """ Show the window. """
        pass

    def save_my_size(self):
        """ Save the window size into settings, if not maximized. """
        if not settings.get_bool('maximized', False):
            width, height = self.OptionsWindow.get_size()
            settings.set('width', width)
            settings.set('height', height)

    def set_unhandled_settings(self):
        """ Set, before exit, any settings not applied during the session.

        Additionally, flush all settings to .conf file.
        """
        # Set any custom settings
        # which where not setted (ex. on some widget's state changed)
        if not self.canceled:
            options.set('dict_to_use', self.current_dict_name)
            options.set('custom_dict', ','.join(self.thedicts['custom']))
            scale = self.adjustment1.get_value()
            options.set('font_scale', int(scale * 100))
            options.set('font', self.fontbutton1.get_font_name())
            boolval = self.checkbuttonShowOnlyBoard.get_active()
            options.set('show_simple', boolval )
            options.set('show_pieces', (not boolval) and self.checkbuttonShowPieces.get_active())
            options.set('show_timer', (not boolval) and self.checkbuttonShowTimer.get_active())

            options.set('fore_color',','.join(['{:0.4f}'.format(x) for x in self.color]))
        # Save all settings
        settings.save()
#********* Standard exit defs END **************************************
#********* Auto created "class defs" END **************************************************************

#********* Window class  END***************************************************************************
