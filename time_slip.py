""" Module """
import time

class TimeSlip:
    """
        This class is for creating a Time Slip for any car, with all the most
        important times and speed.
    """
    def __init__(self):
        """ Initiate instance with 0 values and time of creation """
        self.time_100kph = 0
        self.time_400m = 0
        self.speed_400m = 0
        self.time_finish = 0
        self.speed_finish = 0
        self.time_reaction = 0
        self.time_initial = time.time()

    def time_diff(self):
        """ Return the time diference between the time of creation and function
            call time.
        """
        return time.time() - self.time_initial

    def update_times(self, car_obj):
        """ Check all times """
        self.check_100kph(car_obj)
        self.check_400m(car_obj)
        self.time_finish = self.time_diff()
        self.speed_finish = car_obj.velocity * 3.6

    def check_100kph(self, car_obj):
        """ Check if car hit 100kph and saves its time """
        speed = car_obj.velocity * 3.6
        if self.time_100kph == 0 and speed >= 100:
            self.time_100kph = self.time_diff()

    def check_400m(self, car_obj):
        """ Check if car hit 400m and saves it time"""
        distance = car_obj.distance
        if self.time_400m == 0 and distance >= 400:
            self.time_400m = self.time_diff()
            self.speed_400m = car_obj.velocity * 3.6

    def set_reaction(self):
        """ Get reaction time on main.py """
        if self.time_reaction == 0:
            self.time_reaction = self.time_diff()

    def print_slip(self, car_obj):
        """ Print car's time slip """
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

        print("----------------------------")
        print("Time Slip - " + car_obj.name)
        print("----------------------------")
        print("0 - 100 Km/h: " + str("%.3f" % (self.time_100kph)) + "s")
        print("400m: " + str("%.3f" % (self.time_400m)) + "s @ " + \
            str("%.2f" % (self.speed_400m)) + "Km/h")
        print("Finish Line: " + str("%.3f" % (self.time_finish)) + "s @ " + \
            str("%.2f" % (self.speed_finish)) + "Km/h")
        print("Reaction Time: " + str("%.3f" % (self.time_reaction)) + "s")
        print("----------------------------")
