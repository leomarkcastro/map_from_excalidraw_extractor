import numpy as np
from simplification.cutil import (
    simplify_coords,  # this is Douglas-Peucker
    simplify_coords_vw,  # this is Visvalingam-Whyatt
)

coords = [
    [0, 0],
    [0, 1],
    [0, 2],
    [0, 3],
]

# convert to numpy array
coords = np.array(coords)

# how many coordinates returns DP with eps=0.01?
simplified_coords = simplify_coords(coords, .00025)
# 30 / 5000

# convert back to list
simplified_coords = simplified_coords.tolist()
