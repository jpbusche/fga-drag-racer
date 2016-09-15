class Car:
    #Drag constant for a Corvette
    C_DRAG = 0.4257

    def __intit__(self, mass, max_hp, max_toque):
        self.mass = mass
        self.hp = 0
        self.max_hp = max_hp
        self.max_toque = max_torque
        self.velocity = 0
        self.rpm = 1000
        self.engine_torque = 0;
        self.acceleration = 0
        self.forces = 0

    #Engine's forces
    def traction(self, gear_ratio, differential_ratio):
        # In foot-pounds
        self.hp = self.engine_torque * self.rpm / 5252

        #FDrive = Torque at 'x' rpm * gear_ratio * differential_ratio
        # * transmission_efficiency * wheel_radius
        # Wheel = 13.4 inches
        # Transmission efficiency - It's a guess
        f_drive = self.engine_torque * gear_ratio * differential_ratio * 0.7 * 0.34




    def calculate_forces(self):
        #Calculates moving resistance (MR = FDrag + FRollingResistance)
        f_drag = -(self.velocity * C_DRAG)

        #Rolling resistance should be at least 30 times more than FDrag
        #Tire moving resistance
        f_rr = f_drag * 30

        #Calculates the car's traction based on its configuration
        f_traction = traction()

        #Update car's forces
        self.forces = f_traction + f_rr + f_drag

    def calculate_velocity(self, dt):
        self.acceleration = self.forces / self.mass
        self.velocity = self.velocity + (dt * self.acceleration)
