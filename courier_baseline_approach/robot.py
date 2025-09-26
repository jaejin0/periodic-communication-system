import math

class Neighbor:
    def __init__(self, rendezvous_angle: float, natural_frequency: float, last_meeting_time: int):
        self.rendezvous_angle = rendezvous_angle
        self.natural_frequency = natural_frequency
        self.last_meeting_time = last_meeting_time

class Robot:
    def __init__(self, id_number, natural_frequency, initial_angle, center_position, path_radius, robot_radius,
                 method, is_courier = False):
        # static states
        self.id_number = id_number
        self.natural_frequency = natural_frequency
        self.center_position = center_position
        self.path_radius = path_radius
        self.robot_radius = robot_radius
        self.method = method

        # dynamic states
        self.is_courier = is_courier
        self.angle = initial_angle
        self.control_frequency = 0
        self.robot_position = self.current_robot_position() 
        self.neighbors = {} # key: id_number | value: Neighbor 

    def step(self):
        self.angle += self.control_frequency + self.natural_frequency
        self.robot_position = self.current_robot_position()
    
    def current_robot_position(self):
        x = self.center_position[0] + self.path_radius * math.cos(self.angle)
        y = self.center_position[1] + self.path_radius * math.sin(self.angle)
        return x, y

    def update_control_strategy(self, current_timestep):
        if self.method not in ['coin_flip', 'myopic_heuristic', 'graph_based']:
            return 

        if self.is_courier and bool(self.neighbors): # courier
            earliest_arrival_time = float('inf')
            rendezvous_angle = None
            for neighbor in self.neighbors.values():
                # period = (2 * math.pi) / neighbor.natural_frequency
                
                time_to_arrive = neighbor.last_meeting_time + (2 * math.pi / neighbor.natural_frequency) 
                # i might need a list of time to arrive, for robot to select the possible one, as it might have skipped some of them. Maybe we add until the time is bigger than current time?

                if time_to_arrive < earliest_arrival_time:
                    earliest_arrival_time = time_to_arrive
                    rendezvous_angle = neighbor.rendezvous_angle
           
            rendezvous_angle = rendezvous_angle % (2 * math.pi)
            current_angle = self.angle % (2 * math.pi) 
            # if rendezvous_angle % (2 * math.pi) == self.angle % (2 * math.pi): 
              #   angle_difference = 2 * math.pi
            # else:
            print(rendezvous_angle, current_angle)
            angle_difference = max(rendezvous_angle, current_angle) - min(rendezvous_angle, current_angle) 
            if angle_difference <= 0:
                print("hell yeah")
                print(angle_difference)
                angle_difference += 2 * math.pi
             
            print(angle_difference)
            self.control_frequency = (angle_difference / (earliest_arrival_time - current_timestep)) - self.natural_frequency 
            # self.control_frequency = (2 * math.pi / (earliest_arrival_time - current_timestep)) - self.natural_frequency
            
        else:
            self.control_frequency = 0 # baseline

    # update expected angle of neighbors every step
    # store rendezvous for each neighbors

    # for the neighbor arriving earlist
    # ideal angular velocity = angle / time = (rendezvous angle - own angle) / (latest visit time * neighbor's angular velocity)
    # control angular velocity = ideal angular velocity - natural angular velocity

    def update_neighbor(self, timestep, neighbor_id_number, neighbor_natural_frequency):
        '''
        input: last meeting time, natural frequency, angle of rendezvous
        
        update neighbor's state
        '''
        if neighbor_id_number not in self.neighbors:
            self.neighbors[neighbor_id_number] = Neighbor(self.angle, neighbor_natural_frequency, timestep) 
        else:
            self.neighbors[neighbor_id_number].last_meeting_time = timestep 
                    
    def met(self, timestep, neighbor_id_number, neighbor_natural_frequency, neighbor_is_courier, coin = None): 

        self.update_neighbor(timestep, neighbor_id_number, neighbor_natural_frequency)

        match self.method:
            case 'coin_flip':
                if self.is_courier == neighbor_is_courier:
                    self.is_courier = coin

            case 'myopic_heuristic':
                print('')

            case 'graph_based':
                print('')
            
            case 'full_courier':
                print('')
            
            case 'average':
                self.control_frequency = ((self.control_frequency + self.natural_frequency + neighbor.control_frequency + neighbor.natural_frequency) / 2) - self.natural_frequency

            case 'max':
                self.control_frequency = max(self.control_frequency + self.natural_frequency, neighbor.control_frequency + neighbor.natural_frequency) - self.natural_frequency
                
            case 'min':
                self.control_frequency = min(self.control_frequency + self.natural_frequency, neighbor.control_frequency + neighbor.natural_frequency) - self.natural_frequency
            
            case _:
                print("SOMETHING WRONG SOMETHING WRONG SOMETHING WRONG!!!")

        self.update_control_strategy(timestep)


