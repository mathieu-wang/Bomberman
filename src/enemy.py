## This class stores the types of enemies and how many there are in each level.
class Enemy(object):

    def __init__(self, points, speed, intelligence, wallpass, direction, canMove):
        self.points = points
        self.speed = speed
        self.intelligence = intelligence
        self.wallpass = wallpass
        self.direction = direction   # 0 - North, 1 - East, 2 - South, 3 - West
        self.canMove = canMove

    @staticmethod
    ## This method is a dictionary that returns information for the different enemy types.
    #  @parim type The type of enemy for which information will be returned.
    #  The information that can be returned is the enemies' points, speed, intelligence,
    #  wallpass and direction.
    def getEnemy(type):
        if type == 8:
            return dict(points=100, speed=2, intelligence=1, wallpass=False, direction=0)
        if type == 9:
            return dict(points=200, speed=3, intelligence=2, wallpass=False, direction=0)
        if type == 10:
            return dict(points=400, speed=3, intelligence=1, wallpass=False, direction=0)
        if type == 11:
            return dict(points=800, speed=4, intelligence=2, wallpass=False, direction=0)
        if type == 12:
            return dict(points=1000, speed=1, intelligence=3, wallpass=True, direction=0)
        if type == 13:
            return dict(points=2000, speed=2, intelligence=2, wallpass=True, direction=0)
        if type == 14:
            return dict(points=4000, speed=4, intelligence=3, wallpass=False, direction=0)
        if type == 15:
            return dict(points=8000, speed=4, intelligence=3, wallpass=True, direction=0)

    @staticmethod
    ## This method returns a list of the number of each enemy and the powerup for each level.
    #  @parim level The level for which information is to be returned. 
    def getEnemyListAndPowerUp(level):
        if level == 1:
            NumEnemies = [6, 0, 0, 0, 0, 0, 0, 0]
            Powerup = 2
        elif level == 2:
            NumEnemies = [3, 3, 0, 0, 0, 0, 0, 0]
            Powerup = 1
        elif level == 3:
            NumEnemies = [2, 2, 2, 0, 0, 0, 0, 0]
            Powerup = 5
        elif level == 4:
            NumEnemies = [1, 1, 2, 2, 0, 0, 0, 0]
            Powerup = 3
        elif level == 5:
            NumEnemies = [0, 0, 4, 3, 0, 0, 0, 0]
            Powerup = 1
        elif level == 6:
            NumEnemies = [0, 2, 3, 2, 0, 0, 0, 0]
            Powerup = 1
        elif level == 7:
            NumEnemies = [0, 2, 3, 0, 2, 0, 0, 0]
            Powerup = 2
        elif level == 8:
            NumEnemies = [0, 1, 2, 4, 0, 0, 0, 0]
            Powerup = 5
        elif level == 9:
            NumEnemies = [0, 1, 1, 4, 1, 0, 0, 0]
            Powerup = 6
        elif level == 10:
            NumEnemies = [0, 1, 1, 1, 3, 1, 0, 0]
            Powerup = 4
        elif level == 11:
            NumEnemies = [0, 1, 2, 3, 1, 1, 0, 0]
            Powerup = 1
        elif level == 12:
            NumEnemies = [0, 1, 1, 1, 4, 1, 0, 0]
            Powerup = 1
        elif level == 13:
            NumEnemies = [0, 0, 3, 3, 3, 0, 0, 0]
            Powerup = 5
        elif level == 14:
            NumEnemies = [0, 0, 0, 0, 0, 7, 1, 0]
            Powerup = 6
        elif level == 15:
            NumEnemies = [0, 0, 1, 3, 3, 0, 1, 0]
            Powerup = 2
        elif level == 16:
            NumEnemies = [0, 0, 0, 3, 4, 0, 1, 0]
            Powerup = 4

        return NumEnemies, Powerup
