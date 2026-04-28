# Implementation of the menus used
# (yes this is hardcoding I'm sorry)
from menu import MenuPage
from network_system import NetworkSystem
from sys import exit
from Pathprint import print_path
from djikstras import startfind

# This file is just for buildling the menus, I will likely remove this main, this is for testing
def main():
    MenuSystem()

# Effectively using classes as an excuse to have global variables
# All of the menus in this
class MenuSystem:
    def __init__(self):
        # network system will uploaded through Upload Map
        self.network_system = None
        self.start = None
        self.end = None
        self.build_all_menus()
        self.main_menu.mainloop()

    def build_all_menus(self):
        # Special cases here because they depends on the existence of network_system
        self.start_menu = None
        self.end_menu = None
        self.avoid_modes_menu = None
        
        self.build_preference_menu()
        self.build_settings_menu()
        self.build_main_menu()
    
    def build_avoid_modes_menu(self):

        def set_preference(option):
            avoid_modes = self.network_system.settings["avoid_modes"]

            # Avoiding duplicates
            if option in avoid_modes:
                print("\033[31m" + f"{option} was already avoided" + "\033[0m")
            else:
                avoid_modes.append(option)
                print("\033[32m" + f"Successfully added {option} to avoided modes" + "\033[0m")
                # Build avoids mode menu without these in case menu is entered again
                self.build_avoid_modes_menu()
            
        # Filter out options that are already avoided
        options = [m for m in self.network_system.transport_modes if m not in self.network_system.settings["avoid_modes"]]
        options_dict = {option: (lambda option=option: set_preference(option)) for option in options}

        self.avoid_modes_menu = MenuPage(
            options_dict,
            user_prompt="~~ Set Avoid Modes ~~",
            multiple=True,
            auto_return=True,
        )
    
    def build_end_menu(self):
        def set_end(end):
            if self.network_system.settings["start"] == end:
                print("\033[31m" + f"Failed to set destination because {end} was set as start" + "\033[0m")
                return
            self.network_system.settings["end"] = end
            print("\033[32m" + f"Set {end} as the destination." + "\033[0m")
        
        options_dict = {option: (lambda option=option: set_end(option)) for option in self.network_system.vertices}
        self.end_menu = MenuPage(
            options_dict,
            user_prompt="~~ Set end ~~~",
            auto_return=True,
        )

    def build_main_menu(self):
        # Function implementations of various functions go in options_dict
        options_dict = {
            "Upload Map": self.upload_map,
            "Plan Route": self.plan_route,
            "Change Settings": self.settings_menu.mainloop,
            "Help": lambda: self.print_help("main_menu_help.txt"),
            "Quit": self.quit_program
        }
    
        self.main_menu = MenuPage(
            options_dict,
            user_prompt="~~ Welcome to transport advisor ~~",
            has_return=False
        )
    
    def build_preference_menu(self):

        # Will be called whenever an option is selected
        def set_preference(num: int):
            self.network_system.settings["preference"] = num
            print("\033[32m" + "Set successfully." + "\033[0m")

        options_dict = {
            "Cheapest": lambda: set_preference(0),
            "Fastest": lambda: set_preference(1),
            "Fewest": lambda: set_preference(-1),
        }

        self.preference_menu = MenuPage(
            options_dict,
            user_prompt="~~ Set Preference ~~",
            auto_return=True,
        )
    
    def build_start_menu(self):
        def set_start(start):
            if self.network_system.settings["end"] == start:
                print("\033[31m" + f"Failed to set start because {start} was set as end" + "\033[0m")
                return
            self.network_system.settings["start"] = start
            print("\033[32m" + f"Set {start} as the starting point." + "\033[0m")
        
        options_dict = {option: (lambda option=option: set_start(option)) for option in self.network_system.vertices}
        self.start_menu = MenuPage(
            options_dict,
            user_prompt="~~ Set start ~~~",
            auto_return=True,
        )

    def build_settings_menu(self):
        options_dict = {
            "Set Start": lambda: self.enter_assignment_menu(self.start_menu),
            "Set End": lambda: self.enter_assignment_menu(self.end_menu),
            "Set Preference": lambda: self.enter_assignment_menu(self.preference_menu),
            "Set Avoid Modes": lambda: self.enter_assignment_menu(self.avoid_modes_menu),
            "Clear Preferences": self.clear_settings,
            "Print Settings": self.print_settings,
            "Help": lambda: self.print_help("settings_menu_help.txt"),
        }
        
        self.settings_menu = MenuPage(
            options_dict,
            user_prompt="~~ Settings ~~",
        )

    def clear_settings(self):
        if self.network_system == None:
            print("\033[33m" + "Upload Map to set settings" + "\033[0m")
            return
        
        self.network_system.settings["avoid_modes"] = []
        self.network_system.settings["start"] = None
        self.network_system.settings["end"] = None
        print("\033[32m" + "Cleared all settings" + "\033[0m")

        self.build_avoid_modes_menu()
    
    def enter_assignment_menu(self, menu):
        if self.network_system == None or menu == None:
            print("\033[33m" + "Upload Map to set settings" + "\033[0m")
            return
        
        menu.mainloop()
    
    def plan_route(self):
        if self.network_system is None:
            print("\033[33m" + "Upload Map first" + "\033[0m")
            return

        if self.network_system.settings["start"] is None or self.network_system.settings["end"] is None:
            print("\033[33m" + "Set start and end first" + "\033[0m")
            return

        try:
            routes = startfind(
                self.network_system.settings["start"],
                self.network_system.settings["end"],
                self.network_system.settings["preference"],
                self.network_system.settings["avoid_modes"],
                self.network_system.adjacency_list
            )

            print_path(routes)

        except Exception as e:
            print("\033[31m" + f"Could not plan route: {e}" + "\033[0m")

    # Print whatever help page is there
    def print_help(self, filepath):
        with open(filepath, "r") as file:
            help_content = file.read()
        
        print(help_content)

    def print_settings(self):
        if self.network_system == None:
            print("\033[33m" + "Upload Map in main menu to display settings\n" + "\033[0m")
            return
        
        settings = self.network_system.settings
        print("~~ Current Settings ~~")

        print(f"Start: {settings['start']}")
        print(f"End: {settings['end']}")

        print("Preference:")
        p = {0: "cost", 1: "distance", -1: "segments"}.get(settings.get("preference"))
        print(f"Path is optimised by {p}")

        print("Avoided Modes:")
        if not settings.get("avoid_modes"):
            print("None")
        else:
            for mode in settings.get("avoid_modes"):
                print(mode)
        
        print()

    @staticmethod
    def quit_program():
        print("\033[32m" + "~~ See you next time ~~" + "\033[0m")
        exit(0)
    
    def upload_map(self):
        print("\033[33m" + "Input filename:" + "\033[0m")
        filename = input(">>> ")
        print()

        try:
            self.network_system = NetworkSystem.load_network(filename)

            print("\033[32m" + "Successfully set network" + "\033[0m")
            self.build_avoid_modes_menu()
            self.build_start_menu()
            self.build_end_menu()

        except Exception as e:
            self.network_system = None
            print("\033[31m" + f"There was a problem in setting the network: {e}" + "\033[0m")

if __name__ == '__main__':
    main()