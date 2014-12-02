from PyQt4 import QtCore, QtGui

from database import Database

##This class is a widget that displays the login menu. It includes the following buttons
#and fields that the user can interact with:\n
#youName: is a LineEdit widget the user uses to enter his name.\n
#username: is a LineEdit widget the user uses to enter his username at login or signup.\n
#password: is a LineEdit widget the user uses to enter his password at login or signup.\n
#signupButton: calls register() method when clicked.\n
#loginButton: calls login() method when clicked.\n
class LoginMenu(QtGui.QWidget):

    ##Signal which will be used to launch the main menu.
    loginSuccessSignal = QtCore.pyqtSignal()
    ##the currently logged in user's username. initialized to 'None' if not currently logged in.
    loggedUsername = None

    def __init__(self, parent=None):
        super(LoginMenu, self).__init__(parent)
        self.initUI()
        ##instance of the database.
        self.db = Database()
        self.db.createUserAccountsForDemo()

    ##This method initialize the GUI of the login menu.
    def initUI(self):

        buttonWidth = 150
        column1XCoordinate = 84
        column2XCoordinate = 234

        # First Column

        ##is a QLabel to show the signup Title.
        self.signUpTitle = QtGui.QLabel('Create Account:', self)
        self.signUpTitle.setFixedWidth(buttonWidth)
        self.signUpTitle.setAlignment(QtCore.Qt.AlignHCenter)
        self.signUpTitle.move(column1XCoordinate, 92)
        ##is a QLineEdit that creates a field the user uses to enter his name.
        self.yourName = QtGui.QLineEdit('Your Name', self)
        self.yourName.setFixedWidth(buttonWidth)
        self.yourName.move(column1XCoordinate, 142)
        ##is a QLineEdit that creates a field the user uses to enter his username.
        self.username = QtGui.QLineEdit('Username', self)
        self.username.setFixedWidth(buttonWidth)
        self.username.move(column1XCoordinate, 172)
        ##is a QLineEdit that creates a field the user uses to enter his password
        self.password = QtGui.QLineEdit('Password', self)
        self.password.setEchoMode(QtGui.QLineEdit.Password)
        self.password.setFixedWidth(buttonWidth)
        self.password.move(column1XCoordinate, 202)
        ##is a button that calls the register() method when clicked.
        self.signUpButton = QtGui.QPushButton('SignUp', self)
        self.signUpButton.setFixedWidth(buttonWidth)
        self.signUpButton.move(column1XCoordinate, 232)
        self.signUpButton.clicked.connect(self.register)

        # Second Column
        ##is a QLabel to show the login Title.
        self.loginTitle = QtGui.QLabel('Login:', self)
        self.loginTitle.setAlignment(QtCore.Qt.AlignHCenter)
        self.loginTitle.setFixedWidth(buttonWidth)
        self.loginTitle.move(column2XCoordinate, 92)
        ##is a QLineEdit that creates a field the user uses to enter his username.
        self.loginUsername = QtGui.QLineEdit('Username', self)
        self.loginUsername.setFixedWidth(buttonWidth)
        self.loginUsername.move(column2XCoordinate, 172)
        ##is a QLineEdit that creates a field the user uses to enter his password.
        self.loginPassword = QtGui.QLineEdit('Password', self)
        self.loginPassword.setEchoMode(QtGui.QLineEdit.Password)
        self.loginPassword.setFixedWidth(buttonWidth)
        self.loginPassword.move(column2XCoordinate, 202)
        ##is a button that calls the login() method when clicked.
        self.loginButton = QtGui.QPushButton('Login', self)
        self.loginButton.setFixedWidth(buttonWidth)
        self.loginButton.move(column2XCoordinate, 232)
        self.loginButton.clicked.connect(self.login)

        self.setFixedHeight(468)
        self.setFixedWidth(468)

    ##this method is used to login an existing user.
    #it verifies if the user's information match an existing user account and then emit loginSuccessSignal.
    def login(self):

        username = str(self.loginUsername.text())
        password = str(self.loginPassword.text())

        if self.db.checkUser(username, password):
            self.loggedUsername = username
            self.loginSuccessSignal.emit()
        else:
            QtGui.QMessageBox.warning(self,'Warning!','Wrong username or password',QtGui.QMessageBox.Ok)
    ##this method is used to register a new user.
    #It first verifies if the user's username and password follow the restrictions.
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
            registerSuccessMessage = '''Your account has been successfully registered.'''
            QtGui.QMessageBox.information(self,'Success!',registerSuccessMessage,QtGui.QMessageBox.Ok);
            self.loginSuccessSignal.emit()
        else:
            QtGui.QMessageBox.warning(self,'Warning!','The username has been taken',QtGui.QMessageBox.Ok)
