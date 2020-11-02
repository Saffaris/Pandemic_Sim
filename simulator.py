import random
import json

from agent import Agent


# class to run simulation and create json file with results
class Simulator:

    def __init__(self, numberOfAgents: int, numberOfInfected: int, timeSteps: int,
                 maxSpeed: int, borderX: int, borderY: int):
        # Run parameters (can later be altered)
        self.numberOfAgents = numberOfAgents  # How many persons should be simulated
        self.numberOfInfected = numberOfInfected  # How many persons are infected from the beginning
        self.timeSteps = timeSteps  # How many time steps (= 10 seconds) should be simulated
        # (when all persons are infected the simulation stops early)
        self.maxSpeed = maxSpeed  # Maximum number of fields a agent can move per timeStep (recommended at least 1)
        self.borderX = borderX  # How big the area in the x direction will be (-x to x)
        self.borderY = borderY  # How big the area in the y direction will be (-y to y)

        # Create agents
        self.agents = []
        infectionCounter = numberOfInfected
        for iterator in range(0, self.numberOfAgents):
            infection = infectionCounter > 0
            if infection:
                infectionCounter -= 1
            self.agents.append(
                Agent(iterator, random.randint(-self.borderX, self.borderX),
                      random.randint(-self.borderX, self.borderY), infection))

    def runSimulation(self, filename: str):
        # data setup
        idCode = self.numberOfAgents * self.timeSteps
        data = {'project': filename,
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
        with open('sim/' + filename + '.json', 'w') as outfile:
            json.dump(data, outfile)
