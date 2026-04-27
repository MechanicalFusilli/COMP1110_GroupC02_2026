def print_path(result):
    routes, edgeid = result

    if routes == -1:
        print("No route found.")
        return

    print("\n=== ROUTES ===\n")

    for i, route in enumerate(routes, 1):
        total_weight = route[0]
        path = route[1]

        print(f"Route {i}:")

        city_names = []
        total_distance = 0
        total_cost = 0

        for step in path:
            city_names.append(step[0])

        print("Cities:")
        print(" -> ".join(city_names))

        print("\nDetails:")

        for j in range(1, len(path)):
            previous_city = path[j - 1][0]
            current_city = path[j][0]
            weight = path[j][1]
            edge_id = path[j][2]

            segment = edgeid[edge_id]

            total_distance += segment.distance
            total_cost += segment.cost

            print(f"{previous_city} -> {current_city}")
            print(f"Mode of Transport: {segment.mode}")
            print(f"Distance: {segment.distance}")
            print(f"Cost: {segment.cost}")
            print(f"Weight Used: {weight}")
            print("-" * 20)

        print(f"Total Distance: {total_distance}")
        print(f"Total Cost: {total_cost}")
        print(f"Optimised Total: {total_weight}")
        print()