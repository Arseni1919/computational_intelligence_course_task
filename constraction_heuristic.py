from Algorithms import *
from Cell import Cell


def get_all_possible_positions(curr_cells):
    all_possible_positions = []
    for cell in curr_cells:
        if not cell.occupied_by:
            all_possible_positions.append(cell)
    return all_possible_positions


def change_cells_from_to(cells, copy_cells):
    for cell in cells:
        if cell.occupied_by:
            if cell.occupied_by.kind == 'f':
                cell.remove_facility()
        for copy_cell in copy_cells:
            if copy_cell.get_pos() == cell.get_pos():
                if copy_cell.occupied_by:
                    if copy_cell.occupied_by.kind == 'f':
                        cell.copy_from(copy_cell)


def get_cells_without_facilities(cells):
    copy_cells = []
    for cell in cells:
        new_cell = Cell(cell.cell_size, cell.surf_center, cell.ord_number, cell.cost)
        if cell.occupied_by:
            if cell.occupied_by.kind == 'c':
                new_cell.add_city(cell.occupied_by)
        copy_cells.append(new_cell)
    return copy_cells


def ch(iteration, history, cities, facilities, cells, dist):
    copy_cells = get_cells_without_facilities(cells)
    curr_best_util = calc_utility(cells)
    for indx, curr_facility in enumerate(facilities):
        all_possible_positions = get_all_possible_positions(copy_cells)
        new_cell = random.choice(all_possible_positions)
        new_cell.add_facility(curr_facility)
        new_util = calc_utility(copy_cells)

        if indx == 0:
            curr_best_util = calc_utility(copy_cells)
            continue

        if new_util < curr_best_util:
            new_cell.remove_facility()
        else:
            curr_best_util = new_util

    if iteration == 0:
        change_cells_from_to(cells, copy_cells)
        return {'prev_iter_util': curr_best_util}

    if history['prev_iter_util'] < curr_best_util:
        change_cells_from_to(cells, copy_cells)
        return {'prev_iter_util': curr_best_util}

    return history