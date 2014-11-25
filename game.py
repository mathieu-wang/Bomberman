from PyQt4 import QtGui
import sys

from board import Board
from login_menu import LoginMenu
from main_menu import MainMenu
from leaderboard import Leaderboard
from pause_menu import PauseMenu


class Game(QtGui.QMainWindow):
    
    def __init__(self):
        super(Game, self).__init__()
        self.initUI()
        
    def initUI(self):    

        self.central_widget = QtGui.QStackedWidget()
        self.setCentralWidget(self.central_widget)

        #self.show_main_menu()
        self.show_login_menu()

    def show_login_menu(self):

        self.login_widget = LoginMenu(self)
        self.login_widget.loginSuccessSignal.connect(self.show_main_menu)

        self.central_widget.addWidget(self.login_widget)
        self.central_widget.setCurrentWidget(self.login_widget)
        self.setWindowTitle('Login')
        self.center()

    def show_main_menu(self):

        self.mainMenuWidget = MainMenu(self)
        self.mainMenuWidget.playGameSignal.connect(self.show_board)
        self.mainMenuWidget.logoutGameSignal.connect(self.show_login_menu)
        self.mainMenuWidget.quitGameSignal.connect(self.quit)
        self.mainMenuWidget.showLeaderboardSignal.connect(self.show_leaderboard)

        self.central_widget.addWidget(self.mainMenuWidget)
        self.central_widget.setCurrentWidget(self.mainMenuWidget)
        self.setWindowTitle('Main Menu')
        self.center()

    def show_board(self):

        self.board_widget = Board(self)

        self.central_widget.addWidget(self.board_widget)
        self.central_widget.setCurrentWidget(self.board_widget)
        self.board_widget.start()
        self.resize(468,468) # Standard res
        self.board_widget.pauseGameSignal.connect(self.show_pause_menu)
        self.setWindowTitle('Bomberman')
        self.center()     

    def show_leaderboard(self):

        self.leaderboardWidget = Leaderboard(self)
        self.leaderboardWidget.backToMainMenuSignal.connect(self.show_main_menu)

        self.central_widget.addWidget(self.leaderboardWidget)
        self.central_widget.setCurrentWidget(self.leaderboardWidget)
        self.setWindowTitle('Leaderboard')
        self.center()

    def show_pause_menu(self):

        self.pauseMenuWidget = PauseMenu(self)
        self.central_widget.addWidget(self.pauseMenuWidget)
        self.central_widget.setCurrentWidget(self.pauseMenuWidget)

        self.pauseMenuWidget.resumeGameSignal.connect(self.resume)
        self.pauseMenuWidget.quitGameSignal.connect(self.quit)
        self.pauseMenuWidget.showLeaderboardSignal.connect(self.show_leaderboard)
        #self.pauseMenuWidget.saveGameSignal.connect()
        #self.pauseMenuWidget.loadGameSignal.connect()
        self.pauseMenuWidget.backToMainMenuSignal.connect(self.show_main_menu)
        self.setWindowTitle('Pause')
        self.center()


    def center(self):

        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, 
            (screen.height()-size.height())/2)

    def quit(self):
        
        sys.exit()

    def resume(self):

        self.central_widget.setCurrentWidget(self.board_widget)
        self.board_widget.pause()

def main():

    app = QtGui.QApplication([])
    game = Game()
    game.show()   
    sys.exit(app.exec_())

if __name__ == '__main__':

    main()
