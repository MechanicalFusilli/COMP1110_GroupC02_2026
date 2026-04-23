# This is where data on the network and settings is stored
import os
from db import Seg
from djikstras import startfind

class NetworkLoadError(Exception):
    pass

class NetworkFormatError(NetworkLoadError):
    pass

class NetworkValidationError(NetworkLoadError):
    pass

def main():
    try:
        network_system = NetworkSystem.load_network()
        print("Adjacnecy list")
        print(network_system.output_adjacency_list())
        startfind("hku", "mgk", 1, [], network_system.adjacency_list, network_system.vertices)
    except NetworkLoadError as e:
        print(f"Failed to load network: {e}")


class NetworkSystem:
    def __init__(self, vertices: list, transport_modes: list, segments: list):
        # These two are lists of strings
        self.vertices = vertices
        self.transport_modes = transport_modes

        # List of Seg
        self.segments = segments

        # Settings set to default
        self.settings = {
            "preference": 0,
            "avoid_modes": [],
            "start": None,
            "end": None,
        }

        # This makes self.adjacency_list
        self.make_adjacency_list()

    def make_adjacency_list(self):
        self.adjacency_list = dict()

        for segment in self.segments:
            # Create list at key if it doesn't exist
            if self.adjacency_list.get(segment.start) is None:
                self.adjacency_list[segment.start] = []

            self.adjacency_list[segment.start].append(segment)

    # Debugging function to output the adjacency list contents
    def output_adjacency_list(self):
        for start, seglist in self.adjacency_list.items():
            print("=" * 20)
            print(f"Paths from {start}:")
            print("-" * 20)
            for segment in seglist:
                print(f"End: {segment.end}")
                print(f"Mode of Transport: {segment.mode}")
                print(f"Distance: {segment.distance}")
                print(f"Cost: {segment.cost}")
                print("-" * 20)

    # Loads network from file, to call: NetworkSystem.load_network(insert filename)
    # Validates the file formatting
    # Returns a NetworkSystem object
    @classmethod
    def load_network(cls, filename="network.txt"):
        delimiter = ', '
        file_path = os.path.join(os.path.dirname(__file__), filename)

        try:
            with open(file_path, "r") as file:
                contents = file.readlines()
        except FileNotFoundError as e:
            raise NetworkLoadError(f"File '{filename}' was not found.") from e
        except PermissionError as e:
            raise NetworkLoadError(f"Permission denied while opening '{filename}'.") from e
        except OSError as e:
            raise NetworkLoadError(f"Could not open '{filename}': {e}") from e

        if not contents:
            raise NetworkFormatError("The network file is empty.")

        first_line = contents[0].strip().split(delimiter)
        if not cls.validate_first_line(first_line):
            raise NetworkFormatError(
                "The first line must contain exactly 3 positive integers: "
                "<number of vertices>, <number of transport modes>, <number of path blocks>."
            )

        vertices_count, transport_count, path_count = map(int, first_line)
        expected_lines = 1 + vertices_count + transport_count + path_count
        if len(contents) < expected_lines:
            raise NetworkFormatError(
                "The file does not contain enough lines based on the counts in the first line."
            )

        vertices = [l.strip() for l in contents[1: vertices_count + 1]]
        transport_modes = [l.strip() for l in contents[vertices_count + 1: transport_count + vertices_count + 1]]

        if not cls.validate_list(vertices, delimiter):
            raise NetworkValidationError(
                "The list of vertices contains an empty line, a duplicate entry or an invalid delimiter."
            )

        if not cls.validate_list(transport_modes, delimiter):
            raise NetworkValidationError(
                "The list of transport modes contains an empty line, a duplicate entry or an invalid delimiter."
            )

        segments = []
        remaining_lines = contents[transport_count + vertices_count + 1:]

        subpaths = 0
        bidirectional = 0
        start = ""
        dest = ""
        main_paths_read = 0

        for line_number, raw_line in enumerate(
            remaining_lines,
            start=vertices_count + transport_count + 2
        ):
            line = raw_line.strip().split(delimiter)

            # If main path
            if subpaths == 0:
                if main_paths_read >= path_count:
                    raise NetworkFormatError(
                        f"Unexpected extra content found at line {line_number}."
                    )

                if not cls.validate_path_line(line, vertices):
                    raise NetworkValidationError(
                        f"Invalid path line at line {line_number}: '{raw_line.strip()}'."
                    )

                start, dest, bidirectional, subpaths = line
                bidirectional = int(bidirectional)
                subpaths = int(subpaths)
                main_paths_read += 1

            # If subpath
            else:
                if not cls.validate_subpath_line(line, transport_modes):
                    raise NetworkValidationError(
                        f"Invalid subpath line at line {line_number}: '{raw_line.strip()}'."
                    )

                new_seg = Seg(start, dest, line[0], int(line[1]), int(line[2]))
                segments.append(new_seg)

                if bidirectional:
                    new_seg = Seg(dest, start, line[0], int(line[1]), int(line[2]))
                    segments.append(new_seg)

                subpaths -= 1

        if subpaths > 0:
            raise NetworkFormatError(
                "The file ended before all declared subpaths were provided."
            )

        if main_paths_read != path_count:
            raise NetworkFormatError(
                "The number of main path blocks does not match the number declared in the first line."
            )

        return cls(vertices, transport_modes, segments)

    # For all these validation methods I am assuming a list of strings
    # Because file contents are strings

    @staticmethod
    def validate_first_line(line: list):
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
    def validate_list(lst: list, delimiter: str):
        # Delimiter in any line
        if not all([delimiter not in x for x in lst]):
            return False

        # Any line is empty
        if not all([x.strip() for x in lst]):
            return False
        
        # Any duplicates (not case sensitive)
        if not (len(set(map(lambda x: x.lower(), lst))) == len(lst)):
            return False

        return True

    @staticmethod
    def validate_path_line(line: list, vertices: list):
        # Not 4 items
        if len(line) != 4:
            return False

        # First two parts aren't vertices
        if not (line[0] in vertices and line[1] in vertices):
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

        # Negative cost/time (zero is allowed here)
        if int(line[1]) < 0 or int(line[2]) < 0:
            return False

        return True


if __name__ == "__main__":
    main()