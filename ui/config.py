# encoding: utf-8
#

from os.path import join as osJoin
from pygame.font import init, Font
import game

init()

uiLabelFontName = osJoin(game.res, 'freesansbold.ttf')
uiLabelSizeHint = 10

menuFontName = osJoin(game.res, 'freesans.ttf')
menuTitleFont = Font(menuFontName, 24)
menuSubFont = Font(menuFontName, 10)
menuDefaultFont = Font(menuFontName, 18)
