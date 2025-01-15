import pygame
import math

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Renderer:
    def __init__(self, screen, robots, sources, destinations):
        self.screen = screen
        self.robots = robots
        self.sources = sources
        self.destinations = destinations

    def render_simulation(self, robots, sources, destinations):
        self.screen.fill(WHITE)
        for robot in robots:
            self.render_circumference(robot)
            self.render_robot(robot)
        for source in sources:
            self.render_source(robots[source.robot_id], source.src_angle)
        for destination in destinations:
            self.render_destination(robots[destination.robot_id], destination.dest_angle)

    def render_circumference(robot):
        pygame.draw.circle(self.screen, BLUE, (robot.center_x, robot.center_y), robot.center_radius, 2) 

    def render_robot(robot):
        x, y = robot.get_robot_position()
        pygame.draw.circle(self.screen, RED, (x, y), robot.robot_radius)

    def render_source(robot, src_angle):
        src_x = robot.center_x + robot.center_radius * math.cos(src_angle)
        src_y = robot.center_y + robot.center_radius * math.sin(src_angle)
        pygame.draw.rect(self.screen, GREEN, pygame.Rect(src_x - src_size / 2, src_y - src_size / 2, src_size, src_size))

    def render_destination(robot, dest_angle):
        dest_x = robot.center_x + robot.center_radius * math.cos(dest_angle)
        dest_y = robot.center_y + robot.center_radius * math.sin(dest_angle)
        pygame.draw.rect(self.screen, BLUE, pygame.Rect(dest_x - dest_size / 2, dest_y - dest_size / 2, dest_size, dest_size))

    def render_robot_met(robot):
        x, y = robot.get_robot_position()
        pygame.draw.circle(self.screen, GREEN, (x, y), robot.robot_radius * 3)
