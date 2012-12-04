
import os.path
import re
import math


def dist(point1, point2):
    return math.sqrt(
        abs(point1[0] - point2[0]) ** 2 \
      + abs(point1[1] - point2[1]) ** 2)


class Data(object):
    "Handles a set of data, can plot it, ..."

    def __init__(self, path):
        self.path = path
        self.positions = list(self.load())

    def load(self):
        "Returns a list with the coordinates of each point."
        for line in open(self.path).readlines():
            # Clearing the line
            line = line.strip().replace('\t', ' ').replace('  ', ' ')
            line = line.split()
            yield float(line[0]), float(line[1])

    def dist_matrix(self):
        "Returns a distance matrix between all points."
        matrix = []
        for point1 in self.positions:
            line = []
            for point2 in self.positions:
                line.append(dist(point1, point2))
            matrix.append(line)
        return matrix

    def plot(self):
        "Uses Matplotib to plot the nodes positions."
        import matplotlib.pyplot as plt

        x_axis = [pos[0] for pos in self.positions]
        y_axis = [pos[1] for pos in self.positions]

        plt.plot(x_axis, y_axis, 'bx')
        plt.show()

    def size(self):
        "Return the size of the current data."
        return len(self.positions)

    # ----- Special type functions: -----
    # Length:
    __len__ = size


class Box(object):
    "Access to load data from a data directory."

    def __init__(self, root):
        "Initialize with the path of the data directory."
        self.root = os.path.abspath(root)

    def get(self, path):
        "Returns the content of a data file from it's name."
        full_path = os.path.join(self.root, path)
        return Data(full_path)
