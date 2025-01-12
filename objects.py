class Robot:
    def __init__(
            self,
            center_x,
            center_y,
            center_radius,
            initial_angle,
            initial_velocity,
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
   
    def get_robot_position():
        x = self.center_x + self.center_radius * math.cos(self.angle)
        y = eslf.center_y + self.center_radius * math.sin(self.angle)
        return x, y 

    def transition():
        self.previous_angle = robots[i].angle
        self.angle += robots[i].angular_velocity
        self.angle = float("{:.3f}".format(robots[i].angle))

class Source:
    def __init__(self, robot_id, src_angle):
        self.robot_id
        self.src_angle

class Destination:
    def __init__(self, robot_id, dest_angle):
        self.robot_id
        self.dest_angle


# packet properties
src_id = 0
dest_id = 1
src_angle = 3.14
dest_angle = 0

src_size = 10
dest_size = 10


