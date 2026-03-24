PREFERENCE_MODES = ['Distance', 'Cost', 'Segments']
TRANSPORT_MODES = ['MTR', 'Bus', 'Walking']

def main():
    pass

# Gets user to input variable value and return it
def prompt_input_variable(user_prompt: str, valid_options: list,
                          multiple: bool =False, delimiter: str =' ',
                          case_sensitive: bool=False, input_prompt : str='>>> '):
    
    # Prompt the user for input
    print(user_prompt)

    if multiple:
        print(f'Input one or more options delimited by \'{delimiter}\'.')
    
    if case_sensitive:
        print('Valid options include (case sensitive):')
    else:
        print('Valid options include:')
    print('\n'.join(valid_options))

    # Get user input and validate it
    is_valid = False
    
    # If not case_sensitive, set all valid options to lowercase
    if not case_sensitive:
        valid_options = [option.lower() for option in valid_options]

    while not is_valid:
        #
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