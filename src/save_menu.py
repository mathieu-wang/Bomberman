import datetime

from PyQt4 import QtCore, QtGui

from src.database import Database

##this class is a widget that displays the save menu. It includes the following buttons
#and fields that the user can interact with:\n
#saveButton: calls saveGame() when clicked.\n
#returnButton: emit returnToPauseMenuSignal when clicked.
class SaveMenu(QtGui.QWidget):

    ##Signal which will be used to return to the pause menu.
    returnToPauseMenuSignal = QtCore.pyqtSignal()

    def __init__(self, username, board, parent=None):
        super(SaveMenu, self).__init__(parent)
        ##is a copy of the current board to be saved.
        self.board = board
        ##is the currently active user's username.
        self.username = username
        self.initUI()

    ##this method initialize the GUI of the save menu.
    def initUI(self):

        buttonWidth = 150
        buttonStartXCoordinate = 159

        ##is a QLabel that displays 'Game name'.
        self.saveLabel = QtGui.QLabel('Game name', self)
        self.saveLabel.setAlignment(QtCore.Qt.AlignHCenter)
        self.saveLabel.setFixedWidth(buttonWidth)
        self.saveLabel.move(buttonStartXCoordinate, 94)
        ##is a QLineEdit that let the user enter the name of the game to be saved.
        self.gameTitle = QtGui.QLineEdit('Best game ever', self)
        self.gameTitle.setFixedWidth(buttonWidth)
        self.gameTitle.move(buttonStartXCoordinate, 134)

        saveButton = QtGui.QPushButton('Save Game', self)
        saveButton.setFixedWidth(buttonWidth)
        saveButton.move(buttonStartXCoordinate, 174)
        saveButton.clicked.connect(self.saveGame)

        returnButton = QtGui.QPushButton('Back', self)
        returnButton.setFixedWidth(buttonWidth)
        returnButton.move(buttonStartXCoordinate, 214)
        returnButton.clicked.connect(self.returnToPauseMenu)

        self.setFixedHeight(468)
        self.setFixedWidth(468)

        self.show()

    ##this method saves the current game by calling the database method saveGame().
    def saveGame(self):

        gameTitle = str(self.gameTitle.text())
        if gameTitle == '':
            invalidGameTitle = '''Please enter a name to identify your game.'''
            QtGui.QMessageBox.warning(self,'Warning!',invalidGameTitle,QtGui.QMessageBox.Ok)
            return

        db = Database()
        db.saveGame(self.username, gameTitle, self.board)

        saveSuccessMessage = '''You game has been successfully saved as:\n\n''' + gameTitle + '''\n\nat ''' + datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
        QtGui.QMessageBox.information(self,'Success!',saveSuccessMessage,QtGui.QMessageBox.Ok);
    ##this method emit returnToPauseMenuSignal when called.
    def returnToPauseMenu(self):
        self.returnToPauseMenuSignal.emit()
