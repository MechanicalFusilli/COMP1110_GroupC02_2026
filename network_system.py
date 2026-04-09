# This is where data is stored
import os
from db import Seg

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

    # Loads network from file, to call: NetworkSystem.load_network(insert filename)
    # Validates the file formatting
    # Returns a NetworkSystem object
    @classmethod
    def load_network(cls, filename="network.txt"):
        try:
            # Reads filename in current directory
            with open(os.path.join(os.path.dirname(__file__), filename), "r") as file:
                contents = file.readlines().strip()
            
            # Contents empty
            if not contents:
                return # Throw an exception or something later
            
            first_line = contents[0]

            # First line invalid
            if not cls.validate_first_line(first_line):
                return # Exception
            
            # TODO: Continue to validate other lines
        
        # Exceptions
        except FileNotFoundError:
            print("file not found")
        except Exception as e:
            print(e)
    
    @staticmethod
    def validate_first_line(line : str):
        line = line.split()

        # Not 3 items
        if len(line) != 3:
            return False
        
        # Not integers
        if not all([x.isdecimal() for x in line]):
            return False
        
        return True