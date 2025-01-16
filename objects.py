import math
import sched

class Robot:
    def __init__(
            self,
            center_x,
            center_y,
            center_radius,
            initial_angle,
            initial_angular_velocity,
            rendezvous,
            ):
        # static state
        self.center_x = center_x
        self.center_y = center_y
        self.center_radius = center_radius
        self.initial_angle = initial_angle
        self.initial_angular_velocity = initial_angular_velocity
        self.rendezvous = rendezvous
        
        # dynamic state 
        self.angular_velocity = initial_angular_velocity
        self.angle = initial_angle
        self.previous_angle = None
        
        # default properties
        self.robot_radius = 5
        self.robot_max_velocity = 0.2
   
    def get_robot_position(self):
        x = self.center_x + self.center_radius * math.cos(self.angle)
        y = self.center_y + self.center_radius * math.sin(self.angle)
        return x, y 

    def transition(self):
        self.previous_angle = self.angle
        self.angle += self.angular_velocity
        self.angle = float("{:.3f}".format(self.angle))
 
        if self.angle >= math.pi or self.angle <= -math.pi:
            self.angle = -self.angle
        

class Source:
    def __init__(self, robot_id, src_angle, time_gap):
        self.robot_id = robot_id
        self.src_angle = src_angle
        self.time_gap = time_gap

        # dynamic state
        self.packet_num = 0

        # default properties
        self.src_size = 10
        self.scheduler = sched()

    def push_source(self):
       scheduler.enter(60, 1, do_something, (scheduler,))

class Destination:
    def __init__(self, robot_id, dest_angle):
        self.robot_id = robot_id
        self.dest_angle = dest_angle

        # default properties
        self.dest_size = 10


