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

#RETURN ERROR CODES
ERROR_IMPORT_LIBRARIES_FAIL = -1
ERROR_INVALID_GLADE_FILE = -2
ERROR_GLADE_FILE_READ = -3

TMPDEFAULTPUZZLE = '83....5....29..6....7..8.39..8....2..4.....569............3...8.83.2..6.7.5...29.'

def import_failed(err):
    """ Fail with a friendlier message when imports fail. """
    msglines = (
        'Missing some third-party libraries.',
        'Please install requirements using \'pip\' or your package manager.',
        'The import error was:',
        '    {}'
    )
    print('\n'.join(msglines).format(err))
    sys.exit(ERROR_IMPORT_LIBRARIES_FAIL)

try:
    import os
    import sys
    import math
    from copy import deepcopy

    # Gtk and related
    from gi import require_version as gi_require_version
    gi_require_version('Gtk', '3.0')
    from gi.repository import Gtk
    from gi.repository import Gdk, GdkPixbuf, Pango
    import cairo
    gi_require_version('PangoCairo', '1.0')
    from gi.repository import PangoCairo

    # Configuration and message boxes
    from auxiliary import SectionConfig, OptionConfig
    from auxiliary import MessageBox

    # Localization
    import locale
    from locale import gettext as _

except ImportError as eximp:
    import_failed(eximp)

ROWS = {}
COLS = {}
SQUARES = {}
for xcounter in range(3):
    col = xcounter * 3
    colindex = col * 9
    rowindex = col
    for ycounter in range(3):
        COLS[colindex+(ycounter*9)] = [colindex + (ycounter*9) + x for x in range(9)]
        ROWS[rowindex+ycounter] = [rowindex + ycounter + 9 * x for x in range(9)]
        row = ycounter * 3
        square = col * 9 + row
        SQUARES[square] = [square, square+1, square+2,
                9+square, 10+square, 11+square,
                18+square, 19+square, 20+square]

def find_best_ratio(cr, square, ratio, fname, thelist):
    bigger_from_ratio = []
    cr.save()
    x = square['x']
    y = square['y']
    W = square['W']
    H = square['H']
    cr.translate(x,y)
    layout = PangoCairo.create_layout(cr)
    tmpsize = W  * ratio
    fsize = math.floor(tmpsize)
    if tmpsize - math.floor(fsize) >= 0.4:
        fsize = math.floor(fsize) + 0.5
    font_desc = '{} {:0.1f}'.format(fname, fsize)
    desc = Pango.font_description_from_string(font_desc)
    layout.set_font_description(desc)
    for samplechar in thelist[1:]:
        layout.set_text(samplechar, -1)
        haha = layout.get_pixel_extents()
        if haha[0].width > fsize:
            bigger_from_ratio.append(haha[0].width)
        if haha[0].height > fsize:
            bigger_from_ratio.append(haha[0].height)
    cr.restore()
    if len(bigger_from_ratio):
        new_ratio = fsize / max(bigger_from_ratio)  * ratio
        #print('ratio',new_ratio)
        return new_ratio
    else:
        #print('ratio',ratio)
        return ratio

def print_in_square( cr, square, ratio, samplechar, fname, color=(0,0,0)):
    cr.save()
    x = square['x']
    y = square['y']
    W = square['W']
    H = square['H']
    cr.translate(x,y)
    layout = PangoCairo.create_layout(cr)
    fsize = W  * ratio
    #remove size
    rstring = fname.split(' ')
    if rstring[-1].isnumeric():
        font_desc = ' '.join(rstring[:-1])
    else:
        font_desc = fname
    new_fname = '{} {:0.1f}'.format(font_desc, fsize)
    layout.set_font_description(Pango.font_description_from_string(new_fname))
    layout.set_text(samplechar, -1)
    PangoCairo.update_layout(cr, layout)
    pixel_extents = layout.get_pixel_extents()

    left = (W - pixel_extents[0].width) / 2 - pixel_extents[0].x
    top = (H - pixel_extents[0].height) / 2 - pixel_extents[0].y

    cr.move_to(left,top)
    cr.set_source_rgb(*color)
    PangoCairo.update_layout(cr, layout)
    PangoCairo.show_layout (cr, layout)

    cr.restore()

class DrawPuzzle():
    def __init__(self, thelist=[' ','1','2','3','4','5','6','7','8','9'], thescale = 80, thefontname="Monospace Bold"):
        self.thelist = thelist
        self.thefontname = thefontname
        self.ratio = thescale / 100

    def draw_it(self,  puzzlenums, cr, w, h):
        cr.set_line_width(4)
        cr.set_source_rgb(0,0,0)
        size = min(w,h)-10
        xcenter = (w - 4) / 2
        ycenter = (h - 4) / 2
        startx = xcenter - (size/2)
        starty = ycenter - (size/2)
        cr.set_source_rgb(0,0,0)
        cr.rectangle(startx , starty, size, size)
        cr.stroke()
        the_9 = size / 9
        cr.set_line_width(1)

        square={}
        square['x'] = 0
        square['y'] = 0
        square['W'] = square['H'] = the_9 - 4
        use_ratio = find_best_ratio(cr, square, self.ratio, self.thefontname, self.thelist)
        for rowcounter in range(9):
            for colcounter in range(9):
                cr.set_source_rgb(0,0,0)
                num = colcounter * 9 + rowcounter + 1
                the_x = colcounter * the_9
                the_y = rowcounter * the_9
                d_num = puzzlenums[num-1]['num']
                d_const = puzzlenums[num-1]['const']
                d_sel = puzzlenums[num-1]['sel']
                color = (1,0,0) if puzzlenums[num-1]['red'] else (0,0,0)
                samplechar = self.thelist[d_num]

                # Rectangle
                if d_sel:
                    cr.set_source_rgba(0,0.5,1,0.10)
                elif d_const:
                    cr.set_source_rgb(0.95,0.95,0.95)
                else:
                    cr.set_source_rgb(1,1,1)
                cr.rectangle(startx + the_x + 1, starty + the_y + 1, the_9-2, the_9-2)
                cr.fill()

                cr.rectangle(startx + the_x , starty + the_y, the_9, the_9)
                cr.set_source_rgb(0,0,0)
                cr.stroke()

                # Digit
                square={}
                square['x'] = startx + the_x + 2
                square['y'] = starty + the_y + 2
                square['W'] = square['H'] = the_9-4
                print_in_square(cr, square, use_ratio, samplechar, self.thefontname, color)

        the_3 = size / 3
        cr.set_line_width(3)
        for rowcounter in range(3):
            for colcounter in range(3):
                the_x = colcounter * the_3
                the_y = rowcounter * the_3
                cr.rectangle(startx + the_x , starty + the_y, the_3, the_3)
                cr.stroke()
        return startx, starty, the_9


class Puzzle():
    def __init__(self,  puzzle=TMPDEFAULTPUZZLE, thelist=None, thescale=110, thehistory=None, thefont="Monospace Bold"):
        self.replay = None#(thehistory != None)
        self.the_9 = None
        self.an_9 = None
        self.puzzlenums = {}
        self.start_nums = [int(puzzle[xcounter]) if puzzle[xcounter] != '.' else 0 for xcounter in range(81)]
        #self.history = {}
        self.history = thehistory if thehistory else []
        self.play_history = []
        self.undos = 0
        self.current_cell = 0
        if self.replay:
            pass
        else:
            for xcounter in range(81):
                n = int(puzzle[xcounter]) if puzzle[xcounter] != '.' else 0
                self.puzzlenums[xcounter] = {'num' : n,
                        'const' : True if n else False,
                        'sel' : False,
                        'red' : False,
                        'prev' : None}
            #self.history[0] = deepcopy(self.puzzlenums)
        self.w = None
        self.h = None
        self.has_errors = False
        self.solved = False
        self.drawing = DrawPuzzle(thelist, thescale, thefont)

    def get_remaining(self):
        pieces = {}
        for x in range(10):
            pieces[x] = 0
        for item in self.puzzlenums:
            pieces[self.puzzlenums[item]['num']] += 1
        return pieces

    def draw(self, cr, w, h):
        an_X, an_Y, an_9 = self.startx, self.starty, self.the_9 = self.drawing.draw_it(self.puzzlenums, cr, w, h)
        self.an_9 = an_9
        return an_9

    def get_duplicates(self, oflist):
        response = {}
        for cell_index in oflist[:]:
            cell_num = self.puzzlenums[cell_index]['num']
            if cell_num:
                for others in oflist[:]:
                    if cell_index != others:
                        if self.puzzlenums[others]['num'] == cell_num:
                            response[cell_index] = True
                            response[others] = True
        return response

    def check_puzzle(self):
        dups = {}
        for alist in COLS:
            tmpdups = self.get_duplicates(COLS[alist])
            for d in tmpdups:
                dups[d] = True
        for alist in ROWS:
            tmpdups = self.get_duplicates(ROWS[alist])
            for d in tmpdups:
                dups[d] = True
        for alist in SQUARES:
            tmpdups = self.get_duplicates(SQUARES[alist])
            for d in tmpdups:
                dups[d] = True
        has_zeroes = False
        for xcounter in range(81):
            self.puzzlenums[xcounter]['red'] = xcounter in dups
            if self.puzzlenums[xcounter]['num'] == 0:
                has_zeroes = True
        self.has_errors = len(dups)
        if not self.has_errors and not has_zeroes:
            self.solved = True

    def append_to_history(self, previousnum):
        self.history.append(str(previousnum) + str(self.puzzlenums[self.current_cell]['num']) + str(self.current_cell))

    def go_to_last_position(self):
        for xcounter in range(len(self.history) - self.undos):
            amove = self.history[xcounter]
            num = int(amove[1])
            cell = int(amove[2:4])
            self.puzzlenums[cell]['num'] = num
