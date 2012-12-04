
import os.path
import csv


class Data(object):
    "Handles a set of data, can plot it, ..."

    def __init__(self, path):
        self.path = path

    def positions(self):
        "Returns a list with the coordinates of each point."
        for line in csv.reader(open(self.path), delimiter='\t'):
            yield float(line[0]), float(line[1])

    def dist_matrix(self):
        "Returns a distance matrix between all points."
        raise NotImplementedError

    def plot(self):
        import matplotlib.pyplot as plt
        plt.plot([1,2,3,4], [1,4,9,16], 'ro')
        plt.axis([0, 6, 0, 20])


class Box(object):
    "Access to load data from a data directory."

    def __init__(self, root):
        "Initialize with the path of the data directory."
        self.root = os.path.abspath(root)

    def get(self, path):
        "Returns the content of a data file from it's name."
        full_path = os.path.join(self.root, path)
        return Data(full_path)
