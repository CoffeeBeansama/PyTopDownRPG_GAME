import pygame as pg
from player import Player
from camera import CameraGroup
from slime import Slime


class Level:
    def __init__(self):
        self.screen = pg.display.get_surface()
        self.visibleSprites = CameraGroup()
        self.player = Player((150,150),[self.visibleSprites])
        self.slime = Slime((250,200),self.visibleSprites,self.player)

    def update(self):
        self.visibleSprites.custom_draw(self.player)
        for sprite in self.visibleSprites:
            sprite.update()
