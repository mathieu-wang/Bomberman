from PyQt4 import QtCore, QtGui

class MainMenu(QtGui.QWidget):

    playGameSignal = QtCore.pyqtSignal()
    logoutGameSignal = QtCore.pyqtSignal()
    quitGameSignal = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(MainMenu, self).__init__(parent)
        self.initUI()

    def initUI(self):

        playButton = QtGui.QPushButton('Play Bomberman', self)
        playButton.move(115, 30)
        playButton.clicked.connect(self.play)

        logoutButton = QtGui.QPushButton('Logout', self)
        logoutButton.move(139, 70)
        logoutButton.clicked.connect(self.logout)

        quitButton = QtGui.QPushButton('Quit', self)
        quitButton.move(150, 110)
        quitButton.clicked.connect(self.quit)

        self.setGeometry(300, 300, 280, 170)

        self.show()

    def play(self):
        self.playGameSignal.emit()

    def logout(self):
        self.logoutGameSignal.emit()

    def quit(self):
        self.quitGameSignal.emit()

