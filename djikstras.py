from collections import defaultdict 
import heapq 
import sys
import copy

INT_MAX = sys.maxsize  
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
        a, b, c = input().split()
        c = int(c)
        e[a].append([b,c])
        e[b].append([a,c]) #i decided to make roads two-way, but if we want to change that just remove this 
    return e

def createnetwork():
    #this is where we can start culling roads and paths based on the customization options. 
    #ideally, takedata() would return a messy set of data, which createnetwork would clean up, removing all unnecessay things
    #ex: {a: {b: {3, 5, ["MTR"]}}}
    #point a has a route to point b. it takes 3 minutes to get there for a cost of 5. the mode of transportation is mtr.
    #if we wanted to remove all mtr routes, then this function would first unpack the entire data set, then cull all routes with the term "mtr"
    return takedata()

def routetest(start, end, e):
#route test takes a bfs approach to explore and see if there is a connection between start and end
    citlist = dict()
    for point in e:
        citlist[point] = 1
    citlist[start] = 0
    heap = []
    heapq.heappush(heap, start)
    while heap:
        city = heapq.heappop(heap)
        for dest, w in e[city]:
            if dest == end:
                return True
            if citlist[dest] == 0:
                continue
            else:
                citlist[dest] = 0
                heapq.heappush(heap, dest)
    else:
        return False

def djikstras(start, end, e):
    if start == end:
        return [0, [start]]
    if (not routetest(start, end, e)):
        return [INT_MAX, ["No Route"]]
    heap = []
    heapq.heappush(heap, (0, [start]))
    while heap:
        dist, route = heapq.heappop(heap)
        if route[-1] == end:
            return [dist, route]
        for dest,w in e[route[-1]]:
            newroute = list(route)
            newroute.append(dest)
            heapq.heappush(heap, (w + dist, newroute))

def yens(start, end ,e):
    paths = []  
    #paths is a list of lists. Each list it contains follows the format [Distance Number, [Sequential Route Order]]
    paths.append(djikstras(start, end ,e))
    if paths[-1][1][0] == "No Route":
        return -1
    for i in range(1,3):
        potential = []
        for j in range(len(paths[-1][1])-1):
            spur = paths[-1][1][j]
            root = paths[-1][1][:j+1]
            newe = copy.deepcopy(e)

            rootw, _ = djikstras(start, spur, e)

            #remove instances of previous paths
            for dist, path in paths:
                if path[:j+1] == root and len(path) > j + 1:
                    u = path[j]
                    v = path[j+1]
                    newe[u] = [edge for edge in newe[u] if edge[0] != v]
            #remove root nodes
            for node in root[:-1]:
                newe[node] = []

            w, r = djikstras(spur, end, newe)
            if r[0] == "No Route":
                continue
            path = root[:-1] + r
            heapq.heappush(potential, [w + rootw, path])
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


start, end = input().split()
routes = yens(start, end, createnetwork())
pathprint(routes)
#!BIG NOTE! with this new implementation, u need to input the route to test first before adding the network data.
#ex:
# A B -> route you want to test
# 2 2 -> number of v and e
# A -> vertex 1 name
# B -> vertex 2 name
# A B 2 -> edge 1
# B A 2 -> edge 2

#no visited notes or dictionary set, may need to add for optimization. this can also be used to remove redundancy of routetest
