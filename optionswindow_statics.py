#!/usr/bin/env python3

THEDICTS = {}
THEDICTS['standard'] = [' ','1','2','3','4','5','6','7','8','9']
THEDICTS['arabic'] = [' ','١','٢','٣','٤','٥','٦','٧','٨','٩']
THEDICTS['greek'] = [' ','α','β','γ','δ','ε','ς','ζ','η','θ']
THEDICTS['chinese'] = [' ','一','二','三','四','五','六','七','八','九']
THEDICTS['persian'] = [' ','۱','۲','۳','۴','۵','۶','۷','۸','۹']
THEDICTS['tibetan'] = [ ' ','༡','༢','༣','༤','༥','༦','༧','༨','༩']

def sorting(akey):
    return _(akey)

def col_row_of_point_in_restangle(thepoint, therestangle, thesquares):
    col = -1
    row = -1
    if thepoint.x < therestangle.x:
        pass
        #return -1, -1
    if thepoint.x > therestangle.x + therestangle.width:
        pass
    if thepoint.y < therestangle.y:
        pass
    if thepoint.y > therestangle.y + therestangle.height:
        pass
    else:
        x_in = int(thepoint.x - therestangle.x)
        y_in = int(thepoint.y - therestangle.y)
        W_of_1 = int(therestangle.width / thesquares )
        H_of_1 = int(therestangle.height / thesquares)
        col = x_in // W_of_1
        row = y_in // H_of_1

    return col, row
