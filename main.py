#!/usr/bin/python3 

import pygame
from pygame.locals import *

class Entities:
    def __init__(self):
        self.counter = 0
        self.ids = []
        self.names = [] 

    def add(self, name=""):
        self.counter += 1
        self.ids.append(self.counter)
        self.names.append(name)
        return self.counter
    
    def remove_id(self, id_):
        pass
    
    def remove_name(self, id_):
        pass

    def all_ids(self):
        return self.ids
    
    def all_names(self):
        return self.names

    def name(self, id_):
        return self.names[id_]
    
    def id_for_name(self, name):
        return self.ids.index(name)


class Game:
    def init(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self._running = True
        self.screen_width = 640
        self.screen_height = 640
        self.bg_color = (0,100,0)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), 0, 32)
        
        self.CM = ComponentManager()
        self.entities = Entities()
        
        player = self.entities.add("first")
        self.CM.addSizer(player, SizeComponent(32,32))
        self.CM.addPositioner(player, PositionComponent(64,64))
        self.CM.addMover(player, MoveComponent(0,0))
        self.CM.addController(player, ControlComponent())
        self.CM.addDrawer(player, DrawComponent())


    def execute(self):
        if self.init() == False:
            self._running = False

        while (self._running):
            self.update()
            self.render()
            self.clock.tick(30)
        self.cleanup()


    def update(self):
        key = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self._running = False
                if event.key == pygame.K_RIGHT:
                    key = "moveright"
                if event.key == pygame.K_LEFT:
                    key = "moveleft"
                if event.key == pygame.K_UP:
                    key = "moveup"
                if event.key == pygame.K_DOWN:
                    key = "movedown"
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    key = "moverightstop"
                if event.key == pygame.K_LEFT:
                    key = "moveleftstop"
                if event.key == pygame.K_UP:
                    key = "moveupstop"
                if event.key == pygame.K_DOWN:
                    key = "movedownstop"

        for e in self.entities.all_ids():
            # control is control
            if self.CM.hasControl(e) and self.CM.hasMove(e) and key != None:
                ControlSystem(key, self.CM.getMove(e))
                key = None
            # move is position + move
            if self.CM.hasMove(e) and self.CM.hasPosition(e):
                MoveSystem(self.CM.getPosition(e), self.CM.getMove(e))
            # draw is size + position + draw
            if self.CM.hasSize(e) and self.CM.hasPosition(e) and self.CM.hasDraw(e):
                DrawSystem(self.screen, self.CM.getDraw(e), self.CM.getPosition(e), self.CM.getSize(e))

    def cleanup(self):
        pygame.quit()

    def render(self):
        pygame.display.flip()
        self.screen.fill(self.bg_color)
        for x in range(0, self.screen_width, 64):
            pygame.draw.line(self.screen, (100, 100, 100), (x, 0), (x, self.screen_height))
        for y in range(0, self.screen_height, 64):
            pygame.draw.line(self.screen, (100, 100, 100), (0, y), (self.screen_width, y))

class DrawComponent:
    def __init__(self):
        self.img = pygame.image.load('badguy.png').convert()
        self.img = pygame.transform.scale(self.img, (64,64))
        self.surface = pygame.Surface((64,64), pygame.SRCALPHA)
        self.surface.blit(self.img, (0,0))
        self.rect = self.surface.get_rect()

class ControlComponent:
    def __init__(self):
        pass

class SizeComponent:
    def __init__(self, w, h):
        self.w = w
        self.h = h

class PositionComponent:
    def __init__(self, x, y):
        self.x = x
        self.y = y 

class MoveComponent:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class ComponentManager:
    def __init__(self):
        self.Sizers = {}
        self.Drawers = {}
        self.Movers = {}
        self.Controllers = {}
        self.Positioners = {}
    
    # Control
    def addController(self, entity_id, control_component):
        self.Controllers[entity_id] = control_component

    def removeController(self, entity_id):
        del self.Controllers[entity_id]
    
    def hasControl(self, entity_id):
        if entity_id in self.Controllers:
            return True
    
    def getControl(self, entity_id):
        return self.Controllers[entity_id]
    
    # Size
    def addSizer(self, entity_id, size_component):
        self.Sizers[entity_id] = size_component

    def removeSizer(self, entity_id):
        del self.Sizers[entity_id]
    
    def hasSize(self, entity_id):
        if entity_id in self.Sizers:
            return True
    
    def getSize(self, entity_id):
        return self.Sizers[entity_id]
   
    # Draw
    def addDrawer(self, entity_id, draw_component):
        self.Drawers[entity_id] = draw_component 
    
    def removeDrawer(self, entity_id):
        del self.Drawers[entity_id]
    
    def hasDraw(self, entity_id):
        if entity_id in self.Drawers:
            return True
    
    def getDraw(self, entity_id):
        return self.Drawers[entity_id]

    # Move 
    def addMover(self, entity_id, move_component):
        self.Movers[entity_id] = move_component 
    
    def removeMover(self, entity_id):
        del self.Movers[entity_id]
    
    def hasMove(self, entity_id):
        if entity_id in self.Movers:
            return True
    
    def getMove(self, entity_id):
        return self.Movers[entity_id]
    
    # Position 
    def addPositioner(self, entity_id, pos_component):
        self.Positioners[entity_id] = pos_component
    
    def removePositioner(self, entity_id):
        del self.Positioners[entity_id]
    
    def hasPosition(self, entity_id):
        if entity_id in self.Positioners:
            return True
    
    def getPosition(self, entity_id):
        return self.Positioners[entity_id]
    
def DrawSystem(screen, draw, pos, size):
    screen.blit(draw.surface, (pos.x, pos.y, size.w, size.h))

def ControlSystem(key, move):
    print(key)
    # left right
    if key == "moveright":
        move.x = 64 
    if key == "moverightstop":
        move.x = 0
    if key == "moveleft":
        move.x = -64
    if key == "moveleftstop":
        move.x = 0
    
    # up down
    if key == "moveup":
        move.y = -64
    if key == "moveupstop":
        move.y = 0
    if key == "movedown":
        move.y = 64
    if key == "movedownstop":
        move.y = 0

def MoveSystem(pos_component, move_component):
    pos_component.x += move_component.x
    pos_component.y += move_component.y

if __name__ == "__main__":
    game = Game()
    game.execute()


