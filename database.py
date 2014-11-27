import dataset
import cPickle as pickle

from models import UserAccount

class Database:

    def __init__(self):

        # Create a database in RAM
        # self.db = dataset.connect('sqlite:///:memory:')

        # Connecting to a SQLite database
        self.db = dataset.connect('sqlite:///db.sqlite')

        # Get the table of user/password
        self.userTable = self.db['user']

    def createUser(self, name, username, password):
        userAccount = UserAccount(username, name, password)

        # Check if user already exists
        if self.userTable.find_one(username=username):
            return False

        # Insert user in the table
        if self.userTable.insert(userAccount.__dict__):
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

    def hasUser(self, username):
        user = self.userTable.find_one(username=username)

        # Check if user exists
        if user is None:
            return False
        else:
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
    def isValidPassword(self, password):

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

    def createUserAccountsForDemo(self):
        userAccount1 = UserAccount("Demo01", "Demo01", "Dem@Us3R01", 11, 10000)
        userAccount2 = UserAccount("Demo02", "Demo02", "Dem@Us3R02", 11, 10000)
        userAccount3 = UserAccount("Demo03", "Demo03", "Dem@Us3R03", 13, 13000)
        userAccount4 = UserAccount("Demo04", "Demo04", "Dem@Us3R04", 14, 14000)
        userAccount5 = UserAccount("Demo05", "Demo05", "Dem@Us3R05", 15, 16000)
        userAccount6 = UserAccount("Demo06", "Demo06", "Dem@Us3R06", 16, 16000)
        userAccount7 = UserAccount("Demo07", "Demo07", "Dem@Us3R07", 15, 16000)
        userAccount8 = UserAccount("Demo08", "Demo08", "Dem@Us3R08", 10, 9000)
        userAccount9 = UserAccount("Demo09", "Demo09", "Dem@Us3R09", 11, 11000)
        userAccount10 = UserAccount("Demo10", "Demo10", "Dem@Us3R10", 12, 12000)

        userAccounts = [userAccount1, userAccount2, userAccount3, userAccount4, userAccount5,
                        userAccount6, userAccount7, userAccount8, userAccount9, userAccount10]
        for userAccount in userAccounts:
            if not self.hasUser(userAccount.username):
                self.userTable.insert(userAccount.__dict__)

    def getUserAccount(self, username):
        return self.userTable.find_one(username=username)

    # Get top players sorted by cumulative score.
    # Same score is counted as two. Users with the same score are sorted alphabetically (by username).
    def getTopTenUsers(self):
        return self.userTable.find(_limit=10, order_by=['-cumulativeScore', 'username'])

    def getHighestUnlockedLevel(self, username):
        userAccount = self.getUserAccount(username)
        return userAccount['maxLevelReached']

    def saveGame(self, username, gamename, board):

        try:
            f = file('db.pkl', 'rb')
            self.game = pickle.load(f)
            f.close()
        except:
            self.game = {}
            f = file('db.pkl', 'wb')
            pickle.dump(self.game, f, protocol=pickle.HIGHEST_PROTOCOL)
            f.close()

        if self.game == {}:
            self.game = {username:{gamename:board}}
        elif username not in self.game.keys():
            self.game[username] = {gamename:board}
        else:
            self.game[username][gamename] = board

        f = file('db.pkl', 'wb')
        pickle.dump(self.game, f, protocol=pickle.HIGHEST_PROTOCOL)
        f.close()

    def loadListSavedGames(self, username):

        try:
            f = file('db.pkl', 'rb')
            self.game = pickle.load(f)
            f.close()
        except:
            self.game = {}
            f = file('db.pkl', 'wb')
            pickle.dump(self.game, f, protocol=pickle.HIGHEST_PROTOCOL)
            f.close()

        if username not in self.game.keys():
            return []

        gameList = []

        for g in self.game[username].keys():
            gameList.append(g)

        return gameList

    def loadGame(self, username, gamename):

        try:
            f = file('db.pkl', 'rb')
            self.game = pickle.load(f)
            f.close()
        except:
            self.game = {}
            f = file('db.pkl', 'wb')
            pickle.dump(self.game, f, protocol=pickle.HIGHEST_PROTOCOL)
            f.close()

        if username not in self.game.keys():
            return None
        elif gamename not in self.game[username].keys():
            return None

        return self.game[username][gamename]
