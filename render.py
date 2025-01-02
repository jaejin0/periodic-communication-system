import pygame
import math

def change_angular_velocity():
    current_angle = math.atan2(player.y - center[1], player.x - center[0])
    return current_angle

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
center_x = 300
center_y = 250
radius = 60
angle = 0
angular_speed = 0.05

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


    # transition
    angle += angular_speed

    pygame.display.update()

    clock.tick(60)

pygame.quit()


