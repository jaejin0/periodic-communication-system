import numpy as np
import networkx as nx
import pygame

# screen
WIDTH = 800
HEIGHT = 600

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Node:
    def __init__(self, angle, natural_frequency):
        self.angle = angle
        self.natural_frequency = natural_frequency
        self.angular_velocity = angular_velocity


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
        # random distribution of initial angles and natural frequencies 
        self.angles = 2 * np.pi * np.random.normal(size=N)
        self.natural_frequencies = 0.1 * np.random.normal(size=N)
        # a matrix representing connectivity between particles
        self.adj_mat = nx.to_numpy_array(nx.erdos_renyi_graph(n=N, p=1)) 

        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Kuramoto model simulation")
        self.timestep = pygame.time.get_ticks()

        self.center = (WIDTH // 2, HEIGHT // 2)
        self.radius = HEIGHT // 4
        self.circle_thickness = 2
        self.particle_radius = 5


    def step(self):
        self.angles += self.derivative()
        self.render()
        pygame.display.update()
        self.clock.tick(30)
    
    def derivative(self):
        angles_i, angles_j = np.meshgrid(self.angles, self.angles)
        interactions = self.adj_mat * np.sin(angles_j - angles_i)
        
        derivative = self.natural_frequencies + self.K * interactions.sum(axis=0)
        
        return derivative

    def render(self):
        self.screen.fill(WHITE) 
        pygame.draw.circle(self.screen, BLUE, self.center, self.radius, self.circle_thickness)
        for a in self.angles:
            x, y = self.center[0] + np.cos(a) * self.radius, self.center[1] + np.sin(a) * self.radius
            pygame.draw.circle(self.screen, RED, (x, y), self.particle_radius)


if __name__ == "__main__":
    model = Kuramoto(100, 3)
    while True:
        model.step()
