import unittest
from board import Board
from game import Game
from PyQt4 import QtCore, QtGui

class TestBoard(unittest.TestCase):

    def setUp(self):
        self.app = QtGui.QApplication([])
        self.game = Game()
        self.board = Board(self.game)

    def test_setTileAt(self):
        pass

    def test_setBomb(self):
        pass

    def test_detonateBombHasNoEffectOnConcrete(self):
        pass

    def test_detonateBombDestroysBrick(self):
        pass

    def test_detonateBombDestroysMultipleBricks(self):
        pass

    def test_detonateBombDestroysOnlyClosestBrickInTheSameDirection(self):
        pass

    def test_tileAt(self):
        pass

    def test_tryMove(self):
        pass

if __name__ == '__main__':
    unittest.main()