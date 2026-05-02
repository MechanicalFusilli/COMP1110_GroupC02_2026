from collections import defaultdict 
import heapq 
import copy

def createnetwork(a, trans, dataset):
    # a refers to the number we will take from the data set for this algorithm
    # 0 = cost, 1 = distance, -1 = segs
    # trans is a list of transportation types that are banned

    data = defaultdict(list)
    edgeid = {}

    it = 0 #a counter to provide each edge with a unique id

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


def djikstras(start, end, time, e, eid):
    if start == end:
        return [time, [[start, 0, 0]]]
    heap = []
    visited = dict()

    heapq.heappush(heap, (time, [[start, 0, 0]]))
    visited[start] = time

    while heap:
        curt, route = heapq.heappop(heap) #current time, list route

        if route[-1][0] == end:
            return [curt, route]
        
        for dest, w, edge_id in e[route[-1][0]]: #destination, weight, edgeid
            newtime = curt + w

            if opt == 1:
                #this part calculates the delay from wait times
                starting = eid[edge_id].start_time
                ending = eid[edge_id].end_time
                interval = eid[edge_id].wait_time
                if (starting > (curt%1440)): newtime += starting - (curt%1440)
                if (ending < (curt%1440)): newtime += starting + 1440 - (curt%1440)
                if (starting < (curt%1440) < ending) and (((curt%1440) - starting)%interval)!= 0: 
                    newtime += interval - ((curt%1440) - starting)%interval

            if dest not in visited or newtime < visited[dest]:
                visited[dest] = newtime
                heapq.heappush(heap, (newtime, route + [[dest, newtime - curt, edge_id]]))
                
    return [-1, ["No Route"]]


def yens(start, end, time, e, eid, opt):
    paths = []  
    paths.append(djikstras(start, end, time, e, eid, opt))
    if paths[-1][0] == -1:
        return -1
    potential = []
    for i in range(1, 3):
        for j in range(len(paths[-1][1]) - 1):
            spur = paths[-1][1][j][0]
            root = paths[-1][1][:j + 1]
            newe = copy.deepcopy(e)

            rootw = time + sum(step[1] for step in root) #rootweight

            # remove instances of previous paths
            for dist, path in paths:
                if path[:j+1] == root and len(path) > j + 1:
                    start_a = path[j][0]
                    end_id = path[j+1][2]
                    newe[start_a] = [edge for edge in newe[start_a] if end_id != edge[2]]

            w, r = djikstras(spur, end, rootw, newe, eid, opt)

            if w == -1:
                continue

            heapq.heappush(potential, [w, root + r[1:]])

        if potential:
            dist, new_path = heapq.heappop(potential)
            paths.append([dist, new_path])
        else:
            break

    return paths


def startfind(start, end, time, option, transtype, adjlist):
    # start and end refer to destination
    # time refers to the time of departure  
    # option is customization
    # transtype is list of banned transportation
    # adjlist is the adjacency list

    network, edgeid = createnetwork(option, transtype, adjlist)
    routes = yens(start, end, time, network, edgeid, option)

    return routes, edgeid
