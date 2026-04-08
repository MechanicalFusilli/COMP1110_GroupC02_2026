from collections import defaultdict 
import heapq 
import sys
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

def createnetwork(a, b, c, dataset):
    data = defaultdict(list)
    #a refers to the number we will take from the data set for this algorithm (0 = cost, 1 = distance, 2 = some arbitrary value)
    #if a = -1, then interger b will overwrite the weights of all paths, which is useful for testing stops/segments
    #c is a list of transportation types that are banned. IT IS NOT IMPLEMENTED YET
    #createnetwork(0, 0) will optimize by cost
    #createnetwork(1, 0) will optimize by distance
    #createnetwork(-1, 1) will optimize by stop/segments
    if a != -1:
        for i in dataset:
            for j in dataset[i]:
                data[i].append([j[0], j[a+1]])
    else:
        for i in dataset:
            for j in dataset[i]:
                data[i].append([j[0], b])
    return data

def djikstras(start, end, e, v):
    if start == end:
        return [0, [start]]
    
    heap = []
    visited = dict()
    for i in v:
        visited[i] = INT_MAX

    heapq.heappush(heap, (0, [start]))
    while heap:
        dist, route = heapq.heappop(heap)
        if route[-1] == end:
            return [dist, route]
        
        for dest,w in e[route[-1]]:
            if dest not in visited:
                visited[dest] = INT_MAX #(Vertex Guard)
            if (dist + w) < visited[dest]:
                visited[dest] = dist + w
                heapq.heappush(heap, (visited[dest], route + [dest]))
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
                    v = path[j+1]
                    newe[u] = [edge for edge in newe[u] if edge[0] != v]
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

def pathprint(routes):
    #quick access function for displaying output
    if routes == -1:
        print("No routes possible")
        return
    for numb,i in enumerate(routes):
        dist, path = i
        print(F"Route {numb}: {dist} meters")
        for k in range(len(path)):
            print(path[k], end = "")
            if k == len(path) - 1:
                continue
            print(" -> ", end = "")
        print("")


start, end, na, nb = input().split()
na = int(na)
nb = int(nb)
adjlist, verlist = takedata()
routes = yens(start, end, createnetwork(na, nb, [], adjlist), verlist)
pathprint(routes)
#!BIG NOTE! with this new implementation, u need to input the route to test first before adding the network data.
#ex:
# A B 0 1 -> route you want to test, options
# 2 2 -> number of v and e
# A -> vertex 1 name
# B -> vertex 2 name
# A B 2 4-> edge 1 (start, end, cost, distance)
# B A 2 3-> edge 2 (start, end, cost, distance)
