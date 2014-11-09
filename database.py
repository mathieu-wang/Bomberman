import dataset

class Database:

	def __init__(self):

		# Create a database in RAM
		# self.db = dataset.connect('sqlite:///:memory:')

		# Connecting to a SQLite database
		self.db = dataset.connect('sqlite:///db.sqlite')

		# Get the table of user/password
		self.userTable = self.db['user']

	def createUser(self, name, username, password):

		# Check if user already exists
		if self.userTable.find_one(username=username):
			return False

		# Insert user in the table
		if self.userTable.insert(dict(name=name, username=username, password=password)):
			return True

	def checkUser(self, username, password):

		# Fetch user from table
		user = self.userTable.find_one(username=username)

		# Check if user exists
		if user is None:
			return False

		# Check if password and username matches
		if user['username'] == username and user['password'] == password:
			return True

		return False

	def changePassword(self, username, password):

		# Check if user exists
		if self.userTable.find_one(username=username):
			return False

		# Update to new password
		if table.update(dict(username=username, password=password), [username]):
			return True

	# Usernames must be at least 6 character long.
	# It must only contains UTF-8 characters and digits excluding all accented latin characters.
	def isValidUsername(self, username):

		# At least 6 characters long
		if len(username) < 6:
			return False

		return True

	# A password must be at least 8 character long with the same character constraints as a username.
	# In addition, it must necessarily include a minimum of 1 Upper case letter, 1 Lower case letter, 1 digits and 1 special character.
	def isValidPassword(self,password):

		# At least 8 characters long
		if len(password) < 8:
			return False

		hasUpperCase = False
		hasLowerCase = False
		hasDigit = False
		hasSpecialChar = False
		for char in password:
			# At least 1 upper case letter
			if char >= 'A' and char <= 'Z':
				hasUpperCase = True
			# At least 1 lower case letter
			elif char >= 'a' and char <= 'z':
				hasLowerCase = True
			# At least 1 digit
			elif char >= '0' and char <= '9':
				hasDigit = True
			# At least 1 special character
			else:
				hasSpecialChar = True

		if hasUpperCase and hasLowerCase and hasDigit and hasSpecialChar:
			return True

		return False


