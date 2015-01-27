# encoding: utf-8
#
# this module holds the 'state variables',
# the module is checked on save, so that
# any var named in the saveIncludes list is saved from the module.__dict__

from zoot.config import startPos, moveInitDelay

def newBlock():

  from random import choice, randint
  from zoot.world.blocks import blocks

  newBlock = choice(blocks)()
  newBlock.p = randint(0, len(newBlock.pos) - 1)
  return newBlock

#~ excludes = ['excludes', 'newBlock', '__doc__', '__name__', '__file__', '__builtins__', '__package__', 'redrawGrids', 'left', 'right', 'quick', 'rightDelay', 'leftDelay', 'hold']
saveIncludes = ['cx', 'cy', 'c', 'score', 'levelCounter', 'lineCounter', 'ghost', 'cBlock', 'hBlock', 'nBlock']

cx, cy = startPos

c = 0
levelCounter = 1
lineCounter = 0

ghost = True

nBlock = newBlock()
cBlock = newBlock()
hBlock = None
score = 0

hold = False
shifted = False
quick = False
left = False
right = False

leftDelay = rightDelay = moveInitDelay

redrawGrids = True
