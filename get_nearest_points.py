from scipy.spatial import KDTree
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

how_many_points = 10
how_many_vertices = 4 + 1


def get_nearest_points(points, vertices=how_many_vertices):
    points = points or np.random.rand(how_many_points, 2)
    kdtree = KDTree(points)

    points_to_vertices = []

    # for each point, get the 5 nearest points
    # make sure that the connection is bidirectional
    for i in range(len(points)):
        ds, pt = kdtree.query(points[i], k=vertices)
        points_to_vertices.append(
            list(map(lambda x: round(x, 2), (pt.tolist())))[1:]
            # list(zip(list(map(lambda x: round(x, 2), (pt.tolist()))), list(map(lambda x: round(x, 2), ds))))[1:]
        )

    # pretty_print(points_to_vertices)
    # draw_graph(points_to_vertices)

    return points_to_vertices


def pretty_print(points_to_vertices):
    for i in range(len(points_to_vertices)):
        print(f"Pt {i} ->")
        for j in range(len(points_to_vertices[i])):
            print(
                f"\t* Pt {points_to_vertices[i][j][0]} [{points_to_vertices[i][j][1]:.2f}]")


def draw_graph(points_to_vertices):
    G = nx.Graph()

    for i in range(len(points_to_vertices)):
        for j in range(len(points_to_vertices[i])):
            G.add_edge(i, points_to_vertices[i][j][0])

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True)
    plt.show()


if __name__ == "__main__":
    get_nearest_points(False)
