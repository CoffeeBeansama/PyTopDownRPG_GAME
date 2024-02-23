import pygame as pg
from player import Player
from camera import CameraGroup
from slime import Slime
from attack import PlayerAttack

class Level:
    def __init__(self):
        self.screen = pg.display.get_surface()

        self.visibleSprites = CameraGroup()
        self.playerAttackCollision = pg.sprite.Group()
        self.enemyCollision = pg.sprite.Group()

        self.player = Player((150,150),[self.visibleSprites],self.createPlayerAttack)
        self.slime = Slime((250,200),[self.visibleSprites,self.enemyCollision],self.player) 
        self.playerAttack = None


    def createPlayerAttack(self):
        self.playerAttack = PlayerAttack([self.playerAttackCollision],self.player)
        self.handlePlayerAttackCollision()

         
    def handlePlayerAttackCollision(self):
        for attack in self.playerAttackCollision:
            playerAttackConnect = pg.sprite.spritecollide(attack,self.enemyCollision,False)
            if playerAttackConnect:
               attack.playerHit(playerAttackConnect)
               self.playerAttack = None
               attack.kill()

    def update(self):
        self.visibleSprites.custom_draw(self.player)
        for sprite in self.visibleSprites:
            sprite.update()
