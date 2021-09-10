from ursina import *

class MenuButton(Button):
    def __init__(self, text='', ignore_paused = True, **kwargs):
        super().__init__(text, scale=(.25, .075), **kwargs)

        for key, value in kwargs.items():
            setattr(self, key ,value)
        self.was_hov = False

    def input(self, key):
        if key == 'left mouse down' and self.hovered:
            Audio('sfx/pop.wav', volume = .3, ignore_paused = True)




