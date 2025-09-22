import math
import numpy as np

import time

class Robot:
    def __init__(self, natural_frequency, initial_angle, center_position, path_radius, robot_radius,
                 method, courier = False):
        # static states
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

    def step(self):
        self.angle += self.control_frequency + self.natural_frequency
        self.robot_position = self.current_robot_position()

    def current_robot_position(self):
        x = self.center_position[0] + self.path_radius * math.cos(self.angle)
        y = self.center_position[1] + self.path_radius * math.sin(self.angle)
        return x, y

    def met(self, neighbor):
        
        match self.method:
            case 'coin_flip':
                print('coin_flip')

            case 'myopic_heuristic':

                print('coin_flip')

            case 'graph_based':

                print('coin flip')
            case 'full_courier':

                print('coin flip')
            case 'average':
                self.control_frequency = ((self.control_frequency + self.natural_frequency + neighbor.control_frequency + neighbor.natural_frequency) / 2) - self.natural_frequency

            case 'max':
                self.control_frequency = max(self.control_frequency + self.natural_frequency, neighbor.control_frequency + neighbor.natural_frequency) - self.natural_frequency
                
            case 'min':
                self.control_frequency = min(self.control_frequency + self.natural_frequency, neighbor.control_frequency + neighbor.natural_frequency) - self.natural_frequency
            
            case _:
                print("SOMETHING WRONG SOMETHING WRONG SOMETHING WRONG!!!")


