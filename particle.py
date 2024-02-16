import pygame as pg
from timer import Timer
from support import import_folder

class DustParticle(pg.sprite.Sprite):
  def __init__(self,group):
      super().__init__(group)

      self.pos = (-9999,-9999)
      self.spritePath = "Sprites/Particles/"
      self.sprite = pg.image.load(f"{self.spritePath}00.png").convert_alpha()
      self.rect = self.sprite.get_rect(topleft=(self.pos))
      self.hitbox = self.rect.inflate(0,0)      

      self.spriteList = import_folder(self.spritePath)
    

      self.frame_index = 0
      self.animationTime = 1 / 8
      
      self.createParticle = False

  def handleAnimation(self):
      self.frame_index += self.animationTime

      if self.frame_index >= len(self.spriteList):
          self.frame_index = 0
          self.resetParticle() 
        
      self.sprite = self.spriteList[int(self.frame_index)]
  
  def resetParticle(self):
      self.rect.center = self.pos

  def startParticle(self,pos):
      self.createParticle = True
      self.frame_index = 0
      self.rect.center = pos

  def update(self):
      if not self.createParticle: return

      self.handleAnimation()

      
