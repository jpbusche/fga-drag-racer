# Workarround for importing in pygamezero
import sys; sys.path.append('.')

#from FGAme import *
from car import *
from world import *
from background import *
import pygame

WIDTH = 450
HEIGHT = 800

def on_mouse_down(pos, button):
    if button == mouse.LEFT and bt_sair.actor.collidepoint(pos):
        pygame.display.quit()
        pygame.quit()
        quit()
    elif button == mouse.LEFT and bt_voltar.actor.collidepoint(pos):
        world.paused = False
        world.drawed_pause = False

        #Workarround
        bt_voltar.actor.pos = 1063.4, 375

        world.remove(bk_pause)
        world.remove(bt_sair)
        world.remove(bt_voltar)
    elif button == mouse.LEFT and bt_again.actor.collidepoint(pos):
        world.paused = False
        world.drawed_pause = False
        world.remove(bt_sair)
        world.remove(bt_again)

        if world.game_won:
            world.remove(bk_win)
        else:
            world.remove(bk_lose)

        reset_game(car_player, car_other)

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
        reset_game(car_player, car_other)

def reset_game(player, other):
    world.game_won = 0
    world.game_lost = 0
    player.__init__(Actor('car_player', anchor=('middle', 'top')), "Player", 1414.3 , 330, 500, 6800, False)
    other.__init__(Actor('car_ai', anchor=('middle', 'top')), "Computer", 1600 , 130, 500, 6800, True, 1)

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

def check_win(player, other):
    if world.game_won or world.game_lost:
        return 0
    if player.distance >= world.max_distance:
        world.game_won = 1
        return 1
    elif other.distance >= world.max_distance:
        world.game_lost = 1
        return -1

def pause_menu():
    if not world.drawed_pause:
        world.add(bk_pause)
        world.add(bt_sair)
        world.add(bt_voltar)
        world.draw()
        world.drawed_pause = True

def win_menu():
    if not world.drawed_pause:
        world.add(bk_win)
        world.add(bt_sair)
        world.add(bt_again)
        world.draw()
        world.drawed_pause = True

def lose_menu():
    if not world.drawed_pause:
        world.add(bk_lose)
        world.add(bt_sair)
        world.add(bt_again)
        world.draw()
        world.drawed_pause = True

def show_stats(car_object, other):
    rect_max_width = 410
    rect_height = 30

    rect_rpm_width = (car_object.rpm * rect_max_width) / (car_object.max_rpm * 1.05)
    rect_other_width = (other.distance * rect_max_width) / world.max_distance
    rect_player_width = (car_object.distance * rect_max_width) / world.max_distance

    RED = 200, 0, 0
    GREEN = 0, 200, 0
    BLACK = 0, 0, 0
    BLUE = 0, 0, 200

    rpm_color = GREEN if car_object.rpm < car_object.max_rpm else RED

    if not world.paused:
        screen.draw.text("Velocity (Km/h): " + str("%.0f" % (car_object.velocity * 3.6)), (20, 10), color="black")
        screen.draw.text("Gear: " + str(car_object.gear), (20, 30), color="black")
        screen.draw.text("RPM: " + str("%.0f" %  car_object.rpm), (20, 50), color="black")
        screen.draw.text("Distance (m): " + str("%.0f" %  car_object.distance), (20, 110), color="black")

        rect_rpm = Rect((20, 70), (rect_rpm_width, rect_height))
        rect_player_distance = Rect((20, 130), (rect_player_width, rect_height))
        rect_other_distance = Rect((20, 130), (rect_other_width, rect_height))
        rect_end_distance = Rect((430, 130), (2, rect_height))
        rect_end_rpm = Rect((430, 70), (2, rect_height))

        screen.draw.filled_rect(rect_rpm, rpm_color)
        screen.draw.filled_rect(rect_other_distance, RED)
        screen.draw.filled_rect(rect_player_distance, BLACK)
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

def draw():
    world.draw()
    show_stats(car_player, car_other)

def update(dt):
    # Here you can define the win distance - Default: 1000m in World Class
    win_status = check_win(car_player, car_other)

    if win_status == 1:
        world.paused = True
        win_menu()
    elif win_status == -1:
        world.paused = True
        lose_menu()

    if not world.paused:
        screen.clear()
        check_brake(car_player)
        set_acceleration(car_player)
        move_other(car_player, car_other)
        move_road(bk_1, bk_2, car_player)
        world.update(dt)
    elif world.paused:
        pause_menu()

# Starting pygamezero simulation
world = World()

#CAR CLASS: actor, name, mass, x, y, max_rpm, automatic, throttle_position = 0
car_player = Car(Actor('car_player', anchor=('middle', 'top')), "Player", 1414.3 , 330, 500, 6800, False)
car_other = Car(Actor('car_ai', anchor=('middle', 'top')), "Computer", 1600 , 130, 500, 6800, True, 1)

bk_1 = Background(Actor('road', anchor=('left', 'top')), 0, 0, "bk_1")
bk_2 = Background(Actor('road', anchor=('left', 'top')), 0, -800, "bk_2")

#For pause_menu
bt_voltar = Background(Actor('bt_voltar', anchor=('left', 'top')), 63.4, 375, "bt_voltar")
bt_sair = Background(Actor('bt_sair', anchor=('left', 'top')), 63.4, 490, "bt_sair")
bk_pause = Background(Actor('pause_bk', anchor=('left', 'top')), 0, 0, "bk_pause")

#For Win or Lose
bt_again = Background(Actor('bt_again', anchor=('left', 'top')), 63.4, 375, "bt_again")
bk_win = Background(Actor('win_bk', anchor=('left', 'top')), 0, 0, "bk_win")
bk_lose = Background(Actor('lose_bk', anchor=('left', 'top')), 0, 0, "bk_lose")

world.add(bk_1)
world.add(bk_2)
world.add(car_player)
world.add(car_other)
