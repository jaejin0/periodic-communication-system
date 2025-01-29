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
    def __init__(self, angle=None, natural_frequency=None, K: float = 0.1,
                 center_x: int = 0, center_y: int = 0, radius: float = 30,
                 max_derivative: float = float('inf'), min_derivative: float = float('-inf'),
                 source: bool = False, is_absolute_difference: bool = False):
        # initial values
        self.angle = angle if angle else np.random.normal(loc=0, scale=2*np.pi)
        self.natural_frequency = natural_frequency if natural_frequency else np.random.normal(loc=0, scale=0.03)
        self.max_derivative, self.min_derivative = max_derivative, min_derivative 
        self.K = K
        self.center = (center_x, center_y)
        self.radius = radius
        self.is_absolute_difference = is_absolute_difference
        self.packets = 0 # as packets intended to flow in one direction, counting packets work fine without storing packet ids
        
        # updated with add_neighbor function 
        self.neighbors = []
        self.rendezvous = {} # Node : angle pair 
        self.adj_mat = nx.to_numpy_array(nx.erdos_renyi_graph(n=0, p=1)) 

        # configured for rendering 
        self.circle_color = BLUE
        self.circle_thickness = 2
        self.particle_color = RED
        self.particle_radius = 5
        self.color_timer = 0

        # assign this node to receive source randomly
        self.source = source 
        self.source_random_param = 0.01 if source else 0

    def add_neighbor(self, neighbor):
        epsilon = 3
        center_to_center_distance = math.sqrt((self.center[0] - neighbor.center[0])**2 + (self.center[1] - neighbor.center[1])**2) 
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
        derivative = max(self.min_derivative, min(self.max_derivative, self.derivative()))
        self.angle += derivative
        self.color_timer -= 1
        if self.source:
            if np.random.random() < self.source_random_param:
                self.packets += 1
                self.change_particle_color(BLACK)
                print("Packet added!")
        if self.color_timer == 0 and self.particle_color != RED:
            self.particle_color = RED
        self.met_neighbor()

    def change_particle_color(self, color):
        self.particle_color = color
        self.color_timer = 10

    def derivative(self):
        N = len(self.neighbors)

        summation = 0
        for n, r in zip(self.neighbors, self.rendezvous):
            new_packets = self.new_packet_num(n)
            summation += self.K * new_packets * np.sin((n.angle + n.rendezvous[self]) - (self.angle + self.rendezvous[n]))
        derivative = self.natural_frequency + (summation / N)
        return derivative

    def new_packet_num(self, neighbor) -> int:
        if self.is_absolute_difference: # both sides of packet delivery synchronize
            return abs(neighbor.packets - self.packets)
        else: # only the particle without packets synchronize to the other particle with new packet
            return max(neighbor.packets - self.packets, 0)

    def met_neighbor(self):
        x, y = self.particle_position()
        for n in self.neighbors:
            n_x, n_y = n.particle_position()
            particle_to_particle_distance = math.sqrt((x - n_x)**2 + (y - n_y)**2)
            if particle_to_particle_distance < self.particle_radius + n.particle_radius:
                # met
                self.receive_packets(n)

    def receive_packets(self, neighbor):
        if self.new_packet_num(neighbor) > 0:
            self.packets = neighbor.packets
            self.change_particle_color(GREEN)

    def particle_position(self):
        x = self.center[0] + self.radius * math.cos(self.angle)
        y = self.center[1] + self.radius * math.sin(self.angle)
        return x, y

class Simulation:
    def __init__(self, nodes: list[Node]): 
        # game setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Kuramoto-based Communication model simulation")
        self.timestep = 0

        # node setup
        self.nodes = nodes
        for i in range(len(nodes)):
            for j in range(len(nodes)):
                if i == j:
                    continue
                self.nodes[i].add_neighbor(self.nodes[j])

    def step(self):
        if self.timestep % 300 == 0:
            print("=============")
            print("Node | Packet")
            for i, n in enumerate(self.nodes):
                print(f"{i}    | {n.packets}")
            print("-------------")
        
        for n in self.nodes:
            n.step()
        self.render()
        pygame.display.update()
        self.clock.tick(60)
        self.timestep += 1

    def render(self):
        self.screen.fill(WHITE) 
        for n in self.nodes:
            pygame.draw.circle(self.screen, n.circle_color, n.center, n.radius, n.circle_thickness)
        for n in self.nodes: 
            x, y = n.particle_position()
            pygame.draw.circle(self.screen, n.particle_color, (x, y), n.particle_radius)

if __name__ == "__main__":
    # a balance between the scale of natural frequencies and constant K matters. If not, the simulation does not converge
    # def __init__(self, angle=None, natural_frequency=None, K: float = 0.1
    #              center_x: int, center_y: int, radius: float):
   
    K = 0.1
    is_absolute_difference = True
    if len(sys.argv) == 2:
        K = float(sys.argv[1]) 


    nodes = [
        Node(source = True, natural_frequency = 0.02, K = K, center_x = 300, center_y = 300, radius = 50, is_absolute_difference = is_absolute_difference),
        Node(natural_frequency = -0.01, K = K, center_x = 400, center_y = 300, radius = 50, is_absolute_difference = is_absolute_difference),
        Node(natural_frequency = 0.02, K = K, center_x = 500, center_y = 300, radius = 50, is_absolute_difference = is_absolute_difference) 
    ]
    
    model = Simulation(nodes)
    while True:
        model.step()
