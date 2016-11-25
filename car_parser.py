import json
from car import Car

FILE_NAME = 'car_data.json'

def load_json():
    with open(FILE_NAME) as data_file:
        return json.load(data_file)

def car_decoder(obj):
    cars_array = []

    for car in obj:
        if '__type__' in car and car['__type__'] == 'Car':
            cars_array.append(car)
    return cars_array

def get_names(car_array):
    car_names = []

    for car in car_array:
        car_names.append(car['name'])
    return car_names

def find_car(car_array, name):
    for car in car_array:
        if name == car['name']:
            return Car(actor=car['actor'], name=car['name'], mass=car['mass'], \
                max_rpm=car['max_rpm'], differential_ratio=car['differential_ratio'],\
                torque_array=car['torque_array'], gear_ratio=car['gear_ratio'], \
                idle_rpm=car['idle_rpm'], wheel_radius=car['wheel_radius'], \
                total_gears=car['total_gears'])

def get_car(car_array, name, x_pos, y_pos, automatic, throttle_position=0):
    new_car = find_car(car_array, name)
    new_car.x = x_pos
    new_car.y = y_pos
    new_car.automatic = automatic
    new_car.throttle_position = throttle_position
    return new_car
