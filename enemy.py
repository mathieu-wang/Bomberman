class Enemy(object):

    def __init__(self, points, speed, intelligence, wallpass, direction, canMove):
        self.points = points
        self.speed = speed
        self.intelligence = intelligence
        self.wallpass = wallpass
        self.direction = direction   # 0 - North, 1 - East, 2 - South, 3 - West
        self.canMove = canMove

    @staticmethod
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
