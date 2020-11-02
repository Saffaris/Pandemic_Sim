from manager import Manager

"""
Title: Pandemic Sim
Author: Maximilian Waiblinger
Date: 10/2020

This project was created as part of the subject 'Aktuelle Entwicklungen der Angewandten Informatik'
at the university Reutlingen.

The application creates simulates the spread of a infectious disease. The results are presented as a .json file
containing all events of the simulation and a gif that animates the progress on a map.

Contact:    maximilian.waiblinger@student.university-reutlingen.de
            max.waiblinger@t-online.de
"""

# default values
fileName = 'PandemicSim'  # Name used to save results
numberOfAgents = 10  # How many persons should be simulated
numberOfInfected = 1  # How many persons are infected from the beginning
timeSteps = 3600  # How many time steps (= 10 seconds) should be simulated
# (when all persons are infected the simulation stops early)
maxSpeed = 1  # Maximum number of fields a agent can move per timeStep (recommended at least 1)
borderX = 10  # How big the area in the x direction will be (-x to x)
borderY = 10  # How big the area in the y direction will be (-y to y)

array = [fileName, numberOfAgents, numberOfInfected, timeSteps, maxSpeed, borderX, borderY]

# instantiate manager
mng = Manager(array)

