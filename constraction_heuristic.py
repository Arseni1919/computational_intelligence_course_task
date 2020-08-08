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


def return_add_facility_to_allocations(cities, cells, curr_facility, curr_allocations):
    curr_facility_cell = get_cell_of_facility(cells, curr_facility)
    curr_facility_cap_left = curr_facility.get_cap()
    return_allocations = np.zeros([len(curr_allocations), len(curr_allocations[0])])
    copy_allocations_from_to(curr_allocations, return_allocations)

    # build dictionary of cities and left request
    cities_by_req = {}
    for indx, curr_city in enumerate(cities):
        # sum the request already answered for each city
        total_req_answered = 0
        for row in range(len(return_allocations)):
            total_req_answered = total_req_answered + return_allocations[row][indx]

        request_left = curr_city.get_req() - total_req_answered
        cities_by_req[curr_city] = request_left

    # build dictionary of cities and distances from current facility
    cities_by_dist = {}
    for indx, curr_city in enumerate(cities):
        # calculate the distance from cities with remaining requests to the current facility
        if curr_city in cities_by_req:
            city_cell = get_cell_of_city(cells, curr_city)
            curr_dist = get_dist(curr_facility_cell,city_cell)
            cities_by_dist[curr_city] = curr_dist

    # add cities to the current facility, from the closest city to the farthest
    while curr_facility_cap_left > 0 and requests_not_complete(cities, return_allocations):
        next_city, next_city_dist = get_closest_city(cities_by_dist)

        next_city_left_req = cities_by_req[next_city]

        if next_city_left_req <= curr_facility_cap_left:
            return_allocations[curr_facility.num][next_city.num] = next_city_left_req
            curr_facility_cap_left = curr_facility_cap_left - next_city_left_req
            cities_by_req.pop(next_city)
            cities_by_dist.pop(next_city)

        else:
            return_allocations[curr_facility.num][next_city.num] = curr_facility_cap_left
            cities_by_req[next_city] = next_city_left_req - curr_facility_cap_left
            curr_facility_cap_left = 0

    return return_allocations


def ch(iteration, history, cities, facilities, cells, allocations, dist):
    copy_cells = get_cells_without_facilities(cells)
    curr_best_util = 0
    new_allocations = np.zeros([len(allocations), len(allocations[0])])

    for indx, curr_facility in enumerate(facilities):
        # add the current facility to a random cell
        all_possible_positions = get_all_possible_positions(copy_cells)
        new_cell = random.choice(all_possible_positions)
        new_cell.add_facility(curr_facility)

        # create an updated allocations with the added facility
        copy_allocations = return_add_facility_to_allocations(cities, copy_cells, curr_facility, new_allocations)

        # calculate the utility after adding the facility
        new_util = calc_utility(copy_allocations, copy_cells)

        if new_util < curr_best_util:
            new_cell.remove_facility()
        else:
            # update allocations and utility
            curr_best_util = new_util
            copy_allocations_from_to(copy_allocations, new_allocations)

    if iteration == 0:
        change_cells_from_to(cells, copy_cells)
        copy_allocations_from_to(new_allocations, allocations)
        return {'prev_iter_util': curr_best_util}

    if history['prev_iter_util'] < curr_best_util:
        change_cells_from_to(cells, copy_cells)
        copy_allocations_from_to(new_allocations, allocations)
        return {'prev_iter_util': curr_best_util}

    return history
