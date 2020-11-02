from tkinter import *
import json

from window import Window
from simulator import Simulator
from visualizer import Visualizer


# used to communicate between the window, simulator and visualizer scripts
class Manager:

    # set up display window
    def __init__(self, defaultValues):
        self.win = Window(defaultValues)
        self.win.setupButtons(simulate=self.simulate, visualize=self.visualize, load=self.insert)
        self.win.show()

    # method called by buttonpress, forwards input information to simulator
    def simulate(self):
        if self.win.checkInputs():
            sim = Simulator(numberOfAgents=int(self.win.numOfAgents.get()),
                            numberOfInfected=int(self.win.startInfected.get()),
                            timeSteps=int(self.win.timeSteps.get()),
                            maxSpeed=int(self.win.maxSpeed.get()),
                            borderX=int(self.win.fieldWidth.get()),
                            borderY=int(self.win.fieldHeight.get()))
            sim.runSimulation(self.win.fileName.get())

    # method called by buttonpress, forwards simulated data to visualizer
    def visualize(self):
        try:
            if self.load():
                vis = Visualizer(int(self.data['borderX']), int(self.data['borderY']))
                vis.createImage(self.data)
        except Exception:
            Window.error("There is no .json file for the given project name.\nRun the simulation first.")
        self.win.showResults("gif/" + self.data['project'] + ".gif")

    # loads project by name and displays the given values
    def insert(self):
        if self.load():
            self.changeField(self.win.numOfAgents, self.data['numberOfAgents'])
            self.changeField(self.win.startInfected, self.data['numberOfInfected'])
            self.changeField(self.win.timeSteps, self.data['timeSteps'])
            self.changeField(self.win.maxSpeed, self.data['maxSpeed'])
            self.changeField(self.win.fieldWidth, self.data['borderX'])
            self.changeField(self.win.fieldHeight, self.data['borderY'])
            print("We loaded")

    # loads an old simulation by given project name
    def load(self):
        try:
            path = 'sim/'+self.win.fileName.get() + '.json'
            with open(path) as json_file:
                self.data = json.load(json_file)
            return True
        except Exception:
            Window.error(text="No file with given name.")
            return False

    # changes text of input field
    @staticmethod
    def changeField(field: Entry, newText: str):
        field.delete(0, END)
        field.insert(0, newText)