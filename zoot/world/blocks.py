# encoding: utf-8
#
# this module stores the tetris blocks,
# the ingame blocks sublcass the block object
# self.data provides relative coordinates as if in a grid
# self.pos stores the rotation data,
# while self.p is an index for this list -> the current rotation

class block(object):

  def __init__(self):

    self.data = (0, 0)
    self.settle = False
    self.color = (255, 255, 255)
    self.pos = (self.data,)
    self.p = 0

  def rotated(self, i):

    rt = self.data
    x = 0

    if i >= 0:

      while x != i:

        rt = [(-rt[a][1], rt[a][0]) for a in range(len(self.data))]
        x += 1

      return rt

    if i < 0:

      while x != i:

        rt = [(rt[b][1], -rt[b][0]) for b in range(len(self.data))]
        x -= 1

      return rt

class iBlock(block):

  def __init__(self):

    block.__init__(self)

    self.data = ((2, 0), (-1, 0), (1, 0), (0, 0))
    self.color = (0, 255, 255)

    self.pos = (self.data, self.rotated(1))

class jBlock(block):

  def __init__(self):

    block.__init__(self)

    self.data = ((-1, 0), (-1, -1), (1, 0), (0, 0))
    self.color = (0, 0, 255)

    self.pos = (self.data, self.rotated(1), self.rotated(2), self.rotated(-1))

class lBlock(block):

  def __init__(self):

    block.__init__(self)

    self.data = ((-1, 0), (1, -1), (1, 0), (0, 0))
    self.color = (255, 128, 16)

    self.pos = (self.data, self.rotated(1), self.rotated(2), self.rotated(-1))

class tBlock(block):

  def __init__(self):

    block.__init__(self)

    self.data = ((-1, 0), (0, -1), (1, 0), (0, 0))
    self.color = (192, 0, 192)

    self.pos = (self.data, self.rotated(1), self.rotated(2), self.rotated(-1))

class zBlock(block):

  def __init__(self):

    block.__init__(self)

    self.data = ((-1, -1), (0, -1), (1, 0), (0, 0))
    self.color = (255, 0, 0)

    self.pos = (self.data, self.rotated(1))

class sBlock(block):

  def __init__(self):

    block.__init__(self)

    self.data = ((-1, 0), (0, -1), (1, -1), (0, 0))
    self.color = (0, 255, 0)

    self.pos = (self.data, self.rotated(1))

class oBlock(block):

  def __init__(self):

    block.__init__(self)

    self.data = ((1, 0), (1, -1), (0, -1), (0, 0))
    self.color = (255, 255, 0)

    self.pos = (self.data,)

class fBlock(block):

  pass

blocks = iBlock, jBlock, lBlock, tBlock, zBlock, sBlock, oBlock
