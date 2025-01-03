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
robot_radius = 5
robot_sensor_range = 10

robot_num = 2
robots = [{} for i in range(robot_num)]
    # robot 0
robots[0]["center_x"] = 300
robots[0]["center_y"] = 250
robots[0]["radius"] = 50
robots[0]["angle"] = 0
robots[0]["angular_speed"] = 0.00
    # robot 1
robots[1]["center_x"] = 400
robots[1]["center_y"] = 250
robots[1]["radius"] = 50
robots[1]["angle"] = 0
robots[1]["angular_speed"] = 0.05

# packet properties
src_id = 0
dest_id = 1
src_angle = 3.14
dest_angle = 0

src_size = 10
dest_size = 10

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
    current_positions = []
    for i in range(robot_num):
        # render circumference
        pygame.draw.circle(screen, BLUE, (robots[i]["center_x"], robots[i]["center_y"]), robots[i]["radius"], 2) 

        # render src and dest
        src_x = robots[src_id]["center_x"] + robots[src_id]["radius"] * math.cos(src_angle)
        src_y = robots[src_id]["center_y"] + robots[src_id]["radius"] * math.sin(src_angle)
        dest_x = robots[dest_id]["center_x"] + robots[dest_id]["radius"] * math.cos(dest_angle)
        dest_y = robots[dest_id]["center_y"] + robots[dest_id]["radius"] * math.sin(dest_angle)
               
        pygame.draw.rect(screen, GREEN, pygame.Rect(src_x - src_size / 2, src_y - src_size / 2, src_size, src_size))
        pygame.draw.rect(screen, BLUE, pygame.Rect(dest_x - dest_size / 2, dest_y - dest_size / 2, dest_size, dest_size))


        # render robot
        x = robots[i]["center_x"] + robots[i]["radius"] * math.cos(robots[i]["angle"])
        y = robots[i]["center_y"] + robots[i]["radius"] * math.sin(robots[i]["angle"])
        pygame.draw.circle(screen, RED, (x, y), robot_radius)

        # check if they met
        for i, (_x, _y) in enumerate(current_positions):
            if math.sqrt((x - _x)**2 + (y - _y) **2) <= robot_sensor_range:
                pygame.draw.circle(screen, GREEN, (x, y), robot_sensor_range, 2)
        
        current_positions.append([x, y])



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


