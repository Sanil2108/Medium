import pygame.draw as draw

class Player(object):
	init_x = 100
	init_y = 400

	jump_height = 250
	jump_speed = 5
	jump_speed_accel = 0

	def __init__(self):
		self.x = Player.init_x
		self.y = Player.init_y
		self.width = 50
		self.height = 50
		self.speed = 0
		self.color = (0, 0, 0)
		self.jumping = False

		self.current_jump_speed = 0

		self.inair = False

	def draw_it(self, display):
		draw.rect(display, self.color, (self.x, self.y, self.width, self.height))

	def get_x(self):
		return self.x

	def get_y(self):
		return self.y

	def update(self):
		self.x += self.speed
		if self.y >= Player.init_y:
			self.inair = False
		else:
			self.inair = True
		if(self.jumping):
			self.y -= Player.jump_speed
			self.current_jump_speed += Player.jump_speed_accel
			if self.y <= Player.init_y - Player.jump_height:
				self.jumping=False
		else:
			self.current_jump_speed -= Player.jump_speed_accel
			if self.y <= Player.init_y:
				self.y += Player.jump_speed

	def jump(self):
		self.current_jump_speed = Player.jump_speed
		self.inair = True
		if self.y >= Player.init_y:
			self.jumping = True

	def setSpeed(self, speed):
		self.speed = speed