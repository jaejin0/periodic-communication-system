from objects import Robot, Source, Destination
from render import render_simulation, render_robot_met
import math

class Simulation:
    def __init__(self, seed=0):
        match seed:
            case 0:
                self.robots = [] 
                
                # robot 0
                self.robots.append(Robot( 
                    center_x = 300,
                    center_y = 250,
                    center_radius = 50,
                    initial_angle = 1.0,
                    initial_angular_velocity = 0.1,
                    rendezvous = [[0, 1]])
                )
                # robot 1
                self.robots.append(Robot(
                    center_x = 400,
                    center_y = 250,
                    center_radius = 50,
                    initial_angle = 1.0,
                    initial_angular_velocity = 0.1,
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
        for robot in self.robots:
            robot.transition()
        self.robot_met()
        render_simulation(self.robots)


    def robot_met(self):
        # check if the robots met
        current_positions = []
        for robot in self.robots:
            x, y = robot.get_robot_position()
            for _x, _y in current_positions:
                if math.sqrt((x - _x)**2 + (y - _y) **2) <= robot.robot_radius:
                    render_robot_met(i) 
            current_positions.append([x, y]) 
       


