from ursina import *

class Star(Sprite):
	def __init__(self, position, texture):
		super().__init__(
			texture = texture,
			position = position,
			eternal = True,
			scale = .1,
			)