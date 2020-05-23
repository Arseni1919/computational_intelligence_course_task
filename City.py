from CONSTANTS import *


class City:  # (pygame.sprite.Sprite)
    def __init__(self, req, num):
        # super(City, self).__init__()
        self.req = req
        self.num = num
        self.coordinates = (-1, -1)
        self.cell = None

    def get_req(self):
        return self.req

    def get_pos(self):
        return self.coordinates

    def set_pos(self, coordinates):
        self.coordinates = coordinates


