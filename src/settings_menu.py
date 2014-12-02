from PyQt4 import QtCore, QtGui

from src.database import Database

##this class is a widget that displays the account settings menu. It includes buttons
#and fields that the user can interact with.\n
class AccountSettingsMenu(QtGui.QWidget):

    ##instance of the currently active user's username.
    loggedUsername = None
    ##Signal which will be used to return to the main menu.
    backToMainMenuSignal = QtCore.pyqtSignal()

    def __init__(self, parent, username):
        super(AccountSettingsMenu, self).__init__(parent)
        ##instance of this class's parent.
        self.parent = parent
        self.loggedUsername = username
        ##instance of the database.
        self.db = Database()
        self.initUI()

    ##this method initialize the GUI for the account settings menu.
    def initUI(self):
        user = self.db.getUserAccount(self.loggedUsername)
        oldRealName = user['realname']
        oldUsername = user['username']
        oldPassword = user['password']

        buttonWidth = 150
        column1XCoordinate = 84
        column2XCoordinate = 234

        ##is a QLabel that displays the titles of following fields.
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

        ##is a QLineEdit which the user can use to enter his new real name.
        self.yourName = QtGui.QLineEdit(oldRealName, self)
        self.yourName.setFixedWidth(buttonWidth)
        self.yourName.move(column2XCoordinate, 142)
        ##is a QLineEdit which the user can use to enter his new username.
        self.username = QtGui.QLineEdit(oldUsername, self)
        self.username.setFixedWidth(buttonWidth)
        self.username.move(column2XCoordinate, 172)
        ##is a QLineEdit which the user can use to enter his new password.
        self.password = QtGui.QLineEdit(oldPassword, self)
        self.password.setEchoMode(QtGui.QLineEdit.Password)
        self.password.setFixedWidth(buttonWidth)
        self.password.move(column2XCoordinate, 202)
        ##is a buttton that calls changeSettings() when clicked.
        self.changeButton = QtGui.QPushButton('Change Settings', self)
        self.changeButton.setFixedWidth(buttonWidth)
        self.changeButton.move(column2XCoordinate, 232)
        self.changeButton.clicked.connect(self.changeSettings)
        ##is a button that calls backToMainMenu() when clicked.
        self.backButton = QtGui.QPushButton('Back to Main Menu', self)
        self.backButton.setFixedWidth(buttonWidth)
        self.backButton.move(column2XCoordinate, 272)
        self.backButton.clicked.connect(self.backToMainMenu)

        self.setFixedHeight(468)
        self.setFixedWidth(468)

    ##this method is used to change the user's name,username AND password.
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
    ##this method emit backToMainMenuSignal when called.
    def backToMainMenu(self):
        self.backToMainMenuSignal.emit()