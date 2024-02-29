import pygame as pg
from support import loadSprite,import_folder,drawBox
from eventhandler import EventHandler
from timer import Timer

class Player(pg.sprite.Sprite):
    def __init__(self,pos,group,createAttack):
        super().__init__(group)
        
        self.screen = pg.display.get_surface()
        self.pos = pos
        self.group = group
        self.createAttack = createAttack

        self.currentState = "Down_Idle"

        self.frame_index = 0
        self.animationTime = 1 / 8

        self.direction = pg.math.Vector2()
        
        self.maxHP = 50
        self.currentHP = self.maxHP

        self.speed = 2
        
        self.attack = 5

        self.maxHPBarWidth = 300
        self.maxHPBarHeight = 25
        self.hpBarXPosition = 10
        self.hpBarYPosition = 460

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
    

    def switchState(self,newState):
        self.frame_index = 0
        self.currentState = newState

    def isMoving(self):
        if self.direction.x != 0:
           return True
        if self.direction.y != 0:
           return True
        return False
    
    def takeDamage(self,damage):
        self.currentHP -= damage
        print(self.currentHP)
        if self.currentHP <= 0:
           self.switchState("Death")

    def handlePlayerAttack(self):
        if "_Attack" in self.currentState: return

        for direction in ["Up","Down","Left","Right"]:
            if direction in self.currentState:
               self.switchState(f"{direction}_Attack")
               self.createAttack()


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

        if EventHandler.pressingAttackButton() and not self.isMoving():
           if not self.attackTimer.activated:
              self.handlePlayerAttack()
              self.attackTimer.activate()

    def getHPBar(self,x,y,width,maxWidth,height): 
        red = (255,0, 0)
        green = (0, 255, 0)
        pg.draw.rect(self.screen,red,(x,y,maxWidth,height))
        return pg.draw.rect(self.screen,green,(x,y,width,height))

    def renderHPBar(self):

        diff = (self.maxHPBarWidth / self.maxHP) * self.maxHPBarWidth 
        enemyHPBarWidth = (self.currentHP / self.maxHPBarWidth) * diff
        
        x = self.hpBarXPosition
        y = self.hpBarYPosition

        black = (0,0,0)

        background = pg.draw.rect(self.screen,black,(x,y,self.maxHPBarWidth+10,self.maxHPBarHeight+10))
        hpBar = self.getHPBar(x+5,y+5,enemyHPBarWidth,self.maxHPBarWidth,self.maxHPBarHeight)
    
    def update(self):
        self.attackTimer.update()
        self.handlePlayerInput()
        self.renderHPBar()
        self.handleMovement()
        self.handleRendering()
