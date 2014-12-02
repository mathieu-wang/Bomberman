import random
import constant

from tile import Tile
from enemy import Enemy
from bomberman import Bomberman

## This class Level contains all the attributes and methods necessary to one level of gameplay
class Level(object):

    ## Constructor of a level which takes a username and a level as argument
    def __init__(self, username, levelNum):

        ## Initialize bomberman
        self.bomberman = Bomberman()

        ## String Player's username
        self.username = username

        # Level info

        ## Integer the level's number
        self.levelNum = levelNum
        ## Boolean True if the game has started
        self.isInitialized = False

        ## Nested List of Tile(s) representing the game board
        self.board = []
        ## Queue containing the coords and time left of bombs laid by bomberman
        self.bombQueue = []
        ## Queue containing the coords and time left of flame tiles produced by bomb(s)
        self.flashQueue = []

        ## List coordinates of the powerup tile
        self.powerUpCoord = [0, 0]
        ## List coordinates of the exit tile
        self.exitCoord = [0, 0]
        ## Integer type of powerup
        self.powerUp = 0
        ## Integer number of enemies in the board
        self.numberEnemies = 0
        ## List of all enemies in the board
        self.listEnemies = []
        ## List of Integer all enemies by type, e.g. value at index 0 represents the number of enemies of level 0
        self.listTypeEnemies = [0, 0, 0, 0, 0, 0, 0, 0]

        # Status bar info

        ## Integer time left in the game
        self.timeLeft = 200
        ## Boolean True if time has elapsed
        self.timeDone = False
        ## Integer player's score
        self.score = 0

    ## Reinitialize all of level's variables and bomberman's variable to start new level
    def setNewLevel(self):

        self.bomberman.reset()

        self.timeLeft = 200

        self.board = []
        self.bombQueue = []
        self.flashQueue = []

        self.powerUpCoord = [0, 0]
        self.exitCoord = [0, 0]
        self.powerUp = 0
        self.numberEnemies = 0
        self.listEnemies = []
        self.listTypeEnemies = [0, 0, 0, 0, 0, 0, 0, 0]

        self.clearBoard()
        self.clearBombs()

        self.setLevelInfo()
        self.setConcrete()
        self.setExit()
        self.setPowerup()
        # self.setBrick()
        self.setEnemies()
        self.setBomberman()

    ## This method activates the current level's powerup and add attribute to bomberman
    def gainPowerUp(self):
        if(self.powerUp == 1):
            self.bomberman.numBombs += 1
        if(self.powerUp == 2):
            self.bomberman.rangeOfBombs += 1
        if(self.powerUp == 3):
            self.bomberman.speed = 400
        if(self.powerUp == 4):
            self.bomberman.wallPass = True
        if(self.powerUp == 5):
            self.bomberman.hasDetonator = True
        if(self.powerUp == 6):
            self.bomberman.bombPass = True
        if(self.powerUp == 7):
            self.bomberman.flamePass = True
        if(self.powerUp == 8):
            self.bomberman.invincible = True

    ## This method returns the tile at x and y from the board
    def tileAt(self, x, y):
        return self.board[y][x].peek()

    ## This method sets tile at x and y on the board
    def setTileAt(self, x, y, tile):
        self.board[y][x].push(tile)

    ## This method removes the tile at x and y from the board
    def popTileAt(self, x, y):
        self.board[y][x].pop()

    ## This method lays a bomb at bomberman's current position
    def setBomb(self):
        self.bombQueue.append((self.bomberman.curX, self.bomberman.curY, constant.TIME_BOMB))
        tempTile = self.tileAt(self.bomberman.curX, self.bomberman.curY)
        self.popTileAt(self.bomberman.curX, self.bomberman.curY)
        self.setTileAt(self.bomberman.curX, self.bomberman.curY, Tile.Bomb)
        self.setTileAt(self.bomberman.curX, self.bomberman.curY, tempTile)

    # LEVEL SETUP

    ## This method clears all tiles on the board
    def clearBoard(self):
        self.board = [[Tile() for x in range(constant.BOARD_WIDTH)] for y in range(constant.BOARD_HEIGHT)]

    ## This method clears all bombs from the bomb queue
    def clearBombs(self):
        self.bombQueue = []

    ## This method sets concrete tiles systematically on the board
    def setConcrete(self):
        for y in range(constant.BOARD_HEIGHT):
            for x in range(constant.BOARD_WIDTH):
                if x == 0 or x == 30 or y == 0 or y == 12:
                    self.setTileAt(x,y,Tile.Concrete)
                elif x % 2 == 0 and y % 2 == 0:
                    self.setTileAt(x,y,Tile.Concrete)

    ## This method sets an exit tile randomly on the board and set a brick on top of it
    def setExit(self):
        while True:
            tempX = random.randint(1, constant.BOARD_WIDTH) - 1
            tempY = random.randint(1, constant.BOARD_HEIGHT) - 1

            if (self.tileAt(tempX, tempY) == Tile.Empty and not (tempX == 1 and tempY == constant.BOARD_HEIGHT - 2) and not (tempX == 1 and tempY == constant.BOARD_HEIGHT - 3) and not (tempX == 2 and tempY == constant.BOARD_HEIGHT - 2)):
                self.setTileAt(tempX, tempY, Tile.Exit)
                self.setTileAt(tempX, tempY, Tile.Brick)
                self.exitCoord[0] = tempX
                self.exitCoord[1] = tempY
                break

    ## This method fetches a the list of enemies and powerup matching the current level number
    def setLevelInfo(self):
        self.listTypeEnemies, self.powerUp = Enemy.getEnemyListAndPowerUp(self.levelNum)

    ## This method sets a powerup tile randomly on the board and set a brick on top of it
    def setPowerup(self):
        while True:
            tempX = random.randint(1, constant.BOARD_WIDTH) - 1
            tempY = random.randint(1, constant.BOARD_HEIGHT) - 1

            if (self.tileAt(tempX, tempY) == Tile.Empty and not (tempX == 1 and tempY == constant.BOARD_HEIGHT - 2) and not (tempX == 1 and tempY == constant.BOARD_HEIGHT - 3) and not (tempX == 2 and tempY == constant.BOARD_HEIGHT - 2)):
                self.setTileAt(tempX, tempY, Tile.Powerup)
                self.setTileAt(tempX, tempY, Tile.Brick)
                self.powerUpCoord[0] = tempX
                self.powerUpCoord[1] = tempY
                break

    ## This method sets brick tiles randomly on the board
    def setBrick(self):
        for y in range(constant.BOARD_HEIGHT):
            for x in range (constant.BOARD_WIDTH):
                if (self.tileAt(x, y) == Tile.Empty and not (x == 1 and y == constant.BOARD_HEIGHT - 2) and not (x == 1 and y == constant.BOARD_HEIGHT - 3) and not (x == 2 and y == constant.BOARD_HEIGHT - 2)):
                    if (random.random() <= constant.PERCENT_BRICK):
                        self.setTileAt(x, y, Tile.Brick)

    ## This method sets bomberman at x and y on the board
    def setBomberman(self):
        self.setTileAt(self.bomberman.curX,self.bomberman.curY,Tile.Bomberman)

    ## This method sets enemies randomly on the map
    def setEnemies(self):
        # print self.listTypeEnemies
        for i in range(8):
            for j in range(self.listTypeEnemies[i]):
                while True:
                    tempX = random.randint(1, constant.BOARD_WIDTH) - 1
                    tempY = random.randint(1, constant.BOARD_HEIGHT) - 1

                    if (self.tileAt(tempX, tempY) == Tile.Empty and not (tempX == 1 and tempY == constant.BOARD_HEIGHT - 2) and not (tempX == 1 and tempY == constant.BOARD_HEIGHT - 3) and not (tempX == 2 and tempY == constant.BOARD_HEIGHT - 2)):
                        self.setTileAt(tempX, tempY, i + 8)
                        tempList = [tempX, tempY, random.randint(0, 3), i + 8]
                        self.listEnemies.append(tempList)
                        self.numberEnemies += 1
                        break

    ## This method clears all enemies on the map and in the list of enemies and list of enemies type
    def clearEnemies(self):
        for enemy in self.listEnemies:
            self.popTileAt(enemy[0],enemy[1])
        self.numberEnemies = 0
        self.listEnemies = []
        self.listTypeEnemies = [0, 0, 0, 0, 0, 0, 0, 0]

    ## This method sets 8 mega enemies everywhere, used when bomb detonates an exit tile or powerup tile
    def setChaos(self):
        highestIndex = 0
        self.setLevelInfo()
        for x in xrange(len(self.listTypeEnemies)):
            if self.listTypeEnemies[x] != 0:
                highestIndex = x
        if highestIndex != 7:
            highestIndex += 1
        self.clearEnemies()

        self.listTypeEnemies[highestIndex] = 8

        self.setEnemies()

    ## This method sets 8 maximum level enemies everywhere
    def setSuperChaos(self):
        self.setLevelInfo()

        self.clearEnemies()

        self.listTypeEnemies[7] = 8

        self.setEnemies()