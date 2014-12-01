## Instances of this class represent all information relevant to a specific user account
class UserAccount:

    ## Constructor with three required parameters: username, realname, and password
    # @param username Required. The username associated to the account. Used as key to retrieve all other fields from the database
    # @param realname Required. The real name of the user
    # @param password Required. The password of the user
    # @param maxLevelReached Default is 1. Used to initialize the user account with a specific unlocked level
    # @param cumulativeScore Default is 0. Used to initialize the user account with a specific cumulative score
    # @param numGamesPlated Default is 0. Used to initialize the user account with a specific number of games played
    # @param numGamesPlated Default is 0. Used to initialize the user account with a specific number of games played
    def __init__(self, username, realname, password, maxLevelReached=1,
            cumulativeScore=0, numGamesPlayed=0,):
        self.username = username
        self.realname = realname
        self.password = password
        self.maxLevelReached = maxLevelReached
        self.cumulativeScore = cumulativeScore
        self.numGamesPlayed = numGamesPlayed