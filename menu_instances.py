# Implementation of the menus used
# (yes this is hardcoding I'm sorry)
from menu import MenuPage
from network_system import NetworkSystem
from sys import exit
from pathprint import print_path

# This file is just for buildling the menus, I will likely remove this main, this is for testing
def main():
    MenuSystem()

# Effectively using classes as an excuse to have global variables
# All of the menus in this
class MenuSystem:
    def __init__(self):
        # network system will uploaded through Upload Map
        self.network_system = None
        self.build_all_menus()
        self.main_menu.mainloop()

    def build_all_menus(self):
        # Special case here because this depends on the existence of network_system
        self.avoid_modes_menu = None
        
        self.build_preference_menu()
        self.build_settings_menu()
        self.build_main_menu()
    
    def build_avoid_modes_menu(self):

        def set_preference(option):
            avoid_modes = self.network_system.settings["avoid_modes"]

            # Avoiding duplicates
            if option in avoid_modes:
                print(f"{option} was already avoided")
            else:
                avoid_modes.append(option)
                print(f"Successfully added {option} to avoided modes")
                # Build avoids mode menu without these in case menu is entered again
                self.build_avoid_modes_menu()
            
        # Filter out options that are already avoided
        options = [m for m in self.network_system.transport_modes if not m in self.network_system.settings["avoid_modes"]]
        options_dict = {option:(lambda option=option: set_preference(option)) for option in options}

        self.avoid_modes_menu = MenuPage(
            options_dict,
            user_prompt="~~ Set Avoid Modes ~~",
            multiple=True
        )

    def build_main_menu(self):
        # Function implementations of various functions go in options_dict
        options_dict = {
            "Upload Map" : self.upload_map,
            "Plan Route" : self.plan_route,
            "Change Settings" : self.settings_menu.mainloop, # enter settings menu
            "Help" : lambda: self.print_help("main_menu_help.txt"),
            "Quit" : self.quit_program
        }
    
        self.main_menu = MenuPage(
            options_dict,
            user_prompt="~~ Welcome to transport advisor ~~",
            has_return=False
        )
    
    def build_preference_menu(self):

        # Will be called whenever an option is selected
        def set_preference(num : int):
            self.network_system.settings["preference"] = num
            print("Set successfully.")

        options_dict = {
            # ref to Carl's part: preferences are cheapest, fastest, fewest
            "Cheapest" : lambda: set_preference(0),
            "Fastest" : lambda: set_preference(1),
            "Fewest": lambda: set_preference(-1),
        }

        self.preference_menu = MenuPage(
            options_dict,
            user_prompt="~~ Set Preference ~~",
        )

    def build_settings_menu(self):
        options_dict = {
            "Set Preference" : lambda: self.enter_assignment_menu(self.preference_menu),
            "Set Avoid Modes" : lambda: self.enter_assignment_menu(self.avoid_modes_menu),
            "Clear Avoid Modes" : self.clear_avoid_modes,
            "Print Settings": self.print_settings,
            "Help": lambda: self.print_help("settings_menu_help.txt"),
        }
        
        self.settings_menu = MenuPage(
            options_dict,
            user_prompt="~~ Settings ~~",
        )
        
    # ask user for start/end, then run Dijkstra and print the route
    def plan_route(self):
        if self.network_system is None:
            print("Upload Map first")
            return

        start = input("Start: ").strip()
        end = input("End: ").strip()

        print_path(self.network_system, start, end)

    def clear_avoid_modes(self):
        # To prevent unexpected behaviour if no network_system
        if self.network_system == None:
            print("Upload Map to set settings")
            return
        
        self.network_system.settings["avoid_modes"] = []
        print("Cleared avoid modes")

        #Reset menu
        self.build_avoid_modes_menu()
    
    # An extra function is needed here because of undefined behaviour if network_system == None
    def enter_assignment_menu(self, menu):
        # To prevent unexpected behaviour if no network_system
        if self.network_system == None or menu == None:
            print("Upload Map to set settings")
            return
        
        menu.mainloop()

    # Print whatever help page is there
    def print_help(self, filepath):
        with open(filepath, "r") as file:
            help_content = file.read()
        
        print(help_content)
    
    def print_settings(self):

        # To prevent unexpected behaviour if no network_system
        if self.network_system == None:
            print("Upload Map in main menu to display settings\n")
            return
        
        settings = self.network_system.settings
        print("~~ Current Settings ~~")

        print("Preference:")
        p = {0:"cost", 1:"distance", -1:"segments"}.get(settings.get("preference"))
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
        print("~~ See you next time ~~")
        exit(0)
    
    def upload_map(self):
        print("Input filename:")
        filename = input(">>> ")
        print()

        self.network_system = NetworkSystem.load_network(filename)

        if self.network_system != None:
            print("Successfully set network")
            self.build_avoid_modes_menu()
        else:
            print("There was a problem in setting the network")

if __name__ == '__main__':
    main()
