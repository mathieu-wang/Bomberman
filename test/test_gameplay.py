import unittest
import sys

from PyQt4 import QtGui

from src.board import Board
from src.level import Level
from src.tile import Tile
from src.game import Game
from src.enemy import Enemy
from src import constant

class TestGameplay(unittest.TestCase):
    app = None

    @classmethod
    def setUpClass(cls):
        global app
        app = QtGui.QApplication([])

    def setUp(self):
        self.game = Game()
        self.level = Level("testUser", 1)
        self.board = Board(self.level, self.game)
        self.board.start()

    def tearDown(self):
        self.board.destroy()
        self.game.destroy()

    @classmethod
    def tearDownClass(cls):
        app.quit()

    def testInitializeBoardWithConcreteWalls(self):
        self.assertEqual(self.board.level.board[0][0].peek(), Tile.Concrete, "Corner tile should be Concrete, board not initialized properly")

    def testInitializeBoardWithExactlyOneBomberman(self):
        numberOfBombermanOnTheBoard = 0
        board = self.board.level.board
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j].peek() == Tile.Bomberman:
                    numberOfBombermanOnTheBoard += 1

        self.assertEqual(numberOfBombermanOnTheBoard, 1, "Did not see exactly one level on the board")

    def testSetTileAt(self):
        self.assertEqual(self.board.level.board[1][1].peek(), Tile.Empty)
        self.board.setTileAt(1, 1, Tile.Brick)
        self.assertEqual(self.board.level.board[1][1].peek(), Tile.Brick)

    def testTileAt(self):
        for i in range(len(self.board.level.board)):
            for j in range(len(self.board.level.board[i])):
                self.assertEqual(self.board.tileAt(j, i), self.board.level.board[i][j].peek())

    def testSetBomberman(self):
        self.assertNotEqual(self.board.tileAt(1, 2), Tile.Bomberman)
        self.board.level.bomberman.curX = 1
        self.board.level.bomberman.curY = 2
        self.board.level.setBomberman()
        self.assertEqual(self.board.tileAt(1, 2), Tile.Bomberman)

    def testSetBomb(self):
        self.assertNotEqual(self.board.tileAt(1, 2), Tile.Bomb)
        self.board.level.bomberman.curX = 1
        self.board.level.bomberman.curY = 2
        self.board.level.setBomberman() #level should be here already
        self.board.level.setBomb()

        self.assertEqual(len(self.board.level.bombQueue), 1, "Bomb did not get enqueued")
        self.assertEqual(self.board.level.bombQueue.pop(), (1, 2, constant.TIME_BOMB), "Bomb's coordinates are wrong")
        self.assertEqual(self.board.tileAt(1, 2), Tile.Bomberman, "Bomberman is not on top of a bomb")

        self.board.popTileAt(1, 2)
        self.assertEqual(self.board.tileAt(1, 2), Tile.Bomb, "There is no bomb underneath Bomberman")

    def testDetonateBomb(self):
        self.board.level.bomberman.curX = 1
        self.board.level.bomberman.curY = 1
        self.board.level.setBomberman()
        self.board.level.setBomb()

        self.board.detonateBomb()

        self.board.popTileAt(1, 1) #pop Bomberman
        self.assertNotEqual(self.board.tileAt(1, 1), Tile.Bomb, "Bomb did not explode")

    def testDetonateBombHasNoEffectOnConcrete(self):
        self.board.curX = 1
        self.board.curY = 1
        self.board.level.setBomberman()
        self.board.level.setBomb()

        self.board.detonateBomb()

        self.board.popTileAt(1, 1) #pop Bomberman
        self.assertEqual(self.board.tileAt(1, 0), Tile.Concrete, "Concrete got destroyed by bomb")

    def testDetonateBombDestroysBrick(self):
        self.board.setTileAt(1, 2, Tile.Brick)
        self.board.level.bomberman.curX = 1
        self.board.level.bomberman.curY = 1
        self.board.level.setBomberman()
        self.board.level.setBomb()
        
        self.board.level.bomberman.rangeOfBombs = 3

        self.board.detonateBomb()

        self.assertEqual(self.board.tileAt(1, 2), Tile.Empty, "Brick did not get destroyed by bomb")

    def testDetonateBombDestroysOnlyClosestBrickInTheSameDirection(self):
        self.board.setTileAt(1, 2, Tile.Brick)
        self.board.setTileAt(1, 3, Tile.Brick)
        self.board.level.bomberman.curX = 1
        self.board.level.bomberman.curY = 1
        self.board.level.setBomberman()
        self.board.level.setBomb()

        self.board.level.bomberman.rangeOfBombs = 3

        self.board.detonateBomb()

        self.assertEqual(self.board.tileAt(1, 2), Tile.Empty, "Closer Brick did not get destroyed by bomb")
        self.assertEqual(self.board.tileAt(1, 3), Tile.Brick, "Further Brick got destroyed by bomb")

    def testDetonateBombDestroysMultipleBricks(self):
        self.board.setTileAt(1, 2, Tile.Brick)
        self.board.setTileAt(2, 1, Tile.Brick)
        self.board.level.bomberman.curX = 1
        self.board.level.bomberman.curY = 1
        self.board.level.setBomberman()
        self.board.level.setBomb()

        self.board.level.bomberman.rangeOfBombs = 3

        self.board.detonateBomb()

        self.assertEqual(self.board.tileAt(1, 2), Tile.Empty, "One of the Bricks did not get destroyed by bomb")
        self.assertEqual(self.board.tileAt(2, 1), Tile.Empty, "One of the Bricks did not get destroyed by bomb")

    def testDetonateBombKillsEnemies(self):
        self.level.clearEnemies()
        self.board.setTileAt(2, 1, Tile.Balloom)
        self.board.level.bomberman.curX = 1
        self.board.level.bomberman.curY = 1
        self.board.level.setBomberman()
        self.board.level.setBomb()

        tempList = [2, 1, constant.DIRECTION_WEST, Tile.Balloom]
        self.level.listEnemies.append(tempList)

        self.level.numberEnemies = 1
        self.level.listTypeEnemies[0] = 1
        self.board.level.bomberman.rangeOfBombs = 3

        self.board.detonateBomb()

        self.assertEqual(self.board.tileAt(2, 1), Tile.Empty, "Bomb detonation did not kill enemy")
        self.assertEqual(0, self.level.numberEnemies, "Enemy was not removed from map")

    def testDetonateBombSpawnsEnemiesWhenExitIsHit(self):
        self.board.setTileAt(1, 2, Tile.Exit)

        self.board.level.bomberman.curX = 1
        self.board.level.bomberman.curY = 1
        self.board.level.setBomberman()
        self.board.level.setBomb()

        self.board.level.bomberman.rangeOfBombs = 3

        self.board.detonateBomb()

        count = 0

        for i in range(self.level.numberEnemies):
            if (self.level.listTypeEnemies[i] != 0):
                count += 1

        self.assertEqual(count, 1, "Not all enemies are the same type when the exit is hit")
        self.assertEqual(len(self.level.listEnemies), 8, "The number of enemies when the exit is hit is not 8")

    def testDetonateBombSpawnsEnemiesWhenPowerupIsHit(self):
        self.board.setTileAt(1, 2, Tile.Powerup)

        self.board.level.bomberman.curX = 1
        self.board.level.bomberman.curY = 1
        self.board.level.setBomberman()
        self.board.level.setBomb()

        self.board.level.bomberman.rangeOfBombs = 3

        self.board.detonateBomb()

        count = 0

        for i in range(self.level.numberEnemies):
            if (self.level.listTypeEnemies[i] != 0):
                count += 1

        self.assertEqual(count, 1, "Not all enemies are the same type when the powerup is hit")
        self.assertEqual(len(self.level.listEnemies), 8, "The number of enemies when the powerup is hit is not 8")

    def testTimeRunsOut(self):
        self.level.timeLeft = 0
        self.level.timeDone = False
        self.board.timeoutEvent()

        check = False

        for i in range(7):
            if (self.level.listTypeEnemies[i] != 0):
                check = True

        self.assertEqual(self.level.numberEnemies, 8, "Number of enemies is not equal to 8")
        self.assertFalse(check, "At least one enemy is not a Pontan")


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
        self.level.clearEnemies()
        self.board.setTileAt(2, 1, Tile.Balloom)
        self.board.setTileAt(1, 1, Tile.Empty)

        tempList = [2, 1, constant.DIRECTION_WEST, Tile.Balloom]
        self.level.listEnemies.append(tempList)

        self.level.numberEnemies = 1
        self.level.listTypeEnemies[0] = 1

        self.board.moveEnemy(constant.SPEED_SLOW)

        self.assertEqual(self.board.tileAt(1, 1), Tile.Balloom, "Enemy did not move")
        
    def testMoveEnemyWithIntelligence2(self):
        self.level.clearEnemies()
        self.board.setTileAt(2, 1, Tile.Oneal)
        self.board.setTileAt(1, 1, Tile.Empty)
        self.board.setTileAt(3, 1, Tile.Empty)
        self.board.setTileAt(2, 0, Tile.Empty)
        self.board.setTileAt(2, 2, Tile.Empty)

        tempList = [2, 1, constant.DIRECTION_WEST, Tile.Oneal]
        self.level.listEnemies.append(tempList)

        self.level.numberEnemies = 1
        self.level.listTypeEnemies[0] = 1

        self.board.moveEnemy(constant.SPEED_NORMAL)

        check = False
        if (self.board.tileAt(1, 1) == Tile.Oneal or self.board.tileAt(3, 1) == Tile.Oneal or self.board.tileAt(2, 0) == Tile.Oneal or self.board.tileAt(2, 2) == Tile.Oneal):
            check = True
        self.assertTrue(check, "Enemy did not move")

    def testMoveEnemyWithIntelligence3(self):
        self.level.clearEnemies()
        self.board.setTileAt(2, 1, Tile.Kondoria)
        self.board.setTileAt(1, 1, Tile.Empty)
        self.board.setTileAt(3, 1, Tile.Empty)
        self.board.setTileAt(2, 0, Tile.Empty)
        self.board.setTileAt(2, 2, Tile.Empty)

        tempList = [2, 1, constant.DIRECTION_WEST, Tile.Kondoria]
        self.level.listEnemies.append(tempList)

        self.level.numberEnemies = 1
        self.level.listTypeEnemies[0] = 1

        self.board.moveEnemy(constant.SPEED_SLOWEST)

        check = False
        if (self.board.tileAt(1, 1) == Tile.Kondoria or self.board.tileAt(3, 1) == Tile.Kondoria or self.board.tileAt(2, 0) == Tile.Kondoria or self.board.tileAt(2, 2) == Tile.Kondoria):
            check = True
        self.assertTrue(check, "Enemy did not move")

    def testDetonateBombKillsBomberman(self):
        self.level.lives = 3
        self.board.level.bomberman.curX = 1
        self.board.level.bomberman.curY = 1
        self.board.level.setBomberman()
        self.board.level.setBomb()

        self.board.tryMove(1, 2)

        self.board.detonateBomb()

        self.assertEqual(2, self.level.bomberman.lives, "Bomberman did not lose a life when hit by a bomb")

    def testDeathWhenEnemyMovesToBomberman(self):
        self.level.lives = 3
        self.board.level.bomberman.curX = 1
        self.board.level.bomberman.curY = 1
        self.board.level.setBomberman()

        self.level.clearEnemies()
        self.board.setTileAt(2, 1, Tile.Balloom)
        self.level.numberEnemies = 1

        tempList = [2, 1, constant.DIRECTION_WEST, Tile.Balloom]
        self.level.listEnemies.append(tempList)

        self.level.listTypeEnemies[0] = 1

        self.board.moveEnemy(constant.SPEED_SLOW)

        self.assertEqual(2, self.level.bomberman.lives, "Bomberman did not lose a life when an enemy moves into him")

    def testDeathWhenBombermanMovesToEnemy(self):
        self.level.lives = 3
        self.board.level.bomberman.curX = 1
        self.board.level.bomberman.curY = 1
        self.board.level.setBomberman()
        self.board.setTileAt(1, 2, Tile.Balloom)

        self.board.tryMove(1, 2)

        self.assertEqual(2, self.level.bomberman.lives, "Bomberman did not lose a life when he moves into an enemy")

    def testGetScoreOfKilledEnemies(self):
        # No enemies:
        enemies = [[], [], []]
        self.assertEquals(self.board.getScoreOfKilledEnemies(enemies), 0)

        # 1 enemy at distance 1, with bomb range 1
        enemies = [[Tile.Balloom]]
        self.assertEqual(self.board.getScoreOfKilledEnemies(enemies), Enemy.getEnemy(Tile.Balloom)['points'])

        # 1 enemy at distance 1, with bomb range >1
        enemies = [[Tile.Balloom], [], []]
        self.assertEqual(self.board.getScoreOfKilledEnemies(enemies), Enemy.getEnemy(Tile.Balloom)['points'])

        # 1 enemy at distance >1
        enemies = [[], [Tile.Balloom], []]
        self.assertEqual(self.board.getScoreOfKilledEnemies(enemies), Enemy.getEnemy(Tile.Balloom)['points'])

        # 2 enemies at different distance
        enemies = [[Tile.Balloom], [], [Tile.Doll]]
        self.assertEqual(self.board.getScoreOfKilledEnemies(enemies), Enemy.getEnemy(Tile.Balloom)['points'] + 2*Enemy.getEnemy(Tile.Doll)['points'])

        # 2 enemies at same distance
        enemies = [[Tile.Doll, Tile.Balloom], [], []]
        self.assertEqual(self.board.getScoreOfKilledEnemies(enemies), Enemy.getEnemy(Tile.Balloom)['points'] + 2*Enemy.getEnemy(Tile.Doll)['points'])

        # multiple enemies at multiple distances
        enemies = [[Tile.Doll, Tile.Balloom, Tile.Doll], [], [Tile.Ovapi, Tile.Ovapi], [Tile.Pontan]]
        self.assertEqual(self.board.getScoreOfKilledEnemies(enemies), Enemy.getEnemy(Tile.Balloom)['points']
                                                                    + 2*Enemy.getEnemy(Tile.Doll)['points']
                                                                    + 4*Enemy.getEnemy(Tile.Doll)['points']
                                                                    + 8*Enemy.getEnemy(Tile.Ovapi)['points']
                                                                    + 16*Enemy.getEnemy(Tile.Ovapi)['points']
                                                                    + 32*Enemy.getEnemy(Tile.Pontan)['points'])



        enemies = [[Tile.Balloom, Tile.Oneal], [], [Tile.Doll]]


if __name__ == '__main__':

    unittest.main()
    sys.exit(app.exec_)
