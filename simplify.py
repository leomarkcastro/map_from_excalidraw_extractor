import numpy as np
from simplification.cutil import (
    simplify_coords,  # this is Douglas-Peucker
    simplify_coords_vw,  # this is Visvalingam-Whyatt
)


def simplify_line(coords_list, epsilon=0.00025):

    # convert to numpy array
    coords = np.array(coords_list)

    # how many coordinates returns DP with eps=0.01?
    simplified_coords = simplify_coords(coords, epsilon)
    # 30 / 5000

    # convert back to list
    simplified_coords = [
        [round(i[0], 2), round(i[1], 2)]
        for i in simplified_coords.tolist()]

    return simplified_coords


if __name__ == "__main__":
    # generate coords of 5000 ordered points as a line
    coords = np.sort(np.random.rand(5000, 2), axis=0)
    print(len(coords))
    print(coords[:5])

    # how many coordinates returns DP with eps=0.01?
    print(simplify_coords(coords, .00025).shape)
    # 30 / 5000

    # how many coordinates returns VW with eps=0.001?
    print(simplify_coords_vw(coords, .00001).shape)
    # 28 / 500

    # % % timeit
    print(simplify_coords(coords, .0025)[:5])

    # % % timeit
    # print(simplify_coords_vw(coords, .0001))
