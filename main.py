# ----------------------------------------------------------------------- #
# ------------ COMPUTATIONAL INTELLIGENCE COURSE PROJECT ---------------- #
# ----------------------------------------------------------------------- #

# Import and initialize
from main_help_functions import *
from Algorithms import *
from greedy import *
from constraction_heuristic import *
from simulated_anealing import *
from genetic_algorithm import *
from local_search import *


# ------------------------------------------------------- #
# -------------------- INPUT SETTING -------------------- #
# ------------------------------------------------------- #

grid_size = 20
num_of_problems = 3
num_of_iterations = 500
num_of_facilities = 5
dist = 10
ratio = 0.1
need_to_stop_after_each_problem = False
need_to_save_results = True
add_to_name = f'{num_of_problems}_{num_of_iterations}_{num_of_facilities}_0point1_'
history = {}
# results = np.zeros((num_of_iterations, num_of_problems))
# need_to_render = True
algorithms = {
    'greedy': [f"results/{add_to_name}greedy.p", greedy],
    'ch': [f"results/{add_to_name}ch.p", ch],
    'local_search': [f"results/{add_to_name}local_search.p", local_search],
    'SA': [f"results/{add_to_name}SA.p", SA],
    'GA': [f"results/{add_to_name}GA.p", GA],
}
algorithms_to_run = ['local_search', 'SA',]
# algorithms_to_run = ['GA', 'greedy', 'ch', 'local_search', 'SA', ]
# algorithms_to_run = ['greedy', 'ch', 'local_search', 'SA', ]
results = np.zeros((len(algorithms_to_run), num_of_iterations, num_of_problems))
# ------------------------------------------------------- #
start = time.time()
pygame.init()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_HEIGHT))
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Run problems
for problem in range(num_of_problems):
    print()
    print('#' * 80)

    # Instantiate
    all_sprites = pygame.sprite.Group()
    cities = []
    cells = pygame.sprite.Group()
    # titles = pygame.sprite.Group()

    cell_hight_without_padding = create_field(cells, all_sprites, grid_size)
    # create_titles(titles, all_sprites, 1)
    create_cities(cities, cells, ratio)
    facilities = create_facilities(num_of_facilities)

    for indx_of_alg, alg in enumerate(algorithms_to_run):
        print('\n{:.2f} minutes passed from the beginning.'.format((time.time() - start) / 60.0))
        allocations = np.zeros([len(facilities), len(cities)])
        print('\n%s run' % alg)
        put_facilities_on_map(facilities, cells)

        # run iterations
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

            # -------------------------------------------------------------------------------------------------------- #
            # -------------------------------------------------------------------------------------------------------- #
            # -------------------------------------------------------------------------------------------------------- #

            # greedy_move_example(cities, facilities, cells, cell_hight_without_padding*10)
            # history = ch(iteration, history, cities, facilities, cells, cell_hight_without_padding * dist)
            # history = greedy(iteration, history, cities, facilities, cells, cell_hight_without_padding * dist)
            # history = SA(iteration, history, cities, facilities, cells, cell_hight_without_padding * dist)
            history = algorithms[alg][1](iteration, history, cities, facilities, cells, allocations, cell_hight_without_padding * dist)
            print(f'\r[problem {problem + 1}][iteration {iteration + 1}]: utility = {calc_utility(allocations, cells)}', end='')
            results[indx_of_alg][iteration][problem] = calc_utility(allocations, cells)
            # -------------------------------------------------------------------------------------------------------- #
            # -------------------------------------------------------------------------------------------------------- #
            # -------------------------------------------------------------------------------------------------------- #

            # Fill the screen
            screen.fill(SCREEN_COLOR)

            # Draw the player on the screen
            for entity in all_sprites:
                screen.blit(entity.surf, entity.rect)

            # Flip the display
            pygame.display.flip()
            time.sleep(0.1)

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

if need_to_save_results:
    for indx_of_alg, alg in enumerate(algorithms_to_run):
        pickle.dump(results[indx_of_alg], open(algorithms[alg][0], "wb"))
    # pickle.dump(results, open("results/SA.p", "wb"))
    # pickle.dump(results, open("results/ch.p", "wb"))
    # pickle.dump(results, open("results/greedy.p", "wb"))
    # pickle.dump(results, open("results/ROTEM.p", "wb"))
# Done! Time to quit.
pygame.quit()
end = time.time()
print()
print('#' * 80)
print('#' * 80)
print('#' * 80)
print('\nIt took {:.2f} minutes to finish the run.'.format((end - start) / 60.0))
print(add_to_name)

'''
- save results
- plot results
- write a report
- 

'''
