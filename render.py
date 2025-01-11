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

class Robot:
    def __init__(
            self,
            center_x,
            center_y,
            radius,
            angle,
            angular_velocity,
            rendezvous,
            ):
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        self.angle = angle
        self.angular_velocity = angular_velocity
        self.rendezvous = rendezvous
        self.previous_angle = None
    
    def get_robot_position():
        x = self.center_x + self.radius * math.cos(self.angle)
        y = eslf.center_y + self.radius * math.sin(self.angle)
        return x, y 


# robot properties
robot_radius = 5
robot_max_velocity = 0.2

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

def render_circumference(i):
    pygame.draw.circle(screen, BLUE, (robots[i].center_x, robots[i].center_y), robots[i].radius, 2) 

def render_src():
    src_x = robots[src_id].center_x + robots[src_id].radius * math.cos(src_angle)
    src_y = robots[src_id].center_y + robots[src_id].radius * math.sin(src_angle)
    pygame.draw.rect(screen, GREEN, pygame.Rect(src_x - src_size / 2, src_y - src_size / 2, src_size, src_size))

def render_dest():
    dest_x = robots[dest_id].center_x + robots[dest_id].radius * math.cos(dest_angle)
    dest_y = robots[dest_id].center_y + robots[dest_id].radius * math.sin(dest_angle)
    pygame.draw.rect(screen, BLUE, pygame.Rect(dest_x - dest_size / 2, dest_y - dest_size / 2, dest_size, dest_size))

def render_robot(i):
    x, y = robots[i].get_robot_position()
    pygame.draw.circle(screen, RED, (x, y), robot_radius)

def render():
    for i in range(robot_num):
        render_circumference(i)
        render_src()
        render_dest()
        render_robot(i)


while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # clear screen
    screen.fill("white")

    # render objects
    for i in range(robot_num):
        render_circumference(i)
        render_src()
        render_dest()
        render_robot(i)

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
        robots[i].previous_angle = robots[i].angle
        robots[i].angle += robots[i].angular_velocity
        robots[i].angle = float("{:.3f}".format(robots[i].angle))
    
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
        


    pygame.display.update()
    clock.tick(60)

pygame.quit()


