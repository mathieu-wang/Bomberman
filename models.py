# Class that represents an user account
class UserAccount:
    def __init__(self, username, realname, password, maxLevelReached=1,
                 cumulativeScore=0, numGamesPlayed=0, savedGames=None):
        self.username = username
        self.realname = realname
        self.password = password
        self.maxLevelReached = maxLevelReached
        self.cumulativeScore = cumulativeScore
        self.numGamesPlayed = numGamesPlayed
        self.savedGames = savedGames
