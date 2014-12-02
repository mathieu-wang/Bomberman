import constant

from tile import Tile
from enemy import Enemy

class Bomberman(object):

    def __init__(self):

        # Bomberman info
        self.curX = 1
        self.curY = 11
        self.lives = 3
        self.speed = 300
        self.canMove = True

        # Power ups
        self.numBombs = 1 #
        self.rangeOfBombs = 1 #
        self.wallPass = False #
        self.hasDetonator = False
        self.bombPass = False #
        self.flamePass = False #
        self.invincible = False #


    def reset(self):

        self.curX = 1
        self.curY = 11
        # self.lives = 3
        self.speed = 300
        self.canMove = True

    def death(self):
        # Take off one life
        self.lives -= 1

        # Reset powerups
        self.hasDetonator = False
        self.bombPass = False
        self.wallPass = False
        self.flamePass = False
