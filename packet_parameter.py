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
        self.packets = 0 # as packets intended to flow in one direction, counting packets work fine without storing packet ids
        
        # updated with add_neighbor function 
        self.neighbors = []
        self.rendezvous = [] # can be calculated using neighbor node's center and radius, but storing rendezvous angle reduce computation time
        self.adj_mat = nx.to_numpy_array(nx.erdoes_renyi_graph(n=0, p=1)) 

        # configured for rendering 
        self.circle_thickness = 2
        self.particle_radius = 5

    def add_neighbor(self, neighbor: Node):
        epsilon = 3
        center_to_center_distance = math.sqrt(((self.center[0] - neighbor.center[0])**2) + ((self.center[1] - neighbor.center[1])**2)) 
        # if center_to_center_distance <= self.radius + neighbor.radius:
            # two rendezvous points
        if abs(center_to_center_distance - (self.radius + neighbor.radius)) <= epsilon:
            # one rendezvous points
            self.rendezvous.append(np.arctan2(self.center[1] - neighbor.center[1], self.center[0] - neighbor.center[0])
        else:
            # no rendezvous point -> not a neighbor
            return

        self.neighbors.append(neighbor)
    
    def derivative1(self):
        self.adj_mat = nx.to_numpy_array(nx.erdos_renyi_graph(n=self.new_packet_num(), p=1))

        angles = np.concatenate((self.angles1 + self.rendezvous1, self.angles2 + self.rendezvous2))
        angles_i, angles_j = np.meshgrid(angles, angles)
        interactions = self.adj_mat * np.sin(angles_j - angles_i)
       
        adjust_frequencies = self.K * interactions.sum(axis=0) / (self.N1 + self.N2)
        derivative = self.natural_frequencies1 + adjust_frequencies[:self.N1] 

        return derivative

    def new_packet_num(self):
        new_packet = 0
        for n in self.neighbors:
            if self.packets < n.packets:
                new_packets += (n.packets - self.packets)
        return new_packets

    def find_angles(self):
        

class Simulation:
    def __init__(self): 
        # game setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Kuramoto-based Communication model simulation")
        self.timestep = pygame.time.get_ticks()

    def step(self):
        self.angles1 += self.derivative1()
        self.angles2 += self.derivative2()
        self.render()
        pygame.display.update()
        self.clock.tick(60)
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
