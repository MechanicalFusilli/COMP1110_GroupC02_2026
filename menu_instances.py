# Implementation of the menus used
# (yes this is hardcoding I'm sorry)
from menu import MenuPage
from sys import exit

# This file is just for buildling the menus, I will likely remove this main, this is for testing
def main():
    MenuSystem()

# Effectively using classes as an excuse to have global variables
# All of the menus in this
class MenuSystem:
    def __init__(self, network_system):
        # network system is inteded to contain information about the network
        # and it also makes the adjacency list that Carl's djikstra needs
        # this is the main thing that I will be doing later
        self.network_system = network_system
        self.build_all_menus()
        self.main_menu.mainloop()

    def build_all_menus(self):
        self.build_settings_menu()
        self.build_main_menu()

    def build_main_menu(self):
        # Function implementations of various functions go in options_dict
        options_dict = {
            "Upload Map" : None, # I will hook up the implementations here later
            "Plan Route" : None,
            "Change Settings" : self.settings_menu.mainloop, # enter settings menu
            "Help" : lambda: self.print_help("main_menu_help.txt"),
            "Quit" : self.quit_program
        }
    
        self.main_menu = MenuPage(
            options_dict,
            user_prompt="~~ Welcome to transport advisor ~~",
            has_return=False
        )
    
    def build_settings_menu(self):
        options_dict = {
            # ref to Carl's part: preferences are cheapest, fastest, fewest
            # I'll do this later
            "Set Preference" : None, # This should be a number
            "Set Avoid Modes" : None, # This should be a list of banned modes
            "Help": lambda: self.print_help("settings_menu_help.txt"),
        }
        
        self.settings_menu = MenuPage(
            options_dict,
            user_prompt="~~ Settings ~~",
        )
    
    # Print whatever help page is there
    def print_help(self, filepath):
        with open(filepath, "r") as file:
            help_content = file.read()
        
        print(help_content)

    def quit_program():
        print("~~ See you next time ~~")
        exit(0)

if __name__ == '__main__':
    main()