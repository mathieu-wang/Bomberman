from PyQt4 import QtCore, QtGui

import constant

## This class is a widget that displays the Main menu. It includes the following buttons
# that the user can interact with:\n
# playButton: emit playGameSignal when clicked.\n
# logoutButton: emit logoutGameSignal when clicked.\n
# loadButton: emit loadMenuSignal when clicked.\n
# quitButton: emit quitGameSignal when clicked.\n
# showLeaderboardButton: emit showLeaderboardSignal when clicked.
#
class MainMenu(QtGui.QWidget):

    ##Signal which will be used to launch the game.
    playGameSignal = QtCore.pyqtSignal()
    ##Signal which will be used to exit the current user and send it back to login menu.
    logoutGameSignal = QtCore.pyqtSignal()
    ##Signal which will be used to quit the whole application.
    quitGameSignal = QtCore.pyqtSignal()
    ##Signal which will be used to to launch the leaderboard. Also emit the int 'previousMenu'
    # to keep track of the menu it was called from.
    showLeaderboardSignal = QtCore.pyqtSignal(int)
    ##Signal which will launch the load menu. Also emit the int 'previousMenu'
    #to keep track of the menu it was called from.
    loadMenuSignal = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super(MainMenu, self).__init__(parent)
        self.initUI()

    ##This method initialize the GUI of Main menu.
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

    ##emit playGameSignal when called.
    def play(self):
        self.playGameSignal.emit()
    ##emit logoutGameSignal when called.
    def logout(self):
        self.logoutGameSignal.emit()
    ##emit quitGameSignal when called.
    def quit(self):
        self.quitGameSignal.emit()
    ##emit showLeaderboardSignal when called.
    def showLeaderboard(self):
        self.showLeaderboardSignal.emit(constant.MAIN_MENU)
    ##emit loadMenuSignal when called.
    def load(self):
        self.loadMenuSignal.emit(constant.MAIN_MENU)
