from CONSTANTS import *

# Define the cell object by extending pygame.sprite.Sprite
# Use an image for a better-looking sprite
class Title(pygame.sprite.Sprite):
    def __init__(self, title_size=None, surf_center=None, text=None, mode=None):
        super(Title, self).__init__()
        self.cell_size = title_size
        self.surf = pygame.Surface((title_size, title_size))
        self.surf.fill((232, 89, 67))
        self.title = text
        self.mode = mode
        font = pygame.font.SysFont("comicsansms", 20)
        text = font.render("%s" % text, True, (255, 255, 255))
        self.surf.blit(text, (PADDING*2, title_size/2 - PADDING*10))

        self.rect = self.surf.get_rect(
            center=surf_center
        )
        self.prop = None

    def add_property(self, prop):
        self.prop = prop

    def get_prop(self):
        return self.prop

    def get_pos(self):
        return self.rect.center

    def get_cell_size(self):
        return self.cell_size

    def get_mode(self):
        return self.mode

    def push(self, pushed):
        self.surf = pygame.Surface((self.cell_size, self.cell_size))
        if pushed:
            self.surf.fill((48, 19, 15))
        else:
            self.surf.fill((232, 89, 67))

        font = pygame.font.SysFont("comicsansms", 20)
        text = font.render("%s" % self.title, True, (255, 255, 255))
        self.surf.blit(text, (PADDING * 2, self.cell_size / 2 - PADDING * 10))