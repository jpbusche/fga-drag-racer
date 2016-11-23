from menu import *
from car_parser import get_names

class Main_menu(Menu):
    def __init__(self, actors, cars):
        self.actors = actors
        self.cars = get_names(cars)
        self.cars_len = len(cars)
        self.player = self.cars[0]
        self.player_index = 0
        self.other = self.cars[1]
        self.other_index = 1
        self.in_menu = True
        self.id = "Main Menu"

    def next_car(self, target):
        if target == "player":
            new_index = (self.player_index + 1) % self.cars_len
            self.player = self.cars[new_index]
            self.player_index = new_index
        elif target == "other":
            new_index = (self.other_index + 1) % self.cars_len
            self.other = self.cars[new_index]
            self.other_index = new_index

    def prev_car(self, target):
        if target == "player":
            new_index = (self.player_index - 1) % self.cars_len
            self.player = self.cars[new_index]
            self.player_index = new_index
        elif target == "other":
            new_index = (self.other_index - 1) % self.cars_len
            self.other = self.cars[new_index]
            self.other_index = new_index

    def show_names(self, screen):
        screen.draw.text(self.player, centerx=225, top= 338, color="black")
        screen.draw.text(self.other, centerx=225, top = 400, color="black")
