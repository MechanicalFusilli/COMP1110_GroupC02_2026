def print_path(routes):
    if routes == -1:
        print("No route found.")
        return

    print("\n=== ROUTES ===\n")

    for i, route in enumerate(routes, 1):
        total, path = route

        print(f"Route {i}:")

        city_names = []

        for step in path:
            if isinstance(step, list):
                city_names.append(step[0])
            else:
                city_names.append(step)

        print(" -> ".join(city_names))
        print(f"Total: {total}")
        print()
