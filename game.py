from PyQt4 import QtGui, QtCore
import sys

from board import Board, StatusBar
from login_menu import LoginMenu
from main_menu import MainMenu
from leaderboard import Leaderboard
from pause_menu import PauseMenu
from level_menu import LevelMenu
from save_menu import SaveMenu
from load_menu import LoadMenu
from database import Database
import global_constants

class Game(QtGui.QMainWindow):
    
    def __init__(self):
        super(Game, self).__init__()
        self.initUI()
        
    def initUI(self):    

        self.central_widget = QtGui.QStackedWidget()
        self.setCentralWidget(self.central_widget)

        # self.show_main_menu()
        self.show_login_menu()
        # self.show_board(10)

    def show_login_menu(self):

        self.login_widget = LoginMenu(self)

        self.login_widget.loginSuccessSignal.connect(self.show_main_menu)

        self.central_widget.addWidget(self.login_widget)
        self.central_widget.setCurrentWidget(self.login_widget)

        self.setWindowTitle('Login')
        self.center()

    def show_main_menu(self):

        self.mainMenuWidget = MainMenu(self)

        self.mainMenuWidget.playGameSignal.connect(self.show_level_menu)
        self.mainMenuWidget.logoutGameSignal.connect(self.show_login_menu)
        self.mainMenuWidget.quitGameSignal.connect(self.quit)
        self.mainMenuWidget.showLeaderboardSignal.connect(self.show_leaderboard)

        self.central_widget.addWidget(self.mainMenuWidget)
        self.central_widget.setCurrentWidget(self.mainMenuWidget)

        self.setWindowTitle('Main Menu')
        self.center()

    def show_level_menu(self):

        self.levelMenuWidget = LevelMenu(self, self.login_widget.loggedUsername)

        self.levelMenuWidget.backToMainMenuSignal.connect(self.show_main_menu)
        self.levelMenuWidget.startLevelSignal.connect(self.show_board)

        self.central_widget.addWidget(self.levelMenuWidget)
        self.central_widget.setCurrentWidget(self.levelMenuWidget)

        self.setWindowTitle('Choose Level')
        self.center()

    def show_board(self, level):
        
        self.board_widget = Board(self.login_widget.loggedUsername, level, self)

        self.statusBar = StatusBar(self.board_widget)
        self.statusBar.setFixedWidth(468)

        self.board_widget.pauseGameSignal.connect(self.show_pause_menu)

        self.board_widget.endGameSignal.connect(self.update_lives)
        self.board_widget.gameOverSignal.connect(self.game_over)

        self.statusBar.resize(100, 468)
        self.coundownTimer = QtCore.QTimer()
        self.coundownTimer.start(1000)
        self.coundownTimer.timeout.connect(self.timeout_event)

        self.central_widget.addWidget(self.board_widget)
        self.central_widget.setCurrentWidget(self.board_widget)
        self.board_widget.start()
        self.resize(468, 468)
        self.board_widget.pauseGameSignal.connect(self.show_pause_menu)
        self.setWindowTitle('Bomberman')

    def show_leaderboard(self, previousMenu):

        self.leaderboardWidget = Leaderboard(self, previousMenu)

        if previousMenu == global_constants.MAIN_MENU:
            self.leaderboardWidget.backSignal.connect(self.show_main_menu)
        elif previousMenu == global_constants.PAUSE_MENU:
            self.leaderboardWidget.backSignal.connect(self.show_pause_menu)

        self.central_widget.addWidget(self.leaderboardWidget)
        self.central_widget.setCurrentWidget(self.leaderboardWidget)

        self.setWindowTitle('Leaderboard')
        self.center()

    def timeout_event(self):
        self.statusBar.timeLeft -= 1
        self.statusBar.timesLabel.setText('Time Left: ' + str(self.statusBar.timeLeft))

    def show_pause_menu(self):

        self.coundownTimer.stop()

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
        
        self.saveMenuWidget = SaveMenu(self.login_widget.loggedUsername, self.board_widget.saveBoard(), self)

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

        self.coundownTimer.start(1000)

        self.board_widget.pause()
        self.central_widget.setCurrentWidget(self.board_widget)

    def resumeToPauseMenu(self):

        self.coundownTimer.stop()

        self.board_widget.pause()
        self.central_widget.setCurrentWidget(self.pauseMenuWidget)
        
    def loadSavedGame(self, gamename):
        db = Database()
        savedBoard = db.loadGame(self.login_widget.loggedUsername, str(gamename))

        self.board_widget.loadBoard(savedBoard)

        self.coundownTimer.start(1000)

        self.central_widget.setCurrentWidget(self.board_widget)

    def update_lives(self):
        self.statusBar.livesLabel.setText('Lives: ' + str(self.board_widget.bomberman.lives))

    def game_over(self):
        self.show_main_menu()

def main():

    app = QtGui.QApplication([])
    game = Game()
    game.show()   
    sys.exit(app.exec_())

if __name__ == '__main__':

    main()
