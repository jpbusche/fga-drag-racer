import math
from time_slip import TimeSlip

class Car(object):
    def __init__(self, actor, name, mass, differential_ratio, torque_array, \
        gear_ratio, max_rpm, x=0, y=0, automatic=False, \
        throttle_position=0, idle_rpm=1000, wheel_radius=15, \
        total_gears=6):

        self.mass = mass
        self.name = name
        self.actor = actor
        self.automatic = automatic

        self.x = x
        self.y = y
        self.id = "NoMoreBUGS"

        self.t_slip = TimeSlip()

        self.hp = 0
        self.max_hp = 0
        self.max_torque = 0
        self.throttle_position = throttle_position

        self.velocity = 0
        self.idle_rpm = idle_rpm
        self.rpm = 0
        self.max_rpm = max_rpm
        self.engine_torque = 0
        self.crankshaft_torque = 0
        self.acceleration = 0
        self.distance = 0
        self.forces = 0

        self.differential_ratio = differential_ratio
        self.torque_array = torque_array
        self.gear_ratio = gear_ratio
        self.gear = 1
        self.total_gears = total_gears

        self.C_BRAKE = 9000
        self.breaking = False

        # Inches to m
        self.wheel_radius = wheel_radius / 39.370

        self.road_increment = 0

        self.initial_velocity()

    def auto_gear(self):
        wheel_circumference = self.wheel_radius * 2 * math.pi
        differential_turn = 60 * self.differential_ratio
        rpm_percentage = self.max_rpm * 0.7

        v_max = wheel_circumference *  rpm_percentage / \
            (self.gear_ratio[self.gear] * differential_turn)

        if self.velocity >= v_max and self.gear < self.total_gears:
            self.gear += 1
            return

        if self.gear == 1:
            return

        #Lower Gear
        v_max_lg = wheel_circumference *  rpm_percentage / \
            (self.gear_ratio[self.gear - 1] * differential_turn)

        if self.velocity < v_max_lg and self.gear > 1:
            self.gear -= 1

            #Workarround
            self.velocity -= 2
            return

    def rev_limiter(self):
        if self.rpm >= (self.max_rpm * 1.05):
            self.rpm -= 300
            return 1
        else:
            return 0

    def engine_breaking(self):
        if self.throttle_position == 0.02 and self.rpm > 1000:
            return 1
        else:
            return 0

    def find_max_torque(self):
        size = len(self.torque_array) - 1

        if self.rpm <= self.torque_array[0][0]:
            return self.torque_array[0][1]
        elif self.rpm >= self.torque_array[size][0]:
            return self.torque_array[size][1]

        for line in range(size):
            line_torque = self.torque_array[line][1]
            line_rpm = self.torque_array[line][0]

            next_line_torque = self.torque_array[line + 1][1]
            next_line_rpm = self.torque_array[line + 1][0]

            if self.rpm >= line_rpm and self.rpm < next_line_rpm:
                actual_rpm_percentage = (self.rpm/next_line_rpm) * 100
                return linear_guess(line_torque, next_line_torque, actual_rpm_percentage)

    #Engine's forces
    def traction(self):
        self.rpm = self.velocity * 60 * self.gear_ratio[self.gear] * \
            self.differential_ratio / (2 * math.pi * self.wheel_radius)

        if self.automatic:
            self.auto_gear()

        if self.rev_limiter():
            return 0

        if self.engine_breaking():
            return self.velocity * -50

        self.max_torque = self.find_max_torque()
        self.engine_torque = self.max_torque * self.throttle_position
        #torque_wheel = self.engine_torque * self.gear_ratio[self.gear] * self.differential_ratio

        # Foot-pounds to N.m
        self.hp = ((self.engine_torque * 0.737) * self.rpm / 5252)
        self.crankshaft_torque = (self.gear_ratio[self.gear] * self.differential_ratio)

        #FDrive = Torque at 'x' rpm * self.gear_ratio * differential_ratio
        # * transmission_efficiency * wheel_radius
        # Transmission efficiency - It's a guess - 0.7 (range 0-1)
        return self.engine_torque * self.crankshaft_torque / self.wheel_radius * 0.7

    def breaking_force(self):
        return -1 * (self.C_BRAKE)

    def calculate_forces(self):
        C_DRAG = 0.3757
        C_RR = 0.25

        f_drag = -(self.velocity**2) * C_DRAG
        f_rr = -C_RR * self.velocity

        #Calculates the car's traction based on its configuration
        if self.breaking:
            f_traction = self.breaking_force()
        else:
            f_traction = self.traction()

        #Update car's forces
        self.forces = f_traction  + f_rr + f_drag

    def calculate_velocity(self, dt):
        self.acceleration = self.forces / self.mass
        self.velocity = self.velocity + (dt * self.acceleration)

    def calculate_distance(self, dt):
        self.distance += self.velocity * dt

    def initial_velocity(self):
        self.velocity = self.wheel_radius * (2 * math.pi) *  self.idle_rpm / \
            (60 * self.gear_ratio[self.gear] * self.differential_ratio)

    def update(self, dt):
        C_MOVE = 50

        self.calculate_forces()
        self.calculate_velocity(dt)
        self.calculate_distance(dt)

        self.t_slip.update_times(self)

        #self.y = self.y + -self.velocity * C_MOVE * dt
        self.road_increment = self.velocity * C_MOVE * dt

    def draw(self):
        self.actor.y = self.y
        self.actor.x = self.x
        self.actor.draw()

    def print_stats(self):
        print("----------------------------------")
        print("Name: " + self.name)
        print("Distance Traveled (m):" + str(self.distance))
        print("Velocity (m/s): " + str(self.velocity))
        print("RPM: " + str(self.rpm))
        print("Gear: " + str(self.gear))
        print("Forces (N): " + str(self.forces))
        print("cv: " + str(self.hp * 1.013))
        print("Max torque (Nm): " + str(self.max_torque))
        print("----------------------------------\n")

    def print_time_slip(self):
        self.t_slip.print_slip(self)

def linear_guess(min_value, max_value, percentage):
    difference = max_value - min_value
    return ((difference * percentage)/100) + min_value
