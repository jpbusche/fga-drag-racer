# Workarround for importing in pygamezero
import sys; sys.path.append('.')
from FGAme import *
from car import *
from world import *
from background import *
import pygame

WIDTH = 465
HEIGHT = 600

def move_road(back_1, back_2, player):
    back_increment = int(player.road_increment)

    if back_1.y > 800:
        back_1.y = -(800 - back_2.y)
    if back_2.y > 800:
        back_2.y = -(800 - back_1.y)

    back_1.y = back_1.y + back_increment
    back_2.y = back_2.y + back_increment

def update(dt):
    screen.clear()
    change_gear(car_1)
    check_brake(car_1)
    set_acceleration(car_1)
    move_road(bk_1, bk_2, car_1)
    world.update(dt)

def draw():
    world.draw()
    show_stats(car_1)

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
        car_object.throttle_position = 0.02

def change_gear(car_object):
    if keyboard.up and car_object.gear < 6:
        car_object.gear += 1
    elif keyboard.down and car_object.gear > 1:
        car_object.gear -= 1
    else:
        pass

def check_brake(car_object):
    key = pygame.key.get_pressed()

    if key[pygame.K_b] and car_object.velocity > 0:
        car_object.breaking = True
    elif key[pygame.K_b] and car_object.velocity <= 0:
        car_object.breaking = False
        car_object.velocity = 0
    else:
        car_object.breaking = False

# Starting pygamezero simulation
world = World()

car_1 = Car(Actor('car'), "Carro 1", 1414.3 , 300, 500, 6800)
bk_1 = Background(Actor('backgroundpng', anchor=('left', 'top')), 0, 0)
bk_2 = Background(Actor('backgroundpng', anchor=('left', 'top')), 0, -800)

world.add(bk_1)
world.add(bk_2)
world.add(car_1)
