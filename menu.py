from pathprint import print_path
# 2/4/2026 update:
# Grouped menu functionality together into the menu class
# Removed data storage functionality of the menu class
# I intend for the menu class to loop indefinitely, prompt the user for an option and runs a corresponding function


# https://stackoverflow.com/questions/34997241/a-list-comprehension-of-lambdas-returns-the-same-values
# Dummy example, the functions in this dict print the labels
# I will likely remove main and this later cos this is just a proof of concept
MENU_OPTIONS = ["New Game", "Load Game", "Settings", "Help"]
OPTIONS_DICT = {label:lambda label=label: print(f"TODO: {label}") for label in MENU_OPTIONS}


# Example use of the menu object for a dummy game menu
# MenuPage takes a dict of string:function, other parameters are optional
def main():
    main_menu = MenuPage(OPTIONS_DICT, "The very cool RPG game")
    main_menu.mainloop()

# This class is for menu pages where the user is prompted to choose from several options
class MenuPage:
    # valid_options is inteded to be a dict of string : function
    def __init__(self, valid_options: dict, user_prompt: str ="",
                        multiple: bool =False, delimiter: str ="/",
                        case_sensitive: bool=False, has_return: bool=True):
        
        self.valid_options = valid_options
        self.user_prompt = user_prompt
        self.multiple = multiple
        self.delimiter = delimiter
        self.case_sensitive = case_sensitive
        
        # has_return: there exists a "Return option that breaks out of the mainloop"
        if has_return:
            self.valid_options["Return"] = None
        
        # These are the options that are printed
        self.visual_options = self.valid_options.keys()
        
        # Set keys of valid options to lowercase if not case_sensitive
        if not case_sensitive:
            self.valid_options = {label.lower():func for label, func in self.valid_options.items()}

    # Loop menu indefinitely, include options like "return"/"exit"?
    def mainloop(self):

        while True:
            # Prompt and read user input
            self.prompt_options()
            user_choice = self.get_user_input()
            
            # Break the loop immediately if return is in any part of user input
            if self.multiple:
                if "return" in [choice.lower() for choice in user_choice]:
                    print("Returning to previous page...")
                    print("(If other options were selected, they will be disregarded)")
                    break
            elif user_choice.lower() == "return":
                print("Returning to previous page...")
                break

            # Execute function(s) associated with choice
            # https://stackoverflow.com/questions/624926/how-do-i-detect-whether-a-variable-is-a-function
            if not self.multiple:
                self.run_function(user_choice)
            else:
                for choice in user_choice:
                    self.run_function(choice)
    
    # Get and run functions given a label
    def run_function(self, label):
        function = self.valid_options.get(label)
        if callable(function):
            function()

    # ask user for start/end, then run Dijkstra and print the route
    def plan_route(self):
        if self.network_system is None:
            print("Upload Map first")
            return

        start = input("Start: ").strip()
        end = input("End: ").strip()

        print_path(self.network_system, start, end)

    # Gets user to input variable value and return it
    def prompt_options(self):
        
        # Prompt the user for input (if any)
        if self.user_prompt:
            print(self.user_prompt)
    
        if self.multiple:
            print(f"Input one or more options delimited by \"{self.delimiter}\".")
        
        if self.case_sensitive:
            print("Valid options include (case sensitive):")
        else:
            print("Valid options include:")
    
        for option in self.visual_options:
            print(f"-> {option}")
    
    # Repeatedly read user input until it is valid
    def get_user_input(self):
        is_valid = False

        while not is_valid:
            
            user_input = input(">>> ")

            user_input = user_input if self.case_sensitive else user_input.lower()
    
            # Validate the input
            if not self.multiple:
                is_valid = user_input in self.valid_options.keys()
            else:
                user_input = user_input.split(self.delimiter)
                in_options = all([item in self.valid_options.keys() for item in user_input])
                is_unique = (len(user_input) == len(set(user_input)))
                is_valid = in_options and is_unique
        
        print()

        # Return value: string if not multiple, list of strings if multiple
        # The return value(s) will be in lowercase if not case_sensitive
        return user_input

if __name__ == "__main__":
    main()
