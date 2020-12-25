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
        self._running = True
        self.CM = ComponentManager()
        self.entities = Entities()
        
        first = self.entities.add("first")
        self.CM.addSizer(first, SizeComponent(10,10))
       
        second = self.entities.add()
        self.CM.addSizer(second, SizeComponent(30,30))
        self.CM.addPositioner(second, PositionComponent(120,230))
        self.CM.addDrawer(second, DrawComponent())
        
        third = self.entities.add()
        self.CM.addPositioner(third, PositionComponent(240,110))
        self.CM.addMover(third, MoveComponent(15,5))

        fourth = self.entities.add("fourth")
        self.CM.addPositioner(fourth, PositionComponent(240,110))
        self.CM.addDrawer(fourth, DrawComponent())

    def execute(self):
        if self.init() == False:
            self._running = False

        while (self._running):
            for event in pygame.event.get():
                self.events(event)
            self.update()
            self.render()
        self.cleanup()


    def update(self):
        for e in self.entities.all_ids():
            # draw is size + position + draw
            if self.CM.hasSize(e) and self.CM.hasPosition(e) and self.CM.hasDraw(e):
                DrawSystem(self.CM.getSize(e), self.CM.getPosition(e))
            # move is position + move
            if self.CM.hasMove(e) and self.CM.hasPosition(e):
                MoveSystem(self.CM.getPosition(e), self.CM.getMove(e))

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            print(event.type, event.key)
            if event.key == pygame.K_q:
                self._running = False
        if event.type == pygame.QUIT:
            self._running = False

    def cleanup(self):
        pygame.quit()

    def render(self):
        pass
class DrawComponent:
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
        self.Positioners = {}
    
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
    
def DrawSystem(size_component, pos_component):
    #print("Drawing w: %s h: %s at x: %s y: %s" % (size_component.w, size_component.h, pos_component.x, pos_component.y))
    pass

def MoveSystem(pos_component, move_component):
    print("Moving x: %s y: %s to x: %s y: %s" % (pos_component.x, pos_component.y, move_component.x, pos_component.y))
    pos_component.x += move_component.x
    pos_component.y += move_component.y
    print("Moving x: %s y: %s to x: %s y: %s" % (pos_component.x, pos_component.y, move_component.x, pos_component.y))

if __name__ == "__main__":
    game = Game()
    game.execute()


