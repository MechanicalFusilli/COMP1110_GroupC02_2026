from collections import defaultdict 
import heapq 
import copy

def createnetwork(a, trans, dataset):
    # a refers to the number we will take from the data set for this algorithm
    # 0 = cost, 1 = distance, -1 = segs
    # trans is a list of transportation types that are banned

    data = defaultdict(list)
    edgeid = {}

    it = 0

    for i in dataset:
        for j in dataset[i]:
            if j.mode in trans:
                continue

            it += 1

            if a == 0:
                weight = j.cost
            elif a == 1:
                weight = j.distance
            else:
                weight = 1

            # smaller data set for dijkstra
            # format: [destination, weight, edge id]
            data[i].append([j.end, weight, it])

            # full data stored here
            edgeid[it] = j

    return data, edgeid


def djikstras(start, end, e):
    if start == end:
        return [0, [[start, 0, 0]]]
    heap = []
    visited = dict()

    heapq.heappush(heap, (0, [[start, 0, 0]]))
    visited[start] = 0

    while heap:
        dist, route = heapq.heappop(heap)

        if route[-1][0] == end:
            return [dist, route]
        
        for dest, w, edge_id in e[route[-1][0]]:
            newdist = dist + w
            if dest not in visited or newdist < visited[dest]:
                visited[dest] = newdist
                heapq.heappush(heap, (newdist, route + [[dest, w, edge_id]]))
                
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

            rootw = sum(step[1] for step in root)

            # remove instances of previous paths
            for dist, path in paths:
                if path[:j+1] == root and len(path) > j + 1:
                    start_a = path[j][0]
                    end_b = path[j+1][0]
                    end_w = path[j+1][1]
                    end_id = path[j+1][2]

                    removed = False
                    temp = []
                    for edge in newe[start_a]:
                        if edge[0] == end_b and edge[1] == end_w and edge[2] == end_id and not removed:
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

    network, edgeid = createnetwork(option, transtype, adjlist)
    routes = yens(start, end, network)

    return routes, edgeid