from simulation import Simulation
simulation = Simulation()

done = False
# game loop
while True: 
    simulation.action_choice()
    simulation.step()

    if done:
        simulation.terminate()
        break

