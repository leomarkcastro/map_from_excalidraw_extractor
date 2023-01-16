import random
import math
from shapely.geometry import Point
from shapely.geometry import Polygon


def gridify_point(point_list, holes_list=[], x_box=10, y_box=10):

    points = []

    polygon = Polygon(point_list, holes=holes_list).buffer(0)

    # bounds
    minx, miny, maxx, maxy = polygon.bounds

    # size
    width, height = maxx - minx, maxy - miny

    # print("Number of points: ", number)

    for y_g in range(math.ceil(height / y_box)):
        for x_g in range(math.ceil(width / x_box)):

            pnt = Point(minx + (x_g + 0.5) * x_box, miny + (y_g + 0.5) * y_box)

            if polygon.contains(pnt):
                points.append([round(pnt.x, 2), round(pnt.y, 2)])

    return points
