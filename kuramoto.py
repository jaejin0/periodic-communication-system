import numpy as np

class Node:
    def __init__(self, angle, natural_frequency):
        self.angle = angle
        self.natural_frequency = natural_frequency
        self.angular_velocity = angular_velocity

    def  

    def update_angle(self, derivative):
        self.angle += derivative
        self.limit_angle() 

    def limit_angle():
        self.angular_velocity = float("{:.4f}".format(self.angular_velocity))
        self.angle = float("{:.4f}".format(self.angle))
        if self.angle > np.pi or self.angle < np.pi:
            self.angle *= -1

class Kuramoto:
    def __init__(self, N=30, K=1): 
        self.N = N
        self.K = K
        self.angles = 2 * np.pi * np.random.normal(size=N)
        self.natural_frequencies = np.random.normal(size=N)


