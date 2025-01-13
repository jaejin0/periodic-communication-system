from simulation import Simulation
import pygame
simulation = Simulation()

# game loop
while True: 
    simulation.action_choice()
    simulation.step()

pygame.quit()


