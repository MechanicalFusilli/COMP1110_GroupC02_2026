import heapq

def print_path(network_system, start, end):
    graph = network_system.adjacency_list
    settings = network_system.route_settings
    avoid = network_system.avoid_modes

    # build graph depending on settings
    def get_weight(seg):
        if settings == 0:  # cheapest
            return getattr(seg, "cost", 1)
        elif settings == 1:  # fastest
            return getattr(seg, "time", getattr(seg, "distance", 1))
        else:  # fewest segments
            return 1

    # dijkstra
    pq = [(0, start, [])]  # (cost, current, path)
    visited = set()

    while pq:
        cost, node, path = heapq.heappop(pq)

        if node in visited:
            continue
        visited.add(node)

        if node == end:
            final_path = path
            break

        for seg in graph.get(node, []):
            if hasattr(seg, "mode") and seg.mode in avoid:
                continue

            nxt = seg.to_stop
            weight = get_weight(seg)

            heapq.heappush(pq, (cost + weight, nxt, path + [(node, nxt, seg)]))
    else:
        print(f"No route found between {start} and {end}.")
        return

    # print nicely
    print("\n=== ROUTE ===\n")
    print(f"{start} → {end}\n")

    total = 0

    for i, (a, b, seg) in enumerate(final_path, 1):
        mode = getattr(seg, "mode", "N/A")
        time = getattr(seg, "time", getattr(seg, "distance", "-"))

        print(f"{i}. {a} → {b} ({mode}, {time})")

        total += get_weight(seg)

    print("\n----------------")

    if settings == 0:
        print(f"Total cost: {total}")
    elif settings == 1:
        print(f"Total time: {total}")
    else:
        print(f"Total segments: {len(final_path)}")

    print()
