import sys
import pygame
import json
import matplotlib.pyplot as plt
import numpy as np
import copy
import csv
from datetime import datetime


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

PATH_THICKNESS = 2
PATH_COLOR = BLACK

class Simulation:
    def __init__(self, seed = 0, method = "coin_flip", human_mode = True, store_result = False):  
        self.seed = seed
        self.method = method 
        self.human_mode = human_mode
        self.store_result = store_result 
        print("Simulation Initialized")
        print(f"seed: {seed}")
        print(f"method: {method}") 
        print(f"human mode: {human_mode}") 
        print(f"store result: {store_result}")

        self.robots = []
        with open('seed.json') as file:
            data = json.load(file)[self.seed]
            for r in data['robots']:
                self.robots.append(Robot(
                        r['natural_frequency'], 
                        r['initial_angle'],
                        r['center_position'], 
                        r['path_radius'],
                        ROBOT_RADIUS,
                        method
                ))
        self.robot_num = len(data['robots'])
        print(f"number of robots: {self.robot_num}")

        # csv file to store data
        with open(f'./data/simulation_seed[{seed}]_method[{method}]_time[{datetime.now().strftime("%H:%M:%S")}].csv',
                  'w', newline='') as file:
            self.writer = csv.writer(file)

        # dynamic state
        self.current_robot_positions = [(0, 0)] * self.robot_num 
        self.update_current_robot_positions()
        self.robot_sync_state = [0] * self.robot_num # time counter from previous meeting 
        
        # game setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Multi-Robot Rendezvous Communication")
        self.timestep = 0

        # show initial state
        self.render()

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
        if self.store_result:
            self.store_data()
        
        # update simulation
        if self.human_mode:
            self.render()
        self.timestep += 1
    
    def render(self):
        self.screen.fill(WHITE) 
        for r in self.robots:
            pygame.draw.circle(self.screen, PATH_COLOR, r.center_position, r.path_radius, PATH_THICKNESS)
        for i, r in enumerate(self.robots): 
            x, y = r.current_robot_position()
            if self.robot_sync_state[i] > 0:
                pygame.draw.circle(self.screen, ROBOT_FLASH_COLOR, (x, y), ROBOT_RADIUS)
            else:
                pygame.draw.circle(self.screen, ROBOT_COLOR, (x, y), ROBOT_RADIUS)

        pygame.display.update()
        self.clock.tick(60)

    def update_current_robot_positions(self):
        for i, r in enumerate(self.robots):
            self.current_robot_positions[i] = r.current_robot_position()

    def check_meetings(self):
        for i in range(self.robot_num - 1):
            if self.robot_sync_state[i] > 0:
                continue
            for j in range(i + 1, self.robot_num):
                if self.robot_sync_state[j] > 0:
                    continue

                x1, y1 = self.current_robot_positions[i]
                x2, y2 = self.current_robot_positions[j]
                if (x1 - x2)**2 + (y1 - y2)**2 <= (2 * ROBOT_RADIUS)**2:
                    self.robots[i].met(copy.deepcopy(self.robots[j]))
                    self.robots[j].met(copy.deepcopy(self.robots[i]))

                    # flash
                    self.robot_sync_state[i] = FLASH_DURATION
                    self.robot_sync_state[j] = FLASH_DURATION

    def store_data(self):
        current_state = []
        for i, r in enumerate(self.robots):
            current_state.append(r.natural_frequency + r.control_frequency)
        self.writer.writerows(current_state) 
   
if __name__ == "__main__":
    seed = int(sys.argv[1])
    method = sys.argv[2]
    human_mode = sys.argv[3].lower() == 'true'
    store_result = sys.argv[4].lower() == 'true'

    simulation = Simulation(seed, method, human_mode, store_result)
    while True:
        simulation.step()
