import pygame as pg
from support import import_folder,drawBox
from timer import Timer

class Slime(pg.sprite.Sprite):
    def __init__(self,pos,group,player):
        super().__init__(group)
        self.pos = pos
        self.player = player
        
        self.screen = pg.display.get_surface()

        self.maxHP = 30
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

        self.maxHPBarWidth = 25
        self.maxHPBarHeight = 3
        
        self.attackDamage = 5
        self.attackTimer = Timer(2000,self.damagePlayer)
        

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
    
    def takeDamage(self,damage):
        self.currentHP -= damage
        if self.currentHP <= 0:
           self.switchState("Death")
        else:
           self.switchState("Hurt")
        
            

    def switchState(self,newState):
        self.currentState = newState
        self.frame_index = 0

    def idleState(self):        
        self.direction = pg.math.Vector2()
        if self.getPlayerDistance() <= self.chaseRadius:
           self.switchState("Chase")

    def chaseState(self):
        self.direction = self.getPlayerPosition()
        if self.getPlayerDistance() >= self.chaseRadius:
           self.switchState("Idle")

        if self.getPlayerDistance() <= self.attackRadius:
           self.switchState("Attack") 
    
    def damagePlayer(self):
        if hasattr(self.player,"takeDamage"):
           self.player.takeDamage(self.attackDamage)


    def attackState(self):
        self.attackTimer.update()
        self.direction = pg.math.Vector2()

        if not self.attackTimer.activated:
           self.attackTimer.activate()

        if self.getPlayerDistance() >= self.attackRadius + 5:
           self.switchState("Chase")

    def hurtState(self):
        self.direction = -self.getPlayerPosition()

    def deathState(self):
        self.direction = pg.math.Vector2()
    
    
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
            if self.currentState == "Death":
               self.kill()
            if self.currentState == "Hurt":
               self.switchState("Chase")
            self.frame_index = 0
            

        
        self.sprite = animation[int(self.frame_index)]
        self.sprite = self.handleSpriteRotation()
        self.rect = self.sprite.get_rect(center=self.hitbox.center)
    
    def drawHPBar(self,surface,x,y,width,maxWidth,height): 
        red = (255,0, 0)
        green = (0, 255, 0)
        pg.draw.rect(surface,red,(x,y,maxWidth,height))
        return pg.draw.rect(surface,green,(x,y,width,height))

    def handleRenderingHPBar(self,surface,offset):
        if self.currentState == "Idle": return

        diff = (self.maxHPBarWidth / self.maxHP) * self.maxHPBarWidth 
        enemyHPBarWidth = (self.currentHP / self.maxHPBarWidth) * diff
        
        x = offset[0] + 3
        y = offset[1] + 30

        black = (0,0,0)

        background = pg.draw.rect(surface,black,(x,y,self.maxHPBarWidth+2,self.maxHPBarHeight+2))
        hpBar = self.drawHPBar(surface,x+1,y+1,enemyHPBarWidth,self.maxHPBarWidth,self.maxHPBarHeight)
    

    def update(self):
        self.handleMovement()
        self.handleAnimation()

        currentState = self.stateCache.get(self.currentState)
        currentState()


