from PyQt4 import QtCore, QtGui

class LoginMenu(QtGui.QWidget):

	successLogin = QtCore.pyqtSignal()
	
	def __init__(self, parent=None):
		super(LoginMenu, self).__init__(parent)
		self.initUI()

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
		self.loginUsername = QtGui.QLineEdit('Username')
		self.loginPassword = QtGui.QLineEdit('Password')

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
		self.signUpButton.clicked.connect(self.signUp)

	def login(self):
		print self.loginUsername.text()
		self.successLogin.emit()
	def signUp(self):
		pass
