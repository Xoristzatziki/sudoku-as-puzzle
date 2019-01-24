# Sudoku As Puzzle
==================

Customizable sudoku. Beta version. Sudoku that can use any character from any font as digit. Only single characters can be used. Currently has predefined Arabic, Greek, chinese, Persian and Tibetan numbers.

Dependencies:
-------------

Sudoku-Gtk has several GTK-related dependencies. If you are already creating GTK
apps then you may have some of these installed already.

Also requires qqwing to be installed.
Installe it  with your package manager, like [apt](https://wiki.debian.org/apt-get).

There may be others, I will fill in the missing dependencies as they are found.
Message me or file an issue if you run into errors.

In general:
-----------

This is a beta version. Still requires the generator to call the qqwing.

Download all files to some directory and either change the mode of sudoku-gtk.py to be executable
or run it using:

`python3 sudoku-gtk.py`

TODO:
-----

* Embed libqqwing module.
* Replay and continue.
* Fix presentation of characters, probably using PangoCairo.
* Create deb.

Compatibility:
--------------

Sudoku-Gtk is designed for
[PyGTK3](http://python-gtk-3-tutorial.readthedocs.org/en/latest/install.html),
and [Python 3](https://www.python.org/downloads/).

File an issue if there is something you would like to see.

Contributions:
--------------

Contributions are welcome. That's what this repo is for.
File an issue, or send me a pull request if you would like to see a
feature added to Sudoku-Gtk.

