from menu import MenuPage
from sys import exit

# Main menu example for our program
# I will likely remove this main, this file is just for buildling the menus
def main():
    main_menu = build_main_menu()
    main_menu.mainloop()

def build_main_menu():
    # Function implementations of various functions go in options_dict
    options_dict = {
        "Upload Map" : None,
        "Plan Route" : None,
        "Change Settings" : None,
        "Help" : print_help,
        "Quit" : lambda: exit(0)
    }

    main_menu = MenuPage(
        options_dict,
        user_prompt="Welcome to transport advisor",
        has_return=False
    )

    return main_menu

# Incomplete help function
# I still have not decided what to print here
def print_help():
    print("TODO: Help")
    print("Instructions will be implemented later")

if __name__ == '__main__':
    main()