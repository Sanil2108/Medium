import pygame.draw as draw

class Enemy(object):
	init_x = 1000
	init_y = 450

	base = 25

	def __init__(self):
		self.scoreUpdated = False
		self.x = Enemy.init_x
		self.base = Enemy.base
		self.height = Enemy.base
		self.y = Enemy.init_y - self.height
		self.speed = -3
		self.color = (0, 0, 0)

	def draw_it(self, display):
		draw.polygon(display, self.color, [(self.x, self.y), (self.x-self.base/2, self.y+self.height), (self.x+self.base/2, self.y+self.height)])

	def get_x(self):
		return self.x

	def get_y(self):
		return self.y

	def update(self):
		self.x += self.speed

	def setSpeed(self, speed):
		self.speed = speed