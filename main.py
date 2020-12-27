#!/usr/bin/python3 

import pygame
from pygame.locals import *

class Game:
    def init(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self._running = True
        
        # screen
        self.screen_width = 640
        self.screen_height = 640
        self.cell_size= 64
        self.cells_wide = (self.screen_width / self.cell_size) - 1
        self.cells_high = (self.screen_height / self.cell_size) - 1

        self.bg_color = (0,100,0)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), 0, 32)
       
        # ECS controls
        self.CM = ComponentManager()
        self.entities = Entities()
       
        # player
        player = self.entities.add("player")
        self.CM.addSizer(player, SizeComponent(self.cell_size, self.cell_size))
        self.CM.addPositioner(player, PositionComponent(1,1))
        self.CM.addController(player, ControlComponent())
        self.CM.addMover(player, MoveComponent(0,0))
        self.CM.addDrawer(player, DrawComponent('badguy.png'))
        self.CM.addCollider(player, CollideComponent()) 
        
        # wall
        wall = self.entities.add("wall")
        self.CM.addSizer(wall, SizeComponent(self.cell_size, self.cell_size))
        self.CM.addPositioner(wall, PositionComponent(0,0))
        self.CM.addDrawer(wall, DrawComponent('wall.png'))
        self.CM.addCollider(player, CollideComponent()) 
        
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
                ControlSystem(key, self.CM.getMove(e), self.cell_size)
                key = None
            # collision
            if self.CM.hasCollide(e) and self.CM.hasPosition(e) and self.CM.hasMove(e):
                for c in self.entities.all_ids():
                    if self.CM.hasPosition(c) and self.CM.hasCollide(c):
                        blocked = CollideSystem(self.CM.getPosition(e), self.CM.getMove(e), self.CM.getPosition(c))
                        if blocked: 
                            self.CM.getMove(e).x = 0
                            self.CM.getMove(e).y = 0
            # move is position + move
            if self.CM.hasMove(e) and self.CM.hasPosition(e):
                MoveSystem(self.CM.getPosition(e), self.CM.getMove(e), self.cells_high, self.cells_wide)
            # draw is size + position + draw
            if self.CM.hasSize(e) and self.CM.hasPosition(e) and self.CM.hasDraw(e):
                DrawSystem(self.screen, self.cell_size, self.CM.getDraw(e), self.CM.getPosition(e), self.CM.getSize(e))

    def cleanup(self):
        pygame.quit()

    def render(self):
        pygame.display.flip()
        self.screen.fill(self.bg_color)
        for x in range(0, self.screen_width, self.cell_size):
            pygame.draw.line(self.screen, (100, 100, 100), (x, 0), (x, self.screen_height))
        for y in range(0, self.screen_height, self.cell_size):
            pygame.draw.line(self.screen, (100, 100, 100), (0, y), (self.screen_width, y))



class DrawComponent:
    def __init__(self, filename):
        self.img = pygame.image.load(filename).convert()
        self.img = pygame.transform.scale(self.img, (64,64))
        self.surface = pygame.Surface((64,64), pygame.SRCALPHA)
        self.surface.blit(self.img, (0,0))
        self.rect = self.surface.get_rect()

class ControlComponent:
    def __init__(self):
        pass

class CollideComponent:
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
        self.Colliders = {}
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
    
    # Colliders 
    def addCollider(self, entity_id, collide_component):
        self.Colliders[entity_id] = collide_component 
    
    def removeCollider(self, entity_id):
        del self.Colliders[entity_id]
    
    def hasCollide(self, entity_id):
        if entity_id in self.Colliders:
            return True
    
    def getCollide(self, entity_id):
        return self.Colliders[entity_id]

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
    
def DrawSystem(screen, cell_size, draw, pos, size):
    screen.blit(draw.surface, (pos.x * cell_size, pos.y * cell_size, size.w * cell_size, size.h * cell_size))

def ControlSystem(key, move, cell_size):
    # left right
    if key == "moveright":
        move.x = 1 
    if key == "moverightstop":
        move.x = 0
    if key == "moveleft":
        move.x = -1
    if key == "moveleftstop":
        move.x = 0
    
    # up down
    if key == "moveup":
        move.y = -1
    if key == "moveupstop":
        move.y = 0
    if key == "movedown":
        move.y = 1
    if key == "movedownstop":
        move.y = 0

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

def MoveSystem(pos, move, cells_wide, cells_high):
    print(pos.x, pos.y)
    orig_x = pos.x
    pos.x += move.x
    if pos.x < 0 or pos.x > cells_wide:
        pos.x = orig_x
    
    orig_y = pos.y
    pos.y += move.y
    if pos.y < 0 or pos.y > cells_high:
        pos.y = orig_y


def CollideSystem(pos, move, target):
    if pos.x + move.x == target.x and pos.y + move.y == target.y: 
        return True

if __name__ == "__main__":
    game = Game()
    game.execute()




