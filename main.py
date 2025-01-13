import pygame
import math

# initialization
pygame.init()

# display set up
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Periodic Communication System")

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


