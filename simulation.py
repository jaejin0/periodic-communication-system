from objects import Robot, Source, Destination
from render import render

class Simulation:
    def __init__(self, seed=0)
        match seed:
            case 0:
                robot_num = 2
                robots = [] 
                # robot 0
                robots.append(Robot( 
                    center_x = 300,
                    center_y = 250,
                    radius = 50,
                    angle = 1.0,
                    angular_velocity = 0.1,
                    rendezvous = [[0, 1]])
                )
                # robot 1
                robots.append(Robot(
                    center_x = 400,
                    center_y = 250,
                    radius = 50,
                    angle = 1.0,
                    angular_velocity = 0.1,
                    rendezvous = [[float("{:.3f}".format(math.pi)), 0]])
                )
                
                # packet properties
                src_id = 0
                dest_id = 1
                src_angle = 3.14
                dest_angle = 0

                src_size = 10
                dest_size = 10


    def step(self):
        # transition
        for i in range(robot_num):
            robots[i].transition()
        robot_met()
        render()


    def robot_met(self):
        # check if the robots met
        current_positions = []
        for i in range(robot_num):
            for _x, _y in current_positions:
                if math.sqrt((x - _x)**2 + (y - _y) **2) <= robot_radius:
                    render_robot_met(i) 
            current_positions.append([x, y]) 
        
        for i in range(robot_num): 
            if robots[i].angle >= math.pi or robots[i].angle <= -math.pi:
                robots[i].angle = -robots[i].angle
            



