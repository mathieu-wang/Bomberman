import constant

from tile import Tile
from enemy import Enemy

## Bomberman object containing all the attributes describing the current state of bomberman
class Bomberman(object):

    ## Constructor of a bomberman unit with attributes
    def __init__(self):

        # Bomberman info

        ## Bomberman's current X position
        self.curX = 1
        ## Bomberman's current Y position
        self.curY = 11
        ## Bomberman's current remaining lives
        self.lives = 3
        ## Bomberman's current speed
        self.speed = 300
        ## Boolean whether bomberman can move or not
        self.canMove = True

        # Power ups

        ## Integer powerup maximum number of bombs bomberman can lay
        self.numBombs = 1 #
        ## Integer powerup the range in terms of tiles, the bomb can reach
        self.rangeOfBombs = 1 #
        ## Boolean powerup True if bomberman can pass through bricks
        self.wallPass = False #
        ## Boolean powerup True if bomberman has a detonator powerup
        self.hasDetonator = False
        ## Boolean powerup True if bomberman can pass through bombs
        self.bombPass = False #
        ## Boolean powerup True if bomberman does not die when touching flames
        self.flamePass = False #
        ## Boolean powerup True if bomberman cannot die
        self.invincible = False #

    ## This method resets Bomberman's attribute at the start of a new level or a new game
    def reset(self):

        self.curX = 1
        self.curY = 11
        # self.lives = 3
        self.speed = 300
        self.canMove = True

    ## This method resets Bomberman's attributes as well a its powerup and reduce its lives by 1
    def death(self):
        # Take off one life
        self.lives -= 1

        # Reset powerups
        self.hasDetonator = False
        self.bombPass = False
        self.wallPass = False
        self.flamePass = False
