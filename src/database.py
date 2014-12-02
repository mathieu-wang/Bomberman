import cPickle as pickle

import dataset

from src.models import UserAccount



## Class that handles the interface with database
#
# An instance of this class connects to a local sqlite database with a single table.
# The table stores each attribute of models.UserAccount as a column, with the username being the primary key.
class Database:

    ## Constructor that connects to a sqlite database, and gets the 'user' table from it.
    #
    # It creates the database and the table if it cannot find them.
    # @param test By default False.
    # If set to True, the database will be in memory instead of on the file system. Used in unit tests.
    def __init__(self, test=False):
        if test:
            self.db = dataset.connect('sqlite:///:memory:')  # Create a database in RAM
        else:
            self.db = dataset.connect('sqlite:///db.sqlite')  # Connecting to a SQLite database

        # Get the table of user/password
        self.userTable = self.db['user']

    ## Create a new user in the database
    # @param name the real name
    # @param username the username
    # @param password the password
    # @return True if user account properly created, False if user already exists
    def createUser(self, name, username, password):
        userAccount = UserAccount(username, name, password)

        # Check if user already exists
        if self.userTable.find_one(username=username):
            return False

        # Insert user in the table
        if self.userTable.insert(userAccount.__dict__):
            return True

    ## Update user account information with new username, realname, and password
    # @param oldUsername the old user name with which we retrieve the account
    # @param newUsername the new user name we want to set
    # @param newRealname the new real name we want to set
    # @param newPassword the new password we want to set
    def updateUserAccount(self, oldUsername, newUsername, newRealname, newPassword):
        # Check if user already exists
        if self.userTable.find_one(username=newUsername):
            return False

        userAccount = self.userTable.find_one(username=oldUsername)
        userAccount['username'] = newUsername
        userAccount['realname'] = newRealname
        userAccount['password'] = newPassword

        self.userTable.delete(username=oldUsername)
        self.userTable.insert(userAccount)
        return True

    ## Delete the account from the database
    # @param username the user we want to delete
    def deleteAccount(self, username):
        self.userTable.delete(username=username)

    ## Check whether the provided credentials correspond to a valid user account in the database
    # @param username the username to be checked
    # @param password the password to be checked
    # @return True if the username exists, False otherwise
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

    ## Check whether the provided user name exists in the database
    # @param username the username to be checked
    def hasUser(self, username):
        user = self.userTable.find_one(username=username)

        # Check if user exists
        if user is None:
            return False
        else:
            return True

    ## Check whether the username is at least 6 character long.
    # @param username the username to be checked
    # @return True if the username is valid, False otherwise
    def isValidUsername(self, username):

        # At least 6 characters long
        if len(username) < 6:
            return False

        return True

    ## Check whether a password is valid.
    # A valid password must be at least 8 characters long.
    # In addition, it must necessarily include a minimum of 1 Upper case letter, 1 Lower case letter, 1 digits and 1 special character.
    # @param password the password to be checked
    # @return True if the password is valid, False otherwise
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

    ## Get the UserAccount object as a dictionary from the database
    # @param username the username used as a key to retrieve the UserAccount
    # @return the UserAccount object as a dictionary
    def getUserAccount(self, username):
        return self.userTable.find_one(username=username)

    ## Get top players sorted by cumulative score.
    # Same score is counted as two. Users with the same score are sorted alphabetically (by username).
    # @return a iterable list of UserAccount objects as dictionaries
    def getTopTenUsers(self):
        return self.userTable.find(_limit=10, order_by=['-cumulativeScore', 'username'])

    ## Get highest unlocked level by the user.
    # @param username the user for whom we want to get the highest unlocked level
    # @return the highest unlocked level of that user
    def getHighestUnlockedLevel(self, username):
        userAccount = self.getUserAccount(username)
        return userAccount['maxLevelReached']

    ## Save current game state into a file
    # @param username the user for whom we want to save the game
    # @param gamename the name of the game we want to save
    # @param board the current board containing all game state that needs to be saved
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

    ## Load the list of previously saved games for an user
    # @param username the user for whom we want to load the list of saved game
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

    ## Load a specific game for an user
    # @param username the user for whom we want to load the game
    # @param gamename the name of the game we want to load
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

    ## Update the user's cumulative score in the database
    # @param username the user for whom we want to update the score
    # @param scoreToAdd the score we want to add to the existing cumulative score in the database
    def updateUserScore(self, username, scoreToAdd):
        user = self.userTable.find_one(username=username)
        user['cumulativeScore'] += scoreToAdd
        self.userTable.update(user, ['username'])

    ## Increment the total number of games played for the user
    # @param username the user for whom we want to increment the number of games played
    def incrementNumOfGamesPlayed(self, username):
        user = self.userTable.find_one(username=username)
        user['numGamesPlayed'] += 1
        self.userTable.update(user, ['username'])