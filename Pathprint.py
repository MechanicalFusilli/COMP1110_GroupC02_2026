def print_path(result, time):
    routes, edgeid = result

    if routes == -1:
        print("No route found.")
        return

    print("\n=== ROUTES ===\n")

    for i, route in enumerate(routes, 1):
        path = route[1]

        print(f"Route {i}:")

        city_names = []
        total_distance = time
        total_cost = 0
        distancelist = []

        for step in path:
            city_names.append(step[0])

        # Calculate totals first
        for j in range(1, len(path)):
            edge_id = path[j][2]
            segment = edgeid[edge_id]
            #wait time calculation
            stime = segment.start_time
            etime = segment.end_time
            ival = segment.wait_time
            rtime = total_distance%1440
            if (rtime < stime): wtime = stime - rtime
            if (etime < rtime): wtime = stime + 1440 - rtime
            if (stime < rtime < etime): wtime = ival - ((rtime - stime)%ival)

            total_distance += segment.distance + wtime
            distancelist.append(segment.distance + wtime)
            total_cost += segment.cost

        print("Cities:")
        print(" -> ".join(city_names))

        # 🔥 totals now here
        print(f"\nTime of Arrival: {(total_distance%1440)//60}:{(total_distance%1440)%60:02d} ({total_distance//1440} Days Elapsed)")
        print(f"Time Required: {total_distance - time} mins")
        print(f"Total Cost: ${total_cost}")

        print("\nDetails:")

        for j in range(1, len(path)):
            previous_city = path[j - 1][0]
            current_city = path[j][0]
            edge_id = path[j][2]

            segment = edgeid[edge_id]

            print(f"{previous_city} -> {current_city}")
            print(f"Mode of Transport: {segment.mode}")
            print(f"Time Required: {distancelist[j-1]} mins")
            print(f"Cost: ${segment.cost}")
            print(f"Wait Time: {distancelist[j-1] - segment.distance} mins")
            print(f"Transport Time: {segment.distance} mins")
            print("-" * 20)

        print()
