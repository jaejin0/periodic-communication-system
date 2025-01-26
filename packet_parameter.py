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
        self.rendezvous = {} # Node : angle pair # can be calculated using neighbor node's center and radius, but storing rendezvous angle reduce computation time
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
            self.rendezvous[neighbor] = np.arctan2(self.center[1] - neighbor.center[1], self.center[0] - neighbor.center[0])
        else:
            # no rendezvous point -> not a neighbor
            return

        self.neighbors.append(neighbor)
   
    def step(self):
        self.angles += self.derivative()
 
    def derivative(self):
        N = 0
        for n in self.neighbors:
            N += new_packet_num(n)
        
        summation = 0
        for n, r in zip(self.neighbors, self.rendezvous):
            new_packets = self.new_packet_num(n)
            summation += self.K * new_packets * np.sin((n.angle + n.rendezvous[self]) - (self.angle + self.rendezvous[n]))
        derivative = self.natural_frequency + (summation / N)

        return derivative

    def new_packet_num(self, neighbor) -> int:
        return neighbor.packets - self.packets if self.packets < neighbor.packets else 0

    def render(self):
        pygame.draw.circle(self.screen, BLUE, self.center1, self.radius1, self.circle_thickness)

class Simulation:
    def __init__(self, nodes: List[Node]): 
        # game setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Kuramoto-based Communication model simulation")
        self.timestep = pygame.time.get_ticks()

        # node setup
        self.nodes = nodes

    def step(self):
        for n in self.nodes:
            n.step()
        self.render()
        pygame.display.update()
        self.clock.tick(60)

    def render(self):
        self.screen.fill(WHITE) 
        for n in self.nodes:
            pygame.draw.circle(self.screen, BLUE, n.center, n.radius, n.circle_thickness)
            x, y = n.center[0] + np.cos(n.angle) * n.radius, n.center[1] + np.sin(n.angle) * n.radius
            pygame.draw.circle(self.screen, RED, (x, y), n.particle_radius)

if __name__ == "__main__":
    # a balance between the scale of natural frequencies and constant K matters. If not, the simulation does not converge
    # def __init__(self, angle=None, natural_frequency=None, K: float = 0.1
    #              center_x: int, center_y: int, radius: float):
    
    if len(sys.argv) == 3:
        N1, N2 = int(sys.argv[1]), int(sys.argv[2])
    elif len(sys.argv) == 4:
        N1, N2 = int(sys.argv[1]), int(sys.argv[2])
        K = float(sys.argv[3])
    
    model = Communication(N1, N2, K)
    while True:
        model.step()
