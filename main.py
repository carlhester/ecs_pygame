#!/usr/bin/python3 

import pygame
from pygame.locals import *

class Game:
    def init(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self._running = True
        
        # screen
        self.screen_width = 800
        self.screen_height = 600
        self.cell_size = 50
        self.field_size = int((.75 * self.screen_width) / self.cell_size)
        self.field_width = int(.75 * self.screen_width)
        self.hud_size = int((.25 * self.screen_width) / self.cell_size)
        self.hud_width = int(.25 * self.screen_width)
        self.cells_wide = int(self.screen_width / self.cell_size) - self.hud_size
        self.cells_high = int(self.screen_height / self.cell_size)

        self.bg_color = (0,100,0)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), 0, 32)
       
        self.CM = ComponentManager()
        self.entities = Entities()
        self.message = Message(self.screen, self.field_width)
       
        # player
        player = self.entities.add("player")
        self.CM.addSizer(player, SizeComponent(self.cell_size, self.cell_size))
        self.CM.addPositioner(player, PositionComponent((5,5)))
        self.CM.addController(player, ControlComponent())
        self.CM.addMover(player, MoveComponent(0,0))
        self.CM.addDrawer(player, DrawComponent('badguy.png', self.cell_size))
     
        walls = [] 
        for x in range(0, self.cells_wide):
                walls.append((x,0)) 
                walls.append((x,self.cells_high-1)) 
        for y in range(0, self.cells_high):
                walls.append((0,y)) 
                walls.append((self.cells_wide-1, y)) 

        for w in walls:
            # wall
            wall = self.entities.add("wall")
            self.CM.addSizer(wall, SizeComponent(self.cell_size, self.cell_size))
            self.CM.addPositioner(wall, PositionComponent(w))
            self.CM.addDrawer(wall, DrawComponent('wall.png', self.cell_size))
            self.CM.addBlocker(wall, BlockComponent()) 
        
    def execute(self):
        if self.init() == False:
            self._running = False

        while (self._running):
            self.update()
            self.render()
            self.clock.tick(30)
        self.cleanup()


    def update(self):
        # debug coordinates 
        p = self.entities.id_for_name("player")
        self.message.update("(" + str(self.CM.getPosition(p).x) + "," + str(self.CM.getPosition(p).y) + ")")
        
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

        for e in self.entities.all_ids():
            # control
            if self.CM.hasControl(e) and self.CM.hasMove(e) and key != None:
                ControlSystem(key, self.CM.getMove(e), self.cell_size)
                key = None
            
            # collision
            if self.CM.hasPosition(e) and self.CM.hasMove(e):
                blockers = []
                for c in self.CM.Blockers:
                    blockers.append(self.CM.getPosition(c))
                BlockSystem(self.CM.getPosition(e), self.CM.getMove(e), blockers)
           
           # move
            if self.CM.hasMove(e) and self.CM.hasPosition(e):
                MoveSystem(self.CM.getPosition(e), self.CM.getMove(e), self.cells_wide, self.cells_high)
          
          # draw 
            if self.CM.hasSize(e) and self.CM.hasPosition(e) and self.CM.hasDraw(e):
                DrawSystem(self.screen, self.cell_size, self.CM.getDraw(e), self.CM.getPosition(e), self.CM.getSize(e))

    def cleanup(self):
        pygame.quit()

    def render(self):
        pygame.draw.rect(self.screen, (0, 0, 0), (self.field_width, 0, self.hud_width, self.screen_height))
        self.message.draw()
        pygame.display.flip()
        self.screen.fill(self.bg_color)
        for x in range(0, self.screen_width, self.cell_size):
            pygame.draw.line(self.screen, (100, 100, 100), (x, 0), (x, self.screen_height))
        for y in range(0, self.screen_height, self.cell_size):
            pygame.draw.line(self.screen, (100, 100, 100), (0, y), (self.screen_width, y))
        


class DrawComponent:
    def __init__(self, filename, cell_size):
        self.img = pygame.image.load(filename).convert()
        self.img = pygame.transform.scale(self.img, (cell_size, cell_size))
        self.surface = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
        self.surface.blit(self.img, (0,0))
        self.rect = self.surface.get_rect()

class ControlComponent:
    def __init__(self):
        pass

class BlockComponent:
    def __init__(self):
        pass

class SizeComponent:
    def __init__(self, w, h):
        self.w = w
        self.h = h

class PositionComponent:
    def __init__(self, loc):
        self.x = loc[0]
        self.y = loc[1] 

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
        self.Blockers = {}
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
    
    # Blockers 
    def addBlocker(self, entity_id, collide_component):
        self.Blockers[entity_id] = collide_component 
    
    def removeBlocker(self, entity_id):
        del self.Blockers[entity_id]
    
    def hasBlock(self, entity_id):
        if entity_id in self.Blockers:
            return True
    
    def getBlock(self, entity_id):
        return self.Blockers[entity_id]

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
    elif key == "moveleft":
        move.x = -1
    
    # up down
    if key == "moveup":
        move.y = -1
    elif key == "movedown":
        move.y = 1

class Entities:
    def __init__(self):
        self.counter = 0
        self.ids = []
        self.names = [] 

    def add(self, name=""):
        current = self.counter 
        self.ids.append(current)
        self.names.append(name)
        self.counter += 1
        return current
    
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
        return self.names.index(name)

def MoveSystem(pos, move, cells_wide, cells_high):
    orig_x = pos.x
    pos.x += move.x
    if pos.x < 0 or pos.x > cells_wide+1:
        pos.x = orig_x
    
    orig_y = pos.y
    pos.y += move.y
    if pos.y < 0 or pos.y > cells_high+1:
        pos.y = orig_y

    move.x = 0
    move.y = 0 

# Block System is for immovable objects
def BlockSystem(pos, move, blockers):
    for b in blockers:
        if pos.x + move.x == b.x and pos.y + move.y == b.y: 
            print("blocked! ({:d}, {:d})".format(b.x, b.y)) 
            move.x = 0 
            move.y = 0 

class Message():
    def __init__(self, surface, field_width):
        self.text = ""
        self.field_width = field_width
        self.surface = surface
        self.font = pygame.font.SysFont(None, 32, 0, 1)

    def update(self, text):
        self.text = text
        
    def draw(self):
        if self.text != "":
            text = self.font.render(self.text, False, (255, 255, 255), (0,0,0))
            textrect = text.get_rect()
            textrect.x = self.field_width + 10
            textrect.y = 10
            self.surface.blit(text, textrect)
    
    def clear(self):
        self.text = ""

if __name__ == "__main__":
    game = Game()
    game.execute()

