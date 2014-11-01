#!/usr/bin/python
# -*- coding: utf-8 -*-



import sys
from PyQt4 import QtCore, QtGui

#This is a comment!

class Game(QtGui.QMainWindow):
    
    def __init__(self):
        super(Game, self).__init__()
        
        self.initUI()
        
        
    def initUI(self):    

        self.board = Board(self)
        self.setCentralWidget(self.board)
        
        self.board.start()
        
        self.resize(1116,468) # Standard res
        self.center()
        self.setWindowTitle('Bomberman')        
        self.show()
        

    def center(self):

        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, 
            (screen.height()-size.height())/2)

class Board(QtGui.QFrame):

    msg2Statusbar = QtCore.pyqtSignal(str)

    BoardWidth = 31
    BoardHeight = 13
    Speed = 300

    def __init__(self, parent):
        super(Board, self).__init__(parent)
        self.initBoard()
        
    def initBoard(self):     

        self.timer = QtCore.QBasicTimer()

        self.curX = 0
        self.curY = 0
        self.board = []

        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.isStarted = False
        self.isPaused = False

    def start(self):
        
        if self.isPaused:
            return

        self.isStarted = True
        self.clearBoard()
        self.setConcrete()
        self.initializeBomberman()

        self.timer.start(Board.Speed, self)

    def tileAt(self, x, y):
        return self.board[y][x].peek()

    def setTileAt(self, x, y, tile):
        self.board[y][x].push(tile)
        
    def squareWidth(self):
        return self.contentsRect().width() / Board.BoardWidth
        
    def squareHeight(self):
        return self.contentsRect().height() / Board.BoardHeight

    def clearBoard(self):
        self.board = [[Tile() for x in range(Board.BoardWidth)] for y in range(Board.BoardHeight)]

    def setConcrete(self):
        for y in range(Board.BoardHeight):
            for x in range(Board.BoardWidth):
                if x % 2 != 0 and y % 2 != 0:
                    self.setTileAt(x,y,Tile.Concrete)

    def initializeBomberman(self):

        self.setTileAt(self.curX,self.curY,Tile.Bomberman)

    def paintEvent(self, event):
        
        painter = QtGui.QPainter(self)
        rect = self.contentsRect()

        boardTop = rect.bottom() - Board.BoardHeight * self.squareHeight()

        for i in range(Board.BoardHeight):
            for j in range(Board.BoardWidth):
                shape = self.tileAt(j, Board.BoardHeight - i - 1)
                
                self.drawSquare(painter,
                    rect.left() + j * self.squareWidth(),
                    boardTop + i * self.squareHeight(), shape)

    def drawSquare(self, painter, x, y, shape):
        
        colorTable = [0x99CC33, 0x999999, 0x996633, 0xCC0000,
                      0xFFCC00, 0xCC66CC, 0x66CCCC, 0xDAAA00]

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

        elif key == QtCore.Qt.Key_B:
            self.setBomb()
            
        else:
            super(Board, self).keyPressEvent(event)

    def tryMove(self, newX, newY):
        if (self.tileAt(newX,newY) == Tile.Concrete or self.tileAt(newX,newY) == Tile.Brick or self.tileAt(newX,newY) == Tile.Bomb):
            return False
        if (self.tileAt(self.curX,self.curY) != Tile.Bomb):
            self.setTileAt(self.curX,self.curY,Tile.Empty)
        self.curX = newX
        self.curY = newY
        self.setTileAt(self.curX,self.curY,Tile.Bomberman)
        self.update()
        
        return True

    def setBomb(self):
        self.setTileAt(self.curX,self.curY,Tile.Bomb)
        self.update()

class Tile(object):

    Empty = 0
    Concrete = 1
    Brick = 2
    Bomb = 3
    Bomberman = 4
    Powerup = 5
    Exit = 6

    def __init__(self):
        self.stack = [Tile.Empty]

    def isEmpty(self):
        return self.stack == [Tile.Empty]

    def push(self, tile):
        self.stack.append(tile)

    def peek(self):
        return self.stack[len(self.stack)-1]

    def pop(self):
        return self.stack.pop()

    def size(self):
        return len(self.stack)

def main():

    app = QtGui.QApplication([])
    game = Game()    
    sys.exit(app.exec_())

if __name__ == '__main__':

    main()
