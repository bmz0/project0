# encoding: utf-8
#
# this module holds the menu which is pretty independent from the game/engine
# yet quite some stuff uses pygame, though possibly replaceable things
#

from pygame import Rect, Surface
from pygame.sprite import Sprite, Group
import pygame.image #, pygame.font
from pygame.transform import flip
from pygame.locals import *

from config import *

pygame.init()

class menuGroup(Group):
  """A class for a menu, mostly encapsulated, semi-dynamic with subclass menuItemSprites generated from
     a series of tuples in the form: (&Name, reutrn value, optional hotkeys, ...), ...
     e.g. menu = menuGroup(('&Resume', 'play', 'K_ESCAPE'), None, ('&New game', 'new game'), ('&Quit', 'quit'))"""

  class titleSprite(Sprite):
    """The title class of the menu, on the top, text is changable through menu.title.string."""

    def __init__(self):

      Sprite.__init__(self)
      self.rect = Rect(0, 0, 1, 1)
      self.font = menuTitleFont #pygame.font.Font('freesansbold.ttf', 24)
      self.color = (255,) * 3
      self.string = 'Paused'
      self.image = self.font.render(self.string, 1, self.color)
      self.rect = self.image.get_rect()
      self.rect.top = 5

    def __setattr__(self, name, value):

      Sprite.__setattr__(self, name, value)

      if name == 'string':
        oldCenterX = self.rect.centerx
        self.image = self.font.render(self.string, 1, self.color)
        self.rect = self.image.get_rect()
        self.rect.centerx = oldCenterX
        self.rect.top = 5

  class versionSprite(Sprite):
    """A subscript in lower right corner of the menu - generally used for version number."""

    def __init__(self, text = 'menu'):

      Sprite.__init__(self)
      self.subscript = text
      self.font = menuSubFont #pygame.font.Font('freesansbold.ttf', 10)
      self.color = (255,) * 3
      self.redraw()

    def redraw(self):

      self.image = self.font.render(self.subscript, 1, self.color)
      self.rect = self.image.get_rect()

  class menuItemSprite(Sprite):
    """The menu item class is used to generate the items with hotkeys, coloring and a return value."""

    def __init__(self, name, colors, data):

      Sprite.__init__(self)
      self.font = menuDefaultFont #pygame.font.Font('freesansbold.ttf', 18)

      self.hotKey = []
      index = name.find('&')

      if index >= 0:
        self.imageRenderText = (name[:index], name[index + 1], name[index + 2:])
        self.name = str(name[:index] + name[index + 1] + name[index + 2:])
        self.hotKey.append(eval('K_' + str(name[index + 1].lower())))
      else:
        self.name = name
        self.imageRenderText = (name, '', '')

      self.returnValue = data[0]
      if len(data) > 1:
        for rd in data[1:]:
          self.hotKey.append(eval(str(rd)))

      self.hilight = False
      self.disabled = False
      self.cleanSurface = Surface(self.font.size(self.imageRenderText[0] + self.imageRenderText[1] + self.imageRenderText[2])).convert_alpha()
      self.cleanSurface.fill((0,)*4)
      self.image = self.cleanSurface.copy()
      self.rect = self.image.get_rect()

      self.hiColor = colors[0]
      self.hkColor = colors[1]
      self.gray = colors[2]
      self.darkGray = colors[3]

    def update(self):

      self.image = self.cleanSurface.copy()
      sizeSoFar = 0

      if self.disabled:
        self.image.blit(self.font.render(self.imageRenderText[0] + self.imageRenderText[1] + self.imageRenderText[2], 1, self.darkGray), (0, 0))

      elif self.hilight:
        if self.imageRenderText[0] != '':
          self.image.blit(self.font.render(self.imageRenderText[0], 1, self.hiColor), (0, 0))
          sizeSoFar += self.font.size(self.imageRenderText[0])[0]
        if self.imageRenderText[1] != '':
          self.image.blit(self.font.render(self.imageRenderText[1], 1, self.hkColor), (sizeSoFar, 0))
          sizeSoFar += self.font.size(self.imageRenderText[1])[0]
        if self.imageRenderText[2] != '':
          self.image.blit(self.font.render(self.imageRenderText[2], 1, self.hiColor), (sizeSoFar, 0))
        pygame.draw.aaline(self.image, (32, 96, 192), (2, self.rect.h - 2), (self.rect.w - 2, self.rect.h - 2))

      else:
        if self.imageRenderText[0] != '':
          self.image.blit(self.font.render(self.imageRenderText[0], 1, self.gray), (0, 0))
          sizeSoFar += self.font.size(self.imageRenderText[0])[0]
        if self.imageRenderText[1] != '':
          self.image.blit(self.font.render(self.imageRenderText[1], 1, self.hkColor), (sizeSoFar, 0))
          sizeSoFar += self.font.size(self.imageRenderText[1])[0]
        if self.imageRenderText[2] != '':
          self.image.blit(self.font.render(self.imageRenderText[2], 1, self.gray), (sizeSoFar, 0))

  class separatorSprite(Sprite):
    """A sprite for (visually) separating menu items."""

    def __init__(self, *args):

      Sprite.__init__(self, *args)

      self.disabled = True

      self.image = pygame.Surface((60, 6)).convert_alpha()
      self.image.fill((0,)*4)
      self.image.fill((64, 64, 64, 224), Rect(0, 3, 60, 2))

      self.rect = self.image.get_rect()

  class selectorSprite(Sprite):
    """Little image on the left and right bounding the active menu item."""

    def __init__(self, parent, flipped, *args):

      Sprite.__init__(self, *args)
      self.parent = parent
      self.flipped = flipped

      self.image = pygame.Surface((3, 3))
      self.image.fill(self.parent.borderColor)

      if self.flipped:
        self.image.fill((160,) * 3, Rect(0, 0, 1, 3))
      else:
        self.image.fill((160,) * 3, Rect(2, 0, 1, 3))

      self.rect = self.image.get_rect()
      self.parent.add(self)

    def update(self):

      if self.flipped:
        self.rect.left = self.parent.active.rect.right + 8
        self.rect.bottom = self.parent.active.rect.bottom - 8
      else:
        self.rect.right = self.parent.active.rect.left - 8
        self.rect.bottom = self.parent.active.rect.bottom - 8

  def __init__(self, menuItemSet):

    self.visible = False
    self.maxX = 0
    self.maxY = 0

    Group.__init__(self)

    self.title = self.titleSprite()
    self.add(self.title)
    self.maxY += 48 + 5

    self.active = None

    self.bgColor = (8, 24, 34, 224)
    self.borderColor = (32, 96, 192)

    # hilight - hotkey - normal - disabled
    self.menuItemColors = (128, 192, 255), (24, 128, 255), (192,) * 3, (64,) * 3

    self.enterSurface = None
    self.offsetOnSurface = (0, 0)

    self.orderList = []

    self.generate(menuItemSet)
    self.redraw()
    self.clearBg = Surface(self.bg.get_size())

    self.getFirst()

    self.selectorSprite(self, False)
    self.selectorSprite(self, True)

  def get_size(self):

    return self.bg.get_size()

  def generate(self, items):

    c = 1

    for i in items:

      if i == None:
        thisSprite = self.separatorSprite()
      else:
        thisSprite = self.menuItemSprite(i[0], self.menuItemColors, i[1:])
        thisSprite.order = c
        c += 1
      if thisSprite.image.get_width() > self.maxX:
        self.maxX = thisSprite.image.get_width() + 64
      self.maxY += thisSprite.rect.h + 2
      self.add(thisSprite)

      self.orderList.append(thisSprite)

    self.maxY += 32

    self.bg = Surface((max(self.title.rect.w + 20, self.maxX + 20), self.maxY + 20)).convert_alpha()

  def redraw(self):

    self.bg.fill(self.bgColor) # img?
    self.rect = self.bg.get_rect()
    pygame.draw.rect(self.bg, self.borderColor, self.rect, 1)

    self.title.rect.centerx = int(self.bg.get_width() / 2)
    self.title.rect.top = 10

    yDrawCounter = self.title.rect.h + 10

    for i in self.orderList:
      i.rect.centerx = int(self.bg.get_width() / 2)
      i.rect.top = yDrawCounter + 6
      yDrawCounter += 6 + i.rect.h

    #~ for i in self:
      #~ if isinstance(i, self.versionSprite):
        #~ i.rect.right = self.rect.right - 3
        #~ i.rect.bottom = self.rect.bottom - 2
        #~ break

  def execute(self, item):

    for i in self:
      if isinstance(i, self.menuItemSprite):
        if i.name == item:
          if i.disabled:
            return None
          else:
            self.visible = False
            self.active.hilight = False
            if self.enterSurface is not None:
              self.enterSurface.blit(self.clearBg, self.offsetOnSurface)
              #~ self.backupSurface = self.enterSurface.subsurface(Rect(self.backupOffset, (self.rect.w, self.rect.h)))
              self.enterSurface = None
            return i.returnValue
    else:
      return None

  def enter(self, enterSurface):

    self.clearBg = Surface((self.rect.w, self.rect.h))
    self.clearBg.blit(enterSurface, (0, 0), self.rect)
    self.enterSurface = enterSurface
    #~ self.backupSurface = Surface((self.rect.w, self.rect.h))
    self.offsetOnSurface = self.rect.left, self.rect.top
    self.visible = True
    self.itemName = ''

    if self.active is None or self.active.disabled:
      self.getFirst()

    print 'menu active:', self.active

  def tick(self, eventList):

    rValue = None

    for event in eventList:

      #~ if event.type == QUIT:
        #~ rValue = 'quit'
        #~ break

      if event.type == KEYDOWN:
        rValue = self.execute(self.checkKeys(event.key))

      if event.type == MOUSEBUTTONDOWN:
        self.itemName = self.checkMouse(event.pos)

      elif event.type == MOUSEBUTTONUP and self.itemName != '':
        if self.itemName == self.checkMouse(event.pos):
          rValue = self.execute(self.itemName)

      elif event.type == MOUSEMOTION:
        self.checkMouse(event.pos)

    self.clear()
    self.update()
    self.draw()

    return rValue

  def disable(self, item):

    for i in self:
      if isinstance(i, self.menuItemSprite):
        if i.name == item:
          i.disabled = True
          if item == self.active:
            self.getFirst()
          break

  def enable(self, item):

    for i in self:
      if isinstance(i, self.menuItemSprite):
        if i.name == item:
          i.disabled = False
          break

  def draw(self):

    Group.draw(self, self.bg)
    if self.enterSurface is not None:
      self.enterSurface.blit(self.bg, self.rect)

  def get_rect(self):

    return self.bg.get_rect()

  def clear(self):

    Group.clear(self, self.bg, self.clear_callback)
    if self.enterSurface is not None:
      self.enterSurface.blit(self.clearBg, self.rect)

  def getByName(self, item):

    for i in self:
      if isinstance(i, self.menuItemSprite):
        if i.name == item:
          return i

  def getFirst(self):

    first = None

    for i in self.orderList:
      if isinstance(i, self.menuItemSprite):
        if not i.disabled:
          first = i
          break

    if first != None: first.hilight = True
    self.active = first

  def getLast(self):

    last = None

    for i in reversed(self.orderList):
      if isinstance(i, self.menuItemSprite):
        if not i.disabled:
          last = i
          break

    if last != None: last.hilight = True
    self.active = last

  def checkKeys(self, key):

    self.active.hilight = False

    if self.active == None or self.active.disabled:
      self.getFirst()
      return None

    if key == K_RETURN or key == K_KP_ENTER or key == K_SPACE:
      return self.active.name

    activeIndex = self.orderList.index(self.active)

    if key == K_UP:

      if activeIndex > 0:

        while activeIndex >= 0:
          activeIndex -= 1
          thisItem = self.orderList[activeIndex]
          if not thisItem.disabled:
            self.active = thisItem
            break

      else:
        self.getLast()

    elif key == K_DOWN:

      try:

        while activeIndex < len(self.orderList):
          activeIndex += 1
          thisItem = self.orderList[activeIndex]
          if not thisItem.disabled:
            self.active = thisItem
            break

      except IndexError:
        self.getFirst()

    elif key == K_HOME or key == K_PAGEUP:
      self.getFirst()

    elif key == K_END or key == K_PAGEDOWN:
      self.getLast()

    else:
      for i in self:
        if isinstance(i, self.menuItemSprite):
          if key in i.hotKey and not i.disabled:
            return i.name

    if self.active != None:
      self.active.hilight = True
    return None

  def checkMouse(self, pos):

    x, y = pos
    x -= self.rect.left
    y -= self.rect.top
    rName = ''

    for item in self:

      if isinstance(item, self.menuItemSprite):

        if item.rect.collidepoint(x, y) and not item.disabled:

          if self.active != None:
            self.active.hilight = False

          self.active = item

          item.hilight = True
          rName = item.name

    return rName

  def subscript(self, text=None):

    for i in self:
      if isinstance(i, self.versionSprite):
        self.remove(i)
        break

    if text is not None:

      i = self.versionSprite(text)
      i.rect.right = self.rect.right - 3
      i.rect.bottom = self.rect.bottom - 2
      self.add(i)
      print i.rect

  def clear_callback(self, surf, rect):

    surf.fill(self.bgColor, rect)
