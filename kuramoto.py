import numpy as np
import networkx as nx
import pygame
import sys

# screen
WIDTH = 800
HEIGHT = 600

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Kuramoto:
    def __init__(self, N=100, K=1): 
        self.N = N
        self.K = K
        # random distribution of initial angles and natural frequencies 
        self.angles = np.random.normal(loc=0, scale= 2 * np.pi, size=N)
        self.natural_frequencies = np.random.normal(loc=0.01, scale=0.01, size=N)
        # a matrix representing connectivity between particles
        self.adj_mat = nx.to_numpy_array(nx.erdos_renyi_graph(n=N, p=1)) 

        # game setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Kuramoto model simulation")
        self.timestep = pygame.time.get_ticks()

        # configuration
        self.center = (WIDTH // 2, HEIGHT // 2)
        self.radius = HEIGHT // 4
        self.circle_thickness = 2
        self.particle_radius = 5


    def step(self):
        self.angles += self.derivative()
        self.render()
        pygame.display.update()
        self.clock.tick(60)
    
    def derivative(self):
        angles_i, angles_j = np.meshgrid(self.angles, self.angles)
        interactions = self.adj_mat * np.sin(angles_j - angles_i)
        
        derivative = self.natural_frequencies + self.K * interactions.sum(axis=0) / self.N
        return derivative

    def render(self):
        self.screen.fill(WHITE) 
        pygame.draw.circle(self.screen, BLUE, self.center, self.radius, self.circle_thickness)
        for a in self.angles:
            x, y = self.center[0] + np.cos(a) * self.radius, self.center[1] + np.sin(a) * self.radius
            pygame.draw.circle(self.screen, RED, (x, y), self.particle_radius)


if __name__ == "__main__":
    # a balance between the scale of natural frequencies and constant K matters. If not, the simulation does not converge
    N = 100
    K = 0.1
    
    if len(sys.argv) == 2:
        N = int(sys.argv[1])
    elif len(sys.argv) == 3:
        N, K = int(sys.argv[1]), float(sys.argv[2])

    model = Kuramoto(N, K)
    while True:
        model.step()
