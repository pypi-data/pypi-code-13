def prompt_user(prompt_message):
    return raw_input(prompt_message + "\n")

def get_string(message):
    user_input = prompt_user(message)
    # check if there is a string and if that string is made of only alpha characters or commas
    while user_input and not all(c.isalpha() or c.isspace() or c == "," for c in user_input) and user_input == " ":
        print("The value you entered is invalid. It should only contain letters, spaces and commas. Please try again\n")
        user_input = prompt_user(message)

    return user_input

def get_required_string(message):
    # Keep prompting the user if he enters nothing or the value is not a valid string
    user_input = prompt_user(message)

    while not all(c.isalpha() or c.isspace() or c == "," for c in user_input) or user_input == " " or not user_input:
        print("This is a required field that should only contain letters, spaces and commas. Please try again\n")
        user_input = prompt_user(message)
    return user_input

def check_in_range(message, min_value, max_value, default_value):
    # Get the user's input and keep prompting if the int value is out of range
    user_input = prompt_user(message)

    while user_input and int(user_input) not in range(min_value, max_value + 1):
        print("The value you provided is out of range. Sorry, try again\n")
        user_input = prompt_user(message)

    return user_input if user_input else default_value

def check_in_list(message, lst, input_type):
    # Get the user's input and check if it's in the list
    user_input = prompt_user(message)

    #check the type of user_input - if int, cast it to an int

    while user_input and user_input not in lst:
        print("The value you provided is incorrect. Please check the list above\n")
        user_input = prompt_user(message)

    return user_input

    # seek help in the chat about this issue (should I split it into two functions that will check for a string in the
    # list and check for an int in the list or should I make the check inside the function)
    # create two versions and show them to the peeps, see what they think






