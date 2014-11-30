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

    def test_initialize_board_with_concrete_walls(self):
        self.assertEqual(self.board.bomberman.board[0][0].peek(), Tile.Concrete, "Corner tile should be Concrete, board not initialized properly")

    def test_initialize_board_with_exactly_one_bomberman(self):
        number_of_bomberman_on_the_board = 0
        board = self.board.bomberman.board
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j].peek() == Tile.Bomberman:
                    number_of_bomberman_on_the_board += 1

        self.assertEqual(number_of_bomberman_on_the_board, 1, "Did not see exactly one bomberman on the board")

    def test_setTileAt(self):
        self.assertEqual(self.board.bomberman.board[1][1].peek(), Tile.Empty)
        self.board.setTileAt(1, 1, Tile.Brick)
        self.assertEqual(self.board.bomberman.board[1][1].peek(), Tile.Brick)

    def test_tileAt(self):
        for i in range(len(self.board.bomberman.board)):
            for j in range(len(self.board.bomberman.board[i])):
                self.assertEqual(self.board.tileAt(j, i), self.board.bomberman.board[i][j].peek())

    def test_setBomberman(self):
        self.assertNotEqual(self.board.tileAt(1, 2), Tile.Bomberman)
        self.board.bomberman.curX = 1
        self.board.bomberman.curY = 2
        self.board.bomberman.setBomberman()
        self.assertEqual(self.board.tileAt(1, 2), Tile.Bomberman)

    def test_setBomb(self):
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

    def test_detonateBomb(self):
        self.board.bomberman.curX = 1
        self.board.bomberman.curY = 1
        self.board.bomberman.setBomberman()
        self.board.bomberman.setBomb()

        self.board.detonateBomb()

        self.board.popTileAt(1, 1) #pop Bomberman
        self.assertNotEqual(self.board.tileAt(1, 1), Tile.Bomb, "Bomb did not explode")

    def test_detonateBomb_has_no_effect_on_concrete(self):
        self.board.curX = 1
        self.board.curY = 1
        self.board.bomberman.setBomberman()
        self.board.bomberman.setBomb()

        self.board.detonateBomb()

        self.board.popTileAt(1, 1) #pop Bomberman
        self.assertEqual(self.board.tileAt(1, 0), Tile.Concrete, "Concrete got destroyed by bomb")

    def test_detonateBomb_destroys_brick(self):
        self.board.setTileAt(1, 3, Tile.Brick)
        self.board.bomberman.curX = 1
        self.board.bomberman.curY = 1
        self.board.bomberman.setBomberman()
        self.board.bomberman.setBomb()

        self.board.detonateBomb()

        self.assertEqual(self.board.tileAt(1, 2), Tile.Empty, "Brick did not get destroyed by bomb")

    def test_detonateBomb_destroys_multiple_bricks(self):
        self.board.setTileAt(1, 2, Tile.Brick)
        self.board.setTileAt(1, 3, Tile.Brick)
        self.board.bomberman.curX = 1
        self.board.bomberman.curY = 1
        self.board.bomberman.setBomberman()
        self.board.bomberman.setBomb()

        self.board.detonateBomb()

        self.assertEqual(self.board.tileAt(1, 2), Tile.Empty, "Closer Brick did not get destroyed by bomb")
        self.assertEqual(self.board.tileAt(1, 3), Tile.Brick, "Further Brick got destroyed by bomb")

    def test_detonateBomb_destroys_only_closest_brick_in_the_same_direction(self):
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


    def test_try_move_to_concrete(self):
        self.board.setTileAt(0, 0, Tile.Concrete)
        self.assertFalse(self.board.tryMove(0, 0), "Was able to move to a concrete tile")

    def test_try_move_to_brick(self):
        self.board.setTileAt(1, 1, Tile.Brick)
        self.assertFalse(self.board.tryMove(1, 1), "Was able to move to a brick tile")

    def test_try_move_to_brick(self):
        self.board.setTileAt(2, 2, Tile.Empty)
        self.assertTrue(self.board.tryMove(2, 2), "Was not able to move to an empty tile")

if __name__ == '__main__':

    unittest.main()
    sys.exit(app.exec_)
