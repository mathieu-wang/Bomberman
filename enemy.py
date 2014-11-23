class Enemy(object):

    def __init__(self, points, speed, intelligence, wallpass):
        self.points = points
        self.speed = speed
        self.intelligence = intelligence
        self.wallpass = wallpass

    @staticmethod
    def getEnemy(type):
        if type == 8:
            return Balloom()
        if type == 9:
            return Oneal()
        if type == 10:
            return Doll()
        if type == 11:
            return Minvo()
        if type == 12:
            return Kondoria()
        if type == 13:
            return Ovapi()
        if type == 14:
            return Pass()
        if type == 15:
            return Pontan()


class Balloom(Enemy):

    def __init__(self):
        super(Balloom, self).__init__(100, 2, 1, False)

class Oneal(Enemy):

    def __init__(self):
        super(Oneal, self).__init__(200, 3, 2, False)

class Doll(Enemy):

    def __init__(self):
        super(Doll, self).__init__(400, 3, 1, False)

class Minvo(Enemy):

    def __init__(self):
        super(Minvo, self).__init__(800, 4, 2, False)

class Kondoria(Enemy):

    def __init__(self):
        super(Kondoria, self).__init__(1000, 1, 3, True)

class Ovapi(Enemy):

    def __init__(self):
        super(Ovapi, self).__init__(2000, 2, 2, True)

class Pass(Enemy):

    def __init__(self):
        super(Pass, self).__init__(4000, 4, 3, False)

class Pontan(Enemy):

    def __init__(self):
        super(Pontan, self).__init__(8000, 4, 3, True)
