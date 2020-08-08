
from Algorithms import *
from Cell import Cell


# def greedy_move_example(cities, facilities, cells, dist):
#     # curr_facility = random.choice(facilities)
#     for curr_facility in facilities:
#         all_possible_positions_with_distance = get_all_possible_positions_with_distance(dist, curr_facility, cells)
#         previous_cell = curr_facility.cell
#         new_cell = random.choice(all_possible_positions_with_distance)
#
#         previous_util = calc_utility(cities, facilities)
#         previous_cell.remove_facility()
#         new_cell.add_facility(curr_facility)
#         new_util = calc_utility(cities, facilities)
#
#         if new_util < previous_util:
#             new_cell.remove_facility()
#             previous_cell.add_facility(curr_facility)

def generate_allocations(cities, facilities, cells):
    allocations = np.zeros([len(facilities), len(cities)])
    curr_facility_indx = 0

    # build dictionary of cities and left request
    cities_by_req = {}
    for indx, curr_city in enumerate(cities):
        # sum the request already answered for each city
        total_req_answered = 0
        for row in range(len(allocations)):
            total_req_answered = total_req_answered + allocations[row][indx]

        request_left = curr_city.get_req() - total_req_answered
        cities_by_req[curr_city] = request_left

    # open facilities
    while curr_facility_indx < len(facilities) and requests_not_complete(cities, allocations):
        # choose the next facility and get its cell
        curr_facility = facilities[curr_facility_indx]
        curr_facility_cell = get_cell_of_facility(cells, curr_facility)

        # build dictionary of cities and distances from current facility
        cities_by_dist = {}
        for indx, curr_city in enumerate(cities):
            # calculate the distance from cities with remaining requests to the current facility
            if curr_city in cities_by_req:
                city_cell = get_cell_of_city(cells, curr_city)
                curr_dist = get_dist(curr_facility_cell,city_cell)
                cities_by_dist[curr_city] = curr_dist

        curr_facility_cap_left = curr_facility.get_cap()

        # add cities to the current facility, from the closest city to the farthest
        while curr_facility_cap_left > 0 and requests_not_complete(cities, allocations):
            next_city, next_city_dist = get_closest_city(cities_by_dist)

            next_city_left_req = cities_by_req[next_city]

            if next_city_left_req <= curr_facility_cap_left:
                allocations[curr_facility.num][next_city.num] = next_city_left_req
                curr_facility_cap_left = curr_facility_cap_left - next_city_left_req
                cities_by_req.pop(next_city)
                cities_by_dist.pop(next_city)

            else:
                allocations[curr_facility.num][next_city.num] = curr_facility_cap_left
                cities_by_req[next_city] = next_city_left_req - curr_facility_cap_left
                curr_facility_cap_left = 0

        curr_facility_indx = curr_facility_indx+1

    return allocations


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


def greedy(iteration, history, cities, facilities, cells, allocations, dist):

    if iteration == 0:
        copy_allocations_from_to(generate_allocations(cities, facilities, cells), allocations)
    else:
        copy_cells = get_cells_without_facilities(cells)

        # change allocations to curr allocations, add a function to create that allocation !!!!!!!!!!!!
        curr_best_util = calc_utility(allocations, cells)

        for indx, curr_facility in enumerate(facilities):
            all_possible_positions = get_all_possible_positions(copy_cells)
            new_cell = random.choice(all_possible_positions)
            new_cell.add_facility(curr_facility)

        new_allocations = generate_allocations(cities, facilities, copy_cells)
        new_util = calc_utility(new_allocations, copy_cells)

        if new_util > curr_best_util:
            copy_cells_from_to(copy_cells, cells)
            copy_allocations_from_to(new_allocations, allocations)

    return history
