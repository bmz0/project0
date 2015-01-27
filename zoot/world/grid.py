# encoding: utf-8
#
# this module implements the grid object used for both the main playing space
# and the preview/hold grids
# basicly gridRect objects are stored in a dictionary inside gridGroup, with (x, y) tuple as keys
#
# todo: draw() optimize?, possibly numpy

from pygame import Rect
from pygame.draw import rect as drawRect
from pygame.locals import BLEND_MULT, BLEND_SUB

class gridRect(Rect):

  def __init__(self, *args):

    Rect.__init__(self, *args)

    self.color = (255, 255, 255)
    self.active = False
    self.settled = False
    self.ghost = False

class gridGroup(object): # todo: remove?

  def __init__(self, *args):

    self.gridDict = {}
    self.color = (32,) * 3
    self.clearRects = []
    self.overlay = None
    self.blendMode = BLEND_MULT
    self.borderRect = None
    self.hide = False
    self.width = 0
    self.height = 0

    if len(args) != 0: self.add(*args)

  def __iter__(self):

    for r in self.gridDict.iteritems():
      yield r

  def __len__(self):

    return len(self.gridDict.keys())

  def add(self, gridWidth, gridHeight, blockBase, x_offset = 0, y_offset = 0):

    self.blockBase = blockBase

    try:
      wFrom, wTo = gridWidth
    except TypeError:
      wFrom = 0
      wTo = gridWidth

    try:
      hFrom, hTo = gridHeight
    except TypeError:
      hFrom = 0
      hTo = gridHeight

    self.width = wTo
    self.height = hTo

    addList = [((x, y), gridRect(x_offset  + x * blockBase, y_offset +y * blockBase, blockBase, blockBase)) for x in range(wFrom, wTo) for y in range(hFrom, hTo)]

    self.pxWide = x * blockBase
    self.pxTall = y * blockBase

    self.addFromList(addList)

  def addFromList(self, args):

    for c, r in args:
      if isinstance(r, Rect):
        if c not in self.gridDict.keys():
          self.gridDict[c] = r

    if isinstance(r, Rect):
      self.borderRect = r.unionall(self.gridDict.values()).inflate(-1, -1)

  def get(self, x, y = None):

    if y == None:
      try:
        x, y = x
      except TypeError:
        print ' gridGroup.get requires 2 integers.'
        raise

    return self.gridDict[(x, y)]

  def getXY(self, rect):

    for k, v in self.gridDict.iteritems():

      if v == rect:
        return k

  def getActive(self):

    rList = []

    for k, v in self.gridDict.iteritems():
      if v.active:
        rList.append((k, v.color))

    return rList

  def getSettled(self):

    rList = []

    for k, v in self.gridDict.iteritems():
      if v.settled:
        rList.append((k, v.color))

    return rList

  def clear(self, surf):

    if self.clearRects != []:
      for r in self.clearRects:
        surf.fill((0, 0, 0), r)
        r.active = False
        r.ghost = False
        #~ drawRect(self.lastSurf, (0, 0, 0), r)

    self.clearRects = []

  def clearAll(self, surf):

    for t, r in self:
      surf.fill((0, 0, 0), r)
      r.active = False
      r.ghost = False
      r.settled = False
      #~ drawRect(self.lastSurf, (0, 0, 0), r)

    self.clearRects = []

  def draw(self, surf):

    for r in self.gridDict.values():
      if self.hide:
        #~ drawRect(surf, (0,0,0), r)
        surf.fill((0,0,0), r)
      elif r.active:
        #~ drawRect(surf, r.color, r)
        surf.fill(r.color, r)
        if self.overlay is not None:
          surf.blit(self.overlay, r, None, self.blendMode)
      elif r.settled:
        #~ drawRect(surf, r.color, r)
        surf.fill(r.color, r)
        if self.overlay is not None:
          surf.blit(self.overlay, r, None, self.blendMode)
      elif r.ghost:
        #~ drawRect(surf, self.color, r)
        surf.fill(self.color, r)
      else:
        pass
          #~ drawRect(surf, self.color, r, 1) # to draw a grid

    if self.borderRect is not None:
      drawRect(surf, (128,)*3, self.borderRect, 2)

  def checkLines(self):

    yLines = []
    lastEmptyLine = -1

    for b in range(self.height):

      lineStr = ''

      for a in range(self.width):

        if self.get(a, b).settled != True:
          lineStr += '0'
        else:
          lineStr += '1'

      if lineStr == '1' * self.width:
        yLines.append(b)
      elif lineStr == '0' * self.height:
        lastEmptyLine = b

    returnValue = len(yLines)

    if len(yLines) > 0:

      lec = 0

      while lastEmptyLine != max(yLines):

        lec += 1

        if lec > 50:
          print 'warning: line counter overflow'
          break

        y = yLines.pop()
        prevLine = y - 1
        while prevLine in yLines:
          prevLine -= 1

        for x in range(self.width): # hmm...

          oldRect = self.get(x, prevLine)
          r = gridRect(x * self.blockBase, y * self.blockBase, self.blockBase, self.blockBase)
          r.settled = oldRect.settled
          r.color = oldRect.color
          self.gridDict[(x, y)] = r
          self.clearRects.append(r)

        yLines.append(prevLine)
        yLines.sort()

    return returnValue

  def save(self):

    returnList = self.getSettled()
    if returnList == []:
      return None
    else:
     return self.getSettled()

  def load(self, data):

    for xy, color in data:
      thisRect = self.gridDict[xy]
      thisRect.settled = True
      thisRect.color = color
