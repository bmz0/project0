# encoding: utf-8
#
# the statemachine object, create an instance then call run()
# state() as a decorator adds states and their methods
#

from pygame.event import get, peek
from pygame.locals import QUIT
from pygame.time import Clock

import game
#~ import display

class simpleStateObject(object):

  def __init__(self, stateMethod=None):

    if callable(stateMethod):
      self.method = stateMethod
    else:
      self.method = lambda: stateMethod

  def __str__(self):

    return '(simple)'

class stateObject(object): # context manager..?

  def __init__(self, enter=None, tick=None, exit=None):

    self._strSet = set()

    if callable(enter):
      self.enter = enter
    else:
      self.enter = lambda: enter

    if callable(tick):
      self.tick = tick
    else:
      self.tick = lambda: tick

    if callable(exit):
      self.exit = exit
    else:
      self.exit = lambda: exit

    if enter is not None:
      self._strSet.add('enter')

    if tick is not None:
      self._strSet.add('tick')

    if exit is not None:
      self._strSet.add('exit')

  def __str__(self):

    rStr = '('
    if 'enter' in self._strSet:
      rStr += 'enter '
    if 'tick' in self._strSet:
      rStr += 'tick '
    if 'exit' in self._strSet:
      rStr += 'exit'

    return rStr.strip() + ')'

class stateMachine(object):

  def __init__(self, *args):

    self.states = {}
    self.states['null'] = self.nullState = simpleStateObject()
    self.activeName = 'null'
    self.running = False
    self.globals = {}
    self.previous = None
    self.lastTickState = None
    self.next = 'init'
    self.flags = set() # tmp
    self.autoSwitch = {'null': 'init', 'quit': 'null'}

    self.clock = Clock()

  def quit(self):

    self.running = False
    if 'quit' in self.states:
      self._next('quit')

  def state(self, stateName, stateType='simple'):

    def registerState(f):

      if stateType == 'simple':
        self.states[stateName] = simpleStateObject(f)

      try:

        thisState = self.states[stateName]

        if stateType == 'enter':
          thisState.enter = f
          self.states[stateName]._strSet.add('enter')
        elif stateType == 'tick':
          thisState.tick = f
          self.states[stateName]._strSet.add('tick')
        elif stateType == 'exit':
          thisState.exit = f
          self.states[stateName]._strSet.add('exit')

      except KeyError:

        if stateType == 'enter':
          self.states[stateName] = stateObject(f)
        elif stateType == 'tick':
          self.states[stateName] = stateObject(None, f, None)
        elif stateType == 'exit':
          self.states[stateName] = stateObject(None, None, f)

      return f

    return registerState

  def addState(self, name, enter=None, tick=None, exit=None):

    self.states[name] = stateObject(enter, tick, exit)

  def removeState(self, name):

    del self.states[name]

  def switch(self, newState):

    self.next = newState

  def _next(self, newState):

    active = self.states[self.activeName]

    if not isinstance(active, simpleStateObject):
      active.exit()
      print self.activeName,
    else:
      print '...',

    self.previous = self.activeName
    if isinstance(active, stateObject):
      self.lastTickState = self.activeName
    self.activeName = newState
    active = self.states[self.activeName]

    if not isinstance(active, simpleStateObject):

      print '-->', self.activeName, active
      active.enter()
      try:
        self.next = self.autoSwitch[self.activeName]
      except KeyError:
        self.next = self.activeName

    else:

      print '-->', self.activeName, active, '...'
      active.method()
      if self.next is None or self.next == self.activeName:
        try:
          self.next = self.autoSwitch[self.activeName]
        except KeyError:
          print ' Error: no switch parameter for simple state:', self.activeName
          raise

      self._next(self.next)

  def run(self):

    import game

    self.running = True

    game.msg.handler('state')(self.switch)

    if self.next is not None and self.next != self.activeName:
      self._next(self.next)

    while self.running and not peek(QUIT):

      self.states[self.activeName].tick()

      if self.next is not None and self.next != self.activeName:
        self._next(self.next)

      game.msg('display::update')
      game.msg.process()
      self.clock.tick(game.fps)

    self.quit()
