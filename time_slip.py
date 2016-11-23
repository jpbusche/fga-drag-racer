import time
import car
import world

class Time_slip():
    def __init__(self):
        self.time_100kph = 0
        self.time_400m = 0
        self.speed_400m = 0
        self.time_finish = 0
        self.speed_finish = 0
        self.time_reaction = 0
        self.time_initial = time.time()

    def time_diff(self):
        return time.time() - self.time_initial

    def update_times(self, car):
        self.check_100kph(car)
        self.check_400m(car)
        self.time_finish = self.time_diff()
        self.speed_finish = car.velocity * 3.6

    def check_100kph(self, car):
        speed = car.velocity * 3.6
        if self.time_100kph == 0 and speed >= 100:
            self.time_100kph = self.time_diff()

    def check_400m(self, car):
        distance = car.distance
        if self.time_400m == 0 and distance >= 400:
            self.time_400m = self.time_diff()
            self.speed_400m = car.velocity * 3.6

    def set_reaction(self):
        if self.time_reaction == 0:
            self.time_reaction = self.time_diff()

    def print_slip(self, car):
        #This is a gambiarra for clear terminal
        for i in range(0,20):
            print("")

        print("----------------------------")
        print("Time Slip - " + car.name)
        print("----------------------------")
        print("0 - 100 Km/h: " + str("%.3f" % (self.time_100kph)) + "s")
        print("400m: " + str("%.3f" % (self.time_400m)) + "s @ " + \
            str("%.2f" % (self.speed_400m)) + "Km/h")
        print("Finish Line: " + str("%.3f" % (self.time_finish)) + "s @ " + \
            str("%.2f" % (self.speed_finish)) + "Km/h")
        print("Reaction Time: " + str("%.3f" % (self.time_reaction)) + "s")
        print("----------------------------")
