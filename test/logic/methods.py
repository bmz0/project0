# encoding: utf-8
#
# every function directly related to gamelogic is in this module
#

from os.path import isfile #,remove as osRemove
from random import randint

from pygame import Surface, Rect, QUIT, KEYDOWN, KEYUP, MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP

#~ from pygame.draw import rect as drawRect
from pygame.event import get as pygameEventGet

from pygame.locals import *

from test.config import *
from test.world.circle import circle

import core.display as display
import sv
import game

@game.state('grow-shrink', 'tick')
def growShrinkTick():

  for event in pygameEventGet():

    if event.type == KEYDOWN:

      if event.key == K_ESCAPE:
        game.sm.switch('menu')

      elif event.key == K_SPACE:
        game.sm.switch('add-remove')
        sv.lastPlayState = 'add-remove'
        game.fbLabel.string = game.fbLabel.string.replace('grow/shrink', 'add/remove')

      elif event.key == K_c:
        display.clear()
        sv.circles.empty()

    elif event.type == MOUSEBUTTONDOWN:

      tx, ty = event.pos
      game.fbLabel.text(str(tx) + ', ' + str(ty) + ' grow/shrink')

      if event.button == 1:

        sv.mb1Down = True
        for c in reversed(list(sv.circles.sprites())):
          if c.rect.collidepoint(tx, ty):
            game.currCircle = c
            break

      elif event.button == 3:

        sv.mb3Down = True
        for c in reversed(list(sv.circles.sprites())):
          if c.rect.collidepoint(tx, ty):
            game.currCircle = c
            break

    elif event.type == MOUSEBUTTONUP:

      if event.button == 1:
        sv.mb1Down = False
        game.currCircle = None

      elif event.button == 3:
        sv.mb3Down = False
        game.currCircle = None

  if sv.mb1Down and game.currCircle != None:
    game.currCircle.radius = min(game.currCircle.radius + 1, radiusMax)

  if sv.mb3Down and game.currCircle != None:
    game.currCircle.radius = max(game.currCircle.radius - 1, radiusMin)

  game.ui.clear(display.screen, clear_callback)
  sv.circles.clear(display.screen, clear_callback)

  if game.currCircle != None:
    game.currCircle.redraw()

  postPlayTick()

@game.state('add-remove', 'tick')
def addRemoveTick():

  toClear = None

  for event in pygameEventGet():

    if event.type == KEYDOWN:

      if event.key == K_ESCAPE:
        game.sm.switch('menu')

      elif event.key == K_SPACE:
        game.sm.switch('grow-shrink')
        sv.lastPlayState = 'grow-shrink'
        game.fbLabel.string = game.fbLabel.string.replace('add/remove', 'grow/shrink')

      elif event.key == K_c:
        display.clear()
        sv.circles.empty()

    elif event.type == MOUSEBUTTONDOWN:

      tx, ty = event.pos
      game.fbLabel.text(str(tx) + ', ' + str(ty) + ' add/remove')

      if event.button == 1:

        sv.mb1Down = True
        thisCircle = circle(tx, ty, sv.circles)
        thisCircle.radius = randint(radiusMin, radiusMax / 2)
        thisCircle.redraw()

      elif event.button == 3:

        for c in reversed(list(sv.circles.sprites())):
          if c.rect.collidepoint(tx, ty):
            toClear = c
            break

    elif event.type == MOUSEBUTTONUP:

      if event.button == 1:
        sv.mb1Down = False
        game.currCircle = None

      elif event.button == 3:
        sv.mb3Down = False
        game.currCircle = None

  game.ui.clear(display.screen, clear_callback)
  sv.circles.clear(display.screen, clear_callback)

  sv.circles.remove(toClear)

  postPlayTick()

def postPlayTick():

  sv.circles.draw(display.screen)

  game.ui.update()
  game.ui.draw(display.screen)

def clear_callback(surf, rect):

  surf.fill(clearColor, rect)

@game.state('new game', 'enter')
@game.state('load', 'enter')
def newGameLoadEnter():

  display.clear()

@game.state('new game', 'exit')
@game.state('load', 'exit')
def newGameLoadExit():

  game.sm.flags.discard('gameOver')

@game.state('menu', 'enter')
def menuEnter():

  if 'gameOver' in game.sm.flags:
    game.menu.disable('Resume')
    game.menu.disable('Save')
  else:
    game.menu.enable('Resume')
    game.menu.enable('Save')
  if isfile(game.saveFile):
    game.menu.enable('Load')
  else:
    game.menu.disable('Load')
  game.menu.enter(display.screen)

@game.state('menu', 'tick')
def menuTick():

  s = game.menu.tick(pygameEventGet())
  if s != None: game.sm.switch(s)

#~ @game.state('menu', 'exit')
#~ def menuExit():
#~
  #~ pass
