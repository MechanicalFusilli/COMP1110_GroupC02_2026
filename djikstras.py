from collections import defaultdict 
#easy adjacency list implementation for edges
import heapq 
#min-heap is used as a priority queue for this implementation of Djikstra's    

#taking in the network first, v = vertex, e = edges
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


#place in route
start, end = input().split()
heap = []
heapq.heappush(heap, (0, start))
while heap:
    dist, point = heapq.heappop(heap)
    if point == end:
        print(dist)
        break
        #note: if there isn't any possible route, this implementation will loop forever. will fix in the future by running bfs to check if its possible first
    for dest,w in e[point]:
        heapq.heappush(heap, (w + dist, dest))
