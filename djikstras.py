from collections import defaultdict 
import heapq 
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
    route = set()
    if (not routetest(start, end, e)):
        return ["No possible routes"]
    heap = []
    heapq.heappush(heap, (0, start))
    while heap:
        dist, point = heapq.heappop(heap)
        if point == end:
            route.add(dist)
            break
            #note: if there isn't any possible route, this implementation will loop forever. will fix in the future by running bfs to check if its possible first
        for dest,w in e[point]:
            heapq.heappush(heap, (w + dist, dest))
    return route

start, end = input().split()
routes = djikstras(start, end, createnetwork())
for i in routes:
    print(i)
#!BIG NOTE! with this new implementation, u need to input the route to test first before adding the network data.
#ex:
# A B -> route you want to test
# 2 2 -> number of v and e
# A -> vertex 1 name
# B -> vertex 2 name
# A B 2 -> edge 1
# B A 2 -> edge 2

#might have to implement yens algo in the future for 3 routes or a distance dict instead
