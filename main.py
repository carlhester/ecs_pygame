#!/usr/bin/python3 

def main():
    entities = []

    CM = ComponentManager()
    
    next_id = 0 
    entities.append(next_id)
    CM.addSizer(next_id, SizeComponent(10,10))
   
    next_id += 1
    entities.append(next_id)
    CM.addSizer(next_id, SizeComponent(30,30))
    CM.addPositioner(next_id, PositionComponent(120,230))
    CM.addDrawer(next_id, DrawComponent())
    
    next_id += 1
    entities.append(next_id)
    CM.addPositioner(next_id, PositionComponent(240,110))
    
    next_id += 1
    entities.append(next_id)
    CM.addPositioner(next_id, PositionComponent(240,110))
    CM.addDrawer(next_id, DrawComponent())

    for e in entities:
        if CM.hasSize(e):
            print(e)
    print(CM.Sizers)
    print(CM.Drawers)
    print(CM.Positioners)

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

class ComponentManager:
    def __init__(self):
        self.Drawers = {}
        self.Sizers = {}
        self.Positioners = {}
    
    def addSizer(self, entity_id, size_component):
        self.Sizers[entity_id] = size_component
    
    def addDrawer(self, entity_id, draw_component):
        self.Drawers[entity_id] = draw_component 
    
    def addPositioner(self, entity_id, pos_component):
        self.Positioners[entity_id] = pos_component

    def hasSize(self, entity_id):
        if entity_id in self.Sizers:
            return True


if __name__ == "__main__":
    main()
