# SAT Implementation
from math import tan, atan, pi


def projection_point_on_a_line(point, line):
    x1, y1 = line[0]
    x2, y2 = line[1]

    x, y = point

    # 1. Find parametric equation of general point on the line
    x_p = [x1, (x2 - x1)]
    y_p = [y1, (y2 - y1)]

    # print("Printing x_p and y_p")
    # print(x_p, y_p)

    # 2. Find vector of point to line
    A = [
        [x - x_p[0], -x_p[1]],
        [y - y_p[0], -y_p[1]]
    ]
    # print("Printing A")
    # print(A)

    # 3. Find vector parallel to line
    B = [
        x2 - x1,
        y2 - y1
    ]

    # 4. Find t
    t = (A[0][0] * B[0] + A[1][0] * B[1]) / (-A[0][1] * B[0] - A[1][1] * B[1])

    # print("Printing t")
    # print(t)

    # 5. Find point on line
    final_point = (x_p[0] + x_p[1] * t, y_p[0] + y_p[1] * t)
    # print("Printing final point")
    # print(final_point)

    return final_point


def check_if_points_intersect(points1, points2, line):
    x1, y1 = line[0]
    x2, y2 = line[1]

    if x2 == x1:
        m = 2
    else:
        m = (y2 - y1) / (x2 - x1)
    if m < 1:
        points1_x = []
        points2_x = []

        for pointx in points1:
            points1_x.append(pointx[0])

        for pointx in points2:
            points2_x.append(pointx[0])

        if (max(points1_x) < min(points2_x)) or (max(points2_x) < min(points1_x)):
            return False
        else:
            return True
    else:
        points1_y = []
        points2_y = []

        for pointy in points1:
            points1_y.append(pointy[1])

        for pointy in points2:
            points2_y.append(pointy[1])

        if (max(points1_y) < min(points2_y)) or (max(points2_y) < min(points1_y)):
            return False
        else:
            return True


def check_collision_between_polygons(polygon1, polygon2):
    # Let's start with polygon 1. The first index should be repeated
    for i in range(len(polygon1) - 1):

        line = [polygon1[i], polygon1[i + 1]]

        # # Now to find projection of all points on this line
        # projected_points_1 = []
        # for point in polygon1:
        #     projected_points_1.append(projection_point_on_a_line(point, line))
        #
        # projected_points_2 = []
        # for point in polygon2:
        #     projected_points_2.append(projection_point_on_a_line(point, line))
        #
        # # print(projected_points_1)
        # # print(projected_points_2)
        #
        # if not check_if_points_intersect(projected_points_1, projected_points_2, line):
        #     return False

        # Finding the normal line
        x1, y1 = line[0]
        x2, y2 = line[1]

        # Getting the normal to the line
        if x2 is not x1:
            current_m = (y2 - y1) / (x2 - x1)
            new_m = tan(atan(current_m) + pi / 2)
        else:
            # current_m = (y2 - y1)/(x2 - x1)
            new_m = 0

        old_point = line[0]
        new_point = (old_point[0] + 1, new_m * ((old_point[0] + 1) - old_point[0]) + old_point[1])
        line = [old_point, new_point]

        # Now to find projection of all points on this line
        projected_points_1 = []
        for point in polygon1:
            projected_points_1.append(projection_point_on_a_line(point, line))

        projected_points_2 = []
        for point in polygon2:
            projected_points_2.append(projection_point_on_a_line(point, line))

        # print(projected_points_1)
        # print(projected_points_2)

        if not check_if_points_intersect(projected_points_1, projected_points_2, line):
            return False

    # Let's start with polygon 2. The first index should be repeated
    for i in range(len(polygon2) - 1):

        line = [polygon2[i], polygon2[i + 1]]

        # # Now to find projection of all points on this line
        # projected_points_1 = []
        # for point in polygon1:
        #     projected_points_1.append(projection_point_on_a_line(point, line))
        #
        # projected_points_2 = []
        # for point in polygon2:
        #     projected_points_2.append(projection_point_on_a_line(point, line))
        #
        # # print(projected_points_1)
        # # print(projected_points_2)
        #
        # if not check_if_points_intersect(projected_points_1, projected_points_2, line):
        #     return False

        # Finding the normal line
        x1, y1 = line[0]
        x2, y2 = line[1]

        # Getting the normal to the line
        if x2 is not x1:
            current_m = (y2 - y1) / (x2 - x1)
            new_m = tan(atan(current_m) + pi / 2)
        else:
            # current_m = (y2 - y1)/(x2 - x1)
            new_m = 0
        old_point = line[0]
        new_point = (old_point[0] + 1, new_m * ((old_point[0]+1) - old_point[0]) + old_point[1])
        line = [old_point, new_point]

        # Now to find projection of all points on this line
        projected_points_1 = []
        for point in polygon1:
            projected_points_1.append(projection_point_on_a_line(point, line))

        projected_points_2 = []
        for point in polygon2:
            projected_points_2.append(projection_point_on_a_line(point, line))

        # print(projected_points_1)
        # print(projected_points_2)

        if not check_if_points_intersect(projected_points_1, projected_points_2, line):
            return False

    return True


# projection_point_on_a_line((0.5, 0.25), [(2.5, 0), (0, 5)])
# print(check_if_points_intersect([(1, 2), (2, 3), (7, 8)], [(3, 4), (4, 5), (7, 8)], [(1, 2), (7, 8)]))
# print(check_collision_between_polygons([(2, 1), (2, 3), (4, 3), (4, 1), (2, 1)], [(2, 6), (6, 6), (6, 1), (2, 6)]))-