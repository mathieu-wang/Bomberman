from PyQt4 import QtCore, QtGui

from database import Database

class LoginMenu(QtGui.QWidget):

    loginSuccessSignal = QtCore.pyqtSignal()
    loggedUsername = None

    def __init__(self, parent=None):
        super(LoginMenu, self).__init__(parent)
        self.initUI()
        self.db = Database()
        self.db.createUserAccountsForDemo()

    def initUI(self):

        buttonWidth = 150
        column1XCoordinate = 84
        column2XCoordinate = 234

        #first Column

        self.signUpTitle = QtGui.QLabel('Create Account:', self)
        self.signUpTitle.setFixedWidth(buttonWidth)
        self.signUpTitle.setAlignment(QtCore.Qt.AlignHCenter)
        self.signUpTitle.move(column1XCoordinate, 92)

        self.yourName = QtGui.QLineEdit('Your Name', self)
        self.yourName.setFixedWidth(buttonWidth)
        self.yourName.move(column1XCoordinate, 142)

        self.username = QtGui.QLineEdit('Username', self)
        self.username.setFixedWidth(buttonWidth)
        self.username.move(column1XCoordinate, 172)

        self.password = QtGui.QLineEdit('Password', self)
        self.password.setEchoMode(QtGui.QLineEdit.Password)
        self.password.setFixedWidth(buttonWidth)
        self.password.move(column1XCoordinate, 202)

        self.signUpButton = QtGui.QPushButton('SignUp', self)
        self.signUpButton.setFixedWidth(buttonWidth)
        self.signUpButton.move(column1XCoordinate, 232)
        self.signUpButton.clicked.connect(self.register)

        #second Column

        self.loginTitle = QtGui.QLabel('Login:', self)
        self.loginTitle.setAlignment(QtCore.Qt.AlignHCenter)
        self.loginTitle.setFixedWidth(buttonWidth)
        self.loginTitle.move(column2XCoordinate, 92)

        self.loginUsername = QtGui.QLineEdit('Username', self)
        self.loginUsername.setFixedWidth(buttonWidth)
        self.loginUsername.move(column2XCoordinate, 172)

        self.loginPassword = QtGui.QLineEdit('Password', self)
        self.loginPassword.setEchoMode(QtGui.QLineEdit.Password)
        self.loginPassword.setFixedWidth(buttonWidth)
        self.loginPassword.move(column2XCoordinate, 202)

        self.loginButton = QtGui.QPushButton('Login', self)
        self.loginButton.setFixedWidth(buttonWidth)
        self.loginButton.move(column2XCoordinate, 232)
        self.loginButton.clicked.connect(self.login)

        self.setFixedHeight(468)
        self.setFixedWidth(468)

    def login(self):

        username = str(self.loginUsername.text())
        password = str(self.loginPassword.text())

        if self.db.checkUser(username, password):
            self.loginSuccessSignal.emit()
            self.loggedUsername = username
        else:
            QtGui.QMessageBox.warning(self,'Warning!','Wrong username or password',QtGui.QMessageBox.Ok)

    def register(self):

        name = str(self.yourName.text())
        username = str(self.username.text())
        password = str(self.password.text())

        if (not self.db.isValidUsername(username)):
            invalidUsernameMessage = '''Usernames must be at least 6 characters long.'''
            QtGui.QMessageBox.warning(self,'Warning!',invalidUsernameMessage,QtGui.QMessageBox.Ok)
        elif (not self.db.isValidPassword(password)):
            invalidPasswordMessage = '''Invalid password. The password must be at least 8 characters long and contain the following:\n - 1 Upper case letter\n - 1 Lower case letter\n - 1 Digit\n - 1 Special character'''
            QtGui.QMessageBox.warning(self,'Warning!',invalidPasswordMessage,QtGui.QMessageBox.Ok)
        elif self.db.createUser(name,username,password):
            registerSuccessMessage = '''Your account has been successfully registered. Please login using the right side menu.'''
            QtGui.QMessageBox.information(self,'Success!',registerSuccessMessage,QtGui.QMessageBox.Ok);
        else:
            QtGui.QMessageBox.warning(self,'Warning!','The username has been taken',QtGui.QMessageBox.Ok)
