import pygame
import math

def move_circle():
    speed = 1 # degree / timestep
    
    current_angle = math.atan2(player.y - center[1], player.x - center[0])
    print(current_angle)

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

player = pygame.Rect((300, 250, 50, 50))
center = pygame.Rect((300, 200, 10, 10))

running = True
while running:
    screen.fill("white")
    pygame.draw.circle(screen, (255, 0, 0), (player.x, player.y), 10)
    pygame.draw.circle(screen, (0, 0, 255), (center.x, center.y), 4)
    move_circle()

    key = pygame.key.get_pressed()
    if key[pygame.K_a] == True:
        player.move_ip(-1, 0)
    elif key[pygame.K_d] == True:
        player.move_ip(1, 0)
    elif key[pygame.K_w] == True:
        player.move_ip(0, -1)
    elif key[pygame.K_s] == True:
        player.move_ip(0, 1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()


