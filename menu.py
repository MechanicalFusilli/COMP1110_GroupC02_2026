# 2/4/2026 2am update:
# Grouped menu functionality together into the menu class
# Removed data storage functionality of the 
# I might split off the hard coded implementations of menus (e.g. the main menu) into another file
PREFERENCE_MODES = ["Distance", "Cost", "Segments"]
TRANSPORT_MODES = ["MTR", "Bus", "Walking"]
MAIN_MENU_OPTIONS = ["Upload Map", "Plan Route", "Change Settings", "Help", "Exit"]

def main():
    MAIN_MENU_OPTIONS_DICT = {x:print for x in MAIN_MENU_OPTIONS}
    main_menu = MenuPage(MAIN_MENU_OPTIONS_DICT, "Welcome to transport advisor.")
    main_menu.mainloop()

# This class is for menu pages where the user is prompted to choose from several options
class MenuPage:
    # valid_options is inteded to be a dict of string : function
    def __init__(self, valid_options: dict, user_prompt: str ="",
                        multiple: bool =False, delimiter: str =" ",
                        case_sensitive: bool=False):
        
        self.valid_options = valid_options
        self.user_prompt = user_prompt
        self.multiple = multiple
        self.delimiter = delimiter
        self.case_sensitive = case_sensitive
        
        # This list is for direct comparison in validation, entirely lowercase if not case sensitive
        self.checked_options = self.valid_options.keys() if self.case_sensitive \
        else [option.lower() for option in self.valid_options]

    # Loop menu indefinitely, include options like "return"/"exit"?
    def mainloop(self):
        while True:
            self.prompt_options()
            user_choice = self.get_user_input()

            # TODO: split this off and not hardcode the options
            match user_choice.lower():
                case "upload map":
                    print("TODO: UPLOAD MAP")
                
                case "plan route":
                    print("TODO: PLAN ROUTE")

                case "change settings":
                    print("TODO: CHANGE SETTINGS")
                
                case "help":
                    print("TODO: HELP")

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
    
        for option in self.valid_options.keys():
            print(f"-> {option}")
    
    # Repeatedly read user input until it is valid
    def get_user_input(self):
        is_valid = False

        while not is_valid:
            
            user_input = input(">>> ")

            user_input = user_input if self.case_sensitive else user_input.lower()
    
            # Validate the input
            if not self.multiple:
                is_valid = user_input in self.checked_options
            else:
                user_input = user_input.split(self.delimiter)
                is_valid = all([item in self.checked_options for item in user_input])
        
        # Return value: string if not multiple, list of strings if multiple
        return user_input

if __name__ == "__main__":
    main()