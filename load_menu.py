from PyQt4 import QtCore, QtGui

from database import Database

class LoadMenu(QtGui.QWidget):

    returnToPauseMenuSignal = QtCore.pyqtSignal()
    loadSavedGameSignal = QtCore.pyqtSignal(str)

    gamename = 'best'

    def __init__(self, username, parent=None):
        super(LoadMenu, self).__init__(parent)

        self.username = username

        self.initUI()

    def initUI(self):

        buttonWidth = 150
        buttonStartXCoordinate = 159

        loadButton = QtGui.QPushButton('Load', self)
        loadButton.setFixedWidth(buttonWidth)
        loadButton.move(buttonStartXCoordinate, 174)
        loadButton.clicked.connect(self.loadGame)

        returnButton = QtGui.QPushButton('Back', self)
        returnButton.setFixedWidth(buttonWidth)
        returnButton.move(buttonStartXCoordinate, 214)
        returnButton.clicked.connect(self.returnToPauseMenu)

        self.setFixedHeight(468)
        self.setFixedWidth(468)

        self.show()

    def loadGame(self):
    	self.loadSavedGameSignal.emit(self.gamename)

    def loadGameList(self):
        db = Database()
        return db.loadListSavedGames(self.username)

    def returnToPauseMenu(self):
        self.returnToPauseMenuSignal.emit()