# encoding: utf-8
#
# initial setup of more general state methods (init, save...)
#

import sys
import cPickle as pickle, zlib
from os.path import abspath, join as osJoin

import game, zoot
import logic, core.display as display
import sv

from types import InstanceType

from pygame import Rect, init, quit
from pygame.display import set_caption
from pygame.font import Font
from pygame.mouse import get_cursor
from pygame.sprite import Group

from ui.menu import menuGroup
from ui.ui import labelSprite

from zoot.config import *
from zoot.world.grid import gridGroup

print ' Running game at:', abspath(game.dir)

@game.state('init', 'simple')
def gameInit():

  version = '0.8e'
  versionString = 'zoot v' + version

  print ' ' + versionString

  display.clearColor = (32,) * 3
  display.reset(width, height)

  init()

  set_caption(versionString)

  menuSetup = ('&Resume', 'play', 'K_ESCAPE'), \
            None, \
            ('&New game', 'new game'), \
            ('&Save', 'save'), \
            ('&Load', 'load'), \
            ('&Quit', 'quit')

  game.menu = menuGroup(menuSetup)
  game.menu.rect.centerx = width / 2
  game.menu.rect.centery = height / 2
  game.menu.subscript(versionString)

  game.grid = gridGroup(gridWidth, (-4, gridHeight), blockBase)
  game.nextGrid = gridGroup(4, 4, blockBase, game.grid.pxWide + 2 * blockBase, game.grid.pxTall / 3 - 2 * blockBase)
  game.holdGrid = gridGroup(4, 4, blockBase, game.grid.pxWide + 2 * blockBase, game.grid.pxTall / 3 * 2)

  # string offset [fontsize] [color]
  levelLabel = labelSprite('level 1 - 0', ((size[0]- 80), size[1] - 20))
  nextLabel = labelSprite('Next up:', (game.nextGrid.borderRect.left + 4, game.nextGrid.borderRect.top - 20))
  holdLabel = labelSprite('Hold:', (game.holdGrid.borderRect.left + 4, game.holdGrid.borderRect.top - 20))
  game.ui = Group(levelLabel, nextLabel, holdLabel)

  game.msg.handler('levelLabel')(levelLabel.text)

  from os.path import isfile

  game.stdCursor = get_cursor()

  game.saveFile = osJoin(abspath(game.dir), 'zoot.save')

  game.saveRegister = []
  for name, obj in game.__dict__.iteritems():
    if hasattr(obj, 'save'):
      if callable(obj.save) and not isinstance(obj, type):
        game.saveRegister.append((name, obj))

  game.sm.autoSwitch = { 'new game': 'play', 'load': 'play', 'save': 'play' }

  if isfile(game.saveFile):
    game.sm.autoSwitch['init'] = 'load'
  else:
    game.sm.autoSwitch['init'] = 'new game'

@game.state('quit')
def gameQuit():

  #~ if game.sm.previous != 'save':
    #~ game.sm.autoSwitch['save'] = 'quit'
    #~ game.sm.switch('save')
  #~ else:
  quit()
  sys.exit()

@game.state('load', 'tick')
def loadTick(): # seperate loadRegister? if saver-loader objs differs

  with open(game.saveFile, 'rb') as saveFile:
    pString = zlib.decompress(saveFile.read())

  loadDict = pickle.loads(pString)

  for k, v in loadDict.iteritems():

    if k in sv.__dict__:
      sv.__dict__[k] = v
    else:
      for name, loadObj in game.saveRegister:
        if name == k:
          loadObj.load(v)
          break
      else:
        print 'cannot load:', k
        raise KeyError

@game.state('new game', 'tick')
def newGameTick():

  reload(sv)

@game.state('save')
def saveState():

  display.clear((0, 0, 0), Rect(0, size[1] - 13, 50, 15))
  display.draw(Font('freesansbold.ttf', 10).render('saving...', 1, (255, 255, 255)), Rect(1, size[1] - 14, 47, 13))
  display.update()

  print ' Saving:', 'level ' + str(sv.levelCounter) + ' - ' + str(sv.score)

  saveDict = {}

  if 'gameOver' not in game.sm.flags:

    for k, v in sv.__dict__.iteritems():
      if k in sv.saveIncludes:
        saveDict[k] = v

    for name, obj in game.saveRegister:
      data = obj.save()
      if data != None: saveDict[name] = data

    with open(game.saveFile, 'wb') as saveFile:
      saveFile.write(zlib.compress(pickle.dumps(saveDict, 2)))
