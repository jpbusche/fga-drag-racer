from menu import Menu
import pygame

class Countdown(Menu):
    def __init__(self, backgrounds=None):
        Menu.__init__(self, None)
        self.backgrounds = backgrounds
        self.actual = backgrounds[0]
        self.in_countdown = False
        self.start_time = 0
        self.id = "Countdown"

    def draw(self):
        if self.in_countdown:
            self.update()
            self.actual.draw()

    def remove_from_screen(self):
        self.actual.actor.pos = 3000, 0

    def start_countdown(self):
        self.start_time = pygame.time.get_ticks()
        self.in_countdown = True

    def finish_countdown(self, world):
        self.start_time = 0
        self.destroy(world)

    def check_finished(self):
        return not self.in_countdown and self.start_time != 0

    def update(self):
        miliseconds = 1000
        seconds = (pygame.time.get_ticks() - self.start_time) / miliseconds

        if seconds <= 1:
            self.actual = self.backgrounds[0]
        elif seconds <= 2:
            self.actual = self.backgrounds[1]
        elif seconds <= 3:
            self.actual = self.backgrounds[2]
        elif seconds <= 3.5:
            self.actual = self.backgrounds[3]
        else:
            self.in_countdown = False
