
class Simulation:
    def __init__(self, circumferences: List[float], max_velocities: List[float], initial_angles: List[float], 
                 src_index: int, dest_index: int, src_angle: float, dest_angle: float,
                 rendezvous: dict):
        self.circumferences = circumferences
        self.max_velocities = max_velocities
        self.initial_angles = initial_angles 
        self.src_index = src_index
        self.dest_index = dest_index
        self.src_angle = src_angle
        self.dest_angle = dest_angle
        self.rendezvous = rendezvous # key: (i, j), value: [angle, angle] 
        
        self.robot_num = len(circumferences)
        self.initial_velocity = 1 
        # robots : [current velocity, current angle, holding packet ids]
        self.robots = [[self.initial_velocity, initial_angles[i], []] for i in self.robot_num] 
     
        self.timestep = 0
        self.staleness = 0
        self.packet_id = 0
        self.packets = [] # [[timestep at src, timestep at dest]] 

    def reset:
        for i in range(self.robot_num):
            self.robots[i][0] = self.initial_velocity # current_velocity
            self.robots[i][1] = self.initial_angles[i] # current_angle

    def step:
        self.action()        
        self.transition()

    def action:
        # set velocity if this simulation provides the action choice per timestep
        pass

    def transition:          
  
        # calculate the diameter and the angle derivative
        # check if there is any packet sharing between robots
        # check if the robot of src index passed src angle
        # check if the robot of dest index passed 
        
        # change the angle of the robot
       
    def passing_src:
        

    def get_staleness:
        # largest shift from src to dest
        pass


