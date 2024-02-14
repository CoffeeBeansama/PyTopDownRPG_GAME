import pygame as pg
import sys
from level import Level
from eventhandler import EventHandler

class Game:
  def __init__(self):
      pg.init()
      windowSize = (700,500)
      
      self.screen = pg.display.set_mode(windowSize)

      self.FPS = 60

      self.clock = pg.time.Clock()

      pg.display.set_caption("COOL RPG GAME")
    
      self.fontColor = (255,255,255)
      self.font = pg.font.Font("Fonts/DeterminationMonoWebRegular-Z5oq.ttf",18)

      self.level = Level()
  

  def renderFPS(self):
      fps = self.font.render(f"{round(self.clock.get_fps())}",True,self.fontColor)
      pos = (670,10)
      self.screen.blit(fps,pos)


  def run(self):
      while True:
          for event in pg.event.get():
              if event.type == pg.QUIT:
                 pg.quit()
                 sys.exit()
              if event.type == pg.KEYDOWN:
                 if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()

          EventHandler.handlePlayerInput()
          self.screen.fill("black")
          self.renderFPS()                  
          self.level.update()
          pg.display.update()
          self.clock.tick(self.FPS)



if __name__ == "__main__":
   game = Game()
   game.run()
