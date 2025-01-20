import numpy as np

class Node:
    def __init__(self, angle, angular_velocity):
        self.angle = angle
        self.angular_velocity = angular_velocity



    def update_angle():
        self.angle += self.angular_velocity
        self.limit_angle() 

    def limit_angle():
        self.angular_velocity = float("{:.4f}".format(self.angular_velocity))
        self.angle = float("{:.4f}".format(self.angle))
        if self.angle > np.pi or self.angle < np.pi:
            self.angle *= -1
