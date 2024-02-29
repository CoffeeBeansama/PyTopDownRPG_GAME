import pygame as pg

class PlayerAttack(pg.sprite.Sprite):
    def __init__(self,group,player):
        super().__init__(group)

        self.sprite = pg.Surface((10,10))
        
        self.damage = player.attack

        self.positions = {
            "Up" : self.sprite.get_rect(midbottom=player.rect.midtop + pg.math.Vector2(0, 20)),
            "Down" : self.sprite.get_rect(midtop=player.rect.midbottom - pg.math.Vector2(0, 0)),
            "Left" : self.sprite.get_rect(midright=player.rect.midleft + pg.math.Vector2(12, 10)),
            "Right" : self.sprite.get_rect(midleft=player.rect.midright - pg.math.Vector2(12, -10))
        }

        for playerDirection in ["Up","Down","Right","Left"]:
            if playerDirection in player.currentState:
               self.rect = self.positions.get(playerDirection)

    def playerHit(self,enemies):
        for enemy in enemies:
            if hasattr(enemy,"takeDamage"):
               enemy.takeDamage(self.damage)
            
        
