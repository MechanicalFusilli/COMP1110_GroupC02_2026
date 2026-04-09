# Completely removed Node
# Adjusted Seg to fit input specification from Carl
# Currently reworking load_network, moved to network_system

class Seg:
    def __init__(self, start, end, mode, time, cost):
        self.start = start
        self.end = end
        self.mode = mode
        self.time = time
        self.cost = cost