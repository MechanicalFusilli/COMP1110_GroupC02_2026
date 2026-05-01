def print_path(result):
    routes, edgeid = result

    if routes == -1:
        print("No route found.")
        return

    print("\n=== ROUTES ===\n")

    for i, route in enumerate(routes, 1):
        path = route[1]

        print(f"Route {i}:")

        city_names = []
        total_distance = 0
        total_cost = 0
        total_wait_time = 0

        for step in path:
            city_names.append(step[0])

        # Calculate totals first
        for j in range(1, len(path)):
            edge_id = path[j][2]
            segment = edgeid[edge_id]

            total_distance += segment.distance
            total_cost += segment.cost
            total_wait_time += segment.wait_time

        print("Cities:")
        print(" -> ".join(city_names))

        # 🔥 totals now here
        print(f"\nTime Required: {total_distance} mins")
        print(f"Total Cost: ${total_cost}")
        print(f"Maximum Wait Time: {total_wait_time} mins")

        print("\nDetails:")

        for j in range(1, len(path)):
            previous_city = path[j - 1][0]
            current_city = path[j][0]
            edge_id = path[j][2]

            segment = edgeid[edge_id]

            print(f"{previous_city} -> {current_city}")
            print(f"Mode of Transport: {segment.mode}")
            print(f"Time Required: {segment.distance} mins")
            print(f"Cost: ${segment.cost}")
            print(f"Wait Time: {segment.wait_time} mins")
            print("-" * 20)

        print()
