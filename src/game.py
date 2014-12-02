import sys

from PyQt4 import QtGui

from board import Board
from login_menu import LoginMenu
from main_menu import MainMenu
from leaderboard import Leaderboard
from pause_menu import PauseMenu
from level_menu import LevelMenu
from save_menu import SaveMenu
from load_menu import LoadMenu
from settings_menu import AccountSettingsMenu
from database import Database
from level import Level
import constant

## Main controller
class Game(QtGui.QMainWindow):
    
    ## Constructor, initializes UI
    def __init__(self):
        super(Game, self).__init__()
        self.initUI()
    
    ## This method initializes the UI and center the window
    def initUI(self):    

        self.centralWidget = QtGui.QStackedWidget()
        self.setCentralWidget(self.centralWidget)

        self.showLoginMenu()

    ## This method displays the login menu
    def showLoginMenu(self):

        self.loginWidget = LoginMenu(self)

        self.loginWidget.loginSuccessSignal.connect(self.showMainMenu)

        self.centralWidget.addWidget(self.loginWidget)
        self.centralWidget.setCurrentWidget(self.loginWidget)

        self.setWindowTitle('Login')
        self.center()

    ## This method displays the login menu after successful login
    def showMainMenu(self):

        self.username = self.loginWidget.loggedUsername

        self.mainMenuWidget = MainMenu(self)

        self.mainMenuWidget.playGameSignal.connect(self.showLevelMenu)
        self.mainMenuWidget.logoutGameSignal.connect(self.showLoginMenu)
        self.mainMenuWidget.quitGameSignal.connect(self.quit)
        self.mainMenuWidget.showLeaderboardSignal.connect(self.showLeaderboard)
        self.mainMenuWidget.loadMenuSignal.connect(self.showLoadMenu)
        self.mainMenuWidget.changeSettingsSignal.connect(self.showAccountSettingsMenu)

        self.centralWidget.addWidget(self.mainMenuWidget)
        self.centralWidget.setCurrentWidget(self.mainMenuWidget)

        self.setWindowTitle('Main Menu')
        self.center()

    ## This method displays the level menu where player is asked to select level to play
    def showLevelMenu(self):

        self.levelMenuWidget = LevelMenu(self, self.username)

        self.levelMenuWidget.backToMainMenuSignal.connect(self.showMainMenu)
        self.levelMenuWidget.startLevelSignal.connect(self.showBoard)

        self.centralWidget.addWidget(self.levelMenuWidget)
        self.centralWidget.setCurrentWidget(self.levelMenuWidget)

        self.setWindowTitle('Choose Level')
        self.center()

    ## This method displays the bomberman gameplay and initiliazes the game to the selected level
    # @param levelNum: Integer the level number
    # @param level: Level object containing all the information necessary to run the game
    def showBoard(self, levelNum, level=None):

        if not level:
            level = Level(self.username,levelNum)
        
        self.board_widget = Board(level, self)

        self.board_widget.pauseGameSignal.connect(self.showPauseMenu)
        self.board_widget.gameOverSignal.connect(self.gameOver)
        self.board_widget.updateScoreInDbSignal.connect(self.updateScoreInDb)

        self.centralWidget.addWidget(self.board_widget)
        self.centralWidget.setCurrentWidget(self.board_widget)

        self.board_widget.start()

        self.resize(468, 468)
        self.setWindowTitle('Bomberman')

    ## This method isplays the leaderboard
    def showLeaderboard(self, previousMenu):

        self.leaderboardWidget = Leaderboard(self, previousMenu)

        if previousMenu == constant.MAIN_MENU:
            self.leaderboardWidget.backSignal.connect(self.showMainMenu)
        elif previousMenu == constant.PAUSE_MENU:
            self.leaderboardWidget.backSignal.connect(self.showPauseMenu)

        self.centralWidget.addWidget(self.leaderboardWidget)
        self.centralWidget.setCurrentWidget(self.leaderboardWidget)

        self.setWindowTitle('Leaderboard')
        self.center()

    ## This method displays pause menu
    def showPauseMenu(self):

        self.pauseMenuWidget = PauseMenu(self)

        self.pauseMenuWidget.resumeGameSignal.connect(self.resumeToGame)
        self.pauseMenuWidget.quitGameSignal.connect(self.quit)
        self.pauseMenuWidget.showLeaderboardSignal.connect(self.showLeaderboard)
        self.pauseMenuWidget.saveMenuSignal.connect(self.showSaveMenu)
        self.pauseMenuWidget.loadMenuSignal.connect(self.showLoadMenu)
        self.pauseMenuWidget.backToMainMenuSignal.connect(self.showMainMenu)

        self.centralWidget.addWidget(self.pauseMenuWidget)
        self.centralWidget.setCurrentWidget(self.pauseMenuWidget)

        self.setWindowTitle('Pause')
        self.center()

    ## This method displays the menu to save game instances
    def showSaveMenu(self):
        
        self.saveMenuWidget = SaveMenu(self.username, self.board_widget.saveBomberman(), self)

        self.saveMenuWidget.returnToPauseMenuSignal.connect(self.resumeToPauseMenu)

        self.centralWidget.addWidget(self.saveMenuWidget)
        self.centralWidget.setCurrentWidget(self.saveMenuWidget)

        self.setWindowTitle('Save Game Menu')
        self.center()

    ## This method displays the menu to load saved game instances
    def showLoadMenu(self, previousMenu):
        
        self.loadMenuWidget = LoadMenu(self, self.loginWidget.loggedUsername, previousMenu)

        self.loadMenuWidget.loadSavedGameSignal.connect(self.loadSavedGame)

        if previousMenu == constant.MAIN_MENU:
            self.loadMenuWidget.backSignal.connect(self.showMainMenu)
        elif previousMenu == constant.PAUSE_MENU:
            self.loadMenuWidget.backSignal.connect(self.showPauseMenu)

        self.centralWidget.addWidget(self.loadMenuWidget)
        self.centralWidget.setCurrentWidget(self.loadMenuWidget)

        self.setWindowTitle('Load Game Menu')
        self.center()

    ## This method displays the account settings menu
    def showAccountSettingsMenu(self):

        self.accountSettingsMenuWidget = AccountSettingsMenu(self, self.loginWidget.loggedUsername)
        self.accountSettingsMenuWidget.backToMainMenuSignal.connect(self.showMainMenu)
        self.centralWidget.addWidget(self.accountSettingsMenuWidget)
        self.centralWidget.setCurrentWidget(self.accountSettingsMenuWidget)

        self.setWindowTitle('Account Settings')
        self.center()

    ## This method centers the current window to the middle
    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, 
            (screen.height()-size.height())/2)

    ## This method exits the process
    def quit(self):
        sys.exit()

    ## This method resumes the game after a pause action
    def resumeToGame(self):

        self.centralWidget.setCurrentWidget(self.board_widget)
        self.board_widget.start()

    ## This method navigates back to pause menu 
    def resumeToPauseMenu(self):

        self.centralWidget.setCurrentWidget(self.pauseMenuWidget)
    
    ## This method loads the current user's saved game instance corresponding to the provided game name 
    def loadSavedGame(self, gamename):

        db = Database()
        level = db.loadGame(self.username, str(gamename))

        self.showBoard(1, level)

    ## This method emits a signal to acknowledge game over state
    def gameOver(self):
        print 'Game over!'
        self.updateGamesPlayedInDb()
        self.showMainMenu()

    ## This method updates the user's current score to the database
    def updateScoreInDb(self, incrementalScore):
        db = Database()
        db.updateUserScore(self.loginWidget.loggedUsername, self.board_widget.level.score + incrementalScore)

    ## This method updates the users' number of games played to the database
    def updateGamesPlayedInDb(self):
        db = Database()
        db.incrementNumOfGamesPlayed(self.loginWidget.loggedUsername)

## Main method starting the process
def main():

    app = QtGui.QApplication([])
    game = Game()
    game.show()   
    sys.exit(app.exec_())

if __name__ == '__main__':

    main()
