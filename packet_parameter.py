import numpy as np
import networkx as nx
import math
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

class Node:
    def __init__(self, angle=None, natural_frequency=None, K: float = 0.1
                 center_x: int, center_y: int, radius: float):
        # initial values
        self.angle = angle if angle else np.random.normal(loc=0, scale=2*np.pi)
        self.natural_frequency = natural_frequency if natural_frequency else np.random.normal(loc=0.02, scale=0.01)
        self.K = K
        self.center = (center_x, center_y)
        self.radius = radius

        # updated with 
        self.neighbors = []
        self.rendezvous = [] # can be calculated using neighbor node's center and radius, but storing rendezvous angle reduce computation time
        
        self.packets = 0 # as packets intended to flow in one direction, counting packets work fine without storing packet ids
    
    def add_neighbor(self, neighbor: Node):
        self.neighbors.append(neighbor)
        self.rendezvous.append(self.compute_rendezvous(neighbor))

    def compute_rendezvous(self, neighbor: Node):
        center_to_center_distance = math.sqrt(((self.center[0] - neighbor.center[0])**2) + ((self.center[1] - neighbor.center[1])**2)) 

class Communication:
    def __init__(self, N1=1, N2=1, K=1): 
        self.N1 = N1
        self.N2 = N2
        self.K = K
        # random distribution of initial angles and natural frequencies 
        self.angles1 = np.random.normal(loc=0, scale= 2 * np.pi, size=N1)
        self.angles2 = np.random.normal(loc=0, scale= 2 * np.pi, size=N2)
        self.natural_frequencies1 = np.random.normal(loc=0.02, scale=0.01, size=N1)  
        self.natural_frequencies2 = np.random.normal(loc=0.02, scale=0.01, size=N2)
        # a matrix representing connectivity between particles
        self.adj_mat = nx.to_numpy_array(nx.erdos_renyi_graph(n=N1+N2, p=1)) 

        # game setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Kuramoto-based Communication model simulation")
        self.timestep = pygame.time.get_ticks()

        # configuration
        self.radius1 = HEIGHT // 4
        self.radius2 = HEIGHT // 4
        self.center1 = ((WIDTH // 2) - ((self.radius1 + self.radius2) / 2), HEIGHT // 2)
        self.center2 = ((WIDTH // 2) + ((self.radius1 + self.radius2) / 2), HEIGHT // 2)
        self.rendezvous1 = 0
        self.rendezvous2 = np.pi 
        self.circle_thickness = 2
        self.particle_radius = 5

    def step(self):
        self.angles1 += self.derivative1()
        self.angles2 += self.derivative2()
        self.render()
        pygame.display.update()
        self.clock.tick(60)
    
    def derivative1(self):
        angles = np.concatenate((self.angles1 + self.rendezvous1, self.angles2 + self.rendezvous2))
        angles_i, angles_j = np.meshgrid(angles, angles)
        interactions = self.adj_mat * np.sin(angles_j - angles_i)
       
        adjust_frequencies = self.K * interactions.sum(axis=0) / (self.N1 + self.N2)
        derivative = self.natural_frequencies1 + adjust_frequencies[:self.N1] 
        
        return self.natural_frequencies1

        return derivative

    def derivative2(self):
        angles = np.concatenate((self.angles1 + self.rendezvous1, self.angles2 + self.rendezvous2))
        angles_i, angles_j = np.meshgrid(angles, angles)
        interactions = self.adj_mat * np.sin(angles_j - angles_i)
       
        adjust_frequencies = self.K * interactions.sum(axis=0) / (self.N1 + self.N2)
        derivative = self.natural_frequencies2 + adjust_frequencies[self.N1:] 
        return derivative

    def render(self):
        self.screen.fill(WHITE) 
        pygame.draw.circle(self.screen, BLUE, self.center1, self.radius1, self.circle_thickness)
        pygame.draw.circle(self.screen, BLUE, self.center2, self.radius2, self.circle_thickness)
        for a in self.angles1:
            x, y = self.center1[0] + np.cos(a) * self.radius1, self.center1[1] + np.sin(a) * self.radius1
            pygame.draw.circle(self.screen, RED, (x, y), self.particle_radius)
        for a in self.angles2:
            x, y = self.center2[0] + np.cos(a) * self.radius2, self.center2[1] + np.sin(a) * self.radius2
            pygame.draw.circle(self.screen, RED, (x, y), self.particle_radius)


if __name__ == "__main__":
    # a balance between the scale of natural frequencies and constant K matters. If not, the simulation does not converge
    N1, N2 = 1, 1
    K = 0.1
    
    if len(sys.argv) == 3:
        N1, N2 = int(sys.argv[1]), int(sys.argv[2])
    elif len(sys.argv) == 4:
        N1, N2 = int(sys.argv[1]), int(sys.argv[2])
        K = float(sys.argv[3])
    
    model = Communication(N1, N2, K)
    while True:
        model.step()
