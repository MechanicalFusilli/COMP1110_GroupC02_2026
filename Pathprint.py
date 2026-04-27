def print_path(routes):
    if routes == -1:
        print("No route found.")
        return

    print("\n=== ROUTES ===\n")

    for i, route in enumerate(routes, 1):
        total, path = route

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
            mode = path[j][1]
            distance = path[j][3]
            cost = path[j][4]

            total_distance += distance
            total_cost += cost

            print(f"{previous_city} -> {current_city}")
            print(f"Mode of Transport: {mode}")
            print(f"Distance: {distance}")
            print(f"Cost: {cost}")
            print("-" * 20)

        print(f"Total Distance: {total_distance}")
        print(f"Total Cost: {total_cost}")
        print(f"Optimised Total: {total}")
        print()