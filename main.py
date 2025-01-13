import pygame
import math

from objects import Robot, Source, Destination
from render import render

# initialization
pygame.init()

# display set up
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Periodic Communication System")

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


robot_num = 2
robots = []
# robot 0
robots.append(Robot(
    center_x = 300,
    center_y = 250,
    radius = 50,
    angle = 1.0,
    angular_velocity = 0.1,
    rendezvous = [[0, 1]]))
# robot 1
robots.append(Robot(
    center_x = 400,
    center_y = 250,
    radius = 50,
    angle = 1.0,
    angular_velocity = 0.1,
    rendezvous = [[float("{:.3f}".format(math.pi)), 0]]))

def robot_met():
    # check if the robots met
    current_positions = []
    for i in range(robot_num):
        x, y = robots[i].get_robot_position()
        for _x, _y in current_positions:
            if math.sqrt((x - _x)**2 + (y - _y) **2) <= robot_radius:
                pygame.draw.circle(screen, GREEN, (x, y), robot_radius * 3)
        current_positions.append([x, y]) 
    
    for i in range(robot_num): 
        if robots[i].angle >= math.pi or robots[i].angle <= -math.pi:
            robots[i].angle = -robots[i].angle
        

# game loop
running = True
clock = pygame.time.Clock()
while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # check if they met
        # if (i, robots[i]["angle"]) in rendezvous:
    # action choice
    key = pygame.key.get_pressed()
    if key[pygame.K_a] == True and robots[0].angular_velocity <= robot_max_velocity - 0.01:
        robots[0].angular_velocity += 0.01
    elif key[pygame.K_d] == True and robots[0].angular_velocity >= -robot_max_velocity + 0.01:
        robots[0].angular_velocity -= 0.01
        
    # transition
    for i in range(robot_num):
        robots[i].transition()

    robot_met()

    render()

    pygame.display.update()
    clock.tick(60)

pygame.quit()


