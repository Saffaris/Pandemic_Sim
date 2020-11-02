from PIL import Image
import numpy as np
import imageio


# class to create image from json file with results
class Visualizer:

    def __init__(self, width, height):
        self.width = width
        self.height = height

    # create pictures of all timestamps and create a gif animation
    def createImage(self, data):
        animation = []
        # iterate over all timestamps
        for iterator in range(1, int(data['takenSteps'])):
            # initialize image
            array = np.empty((self.width * 2 + 1, self.height * 2 + 1))
            array.fill(255)  # fill with white space
            img = Image.fromarray(array)
            img = img.convert('RGB')

            # draw each agent
            for point in data['events']:
                if int(point['timeStamp']) == iterator:
                    x = point['x'] + self.width
                    y = point['y'] + self.height
                    col = img.getpixel((x, y))
                    newCol = list(col)
                    if int(point['contagious']) == 0:
                        newCol[0] = 0
                    else:
                        newCol[1] = 0
                    newCol[2] = 0
                col = tuple(newCol)
                img.putpixel((x, y), col)

            # save pictures of time steps
            img.save('pic/picture' + str(iterator) + '.png')
            animation.append(img)

        # save all time steps as gif animation
        # imageio.mimsave('gif/' + data['project'] + '.gif', animation)
        print(len(animation))
        animation[0].save('gif/' + data['project'] + '.gif',
                          save_all=True, append_images=animation[1:], optimize=False, duration=40, loop=0)
