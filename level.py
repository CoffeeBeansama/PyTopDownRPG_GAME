import pygame as pg
from player import Player
from camera import CameraGroup

class Level:
    def __init__(self):
        self.screen = pg.display.get_surface()
        self.visibleSprites = CameraGroup()
        self.player = Player((150,150),self.visibleSprites)


    def update(self):
        self.visibleSprites.custom_draw(self.player)
        self.player.update()
