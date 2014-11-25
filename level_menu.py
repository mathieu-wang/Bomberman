from PyQt4 import QtCore, QtGui

from database import Database

class LevelMenu(QtGui.QWidget):

    backToMainMenuSignal = QtCore.pyqtSignal()
    startLevelSignal = QtCore.pyqtSignal(int)

    def __init__(self, parent, username):
        super(LevelMenu, self).__init__(parent)
        print "initializing level menu for user: " + str(username)
        self.username = username
        self.db = Database()
        self.initUI()

    def initUI(self):
        grid = QtGui.QGridLayout()
        self.setLayout(grid)

        maxLevel = self.db.getHighestUnlockedLevel(self.username)
        print "Max level reached by user: " + str(self.username)

        # Add enabled buttons
        for i in range(0, maxLevel):
            levelButton = QtGui.QPushButton(str(i+1), self)
            levelButton.clicked.connect(lambda j=i: self.startLevel(j+1))
            grid.addWidget(levelButton)
            print "level: " + str(i+1)

        for i in range(maxLevel, 50):
            levelButton = QtGui.QPushButton(str(i+1), self)
            levelButton.setEnabled(False)
            grid.addWidget(levelButton)
            print "level: " + str(i+1)

        backButton = QtGui.QPushButton('Back To Main Menu', self)
        backButton.setFixedWidth(200)
        backButton.clicked.connect(self.backToMainMenu)
        grid.addWidget(backButton)

    def backToMainMenu(self):
        self.backToMainMenuSignal.emit()

    def startLevel(self, level):
        self.startLevelSignal.emit(level)