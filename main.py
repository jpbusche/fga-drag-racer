# Workarround for importing in pygamezero
import sys; sys.path.append('.')

#from FGAme import *
from car import *
from world import *
from background import *
from ui_elements import *
from menu import *
from car_parser import *
import pygame

WIDTH = 450
HEIGHT = 800
PLAYER_MODEL = "Gamavette"
OTHER_MODEL = "Enemy_Default"

def on_mouse_down(pos, button):
    if button == mouse.LEFT and bt_sair.actor.collidepoint(pos):
        quit_game()
    elif button == mouse.LEFT and bt_voltar.actor.collidepoint(pos):
        pause_menu.destroy(world)
    elif button == mouse.LEFT and bt_again.actor.collidepoint(pos):
        if world.game_won:
            win_menu.destroy(world)
        else:
            lose_menu.destroy(world)

        reset_game()

def on_key_down(key):
    if key == keys.UP and car_player.gear < 6:
        car_player.gear += 1
        print("Upshift")
    elif key == keys.DOWN and car_player.gear > 1:
        car_player.gear -= 1
        print("Downshift")
    elif key == keys.P:
        if not world.paused:
            world.paused = True
    elif key == keys.R:
        #For Debug or cheating
        reset_game()

def reset_game():
    global car_player, car_other
    world.game_won = 0
    world.game_lost = 0

    world.remove(car_player)
    world.remove(car_other)

    car_player = get_car(car_array, PLAYER_MODEL, 330, 500, False)
    car_other = get_car(car_array, OTHER_MODEL, 130, 500, True, 1)

    world.add(car_player)
    world.add(car_other)

def move_road(back_1, back_2, player):
    back_increment = int(player.road_increment)

    if back_1.y > 800:
        back_1.y = -(800 - back_2.y)
    if back_2.y > 800:
        back_2.y = -(800 - back_1.y)

    back_1.y = back_1.y + back_increment
    back_2.y = back_2.y + back_increment

def move_other(player, other):
    # "30" defined in Car Class as C_MOVE
    other.y = 500 + ((player.distance - other.distance) * 30)

def assign_actors(car_array):
    for car in car_array:
        image = car['actor']
        print(image)

        car['actor'] = Actor(image, anchor=('middle', 'top'))

def check_win(player, other):
    if world.game_won or world.game_lost:
        return 0
    if player.distance >= world.max_distance:
        world.game_won = 1
        return 1
    elif other.distance >= world.max_distance:
        world.game_lost = 1
        return -1

def show_stats(car_object, other):
    RED = 200, 0, 0
    GREEN = 0, 200, 0
    BLACK = 0, 0, 0
    COLOR_PLAYER = 190, 4, 17
    COLOR_OTHER = 184, 90, 10

    sizes = set_rect_sizes(car_object, other, world)
    rpm_color = GREEN if car_object.rpm < car_object.max_rpm else RED

    if not world.paused:
        draw_basic_info(car_object, screen)

        rect_rpm = Rect((20, 70), (sizes['rect_rpm_width'], sizes['rect_height']))
        rect_player_distance = Rect((20, 130), (sizes['rect_player_width'], 12.5))
        rect_other_distance = Rect((20, 147.5), (sizes['rect_other_width'], 12.5))
        rect_end_distance = Rect((430, 130), (2, sizes['rect_height']))
        rect_end_rpm = Rect((430, 70), (2, sizes['rect_height']))

        screen.draw.filled_rect(rect_rpm, rpm_color)
        screen.draw.filled_rect(rect_other_distance, COLOR_OTHER) \
            if car_object.distance < other.distance \
            else screen.draw.filled_rect(rect_player_distance, COLOR_PLAYER)
        screen.draw.filled_rect(rect_player_distance, COLOR_PLAYER) \
            if car_object.distance < other.distance \
            else screen.draw.filled_rect(rect_other_distance, COLOR_OTHER)
        screen.draw.filled_rect(rect_end_distance, BLACK)
        screen.draw.filled_rect(rect_end_rpm, BLACK)

def set_acceleration(car_object):
    if keyboard.space:
        car_object.throttle_position = 1
    else:
        car_object.throttle_position = 0.02

def check_brake(car_object):
    if keyboard.b and car_object.velocity > 0:
        car_object.breaking = True
    elif keyboard.b and car_object.velocity <= 0:
        car_object.breaking = False
        car_object.velocity = 0
    else:
        car_object.breaking = False

def load_cars():
    json_data = load_json()
    car_array = car_decoder(json_data)
    assign_actors(car_array)

    return car_array

def draw():
    world.draw()
    show_stats(car_player, car_other)

def update(dt):
    # You can define the max distance in world.py - Default: 1000m
    win_status = check_win(car_player, car_other)

    if win_status == 1:
        world.paused = True
        win_menu.show(world)
    elif win_status == -1:
        world.paused = True
        lose_menu.show(world)

    if not world.paused:
        screen.clear()
        check_brake(car_player)
        set_acceleration(car_player)
        move_other(car_player, car_other)
        move_road(bk_1, bk_2, car_player)
        world.update(dt)
        car_player.print_stats()
    elif world.paused:
        pause_menu.show(world)

# Starting pygamezero simulation
world = World()

#Loading car files
car_array = load_cars()

# Creates the first cars references
car_player = get_car(car_array, PLAYER_MODEL, 330, 500, False)
car_other = get_car(car_array, OTHER_MODEL, 130, 500, True, 1)

# Defines the 2 backgrounds
bk_1 = Image(Actor('road', anchor=('left', 'top')), 0, 0, "bk_1")
bk_2 = Image(Actor('road', anchor=('left', 'top')), 0, -800, "bk_2")

#For pause_menu
bt_voltar = Image(Actor('bt_voltar', anchor=('left', 'top')), 63.4, 375, "bt_voltar")
bt_sair = Image(Actor('bt_sair', anchor=('left', 'top')), 63.4, 490, "bt_sair")
bk_pause = Image(Actor('pause_bk', anchor=('left', 'top')), 0, 0, "bk_pause")

#For Win or Lose
bt_again = Image(Actor('bt_again', anchor=('left', 'top')), 63.4, 375, "bt_again")
bk_win = Image(Actor('win_bk', anchor=('left', 'top')), 0, 0, "bk_win")
bk_lose = Image(Actor('lose_bk', anchor=('left', 'top')), 0, 0, "bk_lose")

# Create lists for the itens
pause_actors = [bk_pause, bt_voltar, bt_sair]
lose_actors = [bk_lose, bt_again, bt_sair]
win_actors = [bk_win, bt_again, bt_sair]

# Create object for each menu
pause_menu = Menu(pause_actors)
lose_menu = Menu(lose_actors)
win_menu = Menu(win_actors)

# Add objects to World
world.add(bk_1)
world.add(bk_2)
world.add(car_player)
world.add(car_other)
