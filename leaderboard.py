from PyQt4 import QtCore, QtGui

from database import Database

class Leaderboard(QtGui.QWidget):

    backToMainMenuSignal = QtCore.pyqtSignal()
    backToPauseMenuSignal = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(Leaderboard, self).__init__(parent)
        self.initUI()
        self.db = Database()
        self.fillData()

    def initUI(self):
        vbox = QtGui.QVBoxLayout()
        self.setLayout(vbox)

        self.rowCount = 10
        self.colCount = 5

        self.table = QtGui.QTableWidget()
        self.table.setRowCount(self.rowCount)
        self.table.setColumnCount(self.colCount)

        tableHeader = ['User Name', 'Real Name', 'Level Unlocked', 'Number of Games Played', 'Cumulative Score']
        self.table.setHorizontalHeaderLabels(tableHeader)
        self.table.resizeColumnsToContents()

        backPauseButton = QtGui.QPushButton('Back To Pause Menu', self)
        backPauseButton.setFixedWidth(200)
        backPauseButton.clicked.connect(self.backToPauseMenu)

        backButton = QtGui.QPushButton('Back To Main Menu', self)
        backButton.setFixedWidth(200)
        backButton.clicked.connect(self.backToMainMenu)

        vbox.addWidget(self.table)
        vbox.addWidget(backPauseButton)
        vbox.addWidget(backButton)

    def fillData(self):
        users = self.db.getTopTenUsers()

        i = 0
        for user in users:
            userNameItem = QtGui.QTableWidgetItem(QtCore.QString(user['username']))
            realNameItem = QtGui.QTableWidgetItem(QtCore.QString(user['realname']))
            maxLevelItem = QtGui.QTableWidgetItem(QtCore.QString(str(user['maxLevelReached'])))
            numGamesItem = QtGui.QTableWidgetItem(QtCore.QString(str(user['numGamesPlayed'])))
            cumScoreItem = QtGui.QTableWidgetItem(QtCore.QString(str(user['cumulativeScore'])))

            #Set flag to prevent user from selecting/editing cells
            userNameItem.setFlags(QtCore.Qt.ItemIsEnabled)
            realNameItem.setFlags(QtCore.Qt.ItemIsEnabled)
            maxLevelItem.setFlags(QtCore.Qt.ItemIsEnabled)
            numGamesItem.setFlags(QtCore.Qt.ItemIsEnabled)
            cumScoreItem.setFlags(QtCore.Qt.ItemIsEnabled)

            self.table.setItem(i, 0, userNameItem)
            self.table.setItem(i, 1, realNameItem)
            self.table.setItem(i, 2, maxLevelItem)
            self.table.setItem(i, 3, numGamesItem)
            self.table.setItem(i, 4, cumScoreItem)
            i += 1

    def backToMainMenu(self):
        self.backToMainMenuSignal.emit()

    def backToPauseMenu(self):
        self.backToPauseMenuSignal.emit()
