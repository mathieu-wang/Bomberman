from PyQt4 import QtCore, QtGui

from src.database import Database

##This class is a widget that displays the leaderBoard. It includes the following buttons
#and fields that the user can interact with:\n
#table: is a field that contains the top 10 players sorted by cumulative scores.
#backButton: emit backSignal when clicked.
class Leaderboard(QtGui.QWidget):

    ##Signal which will be used to go back to the previous menu based on an int.
    #@Param int is set as 'previousMenu'
    backSignal = QtCore.pyqtSignal(int)

    def __init__(self, parent, previousMenu):
        super(Leaderboard, self).__init__(parent)
        ##int used to keep track of the previous menu.
        self.previousMenu = previousMenu
        self.initUI()
        ##instance of the database.
        self.db = Database()
        self.fillData()

    ##this method initiaze the GUI of the leaderboard.
    def initUI(self):
        vbox = QtGui.QVBoxLayout()
        self.setLayout(vbox)

        ##the number of rows is set to 10.
        self.rowCount = 10
        ##the number of columns is set to 5
        self.colCount = 5
        ##Is a table of 5 columns (colCount) and 10 rows (rowCount) which contains the top 10 scores.
        self.table = QtGui.QTableWidget()
        self.table.setRowCount(self.rowCount)
        self.table.setColumnCount(self.colCount)

        tableHeader = ['User Name', 'Real Name', 'Level Unlocked', 'Number of Games Played', 'Cumulative Score']
        self.table.setHorizontalHeaderLabels(tableHeader)
        self.table.resizeColumnsToContents()

        backButton = QtGui.QPushButton('Back', self)
        backButton.setFixedWidth(200)
        backButton.clicked.connect(self.back)

        vbox.addWidget(self.table)
        vbox.addWidget(backButton)

    ##this methods fills the data in the table.
    #users: contains top 10 players sorted by cumulative scores.
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
    ##emit backSignal when called.
    def back(self):
        self.backSignal.emit(self.previousMenu)