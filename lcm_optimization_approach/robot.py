import math
import numpy as np

import time

class Robot:
    def __init__(self, natural_frequency, initial_angle, center_position, path_radius, robot_radius, discretization = 10):
        self.discretization = discretization # affects frequencies to enable optimization computing
        self.natural_frequency = self.prune_decimal_points(natural_frequency)
        self.center_position = center_position
        self.path_radius = path_radius
        self.robot_radius = robot_radius
    
        self.angle = initial_angle
        self.control_frequency = 0
        self.robot_position = self.find_robot_position() 

        self.pi = self.prune_decimal_points(math.pi)
        self.frequency_upper_bound = 0.06
        self.frequency_lower_bound = 0

    def step(self):
        self.angle += self.control_frequency + self.natural_frequency
        self.angle %= 2 * math.pi    
        
        self.robot_position = self.find_robot_position()

    def find_robot_position(self):
        x = self.center_position[0] + self.path_radius * math.cos(self.angle)
        y = self.center_position[1] + self.path_radius * math.sin(self.angle)
        return x, y

    def update_control_frequency(self, other_frequency):
        my_frequency = self.control_frequency + self.natural_frequency

        my_frequency = int(my_frequency * 10 ** self.discretization)
        other_frequency = int(other_frequency * 10 ** self.discretization)

        minimum_value = float("inf")
        minimum_frequency = None
        
        
        
        for freq in range(int(self.frequency_lower_bound * 10 ** self.discretization), int(self.frequency_upper_bound * 10 ** self.discretization)):
            cur_value = (np.lcm(freq, my_frequency) / freq) + (np.lcm(freq, other_frequency) / freq)
            if minimum_value > cur_value:
                minimum_frequency = freq
                minimum_value = cur_value 

            # print(f"freq: {freq} | my_frequency: {my_frequency}")
            # print(minimum_value)
            # print(minimum_frequency)

        minimum_frequency /= 10 ** self.discretization

        self.control_frequency = self.prune_decimal_points(minimum_frequency - self.natural_frequency)
        
        return minimum_frequency

    def prune_decimal_points(self, n):
        return float("{:.{}f}".format(n, self.discretization))


