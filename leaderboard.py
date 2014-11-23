from PyQt4 import QtCore, QtGui

from database import Database

class Leaderboard(QtGui.QTableWidget):

    backToMainMenuSignal = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(Leaderboard, self).__init__(parent)
        self.initUI()
        self.db = Database()

    def initUI(self):
        self.setRowCount(10)
        self.setColumnCount(5)

        tableHeader = ['User Name', 'Real Name', 'Level Unlocked', 'Number of Games Played', 'Cumulative Score']
        self.setHorizontalHeaderLabels(tableHeader)

        #item.setFlags(QtCore.Qt.ItemIsEnabled)

        # Same score is counted as two. Users with the same score are sorted alphabetically (by username).

