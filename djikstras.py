from collections import defaultdict 
import heapq 
import copy

def createnetwork(a, trans, dataset):
    #a refers to the number we will take from the data set for this algorithm (0 = cost, 1 = distance, -1 = segs)
    #trans is a list of transportation types that are banned

    data = defaultdict(list)
    edgeid = defaultdict(list)


    it = 0
    if a == 0:

        for i in dataset:
            for j in dataset[i]:
                if j.mode in trans:
                    continue
                it += 1
                data[i].append([j.end, j.cost, it])
                edgeid[it] = j
    
    elif a == 1:
        for i in dataset:
            for j in dataset[i]:
                if j.mode in trans:
                    continue
                it += 1
                data[i].append([j.end, j.distance, it])
                edgeid[it] = j
    else:
        for i in dataset:
            for j in dataset[i]:
                if j.mode in trans:
                    continue
                it += 1
                data[i].append([j.end, 1, it])
                edgeid[it] = j
    return data, edgeid


def djikstras(start, end, e):
    if start == end:
        return [0, [start]]
    heap = []
    visited = dict()

    heapq.heappush(heap, (0, [[start, 0, 0]]))
    visited[start] = 0

    while heap:
        dist, route = heapq.heappop(heap)
        if route[-1][0] == end:
            return [dist, route]
        
        for dest, w, id in e[route[-1][0]]:
            newdist = dist + w
            if dest not in visited or newdist < visited[dest]:
                visited[dest] = newdist
                heapq.heappush(heap, (newdist, route + [[dest, w, id]]))
                
    return [-1, ["No Route"]]

def yens(start, end, e, eid):
    paths = []  
    paths.append(djikstras(start, end, e))
    if paths[-1][0] == -1:
        return -1

    for i in range(1,3):
        potential = []
        for j in range(len(paths[-1][1])-1):
            spur = paths[-1][1][j][0]
            root = paths[-1][1][:j+1]
            newe = copy.deepcopy(e)

            rootw = sum(w for _, w, _ in root)

            #remove instances of previous paths
            for dist, path in paths:
                if path[:j+1] == root and len(path) > j + 1:
                    start_a = path[j][0]
                    end_b = path[j+1][0]
                    end_w = path[j+1][1]

                    removed = False
                    temp = []
                    for edge in newe[start_a]:
                        if edge[0] == end_b and edge[1] == end_w and (not removed):
                            removed = True
                        else:
                            temp.append(edge)
                    newe[start_a] = temp

            #remove root nodes
            for node, _ in root[:-1]:
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
    #start and end refer to destination
    #option is customization
    #transtype is list of banned transportation
    #adjlist is the adjacency list
    #verlist is the vertex list

    network, edgeid = createnetwork(option, transtype, adjlist)
    return yens(start, end, network, edgeid)

start, end = input().split()
adjlist = defaultdict(list)
eid = defaultdict(list)

n, m = input().split()
for i in range(int(n)):
    a = input()
    adjlist[a] = []


it = 0
for i in range(int(m)):
    a, b, c = input().split()
    w = int(c)
    it += 1
    adjlist[a].append([b, w, it])
    it += 1
    adjlist[b].append([a, w, it])

paths = yens(start, end, adjlist, eid)
if paths == -1:
    print("No Routes")
for n, i in enumerate(paths):
    print(f"Route {n + 1}: {i[0]}")
    for j, k, l in i[1]:
        print(f"{j}: {k}, {l};   ", end = "")
    print()

