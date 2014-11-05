#!/usr/bin/python
# -*- coding: utf-8 -*-



import sys
from PyQt4 import QtCore, QtGui
from board import Board

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


def main():

    app = QtGui.QApplication([])
    game = Game()    
    sys.exit(app.exec_())

if __name__ == '__main__':

    main()
