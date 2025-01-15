
import math
import pygame

from objects import Robot, Source, Destination
from renderer import Renderer

class Simulation:
    def __init__(self, seed=0, SCREEN_WIDTH=800, SCREEN_HEIGHT=600):
        # initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Periodic Communication System")

        match seed:
            case 0:
                self.robots = [] 
                # robot 0
                self.robots.append(Robot( 
                    center_x = 300,
                    center_y = 250,
                    center_radius = 50,
                    initial_angle = 1.0,
                    initial_angular_velocity = 0.1,
                    rendezvous = [[0, 1]]
                ))
                # robot 1
                self.robots.append(Robot(
                    center_x = 400,
                    center_y = 250,
                    center_radius = 50,
                    initial_angle = 1.0,
                    initial_angular_velocity = 0.1,
                    rendezvous = [[float("{:.3f}".format(math.pi)), 0]]
                ))

                self.sources = []
                # source 0
                self.sources.append(Source(
                    robot_id = 0,
                    src_angle = float("{:.3f}".format(math.pi))
                ))
               
                self.destinations = []
                # destination 0
                self.destinations.append(Destination(
                    robot_id = 1,
                    dest_angle = 0
                ))

        self.renderer = Renderer(self.screen, self.robots, self.sources, self.destinations)

    def step(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # transition
        for robot in self.robots:
            robot.transition()
        
        self.renderer.render_simulation(self.robots, self.sources, self.destinations) 

        self.robot_met()
        
        pygame.display.update()
        self.clock.tick(60)
   
    def terminate(self):
        pygame.quit()
        print("Game terminated")
        return True

    def robot_met(self):
        # check if the robots met
        n = len(self.robots)
        current_positions = [self.robots[i].get_robot_position() for i in range(n)]
        for i in range(n):
            x, y = current_positions[i]
            for j in range(n):
                if i == j:
                    continue
                _x, _y = current_positions[j]
                if math.sqrt((x - _x)**2 + (y - _y) **2) <= self.robots[i].robot_radius + self.robots[j].robot_radius:
                    # robot met
                    self.renderer.render_robot_met(self.robots[i]) 

    def action_choice(self):
        # action choice
        key = pygame.key.get_pressed()
        if key[pygame.K_a] == True and self.robots[0].angular_velocity <= self.robots[0].robot_max_velocity - 0.01:
            self.robots[0].angular_velocity += 0.01
        elif key[pygame.K_d] == True and self.robots[0].angular_velocity >= -self.robots[0].robot_max_velocity + 0.01:
            self.robots[0].angular_velocity -= 0.01
     
