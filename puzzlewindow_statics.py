#!/usr/bin/env python3

MOVE_NEW = 0
MOVE_UNDO = 1
MOVE_REDO = 2

def col_row_of_point_in_restangle(thepoint, therestangle):

    if thepoint.x < therestangle.x:return -1, -1
    if thepoint.x > therestangle.x + therestangle.width:return -1, -1
    if thepoint.y < therestangle.y:return -1, -1
    if thepoint.y > therestangle.y + therestangle.height:return -1, -1

    x_in = int(thepoint.x - therestangle.x)
    y_in = int(thepoint.y - therestangle.y)

    W_of_1 = int(therestangle.width / 9 )
    H_of_1 = int(therestangle.height / 9)

    col = x_in // W_of_1
    row = y_in // H_of_1
    return col, row

def col_row_of_x_y_in_restangle(x, y, therestangle):

    if x < therestangle.x:return -1, -1
    if x > therestangle.x + therestangle.width:return -1, -1
    if y < therestangle.y:return -1, -1
    if y > therestangle.y + therestangle.height:return -1, -1

    x_in = int(x - therestangle.x)
    y_in = int(y - therestangle.y)

    W_of_1 = int(therestangle.width / 9 )
    H_of_1 = int(therestangle.height / 9)

    col = x_in // W_of_1
    row = y_in // H_of_1
    return col, row

