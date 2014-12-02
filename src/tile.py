## This class stores tiles as stacks and provides methods for them.
class Tile(object):

    Empty = 0
    Concrete = 1
    Brick = 2
    Bomb = 3
    Bomberman = 4
    Powerup = 5
    Exit = 6
    Flash = 7
    Balloom = 8
    Oneal = 9
    Doll = 10
    Minvo = 11
    Kondoria = 12
    Ovapi = 13
    Pass = 14
    Pontan = 15

    def __init__(self):
        # Initialize a stack for a new tile.
        self.stack = [Tile.Empty]

    ## This method returns True if the tile on top of the stack is Empty.
    def isEmpty(self):
        return self.stack == [Tile.Empty]

    ## This method pushes a new tile on the stack.
    #  @param tile The tile to be pushed on the stack.
    def push(self, tile):
        self.stack.append(tile)

    ## This method returns the tile on the top of the stack.
    def peek(self):
        return self.stack[len(self.stack)-1]

    ## This methods removes the tile on top of the stack.
    def pop(self):
        return self.stack.pop()

    ## This method returns the number of tiles in the stack.
    def size(self):
        return len(self.stack)

    @staticmethod
    ## This element returns True if the topmost tile is Empty.
    #  @param tile the tile to be checked.
    def isEmpty(tile):
        return tile == Tile.Empty

    @staticmethod
    ## This element returns True if the topmost tile is Enemy.
    #  @param tile the tile to be checked.
    def isEnemy(tile):
        return 8 <= tile <=15

    @staticmethod
    ## This element returns True if the topmost tile is Bomberman.
    #  @param tile the tile to be checked.
    def isBomberman(tile):
        return tile == Tile.Bomberman

    @staticmethod
    ## This element returns True if the topmost tile is Exit.
    #  @param tile the tile to be checked.
    def isExit(tile):
        return tile == Tile.Exit

    @staticmethod
    ## This element returns True if the topmost tile is Powerup.
    #  @param tile the tile to be checked.
    def isPowerup(tile):
        return tile == Tile.Powerup