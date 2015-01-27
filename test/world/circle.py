# encoding: utf-8

from pygame import Surface, Rect
from pygame.draw import circle as drawCircle
from pygame.sprite import Sprite
from random import randint
from test.config import *

class circle(Sprite):

  def __init__(self, x=0, y=0, *args):

    Sprite.__init__(self, *args)

    self.x, self.y = x, y
    self.radius = radiusMin
    self.color = randint(1, 255), randint(1, 255), randint(1, 255), randint(92, 208)
    self.redraw()

  def redraw(self):

    self.image = Surface((self.radius * 2,) * 2).convert_alpha()
    self.image.fill((0,) * 4)
    self.rect = self.image.get_rect()
    self.rect.centerx = self.x
    self.rect.centery = self.y
    drawCircle(self.image, (255,)*3, (self.radius, self.radius), self.radius)
    drawCircle(self.image, self.color, (self.radius, self.radius), self.radius - 2)
