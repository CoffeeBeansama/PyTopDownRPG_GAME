import pygame as pg
from support import loadSprite,import_folder
from eventhandler import EventHandler
from timer import Timer

class Player(pg.sprite.Sprite):
    def __init__(self,pos,group):
        super().__init__(group)
        
        self.pos = pos
        self.group = group
        
        self.currentState = "Down_Idle"

        self.frame_index = 0
        self.animationTime = 1 / 8

        self.direction = pg.math.Vector2()

        self.speed = 2
        
        self.attackTimer = Timer(300)

        self.initializeSprites()

    def initializeSprites(self):
        self.spritePath = "Sprites/Player/"

        self.sprite = pg.image.load(f"{self.spritePath}{self.currentState}/00.png")
        self.rect = self.sprite.get_rect(topleft=self.pos)
        self.hitbox = self.rect.inflate(0,0)

        self.animationStates = {
            "Down": [], "Up": [], "Left": [], "Right" : [],
            "Down_Idle": [],"Up_Idle": [], "Left_Idle": [] , "Right_Idle": [],
            "Down_Attack": [],"Up_Attack" : [], "Left_Attack" : [], "Right_Attack" : [],
            "Death" : []
        }

        for animations in self.animationStates.keys():
            fullPath = self.spritePath + animations
            self.animationStates[animations] = import_folder(fullPath)

    def handleAnimation(self):
        animation = self.animationStates[self.currentState]
        self.frame_index += self.animationTime

        if self.frame_index >= len(animation):
            self.frame_index = 0
            if "_Attack" in self.currentState:
                self.currentState = self.currentState.replace("_Attack","_Idle")

        
        self.sprite = animation[int(self.frame_index)].convert_alpha()
        self.rect = self.sprite.get_rect(center=self.hitbox.center)

    def handleRendering(self):
        self.handleAnimation()
   
    def idleState(self):
        if "_Attack" in self.currentState: return

        self.direction.x = 0 
        self.direction.y = 0
        if not "_Idle" in self.currentState:
           self.currentState = f"{self.currentState}_Idle"

    def handleMovement(self):
        self.hitbox.x += self.direction.x * self.speed
        self.hitbox.y += self.direction.y * self.speed
        self.rect.center = self.hitbox.center    
    

    def handlePlayerAttack(self):
        for direction in ["Up","Down","Left","Right"]:
            if direction in self.currentState:
               self.frame_index = 0
               self.currentState = f"{direction}_Attack"

    def handleStateDirection(self,value,state):
        if "_Attack" in self.currentState: return

        if state in ["Up","Down"]:
           self.direction.x = 0
           self.direction.y = value
        elif state in ["Left","Right"]:
           self.direction.x = value
           self.direction.y = 0
        self.currentState = state

    def handlePlayerInput(self): 
        if EventHandler.pressingUpButton():
           self.handleStateDirection(-1,"Up")
        elif EventHandler.pressingDownButton():
           self.handleStateDirection(1,"Down")
        elif EventHandler.pressingLeftButton():
           self.handleStateDirection(-1,"Left")
        elif EventHandler.pressingRightButton():
           self.handleStateDirection(1,"Right")
        else:
           self.idleState()

        if EventHandler.pressingAttackButton():
           if not self.attackTimer.activated:
              self.handlePlayerAttack()
              self.attackTimer.activate()

    def update(self):
        self.attackTimer.update()
        self.handlePlayerInput()
        self.handleMovement()
        self.handleRendering()
