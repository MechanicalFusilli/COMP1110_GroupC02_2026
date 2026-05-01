from Pathprint import print_path
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
    def __init__(self, valid_options: dict, user_prompt: str ="",
                        multiple: bool =False, delimiter: str ="/",
                        case_sensitive: bool=False, has_return: bool=True,
                        auto_return: bool=False):
        
        self.valid_options = valid_options
        self.user_prompt = user_prompt
        self.multiple = multiple
        self.delimiter = delimiter
        self.case_sensitive = case_sensitive
        self.auto_return = auto_return

        if has_return:
            self.valid_options["Return"] = None

        self.visual_options = list(self.valid_options.keys())

        # Store number choices
        self.number_map = {
            str(i + 1): label for i, label in enumerate(self.visual_options)
        }

        if not case_sensitive:
            self.valid_options = {
                label.lower(): func for label, func in self.valid_options.items()
            }

    def mainloop(self):
        while True:
            self.prompt_options()
            user_choice = self.get_user_input()

            if self.multiple:
                if "return" in [choice.lower() for choice in user_choice]:
                    print("\033[33mReturning to previous page...\033[0m")
                    break
            else:
                if user_choice.lower() == "return":
                    print("\033[33mReturning to previous page...\033[0m")
                    break

            if not self.multiple:
                self.run_function(user_choice)
            else:
                for choice in user_choice:
                    self.run_function(choice)

            if self.auto_return:
                print("\033[33mReturning to previous page...\033[0m")
                break

    def run_function(self, label):
        function = self.valid_options.get(label)

        if callable(function):
            function()

    def prompt_options(self):
        if self.user_prompt:
            print(self.user_prompt)

        if self.multiple:
            print(f"Input one or more options delimited by \"{self.delimiter}\".")

        print("Choose an option:")

        for i, option in enumerate(self.visual_options, 1):
            print(f"({i}) {option}")

    def get_user_input(self):
        while True:
            user_input = input(">>> ").strip()

            if not self.multiple:
                if user_input in self.number_map:
                    user_input = self.number_map[user_input]

                if not self.case_sensitive:
                    user_input = user_input.lower()

                if user_input in self.valid_options:
                    print()
                    return user_input

            else:
                parts = user_input.split(self.delimiter)
                converted = []
                valid = True

                for part in parts:
                    part = part.strip()

                    if part in self.number_map:
                        part = self.number_map[part]

                    if not self.case_sensitive:
                        part = part.lower()

                    if part not in self.valid_options:
                        valid = False
                        break

                    converted.append(part)

                if valid and len(converted) == len(set(converted)):
                    print()
                    return converted

            print("Invalid input. Please enter a valid number.")

if __name__ == "__main__":
    main()
