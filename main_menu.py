from PyQt4 import QtCore, QtGui

class MainMenu(QtGui.QWidget):

    playGameSignal = QtCore.pyqtSignal()
    logoutGameSignal = QtCore.pyqtSignal()
    quitGameSignal = QtCore.pyqtSignal()
    showLeaderboardSignal = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(MainMenu, self).__init__(parent)
        self.initUI()

    def initUI(self):
        buttonWidth = 150
        buttonStartXCoordinate = 75

        playButton = QtGui.QPushButton('Play Bomberman', self)
        playButton.setFixedWidth(buttonWidth)
        playButton.move(buttonStartXCoordinate, 30)
        playButton.clicked.connect(self.play)

        logoutButton = QtGui.QPushButton('Logout', self)
        logoutButton.setFixedWidth(buttonWidth)
        logoutButton.move(buttonStartXCoordinate, 70)
        logoutButton.clicked.connect(self.logout)

        quitButton = QtGui.QPushButton('Quit', self)
        quitButton.setFixedWidth(buttonWidth)
        quitButton.move(buttonStartXCoordinate, 110)
        quitButton.clicked.connect(self.quit)

        showLeaderboardButton = QtGui.QPushButton('Leaderboard', self)
        showLeaderboardButton.setFixedWidth(buttonWidth)
        showLeaderboardButton.move(buttonStartXCoordinate, 150)
        showLeaderboardButton.clicked.connect(self.showLeaderboard)

        self.setFixedHeight(300)
        self.setFixedWidth(300)

        self.show()

    def play(self):
        self.playGameSignal.emit()

    def logout(self):
        self.logoutGameSignal.emit()

    def quit(self):
        self.quitGameSignal.emit()

    def showLeaderboard(self):
        self.showLeaderboardSignal.emit()