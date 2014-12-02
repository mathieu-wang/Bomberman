from functools import partial

from PyQt4 import QtCore, QtGui

from src.database import Database

##this class is a widget that displays the level menu. It includes buttons 
#that the user can interact with.
class LevelMenu(QtGui.QWidget):

    ##Signal which will be used to go back to the main menu.
    backToMainMenuSignal = QtCore.pyqtSignal()
    ##Signal which will be used to start the game.
    #@Param int is the number representing the level chosen by the user.
    startLevelSignal = QtCore.pyqtSignal(int)

    def __init__(self, parent, username):
        super(LevelMenu, self).__init__(parent)
        print "Initializing level menu for user: " + str(username)
        ##the currently active user's username.
        self.username = username
        ##instance of the database.
        self.db = Database()
        self.initUI()

    ##this method initialize the GUI of the level menu.
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

    ##emit backToMainMenuSignal when called.
    def backToMainMenu(self):
        self.backToMainMenuSignal.emit()
    ##emit startLevelSignal when called.
    def startLevel(self, level):
        self.startLevelSignal.emit(level)
