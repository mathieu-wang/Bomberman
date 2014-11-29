from PyQt4 import QtCore, QtGui

from database import Database

class LoadMenu(QtGui.QWidget):

    returnToPauseMenuSignal = QtCore.pyqtSignal()
    loadSavedGameSignal = QtCore.pyqtSignal(str)
    backSignal = QtCore.pyqtSignal(int)

    def __init__(self, username, parent=None):
        super(LoadMenu, self).__init__(parent)

        self.username = username

        self.initUI()

    def initUI(self):

        buttonWidth = 150
        buttonStartXCoordinate = 159

        gameListWidth = 368
        gameListStartXCoordinate = 50

        savedGameList = self.loadSavedGameList()

        self.gameList = QtGui.QListWidget(self)

        for savedGame in savedGameList:
            self.gameList.addItem(savedGame)

        self.gameList.setFixedWidth(gameListWidth)
        self.gameList.move(gameListStartXCoordinate, 94)

        loadButton = QtGui.QPushButton('Load', self)
        loadButton.setFixedWidth(buttonWidth)
        loadButton.move(buttonStartXCoordinate, 314)
        loadButton.clicked.connect(self.loadSavedGame)

        returnButton = QtGui.QPushButton('Back', self)
        returnButton.setFixedWidth(buttonWidth)
        returnButton.move(buttonStartXCoordinate, 354)
        returnButton.clicked.connect(self.back)

        self.setFixedHeight(468)
        self.setFixedWidth(468)

        self.show()

    def loadSavedGame(self):
        self.loadSavedGameSignal.emit(str(self.gameList.currentItem().text()))

    def loadSavedGameList(self):
        db = Database()
        return db.loadListSavedGames(self.username)

    def back(self):
        self.backSignal.emit(self.previousMenu)