
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
        # robots : [current_velocity, current_angle]
        self.robots = [[0, initial_angles[i]] for i in self.robot_num] 
        
    def reset:
        for i in range(self.robot_num):
            self.robots[i][0] = 0 # current_velocity
            self.robots[i][1] = self.initial_angles[i] # current_angle

    def step:
        # calculate the diameter and change the angle of the robot

    def transition:
        pass

    def get_staleness:
        # largest shift from src to dest
        pass


