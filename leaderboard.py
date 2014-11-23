from PyQt4 import QtCore, QtGui

from database import Database

class Leaderboard(QtGui.QTableWidget):

    backToMainMenuSignal = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(Leaderboard, self).__init__(parent)
        self.initUI()
        self.db = Database()
        self.fillData()

    def initUI(self):
        self.rowCount = 10
        self.colCount = 5
        self.setRowCount(self.rowCount)
        self.setColumnCount(self.colCount)

        tableHeader = ['User Name', 'Real Name', 'Level Unlocked', 'Number of Games Played', 'Cumulative Score']
        self.setHorizontalHeaderLabels(tableHeader)

        #item.setFlags(QtCore.Qt.ItemIsEnabled)

        # Same score is counted as two. Users with the same score are sorted alphabetically (by username).


    def fillData(self):
        users = self.db.getTopTenUsers()

        i = 0
        for user in users:
            self.setItem(i, 0, QtGui.QTableWidgetItem(QtCore.QString(user['username'])))
            self.setItem(i, 1, QtGui.QTableWidgetItem(QtCore.QString(user['realname'])))
            self.setItem(i, 2, QtGui.QTableWidgetItem(QtCore.QString(str(user['maxLevelReached']))))
            self.setItem(i, 3, QtGui.QTableWidgetItem(QtCore.QString(str(user['numGamesPlayed']))))
            self.setItem(i, 4, QtGui.QTableWidgetItem(QtCore.QString(str(user['cumulativeScore']))))
            i += 1

