# Implementation of the menus used
# TO MY TEAMMATES: focus on the functions build_all_menus, build_main_menu and build_settings_menu
# (yes this is hardcoding im sorry)
from menu import MenuPage
from sys import exit

# This file is just for buildling the menus, I will likely remove this main, this is for testing
def main():
    main_menu = build_all_menus()
    main_menu.mainloop()

# Builds all menus, returns only the main menu
def build_all_menus():
    settings_menu = build_settings_menu()
    main_menu = build_main_menu(settings_menu) # Idk what I'm doing with the function scope anymore
    return main_menu

def build_main_menu(settings_menu):
    # Function implementations of various functions go in options_dict
    options_dict = {
        "Upload Map" : None, # your implementations go here, replace the "None"
        "Plan Route" : None,
        "Change Settings" : settings_menu.mainloop, # enter settings menu
        "Help" : print_help_main,
        "Quit" : quit_program
    }

    main_menu = MenuPage(
        options_dict,
        user_prompt="~~ Welcome to transport advisor ~~",
        has_return=False
    )

    return main_menu

# I still have not decided what to print here
def print_help_main():
    print("TODO: IMPLEMENT INSTRUCTIONS IN HELP")
    print("This transport advisor helps you find the best route given certain conditions (which can be adjusted in settings).")
    print("~~ Main Menu Options ~~")
    print("Upload Map: TODO EXPLANATION")
    print("Plan Route: TODO EXPLANATION")
    print("Change Settings: There is a help page within the settings menu that will explain the settings.")
    print("Help: Print this page.")
    print("Quit: Exit the program.")
    print()

def quit_program():
    print("~~ See you next time ~~")
    exit(0)

def build_settings_menu():
    options_dict = {
        # ref to Ezekiel's part: preferences are cheapest, fastest, fewest
        "Set Preference" : None,
        "Set Avoid Modes" : None,
        "Set Preferred Modes" : None,
        "Set Max Budget" : None,
        "Set Max Segments" : None,
        "Help": print_help_settings,
    }
    
    settings_menu = MenuPage(
        options_dict,
        user_prompt="~~ Settings ~~",
    )

    return settings_menu

def print_help_settings():
    print("~~ Options in Settings ~~")
    print("Preference: choose whether the best route is determined by being the cheapest, fastest or having the fewest segments.")
    print("Set Avoid Modes: Set which modes of transport to avoid.")
    print("Set Preferred Modes: Set which modes of transport to prioritise.")
    print("Set Max Budget: Set the maximum price for a valid route.")
    print("Set Max Segments: Set the maximum number of segments for a valid route.")
    print("Help: Print this page.")
    print("Return: Returns to the main menu.")
    print()

if __name__ == '__main__':
    main()