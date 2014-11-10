from PyQt4 import QtCore, QtGui

from database import Database


class LoginMenu(QtGui.QWidget):

	loginSuccessful = QtCore.pyqtSignal()
	
	def __init__(self, parent=None):
		super(LoginMenu, self).__init__(parent)
		self.initUI()
		self.db = Database()

	def initUI(self):

		grid = QtGui.QGridLayout()
		self.setLayout(grid)

		self.empty = QtGui.QLabel('     ')
		self.title1 = QtGui.QLabel('Create Account Here!')
		self.title2 = QtGui.QLabel('Login Here!')
		self.loginButton = QtGui.QPushButton('Login')
		self.signUpButton = QtGui.QPushButton('Sign Up')
		self.yourName = QtGui.QLineEdit('Your name')
		self.username = QtGui.QLineEdit('Username')
		self.password = QtGui.QLineEdit('Password')
		self.password.setEchoMode(QtGui.QLineEdit.Password)
		self.loginUsername = QtGui.QLineEdit('Username')
		self.loginPassword = QtGui.QLineEdit('Password')
		self.loginPassword.setEchoMode(QtGui.QLineEdit.Password)

		grid.addWidget(self.title1, 0, 0)
		grid.addWidget(self.empty, 0, 1)
		grid.addWidget(self.title2, 0, 2)
		grid.addWidget(self.yourName, 1, 0)
		grid.addWidget(self.empty, 1, 1)
		grid.addWidget(self.empty, 1, 2)
		grid.addWidget(self.username, 2, 0)
		grid.addWidget(self.empty, 2, 1)
		grid.addWidget(self.loginUsername, 2, 2)
		grid.addWidget(self.password, 3, 0)
		grid.addWidget(self.empty, 3, 1)
		grid.addWidget(self.loginPassword, 3, 2)
		grid.addWidget(self.loginButton, 4, 2)
		grid.addWidget(self.empty, 4, 1)
		grid.addWidget(self.signUpButton, 4, 0)

		self.loginButton.clicked.connect(self.login)
		self.signUpButton.clicked.connect(self.register)

	def login(self):

		username = str(self.loginUsername.text())
		password = str(self.loginPassword.text())

		if self.db.checkUser(username,password):
			self.loginSuccessful.emit()
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
