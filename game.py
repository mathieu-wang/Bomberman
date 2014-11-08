#!/usr/bin/python
# -*- coding: utf-8 -*-



import sys
from PyQt4 import QtCore, QtGui
from board import Board
from login_menu import LoginMenu

class Game(QtGui.QMainWindow):
    
    def __init__(self):
        super(Game, self).__init__()
        self.initUI()
        
    def initUI(self):    

        self.central_widget = QtGui.QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.show_login_menu()

    def show_login_menu(self):

        login_widget = LoginMenu(self)

        login_widget.button.clicked.connect(self.show_board)
        self.central_widget.addWidget(login_widget)
        self.setWindowTitle('Login')
        self.center()

    def show_board(self):

        self.board_widget = Board(self)

        self.central_widget.addWidget(self.board_widget)
        self.central_widget.setCurrentWidget(self.board_widget)

        self.board_widget.start()
        self.resize(1116,468) # Standard res
        self.setWindowTitle('Bomberman')
        self.center()     
        
    def center(self):

        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, 
            (screen.height()-size.height())/2)

def main():

    app = QtGui.QApplication([])
    game = Game()
    game.show()   
    sys.exit(app.exec_())

if __name__ == '__main__':

    main()