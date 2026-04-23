from collections import defaultdict 
import heapq 
import copy

INT_MAX = float("inf")
#default dict provides an adjacency list implementation, which stores edges and their weights
#heapq provides a min-heap implementation, which is used as a priority queue that accesses elements in O(1)

def takedata():
    #this part is subject to change, but for now it takes in data based upon the format in the whatsapp group
    n, m = map(int, input().split())
    v = list()
    e = defaultdict(list)
    for i in range(n):
        v.append(input())
    for i in range(m):
        a, b, c, d = input().split()
        c = int(c)
        d = int(d)
        e[a].append([b,c,d])
        e[b].append([a,c,d]) #i decided to make roads two-way, but if we want to change that just remove this 
    return e, v

def createnetwork(a, trans, dataset):
    data = defaultdict(list)
    #a refers to the number we will take from the data set for this algorithm (0 = cost, 1 = distance, -1 = segs)
    #trans is a list of transportation types that are banned
    #use segments
    if a == 0:
        for i in dataset:
            for j in dataset[i]:
                if j.mode in trans:
                    continue
                data[i].append([j.end, j.cost])
    
    elif a == 1:
        for i in dataset:
            for j in dataset[i]:
                if j.mode in trans:
                    continue
                data[i].append([j.end, j.distance])
    else:
        for i in dataset:
            for j in dataset[i]:
                if j.mode in trans:
                    continue
                data[i].append([j.end, 1])
    return data

def djikstras(start, end, e, v):
    if start == end:
        return [0, [start]]
    
    heap = []
    visited = dict()

    heapq.heappush(heap, (0, [start]))
    visited[start] = 0

    while heap:
        dist, route = heapq.heappop(heap)
        if route[-1] == end:
            return [dist, route]
        
        for dest, w in e[route[-1]]:
            newdist = dist + w
            if dest not in visited or newdist < visited[dest]:
                visited[dest] = newdist
                heapq.heappush(heap, (newdist, route + [dest]))

    return [INT_MAX, ["No Route"]]

def yens(start, end, e, v):
    paths = []  
    paths.append(djikstras(start, end ,e, v))
    if paths[-1][1][0] == "No Route":
        return -1
     #paths is a list of lists. Each list it contains follows the format [Distance Number, [Sequential Route Order]]

    for i in range(1,3): #maybe we can make it more adaptable to show k amount of paths by changing 3 here
        potential = []
        for j in range(len(paths[-1][1])-1):
            spur = paths[-1][1][j]
            root = paths[-1][1][:j+1]
            newe = copy.deepcopy(e)

            rootw, _ = djikstras(start, spur, e, v)

            #remove instances of previous paths
            for dist, path in paths:
                if path[:j+1] == root and len(path) > j + 1:
                    u = path[j]
                    nextv = path[j+1]
                    newe[u] = [edge for edge in newe[u] if edge[0] != nextv]

            #remove root nodes
            for node in root[:-1]:
                newe[node] = []

            w, r = djikstras(spur, end, newe, v)
            if r[0] == "No Route":
                continue

            heapq.heappush(potential, [w + rootw, root[:-1] + r])

        if potential:
            dist, new_path = heapq.heappop(potential)
            paths.append([dist, new_path])
        else:
            break
    return paths

def startfind(start, end, option, transtype, adjlist, verlist):
    #start and end refer to destination
    #option is customization
    #transtype is list of banned transportation
    #adjlist is the adjacency list
    #verlist is the vertex list
    return yens(start, end, createnetwork(option, transtype, adjlist), verlist)