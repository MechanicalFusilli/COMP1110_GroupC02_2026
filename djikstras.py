from collections import defaultdict
import heapq
import copy

INT_MAX = float("inf")

def createnetwork(a, trans, dataset):
    data = defaultdict(list)
    # a refers to the number we will take from the data set for this algorithm
    # 0 = cost, 1 = distance, -1 = segs
    # trans is a list of transportation types that are banned

    for i in dataset:
        for j in dataset[i]:
            if j.mode in trans:
                continue

            if a == 0:
                weight = j.cost
            elif a == 1:
                weight = j.distance
            else:
                weight = 1

            data[i].append([j.end, weight, j.mode, j.distance, j.cost])

    return data


def djikstras(start, end, e):
    if start == end:
        return [0, [[start, None, 0, 0, 0]]]

    heap = []
    visited = dict()

    heapq.heappush(heap, (0, [[start, None, 0, 0, 0]]))
    visited[start] = 0

    while heap:
        dist, route = heapq.heappop(heap)
        current = route[-1][0]

        if current == end:
            return [dist, route]

        for dest, w, mode, distance, cost in e[current]:
            newdist = dist + w

            if dest not in visited or newdist < visited[dest]:
                visited[dest] = newdist

                new_step = [dest, mode, w, distance, cost]
                heapq.heappush(heap, (newdist, route + [new_step]))

    return [-1, ["No Route"]]


def yens(start, end, e):
    paths = []
    paths.append(djikstras(start, end, e))

    if paths[-1][0] == -1:
        return -1

    for i in range(1, 3):
        potential = []

        for j in range(len(paths[-1][1]) - 1):
            spur = paths[-1][1][j][0]
            root = paths[-1][1][:j + 1]
            newe = copy.deepcopy(e)

            rootw = sum(step[2] for step in root)

            # remove instances of previous paths
            for dist, path in paths:
                if path[:j + 1] == root and len(path) > j + 1:
                    start_a = path[j][0]
                    end_b = path[j + 1][0]
                    end_w = path[j + 1][2]

                    removed = False
                    temp = []

                    for edge in newe[start_a]:
                        if edge[0] == end_b and edge[1] == end_w and not removed:
                            removed = True
                        else:
                            temp.append(edge)

                    newe[start_a] = temp

            # remove root nodes
            for step in root[:-1]:
                node = step[0]
                newe[node] = []

            w, r = djikstras(spur, end, newe)

            if w == -1:
                continue

            heapq.heappush(potential, [w + rootw, root[:-1] + r])

        if potential:
            dist, new_path = heapq.heappop(potential)
            paths.append([dist, new_path])
        else:
            break

    return paths


def startfind(start, end, option, transtype, adjlist):
    # start and end refer to destination
    # option is customization
    # transtype is list of banned transportation
    # adjlist is the adjacency list
    return yens(start, end, createnetwork(option, transtype, adjlist))