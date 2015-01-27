# encoding: utf-8
#
# this module is for gui objects, holds only a simple label for now
# which is used as the next/hold lables and the score

from pygame.sprite import Sprite
from pygame.font import Font

from config import *

class labelSprite(Sprite):

  def __init__(self, string, offset, fontsize = None, color = (255, 255, 255), *args):

    if fontsize is None:
      fontsize = uiLabelSizeHint

    Sprite.__init__(self, *args)
    self.font = Font(uiLabelFontName, fontsize)
    self.string = string
    self.color = color
    self.offset = offset

  def update(self):

    self.image = self.font.render(self.string, 1, self.color).convert_alpha()
    self.rect = self.image.get_rect()
    self.rect.left, self.rect.top = self.offset

  def text(self, textOut):

    self.string = str(textOut)
