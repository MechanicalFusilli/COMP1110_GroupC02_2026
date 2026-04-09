# This is where data is stored
# I have not tested the network validation stuff yet
# For network loading validation: TODO: exception handling
import os
from db import Seg

def main():
    network_system = NetworkSystem.load_network()
    if network_system == None:
        print("Failed to load network")
        return

class NetworkSystem:
    def __init__(self, vertices : list, transport_modes : list, segments : list):
        
        # These two are lists of strings
        self.vertices = vertices
        self.transport_modes = transport_modes
        
        # List of Seg
        self.segments = segments

        # Settings set to default
        # Inspired by Ezekiel's implementation but it needs to fit Carl's djikstra
        # I will do functionality related to settings later
        self.settings = {
            "priority": 0,
            "avoid_modes" : [],
        }

        # Testing
        print(self.vertices)
        print(self.transport_modes)
        print(len(self.segments))

    # Loads network from file, to call: NetworkSystem.load_network(insert filename)
    # Validates the file formatting
    # Returns a NetworkSystem object
    @classmethod
    def load_network(cls, filename="network.txt"):

        delimiter = ', '

        try:
            # Reads filename in current directory
            with open(os.path.join(os.path.dirname(__file__), filename), "r") as file:
                contents = file.readlines()
            
            # Contents empty
            if not contents:
                return # Throw Exception or something later
            
            first_line = contents[0].strip().split(delimiter)

            # First line invalid
            if not cls.validate_first_line(first_line):
                return # Throw Exception
            
            vertices_count, transport_count, path_count = map(int, first_line)

            # Remaining lines are insufficient
            if (len(contents) -1) < (vertices_count + transport_count + path_count):
                return #Throw Exception
            
            # Get sublists
            vertices = [l.strip() for l in contents[1 : vertices_count+1]]
            transport_modes = [l.strip() for l in contents[vertices_count+1 : transport_count+vertices_count+1]]

            # Delimiters in vertices list
            if not cls.validate_list(vertices, delimiter):
                return # Throw Exception
            
            # Delimiters in transport modes list
            if not cls.validate_list(transport_modes, delimiter):
                return # Throw Exception
            
            segments = []
            remaining_lines = contents[transport_count+vertices_count+1:]

            # Loop through remaining lines
            subpaths = 0
            bidirectional = 0
            start = dest = ""
            for line in remaining_lines:
                line = line.strip().split(delimiter)
                # If main path
                if not subpaths:
                    
                    # Invalid path line
                    if not cls.validate_path_line(line, vertices):
                        return # Throw Exception
                    
                    start, dest, bidirectional, subpaths = line
                    bidirectional, subpaths = int(bidirectional), int(subpaths)

                # If subpath
                else:

                    # Invalid subpath line
                    if not cls.validate_subpath_line(line, transport_modes):
                        return # Throw Exception
                    
                    new_Seg = Seg(start, dest, line[0], line[1], line[2])
                    segments.append(new_Seg)

                    if bidirectional:
                        new_Seg = Seg(dest, start, line[0], line[1], line[2])
                        segments.append(new_Seg)

                    subpaths -= 1
            
            # Inaccurate number of subpaths
            if subpaths > 0:
                return # Throw exception
            
            return cls(vertices, transport_modes, segments)
        
        # Exceptions
        except FileNotFoundError:
            print("file not found")
        except Exception as e:
            print(e)
    
    
    # For all these validation methods I am assuming a list of strings
    # Because file contents are strings

    @staticmethod
    def validate_first_line(line : list):

        # Not 3 items
        if len(line) != 3:
            return False
        
        # Not integers
        if not all([x.isdecimal() for x in line]):
            return False
        
        # Nonpositives not allowed
        if not all([int(x) > 0 for x in line]):
            return False

        return True
    
    # For nodes or transport modes
    @staticmethod
    def validate_list(lst: list, delimiter : str):
        
        # Delimiter in any line
        if not all([delimiter not in x for x in lst]):
            return False
        
        # Any line is empty
        if not all([x.strip() for x in lst]):
            return False
        
        return True

    @staticmethod
    def validate_path_line(line: list, vertices: list):

        # Not 4 items
        if len(line) != 4:
            return False
        
        # First two parts aren't vertices
        if not (line[0] in vertices or line[1] in vertices):
            return False

        # Last two parts aren't integers
        if not (line[2].isdecimal() and line[3].isdecimal()):
            return False
        
        # Bidirectional parameters out of range
        if int(line[2]) not in [0, 1]:
            return False
        
        # Nonpositive subpaths
        if not int(line[3]) > 0:
            return False
        
        return True

    @staticmethod
    def validate_subpath_line(line: list, transport_modes: list):
        
        # Not 3 items
        if len(line) != 3:
            return False
        
        # First item not in transport modes
        if line[0] not in transport_modes:
            return False
        
        # Last two parts aren't integers
        if not (line[1].isdecimal() and line[2].isdecimal()):
            return False

        # Negative cost/distance (zero is allowed here)
        if int(line[1]) < 0 or int(line[2]) < 0:
            return False
        
        return True

if __name__ == "__main__":
    main()