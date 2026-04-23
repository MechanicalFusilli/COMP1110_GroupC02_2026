def print_path(routes):
    if routes == -1:
        print("No route found.")
        return

    print("\n=== ROUTES ===\n")

    for i, route in enumerate(routes, 1):
        total, path = route
        print(f"Route {i}:")
        print(" -> ".join(path))
        print(f"Total: {total}")
        print()