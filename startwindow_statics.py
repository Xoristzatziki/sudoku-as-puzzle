#!/usr/bin/env python3
import os
import sys
import io

import tempfile

# Gtk and related
from gi import require_version as gi_require_version
gi_require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Pango
from gi.repository import GdkPixbuf
from gi.repository.GdkPixbuf import Pixbuf, Colorspace
gi_require_version('PangoCairo', '1.0')
from gi.repository import PangoCairo

import cairo

from puzzle import find_best_ratio, print_in_square

thelist = ['0','1','2','3','4','5','6','7','8','9']
def get_imagename(thewindow, thelist=thelist, fontaspect = 0.85, fname = 'Sans', color=(0,0,0)):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1024, 1024)
    cr = cairo.Context(surface)
    create_the_image(cr, thelist, fontaspect, fname, color)

    fd, tmppath = tempfile.mkstemp()
    surface.write_to_png(tmppath)
    surface.finish()
    return tmppath

def create_the_image(cr, thelist, fontaspect, fname, color):
    size = 1024
    square={}
    square['x'] = square['y'] = square['W'] = square['H'] = int(size/3)
    use_ratio = find_best_ratio(cr, square, fontaspect, fname, thelist)
    #print('thelist',thelist, fname, color, use_ratio)
    for rowcounter in range(3):
        for colcounter in range(3):
            the_x = colcounter * (size / 3)
            the_y = rowcounter * (size / 3)
            square['W'] = square['H'] = int(size/3)
            square['x'] = the_x
            square['y'] = the_y
            cr.rectangle( square['x'] ,  square['y'], square['W'], square['H'])
            cr.stroke()
            samplechar = thelist[rowcounter * 3 + colcounter +1]
            print_in_square(cr, square, fontaspect, samplechar, fname, color)
