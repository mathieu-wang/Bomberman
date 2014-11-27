from PyQt4 import QtCore, QtGui
import global_constants

class PauseMenu(QtGui.QWidget):

    resumeGameSignal = QtCore.pyqtSignal()
    quitGameSignal = QtCore.pyqtSignal()
    showLeaderboardSignal = QtCore.pyqtSignal(int)
    saveMenuSignal = QtCore.pyqtSignal()
    loadMenuSignal = QtCore.pyqtSignal()
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

        backButton = QtGui.QPushButton('Back to Main Menu', self)
        backButton.setFixedWidth(buttonWidth)
        backButton.move(buttonStartXCoordinate, 254)
        backButton.clicked.connect(self.back)

        quitButton = QtGui.QPushButton('Quit Game', self)
        quitButton.setFixedWidth(buttonWidth)
        quitButton.move(buttonStartXCoordinate, 294)
        quitButton.clicked.connect(self.quit)

        self.setFixedHeight(468)
        self.setFixedWidth(468)

        self.show()

    def resume(self):
        self.resumeGameSignal.emit()

    def quit(self):
        self.quitGameSignal.emit()

    def showLeaderboard(self):
        self.showLeaderboardSignal.emit(global_constants.PAUSE_MENU)

    def back(self):
        self.backToMainMenuSignal.emit()

    def save(self):
        self.saveMenuSignal.emit()

    def load(self):
        self.loadMenuSignal.emit()