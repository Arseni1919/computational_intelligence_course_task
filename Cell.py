# Import the pygame module
from CONSTANTS import *


# Define the cell object by extending pygame.sprite.Sprite
# Use an image for a better-looking sprite
class Cell(pygame.sprite.Sprite):
    def __init__(self, cell_size=None, surf_center=None, ord_number=None, cost=0):
        super(Cell, self).__init__()
        self.cell_size = cell_size
        self.surf = pygame.Surface((cell_size, cell_size))
        self.surf.fill(EMPTY_COLOR)
        self.rect = self.surf.get_rect(
            center=surf_center
        )
        # self.on = False
        self.occupied_by = None
        self.cost = cost
        self.ord_number = ord_number
        self.FONT_SIZE = int(cell_size * 0.45)
        # Number of Robot
        font = pygame.font.SysFont("comicsansms", self.FONT_SIZE)
        text = font.render("%s" % self.ord_number, True, (225, 0, 0))
        wt, ht = text.get_size()
        self.surf.blit(text, (cell_size - wt, 0))

    def get_pos(self):
        return self.rect.center

    def get_cell_size(self):
        return self.cell_size

    def get_ord_number(self):
        return self.ord_number

    def add_city(self, city):
        if self.occupied_by:
            raise ValueError()
        self.occupied_by = 'city', city
        city.coordinates = self.get_pos()
        city.cell = self
        self.surf.fill(OCCUPIED_COLOR)
        self.render_number()

    def add_facility(self, facility):
        if self.occupied_by:
            raise ValueError()
        self.occupied_by = 'facility', facility
        facility.coordinates = self.get_pos()
        facility.cell = self
        self.surf.fill(CLOSED_COLOR)
        self.render_number()

    def remove_facility(self):
        self.occupied_by = None
        self.surf.fill(EMPTY_COLOR)
        self.render_number()


    def render_number(self):
        # Number of Robot
        font = pygame.font.SysFont("comicsansms", self.FONT_SIZE)
        text = font.render("%s" % self.ord_number, True, (225, 0, 0))
        wt, ht = text.get_size()
        self.surf.blit(text, (self.cell_size - wt, 0))

