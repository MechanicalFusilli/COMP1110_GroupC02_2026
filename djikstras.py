from collections import defaultdict 
import heapq 
import copy

INT_MAX = float("inf")

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


def djikstras(start, end, e):
    if start == end:
        return [0, [start]]
    heap = []
    visited = dict()

    heapq.heappush(heap, (0, [[start, 0]]))
    visited[start] = 0

    while heap:
        dist, route = heapq.heappop(heap)
        if route[-1][0] == end:
            return [dist, route]
        
        for dest, w in e[route[-1][0]]:
            newdist = dist + w
            if dest not in visited or newdist < visited[dest]:
                visited[dest] = newdist
                heapq.heappush(heap, (newdist, route + [[dest, w]]))
                
    return [-1, ["No Route"]]

def yens(start, end, e):
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

            rootw = sum(w for _, w in root)

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
    return yens(start, end, createnetwork(option, transtype, adjlist))
