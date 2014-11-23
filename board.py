from PyQt4 import QtCore, QtGui
import random

from tile import Tile


class Board(QtGui.QFrame):

    msg2Statusbar = QtCore.pyqtSignal(str)

    BoardWidth = 31
    BoardHeight = 13
    ViewWidth = 13
    ViewHeight = 13
    Speed = 300
    BombTime = 3000
    FlashTime = 700
    BombRadius = 3
    NumberBricks = 8
    BrickPercent = 0.12
    PowerupCoordinate = [0, 0]
    ExitCoordinate = [0, 0]
    Level = 1
    
    NumEnemies = [0, 0, 0, 0, 0, 0, 0, 0]

    def __init__(self, parent):
        super(Board, self).__init__(parent)
        self.initBoard()
        
    def initBoard(self):     

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
        self.setBomberman()

        self.timer.start(Board.Speed, self)

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
            tempX = random.randint(1, self.BoardWidth) - 1
            tempY = random.randint(1, self.BoardHeight) - 1

            if (self.tileAt(tempX, tempY) == Tile.Empty and not (tempX == 1 and tempY == Board.BoardHeight - 2) and not (tempX == 1 and tempY == Board.BoardHeight - 3) and not (tempX == 2 and tempY == Board.BoardHeight - 2)):
                self.setTileAt(tempX, tempY, Tile.Exit)
                self.setTileAt(tempX, tempY, Tile.Brick)
                Board.ExitCoordinate[0] = tempX
                Board.ExitCoordinate[1] = tempY
                break

    def setPowerup(self):
        while True:
            tempX = random.randint(1, self.BoardWidth) - 1
            tempY = random.randint(1, self.BoardHeight) - 1

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
        for i in range(self.NumEnemies[0]):
            while True:
                tempX = random.randint(1, self.BoardWidth) - 1
                tempY = random.randint(1, self.BoardHeight) - 1

                if (self.tileAt(tempX, tempY) == Tile.Empty and not (tempX == 1 and tempY == Board.BoardHeight - 2) and not (tempX == 1 and tempY == Board.BoardHeight - 3) and not (tempX == 2 and tempY == Board.BoardHeight - 2)):
                    self.setTileAt(tempX, tempY, Tile.Balloom)
                    break

    def paintEvent(self, event):

        # Check for bomberman X pos for moving viewPort
        print self.curX
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
                      0xFFCC00, 0xCC66CC, 0x66CCCC, 0xFF9900,
                      0x0033CC]

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
        
        # if key == QtCore.Qt.Key_P:
        #     self.pause()
        #     return
            
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
            self.setBomb()
            
        else:
            super(Board, self).keyPressEvent(event)

    def tryMove(self, newX, newY):
        if (self.tileAt(newX,newY) == Tile.Concrete or self.tileAt(newX,newY) == Tile.Brick or self.tileAt(newX,newY) == Tile.Bomb):
            return False
        self.popTileAt(self.curX,self.curY)
        self.curX = newX
        self.curY = newY
        self.setTileAt(self.curX,self.curY,Tile.Bomberman)
        
        return True

    def setBomb(self):
        self.bombQueue.append((self.curX,self.curY))
        tempTile = self.tileAt(self.curX,self.curY)
        self.popTileAt(self.curX,self.curY)
        self.setTileAt(self.curX,self.curY,Tile.Bomb)
        self.setTileAt(self.curX,self.curY,tempTile)
        QtCore.QTimer.singleShot(Board.BombTime, self.detonateBomb)

    def timerEvent(self, event):
        
        if event.timerId() == self.timer.timerId():
            pass
        else:
            super(Board, self).timerEvent(event)

    def detonateBomb(self):

        x, y = self.bombQueue.pop(0)
        self.popTileAt(x,y)

        flashList = []
        popList = []

        # NORTH
        for i in range(1,Board.BombRadius+1):
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
        for i in range(1,Board.BombRadius+1):
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
        for i in range(1,Board.BombRadius+1):
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
        for i in range(1,Board.BombRadius+1):
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
