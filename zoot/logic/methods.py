# encoding: utf-8
#
# every function directly related to gamelogic is in this module
# with a main playTick method (for the main game state) holding all together
#
# fixed - ?bug: playtick: move left-right after settle
# bug: startpos filled/top out fixme!

from os.path import isfile #,remove as osRemove

from pygame import Surface, Rect, QUIT, KEYDOWN, KEYUP, MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP

from pygame.draw import rect as drawRect
from pygame.event import get as pygameEventGet
from pygame.mouse import set_cursor

from pygame.locals import *

from zoot.config import *

import core.display as display
import statevars as sv
import game

def check(x, y, checkSettled = True):

  oldPos = sv.cx, sv.cy
  newPos = sv.cx + x, sv.cy + y

  for bx, by in sv.cBlock.pos[sv.cBlock.p]:

    if newPos[0] + bx > gridWidth - 1 or newPos[0] + bx < 0:
      return oldPos

    if newPos[1] + by > gridHeight - 1:
      if checkSettled: sv.cBlock.settle = True
      return oldPos

    elif game.grid.get(newPos[0] + bx, newPos[1] + by).settled == True:
      if oldPos[1] - newPos[1] == -1:
        if checkSettled: sv.cBlock.settle = True
      return oldPos

  else:

    return newPos

def checkDrop():

  dy = 1
  while (sv.cx, sv.cy) != check(0, dy, False):
    dy += 1

  return sv.cx, sv.cy + dy - 1

def checkSide(side=0):

  if side != 1 and side != -1:

    print ' Warning: invalid parameter for checkSide():', side
    return sv.cx, sv.cy

  else:

    dx = side
    while (sv.cx, sv.cy) != check(dx, 0, False):
      dx += side

    return sv.cx + dx - side, sv.cy

def checkRotated(rotation):

  p = sv.cBlock.p + rotation

  if p == len(sv.cBlock.pos):
    p = 0
  elif p  < 0:
    p = len(sv.cBlock.pos) - 1

  for bx, by in sv.cBlock.pos[p]:

    try:
      if game.grid.get(sv.cx + bx, sv.cy + by).settled == True:
        return sv.cBlock.pos[sv.cBlock.p]
    except KeyError:
      return sv.cBlock.pos[sv.cBlock.p]

  else:

    sv.cBlock.p = p
    return sv.cBlock.pos[sv.cBlock.p]

def setBlock(block, grid, ox, oy):

  for bx, by in block.pos[block.p]:

    thisRect = grid.get(ox + bx, oy + by)
    grid.clearRects.append(thisRect)
    thisRect.color = block.color
    thisRect.active = True

def hideGrids():

  game.grid.hide = True
  game.grid.draw(display.screen)
  game.nextGrid.hide = True
  game.nextGrid.draw(display.screen)
  game.holdGrid.hide = True
  game.holdGrid.draw(display.screen)

def clearGrids():

  game.grid.clearAll(display.screen)
  game.holdGrid.clearAll(display.screen)
  game.nextGrid.clearAll(display.screen)

def drawGrids():

  game.grid.hide = False
  game.nextGrid.hide = False
  game.holdGrid.hide = False

  game.nextGrid.draw(display.screen)
  game.holdGrid.draw(display.screen)

  sv.redrawGrids = False

@game.state('new game', 'enter')
@game.state('load', 'enter')
def newGameLoadEnter():

  display.clear()
  clearGrids()

@game.state('new game', 'exit')
@game.state('load', 'exit')
def newGameLoadExit():

  sv.hold = False
  sv.shifted = False
  sv.quick = False
  sv.left = False
  sv.right = False

  sv.leftDelay = sv.rightDelay = moveInitDelay

  setBlock(sv.nBlock, game.nextGrid, 1, 1)
  if sv.hBlock != None: setBlock(sv.hBlock, game.holdGrid, 1, 1)

  gridSurf = Surface((blockBase, blockBase))

  cL = range(1, blockBase / 2)
  cL.reverse()
  for c in cL:

    drawRect(gridSurf, (min(255, int(255 / (c * overlayColorConstant))) ,) * 3, Rect((blockBase / 2) - c, (blockBase / 2) - c, c * 2, c * 2), 1)

  game.grid.overlay = gridSurf
  game.nextGrid.overlay = gridSurf
  game.holdGrid.overlay = gridSurf

  game.sm.flags.discard('gameOver')
  game.msg('levelLabel::level' + str(sv.levelCounter) + ' - ' + str(sv.score))

@game.state('play', 'tick')
def playTick():

  import zoot.config as config

  if sv.c >= config.speed - ((sv.levelCounter - 1) * config.levelSpeedIncrease):

    sv.c = 0
    sv.cx, sv.cy = check(0, 1)

  sv.c += 1

  for event in pygameEventGet():

    if event.type == ACTIVEEVENT:
      if event.gain == 0 and event.state in (2, 4, 6):
        game.sm.switch('menu')

    if event.type == KEYDOWN and event.key == K_ESCAPE:
      #~ game.sm.switch('menu')
      game.msg('state::menu')

    if not sv.cBlock.settle:

      if event.type == KEYDOWN:

        if event.key == K_s:
          checkRotated(1)

        elif (event.key == K_a or event.key == K_UP):
          checkRotated(-1)

        elif event.key == K_LEFT:
          if event.mod & KMOD_SHIFT and not sv.shifted:
            sv.cx, sv.cy = checkSide(-1)
            sv.shifted = True
          else:
            sv.cx, sv.cy = check(-1, 0)
            sv.left = True

        elif event.key == K_RIGHT:
          if event.mod & KMOD_SHIFT and not sv.shifted:
            sv.cx, sv.cy = checkSide(1)
            sv.shifted = True
          else:
            sv.cx, sv.cy = check(1, 0)
            sv.right = True

        elif event.key == K_DOWN:
          sv.quick = True

    if event.type == KEYDOWN:

      if event.key == K_SPACE:
        sv.cx, sv.cy = checkDrop()
        sv.c = 1

      elif event.key == K_c:
        sv.ghost = not sv.ghost

      elif event.key == K_TAB:
        sv.hold = True

    if event.type == KEYUP:

      if event.key == K_LEFT:
        sv.left = False
        if sv.levelCounter < 19:
          sv.leftDelay = config.moveInitDelay
        else:
          sv.rightDelay = config.moveDelay

      elif event.key == K_RIGHT:
        sv.right = False
        if sv.levelCounter < 19:
          sv.rightDelay = config.moveInitDelay
        else:
          sv.rightDelay = config.moveDelay

      elif event.key == K_DOWN:
        sv.quick = False

      elif event.key == K_SPACE:
        sv.cx, sv.cy = check(0, 1)

      elif (event.key == K_LSHIFT or event.key == K_RSHIFT):
        sv.shifted = False

  if not sv.cBlock.settle:

    if sv.quick:
      sv.cx, sv.cy = check(0, 1)

    if sv.left:
      sv.leftDelay -= 1
      if sv.leftDelay == 0:
        sv.cx, cy = check(-1, 0)
        sv.leftDelay = config.moveDelay

    if sv.right:
      sv.rightDelay -= 1
      if sv.rightDelay == 0:
        sv.cx, sv.cy = check(1, 0)
        sv.rightDelay = config.moveDelay

    if sv.ghost:
      gx, gy = checkDrop()

  if sv.hold:

    if sv.hBlock is None:
      sv.hBlock = sv.nBlock
      sv.nBlock = sv.newBlock()
    else:
      sv.hBlock, sv.nBlock = sv.nBlock, sv.hBlock

    game.holdGrid.clear(display.screen)

    setBlock(sv.hBlock, game.holdGrid, 1, 1)

    game.nextGrid.clear(display.screen)

    setBlock(sv.nBlock, game.nextGrid, 1, 1)

    sv.redrawGrids = True
    sv.hold = False

  game.grid.clear(display.screen)

  game.ui.clear(display.screen, display.background)

  setBlock(sv.cBlock, game.grid, sv.cx, sv.cy)

  if sv.cBlock.settle:

    for bx, by in sv.cBlock.pos[sv.cBlock.p]:
      thisRect = game.grid.get(sv.cx + bx, sv.cy + by)
      thisRect.settled = True
      thisRect.active = False

    sv.quick = False

    sv.cBlock.settle = False

    fullLines = game.grid.checkLines()

    #~ bgc = 0
    #~ for bottomGrid in range(config.gridWidth):
      #~ if game.grid.get(bottomGrid, config.gridHeight - 1).settled:
        #~ bgc += 1

    #~ print bgc

    if fullLines > 0:

      if fullLines == 1:
        sv.score += 10
      elif fullLines == 2:
        sv.score += 30
      elif fullLines == 3:
        sv.score += 60
      elif fullLines == 4:
        sv.score += 100

      sv.lineCounter += fullLines

      sv.levelCounter = (sv.lineCounter / config.nextLevelLines) + 1

      game.msg.post('levelLabel::level' + str(sv.levelCounter) + ' - ' + str(sv.score))

    sv.cBlock = sv.nBlock
    sv.cx, sv.cy = config.startPos

    setBlock(sv.cBlock, game.grid, sv.cx, sv.cy)

    sv.nBlock = sv.newBlock()

    game.nextGrid.clear(display.screen)

    setBlock(sv.nBlock, game.nextGrid, 1, 1)

    game.nextGrid.draw(display.screen)

    if game.grid.get(config.startPos).settled: # fixme!
      #from os import remove as osRemove
      print 'level ' + str(sv.levelCounter) + ' - ' + str(sv.score)
      # osRemove('zoot.save')
      game.sm.flags.add('gameOver')
      game.sm.switch('menu')

  elif sv.ghost:

    for bx, by in sv.cBlock.pos[sv.cBlock.p]:

      thisRect = game.grid.get(gx + bx, gy + by)
      thisRect.ghost = True
      game.grid.clearRects.append(thisRect)

  game.ui.update()

  game.grid.draw(display.screen)

  if sv.redrawGrids:

    drawGrids()

  game.ui.draw(display.screen)

@game.state('menu', 'enter')
def menuEnter():

  set_cursor(*game.stdCursor)
  hideGrids()
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

@game.state('menu', 'exit')
def menuExit():

  sv.redrawGrids = True
