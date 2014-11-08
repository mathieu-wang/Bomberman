from PyQt4 import QtCore, QtGui

class LoginMenu(QtGui.QWidget):
    def __init__(self, parent=None):
        super(LoginMenu, self).__init__(parent)
        layout = QtGui.QHBoxLayout()
        self.button = QtGui.QPushButton('Login')
        layout.addWidget(self.button)
        self.setLayout(layout)
        # you might want to do self.button.click.connect(self.parent().login) here