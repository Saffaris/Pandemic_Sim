import random


# Cap values at given boarder to prevent infinite growth
def cap(value, maxValue):
    if value > maxValue:
        return maxValue
    if value < -maxValue:
        return -maxValue
    return value


# class to represent a single person in the simulation
class Agent:

    def __init__(self, idCode, x, y, infected):
        # individual ID
        self.idCode = idCode

        # position on map
        self.x = x
        self.y = y

        # infection information
        self.infected = infected
        self.contagious = int(infected)

        # current velocity
        self.vel = (0, 0)

    # Alter the velocity and move the agent
    def move(self, maxSpeed, xBorder, yBorder):
        # alter velocity
        self.vel = (cap(self.vel[0] + random.randint(-1, 1), maxSpeed),
                    cap(self.vel[1] + random.randint(-1, 1), maxSpeed))

        # move agent
        self.x = cap(self.x + self.vel[0], xBorder)
        self.y = cap(self.y + self.vel[1], yBorder)

    def infect(self):
        self.infected = True
        self.contagious = 1
