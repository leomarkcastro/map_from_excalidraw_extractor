# import json file
import json
import math
from simplify import simplify_line
from display_poly import display
from random_point import generate_random
from gridify_point import gridify_point
from gridify_tile import gridify_tile, gridify_tile_combined
from get_nearest_points import get_nearest_points, how_many_vertices
import random
import numpy as np

data = json.load(open('boracayv2_2.excalidraw'))
elements = data['elements']


def random_id_generator(length=16):
    return ''.join(random.choices('0123456789abcdef', k=length))


def get_building_data(data, bldg_type="house"):
    return {
        "id": data["id"],
        "center": list(map(lambda x: round(x, 2), (data["x"] + data["width"] / 2, data["y"] + data["height"] / 2))),
        "width": round(data["width"], 2),
        "height": round(data["height"], 2),
        "radius": round(max(data["width"], data["height"]) / 2, 2),
        "bldg_type": bldg_type,
    }


def get_element_from_json(building_list, color, color2="#000000"):
    return list(
        filter(lambda x: x['backgroundColor'] == color and x["strokeColor"] == color2, building_list))


def get_building_processed_list(building_list, color, bldg_type="house", stroke_color="#000000"):
    return list(map(lambda x: get_building_data(x, bldg_type), get_element_from_json(building_list, color, stroke_color)))


def convert_pathpoints_to_2dmesh(pathpoints):
    # convert path points to svg path string
    path_string = "M" + "L".join(
        list(map(lambda x: f"{x[0]},{x[1]}", pathpoints)))
# convert svg path string to 2d mesh


def getmesh_data(x, simplify_rate=1.0, generate_points_data=False):
    actual = list(
        map(
            lambda y:
            [round(y[0], 2), round(y[1], 2)], x["points"]
        )
    )
    minimized = simplify_line(actual, simplify_rate)
# print("Minimized: ", len(minimized), "Actual: ", len(actual))

# get hypothenuse of width and height
    hypothenuse = math.sqrt(x["width"]**2 + x["height"]**2)

    ret_data = {
        "id": x["id"],
        "points": actual,
        "points_less": minimized,
        "center": list(map(lambda _x: round(_x, 2), (x["x"] + x["width"] / 2, x["y"] + x["height"] / 2))),
        "width": round(x["width"], 2),
        "height": round(x["height"], 2),
        "radius": round(hypothenuse, 2),
        "start":
        list(map(lambda x: round(x, 2),
                 (x["x"], x["y"])))
    }

    if generate_points_data:
        [
            density,
            tree_percent,
            spawn_percent,
        ] = generate_points_data
        points = generate_random(ret_data["points_less"], density=density)

        random.shuffle(points)
        len_points = len(points)

        ret_data["points_data"] = list(map(lambda x: {
            "point_type": "tree",
            "center": x,
            "id": random_id_generator()
        }, points[:int(len_points * tree_percent)]))

        ret_data["points_data"] += list(map(lambda x: {
            "point_type": "spawn",
            "center": x,
            "id": random_id_generator()
        }, points[int(
            len_points * (tree_percent)):]))

    return ret_data


def get_pointlist(elements, color, color2="#000000", generate_points_data=False):
    return list(
        map(
            lambda data: getmesh_data(
                data, generate_points_data=generate_points_data),
            get_element_from_json(elements, color, color2)
        )
    )


def extract_map_shapes():

    # get home locaiton
    home = get_building_data(get_element_from_json(
        elements, "#ff0000")[0], "home")
    print(home)

    # get all loot houses
    loot_houses = get_building_processed_list(elements, "#e64980", "loot")
    print(f"Extracted houses: {len(loot_houses)}")
    # print(loot_houses[:5])

    # get all big houses
    big_houses = get_building_processed_list(elements, "#e6aaaa", "big")
    print(f"Extracted hotels: {len(big_houses)}")
    # print(big_houses[:5])

    # get all markets
    markets = get_building_processed_list(elements, "#7950f2", "market")
    print(f"Extracted markets: {len(markets)}")
    # print(markets[:5])

    # get all clinics
    clinics = get_building_processed_list(elements, "#12b886", "clinic")
    print(f"Extracted clinics: {len(clinics)}")
    # print(clinics[:5])

    # get all Mechanic
    mechanics = get_building_processed_list(elements, "#dddd55", "mechanic")
    print(f"Extracted mechanics: {len(mechanics)}")
    # print(mechanics[:5])

    # get all gunshop
    gunshop = get_building_processed_list(elements, "#ff5252", "gunshop")
    print(f"Extracted gunshop: {len(gunshop)}")
    # print(gunshop[:5])

    mission = get_building_processed_list(elements, "#e6e6fa", "mission")
    print(f"Extracted mission: {len(mission)}")
    # print(mission[:5])

    island_vectorpoints = getmesh_data(
        get_element_from_json(elements, "#40c057aa")[0], 4.0)
    # print(
    #     f"Island vector points: {len(island_vectorpoints)}. => {island_vectorpoints[1]}")

    sand_vectorpoints = getmesh_data(
        get_element_from_json(elements, "#ddddca")[0], 4.0)

    # print(
    #     f"Sand vector points: {len(sand_vectorpoints)}. => {sand_vectorpoints[1]}")

    mountain_list_vectorpoints = get_pointlist(elements, "#82c91e")
    # print(
    #     f"Island vector points: {len(mountain_list_vectorpoints)}. => {mountain_list_vectorpoints[0][1]}")
    mountain_list_data = get_building_processed_list(
        elements, "#82c91e", "mountain")
    print(f"Extracted mountain list: {len(mountain_list_data)}")

    forest_list_vectorpoints = get_pointlist(
        elements, "#40c057", "#5c940d", [0.0035, 0.65, 0.35])
    # print(
    #     f"Forest vector points: {len(forest_list_vectorpoints)}. => {forest_list_vectorpoints[0][1]}")
    forest_list_data = get_building_processed_list(
        elements, "#40c057", "forest", stroke_color="#5c940d")
    print(f"Extracted forest list: {len(forest_list_data)}")

    grayroad_list_vectorpoints = get_pointlist(elements, "#be4bdb", "#495057")

    grayroad_list_data = get_building_processed_list(
        elements, "#be4bdb", "road", stroke_color="#495057")
    print(f"Extracted road list: {len(grayroad_list_data)}")

    grassfield_list_vectorpoints = get_pointlist(
        elements, "#40c057", "#5cf40dd3", [0.002, 0.5, 0.5])

    grassfield_list_data = get_building_processed_list(
        elements, "#40c057", "grass", stroke_color="#5cf40dd3")
    print(f"Extracted grassfield list: {len(grassfield_list_data)}")

    # export to map json
    map_data = {
        "buildings": [
            home,
            *loot_houses,
            *big_houses,
            *markets,
            *clinics,
            *mechanics,
            *gunshop,
            *mission,
            # *mountain_list_data,
            # *forest_list_data,
            # *grayroad_list_data,
        ],
        "mountain_list_vectorpoints": mountain_list_vectorpoints,
        "grayroad_list_vectorpoints": grayroad_list_vectorpoints,
        "forest_list_vectorpoints": forest_list_vectorpoints,
        "grassfield_list_vectorpoints": grassfield_list_vectorpoints,
        "land_vectorpoints_outline": island_vectorpoints,
        "sand_vectorpoints_outline": sand_vectorpoints,
    }

    # print(map_data)
    with open('map.json', 'w') as outfile:
        json.dump(map_data, outfile)

    print("Saved map.json")


def get_pointslist(list_object):
    return list(map(lambda x: x["points_less"], list_object))


def translate_pointslist(pointslist, dx, dy):
    return list(map(lambda x: [x[0] + dx, (x[1] - dy) * -1], pointslist))


def extract_map_points():
    island_vectorpoints = getmesh_data(
        get_element_from_json(elements, "#40c057aa")[0], 4.0)

    mountain_list_vectorpoints = get_pointlist(elements, "#82c91e")

    # check_what = 7
    all_points = []
    # for forest in grassfield_list_vectorpoints[check_what:check_what+1]:
    #     all_points.extend(generate_random(forest["points_less"]))
    # print(island_vectorpoints["points_less"], end="\n\n----\n\n")
    # print(list(
    #     map(lambda x:  translate_pointslist(
    #         x["points_less"], x["start"][0], x["start"][1]), mountain_list_vectorpoints)
    # )[0])
    all_points.extend(
        gridify_point(
            translate_pointslist(
                island_vectorpoints["points_less"], island_vectorpoints["start"][0], island_vectorpoints["start"][1]*-1),
            holes_list=list(
                map(lambda x:  translate_pointslist(
                    x["points_less"], x["start"][0], x["start"][1]*-1), mountain_list_vectorpoints)
            ),
            x_box=10.0,
            y_box=10.0,
        )
    )

    print("total points: ", len(all_points))
    print("total vertices: ", len(all_points) * (5 - 1))
    # display(
    #     [
    #         translate_pointslist(
    #             island_vectorpoints["points_less"], island_vectorpoints["start"][0], island_vectorpoints["start"][1]*-1),
    #         *list(
    #             map(lambda x:  translate_pointslist(
    #                 x["points_less"], x["start"][0], x["start"][1]*-1), mountain_list_vectorpoints)
    #         )
    #     ],
    #     all_points
    #     # []
    # )

    graph_data = get_nearest_points([np.array(i) for i in all_points], 5)

    with open('graph.json', 'w') as outfile:
        json.dump({"points": all_points, "vertices": graph_data}, outfile)

    print("Saved graph.json")


def extract_map_tiles_grass():
    island_vectorpoints = getmesh_data(
        get_element_from_json(elements, "#40c057aa")[0], simplify_rate=4.0)

    # mountain_list_vectorpoints = get_pointlist(elements, "#82c91e")

    data = gridify_tile(
        translate_pointslist(
            island_vectorpoints["points_less"], island_vectorpoints["start"][0], island_vectorpoints["start"][1]*-1),
        x_box=16.0,
        y_box=16.0,
    )

    # print("total points: ", len(all_points["points"]))
    with open('tiledata_grass.json', 'w') as outfile:
        json.dump(data, outfile)

    print("Saved tiledata_grass.json")
    return data["bounds"]


def extract_map_tiles_mountains(bounds):
    # island_vectorpoints = getmesh_data(
    #     get_element_from_json(elements, "#40c057aa")[0], simplify_rate=4.0)

    mountain_list_vectorpoints = get_pointlist(elements, "#82c91e")

    data = gridify_tile_combined(
        list(
            map(lambda x:  translate_pointslist(
                x["points_less"], x["start"][0], x["start"][1]*-1), mountain_list_vectorpoints)
        ),
        x_box=16.0,
        y_box=16.0,
        bounds=bounds
    )

    # print("total points: ", len(all_points["points"]))
    with open('tiledata_mountain.json', 'w') as outfile:
        json.dump(data, outfile)

    print("Saved tiledata_mountain.json")


def extract_map_tiles_cement(bounds):
    # island_vectorpoints = getmesh_data(
    #     get_element_from_json(elements, "#40c057aa")[0], simplify_rate=4.0)

    cement_list_vectorpoints = get_pointlist(elements, "#868e96", "#343a40")

    data = gridify_tile_combined(
        list(
            map(lambda x:  translate_pointslist(
                x["points_less"], x["start"][0], x["start"][1]*-1), cement_list_vectorpoints)
        ),
        x_box=16.0,
        y_box=16.0,
        bounds=bounds
    )

    # print("total points: ", len(all_points["points"]))
    with open('tiledata_cement.json', 'w') as outfile:
        json.dump(data, outfile)

    print("Saved tiledata_cement.json")


if __name__ == "__main__":
    bounds = extract_map_tiles_grass()
    extract_map_tiles_cement(bounds)
