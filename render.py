import pygame
import math

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

# robot properties
robot_num = 2
robots = [{} for i in range(robot_num)]
    # robot 0
robots[0]["center_x"] = 300
robots[0]["center_y"] = 250
robots[0]["radius"] = 50
robots[0]["angle"] = 0
robots[0]["angular_speed"] = 0.05
    # robot 1
robots[1]["center_x"] = 400
robots[1]["center_y"] = 250
robots[1]["radius"] = 50
robots[1]["angle"] = 0
robots[1]["angular_speed"] = 0.05

# game loop
running = True
clock = pygame.time.Clock()

while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # clear screen
    screen.fill("white")

    # render circumference
    pygame.draw.circle(screen, BLUE, (center_x, center_y), radius, 2)
   
    # render robot
    x = center_x + radius * math.cos(angle)
    y = center_y + radius * math.sin(angle)
    pygame.draw.circle(screen, RED, (x, y), 5)
   
    # action choice
    key = pygame.key.get_pressed()
    if key[pygame.K_a] == True:
        angular_speed += 0.01
    elif key[pygame.K_d] == True:
        angular_speed -= 0.01

    # transition
    angle += angular_speed

    pygame.display.update()

    clock.tick(60)

pygame.quit()


