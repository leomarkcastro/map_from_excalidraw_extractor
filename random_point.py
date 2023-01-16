import random
from shapely.geometry import Point
from shapely.geometry import Polygon

# point(s) per square m2
default_density = 0.0035


def generate_random(point_list, holes_list=[], density=default_density):

    points = []

    if len(holes_list) == 0:
        polygon = Polygon(point_list).buffer(0)
    else:
        polygon = Polygon(point_list, holes=holes_list).buffer(0)

    # bounds
    minx, miny, maxx, maxy = polygon.bounds

    # size
    width, height = maxx - minx, maxy - miny

    # number of points
    number = int(width*height * density)

    # print("Number of points: ", number)

    while len(points) < number:

        pnt = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))

        if polygon.contains(pnt):
            points.append([round(pnt.x, 2), round(pnt.y, 2)])

    return points
