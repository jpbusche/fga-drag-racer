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
        self.gear = 0

    def find_max_torque(self):
        #To-do: Uses an array of some torque curves and interpolation
        torque_array = [[1000, 390], [2000, 440], [3000, 455], [4000, 470],
        [4400, 475], [5000, 460], [5000, 390]]

        for line in range(0,7):
            if self.rpm >= torque_array[line][0] or self.rpm < torque_array[line + 1][0]:
                return torque_array[line][1]


    #Engine's forces
    def traction(self, differential_ratio):
        wheel_radius = 0.33
        gear_ratio= [0.0, 2.66, 1.30, 1.78, 1.0, 0.74, 0.50]

        # Workarround for wheel rotation ratio (Diveded by 10)
        wheel_rotation_rate = self.velocity / wheel_radius / 10

        if self.rpm <= self.max_rpm:
            self.rpm = wheel_rotation_rate * gear_ratio[self.gear] * differential_ratio * 60 / 2 * math.pi
        elif self.throttle_position <= 0.05 and self.velocity < 8/3.6:
            self.rpm = 900
        elif self.rpm > self.max_rpm:
            self.rpm = self.max_rpm - 500
            return 0

        self.max_torque = self.find_max_torque()

        self.engine_torque = self.max_torque * self.throttle_position

        # Foot-pounds to N.m
        self.hp = (self.engine_torque * self.rpm / 5252) * 1.335

        self.crankshaft_torque = (gear_ratio[self.gear] * differential_ratio) * 0.7

        #FDrive = Torque at 'x' rpm * gear_ratio * differential_ratio
        # * transmission_efficiency * wheel_radius
        # Wheel = 13.4 inches
        # Transmission efficiency - It's a guess
        return self.engine_torque * self.crankshaft_torque / 0.34

    def calculate_forces(self):
        #Drag constant for a Corvette
        C_DRAG = 0.4257

        #Calculates moving resistance (MR = FDrag + FRollingResistance)
        f_drag = -(self.velocity * C_DRAG)

        #Rolling resistance should be at least 30 times more than FDrag
        #Tire moving resistance
        f_rr = f_drag * 30

        #Calculates the car's traction based on its configuration
        f_traction = self.traction(3.42)

        #Update car's forces
        self.forces = f_traction + f_rr + f_drag

    def calculate_velocity(self, dt):
        self.acceleration = self.forces / self.mass

        # Workarround for limit rpm
        if self.rpm <= self.max_rpm:
            self.velocity = self.velocity + (dt * self.acceleration)

    def update(self, dt):
        self.calculate_forces()
        self.calculate_velocity(dt)

        self.y -= self.velocity

        self.print_stats()

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
