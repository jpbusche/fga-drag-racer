import math

class Car:
    def __init__(self, actor, name, mass, x, y, max_rpm):
        self.mass = mass
        self.name = name
        self.actor = actor

        self.x = x
        self.y = y

        self.hp = 0
        self.max_hp = 0
        self.max_torque = 0
        self.throttle_position = 0

        self.velocity = 0
        self.rpm = 1000
        self.max_rpm = max_rpm
        self.engine_torque = 0
        self.crankshaft_torque = 0
        self.acceleration = 0
        self.forces = 0

        self.differential_ratio = 3.42
        self.torque_array = [[1000, 390], [2000, 440], [3000, 455], [4000, 470],
        [4400, 475], [5000, 460], [5500, 390]]
        self.gear_ratio = [0.0, 2.66, 1.78, 1.30, 1.0, 0.74, 0.50]
        self.gear = 1

        self.C_BRAKE = 9000
        self.breaking = False

        self.road_increment = 0

    def auto_gear(self):
        change_gear_rpm = self.max_rpm
        v_max = 0.34 * 2 * math.pi *  self.max_rpm / (60 * self.gear_ratio[self.gear] * self.differential_ratio)

        if self.velocity >= v_max and self.gear < 6:
            self.gear += 1
            return

        if self.gear == 1:
            return

        v_max_lg = 0.34 * 2 * math.pi *  self.max_rpm / (60 * self.gear_ratio[self.gear - 1] * self.differential_ratio)
        if self.velocity < v_max_lg and self.gear > 1:
            self.gear -= 1

            #Workarround
            self.velocity -= 2
            return

    def find_max_torque(self):
        #To-do: Uses an array of some torque curves and interpolation
        for line in range(0,7):
            if self.rpm >= self.torque_array[line][0] or self.rpm < self.torque_array[line + 1][0]:
                return self.torque_array[line][1]


    #Engine's forces
    def traction(self):
        wheel_radius = 0.33

        engine_rotation_rate = self.velocity * 60 * self.gear_ratio[self.gear] * self.differential_ratio / (2 * math.pi * wheel_radius)
        self.rpm = engine_rotation_rate

        self.auto_gear()

        self.max_torque = self.find_max_torque()
        self.engine_torque = self.max_torque * self.throttle_position

        # Foot-pounds to N.m
        self.hp = (self.engine_torque * self.rpm / 5252) * 1.335
        self.crankshaft_torque = (self.gear_ratio[self.gear] * self.differential_ratio) * 0.7

        #FDrive = Torque at 'x' rpm * self.gear_ratio * differential_ratio
        # * transmission_efficiency * wheel_radius
        # Wheel = 13.4 inches
        # Transmission efficiency - It's a guess
        return self.engine_torque * self.crankshaft_torque / 0.34

    def breaking_force(self):
        return -1 * (self.C_BRAKE)

    def calculate_forces(self):
        C_DRAG = 0.3757
        C_RR = 0.25

        f_drag = -(self.velocity**2) * C_DRAG
        f_rr = -C_RR * self.velocity

        #Calculates the car's traction based on its configuration
        if self.breaking == True:
            f_traction = self.breaking_force()
        else:
            f_traction = self.traction()

        #Update car's forces
        self.forces = f_traction + f_rr + f_drag

    def calculate_velocity(self, dt):
        self.acceleration = self.forces / self.mass
        self.velocity = self.velocity + (dt * self.acceleration)

    def update(self, dt):
        C_MOVE = 30

        self.calculate_forces()
        self.calculate_velocity(dt)

        #self.y = self.y + -self.velocity * C_MOVE * dt
        self.road_increment = self.velocity * C_MOVE * dt

        #DEBUG
        #self.print_stats()

    def draw(self):
        self.actor.y = self.y
        self.actor.x = self.x
        self.actor.draw()

    def print_stats(self):
        print("----------------------------------")
        print("Name: " + self.name)
        print("X Position: " + str(self.x))
        print("Y Position: " + str(self.y))
        print("Velocity: " + str(self.velocity))
        print("RPM: " + str(self.rpm))
        print("Gear: " + str(self.gear))
        print("Forces: " + str(self.forces))
        print("HP: " + str(self.hp))
        print("Max HP: " + str(self.max_hp))
        print("Max torque: " + str(self.max_torque))
        print("----------------------------------\n")
