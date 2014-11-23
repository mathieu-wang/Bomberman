class Bomberman(object):

	def __init__(self):
		self.lives = 3
		self.speed = 3
		self.numBombs = 1
		self.rangeOfBombs = 1
		self.wallPass = 0
		self.hasDetonator = 0
		self.bombPass = 0
		self.flamePass = 0
		self.invincible = 0

	@property
	def lives(self):
		return self.lives


	@lives.setter
	def lives(self, value):
			self.lives = value
	
	@property
	def speed(self):
		return self.speed

	@speed.setter
	def speed(self, value):
			self.speed = value
	
	@property
	def numBombs(self):
		return self.numBombs

	@numBombs.setter
	def numBombs(self, value):
			self.numBombs = value

	@property
	def rangeOfBombs(self):
		return self.rangeOfBombs

	@rangeOfBombs.setter
	def rangeOfBombs(self, value):
			self.rangeOfBombs = value
	
	@property
	def wallPass(self):
		return self.wallPass

	@wallPass.setter
	def wallPass(self, value):
			self.wallPass = value
	
	@property
	def hasDetonator(self):
		return self.hasDetonator

	@hasDetonator.setter
	def hasDetonator(self, value):
			self.hasDetonator = value
	
	@property
	def bombPass(self):
		return self.bombPass

	@bombPass.setter
	def bombPass(self, value):
			self.bombPass = value
	
	@property
	def flamePass(self):
		return self.flamePass

	@flamePass.setter
	def flamePass(self, value):
			self.flamePass = value

	@property
	def invincible(self):
		return self.invincible

	@invincible.setter
	def invincible(self, value):
			self.invincible = value