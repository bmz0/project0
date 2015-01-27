# encoding: utf-8
#

import sys
#~ from abc import ABCMeta
#~
#~ class messageBase(object):
#~
  #~ __metaclass__ = ABCMeta

#~ class messageHandlerBase(object):
#~
  #~ __metaclass__ = ABCMeta

class messageDispatcher(object):

  def __init__(self):

    self.messageQueue = []
    self.registry = {}

  def __call__(self, *args):

    self.post(self, *args)

  def post(self, *msgs):

    for msg in msgs:

      if isinstance(msg, str):
        msgList = msg.split('::')

        if msgList[0] != 'display':
          print ' messaging:', msgList[0], 'recieved',
          for mm in msgList[1:]:
            print mm

        try:
          self.registry[msgList[0]](*msgList[1:])
        except KeyError:
          print ' Error: handler', msgList[0], 'not registered in game.msg!'
          raise

  def process(self):

    for msg in self.messageQueue:
      self.post(msg)

    self.empty()

  def empty(self):

    self.messageQueue = []

  def queue(self, *msg):

    self.messageQueue.append(msg)

  def handler(self, name):

    def registerHandler(f):

      self.registry[name] = f

      return f

    return registerHandler

