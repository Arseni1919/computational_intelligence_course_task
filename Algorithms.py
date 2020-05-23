from CONSTANTS import *


def get_dist(obj1, obj2):
    x1, y1 = obj1.get_pos()
    x2, y2 = obj2.get_pos()
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)


def get_closest_dist_from_facility(city, facilities):
    min_dist = get_dist(city, facilities[0])
    to_facility = facilities[0]
    for facility in facilities:
        dist = get_dist(city, facility)
        if dist < min_dist:
            min_dist = dist
            to_facility = facility
    return min_dist, to_facility


def get_closest_cities(facility, cities, facilities):
    closest_set = []
    for city in cities:
        _, closest_facility = get_closest_dist_from_facility(city, facilities)
        if closest_facility is facility:
            closest_set.append(city)
    return closest_set


def get_sum_of_req(closest_cities):
    sum = 0
    for city in closest_cities:
        sum += city.req
    return sum


def calc_utility(cities, facilities):
    # - facility cost - distance cost + num_of_metupalim
    facility_cost = 0
    distance_cost = 0
    num_of_metupalim = 0

    for city in cities:
        closest_distance, _ = get_closest_dist_from_facility(city, facilities)
        distance_cost += closest_distance

    for facility in facilities:
        facility_cost += facility.cell.cost * 100
        closest_cities = get_closest_cities(facility, cities, facilities)
        sum_of_req = get_sum_of_req(closest_cities)
        num_of_metupalim += min(facility.cap, sum_of_req)

    return num_of_metupalim - facility_cost - distance_cost


def get_all_possible_positions_with_distance(dist, random_facility, cells):
    all_possible_positions_with_distance = []
    for cell in cells:
        if get_dist(cell, random_facility) <= dist:
            if not cell.occupied_by:
                all_possible_positions_with_distance.append(cell)
    return all_possible_positions_with_distance


def greedy_move_example(cities, facilities, cells, dist):

    # curr_facility = random.choice(facilities)
    for curr_facility in facilities:
        all_possible_positions_with_distance = get_all_possible_positions_with_distance(dist, curr_facility, cells)
        previous_cell = curr_facility.cell
        new_cell = random.choice(all_possible_positions_with_distance)

        previous_util = calc_utility(cities, facilities)
        previous_cell.remove_facility()
        new_cell.add_facility(curr_facility)
        new_util = calc_utility(cities, facilities)

        if new_util < previous_util:
            new_cell.remove_facility()
            previous_cell.add_facility(curr_facility)








