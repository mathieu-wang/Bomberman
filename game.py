from PyQt4 import QtGui
import sys

from board import Board
from login_menu import LoginMenu
from main_menu import MainMenu
from leaderboard import Leaderboard
from pause_menu import PauseMenu
from level_menu import LevelMenu
from save_menu import SaveMenu
from load_menu import LoadMenu
from database import Database
from bomberman import Bomberman
import constant

class Game(QtGui.QMainWindow):
    
    def __init__(self):
        super(Game, self).__init__()
        self.initUI()
        
    def initUI(self):    

        self.centralWidget = QtGui.QStackedWidget()
        self.setCentralWidget(self.centralWidget)

        self.showLoginMenu()

    def showLoginMenu(self):

        self.loginWidget = LoginMenu(self)

        self.loginWidget.loginSuccessSignal.connect(self.showMainMenu)

        self.centralWidget.addWidget(self.loginWidget)
        self.centralWidget.setCurrentWidget(self.loginWidget)

        self.setWindowTitle('Login')
        self.center()

    def showMainMenu(self):

        self.username = self.loginWidget.loggedUsername

        self.mainMenuWidget = MainMenu(self)

        self.mainMenuWidget.playGameSignal.connect(self.showLevelMenu)
        self.mainMenuWidget.logoutGameSignal.connect(self.showLoginMenu)
        self.mainMenuWidget.quitGameSignal.connect(self.quit)
        self.mainMenuWidget.showLeaderboardSignal.connect(self.showLeaderboard)
        self.mainMenuWidget.loadMenuSignal.connect(self.showLoadMenu)

        self.centralWidget.addWidget(self.mainMenuWidget)
        self.centralWidget.setCurrentWidget(self.mainMenuWidget)

        self.setWindowTitle('Main Menu')
        self.center()

    def showLevelMenu(self):

        self.levelMenuWidget = LevelMenu(self, self.username)

        self.levelMenuWidget.backToMainMenuSignal.connect(self.showMainMenu)
        self.levelMenuWidget.startLevelSignal.connect(self.showBoard)

        self.centralWidget.addWidget(self.levelMenuWidget)
        self.centralWidget.setCurrentWidget(self.levelMenuWidget)

        self.setWindowTitle('Choose Level')
        self.center()

    def showBoard(self, level, bomberman=None):

        if not bomberman:
            bomberman = Bomberman(self.username,level)
        
        self.board_widget = Board(bomberman, self)

        self.board_widget.pauseGameSignal.connect(self.showPauseMenu)
        self.board_widget.gameOverSignal.connect(self.gameOver)
        self.board_widget.updateScoreInDbSignal.connect(self.updateScoreInDb)

        self.centralWidget.addWidget(self.board_widget)
        self.centralWidget.setCurrentWidget(self.board_widget)

        self.board_widget.start()

        self.resize(468, 468)
        self.setWindowTitle('Bomberman')

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

    def showSaveMenu(self):
        
        self.saveMenuWidget = SaveMenu(self.username, self.board_widget.saveBomberman(), self)

        self.saveMenuWidget.returnToPauseMenuSignal.connect(self.resumeToPauseMenu)

        self.centralWidget.addWidget(self.saveMenuWidget)
        self.centralWidget.setCurrentWidget(self.saveMenuWidget)

        self.setWindowTitle('Save Game Menu')
        self.center()

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


    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, 
            (screen.height()-size.height())/2)

    def quit(self):
        sys.exit()

    def resumeToGame(self):

        self.centralWidget.setCurrentWidget(self.board_widget)
        self.board_widget.start()

    def resumeToPauseMenu(self):

        self.centralWidget.setCurrentWidget(self.pauseMenuWidget)
        
    def loadSavedGame(self, gamename):

        db = Database()
        bomberman = db.loadGame(self.username, str(gamename))

        self.showBoard(1, bomberman)

    def gameOver(self):
        print 'Game over!'
        self.updateGamesPlayedInDb()
        self.showMainMenu()

    def updateScoreInDb(self, incrementalScore):
        db = Database()
        db.updateUserScore(self.loginWidget.loggedUsername, self.board_widget.bomberman.score + incrementalScore)

    def updateGamesPlayedInDb(self):
        db = Database()
        db.incrementNumOfGamesPlayed(self.loginWidget.loggedUsername)

def main():

    app = QtGui.QApplication([])
    game = Game()
    game.show()   
    sys.exit(app.exec_())

if __name__ == '__main__':

    main()
