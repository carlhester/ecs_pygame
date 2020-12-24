#!/usr/bin/python3 


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

def main():
    CM = ComponentManager()
    entities = Entities()
    
    first = entities.add("first")
    CM.addSizer(first, SizeComponent(10,10))
   
    second = entities.add()
    CM.addSizer(second, SizeComponent(30,30))
    CM.addPositioner(second, PositionComponent(120,230))
    CM.addDrawer(second, DrawComponent())
    
    third = entities.add()
    CM.addPositioner(third, PositionComponent(240,110))
    CM.addMover(third, MoveComponent(15,5))

    fourth = entities.add("fourth")
    CM.addPositioner(fourth, PositionComponent(240,110))
    CM.addDrawer(fourth, DrawComponent())

    print(CM.Positioners)
    print(CM.Movers)
    for e in entities.all_ids():
        # draw is size + position + draw
        if CM.hasSize(e) and CM.hasPosition(e) and CM.hasDraw(e):
            DrawSystem(CM.getSize(e), CM.getPosition(e))
        # move is position + move
        if CM.hasMove(e) and CM.hasPosition(e):
            MoveSystem(CM.getPosition(e), CM.getMove(e))
    print(CM.Positioners)
    print(CM.Movers)

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
    
    def hasSize(self, entity_id):
        if entity_id in self.Sizers:
            return True
    
    def getSize(self, entity_id):
        return self.Sizers[entity_id]
   
    # Draw
    def addDrawer(self, entity_id, draw_component):
        self.Drawers[entity_id] = draw_component 
    
    def hasDraw(self, entity_id):
        if entity_id in self.Drawers:
            return True
    # Move 
    def addMover(self, entity_id, move_component):
        self.Movers[entity_id] = move_component 
    
    def hasMove(self, entity_id):
        if entity_id in self.Movers:
            return True
    
    def getMove(self, entity_id):
        return self.Movers[entity_id]
    
    # Position 
    def addPositioner(self, entity_id, pos_component):
        self.Positioners[entity_id] = pos_component
    
    def hasPosition(self, entity_id):
        if entity_id in self.Positioners:
            return True
    
    def getPosition(self, entity_id):
        return self.Positioners[entity_id]
    
def DrawSystem(size_component, pos_component):
    print("Drawing w: %s h: %s at x: %s y: %s" % (size_component.w, size_component.h, pos_component.x, pos_component.y))

def MoveSystem(pos_component, move_component):
    print("Moving x: %s y: %s to x: %s y: %s" % (pos_component.x, pos_component.y, move_component.x, pos_component.y))
    pos_component.x += move_component.x
    pos_component.y += move_component.y
    print("Moving x: %s y: %s to x: %s y: %s" % (pos_component.x, pos_component.y, move_component.x, pos_component.y))

if __name__ == "__main__":
    main()
