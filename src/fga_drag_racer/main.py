# Workarround for importing in pygamezero
import sys
sys.path.append('.')

#from FGAme import *
from car import *
from world import *
from background import *
from ui_elements import *
from menu import *
from main_menu import *
from car_parser import *
from time_slip import *
from countdown import Countdown
import pygame

WIDTH = 450
HEIGHT = 800

def on_mouse_down(pos, button):
    #Quit Game button - In Main Menu (**_mm) and Pause Menu
    if button == mouse.LEFT and (bt_sair.actor.collidepoint(pos) or \
    bt_sair_mm.actor.collidepoint(pos)):
        quit_game()

    #Back button
    elif button == mouse.LEFT and bt_voltar.actor.collidepoint(pos):
        pause_menu.destroy(world)

    #Play Again button
    elif button == mouse.LEFT and bt_again.actor.collidepoint(pos):
        if world.game_won:
            win_menu.destroy(world)
        else:
            lose_menu.destroy(world)
        screen.clear()
        main_menu.in_menu = True

    #Select player's car
    elif button == mouse.LEFT and bt_next_player.actor.collidepoint(pos):
        main_menu.next_car("player")
    elif button == mouse.LEFT and bt_prev_player.actor.collidepoint(pos):
        main_menu.prev_car("player")

    #Select other's car
    elif button == mouse.LEFT and bt_next_other.actor.collidepoint(pos):
        main_menu.next_car("other")
    elif button == mouse.LEFT and bt_prev_other.actor.collidepoint(pos):
        main_menu.prev_car("other")

    #Play Button
    elif button == mouse.LEFT and bt_play.actor.collidepoint(pos):
        main_menu.in_menu = False
        main_menu.destroy(world)
        reset_game()
        countdown_menu.start_countdown()

def on_key_down(key):
    if key == keys.UP and car_player.gear < car_player.total_gears:
        car_player.gear += 1
    elif key == keys.DOWN and car_player.gear > 1:
        car_player.gear -= 1
    elif key == keys.P and not world.paused:
        world.paused = True
    elif key == keys.R and not world.paused:
        reset_game()
    elif key == keys.M and not world.paused:
        screen.clear()
        main_menu.in_menu = True

def reset_game():
    global car_player, car_other
    world.game_won = 0
    world.game_lost = 0

    world.remove(car_player)
    world.remove(car_other)

    car_player = get_car(car_array, main_menu.player, 330, 500, False)
    car_other = get_car(car_array, main_menu.other, 130, 500, True, 1)

    world.add(car_player)
    world.add(car_other)

def move_other(player, other):
    # "50" defined in Car Class as C_MOVE
    other.y = 500 + ((player.distance - other.distance) * 50)

def assign_actors(car_array):
    for car in car_array:
        image = car['actor']
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
        draw_basic_info(car_object, other, screen)

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
        car_object.t_slip.set_reaction()
        car_object.throttle_position = 1.00
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

    if not main_menu.in_menu:
        show_stats(car_player, car_other)
    else:
        main_menu.show_names(screen)

def update(dt):
    if main_menu.in_menu:
        main_menu.show(world)

    if countdown_menu.in_countdown:
        countdown_menu.show(world)
    elif countdown_menu.check_finished():
        countdown_menu.finish_countdown(world)
        reset_game()

    # You can define the max distance in world.py - Default: 1000m
    win_status = check_win(car_player, car_other)

    if win_status == 1:
        win_menu.show(world)
        car_player.print_time_slip()
    elif win_status == -1:
        lose_menu.show(world)
        car_player.print_time_slip()

    if not world.paused:
        screen.clear()
        check_brake(car_player)
        set_acceleration(car_player)
        move_other(car_player, car_other)
        move_road(bk_1, bk_2, car_player)
        world.update(dt)

        #car_other.print_stats()
        car_player.print_stats()
    elif world.paused:
        if not main_menu.in_menu:
            pause_menu.show(world)

# Starting pygamezero simulation
world = World()

#Loading car files
car_array = load_cars()

#Welcome message
hello_message()

# Defines the 2 backgrounds
bk_1 = Image(Actor('road', anchor=('left', 'top')), 0, 0, "bk_1")
bk_2 = Image(Actor('road', anchor=('left', 'top')), 0, -800, "bk_2")

#For pause_menu
bt_voltar = Image(Actor('bt_voltar', anchor=('left', 'top')), 64, 375, "bt_voltar")
bt_sair = Image(Actor('bt_sair', anchor=('left', 'top')), 64, 490, "bt_sair")
bk_pause = Image(Actor('pause_bk', anchor=('left', 'top')), 0, 0, "bk_pause")

#For Win or Lose
bt_again = Image(Actor('bt_again', anchor=('left', 'top')), 64, 375, "bt_again")
bk_win = Image(Actor('win_bk', anchor=('left', 'top')), 0, 0, "bk_win")
bk_lose = Image(Actor('lose_bk', anchor=('left', 'top')), 0, 0, "bk_lose")

#For Main Menu
bt_next_player = Image(Actor('bt_next', anchor=('left', 'top')), 339, 323, "bt_next_player")
bt_next_other = Image(Actor('bt_next', anchor=('left', 'top')), 339, 385, "bt_next_other")
bt_prev_player = Image(Actor('bt_prev', anchor=('left', 'top')), 64, 323, "bt_prev_player")
bt_prev_other = Image(Actor('bt_prev', anchor=('left', 'top')), 64, 385, "bt_prev_other")
bt_play = Image(Actor('bt_play', anchor=('left', 'top')), 64, 493, "bt_play")
bt_sair_mm = Image(Actor('bt_sair', anchor=('left', 'top')), 64, 596, "bt_sair_mm")


#For Countdown
count_3 = Image(Actor('count_3', anchor=('left', 'top')), 0, 0, "count_3")
count_2 = Image(Actor('count_2', anchor=('left', 'top')), 0, 0, "count_2")
count_1 = Image(Actor('count_1', anchor=('left', 'top')), 0, 0, "count_1")
count_go = Image(Actor('count_go', anchor=('left', 'top')), 0, 0, "count_go")


# Create lists for the itens - Menus
pause_actors = [bk_pause, bt_voltar, bt_sair]
lose_actors = [bk_lose, bt_again, bt_sair]
win_actors = [bk_win, bt_again, bt_sair]
main_actors = [bk_pause, bt_prev_player, bt_next_player, bt_prev_other, \
    bt_next_other, bt_play, bt_sair_mm]
countdown_actors = [count_3, count_2, count_1, count_go]

# Create object for each menu
pause_menu = Menu(pause_actors)
lose_menu = Menu(lose_actors)
win_menu = Menu(win_actors)
main_menu = MainMenu(main_actors, car_array)
countdown_menu = Countdown(countdown_actors)

# Creates the first cars references
car_player = get_car(car_array, main_menu.player, 330, 500, False)
car_other = get_car(car_array, main_menu.other, 130, 500, True, 1)

# Add objects to World
world.add(bk_1)
world.add(bk_2)
world.add(car_player)
world.add(car_other)
