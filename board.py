from PyQt4 import QtCore, QtGui
import random
import constant

from tile import Tile
from enemy import Enemy

class StatusBar(QtGui.QDockWidget):
    def __init__(self, parent=None):
        super(StatusBar, self).__init__(parent)
        self.livesLabel = QtGui.QLabel('Lives: ' + str(parent.level.bomberman.lives), self)
        self.livesLabel.setFixedWidth(100)
        self.livesLabel.move(50, 0)

        self.timesLabel = QtGui.QLabel('Time Left: ' + str(parent.level.timeLeft), self)
        self.timesLabel.setFixedWidth(200)
        self.timesLabel.move(200, 0)

        self.scoreLabel = QtGui.QLabel('Score: ' + str(parent.level.score), self)
        self.scoreLabel.setFixedWidth(200)
        self.scoreLabel.move(300, 0)

class Board(QtGui.QFrame):

    pauseGameSignal = QtCore.pyqtSignal()
    gameOverSignal = QtCore.pyqtSignal()

    resetTimerSignal = QtCore.pyqtSignal()

    updateScoreInDbSignal = QtCore.pyqtSignal(int)

    def __init__(self, level, parent=None):
        super(Board, self).__init__(parent)
        self.level = level # Initialize level attributes
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.initStatusBar()
        self.initBoard()

    def initStatusBar(self):

        self.statusBar = StatusBar(self)
        self.statusBar.setFixedWidth(468)
        self.statusBar.resize(100, 468)

    def initBoard(self):

        print "Username: " + str(self.level.username)
        print "Board level: " + str(self.level.levelNum)

        self.isPaused = True

        self.globalTimer = QtCore.QTimer(self)
        self.globalTimer.timeout.connect(lambda : self.bombLoop())

        self.fastTimer = QtCore.QTimer(self)
        self.fastTimer.timeout.connect(lambda : self.moveEnemy(constant.SPEED_FAST))
        self.normalTimer = QtCore.QTimer(self)
        self.normalTimer.timeout.connect(lambda : self.moveEnemy(constant.SPEED_NORMAL))
        self.slowTimer = QtCore.QTimer(self)
        self.slowTimer.timeout.connect(lambda : self.moveEnemy(constant.SPEED_SLOW))
        self.slowestTimer = QtCore.QTimer(self)
        self.slowestTimer.timeout.connect(lambda : self.moveEnemy(constant.SPEED_SLOWEST))

        self.coundownTimer = QtCore.QTimer(self)
        self.coundownTimer.timeout.connect(self.timeout_event)

        if not self.level.isInitialized:
            self.initLevel()

    def initLevel(self):

        self.level.isInitialized = True
        self.level.setNewLevel()

    def start(self):

        self.isPaused = False
        self.level.bomberman.canMove = True

        self.globalTimer.start(constant.TIME_GLOBAL)
        self.fastTimer.start(constant.TIME_FAST)
        self.normalTimer.start(constant.TIME_NORMAL)
        self.slowTimer.start(constant.TIME_SLOW)
        self.slowestTimer.start(constant.TIME_SLOWEST)
        self.coundownTimer.start(constant.TIME_COUNTDOWN)


    def pause(self):

        self.isPaused = True

        self.stopTimers()

        self.pauseGameSignal.emit()  # Send signal to show pauseMenu

        self.update()

    def death(self):

        if self.level.bomberman.invincible:
            return

        # Stop timers
        self.stopTimers()

        # Take off life
        self.level.bomberman.death()

        if(self.level.bomberman.lives == 0):
            gameoverMessage = '''Game Over!'''
            QtGui.QMessageBox.warning(self,'BOOM!', gameoverMessage, QtGui.QMessageBox.Ok)
            self.gameOverSignal.emit()  # Send signal for game over
            return

        self.statusBar.livesLabel.setText('Lives: ' + str(self.level.bomberman.lives))

        deathMessage = '''You lost a life!'''
        QtGui.QMessageBox.warning(self,'BOOM!',deathMessage,QtGui.QMessageBox.Ok)

        # IMPORTANT sleep a few millisecond to avoid level timer overlap
        QtCore.QTimer.singleShot(self.level.bomberman.speed, self.restartSameLevel)

    def tileAt(self, x, y):
        return self.level.board[y][x].peek()

    def setTileAt(self, x, y, tile):
        self.level.board[y][x].push(tile)
        self.update()

    def setTileAtWithoutUpdate(self, x, y, tile):
        self.level.board[y][x].push(tile)

    def popTileAt(self, x, y):
        self.level.board[y][x].pop()
        self.update()

    def popTileAtWithoutUpdate(self, x, y):
        self.level.board[y][x].pop()

    def squareWidth(self):
        return self.contentsRect().width() / constant.VIEW_WIDTH

    def squareHeight(self):
        return self.contentsRect().height() / constant.VIEW_HEIGHT

    def bombLoop(self):
        indexToDecrement = []
        detonate = False
        for i in xrange(len(self.level.bombQueue)):
            if (self.level.bombQueue[i][2] <= 0):
                detonate = True
            else:
                indexToDecrement.append(i)
        for i in xrange(len(indexToDecrement)):
            self.level.bombQueue[i] = (self.level.bombQueue[i][0],self.level.bombQueue[i][1],self.level.bombQueue[i][2] - constant.TIME_GLOBAL)

        # Loop flashQueue
        coordsToEndFlash = []
        numToEndFlash = 0
        for i in xrange(len(self.level.flashQueue)):
            if (self.level.flashQueue[i][2] <= 0):
                x,y,z = self.level.flashQueue[i]
                coordsToEndFlash.append((x,y))
                numToEndFlash += 1
            else:
                self.level.flashQueue[i][2] -= constant.TIME_GLOBAL
        for j in range(numToEndFlash):
            self.level.flashQueue.pop(0)
        for x,y in coordsToEndFlash:
            self.popTileAtWithoutUpdate(x,y)

        if (detonate):
            self.detonateBomb()

    def paintEvent(self, event):

        # Check for level X pos for moving viewPort
        if self.level.bomberman.curX <= 6:
            viewXFirst = 0
            viewXLast = 12
        elif self.level.bomberman.curX >= 24:
            viewXFirst = 18
            viewXLast = 30
        else:
            viewXFirst = self.level.bomberman.curX - 6
            viewXLast = self.level.bomberman.curX + 6

        painter = QtGui.QPainter(self)
        rect = self.contentsRect()

        boardTop = rect.bottom() - constant.VIEW_HEIGHT * self.squareHeight()

        for i in range(constant.BOARD_HEIGHT):
            for j in range(viewXFirst,viewXLast+1):
                shape = self.tileAt(j, constant.BOARD_HEIGHT - i - 1)

                if(shape == Tile.Exit):
                    self.drawImages(painter, 'Exit', rect.left() + (j-viewXFirst) * self.squareWidth(), boardTop + i * self.squareHeight())
                elif(shape == Tile.Brick):
                    self.drawImages(painter, 'Brick', rect.left() + (j-viewXFirst) * self.squareWidth(), boardTop + i * self.squareHeight())
                elif(shape == Tile.Balloom):
                    self.drawImages(painter, 'Balloom', rect.left() + (j-viewXFirst) * self.squareWidth(), boardTop + i * self.squareHeight())
                elif(shape == Tile.Bomb):
                    self.drawImages(painter, 'Bomb', rect.left() + (j-viewXFirst) * self.squareWidth(), boardTop + i * self.squareHeight())
                elif(shape == Tile.Concrete):
                    self.drawImages(painter, 'Concrete', rect.left() + (j-viewXFirst) * self.squareWidth(), boardTop + i * self.squareHeight())
                elif(shape == Tile.Oneal):
                    self.drawImages(painter, 'Oneal', rect.left() + (j-viewXFirst) * self.squareWidth(), boardTop + i * self.squareHeight())
                elif(shape == Tile.Doll):
                    self.drawImages(painter, 'Doll', rect.left() + (j-viewXFirst) * self.squareWidth(), boardTop + i * self.squareHeight())
                elif(shape == Tile.Minvo):
                    self.drawImages(painter, 'Minvo', rect.left() + (j-viewXFirst) * self.squareWidth(), boardTop + i * self.squareHeight())
                elif(shape == Tile.Kondoria):
                    self.drawImages(painter, 'Kondoria', rect.left() + (j-viewXFirst) * self.squareWidth(), boardTop + i * self.squareHeight())
                elif(shape == Tile.Ovapi):
                    self.drawImages(painter, 'Ovapi', rect.left() + (j-viewXFirst) * self.squareWidth(), boardTop + i * self.squareHeight())
                elif(shape == Tile.Pass):
                    self.drawImages(painter, 'Pass', rect.left() + (j-viewXFirst) * self.squareWidth(), boardTop + i * self.squareHeight())
                elif(shape == Tile.Pontan):
                    self.drawImages(painter, 'Pontan', rect.left() + (j-viewXFirst) * self.squareWidth(), boardTop + i * self.squareHeight())
                elif(shape == Tile.Bomberman):
                    self.drawImages(painter, 'Bomberman', rect.left() + (j-viewXFirst) * self.squareWidth(), boardTop + i * self.squareHeight())
                elif(shape == Tile.Powerup):
                    if (self.level.powerUp == 1):
                        self.drawImages(painter, 'Bombs', rect.left() + (j-viewXFirst) * self.squareWidth(), boardTop + i * self.squareHeight())
                    elif (self.level.powerUp == 2):
                        self.drawImages(painter, 'Flames', rect.left() + (j-viewXFirst) * self.squareWidth(), boardTop + i * self.squareHeight())
                    elif (self.level.powerUp == 3):
                        self.drawImages(painter, 'Speed', rect.left() + (j-viewXFirst) * self.squareWidth(), boardTop + i * self.squareHeight())
                    elif (self.level.powerUp == 4):
                        self.drawImages(painter, 'Wallpass', rect.left() + (j-viewXFirst) * self.squareWidth(), boardTop + i * self.squareHeight())
                    elif (self.level.powerUp == 5):
                        self.drawImages(painter, 'Detonator', rect.left() + (j-viewXFirst) * self.squareWidth(), boardTop + i * self.squareHeight())
                    elif (self.level.powerUp == 6):
                        self.drawImages(painter, 'Bombpass', rect.left() + (j-viewXFirst) * self.squareWidth(), boardTop + i * self.squareHeight())
                    elif (self.level.powerUp == 7):
                        self.drawImages(painter, 'Flamepass', rect.left() + (j-viewXFirst) * self.squareWidth(), boardTop + i * self.squareHeight())
                    elif (self.level.powerUp == 8):
                        self.drawImages(painter, 'Mystery', rect.left() + (j-viewXFirst) * self.squareWidth(), boardTop + i * self.squareHeight())
                else:
                    self.drawSquare(painter,
                                    rect.left() + (j-viewXFirst) * self.squareWidth(),
                                    boardTop + i * self.squareHeight(), shape)

    def drawImages(self, painter, shape, x, y):
        shapePix = QtGui.QPixmap('./res/images/' + shape + '.png')
        scaledShapePix = QtGui.QPixmap.scaled(shapePix,self.squareWidth() + 1,self.squareHeight() + 1,0)
        painter.drawPixmap( x, y, scaledShapePix)

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

        if self.isPaused:
            return

        if key == QtCore.Qt.Key_P:
            self.pause()
            return

        elif key == QtCore.Qt.Key_Left:
            if self.level.bomberman.curX == 0:
                return
            self.tryMove(self.level.bomberman.curX-1,self.level.bomberman.curY)

        elif key == QtCore.Qt.Key_Right:
            if self.level.bomberman.curX == constant.BOARD_WIDTH - 1:
                return
            self.tryMove(self.level.bomberman.curX+1,self.level.bomberman.curY)

        elif key == QtCore.Qt.Key_Down:
            if self.level.bomberman.curY == 0:
                return
            self.tryMove(self.level.bomberman.curX,self.level.bomberman.curY-1)

        elif key == QtCore.Qt.Key_Up:
            if self.level.bomberman.curY == constant.BOARD_HEIGHT-1:
                return
            self.tryMove(self.level.bomberman.curX,self.level.bomberman.curY+1)

        elif key == QtCore.Qt.Key_Space:
            if (len(self.level.bombQueue) < self.level.bomberman.numBombs):
                self.level.setBomb()

        elif key == QtCore.Qt.Key_Z:
            if (len(self.level.bombQueue) < self.level.bomberman.numBombs):
                self.level.setBomb()

        elif key == QtCore.Qt.Key_X:
            if (self.level.bomberman.hasDetonator and self.level.bombQueue is not None):
                self.detonateBomb()

        elif key == QtCore.Qt.Key_B:
            if (self.level.bomberman.hasDetonator and self.level.bombQueue is not None):
                self.detonateBomb()
        else:
            super(Board, self).keyPressEvent(event)

    def tryMove(self, newX, newY):
        if (self.isPaused):
            return False
        elif (not self.level.bomberman.canMove):
            return False
        elif (self.level.bomberman.wallPass and self.level.bomberman.bombPass):
            if (self.tileAt(newX,newY) == Tile.Concrete):
                return False
        elif (self.level.bomberman.wallPass):
            if (self.tileAt(newX,newY) == Tile.Concrete or self.tileAt(newX,newY) == Tile.Bomb):
                return False
        elif (self.level.bomberman.bombPass):
            if (self.tileAt(newX,newY) == Tile.Concrete or self.tileAt(newX,newY) == Tile.Brick):
                return False
        elif (self.tileAt(newX,newY) == Tile.Concrete or self.tileAt(newX,newY) == Tile.Brick or self.tileAt(newX,newY) == Tile.Bomb):
            return False
        elif Tile.isEnemy(self.tileAt(newX,newY)):
            self.death()
            return False

        # Pop level at current pos
        self.popTileAt(self.level.bomberman.curX,self.level.bomberman.curY)

        # Compute new position
        self.level.bomberman.curX = newX
        self.level.bomberman.curY = newY

        # Check if new pos is powerup
        if (self.tileAt(self.level.bomberman.curX,self.level.bomberman.curY) == Tile.Powerup):
            self.popTileAt(newX, newY)
            self.level.gainPowerUp()

        # Check if new pos is exit
        if ((self.tileAt(self.level.bomberman.curX,self.level.bomberman.curY) == Tile.Exit) and self.level.numberEnemies == 0):
            self.exit()
            return # IMPORTANT

        # Set level to new pos
        self.setTileAt(self.level.bomberman.curX,self.level.bomberman.curY,Tile.Bomberman)

        # Limit level move speed
        self.bombermanTriggerCanMove()
        self.globalTimer.singleShot(self.level.bomberman.speed, self.bombermanTriggerCanMove)

        return True

    def moveEnemy(self, speed):
        for i in range(self.level.numberEnemies):
            if (Enemy.getEnemy(self.level.listEnemies[i][3])['speed'] == speed):
                curX = self.level.listEnemies[i][0]
                curY = self.level.listEnemies[i][1]
                tempDir = self.level.listEnemies[i][2]
                tempWP = Enemy.getEnemy(self.level.listEnemies[i][3])['wallpass']
                tempIntel = Enemy.getEnemy(self.level.listEnemies[i][3])['intelligence']
                newX = 0
                newY = 0
                randInt = 0
                hasDied = False
                hasMoved = False

                if (tempIntel == 3): randInt = 2
                elif (tempIntel == 2): randInt = 10

                if (tempIntel == 2 or tempIntel == 3):
                    if (self.level.board[curY+1][curX].peek() == Tile.Bomberman and hasMoved == False):
                        newX = curX
                        newY = curY + 1
                        tempDir = 0
                        hasMoved = True
                        hasDied = True
                    if (self.level.board[curY-1][curX].peek() == Tile.Bomberman and hasMoved == False):
                        newX = curX
                        newY = curY - 1
                        tempDir = 2
                        hasMoved = True
                        hasDied = True
                    if (self.level.board[curY][curX+1].peek() == Tile.Bomberman and hasMoved == False):
                        newX = curX + 1
                        newY = curY
                        tempDir = 1
                        hasMoved = True
                        hasDied = True
                    if (self.level.board[curY][curX-1].peek() == Tile.Bomberman and hasMoved == False):
                        newX = curX - 1
                        newY = curY
                        tempDir = 3
                        hasMoved = True
                        hasDied = True

                    tempTile = self.level.board[curY+1][curX].peek()
                    if (tempTile != Tile.Bomb and ((tempTile == Tile.Brick and tempWP == True) or tempTile != Tile.Brick) and tempTile != Tile.Concrete and random.randint(1,randInt) == 1 and hasMoved == False):
                        newX = curX
                        newY = curY + 1
                        tempDir = 0
                        hasMoved = True

                    tempTile = self.level.board[curY-1][curX].peek()
                    if (tempTile != Tile.Bomb and ((tempTile == Tile.Brick and tempWP == True) or tempTile != Tile.Brick) and tempTile != Tile.Concrete and random.randint(1,randInt) == 1 and hasMoved == False):
                        newX = curX
                        newY = curY - 1
                        tempDir = 2
                        hasMoved = True

                    tempTile = self.level.board[curY][curX+1].peek()
                    if (tempTile != Tile.Bomb and ((tempTile == Tile.Brick and tempWP == True) or tempTile != Tile.Brick) and tempTile != Tile.Concrete and random.randint(1,randInt) == 1 and hasMoved == False):
                        newX = curX + 1
                        newY = curY
                        tempDir = 1
                        hasMoved = True

                    tempTile = self.level.board[curY][curX-1].peek()
                    if (tempTile != Tile.Bomb and ((tempTile == Tile.Brick and tempWP == True) or tempTile != Tile.Brick) and tempTile != Tile.Concrete and random.randint(1,randInt) == 1 and hasMoved == False):
                        newX = curX - 1
                        newY = curY
                        tempDir = 3
                        hasMoved = True

                    if (hasMoved == True):
                        self.level.listEnemies[i][0] = newX
                        self.level.listEnemies[i][1] = newY
                        self.level.listEnemies[i][2] = tempDir
                        self.popTileAt(curX, curY)
                        self.setTileAt(newX, newY, self.level.listEnemies[i][3])
                        if (hasDied == True):
                            self.death()
                            return False

                if (tempIntel == 1 or hasMoved == False):
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

                    tempTile = self.level.board[newY][newX].peek()

                    if (tempTile == Tile.Bomb or (tempTile == Tile.Brick and tempWP == False) or tempTile == Tile.Concrete):
                        if (tempDir == 0): newY -= 2
                        elif (tempDir == 1): newX -= 2
                        elif (tempDir == 2): newY += 2
                        elif (tempDir == 3): newX += 2
                        self.level.listEnemies[i][2] = (self.level.listEnemies[i][2] + 2) % 4

                        # tempTile = self.level.board[newY][newX].peek()
                        #
                        # if (tempTile == Tile.Bomb or tempTile == Tile.Brick or tempTile == Tile.Concrete):
                        #     self.level.listEnemies[i][2] = (self.level.listEnemies[i][2] + 1) % 4

                    tempTile = self.level.board[newY][newX].peek()

                    if ((tempTile == Tile.Brick and tempWP == True) or (tempTile != Tile.Bomb and tempTile != Tile.Brick and tempTile != Tile.Concrete)):
                        self.level.listEnemies[i][0] = newX
                        self.level.listEnemies[i][1] = newY
                        self.popTileAt(curX, curY)
                        self.setTileAt(newX, newY, self.level.listEnemies[i][3])
                        if (tempTile == Tile.Bomberman):
                            self.death()
                            return False

    def bombermanTriggerCanMove(self):
        self.level.bomberman.canMove = not self.level.bomberman.canMove
            
    def killEnemy(self, x, y):
        for i in range (self.level.numberEnemies):
            if (x == self.level.listEnemies[i][0] and y ==  self.level.listEnemies[i][1]):
                self.popTileAt(x, y)
                del self.level.listEnemies[i]
                self.level.numberEnemies -= 1
                self.level.listTypeEnemies[i] -= 1
                break

    def detonateBomb(self):
        x, y, z = self.level.bombQueue.pop(0)
        if (self.tileAt(x,y) == Tile.Bomberman):
            self.popTileAt(x,y)
            self.popTileAt(x,y)
            self.setTileAt(x,y,Tile.Bomberman)
        else:
            self.popTileAt(x,y)

        flashList = []
        popList = []
        killedEnemies = [[] for i in range(self.level.bomberman.rangeOfBombs)]

        # NORTH
        for i in range(1,self.level.bomberman.rangeOfBombs+1):
            modY = y + i
            if (modY < constant.BOARD_HEIGHT-1):
                northTile = self.tileAt(x,modY)
                if (northTile == Tile.Concrete or northTile == Tile.Bomb):
                    break
                if (Tile.isEmpty(northTile)):
                    flashList.append((x,modY))
                if (northTile == Tile.Brick):
                    popList.append((x,modY))
                    break
                if (Tile.isEnemy(northTile)):
                    killedEnemies[i-1].append(northTile)
                    self.killEnemy(x, modY)
                if (Tile.isBomberman(northTile) and not self.level.bomberman.invincible):
                    self.death()
                    break
                if (Tile.isPowerup(northTile) or Tile.isExit(northTile)):
                    self.level.setChaos()
                    break

        # SOUTH
        for i in range(1,self.level.bomberman.rangeOfBombs+1):
            modY = y - i
            if (modY < constant.BOARD_HEIGHT-1):
                southTile = self.tileAt(x,modY)
                if (southTile == Tile.Concrete or southTile == Tile.Bomb):
                    break
                if (Tile.isEmpty(southTile)):
                    flashList.append((x,modY))
                if (southTile == Tile.Brick):
                    popList.append((x,modY))
                    break
                if (Tile.isEnemy(southTile)):
                    killedEnemies[i-1].append(southTile)
                    self.killEnemy(x, modY)
                if (Tile.isBomberman(southTile) and not self.level.bomberman.invincible):
                    self.death()
                    break
                if (Tile.isPowerup(southTile) or Tile.isExit(southTile)):
                    self.level.setChaos()
                    break

        # EAST
        for i in range(1,self.level.bomberman.rangeOfBombs+1):
            modX = x + i
            if (modX < constant.BOARD_WIDTH-1):
                eastTile = self.tileAt(modX,y)
                if (eastTile == Tile.Concrete or eastTile == Tile.Bomb):
                    break
                if (Tile.isEmpty(eastTile)):
                    flashList.append((modX,y))
                if (eastTile == Tile.Brick):
                    popList.append((modX,y))
                    break
                if (Tile.isEnemy(eastTile)):
                    killedEnemies[i-1].append(eastTile)
                    self.killEnemy(modX, y)
                if (Tile.isBomberman(eastTile) and not self.level.bomberman.invincible):
                    self.death()
                    break
                if (Tile.isPowerup(eastTile) or Tile.isExit(eastTile)):
                    self.level.setChaos()
                    break

        # WEST
        for i in range(1,self.level.bomberman.rangeOfBombs+1):
            modX = x - i
            if (modX < constant.BOARD_WIDTH-1):
                westTile = self.tileAt(modX,y)
                if (westTile == Tile.Concrete or westTile == Tile.Bomb):
                    break
                if (Tile.isEmpty(westTile)):
                    flashList.append((modX,y))
                if (westTile == Tile.Brick):
                    popList.append((modX,y))
                    break
                if (Tile.isEnemy(westTile)):
                    killedEnemies[i-1].append(westTile)
                    self.killEnemy(modX, y)
                if (Tile.isBomberman(westTile) and not self.level.bomberman.invincible):
                    self.death()
                if (Tile.isPowerup(westTile) or Tile.isExit(westTile)):
                    self.level.setChaos()
                    break

        self.startFlash(flashList)
        # self.endFlash(flashList)
        self.destroyTiles(popList)
        self.updateScore(killedEnemies)

    def startFlash(self, flashList):
        for x,y in flashList:
            self.setTileAt(x,y,Tile.Flash)
            self.level.flashQueue.append([x,y,constant.TIME_FLASH])

    def endFlash(self, flashList):
        for x,y in flashList:
            self.popTileAtWithoutUpdate(x,y)

    def destroyTiles(self,popList):
        for x,y in popList:
            self.popTileAt(x,y)

    def exit(self):
        if self.level.levelNum == 16:
            winningMessage = '''Congratulations!!! You won the game!!!'''

            return

        # Stop the game
        self.stopTimers()

        # IMPORTANT sleep a few millisecond to avoid level timer overlap
        QtCore.QTimer.singleShot(self.level.bomberman.speed, self.restartNextLevel)

    def stopTimers(self):
        self.isPaused = True
        self.globalTimer.stop()
        self.fastTimer.stop()
        self.normalTimer.stop()
        self.slowTimer.stop()
        self.slowestTimer.stop()
        self.coundownTimer.stop()

    def restartNextLevel(self):
        # Increment level
        self.level.levelNum += 1
        self.initBoard()
        self.initLevel()
        self.start()

    def restartSameLevel(self):
        self.initBoard()
        self.initLevel()
        self.start()       

    # update score in status bar
    def updateScore(self, killedEnemies):
        incrementalScore = self.getScoreOfKilledEnemies(killedEnemies)
        self.updateScoreInDbSignal.emit(incrementalScore)
        newScore = self.level.score + incrementalScore
        self.level.score = newScore
        self.statusBar.scoreLabel.setText('Score: ' + str(newScore))

    ## Method to calculate the score the user gets when a bomb detonates
    # @param killedEnemies
    # Assume the list "killedEnemies" has the following format:
    # [[enemies at distance = 1 from bomb], [enemies at distance = 2 from bomb], ... , [enemies at distance = range from bomb]]
    # e.g.: [[Tile.Balloom, Tile.Oneal], [], [Tile.Doll]] means when the bomb exploded, there was a Balloom and an Oneal at distance 1,
    # nothing at distance 2, and a Doll at distance 3 from the bomb.
    def getScoreOfKilledEnemies(self, killedEnemies):
        score = 0
        multiplier = 1

        for dist in range(len(killedEnemies)):
            list = killedEnemies[dist]
            sortedList = sorted(list)
            for enemy in sortedList:
                score += Enemy.getEnemy(enemy)['points'] * multiplier
                multiplier *= 2

        return score

    def saveBomberman(self):
        return self.level

    def timeout_event(self):
        if (self.level.timeLeft == 0 and self.level.timeDone == False):
            self.level.timeDone = True
            self.level.setSuperChaos()
        elif (self.level.timeDone == True):
            pass
        else:
            self.level.timeLeft -= 1
            self.statusBar.timesLabel.setText('Time Left: ' + str(self.level.timeLeft))
