import random
import json

from agent import Agent


# class to run simulation and create json file with results
class Simulator:

    def __init__(self, values):
        # Run parameters (can later be altered)
        self.fileName = values[0]  # Name for the later saved files
        self.numberOfAgents = int(values[1])  # How many persons should be simulated
        self.numberOfInfected = int(values[2])  # How many persons are infected from the beginning
        self.timeSteps = int(values[3])  # How many time steps (= 10 seconds) should be simulated
        # (when all persons are infected the simulation stops early)
        self.maxSpeed = int(values[4])  # Maximum number of fields a agent can move per timeStep
        self.borderX = int(values[5])  # How big the area in the x direction will be (-x to x)
        self.borderY = int(values[6])  # How big the area in the y direction will be (-y to y)

        # Create agents
        self.agents = []
        infectionCounter = self.numberOfInfected
        for iterator in range(0, self.numberOfAgents):
            infection = infectionCounter > 0
            if infection:
                infectionCounter -= 1
            self.agents.append(
                Agent(iterator, random.randint(-self.borderX, self.borderX),
                      random.randint(-self.borderX, self.borderY), infection))

    def runSimulation(self):
        # data setup
        idCode = self.numberOfAgents * self.timeSteps
        data = {'project': self.fileName,
                'numberOfAgents': self.numberOfAgents,
                'numberOfInfected': self.numberOfInfected,
                'timeSteps': self.timeSteps,
                'takenSteps': 0,
                'maxSpeed': self.maxSpeed,
                'borderX': self.borderX,
                'borderY': self.borderY,
                'events': []}

        # Time iteration
        iterator = 0
        while iterator < self.timeSteps:
            iterator += 1

            infectedFields = []

            # Move agents
            for agent in self.agents:
                agent.move(self.maxSpeed, self.borderX, self.borderY)
                if agent.contagious > 0:
                    infectedFields.append((agent.x, agent.y))

            # Resolve infections
            infected = 0
            for agent in self.agents:
                if agent.contagious == 0:
                    for field in infectedFields:
                        if field == (agent.x, agent.y):
                            agent.infect()
                            infected += 1
                else:
                    infected += 1
                # save information as event
                idCode += 1
                data['events'].append({
                    'timePointID': idCode,
                    'timeStamp': iterator,
                    'personID': agent.idCode,
                    'contagious': agent.contagious,
                    'x': agent.x,
                    'y': agent.y
                })

            # print("Timestamp " + str(iterator) + ": " + str(infected) + " are infected.")

            # Termination condition
            if infected == self.numberOfAgents:
                data['takenSteps'] = iterator
                iterator = self.timeSteps + 1

        # Save generated data
        with open('sim/' + self.fileName + '.json', 'w') as outfile:
            json.dump(data, outfile)
