from PyQt4 import QtCore, QtGui

from database import Database

class AccountSettingsMenu(QtGui.QWidget):

    loggedUsername = None
    backToMainMenuSignal = QtCore.pyqtSignal()

    def __init__(self, parent, username):
        super(AccountSettingsMenu, self).__init__(parent)
        self.parent = parent
        self.loggedUsername = username
        self.db = Database()
        self.initUI()

    def initUI(self):
        user = self.db.getUserAccount(self.loggedUsername)
        oldRealName = user['realname']
        oldUsername = user['username']
        oldPassword = user['password']

        buttonWidth = 150
        column1XCoordinate = 84
        column2XCoordinate = 234

        self.title = QtGui.QLabel('Real Name:', self)
        self.title.setFixedWidth(buttonWidth)
        self.title.setAlignment(QtCore.Qt.AlignHCenter)
        self.title.move(column1XCoordinate, 142)

        self.title = QtGui.QLabel('User Name:', self)
        self.title.setFixedWidth(buttonWidth)
        self.title.setAlignment(QtCore.Qt.AlignHCenter)
        self.title.move(column1XCoordinate, 172)

        self.title = QtGui.QLabel('Password:', self)
        self.title.setFixedWidth(buttonWidth)
        self.title.setAlignment(QtCore.Qt.AlignHCenter)
        self.title.move(column1XCoordinate, 202)

        # Column 2
        self.title = QtGui.QLabel('Change Account Settings:', self)
        self.title.setFixedWidth(buttonWidth)
        self.title.setAlignment(QtCore.Qt.AlignHCenter)
        self.title.move(column2XCoordinate, 92)

        self.yourName = QtGui.QLineEdit(oldRealName, self)
        self.yourName.setFixedWidth(buttonWidth)
        self.yourName.move(column2XCoordinate, 142)

        self.username = QtGui.QLineEdit(oldUsername, self)
        self.username.setFixedWidth(buttonWidth)
        self.username.move(column2XCoordinate, 172)

        self.password = QtGui.QLineEdit(oldPassword, self)
        self.password.setEchoMode(QtGui.QLineEdit.Password)
        self.password.setFixedWidth(buttonWidth)
        self.password.move(column2XCoordinate, 202)

        self.changeButton = QtGui.QPushButton('Change Settings', self)
        self.changeButton.setFixedWidth(buttonWidth)
        self.changeButton.move(column2XCoordinate, 232)
        self.changeButton.clicked.connect(self.changeSettings)

        self.backButton = QtGui.QPushButton('Back to Main Menu', self)
        self.backButton.setFixedWidth(buttonWidth)
        self.backButton.move(column2XCoordinate, 272)
        self.backButton.clicked.connect(self.backToMainMenu)

        self.setFixedHeight(468)
        self.setFixedWidth(468)

    def changeSettings(self):

        name = str(self.yourName.text())
        username = str(self.username.text())
        password = str(self.password.text())

        if (not self.db.isValidUsername(username)):
            invalidUsernameMessage = '''Usernames must be at least 6 characters long.'''
            QtGui.QMessageBox.warning(self,'Warning!',invalidUsernameMessage,QtGui.QMessageBox.Ok)
        elif (not self.db.isValidPassword(password)):
            invalidPasswordMessage = '''Invalid password. The password must be at least 8 characters long and contain the following:\n - 1 Upper case letter\n - 1 Lower case letter\n - 1 Digit\n - 1 Special character'''
            QtGui.QMessageBox.warning(self,'Warning!',invalidPasswordMessage,QtGui.QMessageBox.Ok)
        elif self.db.updateUserAccount(self.loggedUsername, username, name, password):
            changeSuccessMessage = '''Your account information has been successfully changed.'''
            QtGui.QMessageBox.information(self,'Success!',changeSuccessMessage,QtGui.QMessageBox.Ok);
            self.parent.loginWidget.loggedUsername = username
        else:
            QtGui.QMessageBox.warning(self,'Warning!','The username has been taken',QtGui.QMessageBox.Ok)

    def backToMainMenu(self):
        self.backToMainMenuSignal.emit()