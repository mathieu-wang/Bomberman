from PyQt4 import QtCore, QtGui

class PauseMenu(QtGui.QWidget):

    resumeGameSignal = QtCore.pyqtSignal()
    quitGameSignal = QtCore.pyqtSignal()
    showLeaderboardSignal = QtCore.pyqtSignal()
    saveGameSignal = QtCore.pyqtSignal()
    loadGameSignal = QtCore.pyqtSignal()
    backToMainMenuSignal = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(PauseMenu, self).__init__(parent)
        self.initUI()

    def initUI(self):
        buttonWidth = 150
        buttonStartXCoordinate = 159

        resumeButton = QtGui.QPushButton('Resume Game', self)
        resumeButton.setFixedWidth(buttonWidth)
        resumeButton.move(buttonStartXCoordinate, 94)
        resumeButton.clicked.connect(self.resume)

        quitButton = QtGui.QPushButton('Quit Game', self)
        quitButton.setFixedWidth(buttonWidth)
        quitButton.move(buttonStartXCoordinate, 294)
        quitButton.clicked.connect(self.quit)

        backButton = QtGui.QPushButton('Back to Main Menu', self)
        backButton.setFixedWidth(buttonWidth)
        backButton.move(buttonStartXCoordinate, 254)
        backButton.clicked.connect(self.back)

        saveButton = QtGui.QPushButton('Save Game', self)
        saveButton.setFixedWidth(buttonWidth)
        saveButton.move(buttonStartXCoordinate, 134)
        saveButton.clicked.connect(self.save)

        loadButton = QtGui.QPushButton('Load Game', self)
        loadButton.setFixedWidth(buttonWidth)
        loadButton.move(buttonStartXCoordinate, 174)
        loadButton.clicked.connect(self.load)

        showLeaderboardButton = QtGui.QPushButton('Leaderboard', self)
        showLeaderboardButton.setFixedWidth(buttonWidth)
        showLeaderboardButton.move(buttonStartXCoordinate, 214)
        showLeaderboardButton.clicked.connect(self.showLeaderboard)

        #self.setFixedHeight(300)
        #self.setFixedWidth(300)

        self.show()

    def resume(self):
        self.resumeGameSignal.emit()

    def quit(self):
        self.quitGameSignal.emit()

    def showLeaderboard(self):
        self.showLeaderboardSignal.emit()

    def back(self):
        self.backToMainMenuSignal.emit()

    def save(self):
        self.saveGameSignal.emit()

    def load(self):
        self.loadGameSignal.emit()