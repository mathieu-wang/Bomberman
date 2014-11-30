import random
import constant

from tile import Tile
from enemy import Enemy

class Bomberman(object):

    def __init__(self, username, level):

        # Game info
        self.username = username

        # Level info
        self.level = level
        self.isInitialized = False

        # Bomberman info
        self.curX = 1
        self.curY = 11
        self.board = []
        self.bombQueue = []
        self.lives = 3
        self.speed = 300
        self.canMove = True

        self.powerUpCoord = [0, 0]
        self.exitCoord = [0, 0]
        self.powerUp = 0
        self.numberEnemies = 0
        self.listEnemies = []
        self.listTypeEnemies = [0, 0, 0, 0, 0, 0, 0, 0]

        # Power ups
        self.numBombs = 1 #
        self.rangeOfBombs = 1 #
        self.wallPass = False #
        self.hasDetonator = False
        self.bombPass = False #
        self.flamePass = False #
        self.invincible = False #

    def setNewLevel(self):

        self.curX = 1
        self.curY = 11
        self.board = []
        self.bombQueue = []
        self.lives = 3
        self.speed = 300
        self.canMove = True

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

    def gainPowerUp(self):
        if(self.powerUp == 1):
            self.numBombs += 1
        if(self.powerUp == 2):
            self.rangeOfBombs += 1
        if(self.powerUp == 3):
            self.speed = 400
        if(self.powerUp == 4):
            self.wallPass = True
        if(self.powerUp == 5):
            self.hasDetonator = True
        if(self.powerUp == 6):
            self.bombPass = True
        if(self.powerUp == 7):
            self.flamePass = True
        if(self.powerUp == 8):
            self.invincible = True

    def tileAt(self, x, y):
        return self.board[y][x].peek()

    def setTileAt(self, x, y, tile):
        self.board[y][x].push(tile)

    def popTileAt(self, x, y):
        self.board[y][x].pop()

    def setBomb(self):
        self.bombQueue.append((self.curX, self.curY, constant.TIME_BOMB))
        tempTile = self.tileAt(self.curX, self.curY)
        self.popTileAt(self.curX, self.curY)
        self.setTileAt(self.curX, self.curY, Tile.Bomb)
        self.setTileAt(self.curX, self.curY, tempTile)

    # LEVEL SETUP

    def clearBoard(self):
        self.board = [[Tile() for x in range(constant.BOARD_WIDTH)] for y in range(constant.BOARD_HEIGHT)]

    def clearBombs(self):
        self.bombQueue = []

    def setConcrete(self):
        for y in range(constant.BOARD_HEIGHT):
            for x in range(constant.BOARD_WIDTH):
                if x == 0 or x == 30 or y == 0 or y == 12:
                    self.setTileAt(x,y,Tile.Concrete)
                elif x % 2 == 0 and y % 2 == 0:
                    self.setTileAt(x,y,Tile.Concrete)

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

    def setLevelInfo(self):
        self.listTypeEnemies, self.powerUp = Enemy.getEnemyListAndPowerUp(self.level)

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

    def setBrick(self):
        for y in range(constant.BOARD_HEIGHT):
            for x in range (constant.BOARD_WIDTH):
                if (self.tileAt(x, y) == Tile.Empty and not (x == 1 and y == constant.BOARD_HEIGHT - 2) and not (x == 1 and y == constant.BOARD_HEIGHT - 3) and not (x == 2 and y == constant.BOARD_HEIGHT - 2)):
                    if (random.random() <= constant.PERCENT_BRICK):
                        self.setTileAt(x, y, Tile.Brick)

    def setBomberman(self):
        self.setTileAt(self.curX,self.curY,Tile.Bomberman)

    def setEnemies(self):
        for i in range(8):
            for j in range(self.listTypeEnemies[i]):
                while True:
                    tempX = random.randint(1, constant.BOARD_WIDTH) - 1
                    tempY = random.randint(1, constant.BOARD_HEIGHT) - 1

                    if (self.tileAt(tempX, tempY) == Tile.Empty and not (tempX == 1 and tempY == constant.BOARD_HEIGHT - 2) and not (tempX == 1 and tempY == constant.BOARD_HEIGHT - 3) and not (tempX == 2 and tempY == constant.BOARD_HEIGHT - 2)):
                        self.setTileAt(tempX, tempY, i + 8)
                        tempList = [tempX, tempY, random.randint(1,4), i + 8]
                        self.listEnemies.append(tempList)
                        self.numberEnemies += 1
                        break

    def clearEnemies(self):
        for enemy in self.listEnemies:
            self.popTileAt(enemy[0],enemy[1])
        self.numberEnemies = 0
        self.listEnemies = []
        self.listTypeEnemies = [0, 0, 0, 0, 0, 0, 0, 0]

    def setChaos(self):

        self.clearEnemies()
        self.setLevelInfo()

        highestIndex = 0
        for x in xrange(self.listTypeEnemies):
            if listTypeEnemies[x] != 0:
                highestIndex = x
        if highestIndex != 7:
            highestIndex += 1
        self.listTypeEnemies[highestIndex] = 8

        self.setEnemies()


    