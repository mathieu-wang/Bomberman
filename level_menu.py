from PyQt4 import QtCore, QtGui

from database import Database
from functools import partial

class LevelMenu(QtGui.QWidget):

    backToMainMenuSignal = QtCore.pyqtSignal()
    startLevelSignal = QtCore.pyqtSignal(int)

    def __init__(self, parent, username):
        super(LevelMenu, self).__init__(parent)
        print "Initializing level menu for user: " + str(username)
        self.username = username
        self.db = Database()
        self.initUI()

    def initUI(self):
        grid = QtGui.QGridLayout()
        self.setLayout(grid)

        maxLevel = self.db.getHighestUnlockedLevel(self.username)
        print "Max level reached by user: " + str(maxLevel)

        # Add enabled buttons
        for i in range(0, maxLevel):
            level = i+1
            levelButton = QtGui.QPushButton(str(level), self)
            levelButton.setFixedWidth(50)
            levelButton.clicked.connect(partial(self.startLevel, level))
            grid.addWidget(levelButton)

        backButton = QtGui.QPushButton('Back To Main Menu', self)
        backButton.setFixedWidth(200)
        backButton.clicked.connect(self.backToMainMenu)
        grid.addWidget(backButton)

    def backToMainMenu(self):
        self.backToMainMenuSignal.emit()

    def startLevel(self, level):
        self.startLevelSignal.emit(level)
