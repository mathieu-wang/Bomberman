import unittest
import sys

from PyQt4 import QtGui

from src.game import Game
from src.tile import Tile
from src.database import Database
from src import constant

class IntegrationTest(unittest.TestCase):
    app = None

    TestUserName = "testUser"

    @classmethod
    def setUpClass(cls):
        global app
        app = QtGui.QApplication([])

    def setUp(self):
        self.db = Database()
        self.db.createUser("testUserRealName", IntegrationTest.TestUserName, "testUserPassword0$")
        self.game = Game()
        self.game.username = IntegrationTest.TestUserName
        self.game.loginWidget.loggedUsername = IntegrationTest.TestUserName
        self.game.showBoard(1)

    def tearDown(self):
        self.db.deleteAccount(IntegrationTest.TestUserName)
        self.game.board_widget.destroy()
        self.game.destroy()

    @classmethod
    def tearDownClass(cls):
        app.quit()

    def testKillEnemiesOnBoardUpdateDb(self):
        self.assertTrue(self.db.hasUser(IntegrationTest.TestUserName))

        self.game.board_widget.level.clearEnemies()
        self.game.board_widget.setTileAt(2, 1, Tile.Balloom)
        self.game.board_widget.level.bomberman.curX = 1
        self.game.board_widget.level.bomberman.curY = 1
        self.game.board_widget.level.setBomberman()
        self.game.board_widget.level.setBomb()

        tempList = [2, 1, constant.DIRECTION_WEST, Tile.Balloom]
        self.game.board_widget.level.listEnemies.append(tempList)

        self.game.board_widget.level.numberEnemies = 1
        self.game.board_widget.level.listTypeEnemies[0] = 1
        self.game.board_widget.level.bomberman.rangeOfBombs = 3

        self.game.board_widget.detonateBomb()

        self.assertEqual(self.game.board_widget.tileAt(2, 1), Tile.Empty, "Bomb detonation did not kill enemy")
        self.assertEqual(0, self.game.board_widget.level.numberEnemies, "Enemy was not removed from map")

        self.assertEqual(self.db.getUserAccount(IntegrationTest.TestUserName)['cumulativeScore'], 100)


if __name__ == '__main__':

    unittest.main()
    sys.exit(app.exec_)
