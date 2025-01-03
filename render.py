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
robots[0]["angle"] = 3.1
robots[0]["angular_speed"] = 0.03
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

    # render objects 
    for i in range(robot_num):
        # render circumference
        pygame.draw.circle(screen, BLUE, (robots[i]["center_x"], robots[i]["center_y"]), robots[i]["radius"], 2) 
        
        # render robot
        x = robots[i]["center_x"] + robots[i]["radius"] * math.cos(robots[i]["angle"])
        y = robots[i]["center_y"] + robots[i]["radius"] * math.sin(robots[i]["angle"])
        pygame.draw.circle(screen, RED, (x, y), 5)
    
   # action choice
    key = pygame.key.get_pressed()
    if key[pygame.K_a] == True:
        robots[0]["angular_speed"] += 0.01
    elif key[pygame.K_d] == True:
        robots[0]["angular_speed"] -= 0.01

    # transition
    for i in range(robot_num):
        robots[i]["angle"] += robots[i]["angular_speed"]

    pygame.display.update()

    clock.tick(60)

pygame.quit()


