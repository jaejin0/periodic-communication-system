import math
import random
import numpy as np

import time

class Robot:
    def __init__(self, id_number, natural_frequency, initial_angle, center_position, path_radius, robot_radius,
                 method, courier = False):
        # static states
        self.id_number = id_number
        self.natural_frequency = natural_frequency
        self.center_position = center_position
        self.path_radius = path_radius
        self.robot_radius = robot_radius
        self.method = method

        # dynamic states
        self.courier = courier
        self.angle = initial_angle
        self.control_frequency = 0
        self.robot_position = self.current_robot_position() 
        self.neighbors = {}

    def step(self):
        self.angle += self.control_frequency + self.natural_frequency
        self.robot_position = self.current_robot_position()

    def current_robot_position(self):
        x = self.center_position[0] + self.path_radius * math.cos(self.angle)
        y = self.center_position[1] + self.path_radius * math.sin(self.angle)
        return x, y

    def update_neighbor(self, neighbor):
        self.neighbors[neighbor.id_number] = neighbor     
        
    def met(self, neighbor): 
        self.update_neighbor(neighbor)

        match self.method:
            case 'coin_flip':
                if self.courier == neighbor.courier:
                    # flip a coin
                    random_number = random.randint(0, 1)
                    self.courier = bool(random_number)
                    return self.courier

            case 'myopic_heuristic':
                print('')

            case 'graph_based':
                print('')
            
            case 'full_courier':
                print('')
            
            case 'average':
                self.control_frequency = ((self.control_frequency + self.natural_frequency + neighbor.control_frequency + neighbor.natural_frequency) / 2) - self.natural_frequency

            case 'max':
                self.control_frequency = max(self.control_frequency + self.natural_frequency, neighbor.control_frequency + neighbor.natural_frequency) - self.natural_frequency
                
            case 'min':
                self.control_frequency = min(self.control_frequency + self.natural_frequency, neighbor.control_frequency + neighbor.natural_frequency) - self.natural_frequency
            
            case _:
                print("SOMETHING WRONG SOMETHING WRONG SOMETHING WRONG!!!")


