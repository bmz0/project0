# encoding: utf-8

import sys
import cPickle as pickle, zlib
from os.path import abspath, join as osJoin

import game, test, logic, sv
from test.config import *
import core.display as display

from pygame import Surface, Rect, init, quit
from pygame.display import set_caption
from pygame.font import Font
from pygame.locals import *
from pygame.sprite import Group

from ui.menu import menuGroup
from ui.ui import labelSprite

print ' Running game at:', abspath(game.dir)

@game.state('init')
def gameInit():

  version = '0.1e'
  versionString = 'circle test v' + version

  print ' ' + versionString

  display.reset(width, height)

  init()

  set_caption(versionString)

  menuSetup = ('&Resume', 'resume', 'K_ESCAPE'), \
            None, \
            ('&New game', 'new game'), \
            ('&Save', 'save'), \
            ('&Load', 'load'), \
            ('&Quit', 'quit')

  game.menu = menuGroup(menuSetup)
  game.menu.rect.centerx = width / 2
  game.menu.rect.centery = height / 2
  game.menu.subscript(versionString)

  # string offset [fontsize] [color]
  game.fbLabel = labelSprite('0, 0 add/remove', (10, 10))
  game.ui = Group(game.fbLabel)

  game.currCircle = None

  from os.path import isfile

  game.saveFile = osJoin(abspath(game.dir), 'test.save')

  game.saveRegister = []
  for name, obj in game.__dict__.iteritems():
    if hasattr(obj, 'save'):
      if callable(obj.save) and not isinstance(obj, type):
        game.saveRegister.append((name, obj))

  game.sm.autoSwitch = { 'new game': 'add-remove', 'save': 'resume', 'load': 'resume' }

  if isfile(game.saveFile):
    game.sm.autoSwitch['init'] = 'load'
  else:
    game.sm.autoSwitch['init'] = 'new game'

@game.state('resume')
def resumeTransit():

  game.sm.switch(sv.lastPlayState)

@game.state('quit')
def gameQuit():

  if game.sm.previous != 'save':
    game.sm.autoSwitch['save'] = 'quit'
    game.sm.switch('save')
  else:
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

  for s in sv.circles:
    s.redraw()

  if sv.lastPlayState == 'add-remove':
    game.fbLabel.string = '0, 0 add/remove'
  elif sv.lastPlayState == 'grow-shrink':
    game.fbLabel.string = '0, 0 grow/shrink'

@game.state('new game', 'tick')
def newGameTick():

  reload(sv)

@game.state('save')
def saveState():

  bak = Surface((50, 15))
  bak.blit(display.screen, (0, 0), Rect(0, size[1] - 13, 50, 15))
  display.clear((0, 0, 0), Rect(0, size[1] - 13, 50, 15))
  display.draw(Font('freesansbold.ttf', 10).render('saving...', 1, (255, 255, 255)), Rect(1, size[1] - 14, 47, 13))
  display.update()

  print ' Saving...'

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

  display.draw(bak, (0, size[1] - 13))
  display.update()
