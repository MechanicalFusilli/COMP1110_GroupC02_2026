import os

class Node:
    def __init__(self, name):
        self.name = name


class Seg:
    def __init__(self, id, start, end, mode, modespec, time):
        self.id = id
        self.start = start
        self.end = end
        self.mode = mode
        self.modespec = modespec
        self.time = time

def load_network():
    nodes = []
    segs = []
    try:
        with open(os.path.join(os.path.dirname(__file__), "network.txt"), "r") as f:
            lines = f.readlines()
            rm = 0
            id = 0
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                if line == "N":
                    rm = 1
                elif line == "S":
                    rm = 2
                elif rm == 1:
                    node = Node(line)
                    nodes.append(node)
                elif rm == 2:
                    seg_info = line.split()
                    seg = Seg(id, seg_info[0], seg_info[1], seg_info[2], seg_info[3], int(seg_info[4]))
                    segs.append(seg)
                    id += 1
    except FileNotFoundError:
        print("file not found")
    except Exception as e:
        print(e)
    return nodes, segs
