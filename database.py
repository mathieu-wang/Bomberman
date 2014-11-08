import dataset

class Database:

	def __init__(self):

		# Create a database in RAM
		# self.db = dataset.connect('sqlite:///:memory:')

		# Connecting to a SQLite database
		self.db = dataset.connect('sqlite:///db.sqlite')

		# Get the table of user/password
		self.userTable = self.db['user']

	def createUser(self, username, password):

		# Check if user already exists
		if self.userTable.find_one(username=username):
			return False

		# Insert user in the table
		if self.userTable.insert(dict(username=username, password=password)):
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
