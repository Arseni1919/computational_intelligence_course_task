from Algorithms import *
from Cell import Cell
import numpy as np
import operator


def delete_facilities(cells):
    for cell in cells:
        if cell.occupied_by and cell.occupied_by.kind == 'f':
            cell.remove_facility()


def change_facility_location_in_cells(cells, facility, current_cell, next_cell):
    for cell in cells:

        # remove the facility from it's current location
        if cell.get_pos() == current_cell.get_pos():
            cell.remove_facility()

        # add the facility to the next location
        if cell.get_pos() == next_cell.get_pos():
            cell.add_facility(facility)


def copy_cells_from_to(cells_from, cells_to):
    for cell_to in cells_to:
        # clean cell_to
        if cell_to.occupied_by:
            if cell_to.occupied_by.kind == 'f':
                cell_to.remove_facility()

    for cell_from in cells_from:
        for cell_to in cells_to:
            # copy cell_from to cell_to
            if cell_to.get_pos() == cell_from.get_pos():
                if cell_from.occupied_by and cell_from.occupied_by.kind == 'f':
                        cell_to.add_facility(cell_from.occupied_by)


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
    copied_cells = copy_cells(cells)
    delete_facilities(copied_cells)
    allocations = np.zeros([len(facilities), len(cities)])
    num_of_open_facilities = 0

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
    while num_of_open_facilities < len(facilities) and requests_not_complete(cities, allocations):
        # choose the next facility
        curr_facility = facilities[num_of_open_facilities]

        # add the facility to a randomly selected cell
        all_possible_positions = get_all_possible_positions(copied_cells)
        new_cell = random.choice(all_possible_positions)
        new_cell.add_facility(curr_facility)

        # build dictionary of cities and distances from current facility
        cities_by_dist = {}
        for indx, curr_city in enumerate(cities):
            # calculate the distance from cities with remaining requests to the current facility
            if curr_city in cities_by_req:
                city_cell = get_cell_of_city(copied_cells, curr_city)
                curr_dist = get_dist(new_cell,city_cell)
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

        num_of_open_facilities = num_of_open_facilities+1

    return allocations, copied_cells


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


def copy_allocations_from_to(allocations_from, allocation_to):

    for row in range(len(allocations_from)):
        for column in range(len(allocations_from[0])):
            allocation_to[row][column] = allocations_from[row][column]


def create_child(cities, facilities, cells, parents_facility_locations):
    copied_cells = copy_cells(cells)
    delete_facilities(copied_cells)
    allocations = np.zeros([len(facilities), len(cities)])
    num_of_open_facilities = 0

    # build dictionary of cities and their requests
    cities_by_req = {}
    for indx, curr_city in enumerate(cities):
        # sum the request already answered for each city
        total_req_answered = 0
        for row in range(len(allocations)):
            total_req_answered = total_req_answered

        request_left = curr_city.get_req() - total_req_answered
        cities_by_req[curr_city] = request_left

    # open facilities
    while num_of_open_facilities < len(facilities) and requests_not_complete(cities, allocations):
        # choose the next facility
        curr_facility = facilities[num_of_open_facilities]

        # add the facility to the selected cell from one of the child parents
        for cell in copied_cells:
            if cell.get_pos() == parents_facility_locations[num_of_open_facilities].get_pos():
                mutation_cell = cell
                while True:
                    if mutation_cell.occupied_by:
                        print("cell is occupied by", cell.occupied_by.kind)
                        mutation_cell = random.choice(copied_cells)
                    else:
                        mutation_cell.add_facility(curr_facility)
                        break

        # build dictionary of cities and distances from current facility
        cities_by_dist = {}
        for indx, curr_city in enumerate(cities):
            # calculate the distance from cities with remaining requests to the current facility
            if curr_city in cities_by_req:
                city_cell = get_cell_of_city(copied_cells, curr_city)
                curr_dist = get_dist(get_cell_of_facility(copied_cells, curr_facility),city_cell)
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

        num_of_open_facilities = num_of_open_facilities+1

    return allocations, copied_cells


def GA(iteration, history, cities, facilities, cells, allocations, dist):
    # history = population, each with cells and allocation of facilities to cities
    population = history

    # generating starting population
    if iteration == 0:
        population = {}
        for i in range(10):
            new_allocations, new_cells = generate_starting_solution(cities, facilities, cells)
            population[i] = [new_allocations, new_cells]

    else:
        # calculate for each item in the population its utility
        utilities = np.zeros([10])
        sum_utilities = 0
        for i in range(10):
            current_item = population[i]
            added_utility = calc_utility(current_item[0], current_item[1])
            utilities[i] = added_utility
            sum_utilities = sum_utilities + added_utility

        # calculate reproduction probability
        probabilities = np.zeros([10])
        for i in range(10):
            probabilities[i] = utilities[i]/sum_utilities

        # create next population
        new_population = {}
        possible_parents_indx = range(10)
        for i in range(10):
            # choose the next two parents
            parents = random.choices(possible_parents_indx, weights=probabilities, k=2)
            parent_a = parents[0]
            parent_b = parents[1]
            parent_a_info = population[parent_a]
            parent_b_info = population[parent_b]
            cells_parent_a = parent_a_info[1]
            cells_parent_b = parent_b_info[1]

            # choose the facilities to be copied from parent a
            facilities_from_a = random.choices(range(len(facilities)), k=round(len(facilities)//2))
            parents_facility_locations = []
            for j in range(len(facilities)):
                if j in facilities_from_a:
                    parents_facility_locations.append(get_cell_of_facility_by_num(cells_parent_a, j))
                else:
                    parents_facility_locations.append(get_cell_of_facility_by_num(cells_parent_b, j))

            # create child
            child_allocations, child_cells = create_child(cities, facilities, cells, parents_facility_locations)
            new_population[i] = [child_allocations, child_cells]

        population = new_population

    # update allocations and cells pointer, to save the best item in population
    best_item = population[0]
    best_allocation = best_item[0]
    best_cells = best_item[1]
    best_utility = calc_utility(best_allocation, best_cells)

    for i in range(1, 10):
        curr_item = population[i]
        curr_allocations = curr_item[0]
        curr_cells = curr_item[1]
        curr_utility = calc_utility(curr_allocations, curr_cells)

        if curr_utility > best_utility:
            best_allocation = copy_allocations(curr_allocations)
            copy_cells_from_to(curr_cells, best_cells)
            best_utility = curr_utility

    copy_cells_from_to(best_cells, cells)
    copy_allocations_from_to(best_allocation, allocations)

    return population
