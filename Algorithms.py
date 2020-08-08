from CONSTANTS import *
from Cell import Cell
import operator


def requests_not_complete(cities, allocations):

    answer = False

    for city in cities:
        total_req_answered = 0
        for row in range(len(allocations)):
            total_req_answered = total_req_answered + allocations[row][city.num]

        if total_req_answered < city.get_req():
            answer = True

    return answer


def get_cell_of_facility(cells, facility):
    new_cell = None

    for cell in cells:
        if cell.occupied_by == facility:
            new_cell = Cell(cell.cell_size, cell.surf_center, cell.ord_number, cell.cost)
            new_cell.add_facility(cell.occupied_by)

    return new_cell


def get_cell_of_city(cells, city):
    for cell in cells:
        if cell.occupied_by == city:
            new_cell = Cell(cell.cell_size, cell.surf_center, cell.ord_number, cell.cost)
            new_cell.add_city(cell.occupied_by)

            return new_cell

    return None


def get_closest_city(cities_by_dist):
    sorted_cities_by_dist = sorted(cities_by_dist.items(), key=operator.itemgetter(1))
    first_element = sorted_cities_by_dist[0]
    returned_city = first_element[0]
    returned_dist = first_element[1]

    return returned_city, returned_dist


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


# def calc_utility(curr_cells):
#     # - facility cost - distance cost + num_of_metupalim
#     facility_cost = 0
#     distance_cost = 0
#     num_of_metupalim = 0
#     cells_with_cities = []
#     cells_with_facilities = []
#
#     for cell in curr_cells:
#         if cell.occupied_by:
#             if cell.occupied_by.kind == 'c':
#                 cells_with_cities.append(cell)
#             if cell.occupied_by.kind == 'f':
#                 cells_with_facilities.append(cell)
#
#     # if len(cells_with_facilities) == 0:
#     #     return 0
#
#     for city in cells_with_cities:
#         closest_distance, _ = get_closest_dist_from_facility(city, cells_with_facilities)
#         distance_cost += closest_distance
#
#     for cell_of_facility in cells_with_facilities:
#         facility_cost += cell_of_facility.cost
#         cells_of_closest_cities = get_closest_cities(cell_of_facility, cells_with_cities, cells_with_facilities)
#         sum_of_req = get_sum_of_req(cells_of_closest_cities)
#         num_of_metupalim += min(cell_of_facility.occupied_by.cap, sum_of_req)
#
#     return num_of_metupalim * 100 - facility_cost - distance_cost


def get_all_possible_positions_with_distance(dist, random_facility, cells):
    all_possible_positions_with_distance = []
    for cell in cells:
        if get_dist(cell, random_facility) <= dist:
            if not cell.occupied_by:
                all_possible_positions_with_distance.append(cell)
    return all_possible_positions_with_distance


def copy_allocations_from_to(allocations_from, allocation_to):

    for row in range(len(allocations_from)):
        for column in range(len(allocations_from[0])):
            allocation_to[row][column] = allocations_from[row][column]


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







