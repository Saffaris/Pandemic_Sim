import PIL
from PIL import ImageTk
from tkinter import *


# manages the window used for inputs and to display the simulation results
class Window:

    # sets up window, except for the buttons
    def __init__(self, defaults):
        # setup window
        self.root = Tk()
        self.root.geometry("500x300+300+300")
        self.root.title('Pandemic Sim')
        self.root.iconbitmap('res/ps_icon.ico')
        Window.center(self.root)

        # setup frames
        # frame containing later added buttons
        self.frameButtons = Frame(self.root)
        self.frameButtons.pack(side=BOTTOM, fill=X)
        self.frameButtons.config(bg="darkgray")

        # frame containing the input fields
        frameInput = Frame(self.root)
        frameInput.pack(side=LEFT, padx=5)

        # frame containing the output image
        self.frameOutput = Frame(self.root)
        self.frameOutput.pack(side=RIGHT, fill=X)
        logo = PhotoImage(file="res/ps_icon.gif")
        self.display = Label(self.frameOutput, image=logo)
        self.display.pack(side=LEFT, fill=X, expand=True)

        # create input fields
        self.fileName = Window.createInput(frameInput, "Project:", defaults[0])
        self.numOfAgents = Window.createInput(frameInput, "Number of agents:", defaults[1])
        self.startInfected = Window.createInput(frameInput, "Infected at start:", defaults[2])
        self.timeSteps = Window.createInput(frameInput, "Time steps:", defaults[3])
        self.maxSpeed = Window.createInput(frameInput, "Movement speed:", defaults[4])
        self.fieldWidth = Window.createInput(frameInput, "Field width:", defaults[5])
        self.fieldHeight = Window.createInput(frameInput, "Field height:", defaults[6])

    # create buttons
    def setupButtons(self, simulate, visualize, load):
        buttonSim = Button(self.frameButtons, text='Simulate', width=20, command=simulate)
        buttonSim.pack(side=RIGHT, padx=5, pady=5)
        buttonVis = Button(self.frameButtons, text='Visualize', width=20, command=visualize)
        buttonVis.pack(side=RIGHT, padx=5, pady=5)
        buttonVis = Button(self.frameButtons, text='Load', width=20, command=load)
        buttonVis.pack(side=RIGHT, padx=5, pady=5)

    # show window
    def show(self):
        self.root.mainloop()

    # creates error window with given message
    @staticmethod
    def error(text):
        # setup warning-window
        err = Tk()
        err.config(bg="red")
        err.overrideredirect(True)
        err.resizable(width=FALSE, height=FALSE)
        Window.center(err)

        # setup frame
        frame = Frame(err)
        frame.pack(padx=5, pady=5, fill=X)

        # set displayed text
        label = Label(frame, text=text)
        label.pack(side=TOP, fill=X, pady=10)

        # set button to close warning-window
        button = Button(frame, text="OK", width=15, command=err.destroy)
        button.pack(side=BOTTOM, pady=10)

        # make warning-window visible
        err.mainloop()

    # displays given image in new window
    def showResults(self, path):
        root = Toplevel()
        root.title(self.fileName.get())
        root.iconbitmap('res/ps_icon.ico')
        loadImage = PIL.Image.open(path)
        biggerImage = loadImage.resize((400, 400))
        finishedImage = ImageTk.PhotoImage(biggerImage)
        panel = Label(root, image=finishedImage)
        panel.pack(side="bottom", fill="both", expand="yes")
        Window.center(root)
        root.mainloop()

    # static method, creates a labeled input field on the given root-element
    @staticmethod
    def createInput(root, title, default):
        frame = Frame(root)
        frame.pack(fill=X)
        entry = Entry(frame, width=15)
        entry.insert(END, default)
        entry.pack(side=RIGHT, fill=X, padx=5)
        label = Label(frame, text=title, anchor='e')
        label.pack(side=RIGHT, fill=X, padx=1, pady=5, expand=True)

        return entry

    # tests if string can be converted to integer
    @staticmethod
    def tryConvert(string: str):
        try:
            int(string)
            return True
        except Exception:
            return False

    # centers given window on screen
    @staticmethod
    def center(window):
        # gets the height and width
        windowWidth = window.winfo_reqwidth()
        windowHeight = window.winfo_reqheight()

        # calculate position
        positionRight = int(window.winfo_screenwidth() / 2 - windowWidth)
        positionDown = int(window.winfo_screenheight() / 2 - windowHeight)

        # positions the window in the center of the screen
        window.geometry("+{}+{}".format(positionRight, positionDown))

    # checks the given inputs for errors and shows a corresponding message
    def checkInputs(self, values):
        if len(str(values[0])) > 0:
            iterator = 0
            fieldNames = ("filename", "number of agents", "number of infected", "number of time steps",
                          "movement speed", "width", "height")
            for val in values:
                if iterator > 0:
                    if Window.tryConvert(val):
                        if int(val) <= 0:
                            self.error(text="The " + fieldNames[iterator] + " has to be bigger than zero.")
                            return False
                    else:
                        self.error(text="The given " + fieldNames[iterator] + " is not valid.")
                        return False
                iterator += 1
        else:
            self.error(text="The given project name is not valid.")
            return False

        return True
