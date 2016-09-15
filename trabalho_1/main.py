# Workarround for importing in pygamezero
import sys; sys.path.append('.')

from car import *

class World:
    WIDTH = 800
    HEIGHT = 600

    def __init__(self, objects=[]):
        self.objects = list(objects)

    def update(self, dt):
        for obj in self.objects:
            obj.update(dt)

    def draw(self):
        for obj in self.objects:
            obj.draw()

    def add(self, obj):
        self.objects.append(obj)



# Starting pygamezero simulation
world = World()

def update(dt):
    screen.clear()
    world.update(dt)

def draw():
    world.draw()

car_1 = Car(Actor('notacar75px'), "Carro 1", 1000, 300, 500)

#Puts car_1 in first gear - Make it possible to move
car_1.gear = 1

world.add(car_1)
