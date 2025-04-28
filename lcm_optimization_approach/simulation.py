import pygame
import json
import matplotlib.pyplot as plt
import numpy as np


from robot import Robot

# screen
WIDTH = 1200
HEIGHT = 900

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# design
ROBOT_RADIUS = 4
ROBOT_COLOR = BLUE
ROBOT_FLASH_COLOR = RED
FLASH_DURATION = 20 # frames

PATH_THICKNESS = 1
PATH_COLOR = BLACK

class Simulation:
    def __init__(self, seed=0, discretization = 5):  
        self.seed = seed
        self.discretization = discretization
        print(f"initialize with seed: {seed}, discretization: {discretization}") 

        self.robots = []
        with open('seed.json') as file:
            data = json.load(file)[self.seed]
            print(f"seed id: {data.get('id', 'NULL')}")
            for r in data['robots']:
                self.robots.append(Robot(
                        round(r['natural_frequency'], self.discretization), 
                        round(r['initial_angle'], self.discretization),
                        r['center_position'], 
                        r['path_radius'],
                        ROBOT_RADIUS,
                        self.discretization
                ))
        self.robot_num = len(data['robots'])

        # dynamic state
        self.current_robot_positions = [(0, 0)] * self.robot_num 
        self.update_current_robot_positions()
        self.robot_sync_state = [0] * self.robot_num # time counter from previous meeting 
        
        # game setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Multi-Robot Rendezvous Synchronization Problem")
        self.timestep = 0

        # show initial state
        self.render()

        # data collection
        self.frequency_history = [[] for i in range(self.robot_num)]

    def step(self):
        # update states
        for r in self.robots:
            r.step()
        self.update_current_robot_positions()
        self.check_meetings()
        for i in range(self.robot_num):
            if self.robot_sync_state[i] > 0:
                self.robot_sync_state[i] -= 1

        # data collection
        if self.timestep % 60 == 0:
            self.store_data()

        if self.timestep % 6000 == 0:
            self.visualize_frequency_data()
        
        # update simulation
        self.render()
        self.timestep += 1
    
    def render(self):
        self.screen.fill(WHITE) 
        for r in self.robots:
            pygame.draw.circle(self.screen, PATH_COLOR, r.center_position, r.path_radius, PATH_THICKNESS)
        for i, r in enumerate(self.robots): 
            x, y = r.find_robot_position()
            if self.robot_sync_state[i] > 0:
                pygame.draw.circle(self.screen, ROBOT_FLASH_COLOR, (x, y), ROBOT_RADIUS)
            else:
                pygame.draw.circle(self.screen, ROBOT_COLOR, (x, y), ROBOT_RADIUS)


        pygame.display.update()
        self.clock.tick(60)

    def update_current_robot_positions(self):
        for i, r in enumerate(self.robots):
            self.current_robot_positions[i] = r.find_robot_position()

    def check_meetings(self):
        for i in range(self.robot_num - 1):
            if self.robot_sync_state[i] > 0:
                continue
            for j in range(i + 1, self.robot_num):
                if self.robot_sync_state[j] > 0:
                    continue

                x1, y1 = self.current_robot_positions[i]
                x2, y2 = self.current_robot_positions[j]
                if (x1 - x2)**2 + (y1 - y2)**2 <= ROBOT_RADIUS:
                    # update control frequencies
                    other_frequency = self.robots[j].natural_frequency + self.robots[j].control_frequency
                    chosen_frequency = self.robots[i].update_control_frequency(other_frequency)
                    self.robots[j].control_frequency = chosen_frequency - self.robots[j].natural_frequency
                    
                    # flash
                    self.robot_sync_state[i] = FLASH_DURATION
                    self.robot_sync_state[j] = FLASH_DURATION

                    print(f"SYNC between {i+1}, {j+1} to {chosen_frequency}")

    def store_data(self):
        for i, r in enumerate(self.robots):
            self.frequency_history[i].append(r.natural_frequency + r.control_frequency)

    def visualize_frequency_data(self):
        t = np.arange(0, len(self.frequency_history[0]), 1)
        for i in range(self.robot_num):
            plt.plot(t, self.frequency_history[i])
        plt.show()

if __name__ == "__main__": 
    simulation = Simulation()
    while True:
        simulation.step()
