from PyQt4 import QtCore, QtGui

import datetime

from database import Database

class SaveMenu(QtGui.QWidget):

    returnToPauseMenuSignal = QtCore.pyqtSignal()

    def __init__(self, username, board, parent=None):
        super(SaveMenu, self).__init__(parent)

        self.board = board
        self.username = username
        self.initUI()

    def initUI(self):

        buttonWidth = 150
        buttonStartXCoordinate = 159

        self.saveLabel = QtGui.QLabel('Game name', self)
        self.saveLabel.setAlignment(QtCore.Qt.AlignHCenter)
        self.saveLabel.setFixedWidth(buttonWidth)
        self.saveLabel.move(buttonStartXCoordinate, 94)

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

    def returnToPauseMenu(self):
        self.returnToPauseMenuSignal.emit()
