from PyQt4 import QtCore, QtGui

##This class is a widget that displays the pause menu. It includes the following buttons
#that the user can interact with:\n
#resumeButton: emit resumeGameSignal when clicked.\n
#saveButton: emit saveMenuSignal when clicked.\n
#laodButton: emit loadMenuSignal when clicked.\n
#showLeaderboardButton: emit showLeaderboardSignal when clicked.\n
#backButton: emit backToMainMenuSignal when clicked.\n
#quitButton: emit quitGameSignal when clicked.
from src import constant


class PauseMenu(QtGui.QWidget):

    ##Signal which will be used to resume the current game.
    resumeGameSignal = QtCore.pyqtSignal()
    ##Signal which will be used to quit the whole application.
    quitGameSignal = QtCore.pyqtSignal()
    ##Signal which will be used to launch the leaderboard.
    #@Param int is set as 'constant.PAUSE_MENU'.
    showLeaderboardSignal = QtCore.pyqtSignal(int)
    ##Signal which will be used to launch save menu.
    saveMenuSignal = QtCore.pyqtSignal()
    ##Signal which will be used to launch load menu.
    #@Param int is set as 'constant.PAUSE_MENU'.
    loadMenuSignal = QtCore.pyqtSignal(int)
    ##Signal which will be used to go back to the main menu.
    backToMainMenuSignal = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(PauseMenu, self).__init__(parent)
        self.initUI()

    ##this method initialize the GUI of the pause menu.
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

    ##emit resumeGameSignal when called.
    def resume(self):
        self.resumeGameSignal.emit()
    ##emit quitGameSignal when called.
    def quit(self):
        self.quitGameSignal.emit()
    ##emit showLeaderboardSignal with parameter 'constant.PAUSE_MENU' when called.
    def showLeaderboard(self):
        self.showLeaderboardSignal.emit(constant.PAUSE_MENU)
    ##emit backToMainMenuSignal when called.
    def back(self):
        self.backToMainMenuSignal.emit()
    ##emit saveMenuSignal when called.
    def save(self):
        self.saveMenuSignal.emit()
    ##emit loadMenuSignal with parameter 'constant.PAUSE_MENU' when called.
    def load(self):
        self.loadMenuSignal.emit(constant.PAUSE_MENU)