from ursina import *

class Field(Entity):
	def __init__(self, position, texture, shader):
		super().__init__(
			model = 'cube',
			scale = Vec3(2,.1,100),
			position = position,
			texture = texture,
			collider = 'box',
			eternal = True,
			shader = shader,
			)