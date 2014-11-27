from PyQt4 import QtCore, QtGui
import random

from tile import Tile
from bomberman import Bomberman
from enemy import Enemy

class StatusBar(QtGui.QDockWidget):
    def __init__(self, parent=None):
        super(StatusBar, self).__init__(parent)
        self.livesLabel = QtGui.QLabel('Lives: ' + str(parent.bomberman.lives), self)
        self.livesLabel.setFixedWidth(100)
        self.livesLabel.move(50, 0)

        self.timeLeft = 200
        self.timesLabel = QtGui.QLabel('Time Left: ' + str(self.timeLeft), self)
        self.timesLabel.setFixedWidth(200)
        self.timesLabel.move(200, 0)

class Board(QtGui.QFrame):

    setBombermanLivesSignal = QtCore.pyqtSignal(int)
    resetTimerSignal = QtCore.pyqtSignal()
    pauseGameSignal = QtCore.pyqtSignal()
    endGameSignal = QtCore.pyqtSignal()
    gameOverSignal = QtCore.pyqtSignal()

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

    def __init__(self, username, level=1, parent=None):
        super(Board, self).__init__(parent)
        self.username = username
        self.level = level
        self.bomberman = Bomberman() #initialize bomberman attributes
        print "initializing board for level: " + str(level)
        self.initBoard()
        
    def initBoard(self):
        # self.statusBar = StatusBar(self)
        # self.adjustSize()
        self.timer = QtCore.QBasicTimer()

        self.fastTimer = QtCore.QTimer(self)
        self.fastTimer.timeout.connect(lambda : self.moveEnemy(4))
        self.normalTimer = QtCore.QTimer(self)
        self.normalTimer.timeout.connect(lambda : self.moveEnemy(3))
        self.slowTimer = QtCore.QTimer(self)
        self.slowTimer.timeout.connect(lambda : self.moveEnemy(2))
        self.slowestTimer = QtCore.QTimer(self)
        self.slowestTimer.timeout.connect(lambda : self.moveEnemy(1))

        Board.NumberEnemies = 0
        Board.ListofEnemies = []
        Board.NumEnemies = [0, 0, 0, 0, 0, 0, 0, 0]

        self.curX = 1
        self.curY = 11
        self.board = []
        self.bombQueue = []

        self.isStarted = False
        self.isPaused = False

        self.setFocusPolicy(QtCore.Qt.StrongFocus)

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
        self.timer.start(self.Speed, self)
        self.fastTimer.start(Board.FastMoveTime)
        self.normalTimer.start(Board.NormalMoveTime)
        self.slowTimer.start(Board.SlowMoveTime)
        self.slowestTimer.start(Board.SlowestMoveTime)

    def saveBoard(self):

        savedBoard = {}

        savedBoard['BoardWidth'] = self.BoardWidth
        savedBoard['BoardHeight'] = self.BoardHeight
        savedBoard['ViewWidth'] = self.ViewWidth
        savedBoard['ViewHeight'] = self.ViewHeight
        savedBoard['Speed'] = self.Speed
        savedBoard['FastMoveTime'] = self.FastMoveTime
        savedBoard['NormalMoveTime'] = self.NormalMoveTime
        savedBoard['SlowMoveTime'] = self.SlowMoveTime
        savedBoard['SlowestMoveTime'] = self.SlowestMoveTime
        savedBoard['FastCanMove'] = self.FastCanMove
        savedBoard['NormalCanMove'] = self.NormalCanMove
        savedBoard['SlowCanMove'] = self.SlowCanMove
        savedBoard['SlowestCanMove'] = self.SlowestCanMove
        savedBoard['BombermanCanMove'] = self.BombermanCanMove
        savedBoard['BombTime'] = self.BombTime
        savedBoard['FlashTime'] = self.FlashTime
        savedBoard['BrickPercent'] = Board.BrickPercent
        savedBoard['PowerupCoordinate'] = Board.PowerupCoordinate
        savedBoard['ExitCoordinate'] = Board.ExitCoordinate
        savedBoard['Level'] = Board.Level
        savedBoard['Powerup'] = Board.Powerup
        savedBoard['NumberEnemies'] = Board.NumberEnemies
        savedBoard['ListofEnemies'] = Board.ListofEnemies
        savedBoard['NumEnemies'] = Board.NumEnemies

        savedBoard['bomberman'] = self.bomberman 

        savedBoard['curX'] = self.curX
        savedBoard['curY'] = self.curY
        savedBoard['board'] = self.board
        savedBoard['bombQueue'] = self.bombQueue

        savedBoard['isStarted'] = self.isStarted
        savedBoard['isPaused'] = False

        savedBoard['timeLeft'] = self.findChild(QtGui.QDockWidget).timeLeft

        return savedBoard

    def loadBoard(self, savedBoard):
        self.BoardWidth = savedBoard['BoardWidth'] 
        self.BoardHeight = savedBoard['BoardHeight']
        self.ViewWidth = savedBoard['ViewWidth']
        self.ViewHeight = savedBoard['ViewHeight']
        self.Speed = savedBoard['Speed']
        self.FastMoveTime = savedBoard['FastMoveTime']
        self.NormalMoveTime = savedBoard['NormalMoveTime']
        self.SlowMoveTime = savedBoard['SlowMoveTime']
        self.SlowestMoveTime = savedBoard['SlowestMoveTime']
        self.FastCanMove = savedBoard['FastCanMove']
        self.NormalCanMove = savedBoard['NormalCanMove']
        self.SlowCanMove = savedBoard['SlowCanMove']
        self.SlowestCanMove = savedBoard['SlowestCanMove']
        self.BombermanCanMove = savedBoard['BombermanCanMove']
        self.BombTime = savedBoard['BombTime']
        self.FlashTime = savedBoard['FlashTime']
        Board.BrickPercent = savedBoard['BrickPercent']
        Board.PowerupCoordinate = savedBoard['PowerupCoordinate']
        Board.ExitCoordinate = savedBoard['ExitCoordinate']
        Board.Level = savedBoard['Level']
        Board.Powerup = savedBoard['Powerup']
        Board.NumberEnemies = savedBoard['NumberEnemies']
        Board.ListofEnemies = savedBoard['ListofEnemies']
        Board.NumEnemies = savedBoard['NumEnemies']

        self.bomberman = savedBoard['bomberman']

        self.curX = savedBoard['curX']
        self.curY = savedBoard['curY']
        self.board = savedBoard['board']
        self.bombQueue = savedBoard['bombQueue']

        self.isStarted = savedBoard['isStarted']
        self.isPaused = savedBoard['isPaused']

        self.findChild(QtGui.QDockWidget).timeLeft = savedBoard['timeLeft']

        self.update()

    def pause(self):

        if not self.isStarted:
            return

        self.isPaused = not self.isPaused

        if self.isPaused:
            self.timer.stop()
            self.fastTimer.stop()
            self.normalTimer.stop()
            self.slowTimer.stop()
            self.slowestTimer.stop()
            self.pauseGameSignal.emit() # Send signal to show pauseMenu
        else:
            self.timer.start(self.Speed, self)
            self.fastTimer.start(Board.FastMoveTime)
            self.normalTimer.start(Board.NormalMoveTime)
            self.slowTimer.start(Board.SlowMoveTime)
            self.slowestTimer.start(Board.SlowestMoveTime)

        self.update()

    def death(self):

        #stop timer
        self.timer.stop()

        #change attributes
        self.bomberman.lives = self.bomberman.lives - 1
        self.bomberman.hasDetonator = 0
        self.bomberman.bombPass = 0
        self.bomberman.wallPass = 0
        self.bomberman.flamePass = 0

        if(self.bomberman.lives == 0):
            self.gameOverSignal.emit() # Send signal to end game
        else:
            self.endGameSignal.emit() # Send signal to end current board


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
        self.NumEnemies, self.Powerup = Enemy.getEnemyListAndPowerUp(self.level)

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

                if(shape == Tile.Exit):
                    exitPix = QtGui.QPixmap("./images/exit.png")
                    painter.drawPixmap(rect.left() + (j-viewXFirst) * self.squareWidth(),
                    boardTop + i * self.squareHeight(),exitPix)
                elif(shape == Tile.Brick):
                    brickPix = QtGui.QPixmap("./images/brick.png")
                    scaledBrickPix = QtGui.QPixmap.scaled(brickPix,self.squareWidth() + 1,self.squareHeight() + 1,0)
                    painter.drawPixmap(rect.left() + (j-viewXFirst) * self.squareWidth(),
                    boardTop + i * self.squareHeight(),scaledBrickPix)
                elif(shape == Tile.Balloom):
                    balloomPix = QtGui.QPixmap("./images/Balloom.png")
                    scaledBalloomPix = QtGui.QPixmap.scaled(balloomPix,self.squareWidth() + 1,self.squareHeight() + 1,0)
                    painter.drawPixmap(rect.left() + (j-viewXFirst) * self.squareWidth(),
                    boardTop + i * self.squareHeight(),scaledBalloomPix)
                elif(shape == Tile.Bomb):
                    bombPix = QtGui.QPixmap("./images/bomb.png")
                    scaledBombPix = QtGui.QPixmap.scaled(bombPix,self.squareWidth() + 1,self.squareHeight() + 1,0)
                    painter.drawPixmap(rect.left() + (j-viewXFirst) * self.squareWidth(),
                    boardTop + i * self.squareHeight(),scaledBombPix)
                elif(shape == Tile.Concrete):
                    concretePix = QtGui.QPixmap("./images/concrete.png")
                    scaledConcretePix = QtGui.QPixmap.scaled(concretePix,self.squareWidth() + 1,self.squareHeight() + 1,0)
                    painter.drawPixmap(rect.left() + (j-viewXFirst) * self.squareWidth(),
                    boardTop + i * self.squareHeight(),scaledConcretePix)
                else:
                    self.drawSquare(painter,
                        rect.left() + (j-viewXFirst) * self.squareWidth(),
                        boardTop + i * self.squareHeight(), shape)

    def drawSquare(self, painter, x, y, shape):
        
        colorTable = [0x009700, 0x999999, 0x996633, 0xCC0000,
                      0xFFCC00, 0x000000, 0xFFFFFF, 0xFF9900,
                      0xFF6600, 0x00FFFF, 0xCC0099, 0xFF9933,
                      0xFF6600, 0x00FFFF, 0xCC0099, 0xFF9933]

        color = QtGui.QColor(colorTable[shape])

        if (shape == Tile.Empty or shape == Tile.Flash):
            painter.fillRect(x + 1, y + 1, self.squareWidth(), 
            self.squareHeight(), color)
        else:
            painter.fillRect(x + 1, y + 1, self.squareWidth(), 
                self.squareHeight(), color)

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

    def moveEnemy(self, speed):
        for i in range(Board.NumberEnemies):
            if (Enemy.getEnemy(Board.ListofEnemies[i][3])['speed'] == speed):
                curX = Board.ListofEnemies[i][0]
                curY = Board.ListofEnemies[i][1]
                tempDir = Board.ListofEnemies[i][2]
                tempWP = Enemy.getEnemy(Board.ListofEnemies[i][3])['wallpass']
                newX = 0
                newY = 0

                if (tempDir == 0):
                    newX = curX
                    newY = curY + 1
                elif (tempDir == 1):
                    newX = curX + 1
                    newY = curY
                elif (tempDir == 2):
                    newX = curX
                    newY = curY - 1
                elif (tempDir == 3):
                    newX = curX - 1
                    newY = curY

                tempTile = self.board[newY][newX].peek()

                if (tempTile == Tile.Bomb or tempTile == Tile.Brick or tempTile == Tile.Concrete):
                    if (tempDir == 0): newY -= 2
                    elif (tempDir == 1): newX -= 2
                    elif (tempDir == 2): newY += 2
                    elif (tempDir == 3): newX += 2
                    Board.ListofEnemies[i][2] = (Board.ListofEnemies[i][2] + 2) % 4

                tempTile = self.board[newY][newX].peek()

                if (tempTile == Tile.Bomb or tempTile == Tile.Brick or tempTile == Tile.Concrete):
                    Board.ListofEnemies[i][2] = (Board.ListofEnemies[i][2] + 1) % 4

                tempTile = self.board[newY][newX].peek()

                if (tempTile != Tile.Bomb and tempTile != Tile.Brick and tempTile != Tile.Concrete):
                    Board.ListofEnemies[i][0] = newX
                    Board.ListofEnemies[i][1] = newY

                    self.popTileAt(curX, curY)
                    self.setTileAt(newX, newY, i + 8)


    def bombermanCanMove(self):
        Board.BombermanCanMove = True

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
            if (modX < Board.BoardWidth-1):
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
            if (modX < Board.BoardWidth-1):
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


    def startFlash(self, flashList):
        for x,y in flashList:
            self.setTileAt(x,y,Tile.Flash)

    def endFlash(self, flashList):
        for x,y in flashList:
            self.popTileAtWithoutUpdate(x,y)
    
    def destroyTiles(self,popList):
        for x,y in popList:
            self.popTileAtWithoutUpdate(x,y)
        return True

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