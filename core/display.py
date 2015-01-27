# encoding: utf-8
#
# set up screen and background
# used by all draw calls - passed as arg to groups
# minimal api, more todo if/when needed

from pygame import Surface, DOUBLEBUF, OPENGL
from pygame.display import flip
from pygame.display import set_mode

from config import *

import game
import display

size = width, height
clearColor = (0,) * 3

screen = set_mode(size) #, OPENGL | DOUBLEBUF)
screen.fill(clearColor)
background = Surface(screen.get_size())
background.fill(clearColor)

messages = {'update': 'update',
            'reset': 'reset',
            'clear': 'clear'}

def update():

  flip()

def clear(color=None, rect=None, flags=0):

  if color is None:
    color = display.clearColor

  screen.fill(color, rect, flags)

def draw(surf, dest, area=None, flags=0):

  screen.blit(surf, dest, area, flags)

def reset(w=None, h=None):

  if w is None:
    w = display.size

  if h is None:
    w, h = w

  display.screen = set_mode((w, h)) #, OPENGL | DOUBLEBUF)
  display.screen.fill(display.clearColor)
  display.background = Surface(display.screen.get_size())
  display.background.fill(display.clearColor)

@game.msg.handler('display')
def displayMessageHandler(msg):

  try:
    if isinstance(msg, str):
      eval('display.' + display.messages[msg] + '()')
  except KeyError:
    print ' Error: display has no message:', msg
    raise
