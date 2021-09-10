from ursina import *

class Coin(Entity):
	def __init__(self, position, shader, texture):
		super().__init__(
			model = 'coin',
			scale = (.6,.6,.1),
			position = position,
			texture = texture,
			eternal = True,
			collider = 'box',
			shader = shader,
			)
		self.run = False
		self.hit_info = self.intersects()
		self.hit = False
	#	self.light = SpotLight(parent = self, shadows = True, color = color.white, eternal = True)

	def update(self):
		self.hit_info = self.intersects()
		if self.hit_info.hit and self.z < 70:
			self.hit = True
		if self.run:
			self.z -= 25 * time.dt
		'''if self.light.z <= -100:
			self.light.eternal = False

		self.light.position = self.position'''