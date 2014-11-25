from PyQt4 import QtCore, QtGui
import random

from tile import Tile
from bomberman import Bomberman
from enemy import Enemy


class Board(QtGui.QFrame):

    msg2Statusbar = QtCore.pyqtSignal(str)
    pauseGameSignal = QtCore.pyqtSignal()

    BoardWidth = 31
    BoardHeight = 13
    ViewWidth = 13
    ViewHeight = 13
    Speed = 300
    FastMoveTime = 200
    NormalMoveTime = 300
    SlowMoveTime = 600
    SlowestMoveTime = 800
    FastCanMove = True
    NormalCanMove = True
    SlowCanMove = True
    SlowestCanMove = True
    BombermanCanMove = True
    BombTime = 3000
    FlashTime = 700
    BrickPercent = 0.12
    PowerupCoordinate = [0, 0]
    ExitCoordinate = [0, 0]
    Level = 15
    Powerup = 0
    NumberEnemies = 0
    ListofEnemies = []
    NumEnemies = [0, 0, 0, 0, 0, 0, 0, 0]

    # print Enemy.getEnemy(8)['points']

    def __init__(self, parent, level=1):
        super(Board, self).__init__(parent)
        Level = level
        print "initializing board for level: " + str(level)
        self.initBoard()
        
    def initBoard(self):     
        self.bomberman = Bomberman() #initialize bomberman attributes
        self.timer = QtCore.QBasicTimer()

        self.curX = 1
        self.curY = 11
        self.board = []
        self.bombQueue = []

        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.isStarted = False
        self.isPaused = False

    def start(self):
        
        if self.isPaused:
            return

        self.isStarted = True
        self.clearBoard()
        self.clearBombs()
        self.setConcrete()
        self.setExit()
        self.setPowerup()
        self.setBrick()
        self.setEnemies()
        print Board.ListofEnemies
        self.setBomberman()
        self.timer.start(Board.Speed, self)

    def pause(self):

        if not self.isStarted:
            return

        self.isPaused = not self.isPaused

        if self.isPaused:
            self.timer.stop()
            self.pauseGameSignal.emit() #send signal to show pauseMenu
        else:
            self.timer.start(Board.Speed, self)

        self.update()

    def tileAt(self, x, y):
        return self.board[y][x].peek()

    def setTileAt(self, x, y, tile):
        self.board[y][x].push(tile)
        self.update()

    def setTileAtWithoutUpdate(self, x, y, tile):
        self.board[y][x].push(tile)

    def popTileAt(self, x, y):
        self.board[y][x].pop()
        self.update()

    def popTileAtWithoutUpdate(self, x, y):
        self.board[y][x].pop()

    def squareWidth(self):
        return self.contentsRect().width() / Board.ViewWidth
        
    def squareHeight(self):
        return self.contentsRect().height() / Board.ViewHeight

    def clearBoard(self):
        self.board = [[Tile() for x in range(Board.BoardWidth)] for y in range(Board.BoardHeight)]

    def clearBombs(self):
        self.bombQueue = []

    def setConcrete(self):
        for y in range(Board.BoardHeight):
            for x in range(Board.BoardWidth):
                if x == 0 or x == 30 or y == 0 or y == 12:
                    self.setTileAt(x,y,Tile.Concrete)
                elif x % 2 == 0 and y % 2 == 0:
                    self.setTileAt(x,y,Tile.Concrete)

    def setExit(self):
        while True:
            tempX = random.randint(1, Board.BoardWidth) - 1
            tempY = random.randint(1, Board.BoardHeight) - 1

            if (self.tileAt(tempX, tempY) == Tile.Empty and not (tempX == 1 and tempY == Board.BoardHeight - 2) and not (tempX == 1 and tempY == Board.BoardHeight - 3) and not (tempX == 2 and tempY == Board.BoardHeight - 2)):
                self.setTileAt(tempX, tempY, Tile.Exit)
                self.setTileAt(tempX, tempY, Tile.Brick)
                Board.ExitCoordinate[0] = tempX
                Board.ExitCoordinate[1] = tempY
                break

    def setPowerup(self):
        while True:
            tempX = random.randint(1, Board.BoardWidth) - 1
            tempY = random.randint(1, Board.BoardHeight) - 1

            if (self.tileAt(tempX, tempY) == Tile.Empty and not (tempX == 1 and tempY == Board.BoardHeight - 2) and not (tempX == 1 and tempY == Board.BoardHeight - 3) and not (tempX == 2 and tempY == Board.BoardHeight - 2)):
                self.setTileAt(tempX, tempY, Tile.Powerup)
                self.setTileAt(tempX, tempY, Tile.Brick)
                Board.PowerupCoordinate[0] = tempX
                Board.PowerupCoordinate[1] = tempY
                break

    def setBrick(self):
        for y in range(Board.BoardHeight):
            for x in range (Board.BoardWidth):
                if (self.tileAt(x, y) == Tile.Empty and not (x == 1 and y == Board.BoardHeight - 2) and not (x == 1 and y == Board.BoardHeight - 3) and not (x == 2 and y == Board.BoardHeight - 2)):
                    if (random.random() <= Board.BrickPercent):
                        self.setTileAt(x, y, Tile.Brick)

    def setBomberman(self):
        self.setTileAt(self.curX,self.curY,Tile.Bomberman)

    def setEnemies(self):
        if self.Level == 1:
            self.NumEnemies = [6, 0, 0, 0, 0, 0, 0, 0]
            Board.Powerup = 2
        elif self.Level == 2:
            self.NumEnemies = [3, 3, 0, 0, 0, 0, 0, 0]
            Board.Powerup = 1
        elif self.Level == 3:
            self.NumEnemies = [2, 2, 2, 0, 0, 0, 0, 0]
            Board.Powerup = 5
        elif self.Level == 4:
            self.NumEnemies = [1, 1, 2, 2, 0, 0, 0, 0]
            Board.Powerup = 3
        elif self.Level == 5:
            self.NumEnemies = [0, 0, 4, 3, 0, 0, 0, 0]
            Board.Powerup = 1
        elif self.Level == 6:
            self.NumEnemies = [0, 2, 3, 2, 0, 0, 0, 0]
            Board.Powerup = 1
        elif self.Level == 7:
            self.NumEnemies = [0, 2, 3, 0, 2, 0, 0, 0]
            Board.Powerup = 2
        elif self.Level == 8:
            self.NumEnemies = [0, 1, 2, 4, 0, 0, 0, 0]
            Board.Powerup = 5
        elif self.Level == 9:
            self.NumEnemies = [0, 1, 1, 4, 1, 0, 0, 0]
            Board.Powerup = 6
        elif self.Level == 10:
            self.NumEnemies = [0, 1, 1, 1, 3, 1, 0, 0]
            Board.Powerup = 4
        elif self.Level == 11:
            self.NumEnemies = [0, 1, 2, 3, 1, 1, 0, 0]
            Board.Powerup = 1
        elif self.Level == 12:
            self.NumEnemies = [0, 1, 1, 1, 4, 1, 0, 0]
            Board.Powerup = 1
        elif self.Level == 13:
            self.NumEnemies = [0, 0, 3, 3, 3, 0, 0, 0]
            Board.Powerup = 5
        elif self.Level == 14:
            self.NumEnemies = [0, 0, 0, 0, 0, 7, 1, 0]
            Board.Powerup = 6
        elif self.Level == 15:
            self.NumEnemies = [0, 0, 1, 3, 3, 0, 1, 0]
            Board.Powerup = 2
        elif self.Level == 16:
            self.NumEnemies = [0, 0, 0, 3, 4, 0, 1, 0]
            Board.Powerup = 4

        for i in range(8):
            for j in range(self.NumEnemies[i]):
                while True:
                    tempX = random.randint(1, Board.BoardWidth) - 1
                    tempY = random.randint(1, Board.BoardHeight) - 1

                    if (self.tileAt(tempX, tempY) == Tile.Empty and not (tempX == 1 and tempY == Board.BoardHeight - 2) and not (tempX == 1 and tempY == Board.BoardHeight - 3) and not (tempX == 2 and tempY == Board.BoardHeight - 2)):
                        self.setTileAt(tempX, tempY, i + 8)
                        tempList = [tempX, tempY, random.randint(1,4), i + 8]
                        Board.ListofEnemies.append(tempList)
                        Board.NumberEnemies += 1
                        break


    def paintEvent(self, event):

        # Check for bomberman X pos for moving viewPort
        if self.curX <= 6:
            viewXFirst = 0
            viewXLast = 12
        elif self.curX >= 24:
            viewXFirst = 18
            viewXLast = 30
        else:
            viewXFirst = self.curX - 6
            viewXLast = self.curX + 6

        painter = QtGui.QPainter(self)
        rect = self.contentsRect()

        boardTop = rect.bottom() - Board.ViewHeight * self.squareHeight()

        for i in range(Board.BoardHeight):
            for j in range(viewXFirst,viewXLast+1):
                shape = self.tileAt(j, Board.BoardHeight - i - 1)
                
                self.drawSquare(painter,
                    rect.left() + (j-viewXFirst) * self.squareWidth(),
                    boardTop + i * self.squareHeight(), shape)

    def drawSquare(self, painter, x, y, shape):
        
        colorTable = [0x99CC33, 0x999999, 0x996633, 0xCC0000,
                      0xFFCC00, 0x000000, 0x66CCCC, 0xFF9900,
                      0xFF6600, 0x00FFFF, 0xCC0099, 0xFF9933,
                      0xFF6600, 0x00FFFF, 0xCC0099, 0xFF9933]

        color = QtGui.QColor(colorTable[shape])
        painter.fillRect(x + 1, y + 1, self.squareWidth() - 2, 
            self.squareHeight() - 2, color)

        painter.setPen(color.light())
        painter.drawLine(x, y + self.squareHeight() - 1, x, y)
        painter.drawLine(x, y, x + self.squareWidth() - 1, y)

        painter.setPen(color.dark())
        painter.drawLine(x + 1, y + self.squareHeight() - 1,
            x + self.squareWidth() - 1, y + self.squareHeight() - 1)
        painter.drawLine(x + self.squareWidth() - 1, 
            y + self.squareHeight() - 1, x + self.squareWidth() - 1, y + 1)

    def keyPressEvent(self, event):

        key = event.key()
        
        if key == QtCore.Qt.Key_P:
            self.pause()
            return
            
        if self.isPaused:
            return
                
        elif key == QtCore.Qt.Key_Left:
            if self.curX == 0:
                return
            self.tryMove(self.curX-1,self.curY)
            
        elif key == QtCore.Qt.Key_Right:
            if self.curX == Board.BoardWidth - 1:
                return
            self.tryMove(self.curX+1,self.curY)
            
        elif key == QtCore.Qt.Key_Down:
            if self.curY == 0:
                return
            self.tryMove(self.curX,self.curY-1)
            
        elif key == QtCore.Qt.Key_Up:
            if self.curY == Board.BoardHeight-1:
                return
            self.tryMove(self.curX,self.curY+1)

        elif key == QtCore.Qt.Key_Space:
            if (len(self.bombQueue) < self.bomberman.numBombs):
                self.setBomb()

        elif key == QtCore.Qt.Key_B:
            if (self.bomberman.hasDetonator == 1 and self.bombQueue):
                self.detonateBomb()
            
        else:
            super(Board, self).keyPressEvent(event)

    def tryMove(self, newX, newY):
        if (self.bomberman.wallPass == 1):
            if (self.tileAt(newX,newY) == Tile.Concrete or self.tileAt(newX,newY) == Tile.Bomb or Board.BombermanCanMove == False):
                return False
        elif (self.bomberman.bombPass == 1):
            if (self.tileAt(newX,newY) == Tile.Concrete or self.tileAt(newX,newY) == Tile.Brick or Board.BombermanCanMove == False):
                return False
        elif (self.bomberman.wallPass == 1 and self.bomberman.bombPass == 1):
            if (self.tileAt(newX,newY) == Tile.Concrete or Board.BombermanCanMove == False):
                return False
        elif (self.tileAt(newX,newY) == Tile.Concrete or self.tileAt(newX,newY) == Tile.Brick or self.tileAt(newX,newY) == Tile.Bomb or Board.BombermanCanMove == False):
            return False
        self.popTileAt(self.curX,self.curY)
        self.curX = newX
        self.curY = newY
        if (self.tileAt(self.curX,self.curY) == Tile.Powerup):
            self.popTileAt(newX, newY)
            self.gainPowerUps(Board.Powerup)
        self.setTileAt(self.curX,self.curY,Tile.Bomberman)
        Board.BombermanCanMove = False
        QtCore.QTimer.singleShot(Board.NormalMoveTime, self.bombermanCanMove)

        return True

    def tryMoveFast(self):
        for i in range(Board.NumberEnemies):
            if (Enemy.getEnemy(Board.ListofEnemies[i][3])['speed'] == 4):
                print Board.ListofEnemies[i]

    def bombermanCanMove(self):
        Board.BombermanCanMove = True

    def fastCanMove(self):
        Board.FastCanMove = True

    def normalCanMove(self):
        Board.NormalCanMove = True

    def slowCanMove(self):
        Board.SlowCanMove = True

    def slowestCanMove(self):
        Board.SlowestCanMove = True


    def setBomb(self):
        self.bombQueue.append((self.curX,self.curY))
        tempTile = self.tileAt(self.curX,self.curY)
        self.popTileAt(self.curX,self.curY)
        self.setTileAt(self.curX,self.curY,Tile.Bomb)
        self.setTileAt(self.curX,self.curY,tempTile)
        if (self.bomberman.hasDetonator == 0):
            QtCore.QTimer.singleShot(Board.BombTime, self.detonateBomb)

    def timerEvent(self, event):
        
        if event.timerId() == self.timer.timerId():
            pass
        else:
            super(Board, self).timerEvent(event)

    def detonateBomb(self):

        x, y = self.bombQueue.pop(0)
        if (self.tileAt(x,y) == Tile.Bomberman):
            self.popTileAt(x,y)
            self.popTileAt(x,y)
            self.setTileAt(x,y,Tile.Bomberman)
        else:
            self.popTileAt(x,y)

        flashList = []
        popList = []

        # NORTH
        for i in range(1,self.bomberman.rangeOfBombs+1):
            modY = y + i
            if (modY < Board.BoardHeight-1):
                northTile = self.tileAt(x,modY)
                if (northTile == Tile.Concrete or northTile == Tile.Bomb):
                    break
                flashList.append((x,modY))
                if (northTile == Tile.Brick):
                    popList.append((x,modY))
                    break
        # SOUTH
        for i in range(1,self.bomberman.rangeOfBombs+1):
            modY = y - i
            if (modY < Board.BoardHeight-1):
                northTile = self.tileAt(x,modY)
                if (northTile == Tile.Concrete or northTile == Tile.Bomb):
                    break
                flashList.append((x,modY))
                if (northTile == Tile.Brick):
                    popList.append((x,modY))
                    break
        # EAST
        for i in range(1,self.bomberman.rangeOfBombs+1):
            modX = x + i
            if (modX < Board.BoardHeight-1):
                northTile = self.tileAt(modX,y)
                if (northTile == Tile.Concrete or northTile == Tile.Bomb):
                    break
                flashList.append((modX,y))
                if (northTile == Tile.Brick):
                    popList.append((modX,y))
                    break        
        # WEST
        for i in range(1,self.bomberman.rangeOfBombs+1):
            modX = x - i
            if (modX < Board.BoardHeight-1):
                northTile = self.tileAt(modX,y)
                if (northTile == Tile.Concrete or northTile == Tile.Bomb):
                    break
                flashList.append((modX,y))
                if (northTile == Tile.Brick):
                    popList.append((modX,y))
                    break        

        self.startFlash(flashList)
        self.endFlash(flashList)
        self.destroyTiles(popList)

    def startFlash(self,flashList):
        for x,y in flashList:
            self.setTileAt(x,y,Tile.Flash)

    def endFlash(self,flashList):
         for x,y in flashList:
            self.popTileAtWithoutUpdate(x,y)
    
    def destroyTiles(self,popList):
        for x,y in popList:
            self.popTileAtWithoutUpdate(x,y)

    def gainPowerUps(self, powerUpNum):
        if(powerUpNum == 1):
            self.bomberman.numBombs = self.bomberman.numBombs + 1
        if(powerUpNum == 2):
            self.bomberman.rangeOfBombs = self.bomberman.rangeOfBombs + 1
        if(powerUpNum == 3):
            self.bomberman.speed = 4
        if(powerUpNum == 4):
            self.bomberman.wallPass = 1
        if(powerUpNum == 5):
            self.bomberman.hasDetonator = 1
        if(powerUpNum == 6):
            self.bomberman.bombPass = 1
        if(powerUpNum == 7):
            self.bomberman.flamePass = 1
        if(powerUpNum == 8):
            self.bomberman.invincible = 1