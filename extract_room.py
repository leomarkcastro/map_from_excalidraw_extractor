# import json file
import json


def main():
    data = json.load(open('rooms.excalidraw'))
    elements = data['elements']

    room_dict = {
        "house": "#e6498",
        "hotel": "#e6aaa",
        "shop": "#7950f",
        "clinic": "#12b88",
        "mechanic": "#dddd5",
        "gunshop": "#ff525",
    }

    def get_rooms(building_list, roomID):
        rooms = []
        i = 0
        while True:
            _room_dat = (
                list(
                    filter(
                        lambda x:
                            x['backgroundColor']
                            [:len(roomID)+2]
                        ==  # it would collect like this "#ff525" + "0" + "1"
                            f"{roomID}{i}2", building_list
                    )
                )
            )
            if len(_room_dat) > 0:
                rooms.append(_room_dat)
                i += 1
            else:
                break
        return rooms

    element_dict = {
        "enemy_weak": "#880808f0",
        "enemy_mid": "#880808f1",
        "enemy_hard": "#880808f2",
        "enemy_station": "#880808f3",
        "enemy_boss": "#880808f4",
        "pickup_lv1": "#ffd700f0",
        "pickup_lv2": "#ffd700f1",
        "pickup_lv3": "#ffd700f2",
        "pickup_splv1": "#ffd700f3",
        "pickup_splv2": "#ffd700f4",
        "pickup_splv3": "#ffd700f5",
        "world_wall": "#964b00",
        "world_door": "#4b371c",
        "world_roof": "#303030",
        "world_crate": "#e677f0",
    }

    # reverse key val on element dict
    element_dict_rev = {v: k for k, v in element_dict.items()}

    def filter_room_elements(elements_list, elementIDs):
        return [{
            "width": round(i['width'], 2),
            "height": round(i['height'], 2),
            "center": list(map(lambda x: round(x, 2), (i["x"] + i["width"] / 2, i["y"] + i["height"] / 2))),
            "element_type": element_dict_rev[i['strokeColor']],
            "room_code": i['backgroundColor'][:-2],
            "level": int(i['backgroundColor'][-1]),

        } for i in elements_list if i['strokeColor'] in elementIDs]

        # return list(
        #     filter(lambda x: x['strokeColor'] == elementID, elements_list))

    def room_maker(element_list):
        roofmain = filter_room_elements(
            element_list, [element_dict["world_roof"]])
        return {
            "walls": filter_room_elements(element_list, [element_dict["world_wall"]]),
            "doors": filter_room_elements(element_list, [element_dict["world_door"]]),
            "roofs":  filter_room_elements(element_list, [element_dict["world_roof"]]),
            "crates":  filter_room_elements(element_list, [element_dict["world_crate"]]),
            "pickups": filter_room_elements(element_list, [element_dict[i] for i in element_dict if "pickup" in i]),
            "enemies": filter_room_elements(element_list, [element_dict[i] for i in element_dict if "enemy" in i]),
            "center": roofmain[0]["center"] if len(roofmain) > 0 else [0, 0],
            "size": [roofmain[0]["width"], roofmain[0]["height"]] if len(roofmain) > 0 else [0, 0],
        }

    def get_room_data(room_type):
        room_id = room_dict[room_type]
        rooms = get_rooms(elements, room_id)
        print(f"Found {len(rooms)} {room_type} rooms")
        return [room_maker(i) for i in rooms]

    # export to map json
    rooms_data = {
        "house": get_room_data("house"),
        "hotel": get_room_data("hotel"),
        "shop": get_room_data("shop"),
        "clinic": get_room_data("clinic"),
        "mechanic": get_room_data("mechanic"),
        "gunshop": get_room_data("gunshop"),
    }

    # print(map_data)
    with open('rooms.json', 'w') as outfile:
        json.dump(rooms_data, outfile)

    print("Saved rooms.json")


if __name__ == "__main__":
    main()
