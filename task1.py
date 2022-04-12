import copy
import json
import sys
from collections import deque

graph_1 = [
    [0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 0, 0],
    [0, 1, 0, 1, 1, 1],
    [0, 1, 1, 0, 0, 1],
    [0, 0, 1, 0, 0, 1],
    [0, 0, 1, 1, 1, 0]
]


# BFS algorithm looks for shortest path from start to finish node of the graph
def bfs(graph, start, finish):
    parent = [None for _ in range(len(graph))]
    is_visited = [False for _ in range(len(graph))]
    deq = deque([start])
    is_visited[start] = True

    while len(deq) > 0:
        current = deq.pop()
        if current == finish:
            break

        for i, vertex in enumerate(graph[current]):
            if vertex == 1 and not is_visited[i]:
                is_visited[i] = True
                parent[i] = current
                deq.appendleft(i)
    else:
        return None

    way = deque([finish])
    i = finish
    while parent[i] != start:
        way.appendleft(parent[i])
        i = parent[i]
    way.appendleft(start)
    return way


# delete last vertex (adjacent to finish node) from the shortest path
def del_last_link(graph, short_path):
    x = short_path.pop()
    y = short_path.pop()
    graph[y][x] = 0


# unpack from json to matrix based format as graph_1 from the beginning
def unpackjs_to_matrix(fname):
    try:
        with open(fname, "r") as f:
            file_dump = f.read()  # открываем как строку
    except:
        print(f'Ошибка открытия файла: {fname}')
        file_dump = ''
        exit(1)

    file_dict = json.loads(file_dump)
    # shorten dict jump to topology contents
    file_dict = dict(file_dict['topology'])
    # print(file_dict)
    graph_to_fill = [[0 for _ in range(len(file_dict) + 1)] for _ in range(len(file_dict) + 1)]
    # fill the graph_to_fill with adjacency information
    for key in file_dict:
        # print(key, file_dict[key])
        for adj_node in file_dict[key]:
            graph_to_fill[int(key)][adj_node] = 1

    return graph_to_fill


# select only one adjacent link from start position
def mask_first_link(graph_2, start, adj_i_pos):
    for i, vertex in enumerate(graph_2[start]):
        if adj_i_pos == i:
            graph_2[start][i] = 1
        else:
            graph_2[start][i] = 0


def main():
    params = sys.argv[1:]
    if params:
        start = int(params[2])
        fin = int(params[3])
        max_length = int(params[1])
        fname = params[0]
    else:
        print("Please specify params, exiting..")
        exit(1)
    # make up the graph matrix from json
    graph_2 = unpackjs_to_matrix(fname)
    # keep copy of original graph by generator expressions as a = b[:][:] wont work
    graph_3 = [[graph_2[y][x] for y in range(len(graph_2))] for x in range(len(graph_2[0]))]
    # we also can use copy.deepcopy(graph_2)

    # for each link adjacent to start node,
    # run bfs several times, to get the shortest path, each time we remove
    # last link of it in graph, so we would get (probably) all possible routes between start and finish nodes
    # paths are ranged from shortest to longest
    # we finish while True if we have not found path or when length became more than
    # specified by max_length parameter

    paths_str = []
    for i, vertex in enumerate(graph_3[start]):
        if vertex != 0:
            # each time we get original graph, and select (mask) adjacent link from start node to the rest of graph
            graph_2 = [[graph_3[y][x] for y in range(len(graph_3))] for x in range(len(graph_3[0]))]
            mask_first_link(graph_2, start, i)

            while True:
                short_path = bfs(graph_2, start, fin)
                if short_path is None:
                    break
                if len(short_path) > max_length:
                    break
                # add and format path
                short_path_str = ' '.join(str(i) for i in short_path)
                paths_str.append(short_path_str)
                # remove last link (adjacent node to finish node) of this path
                # to get other shortest possible path on next iteration
                del_last_link(graph_2, short_path)

    # print found routes results sorted by length
    # because running each time while True cycle produces new set of possible routes of various lengths
    paths_str = list(sorted(paths_str, key=lambda x: len(x)))
    for i in paths_str:
        print(i)


if __name__ == "__main__":
    main()
