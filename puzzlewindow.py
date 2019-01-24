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
    import datetime

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
    from puzzlewindow_base import PuzzleWindowBase
    from puzzlewindow_statics import *

    from puzzle import Puzzle

except ImportError as eximp:
    print(eximp)
    sys.exit(-1)

class PuzzleWindow(PuzzleWindowBase):
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

        self.targets = None # Gtk.TargetList.new([])
        self.dragaction = Gdk.DragAction.PRIVATE
        self.number_picked = None
        self.init_picker_done = False

        super().__init__(self,  *args, **kwargs)

    def _eb_drag_begin(self, widget, context):
        #print(dir(context))
        if len(widget.get_children()[0].get_label().strip()):
            self.number_picked = widget.my_tag
            #print(self.AppArgs.picker.subpixbufs[5].get_width())
        else:
            self.number_picked = None

    def _eb_drag_end(self, widget, context):
        self.number_picked = None

    def fill_pieces(self):
        """ Fill label with remaining pieces. """
        #do nothing if user has show_pieces=False
        if not self.listboxPieces.get_visible():
            return
        remaining_dict = self.puzzle.get_remaining()
        #print('remaining_dict',remaining_dict)
        thelistbox = self.listboxPieces
        allchildren = thelistbox.get_children()
        for achild in allchildren[:]:
            achild.destroy()
        label = Gtk.Label(_('Remaining numbers:'))
        thelistbox.add(label)
        label.set_visible(True)
        for number_counter in range(9):
            thestr1 = self.AppArgs.strings_to_use[number_counter+1]
            remaining = 9-remaining_dict[number_counter+1]
            label = Gtk.Label(thestr1 * remaining )
            label.set_xalign (0)
            eb = Gtk.EventBox()
            eb.add(label)
            if remaining>0:
                eb.connect('button-press-event', self.on_piece_pressed, number_counter+1)
                eb.drag_source_set(Gdk.ModifierType.BUTTON1_MASK, self.targets, self.dragaction)
                #eb.drag_source_set(Gdk.ModifierType.BUTTON1_MASK, [Gtk.TargetEntry("the num", Gtk.TargetFlags.SAME_APP, x)], Gdk.DragAction.PRIVATE )
                eb.connect_after("drag-begin", self._eb_drag_begin)
                eb.drag_source_add_text_targets()
                eb.connect("drag-end", self._eb_drag_end)
                #eb.drag_source_set_icon_name("gtk-open")
                eb.drag_source_set_icon_pixbuf(self.AppArgs.picker.subpixbufs[number_counter+1])
                #print('fill_pieces', self.AppArgs.picker.subpixbufs[number_counter+1].get_width())
                label.set_tooltip_text( _("Drag «{}» to the board...").format(thestr1))
            else:
                label.set_tooltip_text( _("You have placed all «{}».").format(thestr1))
            thelistbox.add(eb)
            eb.set_visible(True)
            eb.my_tag = str(number_counter+1)

            label.set_visible(True)

        label = Gtk.Label( str(remaining_dict[0]))
        label.set_xalign (0.5)
        eb = Gtk.EventBox()
        eb.add(label)
        thelistbox.insert(eb,1)
        eb.set_visible(True)
        label.set_visible(True)
        theimage = Gtk.Image.new_from_icon_name("gtk-zoom-100",Gtk.IconSize.DND )
        theimage.set_visible(True)
        self.remaining_image = theimage
        thelistbox.add(theimage)
        #theimage.set_from_pixbuf ()

        self.listboxPieces.show_all()

    def on_piece_pressed(self, widget, event, *args):
        """ Handler for any piece.button-press-event.

        Triggered if label with remaining pieces is pressed. """
        #TODO: show all x's in the puzzle.
        #print('on_piece_pressed',args, self.AppArgs.picker.subpixbufs[args[0]].get_width())
        self.remaining_image.set_from_pixbuf(self.AppArgs.picker.subpixbufs[args[0]])
        return False

    def on_piece_released(self, widget, event, *args):
        """ Handler for any piece.button-release-event.

        Triggered if button on label with remaining pieces is released. """
        #TODO: reset "show all x's in the puzzle".
        #print('on_piece_released')
        #self.number_picked = None
        #return False
        pass

    def passed_time(self):
        """ Show time passed.

        Show time if option is enabled.
        Don't use this while playing history.
        """
        if self.playing_history:
            return False
        self.timepassed = datetime.datetime.utcnow() - self.timer_started
        allsecs = self.timepassed.seconds
        secs = int(allsecs % 60)
        mins = allsecs // 60 % 60
        hrs = allsecs // 3600
        #if diff.days:
        prefix = '>' if self.timepassed.days else ''
        tmp = prefix + '{0:02d}:{1:02d}:{2:02d}'.format(hrs, mins, secs)#[:7]
        self.labelClock.set_label(tmp)
        return True and not self.exiting

    def picker_hide(self):
        '''Hide the picker. '''
        if self.is_picker_visible:
            self.AppArgs.picker.PickerWindow.hide()
            self.is_picker_visible = False

    def picker_resize(self, optional=None):
        if self.puzzle and self.puzzle.the_9:
            #set also best ratio
            if self.AppArgs.picker.PickerWindow.get_size() != self.puzzle.the_9-2:
                #self.picker_size = self.puzzle.the_9
                self.AppArgs.picker.image_resize(self.puzzle.the_9-2)
                self.fill_pieces()

    def picker_show(self, event, col, row):
        '''Show picker if not in constant cell. '''
        if self.puzzle.puzzlenums[self.puzzle.current_cell]['const']:
            return False
        if event.button == 1:
            #find window start
            window_x, window_y = self.PuzzleWindow.get_window().get_root_coords(0, 0)
            #find eventbox start
            full_size = self.eventboxPuzzle.get_allocation()
            #find working restangle start
            restangle_x = self.working_restangle.x + 5
            restangle_y = self.working_restangle.y + 5
            size = self.working_restangle.width - 10
            #the size of one cell
            the_9 = size / 9
            arow_x = the_9 * col
            arow_y = the_9 * row

            left = window_x + restangle_x + full_size.x + arow_x
            top = window_y + restangle_y + full_size.y + arow_y

            self.AppArgs.picker.PickerWindow.move(left, top)
            self.AppArgs.picker.PickerWindow.show_all()
            self.AppArgs.picker.PickerWindow.grab_focus()
            self.is_picker_visible = True
            return True

    def puzzle_continue(self):
        ''' Continue last saved game.

        If last game was solved start a new.
        If saved values are not valid start a new.
        If nothing was done start a new.
        '''
        self.puzzle = Puzzle(self.AppArgs.history.board ,
                self.AppArgs.strings_to_use ,
                self.AppArgs.font_scale,
                self.AppArgs.history.history,
                self.AppArgs.font
                )
        self.puzzle.undos = options.get('last_undos', 0)
        self.puzzle.go_to_last_position()
        self.puzzle.check_puzzle()
        self.drawingareaPuzzle.queue_draw()
        self.set_undoredo()
        oldtimediff = datetime.timedelta(
                days=self.AppArgs.history.days,
                seconds=self.AppArgs.history.seconds)
        self.fill_pieces()
        self.timer_started = datetime.datetime.utcnow() - oldtimediff
        GObject.timeout_add(500, self.passed_time)

    def puzzle_move_cursor(self, tocell):
        '''Paint new selected cell. '''
        self.puzzle.puzzlenums[self.puzzle.current_cell]['sel'] = False

        self.puzzle.current_cell = tocell
        self.puzzle.puzzlenums[self.puzzle.current_cell]['sel'] = True
        self.drawingareaPuzzle.queue_draw()
        return True

    def puzzle_set_number(self, anumber=-1, undoredo = MOVE_NEW):
        '''Set a number in selected cell.

        If undo or redo is required use history.
        '''
        previousnum = self.puzzle.puzzlenums[self.puzzle.current_cell]['num']
        if undoredo == MOVE_NEW:
            if self.puzzle.undos:
                #remove all undos from history. We start a new node
                self.puzzle.history = self.puzzle.history[:-self.puzzle.undos]
                self.puzzle.undos = 0
            self.puzzle.puzzlenums[self.puzzle.current_cell]['num'] = anumber
            self.puzzle.append_to_history(previousnum)
        elif undoredo == MOVE_UNDO:
            self.puzzle.undos += 1
            lastplayed = self.puzzle.history[-self.puzzle.undos]
            lastcell = int(lastplayed[2:])
            previousnum = int(lastplayed[0])
            anumber = int(lastplayed[1:2])
            self.puzzle_move_cursor(lastcell)
            self.puzzle.puzzlenums[self.puzzle.current_cell]['num'] = previousnum
        elif undoredo == MOVE_REDO:
            lastplayed = self.puzzle.history[(len(self.puzzle.history) - self.puzzle.undos)]
            lastcell = int(lastplayed[2:])
            anumber = int(lastplayed[1:2])
            self.puzzle.undos -= 1
            self.puzzle_move_cursor(lastcell)
            self.puzzle.puzzlenums[self.puzzle.current_cell]['num'] = anumber
        self.puzzle.check_puzzle()
        self.drawingareaPuzzle.queue_draw()
        self.set_undoredo()
        self.fill_pieces()
        #print('filled after set a piece')
        #print(['{}:{},'.format(x, self.puzzle.puzzlenums[x]['num']) for x in self.puzzle.puzzlenums])
        if self.puzzle.solved:
            self.show_solved()
        return True

    def puzzle_start(self):
        '''Start a new puzzle. '''
        options.set('last_undos', 0)
        options.set('last_history', '')
        options.set('last_solved', False)
        options.set('last_board', self.AppArgs.current_board)
        self.puzzle = Puzzle(self.AppArgs.current_board,
                self.AppArgs.strings_to_use,
                self.AppArgs.font_scale,
                None,
                self.AppArgs.font
                )
        self.fill_pieces()
        self.timer_started = datetime.datetime.utcnow()
        GObject.timeout_add(500, self.passed_time)

    def response_from_picker(self, *args, **kwargs):
        '''Triggered from picker. '''
        #print(kwargs)
        self.is_picker_visible = False
        if kwargs['number_as_str'] != None and kwargs['number_as_str'] != '-1':
            self.puzzle_set_number(int(kwargs['number_as_str']))
        return True

    def set_undoredo(self):
        '''Write history in conf and show/hide undo-redo buttons. '''
        self.buttonUndo.set_sensitive((len(self.puzzle.history) > 0 and self.puzzle.undos < len(self.puzzle.history)))
        self.buttonRedo.set_sensitive( self.puzzle.undos > 0)

    def show_solved(self):
        """ Show that puzzle is solved and call exit window. """
        now = datetime.datetime.utcnow()
        #print('now,self.timer_started',now,self.timer_started)
        diff = now - self.timer_started
        #self.return_parameter = (True, str(diff)[2:7])

        if self.is_picker_visible:
            self.AppArgs.picker.PickerWindow.hide()
        self.exiting = True
        self.msg('{}\n ({}: {})'.format(_('Solved!'),
            _('time passed'),
            str(diff)[2:7])
        )
        self.exit_requested()

    def get_cell_number(self, widget, event):
        ebW = widget.get_allocated_width()
        imgW = ebW//9#self.image1.get_allocated_width()
        ebH = widget.get_allocated_height()
        imgH = ebH//9#self.image1.get_allocated_height()
        xstart = (ebW - imgW)//2
        ystart = (ebH - imgH)//2
        cellsize = int(imgW // 9)
        cellx = event.x // (imgH // 9)
        celly = event.y // (imgW // 9)
        if event.x > xstart and event.x < ebW - xstart:
            if event.y > ystart and event.y < ebH - ystart:
                thex = event.x -  xstart
                they = event.y -  ystart
                cell_number = 9*(event.y // (imgW // 9)) + event.x // (imgH // 9) + 1
        else:
            cell_number = -1
        return int(cell_number), cellsize, cellx, celly
