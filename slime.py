import pygame as pg
from support import import_folder

class Slime(pg.sprite.Sprite):
    def __init__(self,pos,group,player):
        super().__init__(group)
        self.pos = pos
        self.player = player
        
        self.maxHP = 10
        self.currentHP = self.maxHP

        self.initializeSprites()
        
        self.direction = pg.math.Vector2()
        self.speed = 1

        self.chaseRadius = 70
        self.attackRadius = 25

        self.currentState = "Idle"

        self.stateCache = {
            "Idle" : self.idleState,
            "Chase" : self.chaseState,
            "Attack" : self.attackState,
            "Hurt" : self.hurtState,
            "Death" : self.deathState
        }

        self.frame_index = 0
        self.animationTime = 1 / 8

    def initializeSprites(self): 
        self.spritePath = "Sprites/Slime/"
        self.sprite = pg.image.load(f"{self.spritePath}Idle/00.png").convert_alpha()
        self.rect = self.sprite.get_rect(topleft=(self.pos))
        self.hitbox = self.rect.inflate(0,0)
    
        self.animationStates = {
            "Idle" : [], "Chase" : [], "Attack" : [], "Hurt" : [],
            "Death" : []
        }

        for animations in self.animationStates.keys():
            fullPath = self.spritePath + animations
            self.animationStates[animations] = import_folder(fullPath)

    def getPlayerDistance(self):
         enemy_vec = pg.math.Vector2(self.rect.center)
         player_vec = pg.math.Vector2(self.player.rect.center)
         distance = (player_vec - enemy_vec).magnitude()
         return distance

    def getPlayerPosition(self):
        enemy_vec = pg.math.Vector2(self.rect.center)
        player_vec = pg.math.Vector2(self.player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()
        if distance > 0:
           playerPosition = (player_vec - enemy_vec).normalize()
        return playerPosition
    

    def switchState(self,newState):
        self.currentState = newState
        self.frame_index = 0

    def idleState(self):        
        if self.getPlayerDistance() <= self.chaseRadius:
           self.switchState("Chase")

    def chaseState(self):
        self.direction = self.getPlayerPosition()

        if self.getPlayerDistance() >= self.chaseRadius:
           self.direction = pg.math.Vector2()
           self.switchState("Idle")

        if self.getPlayerDistance() <= self.attackRadius:
           self.switchState("Attack") 

    def attackState(self):
        self.direction = pg.math.Vector2()
        if self.getPlayerDistance() >= self.attackRadius + 5:
           self.switchState("Chase")

    def hurtState(self):
        pass

    def deathState(self):
        pass
    
    
    def handleMovement(self):
        self.hitbox.x += self.direction.x * self.speed
        self.hitbox.y += self.direction.y * self.speed
        self.rect.center = self.hitbox.center    

    def handleSpriteRotation(self):
        if self.player.rect.centerx < self.rect.centerx:
           return pg.transform.flip(self.sprite,True,False)
        else:
           return pg.transform.flip(self.sprite,False,False)

    def handleAnimation(self):
        animation = self.animationStates[self.currentState]
        self.frame_index += self.animationTime

        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        self.sprite = animation[int(self.frame_index)]
        self.sprite = self.handleSpriteRotation()
        self.rect = self.sprite.get_rect(center=self.hitbox.center)

    def update(self):
        self.handleMovement()
        self.handleAnimation()
        currentState = self.stateCache.get(self.currentState)
        currentState()


