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

        self.central_widget = QtGui.QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.show_login_menu()

    def show_login_menu(self):

        self.login_widget = LoginMenu(self)

        self.login_widget.loginSuccessSignal.connect(self.show_main_menu)

        self.central_widget.addWidget(self.login_widget)
        self.central_widget.setCurrentWidget(self.login_widget)

        self.setWindowTitle('Login')
        self.center()

    def show_main_menu(self):

        self.username = self.login_widget.loggedUsername

        self.mainMenuWidget = MainMenu(self)

        self.mainMenuWidget.playGameSignal.connect(self.show_level_menu)
        self.mainMenuWidget.logoutGameSignal.connect(self.show_login_menu)
        self.mainMenuWidget.quitGameSignal.connect(self.quit)
        self.mainMenuWidget.showLeaderboardSignal.connect(self.show_leaderboard)
        self.mainMenuWidget.showSettingsSignal.connect(self.show_load_menu)

        self.central_widget.addWidget(self.mainMenuWidget)
        self.central_widget.setCurrentWidget(self.mainMenuWidget)

        self.setWindowTitle('Main Menu')
        self.center()

    def show_level_menu(self):

        self.levelMenuWidget = LevelMenu(self, self.username)

        self.levelMenuWidget.backToMainMenuSignal.connect(self.show_main_menu)
        self.levelMenuWidget.startLevelSignal.connect(self.show_board)

        self.central_widget.addWidget(self.levelMenuWidget)
        self.central_widget.setCurrentWidget(self.levelMenuWidget)

        self.setWindowTitle('Choose Level')
        self.center()

    def show_board(self, level, bomberman=None):

        if not bomberman:
            bomberman = Bomberman(self.username,level)
        
        self.board_widget = Board(bomberman, self)

        self.board_widget.pauseGameSignal.connect(self.show_pause_menu)
        self.board_widget.gameOverSignal.connect(self.gameOver)
        self.board_widget.updateScoreInDbSignal.connect(self.updateScoreInDb)

        self.central_widget.addWidget(self.board_widget)
        self.central_widget.setCurrentWidget(self.board_widget)

        self.board_widget.start()

        self.resize(468, 468)
        self.setWindowTitle('Bomberman')

    def show_leaderboard(self, previousMenu):

        self.leaderboardWidget = Leaderboard(self, previousMenu)

        if previousMenu == constant.MAIN_MENU:
            self.leaderboardWidget.backSignal.connect(self.show_main_menu)
        elif previousMenu == constant.PAUSE_MENU:
            self.leaderboardWidget.backSignal.connect(self.show_pause_menu)

        self.central_widget.addWidget(self.leaderboardWidget)
        self.central_widget.setCurrentWidget(self.leaderboardWidget)

        self.setWindowTitle('Leaderboard')
        self.center()

    def show_pause_menu(self):

        self.pauseMenuWidget = PauseMenu(self)

        self.pauseMenuWidget.resumeGameSignal.connect(self.resumeToGame)
        self.pauseMenuWidget.quitGameSignal.connect(self.quit)
        self.pauseMenuWidget.showLeaderboardSignal.connect(self.show_leaderboard)
        self.pauseMenuWidget.saveMenuSignal.connect(self.show_save_menu)
        self.pauseMenuWidget.loadMenuSignal.connect(self.show_load_menu)
        self.pauseMenuWidget.backToMainMenuSignal.connect(self.show_main_menu)

        self.central_widget.addWidget(self.pauseMenuWidget)
        self.central_widget.setCurrentWidget(self.pauseMenuWidget)

        self.setWindowTitle('Pause')
        self.center()

    def show_save_menu(self):
        
        self.saveMenuWidget = SaveMenu(self.username, self.board_widget.saveBomberman(), self)

        self.saveMenuWidget.returnToPauseMenuSignal.connect(self.resumeToPauseMenu)

        self.central_widget.addWidget(self.saveMenuWidget)
        self.central_widget.setCurrentWidget(self.saveMenuWidget)

        self.setWindowTitle('Save Game Menu')
        self.center()

    def show_load_menu(self):
        
        self.loadMenuWidget = LoadMenu(self.login_widget.loggedUsername, self)

        self.loadMenuWidget.loadSavedGameSignal.connect(self.loadSavedGame)
        self.loadMenuWidget.returnToPauseMenuSignal.connect(self.resumeToPauseMenu)

        self.central_widget.addWidget(self.loadMenuWidget)
        self.central_widget.setCurrentWidget(self.loadMenuWidget)

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

        self.central_widget.setCurrentWidget(self.board_widget)
        self.board_widget.start()

    def resumeToPauseMenu(self):

        self.central_widget.setCurrentWidget(self.pauseMenuWidget)
        
    def loadSavedGame(self, gamename):

        db = Database()
        bomberman = db.loadGame(self.username, str(gamename))

        self.show_board(1, bomberman)

    def gameOver(self):
        print 'Game over!'
        self.updateGamesPlayedInDb()
        self.show_main_menu()

    def updateScoreInDb(self, incrementalScore):
        db = Database()
        db.updateUserScore(self.login_widget.loggedUsername, self.board_widget.bomberman.score + incrementalScore)

    def updateGamesPlayedInDb(self):
        db = Database()
        db.incrementNumOfGamesPlayed(self.login_widget.loggedUsername)

def main():

    app = QtGui.QApplication([])
    game = Game()
    game.show()   
    sys.exit(app.exec_())

if __name__ == '__main__':

    main()
