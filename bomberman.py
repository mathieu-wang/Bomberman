class Bomberman(object):

    def __init__(self):
        self._lives = 3
        self._speed = 3
        self._numBombs = 1
        self._rangeOfBombs = 1
        self._wallPass = 0
        self._hasDetonator = 0
        self._bombPass = 0
        self._flamePass = 0
        self._invincible = 0

    @property
    def lives(self):
        return self._lives

    @lives.setter
    def lives(self, value):
        self._lives = value
    
    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = value
    
    @property
    def numBombs(self):
        return self._numBombs

    @numBombs.setter
    def numBombs(self, value):
        self._numBombs = value

    @property
    def rangeOfBombs(self):
        return self._rangeOfBombs

    @rangeOfBombs.setter
    def rangeOfBombs(self, value):
        self._rangeOfBombs = value
    
    @property
    def wallPass(self):
        return self._wallPass

    @wallPass.setter
    def wallPass(self, value):
        self._wallPass = value
    
    @property
    def hasDetonator(self):
        return self._hasDetonator

    @hasDetonator.setter
    def hasDetonator(self, value):
        self._hasDetonator = value
    
    @property
    def bombPass(self):
        return self._bombPass

    @bombPass.setter
    def bombPass(self, value):
        self._bombPass = value
    
    @property
    def flamePass(self):
        return self._flamePass

    @flamePass.setter
    def flamePass(self, value):
        self._flamePass = value

    @property
    def invincible(self):
        return self._invincible

    @invincible.setter
    def invincible(self, value):
        self._invincible = value