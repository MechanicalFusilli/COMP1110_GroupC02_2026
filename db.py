# Completely removed Node
# Adjusted Seg to fit input specification from Carl
# Currently reworking load_network, moved to network_system


class Seg:
    def __init__(self, start, end, mode, distance, cost, wait_time):
        self.start = start
        self.end = end
        self.mode = mode
        self.distance = distance
        self.cost = cost
        self.wait_time = wait_time
