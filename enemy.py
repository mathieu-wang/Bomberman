from tile import Tile

class Enemy(Tile):

    def __init__(self, points, speed, intelligence, wallpass):
        super(Tile, self).__init__()
        self.points = points
        self.speed = speed
        self.intelligence = intelligence
        self.wallpass = wallpass

class Balloom(Enemy):

    def __init__(self):
        super(Enemy, self).__init__(100, 2, 1, False)

class Oneal(Enemy):

    def __init__(self):
        super(Enemy, self).__init__(200, 3, 2, False)

class Doll(Enemy):

    def __init__(self):
        super(Enemy, self).__init__(400, 3, 1, False)

class Minvo(Enemy):

    def __init__(self):
        super(Enemy, self).__init__(800, 4, 2, False)

class Kondoria(Enemy):

    def __init__(self):
        super(Enemy, self).__init__(1000, 1, 3, True)

class Ovapi(Enemy):

    def __init__(self):
        super(Enemy, self).__init__(2000, 2, 2, True)

class Pass(Enemy):

    def __init__(self):
        super(Enemy, self).__init__(4000, 4, 3, False)

class Pontan(Enemy):

    def __init__(self):
        super(Enemy, self).__init__(8000, 4, 3, True)