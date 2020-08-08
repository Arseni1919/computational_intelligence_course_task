from Algorithms import *
from Cell import Cell
import numpy as np
import operator


def get_temperature(iteration):
    T_0 = 100
    return T_0*(0.9**iteration)


def copy_allocations_from_to(allocations_from, allocation_to):

    for row in range(len(allocations_from)):
        for column in range(len(allocations_from[0])):
            allocation_to[row][column] = allocations_from[row][column]


def delete_facilities(cells):
    for cell in cells:
        if cell.occupied_by and cell.occupied_by.kind == 'f':
            cell.remove_facility()

def change_facility_location_in_cells(cells, facility, current_cell, next_cell):
    for cell in cells:

        # remove the facility from it's current location
        if cell.get_pos() == current_cell.get_pos():
            cell.remove_facility()
            #print("facility", facility.num, "removed from cell", cell.ord_number)

        # add the facility to the next location
        if cell.get_pos() == next_cell.get_pos():
            cell.add_facility(facility)
            #print("facility", facility.num, "added to cell", cell.ord_number)


def calc_utility(allocations, cells):
    facility_cost = 0
    distance_cost = 0
    num_of_metupalim = 0

    for facility_num in range(len(allocations)):
        facility_opened = False
        facility_cell = get_cell_of_facility_by_num(cells, facility_num)

        for city_num in range(len(allocations[0])):
            city_cell = get_cell_of_city_by_num(cells, city_num)

            if allocations[facility_num][city_num] > 0:

                # update facility cost
                if facility_opened == False:
                    facility_opened = True
                    facility_cost = facility_cost + facility_cell.cost

                # update distance cost
                distance_cost = distance_cost + get_dist(facility_cell, city_cell)

                # update num of metupalim
                num_of_metupalim = num_of_metupalim + allocations[facility_num][city_num]

    utility = num_of_metupalim * 100 - facility_cost - distance_cost

    return utility


def get_all_possible_positions(curr_cells):
    all_possible_positions = []
    for cell in curr_cells:
        if not cell.occupied_by:
            all_possible_positions.append(cell)
    return all_possible_positions


def requests_not_complete(cities, allocations):

    answer = False

    for city in cities:
        total_req_answered = 0
        for row in range(len(allocations)):
            total_req_answered = total_req_answered + allocations[row][city.num]

        if total_req_answered < city.get_req():
            answer = True

    return answer


def get_city_with_highest_req(cities_by_req):
    sorted_cities_by_req = sorted(cities_by_req.items(), key=operator.itemgetter(1), reverse=True)
    first_element = sorted_cities_by_req[0]
    returned_city = first_element[0]
    returned_left_req = first_element[1]

    return returned_city, returned_left_req


def get_cell_of_city(cells, city):
    for cell in cells:
        if cell.occupied_by == city:
            new_cell = Cell(cell.cell_size, cell.surf_center, cell.ord_number, cell.cost)
            new_cell.add_city(cell.occupied_by)

            return new_cell

    return None


def get_cell_of_facility(cells, facility):
    new_cell = None

    for cell in cells:
        if cell.occupied_by == facility:
            new_cell = Cell(cell.cell_size, cell.surf_center, cell.ord_number, cell.cost)
            new_cell.add_facility(cell.occupied_by)

    return new_cell


def get_cell_of_city_by_num(cells, city_num):
    for cell in cells:
        if cell.occupied_by and cell.occupied_by.kind == 'c' and cell.occupied_by.num == city_num:
            new_cell = Cell(cell.cell_size, cell.surf_center, cell.ord_number, cell.cost)
            new_cell.add_city(cell.occupied_by)

            return new_cell
    return None


def get_cell_of_facility_by_num(cells, facility_num):
    for cell in cells:
        if cell.occupied_by and cell.occupied_by.kind == 'f' and cell.occupied_by.num == facility_num:
            new_cell = Cell(cell.cell_size, cell.surf_center, cell.ord_number, cell.cost)
            new_cell.add_facility(cell.occupied_by)

            return new_cell
    return None


def get_closest_city(cities_by_dist):
    sorted_cities_by_dist = sorted(cities_by_dist.items(), key=operator.itemgetter(1))
    first_element = sorted_cities_by_dist[0]
    returned_city = first_element[0]
    returned_dist = first_element[1]

    return returned_city, returned_dist


def generate_starting_solution(cities, facilities, cells):
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
        # choose the next facility
        curr_facility = facilities[curr_facility_indx]

        # add the facility to a randomly selected cell
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


def get_next_random_positions(cells):
    next_random_positions = []
    all_possible_positions = get_all_possible_positions(cells)

    for i in range(10):
        next_random_positions.append(random.choice(all_possible_positions))

    return next_random_positions


def copy_cells(cells):
    copy_cells = []

    for cell in cells:
        new_cell = Cell(cell.cell_size, cell.surf_center, cell.ord_number, cell.cost)
        if cell.occupied_by:
            if cell.occupied_by.kind == 'c':
                new_cell.add_city(cell.occupied_by)
            elif cell.occupied_by.kind == 'f':
                new_cell.add_facility(cell.occupied_by)
        copy_cells.append(new_cell)

    return copy_cells


def create_next_solution_cells(cells, facility_to_move, new_random_location):
    next_solution_cells = []

    for cell in cells:
        new_cell = Cell(cell.cell_size, cell.surf_center, cell.ord_number, cell.cost)

        if cell.occupied_by:
            if cell.occupied_by.kind == 'c':
                new_cell.add_city(cell.occupied_by)
            elif cell.occupied_by.kind == 'f' and cell.occupied_by.num != facility_to_move.num:
                new_cell.add_facility(cell.occupied_by)

        if new_cell.get_pos() == new_random_location.get_pos():
            new_cell.add_facility(facility_to_move)

        next_solution_cells.append(new_cell)

    return next_solution_cells


def create_next_solution_allocations(allocations, cities, facilities, cells, facility_to_move, new_random_location):
    next_solution_allocations = np.zeros([len(facilities), len(cities)])

    # copy the allocations without the moved facility
    for row in range(len(allocations)):
        for column in range(len(allocations[0])):
            if row != facility_to_move.num:
                next_solution_allocations[row][column] = allocations[row][column]

    # assign cities to the moved facility
    curr_facility_cap_left = facility_to_move.get_cap()

    # build dictionary of cities and left request
    cities_by_req = {}
    for indx, curr_city in enumerate(cities):
        # sum the request already answered for each city
        total_req_answered = 0
        for row in range(len(next_solution_allocations)):
            total_req_answered = total_req_answered + next_solution_allocations[row][indx]

        request_left = curr_city.get_req() - total_req_answered
        cities_by_req[curr_city] = request_left

    # build dictionary of cities and distances from current facility
    cities_by_dist = {}
    for indx, curr_city in enumerate(cities):
        # calculate the distance from cities with remaining requests to the current facility
        if curr_city in cities_by_req:
            city_cell = get_cell_of_city(cells, curr_city)
            curr_dist = get_dist(new_random_location, city_cell)
            cities_by_dist[curr_city] = curr_dist

    # add cities to the current facility, from the closest city to the farthest
    while curr_facility_cap_left > 0 and requests_not_complete(cities, next_solution_allocations):
        next_city, next_city_dist = get_closest_city(cities_by_dist)

        next_city_left_req = cities_by_req[next_city]

        if next_city_left_req <= curr_facility_cap_left:
            next_solution_allocations[facility_to_move.num][next_city.num] = next_city_left_req
            curr_facility_cap_left = curr_facility_cap_left - next_city_left_req
            cities_by_req.pop(next_city)
            cities_by_dist.pop(next_city)

        else:
            next_solution_allocations[facility_to_move.num][next_city.num] = curr_facility_cap_left
            cities_by_req[next_city] = next_city_left_req - curr_facility_cap_left
            curr_facility_cap_left = 0

    return next_solution_allocations


def copy_allocations(allocations):
    copied_allocations = np.zeros([len(allocations), len(allocations[0])])

    for row in range(len(allocations)):
        for column in range(len(allocations[0])):
            copied_allocations[row][column] = allocations[row][column]

    return copied_allocations


def SA(iteration, history, cities, facilities, cells, allocations, dist):
    # history = allocation of facilities to cities

    # generating starting solution
    if iteration == 0:
        copy_allocations_from_to(generate_starting_solution(cities, facilities, cells), allocations)
    else:
        current_utility = calc_utility(allocations, cells)

        # choose randomly a facility to move
        facility_to_move = random.choice(facilities)
        current_facility_location = get_cell_of_facility(cells, facility_to_move)

        # choose randomly a possible new position for the chosen facility
        all_possible_positions = get_all_possible_positions(cells)
        new_random_location = random.choice(all_possible_positions)

        # calculate the utility of moving the facility and decide whether to move or not
        next_cells = create_next_solution_cells(cells, facility_to_move, new_random_location)
        next_allocations = create_next_solution_allocations(allocations, cities, facilities, cells, facility_to_move, new_random_location)
        next_positions_utility = calc_utility(next_allocations, next_cells)

        if current_utility < next_positions_utility:
            change_facility_location_in_cells(cells, facility_to_move, current_facility_location, new_random_location)
            copy_allocations_from_to(next_allocations, allocations)
        else:
            T = get_temperature(iteration)
            utility_delta = current_utility - next_positions_utility
            moving_probability = math.exp(-(utility_delta/T))
            random_num = random.uniform(0, 1)

            if random_num < moving_probability:
                change_facility_location_in_cells(cells, facility_to_move, current_facility_location, new_random_location)
                copy_allocations_from_to(next_allocations, allocations)

    return history