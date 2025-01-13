from objects import Robot, Source, Destination
from render import render


def simulation():
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
        



