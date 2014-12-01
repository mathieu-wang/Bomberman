from PyQt4 import QtCore, QtGui
import constant

class MainMenu(QtGui.QWidget):

    playGameSignal = QtCore.pyqtSignal()
    logoutGameSignal = QtCore.pyqtSignal()
    quitGameSignal = QtCore.pyqtSignal()
    showLeaderboardSignal = QtCore.pyqtSignal(int)
    showSettingsSignal = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(MainMenu, self).__init__(parent)
        self.initUI()

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

        settingsButton = QtGui.QPushButton('Load Game', self)
        settingsButton.setFixedWidth(buttonWidth)
        settingsButton.move(buttonStartXCoordinate, 179)
        settingsButton.clicked.connect(self.settings)

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
        self.showLeaderboardSignal.emit(constant.MAIN_MENU)

    def settings(self):
        self.showSettingsSignal.emit()