# encoding: utf-8
#
# this module holds config constants
# these aren't saved, they're only used to init vars here and there

speed = 60 #!!!!!

blockBase = 28
gridWidth = 14
gridHeight = 14

startPos = 7, 0

levels = 20
nextLevelLines = 10

levelSpeedIncrease = speed / levels

moveInitDelay = speed / 10
moveDelay = speed / 13 #3

size = width, height = (gridWidth * blockBase) + (6 * blockBase), gridHeight * blockBase

clearColor = (32,) * 3

overlayColorConstant = .18 #.32
