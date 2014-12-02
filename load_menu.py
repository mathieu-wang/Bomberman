from PyQt4 import QtCore, QtGui

from database import Database

##This class is a widget that displays the Load menu. It includes the following buttons
#and fields that the user can interact with:\n
#loadButton: emit loadSavedGameSignal when clicked.\n
#returnButton: emit backSignal when clicked.\n
#savedGameList: list of all the saved game of the current active user.
class LoadMenu(QtGui.QWidget):

    ##Signal which will be used to load the game the user chose.
    #@Param str the name of the game to load.
    loadSavedGameSignal = QtCore.pyqtSignal(str)
    ##Signal which will be used to go back to the previous menu based on an int.
    #@Param int set as 'previousMenu'.
    backSignal = QtCore.pyqtSignal(int)

    def __init__(self, parent, username, previousMenu):
        super(LoadMenu, self).__init__(parent)
        ##int used to keep track of the previous menu
        self.previousMenu = previousMenu
        ##username of the current active user
        self.username = username

        self.initUI()

    ##This method initialize the GUI of the Load menu.
    def initUI(self):

        buttonWidth = 150
        buttonStartXCoordinate = 159

        gameListWidth = 368
        gameListStartXCoordinate = 50

        savedGameList = self.loadSavedGameList()

        ##widget which displays a list from top to bottom.
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

    ##emit loadSavedGameSignal when called.
    def loadSavedGame(self):
        self.loadSavedGameSignal.emit(str(self.gameList.currentItem().text()))
    ##fetch from the database the current user's saved game.
    def loadSavedGameList(self):
        db = Database()
        return db.loadListSavedGames(self.username)
    ##emit backSignal when called.
    def back(self):
        self.backSignal.emit(self.previousMenu)