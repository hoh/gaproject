
import os.path


class Box(object):
    "Access to load data from a data directory."

    def __init__(self, root):
        "Initialize with the path of the data directory."
        self.root = os.path.abspath(root)

    def get_data(self, path):
        "Returns the content of a data file from it's name."
        full_path = os.path.join(self.root, path)
        return open(full_path)
