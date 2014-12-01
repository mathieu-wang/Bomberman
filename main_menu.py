from PyQt4 import QtCore, QtGui

import global_constants

## This class is a widget that displays the Main menu.\n It includes buttons
# that the user can interact with.
#
class MainMenu(QtGui.QWidget):

    playGameSignal = QtCore.pyqtSignal()
    logoutGameSignal = QtCore.pyqtSignal()
    quitGameSignal = QtCore.pyqtSignal()
    showLeaderboardSignal = QtCore.pyqtSignal(int)
    loadMenuSignal = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(MainMenu, self).__init__(parent)
        self.initUI()

    ## This method initialize the GUI of Main menu.
    # Play Bomberman button: emit playGameSignal when clicked which will be used to launch
    #       the game in game.py
    # Logout button: emit logoutGameSignal when clicked which will be used to exit the current
    #       user and send it back to the login menu
    #Load Game button: emit 
    #
    def initUI(self):
        buttonWidth = 150
        buttonStartXCoordinate = 159

        playButton = QtGui.QPushButton('Play Bomberman', self)
        playButton.setFixedWidth(buttonWidth)
        playButton.move(buttonStartXCoordinate, 139)
        playButton.clicked.connect(self.play)

        logoutButton = QtGui.QPushButton('Logout', self)
        logoutButton.setFixedWidth(buttonWidth)
        logoutButton.move(buttonStartXCoordinate, 259)
        logoutButton.clicked.connect(self.logout)

        loadButton = QtGui.QPushButton('Load Game', self)
        loadButton.setFixedWidth(buttonWidth)
        loadButton.move(buttonStartXCoordinate, 179)
        loadButton.clicked.connect(self.load)

        quitButton = QtGui.QPushButton('Quit', self)
        quitButton.setFixedWidth(buttonWidth)
        quitButton.move(buttonStartXCoordinate, 299)
        quitButton.clicked.connect(self.quit)

        showLeaderboardButton = QtGui.QPushButton('Leaderboard', self)
        showLeaderboardButton.setFixedWidth(buttonWidth)
        showLeaderboardButton.move(buttonStartXCoordinate, 219)
        showLeaderboardButton.clicked.connect(self.showLeaderboard)

        self.setFixedHeight(468)
        self.setFixedWidth(468)

        self.show()

    def play(self):
        self.playGameSignal.emit()

    def logout(self):
        self.logoutGameSignal.emit()

    def quit(self):
        self.quitGameSignal.emit()

    def showLeaderboard(self):
        self.showLeaderboardSignal.emit(global_constants.MAIN_MENU)

    def load(self):
        self.loadMenuSignal.emit()