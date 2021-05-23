
import math
import data
import matplotlib.pyplot as plt


def calculate_membership(value, table_name):
    """
    :param value: crisp value
    :param table_name: a table name indicating which value must be calculated
    :return: membership value along with the linguistic variable
    """
    table = {}
    if table_name == 'HV':
        table = data.market_value_of_houses_ms
    elif table_name == 'HL':
        table = data.location_of_houses_ms
    elif table_name == 'AA':
        table = data.assets_of_applicant_ms
    elif table_name == 'IA':
        table = data.income_of_applicant_ms
    elif table_name == 'HE':
        table = data.house_ms
    elif table_name == 'AE':
        table = data.applicant_ms
    elif table_name == 'I':
        table = data.interest_ms
    membership_values = []
    for key in table.keys():
        if table[key][0] <= value < table[key][1]:
            membership_value = ((value - table[key][0])
                                / (table[key][1] - table[key][0]))
            if membership_value != 0:
                membership_values.append((key, membership_value))
        elif table[key][1] <= value <= table[key][2]:
            membership_values.append((key, 1.0))
        elif table[key][2] < value <= table[key][3]:
            membership_value = ((table[key][3] - value)
                                / (table[key][3] - table[key][2]))
            if membership_value != 0:
                membership_values.append((key, membership_value))
    return membership_values


def two_sets_cross_product(set_one, set_two):
    """
    :param set_one: membership value, linguistic variable pairs
    :param set_two: membership value, linguistic variable pairs
    :return: cartesian product of the sets
    """
    combinations = []
    for subset_one in set_one:
        for subset_two in set_two:
            combinations.append((subset_one, subset_two))
    return combinations


def four_sets_cross_product(set_one, set_two, set_three, set_four):
    """
    :param set_one: membership value, linguistic variable pairs
    :param set_two: membership value, linguistic variable pairs
    :param set_three: membership value, linguistic variable pairs
    :param set_four: membership value, linguistic variable pairs
    :return: cartesian product of the sets
    """
    combinations = []
    for subset_one in set_one:
        for subset_two in set_two:
            for subset_three in set_three:
                for subset_four in set_four:
                    combinations.append((subset_one, subset_two, subset_three, subset_four))
    return combinations


def find_min(combinations, evaluation_table):
    """
    :param combinations: the combinations of the cross-products
    :param evaluation_table: name indicating which rule set must be used
    :return: linguistic variable, membership value pair extracted from rule set according to larsen inference method
    """
    result = []
    if evaluation_table == 'HE':
        for combination in combinations:
            if combination[0][0] == 'low':
                result.append(('low', combination[0][1]))
            if combination[1][0] == 'bad':
                result.append(('low', combination[1][1]))
            result.append((data.house_evaluation_rule_set[combination[1][0]][combination[0][0]],
                           min(combination[0][1], combination[1][1])))
    elif evaluation_table == 'AE':
        for combination in combinations:
            result.append((data.applicant_evaluation_rule_set[combination[0][0]][combination[1][0]],
                           min(combination[0][1], combination[1][1])))
    elif evaluation_table == 'CE':
        for combination in combinations:
            if combination[2][0] == 'low':
                result.append(('very_low', combination[2][1]))
            if combination[1][0] == 'very_low':
                result.append(('very_low', combination[2][1]))
            if ((combination[3][0] == 'low' and (combination[0][0] == 'medium' or combination[0][0] == 'high')) or
                    (combination[3][0] == 'medium' and combination[0][0] == 'high')):
                result.append((data.evaluation_of_the_credit_rule_set_ii[combination[3][0]][combination[0][0]],
                               min(combination[3][1], combination[0][1])))
            if combination[2][0] == 'medium' or combination[2][0] == 'high':
                result.append((data.evaluation_of_the_credit_rule_set_ah[combination[2][0]][combination[1][0]],
                               min(combination[2][1], combination[1][1])))
    return result


def filter_memberships(memberships):
    """
    :param memberships: linguistic variable, membership value pair extracted from
                        rule set according to larsen inference method
    :return: if there is linguistic variable, membership value pairs with the same linguistic variable value only keep
            the one with the max membership value
    """
    new_memberships = []
    scanned = []
    for i in range(len(memberships)):
        max_number = memberships[i][1]
        index = i
        for j in range(len(memberships)):
            if i == j or memberships[i][0] != memberships[j][0]:
                continue
            if memberships[j][1] > max_number:
                max_number = memberships[j][1]
                index = j
        if memberships[index][0] not in scanned:
            new_memberships.append(memberships[index])
            scanned.append(memberships[index][0])
    return new_memberships


def larsen_inference_evaluation(memberships, table):
    """
    :param memberships: linguistic variable, membership value pair extracted from
                        rule set according to larsen inference method
    :param table: table name
    :return: fuzzy number, membership pairs according to larsen inference method
    """
    numbers = {}
    if table == 'HMS':
        numbers = data.house_ms
    elif table == 'AMS':
        numbers = data.applicant_ms
    elif table == 'CMS':
        numbers = data.credit_amount_ms
    triangular_numbers = []
    for membership in memberships:
        triangular_numbers.append((numbers[membership[0]], membership[1], membership[0]))
    triangular_numbers.sort(key=lambda x: x[0][3])
    return triangular_numbers


def line_intersection(line1, line2):
    """
    :param line1: list of two points
    :param line2: list of two points
    :return: tuple (x, y) containing the intersection coordinates if the lines intersect
    """
    x_diff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    y_diff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(x_diff, y_diff)
    if div == 0:
        raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, x_diff) / div
    y = det(d, y_diff) / div
    return x, y


def union(numbers, label):
    """
    :param numbers: fuzzy number, membership value pairs
    :param label: name of the evaluation process
    :return: fuzzy union of these fuzzy numbers method used is max()
    """
    plt.style.use('fivethirtyeight')
    x_points = []
    y_points = []
    for number in numbers:
        x_points.append([number[0][0], number[0][1], number[0][2], number[0][3]])
        y_points.append([0, number[1], number[1], 0])
    for i in range(len(x_points)):
        plt.plot(x_points[i], y_points[i], label=numbers[i][2])
    plt.legend()
    plt.title(label)
    plt.show()
    for i in range(len(x_points) - 1):
        line1 = ((x_points[i][2], y_points[i][2]), (x_points[i][3], y_points[i][3]))
        line2 = ((x_points[i + 1][0], y_points[i + 1][0]), (x_points[i + 1][1], y_points[i + 1][1]))
        intersection_point = line_intersection(line1, line2)
        x_points[i][3] = intersection_point[0]
        y_points[i][3] = intersection_point[1]
        x_points[i + 1][0] = intersection_point[0]
        y_points[i + 1][0] = intersection_point[1]

    new_x_points = []
    new_y_points = []
    points_set = []
    for subset in x_points:
        for number in subset:
            new_x_points.append(number)
    for subset in y_points:
        for number in subset:
            new_y_points.append(number)
    for i in range(len(new_x_points)):
        points_set.append((new_x_points[i], new_y_points[i]))
    plt.plot(new_x_points, new_y_points, label=label + ' Union')
    plt.legend()
    plt.title(label)
    plt.show()

    return points_set


def find_line_from_2points(point1, point2):
    """
    :param point1: cartesian coordinate
    :param point2: cartesian coordinate
    :return: a list containing a line as follows [slope, y-intercept]
    """
    slope = (point2[1] - point1[1]) / (point2[0] - point1[0])
    y_intercept = point2[1] - point2[0] * slope
    return [slope, y_intercept]


def line_definite_integral(line, bounds):
    """
    :param line: [slope, y-intercept]
    :param bounds: x-interval [x-left, x-right]
    :return: definite integral of the line on the x-interval
    """
    return (line[0] * (bounds[1] ** 2 / 2) + line[1] * bounds[1]) - (
            line[0] * (bounds[0] ** 2 / 2) + line[1] * bounds[0])


def parabola_definite_integral(line, bounds):
    """
    :param line: [slope, y-intercept]
    :param bounds: x-interval [x-left, x-right]
    :return: definite integral of the line equation multiplied by 'x', on the x-interval
    """
    return (line[0] * (bounds[1] ** 3 / 3) + line[1] * (bounds[1] ** 2 / 2)) - (
            line[0] * (bounds[0] ** 3 / 3) + line[1] * (bounds[0] ** 2 / 2))


def center_of_area(points):
    """
    :param points: a list of cartesian points [(x1, y1), (x2, y2), ..., (xn, yn)]
    :return: x value that identify the center of area formed by the list of points
    """
    denominator = 0
    nominator = 0
    for i in range(len(points) - 1):
        if ((points[i][0] == points[i + 1][0] and points[i][1] == points[i + 1][1]) or
                points[i][0] == points[i + 1][0]):
            continue
        line = find_line_from_2points(points[i], points[i + 1])
        denominator += line_definite_integral(line, [points[i][0], points[i + 1][0]])
        nominator += parabola_definite_integral(line, [points[i][0], points[i + 1][0]])
    return nominator / denominator


def find_x(point_left, point_right, area, half_area):
    """
    :param point_left: a cartesian point in which half of the area lies after
    :param point_right: a cartesian point in which half of the area lies before
    :param area: summed subarea in which it's less than half of the area
    :param half_area: the value of half of the area
    :return: x-coordinate that split the curve into two equal areas
    """
    line = find_line_from_2points(point_left, point_right)
    if line[0] != 0:
        coefficient = 2 / line[0]
        a = 1
        b = coefficient * line[1]
        c = coefficient * (area - line[0] * (point_left[0] ** 2 / 2) -
                           line[1] * point_left[0] - half_area)
        delta = b ** 2 - 4 * a * c
        x1 = (-b + math.sqrt(delta)) / (2 * a)
        x2 = (-b - math.sqrt(delta)) / (2 * a)
        if point_left[0] <= x1 <= point_right[0]:
            return x1
        else:
            return x2
    else:
        return (half_area - area + line[1]*point_left[0]) / line[1]


def find_x_of_half_area(points, half_of_area):
    """
    a function that determines the x interval in which half of the area lies
    :param points: a list of cartesian points [(x1, y1), (x2, y2), ..., (xn, yn)]
    :param half_of_area: the value of half of the area
    :return: x-coordinate that split the curve into two equal areas
    """
    area = 0
    line_points = []
    for i in range(len(points) - 1):
        if ((points[i][0] == points[i + 1][0] and points[i][1] == points[i + 1][1]) or
                points[i][0] == points[i + 1][0]):
            continue
        line = find_line_from_2points(points[i], points[i + 1])
        sub_area = line_definite_integral(line, [points[i][0], points[i + 1][0]])
        if area + sub_area > half_of_area:
            line_points = [points[i], points[i + 1]]
            break
        elif area + sub_area == half_of_area:
            return points[i][0]
        area += sub_area
    return find_x(line_points[0], line_points[1], area, half_of_area)


def bisector_of_area(points):
    """
    determine half of the area value a list of cartesian points [(x1, y1), (x2, y2), ..., (xn, yn)]
    :param points:
    :return:
    """
    total_area = 0
    for i in range(len(points) - 1):
        if ((points[i][0] == points[i + 1][0] and points[i][1] == points[i + 1][1]) or
                points[i][0] == points[i + 1][0]):
            continue
        line = find_line_from_2points(points[i], points[i + 1])
        total_area += line_definite_integral(line, [points[i][0], points[i + 1][0]])
    half_of_area = total_area / 2
    return find_x_of_half_area(points, half_of_area)


def mean_of_maximum(points, defuzzified_table):
    """
    mean of maximum defuzzification method
    :param points: a list of cartesian points [(x1, y1), (x2, y2), ..., (xn, yn)]
    :param defuzzified_table: table name used for determining whether the fuzzy number is triangular or trapezoidal
    :return: defuzzified value
    """
    tables_limit = {'H': 10, 'A': 10, 'C': 500}
    temp_points = points.copy()
    temp_points.sort(key=lambda x: x[1], reverse=True)
    result = [temp_points[0][0], temp_points[1][0]]
    if sum(result) / 2 > tables_limit[defuzzified_table]:
        return result[0]
    return sum(result) / 2


def defuzzify(points, method, defuzzified_table):
    """
    wrapper
    :param points: a list of cartesian points [(x1, y1), (x2, y2), ..., (xn, yn)]
    :param method: a string indicating the defuzzification method
    :param defuzzified_table: used for mean of max only
    :return: defuzzified value
    """
    methods = {'1': center_of_area, '2': bisector_of_area,
               '3': mean_of_maximum}
    defuzzification_method = methods[method]
    if method == '3':
        defuzzified_value = defuzzification_method(points, defuzzified_table)
    else:
        defuzzified_value = defuzzification_method(points)
    return defuzzified_value
