from shapely.geometry import Polygon, Point
import matplotlib.pyplot as plt
import geopandas as gpd
import random


def display(polygonpoint_list_list, point_list=[]):

    # plot polygon and point on the same plot

    fig, ax = plt.subplots(figsize=(6, 6))

    for polygonpoint_list in polygonpoint_list_list:
        polygon1 = Polygon(polygonpoint_list)
        # random color
        color = '#%06X' % random.randint(0, 0xFFFFFF)
        p = gpd.GeoSeries(polygon1)
        p.plot(ax=ax, color=color, alpha=0.5)

    if len(point_list) > 0:
        point_list = [Point(x[0], x[1]) for x in point_list]
        points = gpd.GeoSeries(point_list)
        points.plot(ax=ax, color="red", markersize=1)

    plt.show()
