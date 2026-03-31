# I will continue this on Thursday cos I realised that I have an urgent essay to do

#TODO: import ezeikel code
from sys import exit
PREFERENCE_MODES = ["Distance", "Cost", "Segments"]
TRANSPORT_MODES = ["MTR", "Bus", "Walking"]

def main():
    pass

# This class is the main menu and stores stuff
class MenuPage:
    def __init__(self):
        self.network = None # network object
        self.options = {
            "avoid_modes" : [],
            "max_budget": 0,
            "max_segments": 0,
            "preferred_modes": []
        } # this is a dictionary

    def mainloop(self):
        MAIN_MENU_OPTIONS = ["Upload Map", "Plan Route", "Change Settings", "Help", "Exit"]
        USER_PROMPT = "Welcome to transport advisor."

        while True:
            interface = prompt_input_variable(USER_PROMPT, MAIN_MENU_OPTIONS)

            match interface.lower():

                case "upload map":
                    self.upload_network()
                
                case "plan route":
                    pass # carl code

                case "change settings":
                    self.change_setting()
                
                case "help":
                    self.print_help()

    def change_setting(self):
        pass

    def print_help(self):
        print("placeholder TODO: CHANGE THIS")

    def upload_network(self):
        pass

    def exit(self):
        print("Exiting program.")
        exit(0)

# Gets user to input variable value and return it
def prompt_input_variable(user_prompt: str, valid_options: list,
                          multiple: bool =False, delimiter: str =" ",
                          case_sensitive: bool=False, input_prompt : str=">>> "):
    
    # Prompt the user for input
    print(user_prompt)

    if multiple:
        print(f"Input one or more options delimited by \"{delimiter}\".")
    
    if case_sensitive:
        print("Valid options include (case sensitive):")
    else:
        print("Valid options include:")

    for option in valid_options:
        print(f"->{option}")

    # Get user input and validate it
    is_valid = False
    
    # If not case_sensitive, set all valid options to lowercase
    if not case_sensitive:
        valid_options = [option.lower() for option in valid_options]

    while not is_valid:
        
        user_input = input(input_prompt)

        # Validate the input
        if not multiple:
            is_valid = user_input in valid_options if case_sensitive else user_input.lower() in valid_options
        else:
            user_input = user_input.split(delimiter)
            if case_sensitive:
                is_valid = all([item in valid_options for item in user_input])
            else:
                is_valid = all([item.lower() in valid_options for item in user_input])
    
    # Return value: string if not multiple, list of strings if multiple
    return user_input

main()