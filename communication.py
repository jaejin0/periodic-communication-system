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

class Communication:
    def __init__(self, N: list[int]=[1, 1], K=1): 
        self.N = N
        self.K = K
        # random distribution of initial angles and natural frequencies 
        self.angles = np.array([np.random.normal(loc=0, scale= 2 * np.pi, size=n) for n in N]).flatten()
        self.natural_frequencies = np.array([np.random.normal(loc=0.01, scale=0.01, size=n) for n in N]).flatten()
        # a matrix representing connectivity between particles
        self.adj_mat = nx.to_numpy_array(nx.erdos_renyi_graph(n=sum(N), p=1)) 

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
        self.circle_thickness = 2
        self.particle_radius = 5

    def step(self):
        self.angles += self.derivative()
        self.render()
        pygame.display.update()
        self.clock.tick(60)
    
    def derivative(self):
        '''
        index indicates what derivative it wants to calculate for
        '''
        angles_i, angles_j = np.meshgrid(self.angles, self.angles)
        interactions = self.adj_mat * np.sin(angles_j - angles_i)
        
        derivative = self.natural_frequencies.flatten() + self.K * interactions.sum(axis=0) / sum(self.N)
        return derivative

    def render(self):
        self.screen.fill(WHITE) 
        pygame.draw.circle(self.screen, BLUE, self.center1, self.radius1, self.circle_thickness)
        pygame.draw.circle(self.screen, BLUE, self.center2, self.radius2, self.circle_thickness)
        for a in self.angles[0:self.N[0]]:
            x, y = self.center1[0] + np.cos(a) * self.radius1, self.center1[1] + np.sin(a) * self.radius1
            pygame.draw.circle(self.screen, RED, (x, y), self.particle_radius)
        for a in self.angles[self.N[1]:]:
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
    
    model = Communication([N1, N2], K)
    while True:
        model.step()
