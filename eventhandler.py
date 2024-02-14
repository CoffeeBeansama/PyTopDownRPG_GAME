import pygame as pg

class EventHandler(object):
    pressingUp = False
    pressingDown = False
    pressingRight = False
    pressingLeft = False
    pressingAttack = False

    @staticmethod
    def handlePlayerInput():
        keys = pg.key.get_pressed()

        EventHandler.pressingUp = True if keys[pg.K_UP] else False
        EventHandler.pressingDown = True if keys[pg.K_DOWN] else False
        EventHandler.pressingRight = True if keys[pg.K_RIGHT] else False
        EventHandler.pressingLeft = True if keys[pg.K_LEFT] else False
        EventHandler.pressingAttack = True if keys[pg.K_x] else False

    def pressingUpButton():
        return EventHandler.pressingUp
    
    def pressingDownButton():
        return EventHandler.pressingDown
    
    def pressingRightButton():
        return EventHandler.pressingRight
    
    def pressingLeftButton():
        return EventHandler.pressingLeft
    
    def pressingInteractButton():
        return EventHandler.pressingAttack

