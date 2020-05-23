from Cell import *
from Title import *
from City import *
from Facility import *


def create_field(cells, all_sprites, grid_size):
    ord_number = 1
    curr_hight = SCREEN_HEIGHT - PADDING
    cell_hight_with_padding = math.floor(curr_hight / grid_size)
    cell_hight_without_padding = cell_hight_with_padding - PADDING
    for h in range(grid_size):
        for w in range(grid_size):
            surf_center = (
                h * cell_hight_with_padding + PADDING + cell_hight_without_padding / 2,
                w * cell_hight_with_padding + PADDING + cell_hight_without_padding / 2
            )
            cost = random.random()
            cell = Cell(cell_hight_without_padding, surf_center, ord_number, cost)
            cells.add(cell)
            all_sprites.add(cell)
            ord_number += 1
    return cell_hight_without_padding


def create_cities(cities, cells, ratio):
    num = 0
    for cell in cells:
        if ratio > random.random():
            city = City(random.randint(10, 100), num)
            cell.add_city(city)
            cities.append(city)
            num += 1
            # all_sprites.add(city)


def create_facilities(facilities, cells, num_of_facilities):
    finished = 0
    while finished < num_of_facilities:
        cell = random.choice(cells.sprites())
        if not cell.occupied_by:
            facility = Facility(random.randint(10, 100), finished)
            cell.add_facility(facility)
            facilities.append(facility)
            # all_sprites.add(facility)
            finished += 1


def create_titles(titles, all_sprites, mode):
    title = 'Button'.upper()
    button_hight = SCREEN_WIDTH - SCREEN_HEIGHT - 2 * PADDING
    # (SCREEN_WIDTH + button_hight/2, button_hight/2)
    button = Title(
        button_hight,
        (SCREEN_HEIGHT + button_hight / 2, PADDING + button_hight / 2),
        title,
        mode
    )
    titles.add(button)
    all_sprites.add(button)


def RAN_dist(cells, NUM_OF_PIVOTS):
    not_occupied_cells = []
    for cell in cells:
        if not cell.occupied:
            not_occupied_cells.append(cell)
    for _ in range(NUM_OF_PIVOTS):
        cell = random.choice(not_occupied_cells)
        cell.create_pivot()
        not_occupied_cells.remove(cell)


def neighbours_up_to(dist, q, cells, cell_hight_without_padding):
    neighbours = []
    q_x, q_y = q.get_pos()
    aside = dist * (cell_hight_without_padding + PADDING)

    for cell in cells:
        cell_x, cell_y = cell.get_pos()
        neighbour = False

        if q_x == cell_x and q_y == cell_y + aside:
            neighbour = True
        if q_x == cell_x and q_y == cell_y - aside:
            neighbour = True
        if q_x == cell_x + aside and q_y == cell_y:
            neighbour = True
        if q_x == cell_x - aside and q_y == cell_y:
            neighbour = True

        if q_x == cell_x + aside and q_y == cell_y + aside:
            neighbour = True
        if q_x == cell_x + aside and q_y == cell_y - aside:
            neighbour = True
        if q_x == cell_x - aside and q_y == cell_y + aside:
            neighbour = True
        if q_x == cell_x - aside and q_y == cell_y - aside:
            neighbour = True

        if neighbour:
            if not cell.occupied:
                neighbours.append(cell)

    return neighbours


def DCB_dist(cells, NUM_OF_PIVOTS, cell_hight_without_padding, max_dist):

    occupied_cells = []
    not_occupied_cells = {}
    for cell in cells:
        if cell.occupied:
            occupied_cells.append(cell)
        else:
            not_occupied_cells[cell] = 0

    for occ_cell in occupied_cells:
        for dist in range(max_dist):
            neighbours = neighbours_up_to(dist + 1, occ_cell, cells, cell_hight_without_padding)
            weight = max_dist - dist
            for neighbour in neighbours:
                not_occupied_cells[neighbour] = not_occupied_cells[neighbour] + weight

    sum_of_weights = sum(not_occupied_cells.values())
    p = []
    cells_to_pick = []
    for cell, weight in not_occupied_cells.items():
        cells_to_pick.append(cell)
        p.append(weight/sum_of_weights)

    to_pivots = np.random.choice(cells_to_pick, NUM_OF_PIVOTS, replace=False, p=p)
    for cell in to_pivots:
        cell.create_pivot()


def create_goals(cells):
    kind_of_cell = 0
    for cell in cells:
        if cell.get_goal() != -1:
            kind_of_cell = 1
            break
    mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
    for cell in cells:
        cell_pos_x, cell_pos_y = cell.get_pos()
        cell_size = cell.get_cell_size()
        if cell_pos_x - cell_size / 2 < mouse_pos_x < cell_pos_x + cell_size / 2:
            if cell_pos_y - cell_size / 2 < mouse_pos_y < cell_pos_y + cell_size / 2:
                if cell.get_goal() != -1:
                    cell.set_goal(-1)
                else:
                    cell.set_goal(kind_of_cell)


def upload_map(name, cells, grid_size):
    if name == '':
        return
    file_name = '%s.map' % name
    with open(file_name, 'rb') as fileObject:
        # load the object from the file into var b
        curr_dict = pickle.load(fileObject)

        if len(curr_dict.keys()) != grid_size ** 2:
            print('[ERROR]: grid_size is have to be - %s' % math.sqrt(len(curr_dict.keys())))
            raise ValueError()

        for cell in cells:
            cell.set_occupied(curr_dict[cell.get_ord_number()])


def upload_pivots(name, cells, pivots, grid_size):
    if name == '':
        return
    file_name = '%s.piv' % name
    with open(file_name, 'rb') as fileObject:
        # load the object from the file into var b
        curr_dict = pickle.load(fileObject)

        if len(curr_dict.keys()) != grid_size ** 2:
            print('[ERROR]')
            raise ValueError()

        for cell in cells:
            if curr_dict[cell.get_ord_number()]:
                cell.create_pivot()
                pivots.add(cell)


def update_title_up(titles):
    for title in titles:
        title.push(False)


def button_func(titles, cells, name):
    mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
    for title in titles:
        title_pos_x, title_pos_y = title.get_pos()
        title_size = title.get_cell_size()
        if title_pos_x - title_size / 2 < mouse_pos_x < title_pos_x + title_size / 2:
            if title_pos_y - title_size / 2 < mouse_pos_y < title_pos_y + title_size / 2:
                title.push(True)
                mode = title.get_mode()


def reset_cells(cells):
    for cell in cells:
        cell.reset()


def reset_cells_without_resetting_goal(cells):
    for cell in cells:
        cell.reset_without_resetting_goal()


def second_stage(cells, name, piv_name, piv_dist):
    dict_to_save = {}
    for cell in cells:
        dict_to_save[cell.get_ord_number()] = cell.get_if_pivot()
    file_name = "%s-%s-%s.piv" % (name, piv_name, piv_dist)
    # open the file for writing
    with open(file_name, 'wb') as fileObject:
        pickle.dump(dict_to_save, fileObject)



def save_and_print_results(results_for_map, name_to_load):
    file_name = "%s.results" % name_to_load
    # open the file for writing
    with open(file_name, 'wb') as fileObject:
        pickle.dump(results_for_map, fileObject)

    # results_for_map['RAN', 'DCB', 'ATB'][1,..., 10][range(30)]['dif', 'can'] = indicator
    # results_for_map[piv_type][piv_num][prob_num][heuristic_type] = indicator
    to_print = {}
    for piv_type in results_for_map.keys():
        to_print[piv_type] = {'dif': [], 'can': []}
        for piv_num in results_for_map[piv_type].keys():
            for prob_num in results_for_map[piv_type][piv_num].keys():
                for heuristic_type, indicator in results_for_map[piv_type][piv_num][prob_num].items():
                    to_print[piv_type][heuristic_type].append(indicator)

    for piv_type in to_print.keys():
        for heuristic_type, list_of_indicators in to_print[piv_type].items():
            print('%s: %s -> %s' % (piv_type, heuristic_type, np.mean(list_of_indicators)))



