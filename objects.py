import math
import sched

class Robot:
    def __init__(
            self,
            robot_id,
            center_x,
            center_y,
            center_radius,
            initial_angle,
            initial_angular_velocity,
            rendezvous,
            ):
        # static state
        self.robot_id = robot_id
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
        self.packets = {}

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
    def __init__(self, robot, src_angle, time_gap):
        self.robot_id = robot.robot_id
        self.src_angle = src_angle
        self.time_gap = time_gap # ms

        self.x, self.y = self.get_source_position(robot.center_x, robot.center_y, robot.center_radius)

        # dynamic state
        self.packets = []
        self.packet_id = 0
        self.packet_hold_num = 0
        self.last_create_time = 0

        # default properties
        self.src_size = 10

    def create_packet(self, time):
        if time > self.last_create_time + self.time_gap:
            packet = Packet(self.packet_id, time) 
            self.packets.append(packet)
            self.packet_id += 1
            self.packet_hold_num += 1
            self.last_create_time = time
            print(f"Packet {packet.packet_id} published")
    
    def get_source_position(self, center_x, center_y, center_radius):
        x = center_x + center_radius * math.cos(self.src_angle)
        y = center_y + center_radius * math.sin(self.src_angle)
        return x, y 


class Destination:
    def __init__(self, robot_id, dest_angle, position):
        self.robot_id = robot_id
        self.dest_angle = dest_angle
        self.x, self.y = position

        # default properties
        self.dest_size = 10

class Packet:
    def __init__(self, packet_id, timestep_produced):
        self.packet_id = packet_id
        self.timestep_produced = timestep_produced
        # location for rendering
