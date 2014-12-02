import random

from src import constant
from tile import Tile
from enemy import Enemy
from bomberman import Bomberman


class Level(object):

    def __init__(self, username, levelNum):

        # Initialize level
        self.bomberman = Bomberman()

        # Game info
        self.username = username

        # Level info
        self.levelNum = levelNum
        self.isInitialized = False

        self.board = []
        self.bombQueue = []
        self.flashQueue = []

        self.powerUpCoord = [0, 0]
        self.exitCoord = [0, 0]
        self.powerUp = 0
        self.numberEnemies = 0
        self.listEnemies = []
        self.listTypeEnemies = [0, 0, 0, 0, 0, 0, 0, 0]

        # Status bar info
        self.timeLeft = 200
        self.timeDone = False
        self.score = 0

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

    def gainPowerUp(self):
        if(self.powerUp == 1):
            self.bomberman.numBombs += 1
        if(self.powerUp == 2):
            self.bomberman.rangeOfBombs += 1
        if(self.powerUp == 3):
            self.bomberman.speed = constant.TIME_FAST
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

    def tileAt(self, x, y):
        return self.board[y][x].peek()

    def setTileAt(self, x, y, tile):
        self.board[y][x].push(tile)

    def popTileAt(self, x, y):
        self.board[y][x].pop()

    def setBomb(self):
        self.bombQueue.append((self.bomberman.curX, self.bomberman.curY, constant.TIME_BOMB))
        tempTile = self.tileAt(self.bomberman.curX, self.bomberman.curY)
        self.popTileAt(self.bomberman.curX, self.bomberman.curY)
        self.setTileAt(self.bomberman.curX, self.bomberman.curY, Tile.Bomb)
        self.setTileAt(self.bomberman.curX, self.bomberman.curY, tempTile)

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
        self.listTypeEnemies, self.powerUp = Enemy.getEnemyListAndPowerUp(self.levelNum)

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
        self.setTileAt(self.bomberman.curX,self.bomberman.curY,Tile.Bomberman)

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

    def clearEnemies(self):
        for enemy in self.listEnemies:
            self.popTileAt(enemy[0],enemy[1])
        self.numberEnemies = 0
        self.listEnemies = []
        self.listTypeEnemies = [0, 0, 0, 0, 0, 0, 0, 0]

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

    def setSuperChaos(self):
        self.setLevelInfo()

        self.clearEnemies()

        self.listTypeEnemies[7] = 8

        self.setEnemies()