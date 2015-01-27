# encoding: utf-8
#
# this module holds the 'state variables',
# the module is checked on save, so that
# any var named in the saveIncludes list is saved from the module.__dict__

from pygame.sprite import OrderedUpdates
from test.world.circle import circle

circles = OrderedUpdates()
lastPlayState = 'add-remove'
mb1Down = False
mb3Down = False

saveIncludes = ['circles', 'lastPlayState']
