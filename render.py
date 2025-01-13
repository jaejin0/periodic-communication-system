# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

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


