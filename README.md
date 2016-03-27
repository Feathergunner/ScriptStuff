This is a collection of python-scripts/-programs I work on from time to time.

## BLOCK ##
is a short script that takes a screenshot and displays it fullscreen, thus "blocking" the screen. (Finished, but may be expanded in the future)

## CALENDAR ##
is a script that creates a calender that fits on a single DinA4-page. One can specify holidays and birthdays within a txt-file, these days will be colored. The script creates a tex-file full of tikz-code, which is compiled to pdf by pdflatex.
* Usage: set holidays etc. in file data.txt (see file for information), set year in calendar.py (last line), then run `python calendar.py`
* Finished, but may be expanded in the future

## MANDALAS ##
is becoming a script to create mandala-like circular patterns.
* A lot of work in progress.

## STARMAKER ##
is a script to create recursive (pseudo-fractal) stars of colored lines. Depending on a large set of parameters, a lot of different outputs are possible. Parameters are specified by a file (see starmaker/Init). For example outputs, see starmaker/Example_Output.
* Usage: create parameter file (see any file in starmaker/Init for information), then run `python stars.py path-to-parameterfile`
* Almost finished, some functionalities not yet implemented. May be expanded in the future.

These scripts have been coded and tested on ubuntu with python 2.7.