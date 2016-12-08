import pygame

def draw_basic_info(car_object, other, screen):
    diff = str("%.0f" % (car_object.distance - other.distance))
    screen.draw.text("Velocity (Km/h): " + str("%.0f" % \
        (car_object.velocity * 3.6)), (20, 10), color="black")
    screen.draw.text("Gear: " + str(car_object.gear), (20, 30), color="black")
    screen.draw.text("RPM: " + str("%.0f" %  car_object.rpm), (20, 50), color="black")
    screen.draw.text("Distance (m): " + str("%.0f" %  car_object.distance) + \
        "  |    Difference(m): " + diff, (20, 110), color="black")

def set_rect_sizes(car_object, other, world):
    rects = {}

    rects['rect_max_width'] = 410
    rects['rect_height'] = 30
    rects['rect_rpm_width'] = (car_object.rpm * rects['rect_max_width']) / \
        (car_object.max_rpm * 1.05)
    rects['rect_other_width'] = (other.distance * rects['rect_max_width']) / \
        world.max_distance
    rects['rect_player_width'] = (car_object.distance * \
        rects['rect_max_width']) / world.max_distance

    return rects

def move_road(back_1, back_2, player):
    back_increment = int(player.road_increment)

    if back_1.y > 800:
        back_1.y = -(800 - back_2.y)
    if back_2.y > 800:
        back_2.y = -(800 - back_1.y)

    back_1.y = back_1.y + back_increment
    back_2.y = back_2.y + back_increment

def quit_game():
    pygame.display.quit()
    quit()

def hello_message():
    print("Welcome to FGA DRAG RACER!\n" +
        "By: João Paulo Busche and Matheus de Oliveira\n" +
        "Universidade de Brasília - Campus Gama - 2.2016 - Física para Jogos\n\n" +
        "Follow us on GitHub:  https://github.com/jpbusche/fis-jogos\n" +
        "------------------------------------------------------------------\n" +
        "CONTROLS:\nSPACE - Throttle\nUP - Next Gear\nDOWN - Previous Gear" +
        "\nP - Pause Menu\nM - Main Menu\nB - Break\nR - Secret Reset")
