from ursina import *
from random import randint

class Player(Entity):
	def __init__(self, shader):
		super().__init__(
			model = 'cube',
			scale = Vec3(1,2,1),
			collider = 'box',
			position = (0,0,0),
			eternal = True,
			shader = shader,
			)
		self.in_air = False
		self.in_air_two = False
		self.landing = False
		self.j_right = False
		self.j_left = False
		self.j_mid = False
		self.coins = 0
		self.start = False
		self.change_camera = False
		self.show_fps = True
		self.j_velocity = .14

	def jump(self):
		self.in_air = True

	def double_jump(self):
		self.in_air_two = True

	def jump_left(self):
		self.in_air = True
		self.j_left = True

	def jump_right(self):
		self.in_air = True	
		self.j_right = True

	def jump_mid(self):
		self.in_air = True
		self.j_mid = True

	def update(self):

		if self.in_air:
			
			if self.j_right and self.x < 4:
				self.j_velocity = .3
				self.x += .4

			elif self.j_left and self.x > -4:
				self.j_velocity = .3
				self.x -= .4

			elif self.j_mid and round(self.x,1) > 0.0:
				self.j_velocity = .3
				self.x -= .4
			elif self.j_mid and round(self.x,1) < 0:
				self.j_velocity = .3
				self.x += .4

			else:
				self.j_right = False
				self.j_left = False
				self.j_mid = False
				self.j_velocity = .14

			if round(self.y) <= 2.5 and self.landing == False:
				self.y += self.j_velocity
			if round(self.y) >= 2.5 and self.landing == False and self.in_air_two == False:
				self.landing = True
			if self.landing:
				self.y -= .1
			if round(self.y,1) == 0.0 or round(self.y,1) == -0.0:
				self.in_air = False
				self.landing = False
				self.in_air_two = False

			if self.in_air_two:
				self.landing = False

			if self.in_air_two:
				if round(self.y,1) <= 4.4 and self.landing == False:
					self.y += .18
				if round(self.y,1) >= 4.4 and self.landing == False:
					self.landing = True
					self.in_air_two = False

			print(round(self.y))

		'''if self.jumping:
			if round(self.y, 1) != 2.0:
				self.y += .2 # setting
			if self.jleft and round(self.x, 1) > -2.2:
				self.x -= .2 # setting
			if self.jright and round(self.x, 1) < 2.2:
				self.x += .2 # setting

		if self.jumping and round(self.y, 1) == 2.0:
			self.jumping = False
			self.landing2 = True

		if self.landing2:
			if round(self.y, 1) > 0.0:
				self.y -= .2 # setting
			if self.jleft and round(self.x, 1) > -4.0:
				self.x -= .2 # setting
			if self.jright and round(self.x, 1) < 4.0:
				self.x += .2 # setting

		if self.landing2 and round(self.y, 1) == 0.0:
			self.landing2 = False
			self.jleft = False
			self.jright = False'''
