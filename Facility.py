from CONSTANTS import *


class Facility:
    def __init__(self, cap, num):
        # super(Facility, self).__init__()
        self.cap = cap
        self.num = num
        self.coordinates = (-1, -1)
        self.cell = None

    def get_cap(self):
        return self.cap

    def get_pos(self):
        return self.coordinates
