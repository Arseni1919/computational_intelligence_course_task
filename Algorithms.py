from CONSTANTS import *


def get_dist(cell1, cell2):
    x1, y1 = cell1.get_pos()
    x2, y2 = cell2.get_pos()
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)


def get_closest_dist_from_facility(city, cells_with_facilities):
    min_dist = get_dist(city, cells_with_facilities[0])
    to_cell_of_facility = cells_with_facilities[0]
    for facility in cells_with_facilities:
        dist = get_dist(city, facility)
        if dist < min_dist:
            min_dist = dist
            to_cell_of_facility = facility
    return min_dist, to_cell_of_facility


def get_closest_cities(cell_of_facility, cells_with_cities, cells_with_facilities):
    closest_set = []
    for city in cells_with_cities:
        _, closest_facility = get_closest_dist_from_facility(city, cells_with_facilities)
        if closest_facility is cell_of_facility:
            closest_set.append(city)
    return closest_set


def get_sum_of_req(cells_of_closest_cities):
    sum = 0
    for cell_of_city in cells_of_closest_cities:
        sum += cell_of_city.occupied_by.req
    return sum


def calc_utility(curr_cells):
    # - facility cost - distance cost + num_of_metupalim
    facility_cost = 0
    distance_cost = 0
    num_of_metupalim = 0
    cells_with_cities = []
    cells_with_facilities = []

    for cell in curr_cells:
        if cell.occupied_by:
            if cell.occupied_by.kind == 'c':
                cells_with_cities.append(cell)
            if cell.occupied_by.kind == 'f':
                cells_with_facilities.append(cell)

    # if len(cells_with_facilities) == 0:
    #     return 0

    for city in cells_with_cities:
        closest_distance, _ = get_closest_dist_from_facility(city, cells_with_facilities)
        distance_cost += closest_distance

    for cell_of_facility in cells_with_facilities:
        facility_cost += cell_of_facility.cost
        cells_of_closest_cities = get_closest_cities(cell_of_facility, cells_with_cities, cells_with_facilities)
        sum_of_req = get_sum_of_req(cells_of_closest_cities)
        num_of_metupalim += min(cell_of_facility.occupied_by.cap, sum_of_req)

    return num_of_metupalim * 100 - facility_cost - distance_cost


def get_all_possible_positions_with_distance(dist, random_facility, cells):
    all_possible_positions_with_distance = []
    for cell in cells:
        if get_dist(cell, random_facility) <= dist:
            if not cell.occupied_by:
                all_possible_positions_with_distance.append(cell)
    return all_possible_positions_with_distance















