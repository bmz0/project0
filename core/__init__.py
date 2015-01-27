# encoding: utf-8
#

import sys, types
from os.path import abspath

from pygame import init

from config import *

sys.modules['game'] = types.ModuleType('game')
import game

from msg import messageDispatcher
game.msg = messageDispatcher()

@game.msg.handler('core')
def coreMessageHandler(msg):
  if isinstance(msg, str):
    if msg == 'quit':
      game.sm.running = False
  else:
    print ' Error: core has no message:', msg
    raise ValueError

from sm import stateMachine # needs game.msg
game.sm = stateMachine()
game.state = game.sm.state

import display # needs game.msg

try:
  gameDir = sys.argv[1]
except IndexError:
  gameDir = 'zoot'

game.res = abspath('res')
sys.path.insert(1, game.res)

game.fps = fps
game.dir = str(gameDir)

# needs game.sm, game.state
try:
  exec 'import ' + game.dir
except ImportError:
  print ' Error importing the game in:', game.dir
  raise

init()
game.sm.run()
