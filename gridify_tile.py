from shapely.ops import unary_union
import math
from shapely.geometry import Point
from shapely.geometry import Polygon, MultiPolygon
import geopandas as gpd


def compute_side_from_index(index, x_size):
    top_left = index - x_size - 1
    top = index - x_size
    top_right = index - x_size + 1
    left = index - 1
    center = index
    right = index + 1
    bottom_left = index + x_size - 1
    bottom = index + x_size
    bottom_right = index + x_size + 1

    return [top_left, top, top_right, left, center, right, bottom_left, bottom, bottom_right]


def compare_two_list(list1,  list2):
    if len(list1) != len(list2):
        return False

    for i in range(len(list1)):
        if list2[i] == None:
            continue
        if list1[i] != list2[i]:
            return False

    return True


def gridify_tile(point_list, holes_list=[], x_box=10, y_box=10):

    points = {}

    polygon = Polygon(point_list, holes=holes_list).buffer(0)

    # bounds
    minx, miny, maxx, maxy = polygon.bounds

    # size
    width, height = maxx - minx, maxy - miny

    # print("Number of points: ", number)

    x_size = math.ceil(width / x_box)
    y_size = math.ceil(height / y_box)

    def compute_pnt(x_g, y_g):
        return Point(minx + (x_g + 0.5) * x_box, miny + (y_g + 0.5) * y_box)

    for y_g in range(y_size):
        for x_g in range(x_size):

            pnt = compute_pnt(x_g, y_g)

            '''
                1 2 3  10 11
                4 5 6  12 13
                7 8 9
                -4 -3 -2
                -1  0  1
                 2  3  4
            '''

            keyed_x_y = f"{x_g:04}_{y_g:04}"

            if polygon.contains(pnt) and keyed_x_y not in points:

                sides = compute_side_from_index(y_g * x_size + x_g, x_size)

                did_side_collide = [
                    1 if polygon.contains(compute_pnt(index %
                                                      x_size, index//x_size)) else 0
                    for index in sides
                ]

                # default tile
                tile = 5
                x = 0
                O = 1
                _ = None

                if compare_two_list(did_side_collide, [
                    x, x, _,
                    x, O, O,
                    _, O, _,
                ]):
                    tile = 1
                elif compare_two_list(did_side_collide, [
                    _, x, _,
                    O, O, O,
                    _, O, _,
                ]):
                    tile = 2
                elif compare_two_list(did_side_collide, [
                    _, x, x,
                    O, O, x,
                    _, O, _,
                ]):
                    tile = 3
                elif compare_two_list(did_side_collide, [
                    _, O, _,
                    x, O, O,
                    _, O, _,
                ]):
                    tile = 4
                # 5 is default, so we skip to...
                elif compare_two_list(did_side_collide, [
                    _, O, _,
                    O, O, x,
                    _, O, _,
                ]):
                    tile = 6
                elif compare_two_list(did_side_collide, [
                    _, O, _,
                    x, O, O,
                    x, x, _,
                ]):
                    tile = 7
                elif compare_two_list(did_side_collide, [
                    _, O, _,
                    O, O, O,
                    _, x, _,
                ]):
                    tile = 8
                elif compare_two_list(did_side_collide, [
                    _, O, _,
                    O, O, x,
                    _, x, _,
                ]):
                    tile = 9
                elif compare_two_list(did_side_collide, [
                    _, O, _,
                    O, O, O,
                    _, O, x,
                ]):
                    tile = 10
                elif compare_two_list(did_side_collide, [
                    _, O, _,
                    O, O, O,
                    x, O, _,
                ]):
                    tile = 11
                elif compare_two_list(did_side_collide, [
                    _, O, x,
                    O, O, O,
                    _, O, _,
                ]):
                    tile = 12
                elif compare_two_list(did_side_collide, [
                    x, O, _,
                    O, O, O,
                    _, O, _,
                ]):
                    tile = 13

                points[keyed_x_y] = {
                    "x": round(pnt.x, 2),
                    "y": round(pnt.y, 2),
                    "tile": tile,
                }
    return {
        "xsize": x_size,
        "ysize": y_size,
        "total": x_size * y_size,
        "points": points,
        "bounds": [minx, miny, maxx, maxy],
    }


def gridify_tile_combined(point_list_list, holes_list=[], x_box=10, y_box=10, bounds=[]):

    points = {}

    polygons = [Polygon(poly).buffer(0)
                for poly in point_list_list]
    polygon = unary_union(polygons).buffer(0)

    # bounds
    if bounds:
        minx, miny, maxx, maxy = bounds
    else:
        minx, miny, maxx, maxy = polygon.bounds

    # size
    width, height = maxx - minx, maxy - miny

    # print("Number of points: ", number)

    x_size = math.ceil(width / x_box)
    y_size = math.ceil(height / y_box)

    def compute_pnt(x_g, y_g):
        return Point(minx + (x_g + 0.5) * x_box, miny + (y_g + 0.5) * y_box)

    for y_g in range(y_size):
        for x_g in range(x_size):

            pnt = compute_pnt(x_g, y_g)

            keyed_x_y = f"{x_g:04}_{y_g:04}"

            if polygon.contains(pnt) and keyed_x_y not in points:
                sides = compute_side_from_index(y_g * x_size + x_g, x_size)

                did_side_collide = [
                    1 if polygon.contains(compute_pnt(index %
                                                      x_size, index//x_size)) else 0
                    for index in sides
                ]

                # default tile
                tile = 5
                x = 0
                O = 1
                _ = None

                if compare_two_list(did_side_collide, [
                    x, x, _,
                    x, O, O,
                    _, O, _,
                ]):
                    tile = 1
                elif compare_two_list(did_side_collide, [
                    _, x, _,
                    O, O, O,
                    _, O, _,
                ]):
                    tile = 2
                elif compare_two_list(did_side_collide, [
                    _, x, x,
                    O, O, x,
                    _, O, _,
                ]):
                    tile = 3
                elif compare_two_list(did_side_collide, [
                    _, O, _,
                    x, O, O,
                    _, O, _,
                ]):
                    tile = 4
                # 5 is default, so we skip to...
                elif compare_two_list(did_side_collide, [
                    _, O, _,
                    O, O, x,
                    _, O, _,
                ]):
                    tile = 6
                elif compare_two_list(did_side_collide, [
                    _, O, _,
                    x, O, O,
                    x, x, _,
                ]):
                    tile = 7
                elif compare_two_list(did_side_collide, [
                    _, O, _,
                    O, O, O,
                    _, x, _,
                ]):
                    tile = 8
                elif compare_two_list(did_side_collide, [
                    _, O, _,
                    O, O, x,
                    _, x, _,
                ]):
                    tile = 9
                elif compare_two_list(did_side_collide, [
                    _, O, _,
                    O, O, O,
                    _, O, x,
                ]):
                    tile = 10
                elif compare_two_list(did_side_collide, [
                    _, O, _,
                    O, O, O,
                    x, O, _,
                ]):
                    tile = 11
                elif compare_two_list(did_side_collide, [
                    _, O, x,
                    O, O, O,
                    _, O, _,
                ]):
                    tile = 12
                elif compare_two_list(did_side_collide, [
                    x, O, _,
                    O, O, O,
                    _, O, _,
                ]):
                    tile = 13

                points[keyed_x_y] = {
                    "x": round(pnt.x, 2),
                    "y": round(pnt.y, 2),
                    "tile": tile,
                    # "did_side_collide": did_side_collide,
                }

    return {
        "xsize": x_size,
        "ysize": y_size,
        "total": x_size * y_size,
        "points": points
    }
