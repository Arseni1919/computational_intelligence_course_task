# ----------------------------------------------------------------------- #
# ------------ COMPUTATIONAL INTELLIGENCE COURSE PROJECT ---------------- #
# ----------------------------------------------------------------------- #

# Import and initialize
from main_help_functions import *
from Algorithms import *
from greedy import *

# ------------------------------------------------------- #
# -------------------- INPUT SETTING -------------------- #
# ------------------------------------------------------- #

grid_size = 30
num_of_problems = 10
num_of_iterations = 10
num_of_facilities = 10
dist = 10
ratio = 0.1
need_to_stop_after_each_problem = True
history = {}
# need_to_render = True
# ------------------------------------------------------- #

pygame.init()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_HEIGHT))
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Run until the user asks to quit
for problem in range(num_of_problems):
    print('#' * 80)

    # Instantiate
    all_sprites = pygame.sprite.Group()
    cities = []
    facilities = []
    cells = pygame.sprite.Group()
    # titles = pygame.sprite.Group()

    cell_hight_without_padding = create_field(cells, all_sprites, grid_size)
    # create_titles(titles, all_sprites, 1)
    create_cities(cities, cells, ratio)
    create_facilities(facilities, cells, num_of_facilities)

    for iteration in range(num_of_iterations):

        for event in pygame.event.get():
            # Did the user hit a key?
            if event.type == KEYDOWN:
                # Was it the Escape key? If so, stop the loop.
                if event.key == K_ESCAPE:
                    # need_to_render = False
                    next_problem = True

            # Did the user click the window close button? If so, stop the loop.
            # if event.type == QUIT:
            #     need_to_render = False

        # ------------------------------------------------------------------------------------------------------------ #
        # ------------------------------------------------------------------------------------------------------------ #
        # ------------------------------------------------------------------------------------------------------------ #
        print(f'[problem {problem + 1}][iteration {iteration}]: utility = {calc_utility(cells)}')
        # greedy_move_example(cities, facilities, cells, cell_hight_without_padding*10)
        history = greedy(iteration, history, cities, facilities, cells, cell_hight_without_padding * dist)
        # ------------------------------------------------------------------------------------------------------------ #
        # ------------------------------------------------------------------------------------------------------------ #
        # ------------------------------------------------------------------------------------------------------------ #

        # Fill the screen
        screen.fill(SCREEN_COLOR)

        # Draw the player on the screen
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        # Flip the display
        pygame.display.flip()
        time.sleep(0.01)

    if need_to_stop_after_each_problem:
        next_problem = False
        while not next_problem:
            # Did the user click the window close button?
            for event in pygame.event.get():
                # Did the user hit a key?
                if event.type == KEYDOWN:
                    # Was it the Escape key? If so, stop the loop.
                    if event.key == K_RETURN:
                        next_problem = True

# Done! Time to quit.
pygame.quit()
