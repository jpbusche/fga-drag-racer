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

    screen.blit(('backgroundpng'), pos=(0,0))
    reset_car_pos(car_1)
    change_gear(car_1)
    check_brake(car_1, dt)
    set_acceleration(car_1)
    show_stats(car_1)

    world.update(dt)

def draw():
    world.draw()

def reset_car_pos(car_object):
    if(car_object.y  < -75):
        car_object.y = world.HEIGHT

def show_stats(car_object):
    screen.draw.text("Velocity (m/s): " + str(car_object.velocity), (30, 30), color="green")
    screen.draw.text("Velocity (Km/h): " + str(car_object.velocity * 3.6), (30, 50), color="green")
    screen.draw.text("RPM: " + str(car_object.rpm), (30, 70), color="green")
    screen.draw.text("Gear: " + str(car_object.gear), (30, 90), color="green")
    screen.draw.text("Forces (N): " + str(car_object.forces), (30, 110), color="green")

def set_acceleration(car_object):
    if keyboard.space:
        car_object.throttle_position = 1
    else:
        car_object.throttle_position = 0.05

def change_gear(car_object):
    if keyboard.up and car_object.gear < 6:
        car_object.gear += 1
    elif keyboard.down and car_object.gear > 1:
        car_object.gear -= 1
    else:
        pass

def check_brake(car_object,dt):
    if keyboard.b and car_object.velocity > 0:
        car_object.forces -= 8000
        car_object.calculate_velocity(dt)
    elif keyboard.b and car_object.velocity <= 0:
        car_object.velocity = 0
        car_object.rpm = 900
    else:
        pass

car_1 = Car(Actor('car'), "Carro 1", 1000, 300, 500, 6500)


#Puts car_1 in first gear - Make it possible to move
car_1.gear = 1

world.add(car_1)
