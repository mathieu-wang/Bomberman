import unittest
import sys

from PyQt4 import QtGui

from board import Board
from bomberman import Bomberman
from tile import Tile
from game import Game
import constant


class TestBoard(unittest.TestCase):
    app = None

    @classmethod
    def setUpClass(cls):
        global app
        app = QtGui.QApplication([])

    def setUp(self):
        self.game = Game()
        self.bomberman = Bomberman("testUser", 1)
        self.board = Board(self.bomberman, self.game)
        self.board.start()

    def tearDown(self):
        self.board.destroy()
        self.game.destroy()

    @classmethod
    def tearDownClass(cls):
        app.quit()

    def testInitializeBoardWithConcreteWalls(self):
        self.assertEqual(self.board.bomberman.board[0][0].peek(), Tile.Concrete, "Corner tile should be Concrete, board not initialized properly")

    def testInitializeBoardWithExactlyOneBomberman(self):
        numberOfBombermanOnTheBoard = 0
        board = self.board.bomberman.board
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j].peek() == Tile.Bomberman:
                    numberOfBombermanOnTheBoard += 1

        self.assertEqual(numberOfBombermanOnTheBoard, 1, "Did not see exactly one bomberman on the board")

    def testSetTileAt(self):
        self.assertEqual(self.board.bomberman.board[1][1].peek(), Tile.Empty)
        self.board.setTileAt(1, 1, Tile.Brick)
        self.assertEqual(self.board.bomberman.board[1][1].peek(), Tile.Brick)

    def testTileAt(self):
        for i in range(len(self.board.bomberman.board)):
            for j in range(len(self.board.bomberman.board[i])):
                self.assertEqual(self.board.tileAt(j, i), self.board.bomberman.board[i][j].peek())

    def testSetBomberman(self):
        self.assertNotEqual(self.board.tileAt(1, 2), Tile.Bomberman)
        self.board.bomberman.curX = 1
        self.board.bomberman.curY = 2
        self.board.bomberman.setBomberman()
        self.assertEqual(self.board.tileAt(1, 2), Tile.Bomberman)

    def testSetBomb(self):
        self.assertNotEqual(self.board.tileAt(1, 2), Tile.Bomb)
        self.board.bomberman.curX = 1
        self.board.bomberman.curY = 2
        self.board.bomberman.setBomberman() #bomberman should be here already
        self.board.bomberman.setBomb()

        self.assertEqual(len(self.board.bomberman.bombQueue), 1, "Bomb did not get enqueued")
        self.assertEqual(self.board.bomberman.bombQueue.pop(), (1, 2, constant.TIME_BOMB), "Bomb's coordinates are wrong")
        self.assertEqual(self.board.tileAt(1, 2), Tile.Bomberman, "Bomberman is not on top of a bomb")

        self.board.popTileAt(1, 2)
        self.assertEqual(self.board.tileAt(1, 2), Tile.Bomb, "There is no bomb underneath Bomberman")

    def testDetonateBomb(self):
        self.board.bomberman.curX = 1
        self.board.bomberman.curY = 1
        self.board.bomberman.setBomberman()
        self.board.bomberman.setBomb()

        self.board.detonateBomb()

        self.board.popTileAt(1, 1) #pop Bomberman
        self.assertNotEqual(self.board.tileAt(1, 1), Tile.Bomb, "Bomb did not explode")

    def testDetonateBombHasNoEffectOnConcrete(self):
        self.board.curX = 1
        self.board.curY = 1
        self.board.bomberman.setBomberman()
        self.board.bomberman.setBomb()

        self.board.detonateBomb()

        self.board.popTileAt(1, 1) #pop Bomberman
        self.assertEqual(self.board.tileAt(1, 0), Tile.Concrete, "Concrete got destroyed by bomb")

    def testDetonateBombDestroysBrick(self):
        self.board.setTileAt(1, 3, Tile.Brick)
        self.board.bomberman.curX = 1
        self.board.bomberman.curY = 1
        self.board.bomberman.setBomberman()
        self.board.bomberman.setBomb()

        self.board.detonateBomb()

        self.assertEqual(self.board.tileAt(1, 2), Tile.Empty, "Brick did not get destroyed by bomb")

    def testDetonateBombDestroysOnlyClosestBrickInTheSameDirection(self):
        self.board.setTileAt(1, 2, Tile.Brick)
        self.board.setTileAt(1, 3, Tile.Brick)
        self.board.bomberman.curX = 1
        self.board.bomberman.curY = 1
        self.board.bomberman.setBomberman()
        self.board.bomberman.setBomb()

        self.board.detonateBomb()

        self.assertEqual(self.board.tileAt(1, 2), Tile.Empty, "Closer Brick did not get destroyed by bomb")
        self.assertEqual(self.board.tileAt(1, 3), Tile.Brick, "Further Brick got destroyed by bomb")

    def testDetonateBombDestroysMultipleBricks(self):
        self.board.setTileAt(1, 2, Tile.Brick)
        self.board.setTileAt(2, 1, Tile.Brick)
        self.board.bomberman.curX = 1
        self.board.bomberman.curY = 1
        self.board.bomberman.setBomberman()
        self.board.bomberman.setBomb()

        self.board.bomberman.rangeOfBombs = 3

        self.board.detonateBomb()

        self.assertEqual(self.board.tileAt(1, 2), Tile.Empty, "One of the Bricks did not get destroyed by bomb")
        self.assertEqual(self.board.tileAt(2, 1), Tile.Empty, "One of the Bricks did not get destroyed by bomb")

    def testDetonateBombSpawnsEnemiesWhenExitIsHit(self):
        self.board.setTileAt(1, 2, Tile.Exit)

        self.board.bomberman.curX = 1
        self.board.bomberman.curY = 1
        self.board.bomberman.setBomberman()
        self.board.bomberman.setBomb()

        self.board.bomberman.rangeOfBombs = 3

        self.board.detonateBomb()

        count = 0

        for i in range(self.bomberman.numberEnemies):
            if (self.bomberman.listTypeEnemies[i] != 0):
                count += 1

        self.assertEqual(count, 1, "Not all enemies are the same type when the exit is hit")
        self.assertEqual(len(self.bomberman.listEnemies), 8, "The number of enemies when the exit is hit is not 8")

    def testDetonateBombSpawnsEnemiesWhenPowerupIsHit(self):
        self.board.setTileAt(1, 2, Tile.Powerup)

        self.board.bomberman.curX = 1
        self.board.bomberman.curY = 1
        self.board.bomberman.setBomberman()
        self.board.bomberman.setBomb()

        self.board.bomberman.rangeOfBombs = 3

        self.board.detonateBomb()

        count = 0

        for i in range(self.bomberman.numberEnemies):
            if (self.bomberman.listTypeEnemies[i] != 0):
                count += 1

        self.assertEqual(count, 1, "Not all enemies are the same type when the powerup is hit")
        self.assertEqual(len(self.bomberman.listEnemies), 8, "The number of enemies when the powerup is hit is not 8")

    def testTryMoveToConcrete(self):
        self.board.setTileAt(0, 0, Tile.Concrete)
        self.assertFalse(self.board.tryMove(0, 0), "Was able to move to a concrete tile")

    def testTryMoveToBrick(self):
        self.board.setTileAt(1, 1, Tile.Brick)
        self.assertFalse(self.board.tryMove(1, 1), "Was able to move to a brick tile")

    def testTryMoveToBrick(self):
        self.board.setTileAt(2, 2, Tile.Empty)
        self.assertTrue(self.board.tryMove(2, 2), "Was not able to move to an empty tile")

    def testMoveEnemyWithIntelligence1(self):
        self.bomberman.clearEnemies()
        self.board.setTileAt(2, 1, Tile.Balloom)
        self.board.setTileAt(1, 1, Tile.Empty)

        tempList = [2, 1, 3, 8]
        self.bomberman.listEnemies.append(tempList)

        self.bomberman.numberEnemies = 1
        self.bomberman.listTypeEnemies[0] = 1

        self.board.moveEnemy(constant.SPEED_SLOW)

        self.assertEqual(self.board.tileAt(1, 1), Tile.Balloom, "Enemy did not move")
        
    def testMoveEnemyWithIntelligence2(self):
        self.bomberman.clearEnemies()
        self.board.setTileAt(2, 1, Tile.Oneal)
        self.board.setTileAt(1, 1, Tile.Empty)
        self.board.setTileAt(3, 1, Tile.Empty)
        self.board.setTileAt(2, 0, Tile.Empty)
        self.board.setTileAt(2, 2, Tile.Empty)

        tempList = [2, 1, 3, 9]
        self.bomberman.listEnemies.append(tempList)

        self.bomberman.numberEnemies = 1
        self.bomberman.listTypeEnemies[0] = 1

        self.board.moveEnemy(constant.SPEED_NORMAL)

        check = False
        if (self.board.tileAt(1, 1) == Tile.Oneal or self.board.tileAt(3, 1) == Tile.Oneal or self.board.tileAt(2, 0) == Tile.Oneal or self.board.tileAt(2, 2) == Tile.Oneal):
            check = True
        self.assertTrue(check, "Enemy did not move")

    def testMoveEnemyWithIntelligence3(self):
        self.bomberman.clearEnemies()
        self.board.setTileAt(2, 1, Tile.Kondoria)
        self.board.setTileAt(1, 1, Tile.Empty)
        self.board.setTileAt(3, 1, Tile.Empty)
        self.board.setTileAt(2, 0, Tile.Empty)
        self.board.setTileAt(2, 2, Tile.Empty)

        tempList = [2, 1, 3, 12]
        self.bomberman.listEnemies.append(tempList)

        self.bomberman.numberEnemies = 1
        self.bomberman.listTypeEnemies[0] = 1

        self.board.moveEnemy(constant.SPEED_SLOWEST)

        check = False
        if (self.board.tileAt(1, 1) == Tile.Kondoria or self.board.tileAt(3, 1) == Tile.Kondoria or self.board.tileAt(2, 0) == Tile.Kondoria or self.board.tileAt(2, 2) == Tile.Kondoria):
            check = True
        self.assertTrue(check, "Enemy did not move")

    def testDetonateBombKillsBomberman(self):
        self.bomberman.lives = 3
        self.board.bomberman.curX = 1
        self.board.bomberman.curY = 1
        self.board.bomberman.setBomberman()
        self.board.bomberman.setBomb()

        self.board.tryMove(1, 2)

        self.board.detonateBomb()

        self.assertEqual(2, self.bomberman.lives, "Bomberman did not lose a life when hit by a bomb")

    def testDeathWhenEnemyMovesToBomberman(self):
        self.bomberman.lives = 3
        self.board.bomberman.curX = 1
        self.board.bomberman.curY = 1
        self.board.bomberman.setBomberman()

        self.bomberman.clearEnemies()
        self.board.setTileAt(2, 1, Tile.Balloom)
        self.bomberman.numberEnemies = 1

        tempList = [2, 1, 3, 8]
        self.bomberman.listEnemies.append(tempList)

        self.bomberman.listTypeEnemies[0] = 1

        self.board.moveEnemy(constant.SPEED_SLOW)

        self.assertEqual(2, self.bomberman.lives, "Bomberman did not lose a life when an enemy moves into him")

    def testDeathWhenBombermanMovesToEnemy(self):
        self.bomberman.lives = 3
        self.board.bomberman.curX = 1
        self.board.bomberman.curY = 1
        self.board.bomberman.setBomberman()
        self.board.setTileAt(1, 2, Tile.Balloom)

        self.board.tryMove(1, 2)

        self.assertEqual(2, self.bomberman.lives, "Bomberman did not lose a life when he moves into an enemy")


if __name__ == '__main__':

    unittest.main()
    sys.exit(app.exec_)
